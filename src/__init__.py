# 올리브영 선크림 리뷰 수집 및 분석 파이프라인
"""
올리브영 선크림 카테고리 제품의 리뷰를 수집하고 분석하는 패키지.

Subpackages:
    - processing: 데이터 전처리 (Deduplication, Tagging, LLM Prep)
    - analysis: 데이터 분석 (Join, Pivot, Insight)
    - dashboard: 대시보드 및 리포트 생성

Modules:
    - catalog: 카탈로그 수집
    - reviews: 리뷰 API 호출
    - filters: 노이즈 태깅
    - io: 데이터 저장
    - report: 수집 요약 리포트 생성
    - pipeline: CLI 진입점
"""

__version__ = "1.1.0"
