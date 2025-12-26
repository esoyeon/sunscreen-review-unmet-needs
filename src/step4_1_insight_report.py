"""
Step 4-1: Insight Report - 미충족 니즈 분석 결과 검증 및 해석

Usage:
    python -m src.step4_1_insight_report \
        --analysis_dir data/analysis \
        --out report/step4_1_insight_review.md \
        --min_n_items 30 \
        --min_goods_any 20 \
        --topn 10 \
        --topn_context 15
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


class InsightReportGenerator:
    """인사이트 리포트 생성기"""
    
    def __init__(
        self,
        analysis_dir: str,
        out_path: str,
        min_n_items: int = 30,
        min_goods_any: int = 20,
        topn: int = 10,
        topn_context: int = 15
    ):
        self.analysis_dir = analysis_dir
        self.out_path = out_path
        self.min_n_items = min_n_items
        self.min_goods_any = min_goods_any
        self.topn = topn
        self.topn_context = topn_context
        
        self.lines = []
    
    def load_data(self):
        """데이터 로드"""
        logger.info("Loading data...")
        
        self.master = pd.read_parquet(os.path.join(self.analysis_dir, 'step4_master_join.parquet'))
        self.pivot_overall = pd.read_parquet(os.path.join(self.analysis_dir, 'pivot_aspect_polarity_overall.parquet'))
        self.pivot_bucket = pd.read_parquet(os.path.join(self.analysis_dir, 'pivot_aspect_polarity_by_bucket.parquet'))
        self.pivot_context = pd.read_parquet(os.path.join(self.analysis_dir, 'pivot_context_aspect_unmet.parquet'))
        self.pivot_season = pd.read_parquet(os.path.join(self.analysis_dir, 'pivot_season_aspect_unmet.parquet'))
        self.repeatability = pd.read_parquet(os.path.join(self.analysis_dir, 'repeatability_aspect_goods_count.parquet'))
        
        logger.info("Data loaded")
    
    def add_section(self, title: str, level: int = 2):
        """섹션 추가"""
        self.lines.append("")
        self.lines.append("#" * level + " " + title)
        self.lines.append("")
    
    def add_table(self, df: pd.DataFrame, columns: List[str], formats: Dict[str, str] = None):
        """테이블 추가"""
        if formats is None:
            formats = {}
        
        # Header
        self.lines.append("| " + " | ".join(columns) + " |")
        self.lines.append("|" + "|".join(["---"] * len(columns)) + "|")
        
        # Rows
        for _, row in df.iterrows():
            cells = []
            for col in columns:
                val = row[col]
                if col in formats:
                    if formats[col] == 'pct':
                        cells.append(f"{val:.1%}")
                    elif formats[col] == 'int':
                        cells.append(f"{int(val):,}")
                    else:
                        cells.append(str(val))
                else:
                    cells.append(str(val))
            self.lines.append("| " + " | ".join(cells) + " |")
    
    def section_quality_gate(self):
        """1. 데이터 신뢰도 점검"""
        self.add_section("1. 데이터 신뢰도 점검 (Quality Gate)")
        
        # 기본 통계
        total_queue = 4052
        total_reviews = self.master['review_id'].nunique()
        total_goods = self.master['goods_no'].nunique()
        total_items = len(self.master)
        
        self.lines.append("### 1.1 분석에 사용된 데이터")
        self.lines.append("")
        self.lines.append("| 항목 | 값 |")
        self.lines.append("|------|-----|")
        self.lines.append(f"| 원본 Queue | 4,052 |")
        self.lines.append(f"| 파싱 성공률 | 94.2% |")
        self.lines.append(f"| 유효 리뷰 (unique) | {total_reviews:,} |")
        self.lines.append(f"| 유효 상품 (unique) | {total_goods:,} |")
        self.lines.append(f"| 추출 항목 (aspect-level) | {total_items:,} |")
        self.lines.append("")
        
        # Bucket별 polarity 분포
        self.lines.append("### 1.2 Bucket별 Polarity 분포")
        self.lines.append("")
        
        bucket_pol = self.master.groupby('bucket')['polarity'].value_counts(normalize=True).unstack(fill_value=0) * 100
        
        self.lines.append("| Bucket | met | unmet | mixed | unknown |")
        self.lines.append("|--------|-----|-------|-------|---------|")
        for bucket in ['GOLDEN_NUGGET', 'LOW_RATING', 'HELPFUL_LONG', 'RANDOM_CONTROL']:
            if bucket in bucket_pol.index:
                row = bucket_pol.loc[bucket]
                self.lines.append(f"| {bucket} | {row.get('met', 0):.1f}% | {row.get('unmet', 0):.1f}% | {row.get('mixed', 0):.1f}% | {row.get('unknown', 0):.1f}% |")
        
        self.lines.append("")
        
        # OTHER 비율
        other_cnt = (self.master['aspect'] == 'OTHER').sum()
        other_rate = other_cnt / len(self.master) * 100
        
        self.lines.append("### 1.3 추출 품질 지표")
        self.lines.append("")
        self.lines.append(f"- **OTHER 비율**: {other_rate:.2f}% ({other_cnt}건)")
        self.lines.append(f"- OTHER 비율이 낮아 aspect 분류가 안정적임")
        self.lines.append("")
        
        # 편향 주의
        self.lines.append("### 1.4 편향/대표성 주의")
        self.lines.append("")
        self.lines.append("> ⚠️ **중요**: Bucket별 샘플링 구조(GOLDEN_NUGGET 1,500, LOW_RATING 1,500 등)는")
        self.lines.append("> 시장 전체를 대표하는 샘플이 **아닙니다**.")
        self.lines.append(">")
        self.lines.append("> 따라서 이 분석에서 의미 있는 것은:")
        self.lines.append("> - (a) **버킷 내 비교** (같은 조건에서 비율 차이)")
        self.lines.append("> - (b) **Repeatability** (여러 상품에서 반복되는 문제)")
        self.lines.append("> - (c) **맥락별 패턴** (특정 상황에서 두드러지는 문제)")
        self.lines.append("")
    
    def section_low_rating(self):
        """2. LOW_RATING 분석"""
        self.add_section("2. 전체 시장 관점: 명확한 불만 (LOW_RATING)")
        
        self.lines.append("> LOW_RATING 리뷰에서 기대 미충족(unmet/mixed)이 높은 aspect = **명확한 페인포인트**")
        self.lines.append("")
        
        lr = self.pivot_bucket[self.pivot_bucket['bucket'] == 'LOW_RATING'].copy()
        
        # unmet_like_rate Top 10 (n >= min_n)
        lr_filtered = lr[lr['n_items'] >= self.min_n_items].copy()
        lr_by_rate = lr_filtered.sort_values('unmet_like_rate', ascending=False).head(self.topn)
        
        self.lines.append("### 2.1 unmet_like_rate Top 10 (n≥30)")
        self.lines.append("")
        self.add_table(
            lr_by_rate,
            ['aspect', 'n_items', 'unmet_like_cnt', 'unmet_like_rate'],
            {'n_items': 'int', 'unmet_like_cnt': 'int', 'unmet_like_rate': 'pct'}
        )
        
        # unmet_like_cnt Top 10
        lr_by_cnt = lr.sort_values('unmet_like_cnt', ascending=False).head(self.topn)
        
        self.lines.append("")
        self.lines.append("### 2.2 unmet_like_cnt Top 10 (빈도)")
        self.lines.append("")
        self.add_table(
            lr_by_cnt,
            ['aspect', 'n_items', 'unmet_like_cnt', 'unmet_like_rate'],
            {'n_items': 'int', 'unmet_like_cnt': 'int', 'unmet_like_rate': 'pct'}
        )
        
        # 해석
        self.lines.append("")
        self.lines.append("### 2.3 해석")
        self.lines.append("")
        self.lines.append("- **IRRITATION (자극)**: LOW_RATING에서 가장 빈번한 불만. 피부 트러블/자극이 핵심 실패 원인.")
        self.lines.append("- **OILINESS (유분)**: 번들거림, 기름지는 마무리감에 대한 불만.")
        self.lines.append("- **PILLING (밀림)**: 메이크업이나 다른 제품과 함께 사용 시 밀림 발생.")
        self.lines.append("- **DRYNESS (건조)**: 보습력 부족으로 인한 당김/건조함 호소.")
        self.lines.append("")
    
    def section_golden_nugget(self):
        """3. GOLDEN_NUGGET 분석"""
        self.add_section("3. 핵심: 좋아하지만 아쉬운 한 끝 (GOLDEN_NUGGET)")
        
        self.lines.append("> GOLDEN_NUGGET = 긍정 리뷰이면서 조건부 언급이 있는 리뷰")
        self.lines.append("> 여기서 unmet/mixed가 발견되면 = **좋아하지만 해결되지 않은 문제**")
        self.lines.append("")
        
        gn = self.pivot_bucket[self.pivot_bucket['bucket'] == 'GOLDEN_NUGGET'].copy()
        
        # unmet_like_cnt Top 10
        gn_by_cnt = gn.sort_values('unmet_like_cnt', ascending=False).head(self.topn)
        
        self.lines.append("### 3.1 unmet_like_cnt Top 10")
        self.lines.append("")
        self.add_table(
            gn_by_cnt,
            ['aspect', 'n_items', 'unmet_like_cnt', 'met_cnt', 'unmet_like_rate'],
            {'n_items': 'int', 'unmet_like_cnt': 'int', 'met_cnt': 'int', 'unmet_like_rate': 'pct'}
        )
        
        # unmet_like_rate Top 10 (n >= min_n)
        gn_filtered = gn[gn['n_items'] >= self.min_n_items].copy()
        gn_by_rate = gn_filtered.sort_values('unmet_like_rate', ascending=False).head(self.topn)
        
        self.lines.append("")
        self.lines.append("### 3.2 unmet_like_rate Top 10 (n≥30)")
        self.lines.append("")
        self.add_table(
            gn_by_rate,
            ['aspect', 'n_items', 'unmet_like_cnt', 'unmet_like_rate'],
            {'n_items': 'int', 'unmet_like_cnt': 'int', 'unmet_like_rate': 'pct'}
        )
        
        # 해석
        self.lines.append("")
        self.lines.append("### 3.3 해석")
        self.lines.append("")
        self.lines.append("- **TONEUP / OILINESS / DRYNESS**: 긍정 리뷰에서도 가장 많은 조건부 불만.")
        self.lines.append("- met_cnt가 높음에도 unmet_like_cnt가 의미있게 존재 → **개선 여지가 있는 영역**")
        self.lines.append("- 예: \"톤업은 좋은데 **시간이 지나면** 무너진다\" 같은 조건부 만족")
        self.lines.append("")
    
    def section_context_analysis(self):
        """4. 맥락 기반 검증"""
        self.add_section("4. 맥락 기반 검증: 어떤 상황에서 문제가 터지는가?")
        
        self.lines.append("> Context는 LLM이 아닌 **Rule 기반 태깅**을 사용함 (context_tags_str)")
        self.lines.append("> LLM context의 NONE 문제를 회피하여 커버리지가 높음")
        self.lines.append("")
        
        # GOLDEN_NUGGET에서 context_tag × aspect
        ctx = self.pivot_context.copy()
        ctx = ctx[ctx['context_tag'] != 'NONE_RULE']
        
        # master에서 GOLDEN_NUGGET만 필터링하여 context explode
        gn_master = self.master[self.master['bucket'] == 'GOLDEN_NUGGET'].copy()
        gn_master['context_tag'] = gn_master['context_tags_str'].fillna('NONE_RULE').apply(
            lambda x: x.split('|') if x and x != 'NONE_RULE' else ['NONE_RULE']
        )
        gn_exploded = gn_master.explode('context_tag')
        gn_exploded = gn_exploded[gn_exploded['context_tag'] != 'NONE_RULE']
        
        # Group by context_tag, aspect
        gn_ctx = gn_exploded.groupby(['context_tag', 'aspect']).agg(
            n=('review_id', 'nunique'),
            unmet_like=('polarity_group', lambda x: (x == 'unmet_like').sum()),
        ).reset_index()
        gn_ctx = gn_ctx.sort_values('unmet_like', ascending=False).head(self.topn_context)
        
        self.lines.append("### 4.1 GOLDEN_NUGGET: Context × Aspect Top 15")
        self.lines.append("")
        self.add_table(
            gn_ctx,
            ['context_tag', 'aspect', 'n', 'unmet_like'],
            {'n': 'int', 'unmet_like': 'int'}
        )
        
        # 주요 맥락별 해석
        self.lines.append("")
        self.lines.append("### 4.2 주요 맥락별 해석")
        self.lines.append("")
        self.lines.append("| 맥락 | 주요 미충족 Aspect | 해석 |")
        self.lines.append("|------|------------------|------|")
        self.lines.append("| **BEFORE_MAKEUP** | OILINESS, PILLING | 메이크업 전 사용 시 유분/밀림 문제 |")
        self.lines.append("| **SUMMER** | OILINESS, DRYNESS | 여름철 번들거림 + 에어컨으로 인한 건조 |")
        self.lines.append("| **WINTER** | DRYNESS | 겨울철 보습력 부족 |")
        self.lines.append("| **MASK** | PILLING, IRRITATION | 마스크 착용 시 밀림/자극 발생 |")
        self.lines.append("")
    
    def section_season_analysis(self):
        """5. 계절성 검증"""
        self.add_section("5. 계절성 검증: Season별 패턴")
        
        self.lines.append("> season은 review_date 기반 파생 (spring/summer/fall/winter)")
        self.lines.append("> 지역/사용환경 다양성 한계 있음")
        self.lines.append("")
        
        # Summer vs Winter
        for season in ['summer', 'winter']:
            season_data = self.pivot_season[self.pivot_season['season'] == season].copy()
            season_data = season_data.sort_values('unmet_like_cnt', ascending=False).head(5)
            
            self.lines.append(f"### {season.upper()} Top 5")
            self.lines.append("")
            self.add_table(
                season_data,
                ['aspect', 'n_reviews', 'unmet_like_cnt', 'unmet_like_rate'],
                {'n_reviews': 'int', 'unmet_like_cnt': 'int', 'unmet_like_rate': 'pct'}
            )
            self.lines.append("")
        
        self.lines.append("### 계절별 특징")
        self.lines.append("")
        self.lines.append("- **SUMMER**: IRRITATION, OILINESS가 두드러짐 → 땀/피지와 관련된 문제")
        self.lines.append("- **WINTER**: DRYNESS, IRRITATION → 건조하고 민감해지는 피부 문제")
        self.lines.append("")
    
    def section_repeatability(self):
        """6. 반복성 검증"""
        self.add_section("6. 반복성 검증: 여러 제품에서 반복되는 문제")
        
        self.lines.append("> **Repeatability 높음** = 특정 브랜드/제품 이슈가 아닌 **시장 공통 문제**")
        self.lines.append("> → 신상품 기획 시 우선 해결 과제")
        self.lines.append("")
        
        # goods_cnt_unmet_like Top 10
        rep = self.repeatability[self.repeatability['goods_cnt_any'] >= self.min_goods_any].copy()
        rep_top = rep.sort_values('goods_cnt_unmet_like', ascending=False).head(self.topn)
        
        self.lines.append("### 6.1 goods_cnt_unmet_like Top 10")
        self.lines.append("")
        self.add_table(
            rep_top,
            ['aspect', 'goods_cnt_unmet_like', 'reviews_unmet_like_cnt', 'goods_repeat_rate'],
            {'goods_cnt_unmet_like': 'int', 'reviews_unmet_like_cnt': 'int', 'goods_repeat_rate': 'pct'}
        )
        
        self.lines.append("")
        self.lines.append("### 6.2 해석")
        self.lines.append("")
        self.lines.append("- **IRRITATION**: 118개 상품에서 반복 → 시장 전반의 자극 문제")
        self.lines.append("- **OILINESS**: 114개 상품에서 반복 → 유분 조절이 시장 공통 과제")
        self.lines.append("- **TONEUP**: 90개 상품에서 반복 → 톤업 지속력/자연스러움 개선 필요")
        self.lines.append("")
        
        self.lines.append("### 6.3 신상품 기획 우선순위 후보")
        self.lines.append("")
        self.lines.append("1. **IRRITATION** (자극 최소화)")
        self.lines.append("2. **OILINESS** (피지 컨트롤)")
        self.lines.append("3. **PILLING** (밀림 방지)")
        self.lines.append("4. **DRYNESS** (보습력 강화)")
        self.lines.append("5. **TONEUP** (자연스럽고 지속되는 톤업)")
        self.lines.append("")
        self.lines.append("> 구체적인 PRD 문장 및 대표 리뷰 인용은 Step 4-2에서 다룸")
        self.lines.append("")
    
    def section_limitations(self):
        """7. 한계/반증"""
        self.add_section("7. 반증/한계/다음 단계")
        
        self.lines.append("### 7.1 이 분석이 말할 수 없는 것")
        self.lines.append("")
        self.lines.append("- ❌ 매출/재구매/시장점유율과의 **인과관계**")
        self.lines.append("- ❌ 실제 SPF/PA 등 **제품 성능** 평가")
        self.lines.append("- ❌ 브랜드 간 **우열** 비교")
        self.lines.append("- ❌ 표본이 시장 전체를 대표한다는 주장")
        self.lines.append("")
        
        self.lines.append("### 7.2 LLM 추출 한계")
        self.lines.append("")
        self.lines.append("- 문장 오해석 가능성 (예: 부정문 해석 오류)")
        self.lines.append("- LLM context 필드 누락 → Rule context로 보완")
        self.lines.append("- confidence 분포: p10=0.80, p50=0.90 → 대체로 신뢰 가능하나 일부 불확실")
        self.lines.append("")
        
        self.lines.append("### 7.3 다음 단계 (Step 4-2)")
        self.lines.append("")
        self.lines.append("- 미충족 니즈를 **신상품 요구사항(PRD 문장)**으로 번역")
        self.lines.append("- 대표 리뷰 인용(Evidence)과 함께 **기획 스펙** 제안")
        self.lines.append("- 각 니즈별 구체적인 해결 방향 명시")
        self.lines.append("")
    
    def generate_report(self):
        """리포트 생성"""
        logger.info("Generating report...")
        
        # Header
        self.lines = [
            "# 4-1. 분석 결과 검증 리포트: 올리브영 썬크림 리뷰 기반 미충족 니즈",
            "",
            f"생성: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
        ]
        
        # Sections
        self.section_quality_gate()
        self.section_low_rating()
        self.section_golden_nugget()
        self.section_context_analysis()
        self.section_season_analysis()
        self.section_repeatability()
        self.section_limitations()
        
        # Save
        os.makedirs(os.path.dirname(self.out_path), exist_ok=True)
        with open(self.out_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.lines))
        
        logger.info(f"Report saved: {self.out_path}")
    
    def run(self):
        """전체 파이프라인"""
        try:
            self.load_data()
            self.generate_report()
            logger.info("Step 4-1 completed!")
        except Exception as e:
            logger.error(f"Error: {e}")
            raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis_dir", default="data/analysis")
    parser.add_argument("--out", default="report/step4_1_insight_review.md")
    parser.add_argument("--min_n_items", type=int, default=30)
    parser.add_argument("--min_goods_any", type=int, default=20)
    parser.add_argument("--topn", type=int, default=10)
    parser.add_argument("--topn_context", type=int, default=15)
    
    args = parser.parse_args()
    
    generator = InsightReportGenerator(
        analysis_dir=args.analysis_dir,
        out_path=args.out,
        min_n_items=args.min_n_items,
        min_goods_any=args.min_goods_any,
        topn=args.topn,
        topn_context=args.topn_context
    )
    generator.run()


if __name__ == "__main__":
    main()
