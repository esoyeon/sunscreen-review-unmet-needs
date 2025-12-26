"""
리뷰 수집 모듈

올리브영 리뷰 API를 호출하여 정렬 기반 층화 표본으로 리뷰를 수집합니다.
"""

import time
import random
import hashlib
import logging
from typing import List, Dict, Any, Optional, Set
from datetime import datetime

import requests

logger = logging.getLogger(__name__)


class ReviewCollector:
    """올리브영 리뷰 수집기"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Args:
            config: 설정 딕셔너리 (config.yaml에서 로드)
        """
        self.config = config
        self.reviews_config = config.get('reviews', {})
        self.request_config = config.get('request', {})
        self.headers_config = config.get('headers', {})
        
        self.api_url = self.reviews_config.get(
            'api_url',
            'https://m.oliveyoung.co.kr/review/api/v2/reviews'
        )
        self.page_size = self.reviews_config.get('page_size', 10)
        
        # 정렬별 수집 수량
        self.sort_limits = self.reviews_config.get('sort_limits', {
            'helpful': 30,
            'newest': 20,
            'low_rating': 20,
            'high_rating': 10,
        })
        
        # sortType 매핑
        self.sort_types = self.reviews_config.get('sort_types', {
            'helpful': 'RECOMMENDED_DESC',
            'newest': 'DATETIME_DESC',
            'low_rating': 'RATING_ASC',
            'high_rating': 'RATING_DESC',
            'useful': 'USEFUL_SCORE_DESC',
        })
        
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
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': self.headers_config.get('accept_language', 'ko-KR,ko;q=0.9'),
            'Content-Type': 'application/json',
            'Origin': 'https://www.oliveyoung.co.kr',
            'Referer': 'https://www.oliveyoung.co.kr/',
        })
    
    def _random_delay(self) -> None:
        """랜덤 딜레이 적용"""
        delay = random.uniform(self.delay_min, self.delay_max)
        time.sleep(delay)
    
    def _generate_review_id(self, review_data: Dict[str, Any], goods_no: str) -> str:
        """
        리뷰 고유 ID 생성 (API에서 제공하거나 해시 생성)
        
        Args:
            review_data: 리뷰 원본 데이터
            goods_no: 상품 번호
            
        Returns:
            리뷰 ID 문자열
        """
        # API에서 reviewId 제공 시 사용
        if 'reviewId' in review_data:
            return str(review_data['reviewId'])
        
        # 해시 생성 (상품번호 + 내용 + 날짜)
        content = review_data.get('content', '')
        date = review_data.get('createdDateTime', '')
        hash_input = f"{goods_no}_{content}_{date}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:16]
    
    def _fetch_reviews(
        self, 
        goods_no: str, 
        sort_type: str, 
        page: int = 0
    ) -> Optional[Dict[str, Any]]:
        """
        리뷰 API 호출
        
        Args:
            goods_no: 상품 번호
            sort_type: 정렬 타입 (API 값)
            page: 페이지 번호 (0부터 시작)
            
        Returns:
            API 응답 딕셔너리 또는 None
        """
        payload = {
            'goodsNumber': goods_no,
            'page': page,
            'size': self.page_size,
            'sortType': sort_type,
            'reviewType': 'ALL',
        }
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.post(
                    self.api_url,
                    json=payload,
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                logger.warning(
                    f"리뷰 요청 실패 (goods_no={goods_no}, sort={sort_type}, "
                    f"시도 {attempt + 1}/{self.max_retries}): {e}"
                )
                if attempt < self.max_retries - 1:
                    self._random_delay()
            except ValueError as e:
                logger.error(f"JSON 파싱 오류: {e}")
                return None
        
        return None
    
    def _parse_review(
        self, 
        review_data: Dict[str, Any], 
        goods_no: str,
        sort_source: str
    ) -> Dict[str, Any]:
        """
        리뷰 데이터를 표준 스키마로 변환
        
        Args:
            review_data: API 원본 리뷰 데이터
            goods_no: 상품 번호
            sort_source: 정렬 소스 (helpful, newest, etc.)
            
        Returns:
            표준화된 리뷰 딕셔너리
        """
        # 프로필 정보
        profile = review_data.get('profileDto', {}) or {}
        
        # 이미지 정보
        photo_list = review_data.get('photoReviewList', []) or []
        has_images = review_data.get('hasPhoto', False) or len(photo_list) > 0
        
        return {
            'review_id': self._generate_review_id(review_data, goods_no),
            'goods_no': goods_no,
            'product_id': goods_no,  # alias
            'sort_source': sort_source,
            'rating': review_data.get('reviewScore'),
            'review_date': review_data.get('createdDateTime'),
            'skin_type_raw': profile.get('skinType'),
            'skin_tone_raw': profile.get('skinTone'),
            'skin_trouble_raw': profile.get('skinTrouble'),
            'review_text': review_data.get('content', ''),
            'helpful_count': review_data.get('recommendCount') or review_data.get('usefulPoint', 0),
            'has_images': has_images,
            'image_count': len(photo_list),
            'review_type': review_data.get('reviewType'),  # GIFT, OFFLINE 등
            'is_trial': 0,  # 후처리에서 설정
            'is_low_info': 0,  # 후처리에서 설정
            'source': 'oliveyoung',
            '_raw': review_data,  # 원본 보존 (저장 시 제외 가능)
        }
    
    def collect_reviews_for_product(
        self, 
        goods_no: str,
        sort_sources: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        단일 상품의 리뷰 수집 (정렬별 층화 표본)
        
        Args:
            goods_no: 상품 번호
            sort_sources: 수집할 정렬 소스 리스트 (기본: 전체)
            
        Returns:
            수집된 리뷰 리스트 (중복 제거)
        """
        if sort_sources is None:
            sort_sources = ['helpful', 'newest', 'low_rating', 'high_rating']
        
        all_reviews: Dict[str, Dict[str, Any]] = {}  # review_id -> review
        
        for sort_source in sort_sources:
            if sort_source not in self.sort_types:
                logger.warning(f"알 수 없는 정렬 소스: {sort_source}")
                continue
            
            sort_type = self.sort_types[sort_source]
            limit = self.sort_limits.get(sort_source, 20)
            
            logger.debug(f"상품 {goods_no}: {sort_source} ({sort_type}) 수집 중...")
            
            collected = 0
            page = 0
            
            while collected < limit:
                response = self._fetch_reviews(goods_no, sort_type, page)
                
                if not response:
                    break
                
                # 응답 구조에 따라 리뷰 리스트 추출
                reviews_data = response.get('data', [])
                if not reviews_data:
                    reviews_data = response.get('content', [])
                if not reviews_data:
                    break
                
                for review_data in reviews_data:
                    if collected >= limit:
                        break
                    
                    review = self._parse_review(review_data, goods_no, sort_source)
                    review_id = review['review_id']
                    
                    # 중복 체크 (이미 수집된 리뷰면 sort_source 추가)
                    if review_id not in all_reviews:
                        all_reviews[review_id] = review
                        collected += 1
                    else:
                        # 다른 정렬에서도 등장한 리뷰 표시
                        existing = all_reviews[review_id]
                        if sort_source not in existing.get('sort_sources_all', [existing['sort_source']]):
                            existing.setdefault('sort_sources_all', [existing['sort_source']])
                            existing['sort_sources_all'].append(sort_source)
                
                # 다음 페이지
                if len(reviews_data) < self.page_size:
                    break
                
                page += 1
                self._random_delay()
            
            logger.debug(f"상품 {goods_no}: {sort_source} 완료 ({collected}개)")
            self._random_delay()
        
        return list(all_reviews.values())
    
    def collect_reviews_for_products(
        self,
        products: List[Dict[str, Any]],
        top_n: Optional[int] = None,
        sort_sources: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        여러 상품의 리뷰 수집
        
        Args:
            products: 상품 정보 리스트 (goods_no 포함)
            top_n: 상위 N개 상품만 수집 (list_rank 기준)
            sort_sources: 수집할 정렬 소스 리스트
            
        Returns:
            모든 수집된 리뷰 리스트
        """
        # list_rank로 정렬
        sorted_products = sorted(products, key=lambda x: x.get('list_rank', float('inf')))
        
        if top_n:
            sorted_products = sorted_products[:top_n]
        
        all_reviews = []
        total = len(sorted_products)
        
        logger.info(f"리뷰 수집 시작: {total}개 상품")
        
        for idx, product in enumerate(sorted_products):
            goods_no = product.get('goods_no')
            if not goods_no:
                continue
            
            logger.info(f"[{idx + 1}/{total}] 상품 {goods_no} 리뷰 수집 중...")
            
            try:
                reviews = self.collect_reviews_for_product(goods_no, sort_sources)
                all_reviews.extend(reviews)
                logger.info(f"[{idx + 1}/{total}] 상품 {goods_no}: {len(reviews)}개 리뷰 수집")
            except Exception as e:
                logger.error(f"상품 {goods_no} 리뷰 수집 실패: {e}")
                continue
            
            self._random_delay()
        
        logger.info(f"리뷰 수집 완료: 총 {len(all_reviews)}개 리뷰")
        return all_reviews


def collect_reviews(
    config: Dict[str, Any],
    products: List[Dict[str, Any]],
    top_n: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    리뷰 수집 헬퍼 함수
    
    Args:
        config: 설정 딕셔너리
        products: 상품 정보 리스트
        top_n: 상위 N개 상품만 수집
        
    Returns:
        수집된 리뷰 리스트
    """
    collector = ReviewCollector(config)
    return collector.collect_reviews_for_products(products, top_n)
