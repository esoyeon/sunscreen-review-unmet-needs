"""
Step 3-1 v2: Advanced Tagging 스크립트

Attribute/Context/Skin 태깅, Conditional 탐지, Negation handling, Golden Nugget 식별.
원문 보존, 태그와 플래그로만 통제.

Usage:
    python -m src.processing.tagging \
        --input data/processed/reviews_step3_dedup.parquet \
        --out data/processed/reviews_step3_tagged.parquet \
        --lexicon config/tag_lexicon_v2.yaml
"""

import argparse
import json
import logging
import os
import re
from datetime import datetime
from typing import List, Dict, Any, Optional, Set, Tuple
from collections import Counter

import pandas as pd
import numpy as np
import yaml

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TagLexicon:
    """태그 사전 로더 및 패턴 컴파일러"""
    
    def __init__(self, lexicon_path: str):
        with open(lexicon_path, 'r', encoding='utf-8') as f:
            self.data = yaml.safe_load(f)
        
        self.meta = self.data.get('meta', {})
        self.negation_window = self.meta.get('negation_window_chars', 12)
        self.negation_targets = set(self.meta.get('negation_target_tags', []))
        
        # 컴파일된 패턴 저장
        self.attribute_patterns: Dict[str, re.Pattern] = {}
        self.context_patterns: Dict[str, re.Pattern] = {}
        self.skin_patterns: Dict[str, re.Pattern] = {}
        self.conditional_patterns: Dict[str, re.Pattern] = {}
        self.negation_pattern: Optional[re.Pattern] = None
        
        self._compile_patterns()
    
    def _compile_patterns(self):
        """모든 패턴 컴파일"""
        # Attributes
        for group, tags in self.data.get('attributes', {}).items():
            for tag, pattern in tags.items():
                self.attribute_patterns[tag] = re.compile(pattern, re.IGNORECASE)
        
        # Contexts
        for group, tags in self.data.get('contexts', {}).items():
            for tag, pattern in tags.items():
                self.context_patterns[tag] = re.compile(pattern, re.IGNORECASE)
        
        # Skins
        for group, tags in self.data.get('skins', {}).items():
            for tag, pattern in tags.items():
                self.skin_patterns[tag] = re.compile(pattern, re.IGNORECASE)
        
        # Conditional markers
        for marker, pattern in self.data.get('conditional_markers', {}).items():
            self.conditional_patterns[marker] = re.compile(pattern, re.IGNORECASE)
        
        # Negations (combined pattern)
        negations = self.data.get('negations', [])
        if negations:
            combined = '|'.join(f'({n})' for n in negations)
            self.negation_pattern = re.compile(combined, re.IGNORECASE)
    
    def get_tag_order(self) -> Dict[str, List[str]]:
        """정렬 순서용 태그 목록"""
        order = {
            'attributes': [],
            'contexts': [],
            'skins': []
        }
        
        for group, tags in self.data.get('attributes', {}).items():
            order['attributes'].extend(tags.keys())
        for group, tags in self.data.get('contexts', {}).items():
            order['contexts'].extend(tags.keys())
        for group, tags in self.data.get('skins', {}).items():
            order['skins'].extend(tags.keys())
        
        return order


class ReviewTagger:
    """리뷰 태깅 엔진"""
    
    def __init__(self, lexicon: TagLexicon):
        self.lexicon = lexicon
        self.tag_order = lexicon.get_tag_order()
    
    def _sort_tags(self, tags: Set[str], category: str) -> List[str]:
        """태그 정렬 (사전 정의 순서)"""
        order = self.tag_order.get(category, [])
        order_map = {t: i for i, t in enumerate(order)}
        return sorted(list(tags), key=lambda x: order_map.get(x, 999))
    
    def tag_attributes(self, text: str) -> Tuple[List[str], List[Tuple[str, int, int]]]:
        """속성 태그 매칭 (위치 정보 포함)"""
        tags = set()
        mentions = []  # (tag, start, end)
        
        for tag, pattern in self.lexicon.attribute_patterns.items():
            for match in pattern.finditer(text):
                tags.add(tag)
                mentions.append((tag, match.start(), match.end()))
        
        return self._sort_tags(tags, 'attributes'), mentions
    
    def tag_contexts(self, text: str) -> List[str]:
        """맥락 태그 매칭"""
        tags = set()
        for tag, pattern in self.lexicon.context_patterns.items():
            if pattern.search(text):
                tags.add(tag)
        return self._sort_tags(tags, 'contexts')
    
    def tag_skins(self, text: str) -> List[str]:
        """피부 태그 매칭"""
        tags = set()
        for tag, pattern in self.lexicon.skin_patterns.items():
            if pattern.search(text):
                tags.add(tag)
        return self._sort_tags(tags, 'skins')
    
    def detect_conditional(self, text: str) -> Tuple[bool, List[str]]:
        """조건부 마커 탐지"""
        markers = []
        for marker, pattern in self.lexicon.conditional_patterns.items():
            if pattern.search(text):
                markers.append(marker)
        return len(markers) > 0, sorted(markers)
    
    def analyze_polarity(self, text: str, mentions: List[Tuple[str, int, int]]) -> Dict[str, str]:
        """Negation 분석 (부정어 극성 판단)"""
        polarity = {}
        
        if not self.lexicon.negation_pattern:
            return polarity
        
        window = self.lexicon.negation_window
        
        # 타겟 태그만 분석
        target_mentions = [(t, s, e) for t, s, e in mentions if t in self.lexicon.negation_targets]
        
        # 태그별로 그룹화
        tag_positions = {}
        for tag, start, end in target_mentions:
            if tag not in tag_positions:
                tag_positions[tag] = []
            tag_positions[tag].append((start, end))
        
        for tag, positions in tag_positions.items():
            polarities = []
            
            for start, end in positions:
                # 앞뒤 window 범위에서 부정어 검색
                context_start = max(0, start - window)
                context_end = min(len(text), end + window)
                context = text[context_start:context_end]
                
                if self.lexicon.negation_pattern.search(context):
                    polarities.append('negated')
                else:
                    polarities.append('affirmed')
            
            # 최종 극성 결정
            if all(p == 'negated' for p in polarities):
                polarity[tag] = 'negated'
            elif all(p == 'affirmed' for p in polarities):
                polarity[tag] = 'affirmed'
            elif polarities:
                polarity[tag] = 'mixed'
        
        return polarity
    
    def process_review(self, row: pd.Series) -> Dict[str, Any]:
        """단일 리뷰 처리"""
        # 입력 텍스트 준비
        base_text = row.get('review_text_clean', '') or ''
        
        # 피부 힌트 텍스트
        skin_hints = []
        for col in ['skin_type_raw', 'skin_tone_raw', 'skin_trouble_raw']:
            val = row.get(col)
            # None, NaN, 빈 값 체크
            if val is None:
                continue
            if isinstance(val, float) and pd.isna(val):
                continue
            if isinstance(val, (list, np.ndarray)):
                if len(val) > 0:
                    skin_hints.extend([str(v) for v in val if v])
            elif isinstance(val, str) and val:
                skin_hints.append(val)
        skin_hint_text = ' '.join(skin_hints)
        
        # 태깅
        attr_tags, attr_mentions = self.tag_attributes(base_text)
        ctx_tags = self.tag_contexts(base_text)
        skin_tags = self.tag_skins(base_text + ' ' + skin_hint_text)
        
        # Conditional 탐지
        has_conditional, cond_markers = self.detect_conditional(base_text)
        
        # Negation polarity
        polarity = self.analyze_polarity(base_text, attr_mentions)
        
        # Mention 태그 (위치 정보 제거)
        mention_tags = sorted(list(set(t for t, _, _ in attr_mentions)))
        
        # Toneup vs Whitecast 충돌
        toneup_whitecast_conflict = False
        if 'TONEUP' in attr_tags and 'WHITECAST' in mention_tags:
            wc_polarity = polarity.get('WHITECAST', 'unknown')
            if has_conditional or wc_polarity in ['affirmed', 'mixed']:
                toneup_whitecast_conflict = True
        
        # Golden Nugget
        rating_bucket = row.get('rating_bucket', '')
        text_len = row.get('text_len_chars', 0) or 0
        is_low_info = row.get('is_low_info', 0)
        
        golden_nugget = (
            rating_bucket == 'high' and
            has_conditional and
            text_len >= 100 and
            is_low_info == 0
        )
        
        return {
            'attribute_tags': attr_tags,
            'attribute_tags_str': '|'.join(attr_tags) if attr_tags else None,
            'context_tags': ctx_tags,
            'context_tags_str': '|'.join(ctx_tags) if ctx_tags else None,
            'skin_tags': skin_tags,
            'skin_tags_str': '|'.join(skin_tags) if skin_tags else None,
            'has_conditional': has_conditional,
            'conditional_markers': cond_markers,
            'conditional_markers_str': '|'.join(cond_markers) if cond_markers else None,
            'attribute_mentions': mention_tags,
            'attribute_polarity': json.dumps(polarity, ensure_ascii=False) if polarity else None,
            'toneup_whitecast_conflict': toneup_whitecast_conflict,
            'golden_nugget': golden_nugget,
            'has_attribute_tag': len(attr_tags) > 0,
            'has_context_tag': len(ctx_tags) > 0,
            'has_skin_tag': len(skin_tags) > 0,
        }


class TaggingPipeline:
    """태깅 파이프라인"""
    
    def __init__(self, input_path: str, output_path: str, lexicon_path: str, report_dir: str):
        self.input_path = input_path
        self.output_path = output_path
        self.lexicon_path = lexicon_path
        self.report_dir = report_dir
        
        self.df: Optional[pd.DataFrame] = None
        self.lexicon: Optional[TagLexicon] = None
        self.tagger: Optional[ReviewTagger] = None
        self.stats: Dict[str, Any] = {}
    
    def load_data(self):
        """데이터 및 사전 로드"""
        logger.info(f"Loading lexicon from {self.lexicon_path}")
        self.lexicon = TagLexicon(self.lexicon_path)
        self.tagger = ReviewTagger(self.lexicon)
        
        logger.info(f"Loading data from {self.input_path}")
        self.df = pd.read_parquet(self.input_path)
        logger.info(f"Loaded {len(self.df)} reviews")
    
    def run_tagging(self):
        """태깅 실행"""
        logger.info("Running tagging...")
        
        results = []
        total = len(self.df)
        
        for idx, row in self.df.iterrows():
            if idx % 1000 == 0:
                logger.info(f"Processing {idx}/{total}...")
            
            result = self.tagger.process_review(row)
            results.append(result)
        
        # 결과 병합
        result_df = pd.DataFrame(results)
        self.df = pd.concat([self.df.reset_index(drop=True), result_df], axis=1)
        
        logger.info("Tagging completed")
    
    def compute_stats(self):
        """통계 계산"""
        logger.info("Computing statistics...")
        
        total = len(self.df)
        self.stats['total_reviews'] = total
        self.stats['unique_goods'] = self.df['goods_no'].nunique()
        
        # Coverage
        self.stats['attr_coverage'] = self.df['has_attribute_tag'].sum() / total * 100
        self.stats['ctx_coverage'] = self.df['has_context_tag'].sum() / total * 100
        self.stats['skin_coverage'] = self.df['has_skin_tag'].sum() / total * 100
        
        # Conditional
        self.stats['conditional_rate'] = self.df['has_conditional'].sum() / total * 100
        
        # Rating별 conditional
        cond_by_rating = self.df.groupby('rating_bucket')['has_conditional'].mean() * 100
        self.stats['conditional_by_rating'] = cond_by_rating.to_dict()
        
        # Golden nugget
        self.stats['golden_nugget_count'] = self.df['golden_nugget'].sum()
        self.stats['golden_nugget_rate'] = self.stats['golden_nugget_count'] / total * 100
        
        # Non-trial golden nugget
        non_trial_gn = (self.df['golden_nugget'] & (self.df['is_trial'] == 0)).sum()
        self.stats['golden_nugget_non_trial'] = non_trial_gn
        
        # Top attribute tags
        attr_counter = Counter()
        for tags in self.df['attribute_tags']:
            if tags:
                attr_counter.update(tags)
        self.stats['top_attr_tags'] = attr_counter.most_common(20)
        
        # Low rating attribute tags
        low_attr_counter = Counter()
        for tags in self.df[self.df['rating_bucket'] == 'low']['attribute_tags']:
            if tags:
                low_attr_counter.update(tags)
        self.stats['top_attr_low'] = low_attr_counter.most_common(20)
        
        # High rating + conditional
        high_cond = self.df[(self.df['rating_bucket'] == 'high') & (self.df['has_conditional'])]
        high_cond_counter = Counter()
        for tags in high_cond['attribute_tags']:
            if tags:
                high_cond_counter.update(tags)
        self.stats['top_attr_high_cond'] = high_cond_counter.most_common(20)
        
        # Top context tags
        ctx_counter = Counter()
        for tags in self.df['context_tags']:
            if tags:
                ctx_counter.update(tags)
        self.stats['top_ctx_tags'] = ctx_counter.most_common(20)
        
        # Top skin tags
        skin_counter = Counter()
        for tags in self.df['skin_tags']:
            if tags:
                skin_counter.update(tags)
        self.stats['top_skin_tags'] = skin_counter.most_common(20)
        
        # Polarity distribution (WHITECAST)
        wc_polarity = {'affirmed': 0, 'negated': 0, 'mixed': 0, 'unknown': 0}
        for pol_json in self.df['attribute_polarity'].dropna():
            pol = json.loads(pol_json)
            if 'WHITECAST' in pol:
                wc_polarity[pol['WHITECAST']] += 1
        self.stats['whitecast_polarity'] = wc_polarity
        
        # EYE_STING polarity
        es_polarity = {'affirmed': 0, 'negated': 0, 'mixed': 0, 'unknown': 0}
        for pol_json in self.df['attribute_polarity'].dropna():
            pol = json.loads(pol_json)
            if 'EYE_STING' in pol:
                es_polarity[pol['EYE_STING']] += 1
        self.stats['eye_sting_polarity'] = es_polarity
        
        # Toneup/Whitecast conflict
        self.stats['toneup_whitecast_conflict_count'] = self.df['toneup_whitecast_conflict'].sum()
        
        # Co-occurrence: Skin -> Attribute
        skin_attr_cooc = {}
        for i, row in self.df.iterrows():
            skin_tags = row['skin_tags'] or []
            attr_tags = row['attribute_tags'] or []
            for skin in skin_tags:
                if skin not in skin_attr_cooc:
                    skin_attr_cooc[skin] = Counter()
                skin_attr_cooc[skin].update(attr_tags)
        self.stats['skin_attr_cooc'] = {k: v.most_common(5) for k, v in skin_attr_cooc.items()}
        
        # Co-occurrence: Context -> Attribute
        ctx_attr_cooc = {}
        for i, row in self.df.iterrows():
            ctx_tags = row['context_tags'] or []
            attr_tags = row['attribute_tags'] or []
            for ctx in ctx_tags:
                if ctx not in ctx_attr_cooc:
                    ctx_attr_cooc[ctx] = Counter()
                ctx_attr_cooc[ctx].update(attr_tags)
        self.stats['ctx_attr_cooc'] = {k: v.most_common(5) for k, v in ctx_attr_cooc.items()}
    
    def save_output(self):
        """결과 저장"""
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        self.df.to_parquet(self.output_path, index=False, engine='pyarrow')
        logger.info(f"Saved tagged data to {self.output_path}")
    
    def generate_report(self):
        """QA 리포트 생성"""
        os.makedirs(self.report_dir, exist_ok=True)
        report_path = os.path.join(self.report_dir, "step3_1_tagging.md")
        
        lines = [
            "# Step 3-1 v2: Advanced Tagging 리포트",
            "",
            f"생성 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
            "## 1. 기본 요약",
            "",
            "| 항목 | 값 |",
            "|------|-----|",
            f"| 총 리뷰 수 | {self.stats['total_reviews']:,} |",
            f"| 상품 수 | {self.stats['unique_goods']:,} |",
            f"| Attribute 커버리지 | {self.stats['attr_coverage']:.1f}% |",
            f"| Context 커버리지 | {self.stats['ctx_coverage']:.1f}% |",
            f"| Skin 커버리지 | {self.stats['skin_coverage']:.1f}% |",
            "",
            "### Conditional 비율",
            "",
            f"- 전체: {self.stats['conditional_rate']:.1f}%",
        ]
        
        for rating, rate in self.stats['conditional_by_rating'].items():
            lines.append(f"- {rating}: {rate:.1f}%")
        
        lines.extend([
            "",
            "### Golden Nugget",
            "",
            f"| 항목 | 값 |",
            f"|------|-----|",
            f"| Golden Nugget 건수 | {self.stats['golden_nugget_count']:,} ({self.stats['golden_nugget_rate']:.1f}%) |",
            f"| Non-trial Golden Nugget | {self.stats['golden_nugget_non_trial']:,} |",
            f"| Toneup/Whitecast 충돌 | {self.stats['toneup_whitecast_conflict_count']:,} |",
            "",
            "---",
            "",
            "## 2. Negation 품질 점검",
            "",
            "### WHITECAST Polarity 분포",
            "",
            "| Polarity | 건수 |",
            "|----------|------|",
        ])
        
        for pol, count in self.stats['whitecast_polarity'].items():
            lines.append(f"| {pol} | {count:,} |")
        
        lines.extend([
            "",
            "### EYE_STING Polarity 분포",
            "",
            "| Polarity | 건수 |",
            "|----------|------|",
        ])
        
        for pol, count in self.stats['eye_sting_polarity'].items():
            lines.append(f"| {pol} | {count:,} |")
        
        # 백탁 없 샘플
        lines.extend([
            "",
            "### '백탁 없음' 샘플 (negated WHITECAST)",
            "",
        ])
        
        negated_samples = []
        for idx, row in self.df.iterrows():
            if row['attribute_polarity']:
                pol = json.loads(row['attribute_polarity'])
                if pol.get('WHITECAST') == 'negated':
                    text = row['review_text_clean'][:100] if row['review_text_clean'] else ''
                    negated_samples.append(f"- `{row['review_id']}`: {text}...")
                    if len(negated_samples) >= 10:
                        break
        
        lines.extend(negated_samples if negated_samples else ["(샘플 없음)"])
        
        # Top tags
        lines.extend([
            "",
            "---",
            "",
            "## 3. Top 태그 빈도",
            "",
            "### Attribute Tags (전체 Top 20)",
            "",
            "| Tag | 건수 |",
            "|-----|------|",
        ])
        
        for tag, count in self.stats['top_attr_tags']:
            lines.append(f"| {tag} | {count:,} |")
        
        lines.extend([
            "",
            "### Attribute Tags (Low Rating Top 10)",
            "",
            "| Tag | 건수 |",
            "|-----|------|",
        ])
        
        for tag, count in self.stats['top_attr_low'][:10]:
            lines.append(f"| {tag} | {count:,} |")
        
        lines.extend([
            "",
            "### Attribute Tags (High Rating + Conditional Top 10)",
            "",
            "| Tag | 건수 |",
            "|-----|------|",
        ])
        
        for tag, count in self.stats['top_attr_high_cond'][:10]:
            lines.append(f"| {tag} | {count:,} |")
        
        lines.extend([
            "",
            "### Context Tags (Top 15)",
            "",
            "| Tag | 건수 |",
            "|-----|------|",
        ])
        
        for tag, count in self.stats['top_ctx_tags'][:15]:
            lines.append(f"| {tag} | {count:,} |")
        
        lines.extend([
            "",
            "### Skin Tags (Top 15)",
            "",
            "| Tag | 건수 |",
            "|-----|------|",
        ])
        
        for tag, count in self.stats['top_skin_tags'][:15]:
            lines.append(f"| {tag} | {count:,} |")
        
        # Co-occurrence
        lines.extend([
            "",
            "---",
            "",
            "## 4. Co-occurrence 분석",
            "",
            "### Skin → Attribute Top 5",
            "",
        ])
        
        for skin, attrs in list(self.stats['skin_attr_cooc'].items())[:8]:
            attr_str = ', '.join([f"{a}({c})" for a, c in attrs])
            lines.append(f"- **{skin}**: {attr_str}")
        
        lines.extend([
            "",
            "### Context → Attribute Top 5",
            "",
        ])
        
        for ctx, attrs in list(self.stats['ctx_attr_cooc'].items())[:8]:
            attr_str = ', '.join([f"{a}({c})" for a, c in attrs])
            lines.append(f"- **{ctx}**: {attr_str}")
        
        # 샘플 20개
        lines.extend([
            "",
            "---",
            "",
            "## 5. 예시 샘플 20개",
            "",
        ])
        
        sample_df = self.df.sample(n=min(20, len(self.df)), random_state=42)
        for idx, row in sample_df.iterrows():
            text_preview = (row['review_text_clean'][:80] + '...') if row['review_text_clean'] and len(row['review_text_clean']) > 80 else (row['review_text_clean'] or '')
            lines.extend([
                f"### {row['review_id']}",
                f"- **Rating**: {row['rating']} ({row['rating_bucket']})",
                f"- **Season**: {row['season']}",
                f"- **Attributes**: {row['attribute_tags_str'] or '-'}",
                f"- **Contexts**: {row['context_tags_str'] or '-'}",
                f"- **Skins**: {row['skin_tags_str'] or '-'}",
                f"- **Conditional**: {row['has_conditional']} ({row['conditional_markers_str'] or '-'})",
                f"- **Golden Nugget**: {row['golden_nugget']}",
                f"- **Text**: {text_preview}",
                "",
            ])
        
        # 저장
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        logger.info(f"Generated report: {report_path}")
    
    def run(self):
        """전체 파이프라인 실행"""
        try:
            self.load_data()
            self.run_tagging()
            self.compute_stats()
            self.save_output()
            self.generate_report()
            
            logger.info("=" * 50)
            logger.info("Tagging completed successfully!")
            logger.info(f"Output: {self.output_path}")
            logger.info(f"Golden Nuggets: {self.stats['golden_nugget_count']}")
            
        except Exception as e:
            logger.error(f"Error during tagging: {e}")
            import traceback
            traceback.print_exc()
            raise


def main():
    parser = argparse.ArgumentParser(description="Step 3-1 v2: Advanced Tagging")
    parser.add_argument("--input", "-i", default="data/processed/reviews_step3_dedup.parquet")
    parser.add_argument("--out", "-o", default="data/processed/reviews_step3_tagged.parquet")
    parser.add_argument("--lexicon", "-l", default="config/tag_lexicon_v2.yaml")
    parser.add_argument("--report-dir", default="report")
    
    args = parser.parse_args()
    
    pipeline = TaggingPipeline(
        input_path=args.input,
        output_path=args.out,
        lexicon_path=args.lexicon,
        report_dir=args.report_dir
    )
    pipeline.run()


if __name__ == "__main__":
    main()
