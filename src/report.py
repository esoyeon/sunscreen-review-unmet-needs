"""
요약 리포트 생성 모듈

수집 결과를 분석하여 Markdown 리포트를 생성합니다.
"""

import os
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from collections import Counter

import pandas as pd

logger = logging.getLogger(__name__)


class ReportGenerator:
    """수집 결과 리포트 생성기"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Args:
            config: 설정 딕셔너리 (config.yaml에서 로드)
        """
        self.config = config
        output_config = config.get('output', {})
        self.report_dir = output_config.get('report_dir', 'report')
        os.makedirs(self.report_dir, exist_ok=True)
    
    def generate_summary(
        self,
        products: List[Dict[str, Any]],
        reviews: List[Dict[str, Any]],
        output_paths: Optional[Dict[str, str]] = None
    ) -> str:
        """
        수집 요약 리포트 생성
        
        Args:
            products: 상품 정보 리스트
            reviews: 리뷰 정보 리스트
            output_paths: 저장된 파일 경로 딕셔너리
            
        Returns:
            리포트 파일 경로
        """
        now = datetime.now()
        
        # 리뷰 DataFrame 생성
        reviews_df = pd.DataFrame(reviews) if reviews else pd.DataFrame()
        
        # 리포트 내용 생성
        lines = [
            "# 올리브영 선크림 리뷰 수집 요약 리포트",
            "",
            f"**수집 일시**: {now.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
            "## 1. 카탈로그 수집 결과",
            "",
            f"- **총 상품 수**: {len(products):,}개",
        ]
        
        # 브랜드별 통계
        if products:
            brands = Counter([p.get('brand', '알 수 없음') for p in products])
            top_brands = brands.most_common(10)
            lines.extend([
                f"- **브랜드 수**: {len(brands)}개",
                "",
                "### 상위 10개 브랜드",
                "",
                "| 브랜드 | 상품 수 |",
                "|--------|---------|",
            ])
            for brand, count in top_brands:
                lines.append(f"| {brand} | {count} |")
        
        lines.extend([
            "",
            "---",
            "",
            "## 2. 리뷰 수집 결과",
            "",
            f"- **총 리뷰 수**: {len(reviews):,}개",
        ])
        
        if not reviews_df.empty:
            # 리뷰 수집 대상 상품 수
            unique_products = reviews_df['goods_no'].nunique() if 'goods_no' in reviews_df.columns else 0
            lines.append(f"- **수집 상품 수**: {unique_products:,}개")
            
            # 정렬별 통계
            if 'sort_source' in reviews_df.columns:
                sort_counts = reviews_df['sort_source'].value_counts()
                lines.extend([
                    "",
                    "### 정렬별 리뷰 수",
                    "",
                    "| 정렬 기준 | 리뷰 수 |",
                    "|-----------|---------|",
                ])
                for sort_source, count in sort_counts.items():
                    lines.append(f"| {sort_source} | {count:,} |")
            
            # 평점 분포
            if 'rating' in reviews_df.columns:
                rating_counts = reviews_df['rating'].value_counts().sort_index()
                avg_rating = reviews_df['rating'].mean()
                lines.extend([
                    "",
                    "### 평점 분포",
                    "",
                    f"- **평균 평점**: {avg_rating:.2f}",
                    "",
                    "| 평점 | 리뷰 수 | 비율 |",
                    "|------|---------|------|",
                ])
                for rating, count in rating_counts.items():
                    pct = count / len(reviews_df) * 100
                    lines.append(f"| {rating} | {count:,} | {pct:.1f}% |")
            
            # 노이즈 태깅 결과
            lines.extend([
                "",
                "---",
                "",
                "## 3. 노이즈 태깅 결과",
                "",
            ])
            
            if 'is_trial' in reviews_df.columns:
                trial_count = reviews_df['is_trial'].sum()
                trial_pct = trial_count / len(reviews_df) * 100
                lines.append(f"- **체험단 리뷰 (is_trial=1)**: {trial_count:,}개 ({trial_pct:.1f}%)")
            
            if 'is_low_info' in reviews_df.columns:
                low_info_count = reviews_df['is_low_info'].sum()
                low_info_pct = low_info_count / len(reviews_df) * 100
                lines.append(f"- **저정보 리뷰 (is_low_info=1)**: {low_info_count:,}개 ({low_info_pct:.1f}%)")
            
            # 이미지 포함 리뷰
            if 'has_images' in reviews_df.columns:
                image_count = reviews_df['has_images'].sum()
                image_pct = image_count / len(reviews_df) * 100
                lines.append(f"- **이미지 포함 리뷰**: {image_count:,}개 ({image_pct:.1f}%)")
            
            # 날짜 분포 (가능 시)
            if 'review_date' in reviews_df.columns:
                dates = reviews_df['review_date'].dropna()
                if len(dates) > 0:
                    lines.extend([
                        "",
                        "---",
                        "",
                        "## 4. 리뷰 작성일 분포",
                        "",
                        f"- **최신 리뷰**: {dates.max()}",
                        f"- **가장 오래된 리뷰**: {dates.min()}",
                    ])
        
        # 출력 파일 정보
        if output_paths:
            lines.extend([
                "",
                "---",
                "",
                "## 5. 생성된 파일",
                "",
            ])
            for key, path in output_paths.items():
                lines.append(f"- `{key}`: `{path}`")
        
        # 리포트 저장
        report_content = '\n'.join(lines)
        report_path = os.path.join(self.report_dir, 'data_summary.md')
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        logger.info(f"리포트 생성: {report_path}")
        return report_path


def generate_report(
    config: Dict[str, Any],
    products: List[Dict[str, Any]],
    reviews: List[Dict[str, Any]],
    output_paths: Optional[Dict[str, str]] = None
) -> str:
    """
    리포트 생성 헬퍼 함수
    
    Args:
        config: 설정 딕셔너리
        products: 상품 정보 리스트
        reviews: 리뷰 정보 리스트
        output_paths: 저장된 파일 경로 딕셔너리
        
    Returns:
        리포트 파일 경로
    """
    generator = ReportGenerator(config)
    return generator.generate_summary(products, reviews, output_paths)
