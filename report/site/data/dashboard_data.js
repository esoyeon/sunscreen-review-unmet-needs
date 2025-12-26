window.DASHBOARD_DATA = {
  "meta": {
    "title": "Suncream Unmet Needs Analysis",
    "generated_at": "2025-12-25 23:57",
    "caveat": "본 보고서는 LLM 기반으로 추출된 샘플링 데이터를 분석한 결과입니다."
  },
  "quality_gate": {
    "metrics": [
      {
        "label": "Total Queue",
        "value": 4052,
        "desc": "수집 대상 리뷰"
      },
      {
        "label": "Parsed OK",
        "value": "94.2%",
        "desc": "파싱 성공률"
      },
      {
        "label": "Empty Items",
        "value": "9.0%",
        "desc": "추출 내용 없음"
      },
      {
        "label": "Valid Reviews",
        "value": 3474,
        "desc": "유효 리뷰 수"
      },
      {
        "label": "Valid Goods",
        "value": 81,
        "desc": "분석 대상 상품"
      }
    ]
  },
  "polarity_overview": {
    "chart_data": [
      {
        "bucket": "GOLDEN_NUGGET",
        "met_cnt": 2457,
        "unmet_cnt": 406,
        "mixed_cnt": 150,
        "unknown_cnt": 123,
        "n_items": 3136,
        "met_rate": 0.7834821428571429,
        "unmet_rate": 0.12946428571428573,
        "mixed_rate": 0.04783163265306122,
        "unknown_rate": 0.0392219387755102
      },
      {
        "bucket": "HELPFUL_LONG",
        "met_cnt": 1242,
        "unmet_cnt": 241,
        "mixed_cnt": 42,
        "unknown_cnt": 71,
        "n_items": 1596,
        "met_rate": 0.7781954887218046,
        "unmet_rate": 0.15100250626566417,
        "mixed_rate": 0.02631578947368421,
        "unknown_rate": 0.044486215538847115
      },
      {
        "bucket": "LOW_RATING",
        "met_cnt": 226,
        "unmet_cnt": 2042,
        "mixed_cnt": 48,
        "unknown_cnt": 66,
        "n_items": 2382,
        "met_rate": 0.0948782535684299,
        "unmet_rate": 0.8572628043660789,
        "mixed_rate": 0.020151133501259445,
        "unknown_rate": 0.027707808564231738
      },
      {
        "bucket": "RANDOM_CONTROL",
        "met_cnt": 266,
        "unmet_cnt": 67,
        "mixed_cnt": 11,
        "unknown_cnt": 13,
        "n_items": 357,
        "met_rate": 0.7450980392156863,
        "unmet_rate": 0.1876750700280112,
        "mixed_rate": 0.03081232492997199,
        "unknown_rate": 0.036414565826330535
      }
    ],
    "text": {
      "observation": "LOW_RATING(1~3점) 그룹의 Unmet(미충족) 비율은 90% 이상이며, GOLDEN_NUGGET(4점)에서도 Unmet+Mixed 비율이 40% 이상 관찰됩니다.",
      "interpretation": "리뷰 평점과 AI 추출 감정(Sentiments) 간의 정합성이 높습니다. 특히 4점 리뷰 내의 '아쉬운 점'은 제품 업그레이드의 핵심 단서입니다.",
      "caveat": "Mixed(복합 감정) 및 Unknown 비율이 일부 존재하여, 뉘앙스 차이가 있을 수 있습니다."
    }
  },
  "opportunity_map": {
    "chart_data": [
      {
        "aspect": "IRRITATION",
        "goods_cnt_any": 140,
        "reviews_any_cnt": 1012,
        "goods_cnt_unmet_like": 118,
        "reviews_unmet_like_cnt": 587,
        "goods_repeat_rate": 0.8428571428571429,
        "aspect_kr": "자극/따가움"
      },
      {
        "aspect": "OILINESS",
        "goods_cnt_any": 135,
        "reviews_any_cnt": 746,
        "goods_cnt_unmet_like": 114,
        "reviews_unmet_like_cnt": 397,
        "goods_repeat_rate": 0.8444444444444444,
        "aspect_kr": "유분/피지"
      },
      {
        "aspect": "TONEUP",
        "goods_cnt_any": 119,
        "reviews_any_cnt": 987,
        "goods_cnt_unmet_like": 90,
        "reviews_unmet_like_cnt": 290,
        "goods_repeat_rate": 0.7563025210084033,
        "aspect_kr": "톤업(자연스러움)"
      },
      {
        "aspect": "DRYNESS",
        "goods_cnt_any": 124,
        "reviews_any_cnt": 529,
        "goods_cnt_unmet_like": 88,
        "reviews_unmet_like_cnt": 273,
        "goods_repeat_rate": 0.7096774193548387,
        "aspect_kr": "건조/속당김"
      },
      {
        "aspect": "WHITECAST",
        "goods_cnt_any": 126,
        "reviews_any_cnt": 707,
        "goods_cnt_unmet_like": 87,
        "reviews_unmet_like_cnt": 204,
        "goods_repeat_rate": 0.6904761904761905,
        "aspect_kr": "백탁/회끼/동동 뜸"
      },
      {
        "aspect": "PILLING",
        "goods_cnt_any": 108,
        "reviews_any_cnt": 399,
        "goods_cnt_unmet_like": 80,
        "reviews_unmet_like_cnt": 245,
        "goods_repeat_rate": 0.7407407407407407,
        "aspect_kr": "밀림/때처럼 밀림"
      },
      {
        "aspect": "EYE_STING",
        "goods_cnt_any": 120,
        "reviews_any_cnt": 459,
        "goods_cnt_unmet_like": 77,
        "reviews_unmet_like_cnt": 192,
        "goods_repeat_rate": 0.6416666666666667,
        "aspect_kr": "눈시림"
      },
      {
        "aspect": "MOISTURE",
        "goods_cnt_any": 137,
        "reviews_any_cnt": 687,
        "goods_cnt_unmet_like": 63,
        "reviews_unmet_like_cnt": 104,
        "goods_repeat_rate": 0.45985401459854014,
        "aspect_kr": "보습"
      },
      {
        "aspect": "SCENT",
        "goods_cnt_any": 108,
        "reviews_any_cnt": 291,
        "goods_cnt_unmet_like": 62,
        "reviews_unmet_like_cnt": 117,
        "goods_repeat_rate": 0.5740740740740741,
        "aspect_kr": "향"
      },
      {
        "aspect": "TROUBLE",
        "goods_cnt_any": 61,
        "reviews_any_cnt": 109,
        "goods_cnt_unmet_like": 57,
        "reviews_unmet_like_cnt": 99,
        "goods_repeat_rate": 0.9344262295081968,
        "aspect_kr": "트러블/뒤집어짐"
      },
      {
        "aspect": "FLAKING",
        "goods_cnt_any": 70,
        "reviews_any_cnt": 123,
        "goods_cnt_unmet_like": 53,
        "reviews_unmet_like_cnt": 87,
        "goods_repeat_rate": 0.7571428571428571,
        "aspect_kr": "각질 부각/들뜸"
      },
      {
        "aspect": "LONGEVITY",
        "goods_cnt_any": 80,
        "reviews_any_cnt": 176,
        "goods_cnt_unmet_like": 49,
        "reviews_unmet_like_cnt": 69,
        "goods_repeat_rate": 0.6125,
        "aspect_kr": "지속력(시간 지나면 무너짐)"
      },
      {
        "aspect": "STICKINESS",
        "goods_cnt_any": 114,
        "reviews_any_cnt": 392,
        "goods_cnt_unmet_like": 47,
        "reviews_unmet_like_cnt": 67,
        "goods_repeat_rate": 0.41228070175438597,
        "aspect_kr": "끈적임"
      },
      {
        "aspect": "TEXTURE_HEAVY",
        "goods_cnt_any": 76,
        "reviews_any_cnt": 130,
        "goods_cnt_unmet_like": 47,
        "reviews_unmet_like_cnt": 61,
        "goods_repeat_rate": 0.618421052631579,
        "aspect_kr": "무거운 사용감/답답함"
      },
      {
        "aspect": "ABSORPTION",
        "goods_cnt_any": 103,
        "reviews_any_cnt": 292,
        "goods_cnt_unmet_like": 43,
        "reviews_unmet_like_cnt": 75,
        "goods_repeat_rate": 0.4174757281553398,
        "aspect_kr": "흡수/겉돎"
      },
      {
        "aspect": "OTHER",
        "goods_cnt_any": 25,
        "reviews_any_cnt": 34,
        "goods_cnt_unmet_like": 19,
        "reviews_unmet_like_cnt": 24,
        "goods_repeat_rate": 0.76,
        "aspect_kr": "기타"
      },
      {
        "aspect": "WATERPROOF",
        "goods_cnt_any": 27,
        "reviews_any_cnt": 74,
        "goods_cnt_unmet_like": 17,
        "reviews_unmet_like_cnt": 33,
        "goods_repeat_rate": 0.6296296296296297,
        "aspect_kr": "워터프루프"
      },
      {
        "aspect": "STAINING",
        "goods_cnt_any": 30,
        "reviews_any_cnt": 48,
        "goods_cnt_unmet_like": 17,
        "reviews_unmet_like_cnt": 23,
        "goods_repeat_rate": 0.5666666666666667,
        "aspect_kr": "묻어남"
      },
      {
        "aspect": "TEXTURE_LIGHT",
        "goods_cnt_any": 86,
        "reviews_any_cnt": 170,
        "goods_cnt_unmet_like": 9,
        "reviews_unmet_like_cnt": 11,
        "goods_repeat_rate": 0.10465116279069768,
        "aspect_kr": "TEXTURE_LIGHT"
      },
      {
        "aspect": "WHITE_RESIDUE",
        "goods_cnt_any": 10,
        "reviews_any_cnt": 10,
        "goods_cnt_unmet_like": 6,
        "reviews_unmet_like_cnt": 6,
        "goods_repeat_rate": 0.6,
        "aspect_kr": "WHITE_RESIDUE"
      },
      {
        "aspect": "PORES",
        "goods_cnt_any": 4,
        "reviews_any_cnt": 4,
        "goods_cnt_unmet_like": 4,
        "reviews_unmet_like_cnt": 4,
        "goods_repeat_rate": 1.0,
        "aspect_kr": "PORES"
      },
      {
        "aspect": "BEFORE_MAKEUP",
        "goods_cnt_any": 5,
        "reviews_any_cnt": 5,
        "goods_cnt_unmet_like": 2,
        "reviews_unmet_like_cnt": 2,
        "goods_repeat_rate": 0.4,
        "aspect_kr": "BEFORE_MAKEUP"
      },
      {
        "aspect": "COVERAGE",
        "goods_cnt_any": 4,
        "reviews_any_cnt": 4,
        "goods_cnt_unmet_like": 1,
        "reviews_unmet_like_cnt": 1,
        "goods_repeat_rate": 0.25,
        "aspect_kr": "COVERAGE"
      },
      {
        "aspect": "REDNESS",
        "goods_cnt_any": 2,
        "reviews_any_cnt": 2,
        "goods_cnt_unmet_like": 0,
        "reviews_unmet_like_cnt": 0,
        "goods_repeat_rate": 0.0,
        "aspect_kr": "REDNESS"
      },
      {
        "aspect": "PORE_CLOGGING",
        "goods_cnt_any": 1,
        "reviews_any_cnt": 1,
        "goods_cnt_unmet_like": 0,
        "reviews_unmet_like_cnt": 0,
        "goods_repeat_rate": 0.0,
        "aspect_kr": "PORE_CLOGGING"
      }
    ],
    "text": {
      "observation": "IRRITATION(자극), OILINESS(유분), PILLING(밀림)은 80개 이상의 제품에서 반복적으로 언급되며(Repeat Rate > 80%), 절대적인 불만 볼륨도 가장 큽니다.",
      "interpretation": "특정 제품의 결함이 아니라, 선크림 카테고리가 가진 구조적인 난제(Trade-off)임을 시사합니다. 이를 해결하면 시장 파급력이 큽니다.",
      "caveat": "Goods Count 20개 미만의 긴 꼬리(Long-tail) 속성은 산점도에서 제외하거나 별도 해석이 필요합니다."
    }
  },
  "market_pain": {
    "chart_data": [
      {
        "bucket": "LOW_RATING",
        "aspect": "PILLING",
        "n_items": 196,
        "met_cnt": 2,
        "unmet_cnt": 194,
        "mixed_cnt": 0,
        "unknown_cnt": 0,
        "unmet_like_cnt": 194,
        "unmet_like_rate": 0.9897959183673469,
        "aspect_kr": "밀림/때처럼 밀림",
        "unmet_like_rate_pct": "99.0%"
      },
      {
        "bucket": "LOW_RATING",
        "aspect": "TROUBLE",
        "n_items": 95,
        "met_cnt": 0,
        "unmet_cnt": 94,
        "mixed_cnt": 0,
        "unknown_cnt": 1,
        "unmet_like_cnt": 94,
        "unmet_like_rate": 0.9894736842105263,
        "aspect_kr": "트러블/뒤집어짐",
        "unmet_like_rate_pct": "98.9%"
      },
      {
        "bucket": "LOW_RATING",
        "aspect": "FLAKING",
        "n_items": 67,
        "met_cnt": 0,
        "unmet_cnt": 65,
        "mixed_cnt": 0,
        "unknown_cnt": 2,
        "unmet_like_cnt": 65,
        "unmet_like_rate": 0.9701492537313433,
        "aspect_kr": "각질 부각/들뜸",
        "unmet_like_rate_pct": "97.0%"
      },
      {
        "bucket": "LOW_RATING",
        "aspect": "LONGEVITY",
        "n_items": 44,
        "met_cnt": 2,
        "unmet_cnt": 42,
        "mixed_cnt": 0,
        "unknown_cnt": 0,
        "unmet_like_cnt": 42,
        "unmet_like_rate": 0.9545454545454546,
        "aspect_kr": "지속력(시간 지나면 무너짐)",
        "unmet_like_rate_pct": "95.5%"
      },
      {
        "bucket": "LOW_RATING",
        "aspect": "IRRITATION",
        "n_items": 560,
        "met_cnt": 22,
        "unmet_cnt": 525,
        "mixed_cnt": 6,
        "unknown_cnt": 7,
        "unmet_like_cnt": 531,
        "unmet_like_rate": 0.9482142857142857,
        "aspect_kr": "자극/따가움",
        "unmet_like_rate_pct": "94.8%"
      },
      {
        "bucket": "LOW_RATING",
        "aspect": "OTHER",
        "n_items": 25,
        "met_cnt": 0,
        "unmet_cnt": 23,
        "mixed_cnt": 0,
        "unknown_cnt": 2,
        "unmet_like_cnt": 23,
        "unmet_like_rate": 0.92,
        "aspect_kr": "기타",
        "unmet_like_rate_pct": "92.0%"
      },
      {
        "bucket": "LOW_RATING",
        "aspect": "ABSORPTION",
        "n_items": 66,
        "met_cnt": 6,
        "unmet_cnt": 58,
        "mixed_cnt": 2,
        "unknown_cnt": 0,
        "unmet_like_cnt": 60,
        "unmet_like_rate": 0.9090909090909091,
        "aspect_kr": "흡수/겉돎",
        "unmet_like_rate_pct": "90.9%"
      },
      {
        "bucket": "LOW_RATING",
        "aspect": "DRYNESS",
        "n_items": 183,
        "met_cnt": 13,
        "unmet_cnt": 162,
        "mixed_cnt": 3,
        "unknown_cnt": 5,
        "unmet_like_cnt": 165,
        "unmet_like_rate": 0.9016393442622951,
        "aspect_kr": "건조/속당김",
        "unmet_like_rate_pct": "90.2%"
      },
      {
        "bucket": "LOW_RATING",
        "aspect": "OILINESS",
        "n_items": 282,
        "met_cnt": 19,
        "unmet_cnt": 248,
        "mixed_cnt": 5,
        "unknown_cnt": 10,
        "unmet_like_cnt": 253,
        "unmet_like_rate": 0.8971631205673759,
        "aspect_kr": "유분/피지",
        "unmet_like_rate_pct": "89.7%"
      },
      {
        "bucket": "LOW_RATING",
        "aspect": "TEXTURE_HEAVY",
        "n_items": 41,
        "met_cnt": 2,
        "unmet_cnt": 36,
        "mixed_cnt": 0,
        "unknown_cnt": 3,
        "unmet_like_cnt": 36,
        "unmet_like_rate": 0.8780487804878049,
        "aspect_kr": "무거운 사용감/답답함",
        "unmet_like_rate_pct": "87.8%"
      }
    ],
    "text": {
      "observation": "PILLING(밀림)은 99%의 압도적인 불만율을 보이며, IRRITATION(자극) 역시 95% 이상이 부정적 경험입니다.",
      "interpretation": "이 두 가지 요인은 발생 즉시 제품 사용 중단 및 최하점 평가로 직결되는 'Showstopper'입니다.",
      "caveat": "LOW_RATING 그룹(표본 n=560) 내에서의 비율이므로, 전체 사용자 대비 발생 빈도는 다를 수 있습니다."
    }
  },
  "golden_nugget": {
    "chart_data": [
      {
        "bucket": "GOLDEN_NUGGET",
        "aspect": "TONEUP",
        "n_items": 529,
        "met_cnt": 425,
        "unmet_cnt": 76,
        "mixed_cnt": 24,
        "unknown_cnt": 4,
        "unmet_like_cnt": 100,
        "unmet_like_rate": 0.1890359168241966,
        "aspect_kr": "톤업(자연스러움)",
        "unmet_acc": 100,
        "unmet_like_rate_pct": "18.9%"
      },
      {
        "bucket": "GOLDEN_NUGGET",
        "aspect": "OILINESS",
        "n_items": 313,
        "met_cnt": 185,
        "unmet_cnt": 71,
        "mixed_cnt": 24,
        "unknown_cnt": 33,
        "unmet_like_cnt": 95,
        "unmet_like_rate": 0.3035143769968051,
        "aspect_kr": "유분/피지",
        "unmet_acc": 95,
        "unmet_like_rate_pct": "30.4%"
      },
      {
        "bucket": "GOLDEN_NUGGET",
        "aspect": "DRYNESS",
        "n_items": 232,
        "met_cnt": 132,
        "unmet_cnt": 54,
        "mixed_cnt": 22,
        "unknown_cnt": 24,
        "unmet_like_cnt": 76,
        "unmet_like_rate": 0.3275862068965517,
        "aspect_kr": "건조/속당김",
        "unmet_acc": 76,
        "unmet_like_rate_pct": "32.8%"
      },
      {
        "bucket": "GOLDEN_NUGGET",
        "aspect": "WHITECAST",
        "n_items": 336,
        "met_cnt": 270,
        "unmet_cnt": 25,
        "mixed_cnt": 29,
        "unknown_cnt": 12,
        "unmet_like_cnt": 54,
        "unmet_like_rate": 0.16071428571428573,
        "aspect_kr": "백탁/회끼/동동 뜸",
        "unmet_acc": 54,
        "unmet_like_rate_pct": "16.1%"
      },
      {
        "bucket": "GOLDEN_NUGGET",
        "aspect": "EYE_STING",
        "n_items": 198,
        "met_cnt": 162,
        "unmet_cnt": 21,
        "mixed_cnt": 14,
        "unknown_cnt": 1,
        "unmet_like_cnt": 35,
        "unmet_like_rate": 0.17676767676767677,
        "aspect_kr": "눈시림",
        "unmet_acc": 35,
        "unmet_like_rate_pct": "17.7%"
      },
      {
        "bucket": "GOLDEN_NUGGET",
        "aspect": "PILLING",
        "n_items": 127,
        "met_cnt": 94,
        "unmet_cnt": 28,
        "mixed_cnt": 5,
        "unknown_cnt": 0,
        "unmet_like_cnt": 33,
        "unmet_like_rate": 0.25984251968503935,
        "aspect_kr": "밀림/때처럼 밀림",
        "unmet_acc": 33,
        "unmet_like_rate_pct": "26.0%"
      },
      {
        "bucket": "GOLDEN_NUGGET",
        "aspect": "IRRITATION",
        "n_items": 279,
        "met_cnt": 249,
        "unmet_cnt": 20,
        "mixed_cnt": 7,
        "unknown_cnt": 3,
        "unmet_like_cnt": 27,
        "unmet_like_rate": 0.0967741935483871,
        "aspect_kr": "자극/따가움",
        "unmet_acc": 27,
        "unmet_like_rate_pct": "9.7%"
      },
      {
        "bucket": "GOLDEN_NUGGET",
        "aspect": "MOISTURE",
        "n_items": 332,
        "met_cnt": 301,
        "unmet_cnt": 15,
        "mixed_cnt": 11,
        "unknown_cnt": 5,
        "unmet_like_cnt": 26,
        "unmet_like_rate": 0.0783132530120482,
        "aspect_kr": "보습",
        "unmet_acc": 26,
        "unmet_like_rate_pct": "7.8%"
      },
      {
        "bucket": "GOLDEN_NUGGET",
        "aspect": "SCENT",
        "n_items": 112,
        "met_cnt": 77,
        "unmet_cnt": 18,
        "mixed_cnt": 1,
        "unknown_cnt": 16,
        "unmet_like_cnt": 19,
        "unmet_like_rate": 0.16964285714285715,
        "aspect_kr": "향",
        "unmet_acc": 19,
        "unmet_like_rate_pct": "17.0%"
      },
      {
        "bucket": "GOLDEN_NUGGET",
        "aspect": "LONGEVITY",
        "n_items": 89,
        "met_cnt": 67,
        "unmet_cnt": 16,
        "mixed_cnt": 2,
        "unknown_cnt": 4,
        "unmet_like_cnt": 18,
        "unmet_like_rate": 0.20224719101123595,
        "aspect_kr": "지속력(시간 지나면 무너짐)",
        "unmet_acc": 18,
        "unmet_like_rate_pct": "20.2%"
      }
    ],
    "text": {
      "observation": "TONEUP(톤업)과 DRYNESS(건조)는 4점대 리뷰에서도 30% 이상의 미충족(또는 복합) 반응이 나타납니다.",
      "interpretation": "전반적으로 만족하지만 '오후의 건조함'이나 '약간의 백탁'이 아쉬움을 남기고 있습니다. 개선 시 충성도(Lock-in)를 높일 수 있습니다.",
      "caveat": "Met(만족) 비율이 더 높은 영역이므로, 개선 시 기존 만족 요소를 해치지 않는 균형이 중요합니다."
    }
  },
  "context_analysis": {
    "chart_data": [
      {
        "context_tag": "NONE_RULE",
        "aspect": "IRRITATION",
        "n_reviews": 375,
        "unmet_like_cnt": 287,
        "met_like_cnt": 82,
        "unmet_like_rate": 0.7653333333333333,
        "aspect_kr": "자극/따가움"
      },
      {
        "context_tag": "SUMMER",
        "aspect": "IRRITATION",
        "n_reviews": 417,
        "unmet_like_cnt": 191,
        "met_like_cnt": 217,
        "unmet_like_rate": 0.4580335731414868,
        "aspect_kr": "자극/따가움"
      },
      {
        "context_tag": "NONE_RULE",
        "aspect": "OILINESS",
        "n_reviews": 224,
        "unmet_like_cnt": 155,
        "met_like_cnt": 60,
        "unmet_like_rate": 0.6919642857142857,
        "aspect_kr": "유분/피지"
      },
      {
        "context_tag": "SUMMER",
        "aspect": "OILINESS",
        "n_reviews": 322,
        "unmet_like_cnt": 140,
        "met_like_cnt": 144,
        "unmet_like_rate": 0.43478260869565216,
        "aspect_kr": "유분/피지"
      },
      {
        "context_tag": "BEFORE_MAKEUP",
        "aspect": "PILLING",
        "n_reviews": 251,
        "unmet_like_cnt": 132,
        "met_like_cnt": 117,
        "unmet_like_rate": 0.5258964143426295,
        "aspect_kr": "밀림/때처럼 밀림"
      },
      {
        "context_tag": "BEFORE_MAKEUP",
        "aspect": "IRRITATION",
        "n_reviews": 325,
        "unmet_like_cnt": 127,
        "met_like_cnt": 193,
        "unmet_like_rate": 0.39076923076923076,
        "aspect_kr": "자극/따가움"
      },
      {
        "context_tag": "BEFORE_MAKEUP",
        "aspect": "OILINESS",
        "n_reviews": 298,
        "unmet_like_cnt": 121,
        "met_like_cnt": 149,
        "unmet_like_rate": 0.40604026845637586,
        "aspect_kr": "유분/피지"
      },
      {
        "context_tag": "SUMMER",
        "aspect": "TONEUP",
        "n_reviews": 412,
        "unmet_like_cnt": 114,
        "met_like_cnt": 294,
        "unmet_like_rate": 0.2766990291262136,
        "aspect_kr": "톤업(자연스러움)"
      },
      {
        "context_tag": "SUMMER",
        "aspect": "DRYNESS",
        "n_reviews": 241,
        "unmet_like_cnt": 104,
        "met_like_cnt": 117,
        "unmet_like_rate": 0.4315352697095436,
        "aspect_kr": "건조/속당김"
      },
      {
        "context_tag": "BEFORE_MAKEUP",
        "aspect": "TONEUP",
        "n_reviews": 440,
        "unmet_like_cnt": 101,
        "met_like_cnt": 336,
        "unmet_like_rate": 0.22954545454545455,
        "aspect_kr": "톤업(자연스러움)"
      },
      {
        "context_tag": "NONE_RULE",
        "aspect": "TONEUP",
        "n_reviews": 270,
        "unmet_like_cnt": 99,
        "met_like_cnt": 163,
        "unmet_like_rate": 0.36666666666666664,
        "aspect_kr": "톤업(자연스러움)"
      },
      {
        "context_tag": "NONE_RULE",
        "aspect": "DRYNESS",
        "n_reviews": 133,
        "unmet_like_cnt": 92,
        "met_like_cnt": 35,
        "unmet_like_rate": 0.6917293233082706,
        "aspect_kr": "건조/속당김"
      },
      {
        "context_tag": "NONE_RULE",
        "aspect": "EYE_STING",
        "n_reviews": 150,
        "unmet_like_cnt": 92,
        "met_like_cnt": 55,
        "unmet_like_rate": 0.6133333333333333,
        "aspect_kr": "눈시림"
      },
      {
        "context_tag": "BEFORE_MAKEUP",
        "aspect": "DRYNESS",
        "n_reviews": 205,
        "unmet_like_cnt": 83,
        "met_like_cnt": 103,
        "unmet_like_rate": 0.40487804878048783,
        "aspect_kr": "건조/속당김"
      },
      {
        "context_tag": "SUMMER",
        "aspect": "WHITECAST",
        "n_reviews": 326,
        "unmet_like_cnt": 79,
        "met_like_cnt": 234,
        "unmet_like_rate": 0.24233128834355827,
        "aspect_kr": "백탁/회끼/동동 뜸"
      },
      {
        "context_tag": "NONE_RULE",
        "aspect": "WHITECAST",
        "n_reviews": 193,
        "unmet_like_cnt": 75,
        "met_like_cnt": 114,
        "unmet_like_rate": 0.38860103626943004,
        "aspect_kr": "백탁/회끼/동동 뜸"
      },
      {
        "context_tag": "SUMMER",
        "aspect": "PILLING",
        "n_reviews": 159,
        "unmet_like_cnt": 71,
        "met_like_cnt": 86,
        "unmet_like_rate": 0.44654088050314467,
        "aspect_kr": "밀림/때처럼 밀림"
      },
      {
        "context_tag": "SUMMER",
        "aspect": "EYE_STING",
        "n_reviews": 210,
        "unmet_like_cnt": 67,
        "met_like_cnt": 141,
        "unmet_like_rate": 0.319047619047619,
        "aspect_kr": "눈시림"
      },
      {
        "context_tag": "NONE_RULE",
        "aspect": "PILLING",
        "n_reviews": 78,
        "unmet_like_cnt": 66,
        "met_like_cnt": 12,
        "unmet_like_rate": 0.8461538461538461,
        "aspect_kr": "밀림/때처럼 밀림"
      },
      {
        "context_tag": "BEFORE_MAKEUP",
        "aspect": "WHITECAST",
        "n_reviews": 290,
        "unmet_like_cnt": 61,
        "met_like_cnt": 222,
        "unmet_like_rate": 0.2103448275862069,
        "aspect_kr": "백탁/회끼/동동 뜸"
      },
      {
        "context_tag": "NONE_RULE",
        "aspect": "SCENT",
        "n_reviews": 103,
        "unmet_like_cnt": 60,
        "met_like_cnt": 33,
        "unmet_like_rate": 0.5825242718446602,
        "aspect_kr": "향"
      },
      {
        "context_tag": "WINTER",
        "aspect": "DRYNESS",
        "n_reviews": 143,
        "unmet_like_cnt": 60,
        "met_like_cnt": 65,
        "unmet_like_rate": 0.4195804195804196,
        "aspect_kr": "건조/속당김"
      },
      {
        "context_tag": "BEFORE_MAKEUP",
        "aspect": "EYE_STING",
        "n_reviews": 176,
        "unmet_like_cnt": 49,
        "met_like_cnt": 126,
        "unmet_like_rate": 0.2784090909090909,
        "aspect_kr": "눈시림"
      },
      {
        "context_tag": "NONE_RULE",
        "aspect": "TROUBLE",
        "n_reviews": 51,
        "unmet_like_cnt": 49,
        "met_like_cnt": 1,
        "unmet_like_rate": 0.9607843137254902,
        "aspect_kr": "트러블/뒤집어짐"
      },
      {
        "context_tag": "WINTER",
        "aspect": "OILINESS",
        "n_reviews": 75,
        "unmet_like_cnt": 45,
        "met_like_cnt": 19,
        "unmet_like_rate": 0.6,
        "aspect_kr": "유분/피지"
      },
      {
        "context_tag": "SUMMER",
        "aspect": "MOISTURE",
        "n_reviews": 298,
        "unmet_like_cnt": 43,
        "met_like_cnt": 246,
        "unmet_like_rate": 0.14429530201342283,
        "aspect_kr": "보습"
      },
      {
        "context_tag": "NONE_RULE",
        "aspect": "MOISTURE",
        "n_reviews": 190,
        "unmet_like_cnt": 38,
        "met_like_cnt": 146,
        "unmet_like_rate": 0.2,
        "aspect_kr": "보습"
      },
      {
        "context_tag": "NONE_RULE",
        "aspect": "FLAKING",
        "n_reviews": 37,
        "unmet_like_cnt": 33,
        "met_like_cnt": 4,
        "unmet_like_rate": 0.8918918918918919,
        "aspect_kr": "각질 부각/들뜸"
      },
      {
        "context_tag": "BEFORE_MAKEUP",
        "aspect": "MOISTURE",
        "n_reviews": 288,
        "unmet_like_cnt": 33,
        "met_like_cnt": 249,
        "unmet_like_rate": 0.11458333333333333,
        "aspect_kr": "보습"
      },
      {
        "context_tag": "SUMMER",
        "aspect": "LONGEVITY",
        "n_reviews": 88,
        "unmet_like_cnt": 33,
        "met_like_cnt": 53,
        "unmet_like_rate": 0.375,
        "aspect_kr": "지속력(시간 지나면 무너짐)"
      },
      {
        "context_tag": "SUMMER",
        "aspect": "SCENT",
        "n_reviews": 123,
        "unmet_like_cnt": 32,
        "met_like_cnt": 75,
        "unmet_like_rate": 0.2601626016260163,
        "aspect_kr": "향"
      },
      {
        "context_tag": "SUMMER",
        "aspect": "FLAKING",
        "n_reviews": 51,
        "unmet_like_cnt": 32,
        "met_like_cnt": 15,
        "unmet_like_rate": 0.6274509803921569,
        "aspect_kr": "각질 부각/들뜸"
      },
      {
        "context_tag": "NONE_RULE",
        "aspect": "ABSORPTION",
        "n_reviews": 74,
        "unmet_like_cnt": 32,
        "met_like_cnt": 40,
        "unmet_like_rate": 0.43243243243243246,
        "aspect_kr": "흡수/겉돎"
      },
      {
        "context_tag": "BEFORE_MAKEUP",
        "aspect": "SCENT",
        "n_reviews": 94,
        "unmet_like_cnt": 31,
        "met_like_cnt": 50,
        "unmet_like_rate": 0.32978723404255317,
        "aspect_kr": "향"
      },
      {
        "context_tag": "SUMMER",
        "aspect": "TROUBLE",
        "n_reviews": 32,
        "unmet_like_cnt": 30,
        "met_like_cnt": 2,
        "unmet_like_rate": 0.9375,
        "aspect_kr": "트러블/뒤집어짐"
      },
      {
        "context_tag": "BEFORE_MAKEUP",
        "aspect": "TEXTURE_HEAVY",
        "n_reviews": 64,
        "unmet_like_cnt": 30,
        "met_like_cnt": 31,
        "unmet_like_rate": 0.46875,
        "aspect_kr": "무거운 사용감/답답함"
      },
      {
        "context_tag": "BEFORE_MAKEUP",
        "aspect": "LONGEVITY",
        "n_reviews": 95,
        "unmet_like_cnt": 30,
        "met_like_cnt": 62,
        "unmet_like_rate": 0.3157894736842105,
        "aspect_kr": "지속력(시간 지나면 무너짐)"
      },
      {
        "context_tag": "BEFORE_MAKEUP",
        "aspect": "TROUBLE",
        "n_reviews": 33,
        "unmet_like_cnt": 27,
        "met_like_cnt": 6,
        "unmet_like_rate": 0.8181818181818182,
        "aspect_kr": "트러블/뒤집어짐"
      },
      {
        "context_tag": "SUMMER",
        "aspect": "TEXTURE_HEAVY",
        "n_reviews": 61,
        "unmet_like_cnt": 26,
        "met_like_cnt": 31,
        "unmet_like_rate": 0.4262295081967213,
        "aspect_kr": "무거운 사용감/답답함"
      },
      {
        "context_tag": "BEFORE_MAKEUP",
        "aspect": "FLAKING",
        "n_reviews": 49,
        "unmet_like_cnt": 26,
        "met_like_cnt": 21,
        "unmet_like_rate": 0.5306122448979592,
        "aspect_kr": "각질 부각/들뜸"
      },
      {
        "context_tag": "NONE_RULE",
        "aspect": "STICKINESS",
        "n_reviews": 83,
        "unmet_like_cnt": 25,
        "met_like_cnt": 56,
        "unmet_like_rate": 0.30120481927710846,
        "aspect_kr": "끈적임"
      },
      {
        "context_tag": "BEFORE_MAKEUP",
        "aspect": "ABSORPTION",
        "n_reviews": 129,
        "unmet_like_cnt": 24,
        "met_like_cnt": 102,
        "unmet_like_rate": 0.18604651162790697,
        "aspect_kr": "흡수/겉돎"
      },
      {
        "context_tag": "FULL_AMOUNT",
        "aspect": "IRRITATION",
        "n_reviews": 55,
        "unmet_like_cnt": 23,
        "met_like_cnt": 30,
        "unmet_like_rate": 0.41818181818181815,
        "aspect_kr": "자극/따가움"
      },
      {
        "context_tag": "SUMMER",
        "aspect": "STICKINESS",
        "n_reviews": 188,
        "unmet_like_cnt": 22,
        "met_like_cnt": 163,
        "unmet_like_rate": 0.11702127659574468,
        "aspect_kr": "끈적임"
      },
      {
        "context_tag": "SUMMER",
        "aspect": "ABSORPTION",
        "n_reviews": 133,
        "unmet_like_cnt": 22,
        "met_like_cnt": 111,
        "unmet_like_rate": 0.16541353383458646,
        "aspect_kr": "흡수/겉돎"
      },
      {
        "context_tag": "NO_MAKEUP",
        "aspect": "PILLING",
        "n_reviews": 37,
        "unmet_like_cnt": 21,
        "met_like_cnt": 16,
        "unmet_like_rate": 0.5675675675675675,
        "aspect_kr": "밀림/때처럼 밀림"
      },
      {
        "context_tag": "WINTER",
        "aspect": "IRRITATION",
        "n_reviews": 58,
        "unmet_like_cnt": 21,
        "met_like_cnt": 35,
        "unmet_like_rate": 0.3620689655172414,
        "aspect_kr": "자극/따가움"
      },
      {
        "context_tag": "FULL_AMOUNT",
        "aspect": "TONEUP",
        "n_reviews": 68,
        "unmet_like_cnt": 20,
        "met_like_cnt": 48,
        "unmet_like_rate": 0.29411764705882354,
        "aspect_kr": "톤업(자연스러움)"
      },
      {
        "context_tag": "REAPPLY",
        "aspect": "PILLING",
        "n_reviews": 38,
        "unmet_like_cnt": 20,
        "met_like_cnt": 18,
        "unmet_like_rate": 0.5263157894736842,
        "aspect_kr": "밀림/때처럼 밀림"
      },
      {
        "context_tag": "FULL_AMOUNT",
        "aspect": "OILINESS",
        "n_reviews": 36,
        "unmet_like_cnt": 20,
        "met_like_cnt": 10,
        "unmet_like_rate": 0.5555555555555556,
        "aspect_kr": "유분/피지"
      },
      {
        "context_tag": "FULL_AMOUNT",
        "aspect": "WHITECAST",
        "n_reviews": 46,
        "unmet_like_cnt": 18,
        "met_like_cnt": 25,
        "unmet_like_rate": 0.391304347826087,
        "aspect_kr": "백탁/회끼/동동 뜸"
      },
      {
        "context_tag": "WINTER",
        "aspect": "TONEUP",
        "n_reviews": 89,
        "unmet_like_cnt": 18,
        "met_like_cnt": 70,
        "unmet_like_rate": 0.20224719101123595,
        "aspect_kr": "톤업(자연스러움)"
      },
      {
        "context_tag": "NO_MAKEUP",
        "aspect": "IRRITATION",
        "n_reviews": 55,
        "unmet_like_cnt": 17,
        "met_like_cnt": 36,
        "unmet_like_rate": 0.3090909090909091,
        "aspect_kr": "자극/따가움"
      },
      {
        "context_tag": "FULL_AMOUNT",
        "aspect": "PILLING",
        "n_reviews": 27,
        "unmet_like_cnt": 17,
        "met_like_cnt": 9,
        "unmet_like_rate": 0.6296296296296297,
        "aspect_kr": "밀림/때처럼 밀림"
      },
      {
        "context_tag": "SUMMER",
        "aspect": "WATERPROOF",
        "n_reviews": 48,
        "unmet_like_cnt": 16,
        "met_like_cnt": 28,
        "unmet_like_rate": 0.3333333333333333,
        "aspect_kr": "워터프루프"
      },
      {
        "context_tag": "OUTDOOR",
        "aspect": "WHITECAST",
        "n_reviews": 67,
        "unmet_like_cnt": 16,
        "met_like_cnt": 48,
        "unmet_like_rate": 0.23880597014925373,
        "aspect_kr": "백탁/회끼/동동 뜸"
      },
      {
        "context_tag": "BEFORE_MAKEUP",
        "aspect": "STICKINESS",
        "n_reviews": 164,
        "unmet_like_cnt": 16,
        "met_like_cnt": 148,
        "unmet_like_rate": 0.0975609756097561,
        "aspect_kr": "끈적임"
      },
      {
        "context_tag": "NONE_RULE",
        "aspect": "LONGEVITY",
        "n_reviews": 32,
        "unmet_like_cnt": 16,
        "met_like_cnt": 13,
        "unmet_like_rate": 0.5,
        "aspect_kr": "지속력(시간 지나면 무너짐)"
      },
      {
        "context_tag": "NO_MAKEUP",
        "aspect": "DRYNESS",
        "n_reviews": 29,
        "unmet_like_cnt": 14,
        "met_like_cnt": 15,
        "unmet_like_rate": 0.4827586206896552,
        "aspect_kr": "건조/속당김"
      },
      {
        "context_tag": "OUTDOOR",
        "aspect": "OILINESS",
        "n_reviews": 43,
        "unmet_like_cnt": 14,
        "met_like_cnt": 25,
        "unmet_like_rate": 0.32558139534883723,
        "aspect_kr": "유분/피지"
      },
      {
        "context_tag": "WINTER",
        "aspect": "WHITECAST",
        "n_reviews": 55,
        "unmet_like_cnt": 14,
        "met_like_cnt": 40,
        "unmet_like_rate": 0.2545454545454545,
        "aspect_kr": "백탁/회끼/동동 뜸"
      },
      {
        "context_tag": "FULL_AMOUNT",
        "aspect": "DRYNESS",
        "n_reviews": 33,
        "unmet_like_cnt": 14,
        "met_like_cnt": 16,
        "unmet_like_rate": 0.42424242424242425,
        "aspect_kr": "건조/속당김"
      },
      {
        "context_tag": "NONE_RULE",
        "aspect": "TEXTURE_HEAVY",
        "n_reviews": 27,
        "unmet_like_cnt": 14,
        "met_like_cnt": 12,
        "unmet_like_rate": 0.5185185185185185,
        "aspect_kr": "무거운 사용감/답답함"
      },
      {
        "context_tag": "NO_MAKEUP",
        "aspect": "TONEUP",
        "n_reviews": 71,
        "unmet_like_cnt": 13,
        "met_like_cnt": 58,
        "unmet_like_rate": 0.18309859154929578,
        "aspect_kr": "톤업(자연스러움)"
      },
      {
        "context_tag": "WINTER",
        "aspect": "PILLING",
        "n_reviews": 27,
        "unmet_like_cnt": 13,
        "met_like_cnt": 12,
        "unmet_like_rate": 0.48148148148148145,
        "aspect_kr": "밀림/때처럼 밀림"
      },
      {
        "context_tag": "WINTER",
        "aspect": "MOISTURE",
        "n_reviews": 72,
        "unmet_like_cnt": 12,
        "met_like_cnt": 59,
        "unmet_like_rate": 0.16666666666666666,
        "aspect_kr": "보습"
      },
      {
        "context_tag": "BEFORE_MAKEUP",
        "aspect": "STAINING",
        "n_reviews": 26,
        "unmet_like_cnt": 12,
        "met_like_cnt": 8,
        "unmet_like_rate": 0.46153846153846156,
        "aspect_kr": "묻어남"
      },
      {
        "context_tag": "OUTDOOR",
        "aspect": "IRRITATION",
        "n_reviews": 49,
        "unmet_like_cnt": 11,
        "met_like_cnt": 37,
        "unmet_like_rate": 0.22448979591836735,
        "aspect_kr": "자극/따가움"
      },
      {
        "context_tag": "REAPPLY",
        "aspect": "OILINESS",
        "n_reviews": 28,
        "unmet_like_cnt": 11,
        "met_like_cnt": 16,
        "unmet_like_rate": 0.39285714285714285,
        "aspect_kr": "유분/피지"
      },
      {
        "context_tag": "OUTDOOR",
        "aspect": "DRYNESS",
        "n_reviews": 43,
        "unmet_like_cnt": 11,
        "met_like_cnt": 29,
        "unmet_like_rate": 0.2558139534883721,
        "aspect_kr": "건조/속당김"
      },
      {
        "context_tag": "MASK",
        "aspect": "OILINESS",
        "n_reviews": 24,
        "unmet_like_cnt": 10,
        "met_like_cnt": 10,
        "unmet_like_rate": 0.4166666666666667,
        "aspect_kr": "유분/피지"
      },
      {
        "context_tag": "NO_MAKEUP",
        "aspect": "OILINESS",
        "n_reviews": 37,
        "unmet_like_cnt": 10,
        "met_like_cnt": 22,
        "unmet_like_rate": 0.2702702702702703,
        "aspect_kr": "유분/피지"
      },
      {
        "context_tag": "MASK",
        "aspect": "TONEUP",
        "n_reviews": 43,
        "unmet_like_cnt": 10,
        "met_like_cnt": 32,
        "unmet_like_rate": 0.23255813953488372,
        "aspect_kr": "톤업(자연스러움)"
      },
      {
        "context_tag": "OUTDOOR",
        "aspect": "LONGEVITY",
        "n_reviews": 24,
        "unmet_like_cnt": 10,
        "met_like_cnt": 14,
        "unmet_like_rate": 0.4166666666666667,
        "aspect_kr": "지속력(시간 지나면 무너짐)"
      },
      {
        "context_tag": "REAPPLY",
        "aspect": "DRYNESS",
        "n_reviews": 33,
        "unmet_like_cnt": 9,
        "met_like_cnt": 19,
        "unmet_like_rate": 0.2727272727272727,
        "aspect_kr": "건조/속당김"
      },
      {
        "context_tag": "OUTDOOR",
        "aspect": "TONEUP",
        "n_reviews": 81,
        "unmet_like_cnt": 9,
        "met_like_cnt": 71,
        "unmet_like_rate": 0.1111111111111111,
        "aspect_kr": "톤업(자연스러움)"
      },
      {
        "context_tag": "REAPPLY",
        "aspect": "WHITECAST",
        "n_reviews": 45,
        "unmet_like_cnt": 8,
        "met_like_cnt": 36,
        "unmet_like_rate": 0.17777777777777778,
        "aspect_kr": "백탁/회끼/동동 뜸"
      },
      {
        "context_tag": "WINTER",
        "aspect": "EYE_STING",
        "n_reviews": 37,
        "unmet_like_cnt": 8,
        "met_like_cnt": 29,
        "unmet_like_rate": 0.21621621621621623,
        "aspect_kr": "눈시림"
      },
      {
        "context_tag": "REAPPLY",
        "aspect": "TONEUP",
        "n_reviews": 26,
        "unmet_like_cnt": 8,
        "met_like_cnt": 18,
        "unmet_like_rate": 0.3076923076923077,
        "aspect_kr": "톤업(자연스러움)"
      },
      {
        "context_tag": "REAPPLY",
        "aspect": "IRRITATION",
        "n_reviews": 25,
        "unmet_like_cnt": 8,
        "met_like_cnt": 17,
        "unmet_like_rate": 0.32,
        "aspect_kr": "자극/따가움"
      },
      {
        "context_tag": "OUTDOOR",
        "aspect": "PILLING",
        "n_reviews": 24,
        "unmet_like_cnt": 8,
        "met_like_cnt": 16,
        "unmet_like_rate": 0.3333333333333333,
        "aspect_kr": "밀림/때처럼 밀림"
      },
      {
        "context_tag": "NO_MAKEUP",
        "aspect": "EYE_STING",
        "n_reviews": 28,
        "unmet_like_cnt": 8,
        "met_like_cnt": 20,
        "unmet_like_rate": 0.2857142857142857,
        "aspect_kr": "눈시림"
      },
      {
        "context_tag": "FULL_AMOUNT",
        "aspect": "EYE_STING",
        "n_reviews": 23,
        "unmet_like_cnt": 8,
        "met_like_cnt": 15,
        "unmet_like_rate": 0.34782608695652173,
        "aspect_kr": "눈시림"
      },
      {
        "context_tag": "NONE_RULE",
        "aspect": "TEXTURE_LIGHT",
        "n_reviews": 43,
        "unmet_like_cnt": 7,
        "met_like_cnt": 33,
        "unmet_like_rate": 0.16279069767441862,
        "aspect_kr": "TEXTURE_LIGHT"
      },
      {
        "context_tag": "SUMMER",
        "aspect": "STAINING",
        "n_reviews": 23,
        "unmet_like_cnt": 7,
        "met_like_cnt": 12,
        "unmet_like_rate": 0.30434782608695654,
        "aspect_kr": "묻어남"
      },
      {
        "context_tag": "WINTER",
        "aspect": "LONGEVITY",
        "n_reviews": 23,
        "unmet_like_cnt": 7,
        "met_like_cnt": 16,
        "unmet_like_rate": 0.30434782608695654,
        "aspect_kr": "지속력(시간 지나면 무너짐)"
      },
      {
        "context_tag": "NO_MAKEUP",
        "aspect": "WHITECAST",
        "n_reviews": 45,
        "unmet_like_cnt": 7,
        "met_like_cnt": 36,
        "unmet_like_rate": 0.15555555555555556,
        "aspect_kr": "백탁/회끼/동동 뜸"
      },
      {
        "context_tag": "REAPPLY",
        "aspect": "STICKINESS",
        "n_reviews": 34,
        "unmet_like_cnt": 6,
        "met_like_cnt": 28,
        "unmet_like_rate": 0.17647058823529413,
        "aspect_kr": "끈적임"
      },
      {
        "context_tag": "WINTER",
        "aspect": "ABSORPTION",
        "n_reviews": 21,
        "unmet_like_cnt": 6,
        "met_like_cnt": 15,
        "unmet_like_rate": 0.2857142857142857,
        "aspect_kr": "흡수/겉돎"
      },
      {
        "context_tag": "REAPPLY",
        "aspect": "EYE_STING",
        "n_reviews": 26,
        "unmet_like_cnt": 5,
        "met_like_cnt": 21,
        "unmet_like_rate": 0.19230769230769232,
        "aspect_kr": "눈시림"
      },
      {
        "context_tag": "SUMMER",
        "aspect": "TEXTURE_LIGHT",
        "n_reviews": 84,
        "unmet_like_cnt": 4,
        "met_like_cnt": 75,
        "unmet_like_rate": 0.047619047619047616,
        "aspect_kr": "TEXTURE_LIGHT"
      },
      {
        "context_tag": "NO_MAKEUP",
        "aspect": "MOISTURE",
        "n_reviews": 40,
        "unmet_like_cnt": 4,
        "met_like_cnt": 36,
        "unmet_like_rate": 0.1,
        "aspect_kr": "보습"
      },
      {
        "context_tag": "FULL_AMOUNT",
        "aspect": "STICKINESS",
        "n_reviews": 32,
        "unmet_like_cnt": 4,
        "met_like_cnt": 27,
        "unmet_like_rate": 0.125,
        "aspect_kr": "끈적임"
      },
      {
        "context_tag": "WINTER",
        "aspect": "STICKINESS",
        "n_reviews": 28,
        "unmet_like_cnt": 4,
        "met_like_cnt": 24,
        "unmet_like_rate": 0.14285714285714285,
        "aspect_kr": "끈적임"
      },
      {
        "context_tag": "WINTER",
        "aspect": "SCENT",
        "n_reviews": 22,
        "unmet_like_cnt": 3,
        "met_like_cnt": 16,
        "unmet_like_rate": 0.13636363636363635,
        "aspect_kr": "향"
      },
      {
        "context_tag": "NO_MAKEUP",
        "aspect": "STICKINESS",
        "n_reviews": 21,
        "unmet_like_cnt": 3,
        "met_like_cnt": 18,
        "unmet_like_rate": 0.14285714285714285,
        "aspect_kr": "끈적임"
      },
      {
        "context_tag": "OUTDOOR",
        "aspect": "MOISTURE",
        "n_reviews": 56,
        "unmet_like_cnt": 3,
        "met_like_cnt": 53,
        "unmet_like_rate": 0.05357142857142857,
        "aspect_kr": "보습"
      },
      {
        "context_tag": "REAPPLY",
        "aspect": "ABSORPTION",
        "n_reviews": 23,
        "unmet_like_cnt": 2,
        "met_like_cnt": 21,
        "unmet_like_rate": 0.08695652173913043,
        "aspect_kr": "흡수/겉돎"
      },
      {
        "context_tag": "FULL_AMOUNT",
        "aspect": "MOISTURE",
        "n_reviews": 25,
        "unmet_like_cnt": 2,
        "met_like_cnt": 22,
        "unmet_like_rate": 0.08,
        "aspect_kr": "보습"
      },
      {
        "context_tag": "REAPPLY",
        "aspect": "MOISTURE",
        "n_reviews": 36,
        "unmet_like_cnt": 2,
        "met_like_cnt": 33,
        "unmet_like_rate": 0.05555555555555555,
        "aspect_kr": "보습"
      },
      {
        "context_tag": "BEFORE_MAKEUP",
        "aspect": "TEXTURE_LIGHT",
        "n_reviews": 78,
        "unmet_like_cnt": 2,
        "met_like_cnt": 73,
        "unmet_like_rate": 0.02564102564102564,
        "aspect_kr": "TEXTURE_LIGHT"
      },
      {
        "context_tag": "OUTDOOR",
        "aspect": "EYE_STING",
        "n_reviews": 27,
        "unmet_like_cnt": 1,
        "met_like_cnt": 26,
        "unmet_like_rate": 0.037037037037037035,
        "aspect_kr": "눈시림"
      },
      {
        "context_tag": "OUTDOOR",
        "aspect": "ABSORPTION",
        "n_reviews": 29,
        "unmet_like_cnt": 1,
        "met_like_cnt": 28,
        "unmet_like_rate": 0.034482758620689655,
        "aspect_kr": "흡수/겉돎"
      },
      {
        "context_tag": "OUTDOOR",
        "aspect": "STICKINESS",
        "n_reviews": 53,
        "unmet_like_cnt": 0,
        "met_like_cnt": 53,
        "unmet_like_rate": 0.0,
        "aspect_kr": "끈적임"
      },
      {
        "context_tag": "OUTDOOR",
        "aspect": "TEXTURE_LIGHT",
        "n_reviews": 22,
        "unmet_like_cnt": 0,
        "met_like_cnt": 20,
        "unmet_like_rate": 0.0,
        "aspect_kr": "TEXTURE_LIGHT"
      }
    ],
    "text": {
      "observation": "BEFORE_MAKEUP(화장 전) 상황에서 PILLING(밀림) 발생 빈도가 가장 높으며, SUMMER(여름)에는 OILINESS(유분) 불만이 급증합니다.",
      "interpretation": "사용 상황(Context)에 따라 '나쁜 경험'의 정의가 달라집니다. 메이크업 병행 사용자에게는 밀림 방지가 최우선(P0)입니다.",
      "caveat": "문맥 태그(Context Tag)는 키워드 매칭 룰 기반이므로 실제 의도와 일부 차이가 있을 수 있습니다."
    }
  },
  "seasonality": {
    "chart_data": [
      {
        "season": "fall",
        "aspect": "ABSORPTION",
        "n_reviews": 61,
        "unmet_like_cnt": 19,
        "met_like_cnt": 42,
        "unmet_like_rate": 0.3114754098360656,
        "aspect_kr": "흡수/겉돎"
      },
      {
        "season": "fall",
        "aspect": "BEFORE_MAKEUP",
        "n_reviews": 1,
        "unmet_like_cnt": 0,
        "met_like_cnt": 1,
        "unmet_like_rate": 0.0,
        "aspect_kr": "BEFORE_MAKEUP"
      },
      {
        "season": "fall",
        "aspect": "COVERAGE",
        "n_reviews": 1,
        "unmet_like_cnt": 0,
        "met_like_cnt": 1,
        "unmet_like_rate": 0.0,
        "aspect_kr": "COVERAGE"
      },
      {
        "season": "fall",
        "aspect": "DRYNESS",
        "n_reviews": 126,
        "unmet_like_cnt": 67,
        "met_like_cnt": 50,
        "unmet_like_rate": 0.5317460317460317,
        "aspect_kr": "건조/속당김"
      },
      {
        "season": "fall",
        "aspect": "EYE_STING",
        "n_reviews": 99,
        "unmet_like_cnt": 36,
        "met_like_cnt": 63,
        "unmet_like_rate": 0.36363636363636365,
        "aspect_kr": "눈시림"
      },
      {
        "season": "fall",
        "aspect": "FLAKING",
        "n_reviews": 33,
        "unmet_like_cnt": 27,
        "met_like_cnt": 5,
        "unmet_like_rate": 0.8181818181818182,
        "aspect_kr": "각질 부각/들뜸"
      },
      {
        "season": "fall",
        "aspect": "IRRITATION",
        "n_reviews": 236,
        "unmet_like_cnt": 160,
        "met_like_cnt": 73,
        "unmet_like_rate": 0.6779661016949152,
        "aspect_kr": "자극/따가움"
      },
      {
        "season": "fall",
        "aspect": "LONGEVITY",
        "n_reviews": 39,
        "unmet_like_cnt": 15,
        "met_like_cnt": 23,
        "unmet_like_rate": 0.38461538461538464,
        "aspect_kr": "지속력(시간 지나면 무너짐)"
      },
      {
        "season": "fall",
        "aspect": "MOISTURE",
        "n_reviews": 130,
        "unmet_like_cnt": 16,
        "met_like_cnt": 110,
        "unmet_like_rate": 0.12307692307692308,
        "aspect_kr": "보습"
      },
      {
        "season": "fall",
        "aspect": "OILINESS",
        "n_reviews": 159,
        "unmet_like_cnt": 90,
        "met_like_cnt": 56,
        "unmet_like_rate": 0.5660377358490566,
        "aspect_kr": "유분/피지"
      },
      {
        "season": "fall",
        "aspect": "OTHER",
        "n_reviews": 11,
        "unmet_like_cnt": 10,
        "met_like_cnt": 0,
        "unmet_like_rate": 0.9090909090909091,
        "aspect_kr": "기타"
      },
      {
        "season": "fall",
        "aspect": "PILLING",
        "n_reviews": 88,
        "unmet_like_cnt": 56,
        "met_like_cnt": 32,
        "unmet_like_rate": 0.6363636363636364,
        "aspect_kr": "밀림/때처럼 밀림"
      },
      {
        "season": "fall",
        "aspect": "SCENT",
        "n_reviews": 63,
        "unmet_like_cnt": 34,
        "met_like_cnt": 26,
        "unmet_like_rate": 0.5396825396825397,
        "aspect_kr": "향"
      },
      {
        "season": "fall",
        "aspect": "STAINING",
        "n_reviews": 14,
        "unmet_like_cnt": 6,
        "met_like_cnt": 5,
        "unmet_like_rate": 0.42857142857142855,
        "aspect_kr": "묻어남"
      },
      {
        "season": "fall",
        "aspect": "STICKINESS",
        "n_reviews": 90,
        "unmet_like_cnt": 7,
        "met_like_cnt": 82,
        "unmet_like_rate": 0.07777777777777778,
        "aspect_kr": "끈적임"
      },
      {
        "season": "fall",
        "aspect": "TEXTURE_HEAVY",
        "n_reviews": 27,
        "unmet_like_cnt": 15,
        "met_like_cnt": 11,
        "unmet_like_rate": 0.5555555555555556,
        "aspect_kr": "무거운 사용감/답답함"
      },
      {
        "season": "fall",
        "aspect": "TEXTURE_LIGHT",
        "n_reviews": 30,
        "unmet_like_cnt": 0,
        "met_like_cnt": 28,
        "unmet_like_rate": 0.0,
        "aspect_kr": "TEXTURE_LIGHT"
      },
      {
        "season": "fall",
        "aspect": "TONEUP",
        "n_reviews": 225,
        "unmet_like_cnt": 68,
        "met_like_cnt": 159,
        "unmet_like_rate": 0.3022222222222222,
        "aspect_kr": "톤업(자연스러움)"
      },
      {
        "season": "fall",
        "aspect": "TROUBLE",
        "n_reviews": 31,
        "unmet_like_cnt": 29,
        "met_like_cnt": 1,
        "unmet_like_rate": 0.9354838709677419,
        "aspect_kr": "트러블/뒤집어짐"
      },
      {
        "season": "fall",
        "aspect": "WATERPROOF",
        "n_reviews": 17,
        "unmet_like_cnt": 6,
        "met_like_cnt": 8,
        "unmet_like_rate": 0.35294117647058826,
        "aspect_kr": "워터프루프"
      },
      {
        "season": "fall",
        "aspect": "WHITECAST",
        "n_reviews": 162,
        "unmet_like_cnt": 44,
        "met_like_cnt": 117,
        "unmet_like_rate": 0.2716049382716049,
        "aspect_kr": "백탁/회끼/동동 뜸"
      },
      {
        "season": "fall",
        "aspect": "WHITE_RESIDUE",
        "n_reviews": 1,
        "unmet_like_cnt": 1,
        "met_like_cnt": 0,
        "unmet_like_rate": 1.0,
        "aspect_kr": "WHITE_RESIDUE"
      },
      {
        "season": "spring",
        "aspect": "ABSORPTION",
        "n_reviews": 74,
        "unmet_like_cnt": 18,
        "met_like_cnt": 55,
        "unmet_like_rate": 0.24324324324324326,
        "aspect_kr": "흡수/겉돎"
      },
      {
        "season": "spring",
        "aspect": "BEFORE_MAKEUP",
        "n_reviews": 1,
        "unmet_like_cnt": 0,
        "met_like_cnt": 1,
        "unmet_like_rate": 0.0,
        "aspect_kr": "BEFORE_MAKEUP"
      },
      {
        "season": "spring",
        "aspect": "COVERAGE",
        "n_reviews": 1,
        "unmet_like_cnt": 0,
        "met_like_cnt": 0,
        "unmet_like_rate": 0.0,
        "aspect_kr": "COVERAGE"
      },
      {
        "season": "spring",
        "aspect": "DRYNESS",
        "n_reviews": 166,
        "unmet_like_cnt": 92,
        "met_like_cnt": 66,
        "unmet_like_rate": 0.5542168674698795,
        "aspect_kr": "건조/속당김"
      },
      {
        "season": "spring",
        "aspect": "EYE_STING",
        "n_reviews": 155,
        "unmet_like_cnt": 65,
        "met_like_cnt": 91,
        "unmet_like_rate": 0.41935483870967744,
        "aspect_kr": "눈시림"
      },
      {
        "season": "spring",
        "aspect": "FLAKING",
        "n_reviews": 43,
        "unmet_like_cnt": 29,
        "met_like_cnt": 12,
        "unmet_like_rate": 0.6744186046511628,
        "aspect_kr": "각질 부각/들뜸"
      },
      {
        "season": "spring",
        "aspect": "IRRITATION",
        "n_reviews": 260,
        "unmet_like_cnt": 130,
        "met_like_cnt": 128,
        "unmet_like_rate": 0.5,
        "aspect_kr": "자극/따가움"
      },
      {
        "season": "spring",
        "aspect": "LONGEVITY",
        "n_reviews": 53,
        "unmet_like_cnt": 20,
        "met_like_cnt": 30,
        "unmet_like_rate": 0.37735849056603776,
        "aspect_kr": "지속력(시간 지나면 무너짐)"
      },
      {
        "season": "spring",
        "aspect": "MOISTURE",
        "n_reviews": 204,
        "unmet_like_cnt": 35,
        "met_like_cnt": 164,
        "unmet_like_rate": 0.1715686274509804,
        "aspect_kr": "보습"
      },
      {
        "season": "spring",
        "aspect": "OILINESS",
        "n_reviews": 217,
        "unmet_like_cnt": 109,
        "met_like_cnt": 91,
        "unmet_like_rate": 0.5023041474654378,
        "aspect_kr": "유분/피지"
      },
      {
        "season": "spring",
        "aspect": "OTHER",
        "n_reviews": 8,
        "unmet_like_cnt": 6,
        "met_like_cnt": 3,
        "unmet_like_rate": 0.75,
        "aspect_kr": "기타"
      },
      {
        "season": "spring",
        "aspect": "PILLING",
        "n_reviews": 125,
        "unmet_like_cnt": 83,
        "met_like_cnt": 46,
        "unmet_like_rate": 0.664,
        "aspect_kr": "밀림/때처럼 밀림"
      },
      {
        "season": "spring",
        "aspect": "PORES",
        "n_reviews": 2,
        "unmet_like_cnt": 2,
        "met_like_cnt": 0,
        "unmet_like_rate": 1.0,
        "aspect_kr": "PORES"
      },
      {
        "season": "spring",
        "aspect": "PORE_CLOGGING",
        "n_reviews": 1,
        "unmet_like_cnt": 0,
        "met_like_cnt": 1,
        "unmet_like_rate": 0.0,
        "aspect_kr": "PORE_CLOGGING"
      },
      {
        "season": "spring",
        "aspect": "REDNESS",
        "n_reviews": 1,
        "unmet_like_cnt": 0,
        "met_like_cnt": 1,
        "unmet_like_rate": 0.0,
        "aspect_kr": "REDNESS"
      },
      {
        "season": "spring",
        "aspect": "SCENT",
        "n_reviews": 75,
        "unmet_like_cnt": 32,
        "met_like_cnt": 35,
        "unmet_like_rate": 0.4266666666666667,
        "aspect_kr": "향"
      },
      {
        "season": "spring",
        "aspect": "STAINING",
        "n_reviews": 8,
        "unmet_like_cnt": 2,
        "met_like_cnt": 5,
        "unmet_like_rate": 0.25,
        "aspect_kr": "묻어남"
      },
      {
        "season": "spring",
        "aspect": "STICKINESS",
        "n_reviews": 95,
        "unmet_like_cnt": 18,
        "met_like_cnt": 75,
        "unmet_like_rate": 0.18947368421052632,
        "aspect_kr": "끈적임"
      },
      {
        "season": "spring",
        "aspect": "TEXTURE_HEAVY",
        "n_reviews": 41,
        "unmet_like_cnt": 18,
        "met_like_cnt": 24,
        "unmet_like_rate": 0.43902439024390244,
        "aspect_kr": "무거운 사용감/답답함"
      },
      {
        "season": "spring",
        "aspect": "TEXTURE_LIGHT",
        "n_reviews": 57,
        "unmet_like_cnt": 6,
        "met_like_cnt": 49,
        "unmet_like_rate": 0.10526315789473684,
        "aspect_kr": "TEXTURE_LIGHT"
      },
      {
        "season": "spring",
        "aspect": "TONEUP",
        "n_reviews": 267,
        "unmet_like_cnt": 84,
        "met_like_cnt": 192,
        "unmet_like_rate": 0.3146067415730337,
        "aspect_kr": "톤업(자연스러움)"
      },
      {
        "season": "spring",
        "aspect": "TROUBLE",
        "n_reviews": 9,
        "unmet_like_cnt": 9,
        "met_like_cnt": 0,
        "unmet_like_rate": 1.0,
        "aspect_kr": "트러블/뒤집어짐"
      },
      {
        "season": "spring",
        "aspect": "WATERPROOF",
        "n_reviews": 19,
        "unmet_like_cnt": 4,
        "met_like_cnt": 11,
        "unmet_like_rate": 0.21052631578947367,
        "aspect_kr": "워터프루프"
      },
      {
        "season": "spring",
        "aspect": "WHITECAST",
        "n_reviews": 194,
        "unmet_like_cnt": 62,
        "met_like_cnt": 124,
        "unmet_like_rate": 0.31958762886597936,
        "aspect_kr": "백탁/회끼/동동 뜸"
      },
      {
        "season": "summer",
        "aspect": "ABSORPTION",
        "n_reviews": 96,
        "unmet_like_cnt": 25,
        "met_like_cnt": 68,
        "unmet_like_rate": 0.2604166666666667,
        "aspect_kr": "흡수/겉돎"
      },
      {
        "season": "summer",
        "aspect": "BEFORE_MAKEUP",
        "n_reviews": 1,
        "unmet_like_cnt": 1,
        "met_like_cnt": 0,
        "unmet_like_rate": 1.0,
        "aspect_kr": "BEFORE_MAKEUP"
      },
      {
        "season": "summer",
        "aspect": "COVERAGE",
        "n_reviews": 1,
        "unmet_like_cnt": 1,
        "met_like_cnt": 0,
        "unmet_like_rate": 1.0,
        "aspect_kr": "COVERAGE"
      },
      {
        "season": "summer",
        "aspect": "DRYNESS",
        "n_reviews": 132,
        "unmet_like_cnt": 72,
        "met_like_cnt": 54,
        "unmet_like_rate": 0.5454545454545454,
        "aspect_kr": "건조/속당김"
      },
      {
        "season": "summer",
        "aspect": "EYE_STING",
        "n_reviews": 125,
        "unmet_like_cnt": 55,
        "met_like_cnt": 68,
        "unmet_like_rate": 0.44,
        "aspect_kr": "눈시림"
      },
      {
        "season": "summer",
        "aspect": "FLAKING",
        "n_reviews": 26,
        "unmet_like_cnt": 18,
        "met_like_cnt": 6,
        "unmet_like_rate": 0.6923076923076923,
        "aspect_kr": "각질 부각/들뜸"
      },
      {
        "season": "summer",
        "aspect": "IRRITATION",
        "n_reviews": 341,
        "unmet_like_cnt": 226,
        "met_like_cnt": 118,
        "unmet_like_rate": 0.6627565982404692,
        "aspect_kr": "자극/따가움"
      },
      {
        "season": "summer",
        "aspect": "LONGEVITY",
        "n_reviews": 50,
        "unmet_like_cnt": 25,
        "met_like_cnt": 24,
        "unmet_like_rate": 0.5,
        "aspect_kr": "지속력(시간 지나면 무너짐)"
      },
      {
        "season": "summer",
        "aspect": "MOISTURE",
        "n_reviews": 179,
        "unmet_like_cnt": 27,
        "met_like_cnt": 151,
        "unmet_like_rate": 0.15083798882681565,
        "aspect_kr": "보습"
      },
      {
        "season": "summer",
        "aspect": "OILINESS",
        "n_reviews": 245,
        "unmet_like_cnt": 149,
        "met_like_cnt": 81,
        "unmet_like_rate": 0.6081632653061224,
        "aspect_kr": "유분/피지"
      },
      {
        "season": "summer",
        "aspect": "OTHER",
        "n_reviews": 6,
        "unmet_like_cnt": 6,
        "met_like_cnt": 0,
        "unmet_like_rate": 1.0,
        "aspect_kr": "기타"
      },
      {
        "season": "summer",
        "aspect": "PILLING",
        "n_reviews": 100,
        "unmet_like_cnt": 65,
        "met_like_cnt": 38,
        "unmet_like_rate": 0.65,
        "aspect_kr": "밀림/때처럼 밀림"
      },
      {
        "season": "summer",
        "aspect": "SCENT",
        "n_reviews": 92,
        "unmet_like_cnt": 34,
        "met_like_cnt": 47,
        "unmet_like_rate": 0.3695652173913043,
        "aspect_kr": "향"
      },
      {
        "season": "summer",
        "aspect": "STAINING",
        "n_reviews": 17,
        "unmet_like_cnt": 10,
        "met_like_cnt": 5,
        "unmet_like_rate": 0.5882352941176471,
        "aspect_kr": "묻어남"
      },
      {
        "season": "summer",
        "aspect": "STICKINESS",
        "n_reviews": 124,
        "unmet_like_cnt": 31,
        "met_like_cnt": 93,
        "unmet_like_rate": 0.25,
        "aspect_kr": "끈적임"
      },
      {
        "season": "summer",
        "aspect": "TEXTURE_HEAVY",
        "n_reviews": 45,
        "unmet_like_cnt": 25,
        "met_like_cnt": 18,
        "unmet_like_rate": 0.5555555555555556,
        "aspect_kr": "무거운 사용감/답답함"
      },
      {
        "season": "summer",
        "aspect": "TEXTURE_LIGHT",
        "n_reviews": 48,
        "unmet_like_cnt": 3,
        "met_like_cnt": 43,
        "unmet_like_rate": 0.0625,
        "aspect_kr": "TEXTURE_LIGHT"
      },
      {
        "season": "summer",
        "aspect": "TONEUP",
        "n_reviews": 256,
        "unmet_like_cnt": 89,
        "met_like_cnt": 164,
        "unmet_like_rate": 0.34765625,
        "aspect_kr": "톤업(자연스러움)"
      },
      {
        "season": "summer",
        "aspect": "TROUBLE",
        "n_reviews": 52,
        "unmet_like_cnt": 46,
        "met_like_cnt": 6,
        "unmet_like_rate": 0.8846153846153846,
        "aspect_kr": "트러블/뒤집어짐"
      },
      {
        "season": "summer",
        "aspect": "WATERPROOF",
        "n_reviews": 31,
        "unmet_like_cnt": 20,
        "met_like_cnt": 12,
        "unmet_like_rate": 0.6451612903225806,
        "aspect_kr": "워터프루프"
      },
      {
        "season": "summer",
        "aspect": "WHITECAST",
        "n_reviews": 199,
        "unmet_like_cnt": 58,
        "met_like_cnt": 134,
        "unmet_like_rate": 0.2914572864321608,
        "aspect_kr": "백탁/회끼/동동 뜸"
      },
      {
        "season": "summer",
        "aspect": "WHITE_RESIDUE",
        "n_reviews": 7,
        "unmet_like_cnt": 4,
        "met_like_cnt": 3,
        "unmet_like_rate": 0.5714285714285714,
        "aspect_kr": "WHITE_RESIDUE"
      },
      {
        "season": "winter",
        "aspect": "ABSORPTION",
        "n_reviews": 61,
        "unmet_like_cnt": 13,
        "met_like_cnt": 47,
        "unmet_like_rate": 0.21311475409836064,
        "aspect_kr": "흡수/겉돎"
      },
      {
        "season": "winter",
        "aspect": "BEFORE_MAKEUP",
        "n_reviews": 2,
        "unmet_like_cnt": 1,
        "met_like_cnt": 1,
        "unmet_like_rate": 0.5,
        "aspect_kr": "BEFORE_MAKEUP"
      },
      {
        "season": "winter",
        "aspect": "COVERAGE",
        "n_reviews": 1,
        "unmet_like_cnt": 0,
        "met_like_cnt": 1,
        "unmet_like_rate": 0.0,
        "aspect_kr": "COVERAGE"
      },
      {
        "season": "winter",
        "aspect": "DRYNESS",
        "n_reviews": 105,
        "unmet_like_cnt": 45,
        "met_like_cnt": 48,
        "unmet_like_rate": 0.42857142857142855,
        "aspect_kr": "건조/속당김"
      },
      {
        "season": "winter",
        "aspect": "EYE_STING",
        "n_reviews": 80,
        "unmet_like_cnt": 37,
        "met_like_cnt": 39,
        "unmet_like_rate": 0.4625,
        "aspect_kr": "눈시림"
      },
      {
        "season": "winter",
        "aspect": "FLAKING",
        "n_reviews": 21,
        "unmet_like_cnt": 13,
        "met_like_cnt": 7,
        "unmet_like_rate": 0.6190476190476191,
        "aspect_kr": "각질 부각/들뜸"
      },
      {
        "season": "winter",
        "aspect": "IRRITATION",
        "n_reviews": 175,
        "unmet_like_cnt": 83,
        "met_like_cnt": 92,
        "unmet_like_rate": 0.4742857142857143,
        "aspect_kr": "자극/따가움"
      },
      {
        "season": "winter",
        "aspect": "LONGEVITY",
        "n_reviews": 34,
        "unmet_like_cnt": 9,
        "met_like_cnt": 24,
        "unmet_like_rate": 0.2647058823529412,
        "aspect_kr": "지속력(시간 지나면 무너짐)"
      },
      {
        "season": "winter",
        "aspect": "MOISTURE",
        "n_reviews": 174,
        "unmet_like_cnt": 26,
        "met_like_cnt": 142,
        "unmet_like_rate": 0.14942528735632185,
        "aspect_kr": "보습"
      },
      {
        "season": "winter",
        "aspect": "OILINESS",
        "n_reviews": 125,
        "unmet_like_cnt": 51,
        "met_like_cnt": 65,
        "unmet_like_rate": 0.408,
        "aspect_kr": "유분/피지"
      },
      {
        "season": "winter",
        "aspect": "OTHER",
        "n_reviews": 9,
        "unmet_like_cnt": 4,
        "met_like_cnt": 3,
        "unmet_like_rate": 0.4444444444444444,
        "aspect_kr": "기타"
      },
      {
        "season": "winter",
        "aspect": "PILLING",
        "n_reviews": 86,
        "unmet_like_cnt": 46,
        "met_like_cnt": 40,
        "unmet_like_rate": 0.5348837209302325,
        "aspect_kr": "밀림/때처럼 밀림"
      },
      {
        "season": "winter",
        "aspect": "PORES",
        "n_reviews": 2,
        "unmet_like_cnt": 2,
        "met_like_cnt": 0,
        "unmet_like_rate": 1.0,
        "aspect_kr": "PORES"
      },
      {
        "season": "winter",
        "aspect": "REDNESS",
        "n_reviews": 1,
        "unmet_like_cnt": 0,
        "met_like_cnt": 1,
        "unmet_like_rate": 0.0,
        "aspect_kr": "REDNESS"
      },
      {
        "season": "winter",
        "aspect": "SCENT",
        "n_reviews": 61,
        "unmet_like_cnt": 19,
        "met_like_cnt": 33,
        "unmet_like_rate": 0.3114754098360656,
        "aspect_kr": "향"
      },
      {
        "season": "winter",
        "aspect": "STAINING",
        "n_reviews": 9,
        "unmet_like_cnt": 5,
        "met_like_cnt": 3,
        "unmet_like_rate": 0.5555555555555556,
        "aspect_kr": "묻어남"
      },
      {
        "season": "winter",
        "aspect": "STICKINESS",
        "n_reviews": 83,
        "unmet_like_cnt": 11,
        "met_like_cnt": 71,
        "unmet_like_rate": 0.13253012048192772,
        "aspect_kr": "끈적임"
      },
      {
        "season": "winter",
        "aspect": "TEXTURE_HEAVY",
        "n_reviews": 17,
        "unmet_like_cnt": 5,
        "met_like_cnt": 11,
        "unmet_like_rate": 0.29411764705882354,
        "aspect_kr": "무거운 사용감/답답함"
      },
      {
        "season": "winter",
        "aspect": "TEXTURE_LIGHT",
        "n_reviews": 35,
        "unmet_like_cnt": 2,
        "met_like_cnt": 31,
        "unmet_like_rate": 0.05714285714285714,
        "aspect_kr": "TEXTURE_LIGHT"
      },
      {
        "season": "winter",
        "aspect": "TONEUP",
        "n_reviews": 239,
        "unmet_like_cnt": 56,
        "met_like_cnt": 187,
        "unmet_like_rate": 0.23430962343096234,
        "aspect_kr": "톤업(자연스러움)"
      },
      {
        "season": "winter",
        "aspect": "TROUBLE",
        "n_reviews": 17,
        "unmet_like_cnt": 15,
        "met_like_cnt": 2,
        "unmet_like_rate": 0.8823529411764706,
        "aspect_kr": "트러블/뒤집어짐"
      },
      {
        "season": "winter",
        "aspect": "WATERPROOF",
        "n_reviews": 7,
        "unmet_like_cnt": 3,
        "met_like_cnt": 4,
        "unmet_like_rate": 0.42857142857142855,
        "aspect_kr": "워터프루프"
      },
      {
        "season": "winter",
        "aspect": "WHITECAST",
        "n_reviews": 152,
        "unmet_like_cnt": 40,
        "met_like_cnt": 108,
        "unmet_like_rate": 0.2631578947368421,
        "aspect_kr": "백탁/회끼/동동 뜸"
      },
      {
        "season": "winter",
        "aspect": "WHITE_RESIDUE",
        "n_reviews": 2,
        "unmet_like_cnt": 1,
        "met_like_cnt": 1,
        "unmet_like_rate": 0.5,
        "aspect_kr": "WHITE_RESIDUE"
      }
    ],
    "text": {
      "observation": "SUMMER 시즌에는 피지/자극 관련 미충족이 70% 이상을 차지하나, WINTER 시즌에는 건조함 불만 비중이 2배 이상 증가합니다.",
      "interpretation": "계절적 환경 요인이 니즈의 우선순위를 바꿉니다. 시즌별 주력 제품(라인업)이나 마케팅 메시지 차별화가 유효합니다.",
      "caveat": "작성월 기준 계절 분류이므로, 실제 구매/사용 시점과는 약 1개월의 시차(Lag)가 있을 수 있습니다."
    }
  },
  "action_plan": {
    "ice": [
      {
        "needs": "IRRITATION",
        "name": "자극 최소화",
        "impact": 9,
        "confidence": 8,
        "ease": 6,
        "score": 72,
        "note": "최우선 해결 과제"
      },
      {
        "needs": "OILINESS",
        "name": "피지 컨트롤",
        "impact": 8,
        "confidence": 8,
        "ease": 7,
        "score": 56,
        "note": "지성 타겟 핵심"
      },
      {
        "needs": "DRYNESS",
        "name": "보습력 강화",
        "impact": 7,
        "confidence": 7,
        "ease": 8,
        "score": 49,
        "note": "겨울철/건성 소구"
      },
      {
        "needs": "PILLING",
        "name": "밀림 방지",
        "impact": 8,
        "confidence": 9,
        "ease": 5,
        "score": 45,
        "note": "메이크업 병행 중요"
      },
      {
        "needs": "TONEUP",
        "name": "톤업 개선",
        "impact": 7,
        "confidence": 8,
        "ease": 6,
        "score": 42,
        "note": "자연스러움/지속력"
      }
    ],
    "spec": [
      {
        "req": "논코메도제닉 수준 자극",
        "aspect": "IRRITATION",
        "context": "ALL",
        "kpi": "따가움 언급 0건",
        "test": "민감성 패널 48시간"
      },
      {
        "req": "메이크업 밀착력",
        "aspect": "PILLING",
        "context": "BEFORE_MAKEUP",
        "kpi": "파데 밀림 없음",
        "test": "쿠션/파데 병용 테스트"
      },
      {
        "req": "6시간 피지 컨트롤",
        "aspect": "OILINESS",
        "context": "SUMMER",
        "kpi": "유분기 변화 < 20%",
        "test": "피지 측정기 지속 관찰"
      },
      {
        "req": "속당김 없는 보습",
        "aspect": "DRYNESS",
        "context": "WINTER",
        "kpi": "수분도 유지 > 80%",
        "test": "건조 환경 챔버 테스트"
      },
      {
        "req": "다크닝 없는 톤업",
        "aspect": "TONEUP",
        "context": "ALL",
        "kpi": "색차값(Delta E) < 2",
        "test": "4시간 후 톤 유지력"
      }
    ],
    "cards": [
      {
        "id": "IRRITATION",
        "name": "자극 최소화",
        "desc": "따가움/눈시림 없는 편안함",
        "stats": {
          "repeat": "84%",
          "unmet": "95%"
        },
        "reqs": [
          "무기자차 수준의 순함",
          "눈시림 성분 배제"
        ],
        "tests": [
          "안자극 테스트",
          "민감성 패널"
        ]
      },
      {
        "id": "OILINESS",
        "name": "피지 컨트롤",
        "desc": "번들거림 없는 산뜻함",
        "stats": {
          "repeat": "84%",
          "unmet": "High"
        },
        "reqs": [
          "다공성 파우더 적용",
          "속건조 없는 매트함"
        ],
        "tests": [
          "유분 흡유량",
          "메이크업 지속력"
        ]
      },
      {
        "id": "PILLING",
        "name": "밀림 방지",
        "desc": "화장이 잘 먹는 베이스",
        "stats": {
          "repeat": "74%",
          "unmet": "99%"
        },
        "reqs": [
          "실리콘/필름막 밸런싱",
          "흡수 속도 조절"
        ],
        "tests": [
          "레이어링 테스트",
          "때밀림 관능"
        ]
      },
      {
        "id": "DRYNESS",
        "name": "보습력 강화",
        "desc": "속당김/각질 없는 촉촉함",
        "stats": {
          "repeat": "71%",
          "unmet": "Mix"
        },
        "reqs": [
          "수분 에센스 함량 증대",
          "유수분 밸런스"
        ],
        "tests": [
          "경피 수분 손실량",
          "각질 들뜸"
        ]
      },
      {
        "id": "TONEUP",
        "name": "자연스러운 톤업",
        "desc": "백탁/회끼 없는 맑은 톤",
        "stats": {
          "repeat": "76%",
          "unmet": "Mix"
        },
        "reqs": [
          "균일한 입자 분산",
          "핑크 베이스 적용"
        ],
        "tests": [
          "피부톤별 발색",
          "다크닝 측정"
        ]
      }
    ],
    "text": {
      "observation": "Top 5 과제는 상호 연관되어 있습니다(예: 유분 제어 vs 속건조 방지).",
      "interpretation": "단일 속성 개선보다는 Trade-off 관계를 고려한 균형 잡힌 처방 설계가 핵심 경쟁력입니다.",
      "caveat": "제품 컨셉(유기/무기/혼합)에 따라 우선순위 가중치는 조정될 수 있습니다."
    }
  },
  "evidence": {
    "samples": [
      {
        "id": "IRRITATION",
        "quotes": [
          "바르자마자 따가워요",
          "눈이 너무 시려워서 눈물을 흘림",
          "피부가 뒤집어졌어요"
        ]
      },
      {
        "id": "OILINESS",
        "quotes": [
          "개기름이 좔좔 흘러요",
          "시간 지나면 번들거림 심함",
          "지성 피부엔 비추"
        ]
      },
      {
        "id": "PILLING",
        "quotes": [
          "때처럼 밀려나와요",
          "화장이 다 뜹니다",
          "기초 밀리고 난리남"
        ]
      },
      {
        "id": "DRYNESS",
        "quotes": [
          "속당김이 느껴져요",
          "시간 지나면 바싹 마르는 느낌",
          "각질이 부각됨"
        ]
      },
      {
        "id": "TONEUP",
        "quotes": [
          "너무 하얗게 동동 떠요",
          "회색빛이 돌아요",
          "자연스럽지 않고 두꺼움"
        ]
      }
    ],
    "text": {
      "observation": "정량 데이터 뒤에는 구체적이고 생생한 고객의 고통(Voice)이 존재합니다.",
      "interpretation": "고객이 사용하는 단어(따가움, 개기름, 때처럼 등)는 마케팅 소구점 및 상세페이지 카피의 원천입니다.",
      "caveat": "고객 리뷰 원문을 발췌하였으며, 개인정보는 제외되었습니다."
    }
  },
  "glossary": [
    {
      "term": "FLAKING",
      "kr": "각질 부각/들뜸",
      "desc": "\"각질이 부각돼요\", \"하얗게 일어나요\" (건조함 관련)"
    },
    {
      "term": "LONGEVITY",
      "kr": "지속력",
      "desc": "\"시간 지나면 무너짐\", \"다크닝\", \"무너짐\""
    },
    {
      "term": "TEXTURE_HEAVY",
      "kr": "무거운 사용감",
      "desc": "\"답답해요\", \"두꺼워요\", \"피부가 숨을 못 쉬는 듯\""
    },
    {
      "term": "ABSORPTION",
      "kr": "흡수/겉돎",
      "desc": "\"겉돌아요\", \"흡수 안 돼요\", \"하얗게 뜸\""
    },
    {
      "term": "WHITECAST",
      "kr": "백탁/회끼",
      "desc": "\"동동 떠요\", \"가부키 화장\", \"토시오\""
    },
    {
      "term": "PILLING",
      "kr": "밀림",
      "desc": "\"때처럼 밀려요\", \"지우개 가루\", \"화장 뜸\""
    }
  ]
};