"""
Step 3-0: Baseline 전처리 스크립트

기존 reviews.parquet를 분석 가능한 베이스 테이블로 변환합니다.
원문(review_text)은 절대 수정하지 않고, 분석용 파생 컬럼만 추가합니다.

Usage:
    python -m src.processing.baseline --input data/processed/reviews.parquet --out data/processed/reviews_step3_base.parquet
"""

import argparse
import html
import logging
import os
import re
from datetime import datetime
from typing import Optional, Dict, Any

import pandas as pd
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =============================================================================
# Text Cleaning Functions
# =============================================================================

def clean_text(text: Optional[str]) -> str:
    """
    텍스트 정제 함수 (원문 의미 보존)
    
    1. HTML entity 디코딩
    2. 제어문자/탭 정리
    3. 연속 공백/줄바꿈 정리
    4. 앞뒤 공백 trim
    """
    if pd.isna(text) or not isinstance(text, str):
        return ""
    
    # 1. HTML entity 디코딩 (&#34;, &quot;, &amp; 등)
    result = html.unescape(text)
    
    # 2. 제어문자 정리 (\r -> \n, \t -> space)
    result = result.replace('\r\n', '\n').replace('\r', '\n')
    result = result.replace('\t', ' ')
    
    # 3. 연속 공백 정리 (2개 이상 -> 1개)
    result = re.sub(r' {2,}', ' ', result)
    
    # 4. 연속 줄바꿈 정리 (3개 이상 -> 2개)
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    # 5. 앞뒤 공백 trim
    result = result.strip()
    
    return result


# =============================================================================
# Date Parsing Functions
# =============================================================================

def parse_review_date(date_str: Optional[str]) -> Optional[datetime]:
    """
    리뷰 날짜 파싱 (다양한 형식 지원)
    
    지원 형식:
    - "2023.02.09"
    - "2023-02-09"
    - "2023/02/09"
    """
    if pd.isna(date_str) or not isinstance(date_str, str):
        return None
    
    date_str = date_str.strip()
    
    formats = [
        "%Y.%m.%d",
        "%Y-%m-%d",
        "%Y/%m/%d",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None


def get_season(month: Optional[int]) -> Optional[str]:
    """월 기준 계절 반환"""
    if month is None:
        return None
    
    if month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    elif month in [9, 10, 11]:
        return "fall"
    else:  # 12, 1, 2
        return "winter"


def get_rating_bucket(rating: Optional[int]) -> Optional[str]:
    """평점 구간 반환"""
    if pd.isna(rating):
        return None
    
    rating = int(rating)
    if rating <= 2:
        return "low"
    elif rating == 3:
        return "mid"
    else:  # 4, 5
        return "high"


# =============================================================================
# Main Preprocessing Class
# =============================================================================

class BaselinePreprocessor:
    """Baseline 전처리기"""
    
    def __init__(self, input_path: str, output_path: str, report_dir: str = "report"):
        self.input_path = input_path
        self.output_path = output_path
        self.report_dir = report_dir
        self.df: Optional[pd.DataFrame] = None
        self.stats: Dict[str, Any] = {}
    
    def load_data(self) -> None:
        """데이터 로드"""
        logger.info(f"Loading data from {self.input_path}")
        self.df = pd.read_parquet(self.input_path)
        logger.info(f"Loaded {len(self.df)} reviews")
    
    def normalize_schema(self) -> None:
        """스키마/타입 정규화"""
        logger.info("Normalizing schema...")
        
        # review_id, goods_no -> string
        if 'review_id' in self.df.columns:
            self.df['review_id'] = self.df['review_id'].astype(str)
        
        if 'goods_no' in self.df.columns:
            self.df['goods_no'] = self.df['goods_no'].astype(str)
        
        # rating -> int (1~5), 불가시 null
        if 'rating' in self.df.columns:
            original_count = self.df['rating'].notna().sum()
            self.df['rating'] = pd.to_numeric(self.df['rating'], errors='coerce')
            
            # 범위 체크 (1~5)
            invalid_mask = ~self.df['rating'].between(1, 5, inclusive='both') & self.df['rating'].notna()
            if invalid_mask.sum() > 0:
                logger.warning(f"Found {invalid_mask.sum()} ratings outside 1-5 range, setting to null")
                self.df.loc[invalid_mask, 'rating'] = np.nan
            
            # Int64로 변환 (nullable int)
            self.df['rating'] = self.df['rating'].astype('Int64')
            
            valid_count = self.df['rating'].notna().sum()
            logger.info(f"Rating normalization: {original_count} -> {valid_count} valid")
    
    def parse_dates(self) -> None:
        """날짜 파싱 및 시간 파생 컬럼 생성"""
        logger.info("Parsing dates...")
        
        # review_date_parsed 생성
        self.df['review_date_parsed'] = self.df['review_date'].apply(parse_review_date)
        
        # 파싱 성공률 계산
        total = len(self.df)
        parsed = self.df['review_date_parsed'].notna().sum()
        failed = total - parsed
        
        self.stats['date_parse_success'] = parsed
        self.stats['date_parse_failed'] = failed
        self.stats['date_parse_success_rate'] = parsed / total * 100 if total > 0 else 0
        
        logger.info(f"Date parsing: {parsed}/{total} succeeded ({self.stats['date_parse_success_rate']:.1f}%)")
        
        # 시간 파생 컬럼
        self.df['review_month'] = self.df['review_date_parsed'].apply(
            lambda x: x.strftime('%Y-%m') if pd.notna(x) else None
        )
        
        self.df['review_year'] = self.df['review_date_parsed'].apply(
            lambda x: x.year if pd.notna(x) else None
        ).astype('Int64')
        
        self.df['season'] = self.df['review_date_parsed'].apply(
            lambda x: get_season(x.month) if pd.notna(x) else None
        )
    
    def create_rating_bucket(self) -> None:
        """평점 파생 컬럼 생성"""
        logger.info("Creating rating bucket...")
        self.df['rating_bucket'] = self.df['rating'].apply(get_rating_bucket)
    
    def clean_text_column(self) -> None:
        """텍스트 정제 컬럼 생성"""
        logger.info("Cleaning text...")
        
        # review_text_clean 생성 (원문 보존)
        self.df['review_text_clean'] = self.df['review_text'].apply(clean_text)
        
        # 텍스트 길이/기초 지표
        self.df['text_len_chars'] = self.df['review_text_clean'].str.len().fillna(0).astype(int)
        self.df['text_len_words'] = self.df['review_text_clean'].apply(
            lambda x: len(x.split()) if isinstance(x, str) and x else 0
        )
        self.df['has_text'] = self.df['text_len_chars'] > 0
    
    def run_qa_checks(self) -> None:
        """QA 체크 실행"""
        logger.info("Running QA checks...")
        
        total = len(self.df)
        
        # 1. 총 리뷰 수, goods_no 수
        self.stats['total_reviews'] = total
        self.stats['unique_goods'] = self.df['goods_no'].nunique()
        
        # 2. review_id 중복 확인
        dup_ids = self.df[self.df.duplicated(subset=['review_id'], keep=False)]
        self.stats['duplicate_review_ids'] = len(dup_ids)
        if len(dup_ids) > 0:
            self.stats['duplicate_review_id_list'] = dup_ids['review_id'].unique().tolist()[:20]
            logger.warning(f"Found {len(dup_ids)} duplicate review_ids")
        
        # 3. 핵심 컬럼 결측률
        self.stats['missing_rating'] = self.df['rating'].isna().sum()
        self.stats['missing_rating_rate'] = self.stats['missing_rating'] / total * 100
        
        self.stats['missing_review_text'] = self.df['review_text'].isna().sum()
        self.stats['missing_review_text_rate'] = self.stats['missing_review_text'] / total * 100
        
        self.stats['missing_date_parsed'] = self.df['review_date_parsed'].isna().sum()
        self.stats['missing_date_parsed_rate'] = self.stats['missing_date_parsed'] / total * 100
        
        # 4. rating 분포
        rating_dist = self.df['rating'].value_counts(dropna=False).sort_index()
        self.stats['rating_distribution'] = rating_dist.to_dict()
        
        # 5. 날짜 범위
        valid_dates = self.df['review_date_parsed'].dropna()
        if len(valid_dates) > 0:
            self.stats['date_min'] = valid_dates.min().strftime('%Y-%m-%d')
            self.stats['date_max'] = valid_dates.max().strftime('%Y-%m-%d')
            
            # 월별 카운트
            monthly = self.df['review_month'].value_counts().sort_index()
            self.stats['monthly_top5'] = monthly.tail(5).to_dict()
            self.stats['monthly_bottom5'] = monthly.head(5).to_dict()
        
        # 6. 텍스트 길이 분포
        text_lens = self.df['text_len_chars']
        self.stats['text_len_p50'] = int(text_lens.quantile(0.5))
        self.stats['text_len_p90'] = int(text_lens.quantile(0.9))
        self.stats['text_len_p99'] = int(text_lens.quantile(0.99))
        self.stats['has_text_rate'] = self.df['has_text'].sum() / total * 100
        
        # 7. 짧은 리뷰 비율 (15자 미만)
        short_reviews = (text_lens < 15).sum()
        self.stats['short_reviews_count'] = short_reviews
        self.stats['short_reviews_rate'] = short_reviews / total * 100
        
        # 8. 계절 분포
        self.stats['season_distribution'] = self.df['season'].value_counts(dropna=False).to_dict()
    
    def save_output(self) -> None:
        """결과 저장"""
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        
        # review_date_parsed를 date 타입으로 변환
        self.df['review_date_parsed'] = pd.to_datetime(self.df['review_date_parsed']).dt.date
        
        self.df.to_parquet(self.output_path, index=False, engine='pyarrow')
        logger.info(f"Saved preprocessed data to {self.output_path}")
    
    def generate_report(self) -> str:
        """QA 리포트 생성"""
        os.makedirs(self.report_dir, exist_ok=True)
        report_path = os.path.join(self.report_dir, "step3_0_quality.md")
        
        # 리포트 내용 생성
        lines = [
            "# Step 3-0: Baseline 전처리 품질 리포트",
            "",
            f"생성 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
            "## 1. 기본 통계",
            "",
            f"| 항목 | 값 |",
            f"|------|-----|",
            f"| 총 리뷰 수 | {self.stats['total_reviews']:,} |",
            f"| 상품 수 (goods_no) | {self.stats['unique_goods']:,} |",
            f"| 중복 review_id 건수 | {self.stats['duplicate_review_ids']:,} |",
            "",
            "---",
            "",
            "## 2. Rating 분포",
            "",
            "| Rating | 건수 | 비율 |",
            "|--------|------|------|",
        ]
        
        total = self.stats['total_reviews']
        for rating, count in sorted(self.stats['rating_distribution'].items(), key=lambda x: (x[0] is None, x[0])):
            rate = count / total * 100 if total > 0 else 0
            rating_str = str(rating) if rating is not None else "null"
            lines.append(f"| {rating_str} | {count:,} | {rate:.1f}% |")
        
        lines.extend([
            "",
            f"결측률: {self.stats['missing_rating_rate']:.2f}%",
            "",
            "---",
            "",
            "## 3. 날짜 파싱 결과",
            "",
            f"| 항목 | 값 |",
            f"|------|-----|",
            f"| 파싱 성공 | {self.stats['date_parse_success']:,} ({self.stats['date_parse_success_rate']:.1f}%) |",
            f"| 파싱 실패 | {self.stats['date_parse_failed']:,} |",
            f"| 날짜 범위 | {self.stats.get('date_min', 'N/A')} ~ {self.stats.get('date_max', 'N/A')} |",
            "",
            "### 월별 리뷰 수 (상위 5개월)",
            "",
            "| 월 | 건수 |",
            "|-----|------|",
        ])
        
        for month, count in self.stats.get('monthly_top5', {}).items():
            lines.append(f"| {month} | {count:,} |")
        
        lines.extend([
            "",
            "### 계절별 분포",
            "",
            "| 계절 | 건수 |",
            "|------|------|",
        ])
        
        for season, count in self.stats.get('season_distribution', {}).items():
            season_str = str(season) if season is not None else "null"
            lines.append(f"| {season_str} | {count:,} |")
        
        lines.extend([
            "",
            "---",
            "",
            "## 4. 텍스트 품질",
            "",
            f"| 항목 | 값 |",
            f"|------|-----|",
            f"| 텍스트 존재율 (has_text) | {self.stats['has_text_rate']:.1f}% |",
            f"| 길이 p50 | {self.stats['text_len_p50']:,} 자 |",
            f"| 길이 p90 | {self.stats['text_len_p90']:,} 자 |",
            f"| 길이 p99 | {self.stats['text_len_p99']:,} 자 |",
            f"| 짧은 리뷰 (<15자) | {self.stats['short_reviews_count']:,} ({self.stats['short_reviews_rate']:.1f}%) |",
            "",
            "---",
            "",
            "## 5. 결측률 요약",
            "",
            "| 컬럼 | 결측 건수 | 결측률 |",
            "|------|----------|--------|",
            f"| rating | {self.stats['missing_rating']:,} | {self.stats['missing_rating_rate']:.2f}% |",
            f"| review_text | {self.stats['missing_review_text']:,} | {self.stats['missing_review_text_rate']:.2f}% |",
            f"| review_date_parsed | {self.stats['missing_date_parsed']:,} | {self.stats['missing_date_parsed_rate']:.2f}% |",
            "",
            "---",
            "",
            "## 6. 다음 단계 권고 (Step 3-1 태깅)",
            "",
        ])
        
        # 권고사항 추가
        recommendations = []
        
        if self.stats['short_reviews_rate'] > 10:
            recommendations.append(f"- ⚠️ 짧은 리뷰 비율이 {self.stats['short_reviews_rate']:.1f}%로 높음. 태깅 시 `is_low_info` 필터링 고려")
        
        if self.stats['duplicate_review_ids'] > 0:
            recommendations.append(f"- ⚠️ 중복 review_id {self.stats['duplicate_review_ids']}건 발견. 분석 전 중복 제거 필요")
        
        if self.stats['missing_rating_rate'] > 5:
            recommendations.append(f"- ⚠️ rating 결측률이 {self.stats['missing_rating_rate']:.1f}%로 높음")
        
        if not recommendations:
            recommendations.append("- ✅ 데이터 품질 양호. 다음 단계 진행 가능")
        
        lines.extend(recommendations)
        lines.append("")
        
        # 파일 저장
        report_content = "\n".join(lines)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        logger.info(f"Generated QA report: {report_path}")
        return report_path
    
    def run(self) -> None:
        """전체 파이프라인 실행"""
        try:
            self.load_data()
            self.normalize_schema()
            self.parse_dates()
            self.create_rating_bucket()
            self.clean_text_column()
            self.run_qa_checks()
            self.save_output()
            self.generate_report()
            
            logger.info("=" * 50)
            logger.info("Baseline preprocessing completed successfully!")
            logger.info(f"Output: {self.output_path}")
            logger.info(f"Report: {os.path.join(self.report_dir, 'step3_0_quality.md')}")
            
        except Exception as e:
            logger.error(f"Error during preprocessing: {e}")
            # 가능한 범위까지 저장 시도
            if self.df is not None and len(self.df) > 0:
                try:
                    emergency_path = self.output_path.replace('.parquet', '_partial.parquet')
                    self.df.to_parquet(emergency_path, index=False)
                    logger.info(f"Partial data saved to {emergency_path}")
                except Exception as save_error:
                    logger.error(f"Failed to save partial data: {save_error}")
            raise


def main():
    parser = argparse.ArgumentParser(
        description="Step 3-0: Baseline 전처리 스크립트"
    )
    parser.add_argument(
        "--input", "-i",
        default="data/processed/reviews.parquet",
        help="입력 parquet 파일 경로"
    )
    parser.add_argument(
        "--out", "-o",
        default="data/processed/reviews_step3_base.parquet",
        help="출력 parquet 파일 경로"
    )
    parser.add_argument(
        "--report-dir",
        default="report",
        help="리포트 출력 디렉토리"
    )
    
    args = parser.parse_args()
    
    preprocessor = BaselinePreprocessor(
        input_path=args.input,
        output_path=args.out,
        report_dir=args.report_dir
    )
    preprocessor.run()


if __name__ == "__main__":
    main()
