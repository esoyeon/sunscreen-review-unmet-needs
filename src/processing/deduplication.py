"""
Step 3-0.5: Review Deduplication 스크립트

동일 review_id가 여러 goods_no에 걸쳐 중복된 경우를 통합합니다.
원문 보존, 메타데이터는 merge 규칙에 따라 통합.

Usage:
    python -m src.processing.deduplication \
        --input data/processed/reviews_step3_base.parquet \
        --out data/processed/reviews_step3_dedup.parquet
"""

import argparse
import logging
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

import pandas as pd
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Primary sort 우선순위 (낮을수록 높음)
SORT_PRIORITY = {
    'low_rating': 1,
    'newest': 2,
    'helpful': 3,
    'high_rating': 4
}


def get_mode(series: pd.Series) -> Any:
    """최빈값 반환 (동률이면 첫 번째)"""
    if series.isna().all():
        return None
    mode_result = series.mode()
    if len(mode_result) > 0:
        return mode_result.iloc[0]
    return series.iloc[0]


def check_conflict(series: pd.Series) -> bool:
    """값 충돌 여부 확인 (2개 이상 다른 값)"""
    unique = series.dropna().unique()
    return len(unique) > 1


def union_list(series: pd.Series) -> List:
    """리스트 컬럼의 유니온"""
    result = set()
    for val in series.dropna():
        if isinstance(val, list):
            result.update(val)
        elif isinstance(val, str):
            result.add(val)
    return sorted(list(result))


def get_primary_sort(sort_sources: List[str]) -> Optional[str]:
    """우선순위에 따른 primary_sort 결정"""
    if not sort_sources:
        return None
    
    best = None
    best_priority = float('inf')
    
    for src in sort_sources:
        priority = SORT_PRIORITY.get(src, 999)
        if priority < best_priority:
            best_priority = priority
            best = src
    
    return best


class ReviewDeduplicator:
    """리뷰 중복 통합기"""
    
    def __init__(self, input_path: str, output_path: str, report_dir: str = "report"):
        self.input_path = input_path
        self.output_path = output_path
        self.report_dir = report_dir
        self.df: Optional[pd.DataFrame] = None
        self.df_dedup: Optional[pd.DataFrame] = None
        self.stats: Dict[str, Any] = {}
        self.samples: List[Dict] = []
    
    def load_data(self) -> None:
        """데이터 로드"""
        logger.info(f"Loading data from {self.input_path}")
        self.df = pd.read_parquet(self.input_path)
        self.stats['rows_before'] = len(self.df)
        self.stats['unique_review_ids'] = self.df['review_id'].nunique()
        logger.info(f"Loaded {len(self.df)} reviews, {self.stats['unique_review_ids']} unique review_ids")
    
    def analyze_duplicates(self) -> None:
        """중복 분석"""
        logger.info("Analyzing duplicates...")
        
        dup_counts = self.df.groupby('review_id').size()
        dup_only = dup_counts[dup_counts > 1]
        
        self.stats['dup_groups'] = len(dup_only)
        self.stats['rows_in_dup_groups'] = dup_only.sum()
        
        logger.info(f"Found {self.stats['dup_groups']} duplicate groups ({self.stats['rows_in_dup_groups']} rows)")
    
    def merge_group(self, group: pd.DataFrame) -> Dict[str, Any]:
        """그룹 병합"""
        result = {}
        
        # 기본 정보 (첫 번째 값)
        result['review_id'] = group['review_id'].iloc[0]
        result['goods_no'] = group['goods_no'].iloc[0]
        result['product_id'] = group['product_id'].iloc[0]
        
        # goods_no_all (모든 goods_no 리스트)
        goods_list = group['goods_no'].unique().tolist()
        result['goods_no_all'] = goods_list if len(goods_list) > 1 else None
        
        # 중복 카운트
        result['dup_count'] = len(group)
        
        # 충돌 체크 대상 컬럼
        conflict_cols = ['rating', 'review_date', 'review_text']
        conflicts = {}
        
        for col in conflict_cols:
            if col in group.columns:
                conflicts[col] = check_conflict(group[col])
                result[col] = get_mode(group[col])
        
        # dup_conflict 플래그
        result['dup_conflict'] = any(conflicts.values())
        result['conflict_cols'] = [k for k, v in conflicts.items() if v] if result['dup_conflict'] else None
        
        # review_text_clean도 mode로
        if 'review_text_clean' in group.columns:
            result['review_text_clean'] = get_mode(group['review_text_clean'])
        
        # Max 통합
        for col in ['helpful_count', 'image_count']:
            if col in group.columns:
                result[col] = group[col].max()
        
        # Bool max (OR)
        for col in ['has_images']:
            if col in group.columns:
                result[col] = group[col].any()
        
        # OR 통합 (is_trial, is_low_info)
        for col in ['is_trial', 'is_low_info']:
            if col in group.columns:
                result[col] = 1 if (group[col] == 1).any() else 0
        
        # Sort 메타 통합
        all_sources = set()
        for sources in group['sort_source'].dropna():
            if isinstance(sources, str):
                all_sources.add(sources)
        
        if 'sort_sources_all' in group.columns:
            for sources in group['sort_sources_all'].dropna():
                if isinstance(sources, list):
                    all_sources.update(sources)
                elif isinstance(sources, str):
                    all_sources.add(sources)
        
        sort_list = sorted(list(all_sources))
        result['sort_sources_all'] = sort_list
        result['sort_sources_str'] = '|'.join(sort_list) if sort_list else None
        result['sort_count'] = len(sort_list)
        result['primary_sort'] = get_primary_sort(sort_list)
        
        # 기타 컬럼 (첫 번째 값)
        other_cols = [
            'skin_type_raw', 'skin_tone_raw', 'skin_trouble_raw',
            'review_type', 'source',
            'review_date_parsed', 'review_month', 'review_year', 'season',
            'rating_bucket', 'text_len_chars', 'text_len_words', 'has_text'
        ]
        
        for col in other_cols:
            if col in group.columns:
                result[col] = group[col].iloc[0]
        
        return result
    
    def deduplicate(self) -> None:
        """중복 통합 실행"""
        logger.info("Deduplicating reviews...")
        
        # 샘플 수집 (통합 전)
        dup_ids = self.df.groupby('review_id').filter(lambda x: len(x) > 1)['review_id'].unique()[:10]
        
        for rid in dup_ids:
            sample_before = self.df[self.df['review_id'] == rid][
                ['review_id', 'goods_no', 'sort_source', 'rating', 'helpful_count']
            ].to_dict('records')
            self.samples.append({'review_id': rid, 'before': sample_before})
        
        # 그룹별 병합
        merged_rows = []
        for review_id, group in self.df.groupby('review_id'):
            merged = self.merge_group(group)
            merged_rows.append(merged)
        
        self.df_dedup = pd.DataFrame(merged_rows)
        
        # 샘플에 통합 후 정보 추가
        for sample in self.samples:
            rid = sample['review_id']
            after_row = self.df_dedup[self.df_dedup['review_id'] == rid]
            if len(after_row) > 0:
                sample['after'] = after_row[[
                    'review_id', 'goods_no', 'goods_no_all', 'sort_sources_str',
                    'dup_count', 'dup_conflict'
                ]].to_dict('records')[0]
        
        self.stats['rows_after'] = len(self.df_dedup)
        
        # 충돌 통계
        conflict_count = self.df_dedup['dup_conflict'].sum()
        self.stats['conflict_count'] = conflict_count
        self.stats['conflict_rate'] = conflict_count / len(self.df_dedup) * 100
        
        # primary_sort 분포
        self.stats['primary_sort_dist'] = self.df_dedup['primary_sort'].value_counts(dropna=False).to_dict()
        
        logger.info(f"Deduplicated: {self.stats['rows_before']} -> {self.stats['rows_after']} rows")
        logger.info(f"Conflicts: {conflict_count} ({self.stats['conflict_rate']:.2f}%)")
    
    def save_output(self) -> None:
        """결과 저장"""
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        
        # 컬럼 순서 정리
        priority_cols = [
            'review_id', 'goods_no', 'goods_no_all', 'product_id',
            'rating', 'rating_bucket', 'review_date', 'review_date_parsed',
            'review_month', 'review_year', 'season',
            'review_text', 'review_text_clean', 'text_len_chars', 'text_len_words', 'has_text',
            'helpful_count', 'has_images', 'image_count',
            'skin_type_raw', 'skin_tone_raw', 'skin_trouble_raw',
            'review_type', 'is_trial', 'is_low_info', 'source',
            'sort_sources_all', 'sort_sources_str', 'sort_count', 'primary_sort',
            'dup_count', 'dup_conflict', 'conflict_cols'
        ]
        
        existing_cols = [c for c in priority_cols if c in self.df_dedup.columns]
        other_cols = [c for c in self.df_dedup.columns if c not in existing_cols]
        final_cols = existing_cols + other_cols
        
        self.df_dedup = self.df_dedup[final_cols]
        self.df_dedup.to_parquet(self.output_path, index=False, engine='pyarrow')
        
        logger.info(f"Saved deduplicated data to {self.output_path}")
    
    def generate_report(self) -> str:
        """QA 리포트 생성"""
        os.makedirs(self.report_dir, exist_ok=True)
        report_path = os.path.join(self.report_dir, "step3_0_5_dedup.md")
        
        lines = [
            "# Step 3-0.5: Review Deduplication 리포트",
            "",
            f"생성 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
            "## 1. 통합 결과 요약",
            "",
            "| 항목 | 값 |",
            "|------|-----|",
            f"| 통합 전 행 수 | {self.stats['rows_before']:,} |",
            f"| 통합 후 행 수 | {self.stats['rows_after']:,} |",
            f"| 제거된 중복 행 | {self.stats['rows_before'] - self.stats['rows_after']:,} |",
            f"| 중복 그룹 수 | {self.stats['dup_groups']:,} |",
            "",
            "---",
            "",
            "## 2. 충돌 분석",
            "",
            f"| 항목 | 값 |",
            f"|------|-----|",
            f"| dup_conflict=1 건수 | {self.stats['conflict_count']:,} |",
            f"| dup_conflict 비율 | {self.stats['conflict_rate']:.2f}% |",
            "",
        ]
        
        # 충돌 상세 분석
        if self.stats['conflict_count'] > 0:
            conflict_df = self.df_dedup[self.df_dedup['dup_conflict'] == True]
            conflict_types = conflict_df['conflict_cols'].explode().value_counts()
            
            lines.extend([
                "### 충돌 유형별 분포",
                "",
                "| 컬럼 | 충돌 건수 |",
                "|------|----------|",
            ])
            
            for col, count in conflict_types.items():
                if col:
                    lines.append(f"| {col} | {count:,} |")
            
            lines.append("")
        
        lines.extend([
            "---",
            "",
            "## 3. Primary Sort 분포 (통합 후)",
            "",
            "| Sort | 건수 | 비율 |",
            "|------|------|------|",
        ])
        
        total = self.stats['rows_after']
        for sort_type, count in self.stats['primary_sort_dist'].items():
            rate = count / total * 100 if total > 0 else 0
            sort_str = str(sort_type) if sort_type else "null"
            lines.append(f"| {sort_str} | {count:,} | {rate:.1f}% |")
        
        lines.extend([
            "",
            "---",
            "",
            "## 4. 샘플 비교 (통합 전후)",
            "",
        ])
        
        for i, sample in enumerate(self.samples[:5], 1):
            lines.extend([
                f"### 샘플 {i}: review_id={sample['review_id']}",
                "",
                "**통합 전:**",
                "",
                "| goods_no | sort_source | rating | helpful_count |",
                "|----------|-------------|--------|---------------|",
            ])
            
            for row in sample['before']:
                lines.append(f"| {row['goods_no']} | {row['sort_source']} | {row['rating']} | {row['helpful_count']} |")
            
            lines.append("")
            
            if 'after' in sample:
                after = sample['after']
                lines.extend([
                    "**통합 후:**",
                    "",
                    f"- goods_no: {after['goods_no']}",
                    f"- goods_no_all: {after['goods_no_all']}",
                    f"- sort_sources_str: {after['sort_sources_str']}",
                    f"- dup_count: {after['dup_count']}",
                    f"- dup_conflict: {after['dup_conflict']}",
                    "",
                ])
        
        # 파일 저장
        report_content = "\n".join(lines)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        logger.info(f"Generated report: {report_path}")
        return report_path
    
    def run(self) -> None:
        """전체 파이프라인 실행"""
        try:
            self.load_data()
            self.analyze_duplicates()
            self.deduplicate()
            self.save_output()
            self.generate_report()
            
            logger.info("=" * 50)
            logger.info("Deduplication completed successfully!")
            logger.info(f"Output: {self.output_path}")
            logger.info(f"Report: {os.path.join(self.report_dir, 'step3_0_5_dedup.md')}")
            
        except Exception as e:
            logger.error(f"Error during deduplication: {e}")
            raise


def main():
    parser = argparse.ArgumentParser(
        description="Step 3-0.5: Review Deduplication 스크립트"
    )
    parser.add_argument(
        "--input", "-i",
        default="data/processed/reviews_step3_base.parquet",
        help="입력 parquet 파일 경로"
    )
    parser.add_argument(
        "--out", "-o",
        default="data/processed/reviews_step3_dedup.parquet",
        help="출력 parquet 파일 경로"
    )
    parser.add_argument(
        "--report-dir",
        default="report",
        help="리포트 출력 디렉토리"
    )
    
    args = parser.parse_args()
    
    deduplicator = ReviewDeduplicator(
        input_path=args.input,
        output_path=args.out,
        report_dir=args.report_dir
    )
    deduplicator.run()


if __name__ == "__main__":
    main()
