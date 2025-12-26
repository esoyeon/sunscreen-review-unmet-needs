"""
카탈로그 수집 모듈

올리브영 선크림 카테고리 페이지에서 전체 상품 목록을 수집합니다.
"""

import re
import time
import random
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class CatalogCollector:
    """올리브영 카탈로그 수집기"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Args:
            config: 설정 딕셔너리 (config.yaml에서 로드)
        """
        self.config = config
        self.catalog_config = config.get('catalog', {})
        self.request_config = config.get('request', {})
        self.headers_config = config.get('headers', {})
        
        self.base_url = self.catalog_config.get(
            'base_url', 
            'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do'
        )
        self.disp_cat_no = self.catalog_config.get('disp_cat_no', '100000100110006')
        self.prd_sort = self.catalog_config.get('prd_sort', '03')
        self.rows_per_page = self.catalog_config.get('rows_per_page', 48)
        
        self.delay_min = self.request_config.get('delay_min', 1.0)
        self.delay_max = self.request_config.get('delay_max', 2.0)
        self.max_retries = self.request_config.get('max_retries', 3)
        self.timeout = self.request_config.get('timeout', 30)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.headers_config.get(
                'user_agent',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            ),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': self.headers_config.get('accept_language', 'ko-KR,ko;q=0.9'),
        })
    
    def _random_delay(self) -> None:
        """랜덤 딜레이 적용"""
        delay = random.uniform(self.delay_min, self.delay_max)
        time.sleep(delay)
    
    def _fetch_page(self, page_idx: int) -> Optional[str]:
        """
        카탈로그 페이지 HTML 가져오기
        
        Args:
            page_idx: 페이지 번호 (1부터 시작)
            
        Returns:
            HTML 문자열 또는 None (실패 시)
        """
        params = {
            'dispCatNo': self.disp_cat_no,
            'prdSort': self.prd_sort,
            'pageIdx': page_idx,
            'rowsPerPage': self.rows_per_page,
        }
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(
                    self.base_url,
                    params=params,
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.warning(f"페이지 {page_idx} 요청 실패 (시도 {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    self._random_delay()
        
        logger.error(f"페이지 {page_idx} 수집 실패")
        return None
    
    def _parse_products(self, html: str, page_idx: int) -> List[Dict[str, Any]]:
        """
        HTML에서 상품 정보 파싱
        
        Args:
            html: 페이지 HTML
            page_idx: 현재 페이지 번호
            
        Returns:
            상품 정보 리스트
        """
        soup = BeautifulSoup(html, 'lxml')
        products = []
        
        # 상품 카드 선택
        items = soup.select('ul.cate_prd_list li, ul.main-four-guide-list li, div.prd_info')
        
        if not items:
            # 대체 셀렉터 시도
            items = soup.select('[data-ref-goodsno], .prd_info')
        
        for idx, item in enumerate(items):
            try:
                product = self._extract_product_info(item, page_idx, idx)
                if product and product.get('goods_no'):
                    products.append(product)
            except Exception as e:
                logger.debug(f"상품 파싱 오류: {e}")
                continue
        
        return products
    
    def _extract_product_info(
        self, 
        item, 
        page_idx: int, 
        index: int
    ) -> Optional[Dict[str, Any]]:
        """
        개별 상품 정보 추출
        
        Args:
            item: BeautifulSoup 요소
            page_idx: 페이지 번호
            index: 페이지 내 순서
            
        Returns:
            상품 정보 딕셔너리
        """
        # goodsNo 추출
        goods_no = None
        
        # data 속성에서 추출
        goods_no = item.get('data-ref-goodsno')
        
        # 링크에서 추출
        if not goods_no:
            link_elem = item.select_one('a[href*="goodsNo="]')
            if link_elem:
                href = link_elem.get('href', '')
                match = re.search(r'goodsNo=([A-Z0-9]+)', href)
                if match:
                    goods_no = match.group(1)
        
        if not goods_no:
            return None
        
        # 브랜드명
        brand_elem = item.select_one('.tx_brand, .brand, span[class*="brand"]')
        brand = brand_elem.get_text(strip=True) if brand_elem else ''
        
        # 상품명
        name_elem = item.select_one('.tx_name, .name, p[class*="name"], a[class*="name"]')
        name = name_elem.get_text(strip=True) if name_elem else ''
        
        # 가격
        price_elem = item.select_one('.tx_cur .tx_num, .price .num, span[class*="price"]')
        price_text = price_elem.get_text(strip=True) if price_elem else ''
        price = self._parse_price(price_text)
        
        # 상품 URL 생성
        product_url = f"https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo={goods_no}"
        
        # list_rank 계산 (페이지 * 페이지당개수 + 순서)
        list_rank = (page_idx - 1) * self.rows_per_page + index + 1
        
        return {
            'goods_no': goods_no,
            'product_id': goods_no,  # alias
            'brand': brand,
            'product_name': name,
            'price': price,
            'product_url': product_url,
            'list_rank': list_rank,
            'rating_avg': None,  # 카탈로그에서는 제공되지 않음
            'review_count': None,  # 카탈로그에서는 제공되지 않음
        }
    
    def _parse_price(self, price_text: str) -> Optional[int]:
        """가격 문자열을 정수로 변환"""
        if not price_text:
            return None
        # 숫자만 추출
        numbers = re.sub(r'[^\d]', '', price_text)
        return int(numbers) if numbers else None
    
    def _get_total_count(self, html: str) -> int:
        """총 상품 수 추출"""
        soup = BeautifulSoup(html, 'lxml')
        
        # "543개" 형태의 텍스트 찾기
        count_elem = soup.select_one('.cate_info_tx span, .total_count, [class*="count"]')
        if count_elem:
            text = count_elem.get_text()
            match = re.search(r'(\d+)', text)
            if match:
                return int(match.group(1))
        
        return 0
    
    def collect_all(self) -> List[Dict[str, Any]]:
        """
        전체 카탈로그 수집
        
        Returns:
            모든 상품 정보 리스트 (중복 제거됨)
        """
        all_products = []
        page_idx = 1
        total_count = 0
        
        logger.info("카탈로그 수집 시작...")
        
        while True:
            logger.info(f"페이지 {page_idx} 수집 중...")
            
            html = self._fetch_page(page_idx)
            if not html:
                logger.error(f"페이지 {page_idx} 수집 실패, 중단")
                break
            
            # 첫 페이지에서 총 개수 확인
            if page_idx == 1:
                total_count = self._get_total_count(html)
                logger.info(f"총 상품 수: {total_count}")
            
            products = self._parse_products(html, page_idx)
            
            if not products:
                logger.info(f"페이지 {page_idx}에서 상품 없음, 수집 완료")
                break
            
            all_products.extend(products)
            logger.info(f"페이지 {page_idx}: {len(products)}개 수집 (누적: {len(all_products)}개)")
            
            # 다음 페이지 확인
            if len(all_products) >= total_count * 2 or len(products) < self.rows_per_page:
                break
            
            page_idx += 1
            self._random_delay()
        
        # 중복 제거 (goods_no 기준, 먼저 등장한 것 유지)
        seen = set()
        unique_products = []
        for product in all_products:
            goods_no = product.get('goods_no')
            if goods_no and goods_no not in seen:
                seen.add(goods_no)
                unique_products.append(product)
        
        # list_rank 재계산 (중복 제거 후 순서대로)
        for idx, product in enumerate(unique_products):
            product['list_rank'] = idx + 1
        
        logger.info(f"카탈로그 수집 완료: 총 {len(unique_products)}개 상품 (중복 제거 후)")
        return unique_products


def collect_catalog(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    카탈로그 수집 헬퍼 함수
    
    Args:
        config: 설정 딕셔너리
        
    Returns:
        상품 정보 리스트
    """
    collector = CatalogCollector(config)
    return collector.collect_all()
