"""
Step 3-3: Gemini Extraction 전체 처리 (배치 버전)

전체 LLM Queue(4,052건)를 배치 처리로 추출.

Usage:
    python -m src.processing.llm_batch \
        --input data/llm/llm_queue.parquet \
        --out data/llm/extractions_full.parquet \
        --out_norm data/llm/extractions_full_normalized.parquet \
        --report report/step3_3_full_extraction.md \
        --batch_size 10
"""

import argparse
import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from collections import Counter

import pandas as pd
import numpy as np

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from google import genai
from google.genai import types

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


SYSTEM_INSTRUCTION = """너는 리뷰에서 '기대(Expectation)–경험(Experience)' 구조를 추출하는 분석기다.
여러 리뷰가 주어지면 각 리뷰별로 분석해서 배열로 반환해라.

규칙:
1. 주어진 텍스트에 근거한 내용만 추출. 추측/상상 금지.
2. 반드시 JSON만 출력. 코드펜스, 설명, 마크다운 금지.
3. evidence는 원문에서 짧게 발췌 (20~40자).
4. 한 리뷰에 여러 항목이 있으면 items 배열로 반환.
5. 명확한 기대-경험 쌍이 없으면 빈 items 배열 반환.

aspect 선택지:
WHITECAST, TONEUP, OILINESS, STICKINESS, PILLING, ABSORPTION, DRYNESS, MOISTURE, FLAKING, EYE_STING, IRRITATION, TROUBLE, SCENT, WATERPROOF, LONGEVITY, WHITE_RESIDUE, TEXTURE_HEAVY, TEXTURE_LIGHT, STAINING, OTHER

polarity 선택지:
- met: 기대가 충족됨
- unmet: 기대가 충족되지 않음
- mixed: 부분적으로 충족
- unknown: 판단 불가

출력 JSON:
{
  "reviews": [
    {
      "review_id": "<string>",
      "items": [
        {
          "aspect": "<aspect>",
          "expectation": "<기대. 없으면 null>",
          "experience": "<경험. 없으면 null>",
          "polarity": "<met|unmet|mixed|unknown>",
          "context": "<맥락. 없으면 null>",
          "evidence": "<원문 발췌 20~40자>",
          "confidence": <0.0~1.0>
        }
      ],
      "notes": "<특이사항. 없으면 null>"
    }
  ]
}"""


class FullBatchExtractor:
    """전체 배치 추출기"""
    
    def __init__(
        self,
        input_path: str,
        output_path: str,
        output_norm_path: str,
        report_path: str,
        model_name: str = "gemini-2.0-flash",
        fallback_model: str = "gemini-1.5-flash",
        batch_size: int = 10,
        rpm: int = 10,
        max_retries: int = 5,
        save_every: int = 50,
        force: bool = False
    ):
        self.input_path = input_path
        self.output_path = output_path
        self.output_norm_path = output_norm_path
        self.report_path = report_path
        self.model_name = model_name
        self.fallback_model = fallback_model
        self.batch_size = batch_size
        self.rpm = rpm
        self.max_retries = max_retries
        self.save_every = save_every
        self.force = force
        
        self.sleep_time = 60.0 / rpm
        
        self.queue_df: Optional[pd.DataFrame] = None
        self.results: List[Dict[str, Any]] = []
        self.processed_ids: set = set()
        self.response_times: List[float] = []
        
        self.stats = {
            'total_reviews': 0,
            'total_batches': 0,
            'success_batches': 0,
            'success_reviews': 0,
            'parse_error': 0,
            'api_error': 0,
            'rate_limit_error': 0,
            'empty_items': 0,
            'total_items': 0,
            'model_counts': Counter(),
            'total_prompt_tokens': 0,
            'total_output_tokens': 0,
        }
        
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set")
        
        self.client = genai.Client(api_key=api_key)
        logger.info(f"Initialized: model={model_name}, batch_size={batch_size}")
    
    def load_data(self):
        """데이터 로드 (기존 결과 이어받기)"""
        logger.info(f"Loading queue from {self.input_path}")
        self.queue_df = pd.read_parquet(self.input_path)
        logger.info(f"Total queue: {len(self.queue_df)}")
        
        # 기존 결과가 있으면 로드하고 이어서 처리
        if not self.force and os.path.exists(self.output_path):
            existing_df = pd.read_parquet(self.output_path)
            self.processed_ids = set(existing_df['review_id'].tolist())
            self.results = existing_df.to_dict('records')
            
            # 기존 통계 복원
            self.stats['success_reviews'] = len(existing_df[existing_df['parsed_ok']])
            
            logger.info(f"Resuming: {len(self.processed_ids)} already processed")
        
        # 처리할 데이터 필터링
        remaining = self.queue_df[~self.queue_df['review_id'].isin(self.processed_ids)]
        logger.info(f"Remaining to process: {len(remaining)}")
        
        return remaining
    
    def _parse_json(self, text: str) -> Optional[Dict]:
        if not text:
            return None
        text = text.strip()
        if text.startswith('```'):
            lines = text.split('\n')
            if lines[-1].strip() == '```':
                lines = lines[1:-1]
            else:
                lines = lines[1:]
            text = '\n'.join(lines)
        if text.endswith('```'):
            text = text[:-3]
        text = text.strip()
        try:
            return json.loads(text)
        except:
            return None
    
    def _build_batch_prompt(self, batch_df: pd.DataFrame) -> str:
        lines = []
        for _, row in batch_df.iterrows():
            lines.append(f"=== REVIEW_ID: {row['review_id']} ===")
            lines.append(row['input_text'])
            lines.append("")
        return '\n'.join(lines)
    
    def _call_api(self, prompt: str, model: str) -> Tuple[Optional[str], Optional[Dict], float]:
        start = time.time()
        try:
            response = self.client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.1,
                    max_output_tokens=4096,
                )
            )
            elapsed = time.time() - start
            usage = {}
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                usage['prompt_tokens'] = getattr(response.usage_metadata, 'prompt_token_count', 0)
                usage['output_tokens'] = getattr(response.usage_metadata, 'candidates_token_count', 0)
            return response.text, usage, elapsed
        except Exception as e:
            elapsed = time.time() - start
            if 'resource_exhausted' in str(e).lower() or '429' in str(e):
                raise RateLimitError(str(e))
            raise APIError(str(e))
    
    def _extract_batch(self, batch_df: pd.DataFrame) -> List[Dict[str, Any]]:
        prompt = self._build_batch_prompt(batch_df)
        
        batch_results = []
        for _, row in batch_df.iterrows():
            batch_results.append({
                'review_id': row['review_id'],
                'goods_no': row['goods_no'],
                'bucket': row['bucket'],
                'model_name': None,
                'extraction_json': None,
                'parsed_ok': False,
                'error_type': None,
                'error_message': None,
                'prompt_tokens': 0,
                'output_tokens': 0,
                'response_time': 0,
                'created_at': datetime.now().isoformat()
            })
        
        models = [self.model_name, self.fallback_model]
        
        for model in models:
            retry = 0
            backoff = 10
            
            while retry < self.max_retries:
                try:
                    response_text, usage, elapsed = self._call_api(prompt, model)
                    self.response_times.append(elapsed)
                    self.stats['model_counts'][model] += 1
                    
                    if usage:
                        self.stats['total_prompt_tokens'] += usage.get('prompt_tokens', 0)
                        self.stats['total_output_tokens'] += usage.get('output_tokens', 0)
                    
                    parsed = self._parse_json(response_text)
                    if parsed and 'reviews' in parsed:
                        reviews_data = {r['review_id']: r for r in parsed['reviews']}
                        
                        for res in batch_results:
                            rid = res['review_id']
                            if rid in reviews_data:
                                review_data = reviews_data[rid]
                                res['model_name'] = model
                                res['extraction_json'] = json.dumps(review_data, ensure_ascii=False)
                                res['parsed_ok'] = True
                                res['response_time'] = elapsed / len(batch_df)
                                
                                items = review_data.get('items', [])
                                if not items:
                                    self.stats['empty_items'] += 1
                                else:
                                    self.stats['total_items'] += len(items)
                                
                                self.stats['success_reviews'] += 1
                            else:
                                res['error_type'] = 'MISSING_IN_RESPONSE'
                        
                        self.stats['success_batches'] += 1
                        return batch_results
                    else:
                        self.stats['parse_error'] += 1
                        for res in batch_results:
                            res['error_type'] = 'JSON_PARSE'
                            res['error_message'] = response_text[:200] if response_text else None
                        return batch_results
                        
                except RateLimitError:
                    retry += 1
                    self.stats['rate_limit_error'] += 1
                    logger.warning(f"Rate limit, wait {backoff}s (retry {retry}/{self.max_retries})")
                    time.sleep(backoff)
                    backoff = min(backoff * 2, 120)
                    
                except APIError as e:
                    self.stats['api_error'] += 1
                    for res in batch_results:
                        res['error_type'] = 'API_ERROR'
                        res['error_message'] = str(e)[:200]
                    return batch_results
        
        return batch_results
    
    def run_extraction(self, df: pd.DataFrame):
        """추출 실행"""
        total = len(df)
        num_batches = (total + self.batch_size - 1) // self.batch_size
        
        logger.info(f"Processing {total} reviews in {num_batches} batches")
        self.stats['total_reviews'] = len(self.queue_df)
        self.stats['total_batches'] = num_batches
        
        for batch_idx in range(num_batches):
            start_idx = batch_idx * self.batch_size
            end_idx = min(start_idx + self.batch_size, total)
            batch_df = df.iloc[start_idx:end_idx]
            
            logger.info(f"Batch {batch_idx + 1}/{num_batches} ({start_idx}-{end_idx})")
            
            batch_results = self._extract_batch(batch_df)
            self.results.extend(batch_results)
            
            # 중간 저장
            if (batch_idx + 1) % self.save_every == 0:
                self._save_intermediate()
            
            if batch_idx < num_batches - 1:
                time.sleep(self.sleep_time)
        
        logger.info("Extraction completed")
    
    def _save_intermediate(self):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        df = pd.DataFrame(self.results)
        df.to_parquet(self.output_path, index=False)
        logger.info(f"Saved checkpoint: {len(self.results)} results")
    
    def save_output(self):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        df = pd.DataFrame(self.results)
        df.to_parquet(self.output_path, index=False)
        logger.info(f"Saved: {self.output_path}")
        
        # Normalized
        rows = []
        for result in self.results:
            if not result['parsed_ok'] or not result['extraction_json']:
                continue
            try:
                parsed = json.loads(result['extraction_json'])
                for item in parsed.get('items', []):
                    rows.append({
                        'review_id': result['review_id'],
                        'goods_no': result['goods_no'],
                        'bucket': result['bucket'],
                        'aspect': item.get('aspect'),
                        'expectation': item.get('expectation'),
                        'experience': item.get('experience'),
                        'polarity': item.get('polarity'),
                        'context': item.get('context'),
                        'evidence': item.get('evidence'),
                        'confidence': item.get('confidence'),
                    })
            except:
                continue
        
        if rows:
            norm_df = pd.DataFrame(rows)
            norm_df.to_parquet(self.output_norm_path, index=False)
            logger.info(f"Saved normalized: {len(norm_df)} items")
            self.stats['normalized_items'] = len(norm_df)
            self.norm_df = norm_df
        else:
            self.stats['normalized_items'] = 0
            self.norm_df = pd.DataFrame()
    
    def generate_report(self):
        os.makedirs(os.path.dirname(self.report_path), exist_ok=True)
        
        result_df = pd.DataFrame(self.results)
        total = len(result_df)
        parse_success = result_df['parsed_ok'].sum()
        parse_rate = (parse_success / total * 100) if total > 0 else 0
        
        lines = [
            "# Step 3-3: Full Extraction Report",
            "",
            f"생성: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary",
            "",
            f"| 항목 | 값 |",
            f"|------|-----|",
            f"| 총 리뷰 | {total:,} |",
            f"| 파싱 성공 | {parse_success:,} ({parse_rate:.1f}%) |",
            f"| 정규화 항목 | {self.stats.get('normalized_items', 0):,} |",
            f"| Prompt tokens | {self.stats['total_prompt_tokens']:,} |",
            f"| Output tokens | {self.stats['total_output_tokens']:,} |",
            "",
        ]
        
        # Polarity by bucket
        if hasattr(self, 'norm_df') and len(self.norm_df) > 0:
            lines.append("## Polarity by Bucket")
            lines.append("")
            for bucket in ['GOLDEN_NUGGET', 'LOW_RATING', 'HELPFUL_LONG', 'RANDOM_CONTROL']:
                bucket_data = self.norm_df[self.norm_df['bucket'] == bucket]
                if len(bucket_data) > 0:
                    pol = bucket_data['polarity'].value_counts(normalize=True) * 100
                    pol_str = ', '.join([f"{p}: {pol.get(p, 0):.1f}%" for p in ['met', 'unmet', 'mixed']])
                    lines.append(f"- **{bucket}**: {pol_str}")
            lines.append("")
        
        with open(self.report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        logger.info(f"Report: {self.report_path}")
    
    def run(self):
        try:
            remaining = self.load_data()
            
            if len(remaining) == 0:
                logger.info("All items already processed!")
                return
            
            self.run_extraction(remaining)
            self.save_output()
            self.generate_report()
            
            logger.info("=" * 50)
            logger.info(f"Done! Success: {self.stats['success_reviews']}/{len(self.results)}")
            
        except Exception as e:
            logger.error(f"Error: {e}")
            self._save_intermediate()
            raise


class RateLimitError(Exception):
    pass

class APIError(Exception):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", default="data/llm/llm_queue.parquet")
    parser.add_argument("--out", "-o", default="data/llm/extractions_full.parquet")
    parser.add_argument("--out_norm", default="data/llm/extractions_full_normalized.parquet")
    parser.add_argument("--report", default="report/step3_3_full_extraction.md")
    parser.add_argument("--model", default="gemini-2.0-flash")
    parser.add_argument("--fallback_model", default="gemini-1.5-flash")
    parser.add_argument("--batch_size", type=int, default=10)
    parser.add_argument("--rpm", type=int, default=10)
    parser.add_argument("--max_retries", type=int, default=5)
    parser.add_argument("--save_every", type=int, default=50)
    parser.add_argument("--force", action="store_true")
    
    args = parser.parse_args()
    
    extractor = FullBatchExtractor(
        input_path=args.input,
        output_path=args.out,
        output_norm_path=args.out_norm,
        report_path=args.report,
        model_name=args.model,
        fallback_model=args.fallback_model,
        batch_size=args.batch_size,
        rpm=args.rpm,
        max_retries=args.max_retries,
        save_every=args.save_every,
        force=args.force
    )
    extractor.run()


if __name__ == "__main__":
    main()
