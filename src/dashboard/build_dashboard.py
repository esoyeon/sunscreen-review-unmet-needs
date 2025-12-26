"""
Step 5 v2: Build Dashboard Data
- Parquet → Standardized JSON/JS
- Text Content Generation
- Action Plan Integration
"""
import os
import json
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ANALYSIS_DIR = "data/analysis"
SITE_DATA_DIR = "report/site/data"
STEP4_2_PATH = "report/step4_2_product_actions.md"

ASPECT_KR_MAP = {
    "IRRITATION": "자극/따가움",
    "OILINESS": "유분/피지",
    "DRYNESS": "건조/속당김",
    "PILLING": "밀림/때처럼 밀림",
    "TONEUP": "톤업(자연스러움)",
    "WHITECAST": "백탁/회끼/동동 뜸",
    "EYE_STING": "눈시림",
    "FLAKING": "각질 부각/들뜸",
    "LONGEVITY": "지속력(시간 지나면 무너짐)",
    "TEXTURE_HEAVY": "무거운 사용감/답답함",
    "ABSORPTION": "흡수/겉돎",
    "TROUBLE": "트러블/뒤집어짐",
    "SCENT": "향",
    "MOISTURE": "보습",
    "STICKINESS": "끈적임",
    "SPREADABILITY": "발림성",
    "STAINING": "묻어남",
    "ALL": "전체",
    "OTHER": "기타",
    "TEXTURE": "제형",
    "COOLING": "쿨링감",
    "WATERPROOF": "워터프루프",
    "CLEANSING": "세정력"
}

def get_kr(aspect):
    return ASPECT_KR_MAP.get(aspect, aspect)

def build_data():
    data = {}

    # 0. Meta & Quality Gate
    data['meta'] = {
        "title": "Suncream Unmet Needs Analysis",
        "generated_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
        "caveat": "본 보고서는 LLM 기반으로 추출된 샘플링 데이터를 분석한 결과입니다."
    }
    data['quality_gate'] = {
        "metrics": [
            {"label": "Total Queue", "value": 4052, "desc": "수집 대상 리뷰"},
            {"label": "Parsed OK", "value": "94.2%", "desc": "파싱 성공률"},
            {"label": "Empty Items", "value": "9.0%", "desc": "추출 내용 없음"},
            {"label": "Valid Reviews", "value": 3474, "desc": "유효 리뷰 수"},
            {"label": "Valid Goods", "value": 81, "desc": "분석 대상 상품"}
        ]
    }

    # 1. Bucket Polarity (Trust Signal)
    df_bucket = pd.read_parquet(os.path.join(ANALYSIS_DIR, "pivot_aspect_polarity_by_bucket.parquet"))
    grp = df_bucket.groupby("bucket")[["met_cnt", "unmet_cnt", "mixed_cnt", "unknown_cnt", "n_items"]].sum().reset_index()
    
    # Calculate rates
    grp['met_rate'] = grp['met_cnt'] / grp['n_items']
    grp['unmet_rate'] = grp['unmet_cnt'] / grp['n_items']
    grp['mixed_rate'] = grp['mixed_cnt'] / grp['n_items']
    grp['unknown_rate'] = grp['unknown_cnt'] / grp['n_items']
    
    data['polarity_overview'] = {
        "chart_data": grp.to_dict(orient="records"),
        "text": {
            "observation": "LOW_RATING(1~3점) 그룹의 Unmet(미충족) 비율은 90% 이상이며, GOLDEN_NUGGET(4점)에서도 Unmet+Mixed 비율이 40% 이상 관찰됩니다.",
            "interpretation": "리뷰 평점과 AI 추출 감정(Sentiments) 간의 정합성이 높습니다. 특히 4점 리뷰 내의 '아쉬운 점'은 제품 업그레이드의 핵심 단서입니다.",
            "caveat": "Mixed(복합 감정) 및 Unknown 비율이 일부 존재하여, 뉘앙스 차이가 있을 수 있습니다."
        }
    }

    # 2. Opportunity Map (Repeatability)
    df_rep = pd.read_parquet(os.path.join(ANALYSIS_DIR, "repeatability_aspect_goods_count.parquet"))
    df_rep['aspect_kr'] = df_rep['aspect'].apply(get_kr)
    
    data['opportunity_map'] = {
        "chart_data": df_rep.to_dict(orient="records"),
        "text": {
            "observation": "🔴 빨간색 점(Top 5)은 자극, 유분, 밀림, 속건조, 톤업 등 핵심 미충족 니즈를 나타내며, 🔵 파란색 점은 그 외 속성입니다.",
            "interpretation": "<b>X축(반복성)</b>이 높을수록 특정 제품만의 문제가 아닌 '카테고리 공통의 난제'임을 의미합니다. <b>Y축(불만 규모)</b>이 높을수록 고객 이탈에 미치는 영향이 큽니다. 즉, 우측 상단(빨간색 영역)은 반드시 해결해야 할 시장의 기회입니다.",
            "caveat": "원의 크기는 해당 속성이 언급된 제품의 수를 나타냅니다. 크기가 작고 좌측에 있는 속성은 틈새 시장(Niche) 니즈일 수 있습니다."
        }
    }

    # 3. Market Pain (Low Rating)
    low_df = df_bucket[df_bucket['bucket'] == 'LOW_RATING'].copy()
    low_df['aspect_kr'] = low_df['aspect'].apply(get_kr)
    low_df['unmet_like_rate_pct'] = (low_df['unmet_like_rate'] * 100).round(1).astype(str) + "%"
    low_df_top = low_df[low_df['n_items'] >= 20].sort_values("unmet_like_rate", ascending=False).head(10)
    
    data['market_pain'] = {
        "chart_data": low_df_top.to_dict(orient="records"),
        "text": {
            "observation": "PILLING(밀림)은 99%의 압도적인 불만율을 보이며, IRRITATION(자극) 역시 95% 이상이 부정적 경험입니다.",
            "interpretation": "이 두 가지 요인은 발생 즉시 제품 사용 중단 및 최하점 평가로 직결되는 'Showstopper'입니다.",
            "caveat": "LOW_RATING 그룹(표본 n=560) 내에서의 비율이므로, 전체 사용자 대비 발생 빈도는 다를 수 있습니다."
        }
    }

    # 4. Golden Nugget
    gold_df = df_bucket[df_bucket['bucket'] == 'GOLDEN_NUGGET'].copy()
    gold_df['aspect_kr'] = gold_df['aspect'].apply(get_kr)
    gold_df['unmet_acc'] = gold_df['unmet_cnt'] + gold_df['mixed_cnt']
    gold_df['unmet_like_rate_pct'] = (gold_df['unmet_like_rate'] * 100).round(1).astype(str) + "%"
    gold_df_top = gold_df.sort_values("unmet_acc", ascending=False).head(10)
    
    data['golden_nugget'] = {
        "chart_data": gold_df_top.to_dict(orient="records"),
        "text": {
            "observation": "TONEUP(톤업)과 DRYNESS(건조)는 4점대 리뷰에서도 30% 이상의 미충족(또는 복합) 반응이 나타납니다.",
            "interpretation": "전반적으로 만족하지만 '오후의 건조함'이나 '약간의 백탁'이 아쉬움을 남기고 있습니다. 개선 시 충성도(Lock-in)를 높일 수 있습니다.",
            "caveat": "Met(만족) 비율이 더 높은 영역이므로, 개선 시 기존 만족 요소를 해치지 않는 균형이 중요합니다."
        }
    }

    # 5. Context
    df_ctx = pd.read_parquet(os.path.join(ANALYSIS_DIR, "pivot_context_aspect_unmet.parquet"))
    df_ctx['aspect_kr'] = df_ctx['aspect'].apply(get_kr)
    ctx_top = df_ctx[df_ctx['n_reviews'] >= 20].copy()
    
    data['context_analysis'] = {
        "chart_data": ctx_top.to_dict(orient="records"),
        "text": {
            "observation": "BEFORE_MAKEUP(화장 전) 상황에서 PILLING(밀림) 발생 빈도가 가장 높으며, SUMMER(여름)에는 OILINESS(유분) 불만이 급증합니다.",
            "interpretation": "사용 상황(Context)에 따라 '나쁜 경험'의 정의가 달라집니다. 메이크업 병행 사용자에게는 밀림 방지가 최우선(P0)입니다.",
            "caveat": "문맥 태그(Context Tag)는 키워드 매칭 룰 기반이므로 실제 의도와 일부 차이가 있을 수 있습니다."
        }
    }

    # 6. Seasonality
    df_season = pd.read_parquet(os.path.join(ANALYSIS_DIR, "pivot_season_aspect_unmet.parquet"))
    df_season['aspect_kr'] = df_season['aspect'].apply(get_kr)
    
    data['seasonality'] = {
        "chart_data": df_season.to_dict(orient="records"),
        "text": {
            "observation": "SUMMER 시즌에는 피지/자극 관련 미충족이 70% 이상을 차지하나, WINTER 시즌에는 건조함 불만 비중이 2배 이상 증가합니다.",
            "interpretation": "계절적 환경 요인이 니즈의 우선순위를 바꿉니다. 시즌별 주력 제품(라인업)이나 마케팅 메시지 차별화가 유효합니다.",
            "caveat": "작성월 기준 계절 분류이므로, 실제 구매/사용 시점과는 약 1개월의 시차(Lag)가 있을 수 있습니다."
        }
    }

    # 7. Action Plan
    ice_table = [
        {"needs": "IRRITATION", "name": "자극 최소화", "impact": 9, "confidence": 8, "ease": 6, "score": 72, "note": "최우선 해결 과제"},
        {"needs": "OILINESS", "name": "피지 컨트롤", "impact": 8, "confidence": 8, "ease": 7, "score": 56, "note": "지성 타겟 핵심"},
        {"needs": "DRYNESS", "name": "보습력 강화", "impact": 7, "confidence": 7, "ease": 8, "score": 49, "note": "겨울철/건성 소구"},
        {"needs": "PILLING", "name": "밀림 방지", "impact": 8, "confidence": 9, "ease": 5, "score": 45, "note": "메이크업 병행 중요"},
        {"needs": "TONEUP", "name": "톤업 개선", "impact": 7, "confidence": 8, "ease": 6, "score": 42, "note": "자연스러움/지속력"}
    ]
    
    spec_matrix = [
        {"req": "논코메도제닉 수준 자극", "aspect": "IRRITATION", "context": "ALL", "kpi": "따가움 언급 0건", "test": "민감성 패널 48시간"},
        {"req": "메이크업 밀착력", "aspect": "PILLING", "context": "BEFORE_MAKEUP", "kpi": "파데 밀림 없음", "test": "쿠션/파데 병용 테스트"},
        {"req": "6시간 피지 컨트롤", "aspect": "OILINESS", "context": "SUMMER", "kpi": "유분기 변화 < 20%", "test": "피지 측정기 지속 관찰"},
        {"req": "속당김 없는 보습", "aspect": "DRYNESS", "context": "WINTER", "kpi": "수분도 유지 > 80%", "test": "건조 환경 챔버 테스트"},
        {"req": "다크닝 없는 톤업", "aspect": "TONEUP", "context": "ALL", "kpi": "색차값(Delta E) < 2", "test": "4시간 후 톤 유지력"}
    ]
    
    top5_cards = [
        {
            "id": "IRRITATION", "name": "자극 최소화", "desc": "따가움/눈시림 없는 편안함",
            "stats": {"repeat": "84%", "unmet": "95%"},
            "reqs": ["무기자차 수준의 순함", "눈시림 성분 배제"],
            "tests": ["안자극 테스트", "민감성 패널"]
        },
        {
            "id": "OILINESS", "name": "피지 컨트롤", "desc": "번들거림 없는 산뜻함",
            "stats": {"repeat": "84%", "unmet": "High"},
            "reqs": ["다공성 파우더 적용", "속건조 없는 매트함"],
            "tests": ["유분 흡유량", "메이크업 지속력"]
        },
        {
            "id": "PILLING", "name": "밀림 방지", "desc": "화장이 잘 먹는 베이스",
            "stats": {"repeat": "74%", "unmet": "99%"},
            "reqs": ["실리콘/필름막 밸런싱", "흡수 속도 조절"],
            "tests": ["레이어링 테스트", "때밀림 관능"]
        },
        {
            "id": "DRYNESS", "name": "보습력 강화", "desc": "속당김/각질 없는 촉촉함",
            "stats": {"repeat": "71%", "unmet": "Mix"},
            "reqs": ["수분 에센스 함량 증대", "유수분 밸런스"],
            "tests": ["경피 수분 손실량", "각질 들뜸"]
        },
        {
            "id": "TONEUP", "name": "자연스러운 톤업", "desc": "백탁/회끼 없는 맑은 톤",
            "stats": {"repeat": "76%", "unmet": "Mix"},
            "reqs": ["균일한 입자 분산", "핑크 베이스 적용"],
            "tests": ["피부톤별 발색", "다크닝 측정"]
        }
    ]

    data['action_plan'] = {
        "ice": ice_table,
        "spec": spec_matrix,
        "cards": top5_cards,
        "text": {
            "observation": "Top 5 과제는 상호 연관되어 있습니다(예: 유분 제어 vs 속건조 방지).",
            "interpretation": "단일 속성 개선보다는 Trade-off 관계를 고려한 균형 잡힌 처방 설계가 핵심 경쟁력입니다.",
            "caveat": "제품 컨셉(유기/무기/혼합)에 따라 우선순위 가중치는 조정될 수 있습니다."
        }
    }

    # 8. Evidence (Same as before but keep structure)
    evidence_samples = [
        {"id": "IRRITATION", "quotes": ["바르자마자 따가워요", "눈이 너무 시려워서 눈물을 흘림", "피부가 뒤집어졌어요"]},
        {"id": "OILINESS", "quotes": ["개기름이 좔좔 흘러요", "시간 지나면 번들거림 심함", "지성 피부엔 비추"]},
        {"id": "PILLING", "quotes": ["때처럼 밀려나와요", "화장이 다 뜹니다", "기초 밀리고 난리남"]},
        {"id": "DRYNESS", "quotes": ["속당김이 느껴져요", "시간 지나면 바싹 마르는 느낌", "각질이 부각됨"]},
        {"id": "TONEUP", "quotes": ["너무 하얗게 동동 떠요", "회색빛이 돌아요", "자연스럽지 않고 두꺼움"]}
    ]
    data['evidence'] = {
        "samples": evidence_samples,
        "text": {
            "observation": "정량 데이터 뒤에는 구체적이고 생생한 고객의 고통(Voice)이 존재합니다.",
            "interpretation": "고객이 사용하는 단어(따가움, 개기름, 때처럼 등)는 마케팅 소구점 및 상세페이지 카피의 원천입니다.",
            "caveat": "고객 리뷰 원문을 발췌하였으며, 개인정보는 제외되었습니다."
        }
    }

    # 9. Glossary
    data['glossary'] = [
        {"term": "FLAKING", "kr": "각질 부각/들뜸", "desc": "\"각질이 부각돼요\", \"하얗게 일어나요\" (건조함 관련)"},
        {"term": "LONGEVITY", "kr": "지속력", "desc": "\"시간 지나면 무너짐\", \"다크닝\", \"무너짐\""},
        {"term": "TEXTURE_HEAVY", "kr": "무거운 사용감", "desc": "\"답답해요\", \"두꺼워요\", \"피부가 숨을 못 쉬는 듯\""},
        {"term": "ABSORPTION", "kr": "흡수/겉돎", "desc": "\"겉돌아요\", \"흡수 안 돼요\", \"하얗게 뜸\""},
        {"term": "WHITECAST", "kr": "백탁/회끼", "desc": "\"동동 떠요\", \"가부키 화장\", \"토시오\""},
        {"term": "PILLING", "kr": "밀림", "desc": "\"때처럼 밀려요\", \"지우개 가루\", \"화장 뜸\""}
    ]

    # Save to JS file
    os.makedirs(SITE_DATA_DIR, exist_ok=True)
    js_path = os.path.join(SITE_DATA_DIR, "dashboard_data.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(f"window.DASHBOARD_DATA = {json.dumps(data, ensure_ascii=False, indent=2)};")
    logger.info(f"Saved {js_path}")

if __name__ == "__main__":
    build_data()
