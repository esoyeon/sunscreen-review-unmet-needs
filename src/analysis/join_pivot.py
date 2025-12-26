"""
Step 4-0: Join & Pivot - LLM Aspect/Polarity × Rule Context

LLM 추출 결과와 Rule 기반 태깅을 조인하여 미충족 니즈 분석 테이블 생성.

Usage:
    python -m src.analysis.join_pivot \
        --norm data/llm/extractions_full_normalized.parquet \
        --tagged data/processed/reviews_step3_tagged.parquet \
        --out_dir data/analysis \
        --report report/step4_0_join_pivot.md
"""

import argparse
import logging
import os
from datetime import datetime
from typing import Dict, Any, List

import pandas as pd
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JoinPivotPipeline:
    """Join & Pivot 파이프라인"""
    
    def __init__(
        self,
        norm_path: str,
        tagged_path: str,
        out_dir: str,
        report_path: str,
        min_n: int = 30
    ):
        self.norm_path = norm_path
        self.tagged_path = tagged_path
        self.out_dir = out_dir
        self.report_path = report_path
        self.min_n = min_n
        
        self.norm_df = None
        self.tagged_df = None
        self.master_df = None
        self.stats = {}
    
    def load_data(self):
        """데이터 로드"""
        logger.info("Loading data...")
        
        self.norm_df = pd.read_parquet(self.norm_path)
        self.tagged_df = pd.read_parquet(self.tagged_path)
        
        self.stats['norm_rows'] = len(self.norm_df)
        self.stats['norm_reviews'] = self.norm_df['review_id'].nunique()
        self.stats['tagged_rows'] = len(self.tagged_df)
        
        logger.info(f"Norm: {len(self.norm_df)} rows, {self.stats['norm_reviews']} reviews")
        logger.info(f"Tagged: {len(self.tagged_df)} rows")
    
    def create_master_join(self):
        """마스터 조인 테이블 생성"""
        logger.info("Creating master join...")
        
        # Join columns from tagged
        join_cols = [
            'review_id', 'rating', 'rating_bucket', 'season', 'review_month',
            'context_tags_str', 'attribute_tags_str', 'skin_tags_str',
            'has_conditional', 'golden_nugget', 'is_trial', 'is_low_info',
            'text_len_chars', 'helpful_count', 'primary_sort'
        ]
        
        # Filter existing columns
        available_cols = [c for c in join_cols if c in self.tagged_df.columns]
        tagged_subset = self.tagged_df[available_cols].copy()
        
        # Left join
        self.master_df = self.norm_df.merge(
            tagged_subset,
            on='review_id',
            how='left'
        )
        
        # Join stats
        joined = self.master_df['rating'].notna().sum()
        self.stats['join_success'] = joined
        self.stats['join_rate'] = joined / len(self.master_df) * 100
        
        logger.info(f"Join success: {joined}/{len(self.master_df)} ({self.stats['join_rate']:.1f}%)")
        
        # Add polarity_group
        self.master_df['polarity_group'] = self.master_df['polarity'].apply(
            lambda x: 'unmet_like' if x in ('unmet', 'mixed') else ('met_like' if x == 'met' else 'unknown')
        )
        
        # Save master
        master_path = os.path.join(self.out_dir, 'step4_master_join.parquet')
        self.master_df.to_parquet(master_path, index=False)
        logger.info(f"Saved: {master_path}")
    
    def create_pivot_overall(self):
        """T1: Overall aspect × polarity"""
        logger.info("Creating T1: Overall pivot...")
        
        # Group by aspect
        pivot = self.master_df.groupby('aspect').agg(
            n_items=('review_id', 'count'),
            met_cnt=('polarity', lambda x: (x == 'met').sum()),
            unmet_cnt=('polarity', lambda x: (x == 'unmet').sum()),
            mixed_cnt=('polarity', lambda x: (x == 'mixed').sum()),
            unknown_cnt=('polarity', lambda x: (x == 'unknown').sum()),
        ).reset_index()
        
        pivot['unmet_like_cnt'] = pivot['unmet_cnt'] + pivot['mixed_cnt']
        pivot['unmet_like_rate'] = pivot['unmet_like_cnt'] / pivot['n_items']
        pivot = pivot.sort_values('unmet_like_rate', ascending=False)
        
        path = os.path.join(self.out_dir, 'pivot_aspect_polarity_overall.parquet')
        pivot.to_parquet(path, index=False)
        logger.info(f"Saved: {path}")
        
        self.pivot_overall = pivot
    
    def create_pivot_by_bucket(self):
        """T2: Bucket별 aspect × polarity"""
        logger.info("Creating T2: By bucket pivot...")
        
        pivot = self.master_df.groupby(['bucket', 'aspect']).agg(
            n_items=('review_id', 'count'),
            met_cnt=('polarity', lambda x: (x == 'met').sum()),
            unmet_cnt=('polarity', lambda x: (x == 'unmet').sum()),
            mixed_cnt=('polarity', lambda x: (x == 'mixed').sum()),
            unknown_cnt=('polarity', lambda x: (x == 'unknown').sum()),
        ).reset_index()
        
        pivot['unmet_like_cnt'] = pivot['unmet_cnt'] + pivot['mixed_cnt']
        pivot['unmet_like_rate'] = pivot['unmet_like_cnt'] / pivot['n_items']
        
        path = os.path.join(self.out_dir, 'pivot_aspect_polarity_by_bucket.parquet')
        pivot.to_parquet(path, index=False)
        logger.info(f"Saved: {path}")
        
        self.pivot_by_bucket = pivot
    
    def create_pivot_context_aspect(self):
        """T3: Context × Aspect unmet"""
        logger.info("Creating T3: Context × Aspect pivot...")
        
        # Explode context_tags
        df = self.master_df.copy()
        df['context_tag'] = df['context_tags_str'].fillna('NONE_RULE').apply(
            lambda x: x.split('|') if x and x != 'NONE_RULE' else ['NONE_RULE']
        )
        df = df.explode('context_tag')
        
        # Dedup (review_id, aspect, context_tag)
        df_dedup = df.drop_duplicates(subset=['review_id', 'aspect', 'context_tag'])
        
        self.stats['context_explode_rows'] = len(df_dedup)
        self.stats['context_none_rate'] = (df_dedup['context_tag'] == 'NONE_RULE').mean() * 100
        
        # Group by (context_tag, aspect)
        pivot = df_dedup.groupby(['context_tag', 'aspect']).agg(
            n_reviews=('review_id', 'nunique'),
            unmet_like_cnt=('polarity_group', lambda x: (x == 'unmet_like').sum()),
            met_like_cnt=('polarity_group', lambda x: (x == 'met_like').sum()),
        ).reset_index()
        
        pivot['unmet_like_rate'] = pivot['unmet_like_cnt'] / pivot['n_reviews']
        pivot = pivot.sort_values('unmet_like_cnt', ascending=False)
        
        path = os.path.join(self.out_dir, 'pivot_context_aspect_unmet.parquet')
        pivot.to_parquet(path, index=False)
        logger.info(f"Saved: {path}")
        
        self.pivot_context = pivot
        self.context_exploded_df = df_dedup
    
    def create_pivot_season_aspect(self):
        """T4: Season × Aspect unmet"""
        logger.info("Creating T4: Season × Aspect pivot...")
        
        df = self.master_df[self.master_df['season'].notna()].copy()
        
        pivot = df.groupby(['season', 'aspect']).agg(
            n_reviews=('review_id', 'nunique'),
            unmet_like_cnt=('polarity_group', lambda x: (x == 'unmet_like').sum()),
            met_like_cnt=('polarity_group', lambda x: (x == 'met_like').sum()),
        ).reset_index()
        
        pivot['unmet_like_rate'] = pivot['unmet_like_cnt'] / pivot['n_reviews']
        
        path = os.path.join(self.out_dir, 'pivot_season_aspect_unmet.parquet')
        pivot.to_parquet(path, index=False)
        logger.info(f"Saved: {path}")
        
        self.pivot_season = pivot
    
    def create_repeatability_table(self):
        """T5: 반복성 검증 (상품 반복)"""
        logger.info("Creating T5: Repeatability table...")
        
        df = self.master_df.copy()
        
        # Aspect별 집계
        repeat = df.groupby('aspect').agg(
            goods_cnt_any=('goods_no', 'nunique'),
            reviews_any_cnt=('review_id', 'nunique'),
        ).reset_index()
        
        # unmet_like만 필터
        df_unmet = df[df['polarity_group'] == 'unmet_like']
        unmet_agg = df_unmet.groupby('aspect').agg(
            goods_cnt_unmet_like=('goods_no', 'nunique'),
            reviews_unmet_like_cnt=('review_id', 'nunique'),
        ).reset_index()
        
        # Merge
        repeat = repeat.merge(unmet_agg, on='aspect', how='left').fillna(0)
        repeat['goods_cnt_unmet_like'] = repeat['goods_cnt_unmet_like'].astype(int)
        repeat['reviews_unmet_like_cnt'] = repeat['reviews_unmet_like_cnt'].astype(int)
        repeat['goods_repeat_rate'] = repeat['goods_cnt_unmet_like'] / repeat['goods_cnt_any']
        
        repeat = repeat.sort_values('goods_cnt_unmet_like', ascending=False)
        
        path = os.path.join(self.out_dir, 'repeatability_aspect_goods_count.parquet')
        repeat.to_parquet(path, index=False)
        logger.info(f"Saved: {path}")
        
        self.repeatability = repeat
    
    def generate_report(self):
        """리포트 생성"""
        logger.info("Generating report...")
        
        lines = [
            "# Step 4-0: Join & Pivot 리포트",
            "",
            f"생성: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
            "## 1. 데이터 연결 요약",
            "",
            "| 항목 | 값 |",
            "|------|-----|",
            f"| LLM Norm rows | {self.stats['norm_rows']:,} |",
            f"| LLM Unique reviews | {self.stats['norm_reviews']:,} |",
            f"| Join 성공률 | {self.stats['join_rate']:.1f}% |",
            f"| Context explode rows | {self.stats['context_explode_rows']:,} |",
            f"| NONE_RULE 비율 | {self.stats['context_none_rate']:.1f}% |",
            "",
            "---",
            "",
            "## 2. Overall: unmet_like_rate Top 10 Aspect",
            "",
            "| Aspect | n_items | unmet_like_cnt | unmet_like_rate |",
            "|--------|---------|----------------|-----------------|",
        ]
        
        for _, row in self.pivot_overall.head(10).iterrows():
            lines.append(f"| {row['aspect']} | {row['n_items']:,} | {row['unmet_like_cnt']:,} | {row['unmet_like_rate']:.1%} |")
        
        # Golden Nugget only
        gn = self.pivot_by_bucket[self.pivot_by_bucket['bucket'] == 'GOLDEN_NUGGET'].copy()
        gn = gn.sort_values('unmet_like_cnt', ascending=False)
        
        lines.extend([
            "",
            "---",
            "",
            "## 3. GOLDEN_NUGGET: unmet_like_cnt Top 10",
            "",
            "> 긍정 리뷰에서도 미충족된 니즈 = **좋아하지만 해결되지 않은 문제**",
            "",
            "| Aspect | n_items | unmet_like_cnt | unmet_like_rate |",
            "|--------|---------|----------------|-----------------|",
        ])
        
        for _, row in gn.head(10).iterrows():
            lines.append(f"| {row['aspect']} | {row['n_items']:,} | {row['unmet_like_cnt']:,} | {row['unmet_like_rate']:.1%} |")
        
        # Context × Aspect Top 15 (GOLDEN_NUGGET)
        ctx_gn = self.context_exploded_df[self.context_exploded_df['bucket'] == 'GOLDEN_NUGGET'].copy()
        ctx_gn_agg = ctx_gn.groupby(['context_tag', 'aspect']).agg(
            n=('review_id', 'nunique'),
            unmet_like=('polarity_group', lambda x: (x == 'unmet_like').sum()),
        ).reset_index()
        ctx_gn_agg = ctx_gn_agg[ctx_gn_agg['context_tag'] != 'NONE_RULE']
        ctx_gn_agg = ctx_gn_agg.sort_values('unmet_like', ascending=False).head(15)
        
        lines.extend([
            "",
            "---",
            "",
            "## 4. GOLDEN_NUGGET: Context × Aspect Top 15",
            "",
            "| Context | Aspect | n | unmet_like |",
            "|---------|--------|---|------------|",
        ])
        
        for _, row in ctx_gn_agg.iterrows():
            lines.append(f"| {row['context_tag']} | {row['aspect']} | {row['n']} | {row['unmet_like']} |")
        
        # Season Top 5
        lines.extend([
            "",
            "---",
            "",
            "## 5. Season별 Aspect (unmet_like_cnt 기준)",
            "",
        ])
        
        for season in ['summer', 'winter']:
            season_data = self.pivot_season[self.pivot_season['season'] == season]
            season_data = season_data.sort_values('unmet_like_cnt', ascending=False).head(5)
            lines.append(f"### {season.upper()}")
            lines.append("")
            lines.append("| Aspect | n | unmet_like_cnt |")
            lines.append("|--------|---|----------------|")
            for _, row in season_data.iterrows():
                lines.append(f"| {row['aspect']} | {row['n_reviews']} | {row['unmet_like_cnt']} |")
            lines.append("")
        
        # Repeatability Top 10
        lines.extend([
            "---",
            "",
            "## 6. Repeatability: goods_cnt_unmet_like Top 10",
            "",
            "> 여러 상품에서 반복되는 문제 = **개인 취향이 아닌 시장 문제**",
            "",
            "| Aspect | goods_cnt_unmet | reviews_unmet | goods_repeat_rate |",
            "|--------|-----------------|---------------|-------------------|",
        ])
        
        for _, row in self.repeatability.head(10).iterrows():
            lines.append(f"| {row['aspect']} | {row['goods_cnt_unmet_like']} | {row['reviews_unmet_like_cnt']} | {row['goods_repeat_rate']:.1%} |")
        
        # 해석 가이드
        lines.extend([
            "",
            "---",
            "",
            "## 7. 해석 가이드",
            "",
            "- **GOLDEN_NUGGET unmet_like 높은 aspect**: 제품을 좋아하지만 해결되지 않은 문제",
            "- **LOW_RATING unmet_like 높은 aspect**: 명확한 불만 원인",
            "- **Repeatability 높은 aspect**: 신상품 기획 시 우선 해결 과제",
            "- **Context별 분석**: 특정 맥락(메이크업, 여름 등)에서 두드러지는 문제 파악",
            "",
        ])
        
        os.makedirs(os.path.dirname(self.report_path), exist_ok=True)
        with open(self.report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        logger.info(f"Report saved: {self.report_path}")
    
    def run(self):
        """전체 파이프라인 실행"""
        try:
            os.makedirs(self.out_dir, exist_ok=True)
            
            self.load_data()
            self.create_master_join()
            self.create_pivot_overall()
            self.create_pivot_by_bucket()
            self.create_pivot_context_aspect()
            self.create_pivot_season_aspect()
            self.create_repeatability_table()
            self.generate_report()
            
            logger.info("=" * 50)
            logger.info("Step 4-0 completed!")
            
        except Exception as e:
            logger.error(f"Error: {e}")
            raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--norm", default="data/llm/extractions_full_normalized.parquet")
    parser.add_argument("--tagged", default="data/processed/reviews_step3_tagged.parquet")
    parser.add_argument("--out_dir", default="data/analysis")
    parser.add_argument("--report", default="report/step4_0_join_pivot.md")
    parser.add_argument("--min_n", type=int, default=30)
    
    args = parser.parse_args()
    
    pipeline = JoinPivotPipeline(
        norm_path=args.norm,
        tagged_path=args.tagged,
        out_dir=args.out_dir,
        report_path=args.report,
        min_n=args.min_n
    )
    pipeline.run()


if __name__ == "__main__":
    main()
