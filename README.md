# Sunblock Review Analysis Project

올리브영 선크림 리뷰 데이터를 수집, 전처리, 분석하여 미충족 니즈(Unmet Needs)를 발굴하는 프로젝트입니다.

## 📂 프로젝트 구조

```
.
├── config/                 # 설정 파일 (tag_lexicon 등)
├── data/                   # 데이터 디렉토리
│   ├── raw/                # 수집된 원본 데이터
│   ├── processed/          # 전처리된 데이터
│   ├── llm/                # LLM 추출/분석 데이터
│   └── analysis/           # 최종 분석용 통계 테이블
├── notebooks/              # 분석용 Jupyter Notebook
├── report/                 # 생성된 리포트 및 대시보드
├── src/                    # 소스 코드
│   ├── processing/         # 데이터 전처리 모듈 (Step 3)
│   ├── analysis/           # 데이터 분석 모듈 (Step 4)
│   ├── dashboard/          # 대시보드/PDF 생성 모듈 (Step 5)
│   └── ...                 # 크롤링/공통 모듈
├── config.yaml             # 크롤링 설정
└── requirements.txt        # 의존성 패키지 목록
```

## 🚀 설치 방법

1. Python 3.9+ 환경 준비
2. 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```
3. Playwright 브라우저 설치 (PDF 변환용)
   ```bash
   playwright install chromium
   ```

## 📊 실행 가이드

### 0. 원클릭 파이프라인 실행
전체 분석 과정을 (수집 제외) 한 번에 실행합니다.

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

### 1-2. 데이터 수집 (Crawling)
올리브영 사이트에서 상품 및 리뷰 데이터를 수집합니다.

```bash
# 전체 수집 (카탈로그 -> 리뷰 -> 태깅)
python -m src.pipeline crawl_all

# 단계별 수집
python -m src.pipeline crawl_catalog
python -m src.pipeline crawl_reviews
```

### 3. 데이터 전처리 (Processing)
수집된 리뷰를 정제하고 분석 가능한 형태로 가공합니다.

**Step 3-0: Baseline 전처리**
```bash
python -m src.processing.baseline
```

**Step 3-0.5: 중복 제거**
```bash
python -m src.processing.deduplication
```

**Step 3-1: 태깅 (Attribute/Context/Skin)**
```bash
python -m src.processing.tagging
```

**Step 3-2: LLM 분석 큐 생성**
```bash
python -m src.processing.llm_queue
```

**Step 3-3: LLM 일괄 처리 (선택사항)**
> 주의: OpenAI API 비용이 발생할 수 있습니다.
```bash
python -m src.processing.llm_batch
```

### 4. 데이터 분석 (Analysis)
처리된 데이터를 바탕으로 통계 및 인사이트를 도출합니다.

**Step 4-0: Join & Pivot 테이블 생성**
```bash
python -m src.analysis.join_pivot
```

**Step 4-1: 인사이트 리포트 생성**
```bash
python -m src.analysis.insight_report
```

### 5. 대시보드 및 리포트 (Dashboard)
최종 결과물을 시각화하고 PDF로 변환합니다.

**Step 5: 대시보드 데이터 빌드**
```bash
python -m src.dashboard.build_dashboard
```

**Step 5-1: PDF 발행**
```bash
python -m src.dashboard.export_pdf
```

## 📝 주요 산출물

- **데이터**: `data/analysis/` 내 `parquet` 파일들
- **리포트**: `report/` 내 마크다운 리포트
- **대시보드**: `report/site_v2/index.html`
- **최종 PDF**: `report/final/suncream_unmet_needs_report_v2.pdf`
