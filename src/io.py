"""
데이터 저장 모듈

수집된 데이터를 raw/processed 형식으로 저장합니다.
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

import pandas as pd

logger = logging.getLogger(__name__)


class DataIO:
    """데이터 입출력 관리자"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Args:
            config: 설정 딕셔너리 (config.yaml에서 로드)
        """
        self.config = config
        output_config = config.get('output', {})
        
        self.raw_dir = output_config.get('raw_dir', 'data/raw')
        self.processed_dir = output_config.get('processed_dir', 'data/processed')
        self.log_dir = output_config.get('log_dir', 'logs')
        self.report_dir = output_config.get('report_dir', 'report')
        
        # 디렉토리 생성
        for dir_path in [self.raw_dir, self.processed_dir, self.log_dir, self.report_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
        self.date_str = datetime.now().strftime('%Y%m%d')
    
    def save_products_jsonl(
        self, 
        products: List[Dict[str, Any]],
        filename: Optional[str] = None
    ) -> str:
        """
        상품 카탈로그를 JSONL로 저장
        
        Args:
            products: 상품 정보 리스트
            filename: 파일명 (기본: products_YYYYMMDD.jsonl)
            
        Returns:
            저장된 파일 경로
        """
        if filename is None:
            filename = f"products_{self.date_str}.jsonl"
        
        filepath = os.path.join(self.raw_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for product in products:
                # 저장용 데이터 정리
                save_data = {k: v for k, v in product.items() if not k.startswith('_')}
                f.write(json.dumps(save_data, ensure_ascii=False) + '\n')
        
        logger.info(f"상품 카탈로그 저장: {filepath} ({len(products)}개)")
        return filepath
    
    def save_reviews_jsonl(
        self, 
        reviews: List[Dict[str, Any]],
        filename: Optional[str] = None
    ) -> str:
        """
        리뷰를 JSONL로 저장
        
        Args:
            reviews: 리뷰 정보 리스트
            filename: 파일명 (기본: reviews_YYYYMMDD.jsonl)
            
        Returns:
            저장된 파일 경로
        """
        if filename is None:
            filename = f"reviews_{self.date_str}.jsonl"
        
        filepath = os.path.join(self.raw_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for review in reviews:
                # 저장용 데이터 정리 (_raw 등 내부 필드 제외)
                save_data = {k: v for k, v in review.items() if not k.startswith('_')}
                f.write(json.dumps(save_data, ensure_ascii=False) + '\n')
        
        logger.info(f"리뷰 저장: {filepath} ({len(reviews)}개)")
        return filepath
    
    def save_reviews_parquet(
        self, 
        reviews: List[Dict[str, Any]],
        filename: Optional[str] = None
    ) -> str:
        """
        리뷰를 Parquet으로 저장 (분석용)
        
        Args:
            reviews: 리뷰 정보 리스트
            filename: 파일명 (기본: reviews.parquet)
            
        Returns:
            저장된 파일 경로
        """
        if filename is None:
            filename = "reviews.parquet"
        
        filepath = os.path.join(self.processed_dir, filename)
        
        # 저장용 데이터 정리
        clean_reviews = []
        for review in reviews:
            save_data = {k: v for k, v in review.items() if not k.startswith('_')}
            clean_reviews.append(save_data)
        
        df = pd.DataFrame(clean_reviews)
        
        # 데이터 타입 정리
        if 'rating' in df.columns:
            df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        if 'helpful_count' in df.columns:
            df['helpful_count'] = pd.to_numeric(df['helpful_count'], errors='coerce').fillna(0).astype(int)
        if 'image_count' in df.columns:
            df['image_count'] = pd.to_numeric(df['image_count'], errors='coerce').fillna(0).astype(int)
        if 'is_trial' in df.columns:
            df['is_trial'] = df['is_trial'].astype(int)
        if 'is_low_info' in df.columns:
            df['is_low_info'] = df['is_low_info'].astype(int)
        
        df.to_parquet(filepath, index=False, engine='pyarrow')
        
        logger.info(f"리뷰 Parquet 저장: {filepath} ({len(reviews)}개)")
        return filepath
    
    def load_products_jsonl(self, filename: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        상품 카탈로그 JSONL 로드
        
        Args:
            filename: 파일명 (기본: 가장 최근 파일)
            
        Returns:
            상품 정보 리스트
        """
        if filename is None:
            # 가장 최근 파일 찾기
            files = [f for f in os.listdir(self.raw_dir) if f.startswith('products_') and f.endswith('.jsonl')]
            if not files:
                return []
            filename = sorted(files)[-1]
        
        filepath = os.path.join(self.raw_dir, filename)
        
        if not os.path.exists(filepath):
            return []
        
        products = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    products.append(json.loads(line))
        
        logger.info(f"상품 카탈로그 로드: {filepath} ({len(products)}개)")
        return products
    
    def load_reviews_jsonl(self, filename: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        리뷰 JSONL 로드
        
        Args:
            filename: 파일명 (기본: 가장 최근 파일)
            
        Returns:
            리뷰 정보 리스트
        """
        if filename is None:
            # 가장 최근 파일 찾기
            files = [f for f in os.listdir(self.raw_dir) if f.startswith('reviews_') and f.endswith('.jsonl')]
            if not files:
                return []
            filename = sorted(files)[-1]
        
        filepath = os.path.join(self.raw_dir, filename)
        
        if not os.path.exists(filepath):
            return []
        
        reviews = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    reviews.append(json.loads(line))
        
        logger.info(f"리뷰 로드: {filepath} ({len(reviews)}개)")
        return reviews


def save_data(
    config: Dict[str, Any],
    products: Optional[List[Dict[str, Any]]] = None,
    reviews: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, str]:
    """
    데이터 저장 헬퍼 함수
    
    Args:
        config: 설정 딕셔너리
        products: 상품 정보 리스트
        reviews: 리뷰 정보 리스트
        
    Returns:
        저장된 파일 경로 딕셔너리
    """
    io = DataIO(config)
    paths = {}
    
    if products:
        paths['products_jsonl'] = io.save_products_jsonl(products)
    
    if reviews:
        paths['reviews_jsonl'] = io.save_reviews_jsonl(reviews)
        paths['reviews_parquet'] = io.save_reviews_parquet(reviews)
    
    return paths
