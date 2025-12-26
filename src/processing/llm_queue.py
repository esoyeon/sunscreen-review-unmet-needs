"""
Step 3-2: LLM Queue 생성 스크립트

고가치 리뷰를 버킷별로 분류하여 LLM 추출용 Queue 생성.

Usage:
    python -m src.processing.llm_queue \
        --input data/processed/reviews_step3_tagged.parquet \
        --out data/llm/llm_queue.parquet \
        --report report/step3_2_llm_queue.md
"""

import argparse
import json
import logging
import os
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

import pandas as pd
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LLMQueueBuilder:
    """LLM Queue 생성기"""
    
    def __init__(
        self,
        input_path: str,
        output_path: str,
        report_dir: str,
        max_golden: int = 1500,
        max_low: int = 1500,
        max_helpful: int = 1000,
        max_random: int = 300,
        max_chars: int = 1200,
        seed: int = 42
    ):
        self.input_path = input_path
        self.output_path = output_path
        self.report_dir = report_dir
        self.max_golden = max_golden
        self.max_low = max_low
        self.max_helpful = max_helpful
        self.max_random = max_random
        self.max_chars = max_chars
        self.seed = seed
        
        self.df: Optional[pd.DataFrame] = None
        self.queue_df: Optional[pd.DataFrame] = None
        self.stats: Dict[str, Any] = {}
        
        np.random.seed(seed)
    
    def load_data(self):
        """데이터 로드"""
        logger.info(f"Loading data from {self.input_path}")
        self.df = pd.read_parquet(self.input_path)
        logger.info(f"Loaded {len(self.df)} reviews")
    
    def calculate_priority_score(self, row: pd.Series, bucket: str) -> float:
        """우선순위 점수 계산"""
        text_len = row.get('text_len_chars', 0) or 0
        helpful = row.get('helpful_count', 0) or 0
        
        # Base score
        score = np.log1p(text_len) + 0.2 * np.log1p(helpful)
        
        # Bucket bonus
        if bucket == 'GOLDEN_NUGGET':
            score += 2.0
        elif bucket == 'LOW_RATING':
            score += 1.5
        
        # Conditional bonus
        if row.get('has_conditional', False):
            score += 0.5
        
        # Toneup/Whitecast conflict bonus
        if row.get('toneup_whitecast_conflict', False):
            score += 0.3
        
        return round(score, 4)
    
    def create_input_text(self, row: pd.Series) -> str:
        """LLM 입력 텍스트 생성"""
        # 리뷰 본문
        text = row.get('review_text_clean', '') or ''
        
        # 메타 힌트 구성
        hints = []
        
        rating = row.get('rating')
        if rating:
            hints.append(f"rating={rating}")
        
        season = row.get('season')
        if season:
            hints.append(f"season={season}")
        
        attr_tags = row.get('attribute_tags_str')
        if attr_tags:
            hints.append(f"attr={attr_tags}")
        
        ctx_tags = row.get('context_tags_str')
        if ctx_tags:
            hints.append(f"ctx={ctx_tags}")
        
        skin_tags = row.get('skin_tags_str')
        if skin_tags:
            hints.append(f"skin={skin_tags}")
        
        cond_markers = row.get('conditional_markers_str')
        if cond_markers:
            hints.append(f"cond={cond_markers}")
        
        # 조합
        hint_str = ' | '.join(hints) if hints else ''
        
        if hint_str:
            input_text = f"[{hint_str}]\n\n{text}"
        else:
            input_text = text
        
        # Truncate (끝만 자르기)
        if len(input_text) > self.max_chars:
            input_text = input_text[:self.max_chars - 3] + '...'
        
        return input_text
    
    def create_meta_json(self, row: pd.Series) -> str:
        """메타 정보 JSON 생성"""
        meta = {
            'rating': int(row.get('rating')) if pd.notna(row.get('rating')) else None,
            'rating_bucket': row.get('rating_bucket'),
            'season': row.get('season'),
            'attribute_tags_str': row.get('attribute_tags_str'),
            'context_tags_str': row.get('context_tags_str'),
            'skin_tags_str': row.get('skin_tags_str'),
            'has_conditional': bool(row.get('has_conditional', False)),
            'conditional_markers_str': row.get('conditional_markers_str'),
            'primary_sort': row.get('primary_sort'),
            'helpful_count': int(row.get('helpful_count', 0)),
            'text_len_chars': int(row.get('text_len_chars', 0)),
        }
        return json.dumps(meta, ensure_ascii=False)
    
    def build_queue(self):
        """Queue 생성"""
        logger.info("Building LLM queue...")
        
        queue_rows = []
        used_review_ids = set()
        
        # 1. GOLDEN_NUGGET
        golden_df = self.df[self.df['golden_nugget'] == True].copy()
        golden_df['_priority'] = golden_df.apply(
            lambda r: self.calculate_priority_score(r, 'GOLDEN_NUGGET'), axis=1
        )
        golden_df = golden_df.sort_values('_priority', ascending=False).head(self.max_golden)
        
        for _, row in golden_df.iterrows():
            queue_rows.append({
                'queue_id': str(uuid.uuid4()),
                'review_id': row['review_id'],
                'goods_no': row['goods_no'],
                'bucket': 'GOLDEN_NUGGET',
                'priority_score': row['_priority'],
                'input_text': self.create_input_text(row),
                'meta_json': self.create_meta_json(row),
                'created_at': datetime.now().isoformat()
            })
            used_review_ids.add(row['review_id'])
        
        logger.info(f"GOLDEN_NUGGET: {len(golden_df)} items")
        
        # 2. LOW_RATING
        low_df = self.df[
            (self.df['rating_bucket'] == 'low') &
            (self.df['is_low_info'] == 0) &
            (~self.df['review_id'].isin(used_review_ids))
        ].copy()
        low_df['_priority'] = low_df.apply(
            lambda r: self.calculate_priority_score(r, 'LOW_RATING'), axis=1
        )
        low_df = low_df.sort_values('_priority', ascending=False).head(self.max_low)
        
        for _, row in low_df.iterrows():
            queue_rows.append({
                'queue_id': str(uuid.uuid4()),
                'review_id': row['review_id'],
                'goods_no': row['goods_no'],
                'bucket': 'LOW_RATING',
                'priority_score': row['_priority'],
                'input_text': self.create_input_text(row),
                'meta_json': self.create_meta_json(row),
                'created_at': datetime.now().isoformat()
            })
            used_review_ids.add(row['review_id'])
        
        logger.info(f"LOW_RATING: {len(low_df)} items")
        
        # 3. HELPFUL_LONG
        helpful_df = self.df[
            (self.df['primary_sort'] == 'helpful') &
            (self.df['text_len_chars'] >= 120) &
            (self.df['is_low_info'] == 0) &
            (~self.df['review_id'].isin(used_review_ids))
        ].copy()
        helpful_df['_priority'] = helpful_df.apply(
            lambda r: self.calculate_priority_score(r, 'HELPFUL_LONG'), axis=1
        )
        helpful_df = helpful_df.sort_values('_priority', ascending=False).head(self.max_helpful)
        
        for _, row in helpful_df.iterrows():
            queue_rows.append({
                'queue_id': str(uuid.uuid4()),
                'review_id': row['review_id'],
                'goods_no': row['goods_no'],
                'bucket': 'HELPFUL_LONG',
                'priority_score': row['_priority'],
                'input_text': self.create_input_text(row),
                'meta_json': self.create_meta_json(row),
                'created_at': datetime.now().isoformat()
            })
            used_review_ids.add(row['review_id'])
        
        logger.info(f"HELPFUL_LONG: {len(helpful_df)} items")
        
        # 4. RANDOM_CONTROL
        random_df = self.df[
            (self.df['is_low_info'] == 0) &
            (~self.df['review_id'].isin(used_review_ids))
        ].copy()
        random_df = random_df.sample(n=min(self.max_random, len(random_df)), random_state=self.seed)
        
        for _, row in random_df.iterrows():
            queue_rows.append({
                'queue_id': str(uuid.uuid4()),
                'review_id': row['review_id'],
                'goods_no': row['goods_no'],
                'bucket': 'RANDOM_CONTROL',
                'priority_score': self.calculate_priority_score(row, 'RANDOM_CONTROL'),
                'input_text': self.create_input_text(row),
                'meta_json': self.create_meta_json(row),
                'created_at': datetime.now().isoformat()
            })
        
        logger.info(f"RANDOM_CONTROL: {len(random_df)} items")
        
        self.queue_df = pd.DataFrame(queue_rows)
        
        # 통계
        self.stats['total_queue'] = len(self.queue_df)
        self.stats['bucket_counts'] = self.queue_df['bucket'].value_counts().to_dict()
        
        # 중복 확인
        dup_count = self.queue_df['review_id'].duplicated().sum()
        self.stats['duplicate_review_ids'] = dup_count
        if dup_count > 0:
            logger.warning(f"Found {dup_count} duplicate review_ids in queue!")
        
        # 텍스트 길이 통계
        text_lens = self.queue_df['input_text'].str.len()
        self.stats['text_len_mean'] = text_lens.mean()
        self.stats['text_len_median'] = text_lens.median()
        self.stats['text_len_p90'] = text_lens.quantile(0.9)
        
        logger.info(f"Total queue size: {len(self.queue_df)}")
    
    def save_output(self):
        """결과 저장"""
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        self.queue_df.to_parquet(self.output_path, index=False, engine='pyarrow')
        logger.info(f"Saved queue to {self.output_path}")
    
    def generate_report(self):
        """QA 리포트 생성"""
        os.makedirs(self.report_dir, exist_ok=True)
        report_path = os.path.join(self.report_dir, "step3_2_llm_queue.md")
        
        lines = [
            "# Step 3-2: LLM Queue 생성 리포트",
            "",
            f"생성 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
            "## 1. Queue 요약",
            "",
            "| 항목 | 값 |",
            "|------|-----|",
            f"| 총 Queue 건수 | {self.stats['total_queue']:,} |",
            f"| 중복 review_id | {self.stats['duplicate_review_ids']} |",
            "",
            "### 버킷별 건수",
            "",
            "| Bucket | 건수 | 비율 |",
            "|--------|------|------|",
        ]
        
        total = self.stats['total_queue']
        for bucket, count in self.stats['bucket_counts'].items():
            rate = count / total * 100 if total > 0 else 0
            lines.append(f"| {bucket} | {count:,} | {rate:.1f}% |")
        
        lines.extend([
            "",
            "### 텍스트 길이 통계",
            "",
            "| 항목 | 값 |",
            "|------|-----|",
            f"| 평균 | {self.stats['text_len_mean']:.0f} 자 |",
            f"| 중앙값 | {self.stats['text_len_median']:.0f} 자 |",
            f"| p90 | {self.stats['text_len_p90']:.0f} 자 |",
            "",
            "---",
            "",
            "## 2. 버킷별 샘플",
            "",
        ])
        
        for bucket in ['GOLDEN_NUGGET', 'LOW_RATING', 'HELPFUL_LONG', 'RANDOM_CONTROL']:
            bucket_df = self.queue_df[self.queue_df['bucket'] == bucket].head(3)
            lines.append(f"### {bucket}")
            lines.append("")
            
            for _, row in bucket_df.iterrows():
                text_preview = row['input_text'][:100] + '...' if len(row['input_text']) > 100 else row['input_text']
                lines.extend([
                    f"- **{row['review_id']}** (priority={row['priority_score']:.2f})",
                    f"  - {text_preview}",
                    ""
                ])
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        logger.info(f"Generated report: {report_path}")
    
    def run(self):
        """전체 파이프라인 실행"""
        try:
            self.load_data()
            self.build_queue()
            self.save_output()
            self.generate_report()
            
            logger.info("=" * 50)
            logger.info("LLM Queue creation completed!")
            logger.info(f"Output: {self.output_path}")
            logger.info(f"Total items: {self.stats['total_queue']}")
            
        except Exception as e:
            logger.error(f"Error: {e}")
            raise


def main():
    parser = argparse.ArgumentParser(description="Step 3-2: LLM Queue 생성")
    parser.add_argument("--input", "-i", default="data/processed/reviews_step3_tagged.parquet")
    parser.add_argument("--out", "-o", default="data/llm/llm_queue.parquet")
    parser.add_argument("--report-dir", default="report")
    parser.add_argument("--max_golden", type=int, default=1500)
    parser.add_argument("--max_low", type=int, default=1500)
    parser.add_argument("--max_helpful", type=int, default=1000)
    parser.add_argument("--max_random", type=int, default=300)
    parser.add_argument("--max_chars", type=int, default=1200)
    parser.add_argument("--seed", type=int, default=42)
    
    args = parser.parse_args()
    
    builder = LLMQueueBuilder(
        input_path=args.input,
        output_path=args.out,
        report_dir=args.report_dir,
        max_golden=args.max_golden,
        max_low=args.max_low,
        max_helpful=args.max_helpful,
        max_random=args.max_random,
        max_chars=args.max_chars,
        seed=args.seed
    )
    builder.run()


if __name__ == "__main__":
    main()
