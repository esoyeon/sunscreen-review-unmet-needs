"""
노이즈 태깅 모듈

리뷰에 is_trial, is_low_info 태그를 부여합니다.
원문은 보존하고 태그만 추가합니다.
"""

import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class NoiseFilter:
    """리뷰 노이즈 태깅 필터"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Args:
            config: 설정 딕셔너리 (config.yaml에서 로드)
        """
        self.config = config
        noise_config = config.get('noise_tagging', {})
        
        # is_trial 탐지 키워드
        self.trial_keywords = noise_config.get('trial_keywords', [
            '체험단', '증정', '제공받', '협찬', '이벤트',
            '무료', '선물', '샘플'
        ])
        
        # is_low_info 규칙
        low_info_config = noise_config.get('low_info', {})
        self.min_length = low_info_config.get('min_length', 15)
        self.delivery_keywords = low_info_config.get('delivery_keywords', [
            '배송', '포장', '사은품', '빠름', '빨라', '도착', '친절'
        ])
        
        # 정규식 패턴 컴파일
        self.trial_pattern = self._compile_pattern(self.trial_keywords)
        self.delivery_pattern = self._compile_pattern(self.delivery_keywords)
    
    def _compile_pattern(self, keywords: List[str]) -> re.Pattern:
        """키워드 리스트를 정규식 패턴으로 컴파일"""
        escaped = [re.escape(kw) for kw in keywords]
        pattern = '|'.join(escaped)
        return re.compile(pattern, re.IGNORECASE)
    
    def tag_trial(self, review: Dict[str, Any]) -> int:
        """
        체험단/협찬 리뷰 탐지
        
        Args:
            review: 리뷰 딕셔너리
            
        Returns:
            1 if trial review, 0 otherwise
        """
        text = review.get('review_text', '')
        review_type = review.get('review_type', '')
        
        # reviewType이 GIFT인 경우
        if review_type and review_type.upper() == 'GIFT':
            return 1
        
        # 텍스트에서 키워드 탐지
        if self.trial_pattern.search(text):
            return 1
        
        return 0
    
    def tag_low_info(self, review: Dict[str, Any]) -> int:
        """
        정보량 낮은 리뷰 탐지
        
        Args:
            review: 리뷰 딕셔너리
            
        Returns:
            1 if low info review, 0 otherwise
        """
        text = review.get('review_text', '')
        
        # 글자 수 체크 (공백 제외)
        text_stripped = re.sub(r'\s+', '', text)
        if len(text_stripped) < self.min_length:
            return 1
        
        # 배송/포장 위주 패턴만 포함하는지 체크
        # 배송 키워드가 있고, 제품 관련 내용이 없는 경우
        if self.delivery_pattern.search(text):
            # 제품 사용 경험 관련 키워드가 있는지 체크
            product_keywords = [
                '피부', '바르', '사용', '효과', '좋아', '마음', '추천',
                '촉촉', '건조', '자극', '향', '발림', '흡수', '커버',
                '톤업', '백탁', '끈적', '가벼', '무거', '썬크림', '자외선'
            ]
            product_pattern = re.compile('|'.join(product_keywords))
            
            # 제품 관련 키워드가 없으면 low_info
            if not product_pattern.search(text):
                return 1
        
        return 0
    
    def apply_tags(self, reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        리뷰 리스트에 노이즈 태그 적용
        
        Args:
            reviews: 리뷰 리스트
            
        Returns:
            태그가 적용된 리뷰 리스트 (원본 수정)
        """
        trial_count = 0
        low_info_count = 0
        
        for review in reviews:
            # is_trial 태깅
            is_trial = self.tag_trial(review)
            review['is_trial'] = is_trial
            trial_count += is_trial
            
            # is_low_info 태깅
            is_low_info = self.tag_low_info(review)
            review['is_low_info'] = is_low_info
            low_info_count += is_low_info
        
        logger.info(
            f"노이즈 태깅 완료: 총 {len(reviews)}개 리뷰 중 "
            f"is_trial={trial_count}개 ({trial_count/len(reviews)*100:.1f}%), "
            f"is_low_info={low_info_count}개 ({low_info_count/len(reviews)*100:.1f}%)"
        )
        
        return reviews


def apply_noise_tags(
    config: Dict[str, Any],
    reviews: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    노이즈 태깅 헬퍼 함수
    
    Args:
        config: 설정 딕셔너리
        reviews: 리뷰 리스트
        
    Returns:
        태그가 적용된 리뷰 리스트
    """
    noise_filter = NoiseFilter(config)
    return noise_filter.apply_tags(reviews)
