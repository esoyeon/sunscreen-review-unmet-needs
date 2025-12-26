"""
메인 파이프라인 진입점

CLI를 통해 카탈로그 수집, 리뷰 수집, 전체 파이프라인을 실행합니다.
"""

import os
import sys
import argparse
import logging
from datetime import datetime
from typing import Dict, Any, Optional

import yaml

from .catalog import collect_catalog
from .reviews import collect_reviews
from .filters import apply_noise_tags
from .io import DataIO, save_data
from .report import generate_report

# 로깅 설정
def setup_logging(config: Dict[str, Any]) -> None:
    """로깅 설정"""
    log_dir = config.get('output', {}).get('log_dir', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_filename = f"crawl_{datetime.now().strftime('%Y%m%d')}.log"
    log_path = os.path.join(log_dir, log_filename)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

logger = logging.getLogger(__name__)


def load_config(config_path: str = 'config.yaml') -> Dict[str, Any]:
    """설정 파일 로드"""
    if not os.path.exists(config_path):
        logger.warning(f"설정 파일 없음: {config_path}, 기본값 사용")
        return {}
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config or {}


def crawl_catalog_only(config: Dict[str, Any]) -> None:
    """카탈로그만 수집"""
    logger.info("=== 카탈로그 수집 시작 ===")
    
    products = collect_catalog(config)
    
    if products:
        io = DataIO(config)
        path = io.save_products_jsonl(products)
        logger.info(f"카탈로그 저장 완료: {path}")
    else:
        logger.error("카탈로그 수집 실패")


def crawl_reviews_only(
    config: Dict[str, Any], 
    top_n: Optional[int] = None,
    products_file: Optional[str] = None
) -> None:
    """리뷰만 수집 (기존 카탈로그 사용)"""
    logger.info("=== 리뷰 수집 시작 ===")
    
    # 카탈로그 로드
    io = DataIO(config)
    products = io.load_products_jsonl(products_file)
    
    if not products:
        logger.error("카탈로그 파일 없음. 먼저 카탈로그를 수집하세요.")
        return
    
    # top_n 결정
    if top_n is None:
        top_n = config.get('reviews', {}).get('top_n', 150)
    
    logger.info(f"상위 {top_n}개 상품 리뷰 수집")
    
    # 리뷰 수집
    reviews = collect_reviews(config, products, top_n)
    
    if reviews:
        # 노이즈 태깅
        reviews = apply_noise_tags(config, reviews)
        
        # 저장
        paths = save_data(config, reviews=reviews)
        
        # 리포트 생성
        report_path = generate_report(config, products, reviews, paths)
        logger.info(f"리포트 생성 완료: {report_path}")
    else:
        logger.error("리뷰 수집 실패")


def crawl_all(config: Dict[str, Any], top_n: Optional[int] = None) -> None:
    """전체 파이프라인 실행"""
    logger.info("=== 전체 파이프라인 시작 ===")
    
    # 1. 카탈로그 수집
    logger.info("--- 단계 1: 카탈로그 수집 ---")
    products = collect_catalog(config)
    
    if not products:
        logger.error("카탈로그 수집 실패, 파이프라인 중단")
        return
    
    # 카탈로그 저장
    io = DataIO(config)
    products_path = io.save_products_jsonl(products)
    
    # 2. 리뷰 수집
    logger.info("--- 단계 2: 리뷰 수집 ---")
    if top_n is None:
        top_n = config.get('reviews', {}).get('top_n', 150)
    
    reviews = collect_reviews(config, products, top_n)
    
    if not reviews:
        logger.warning("리뷰 수집 실패, 카탈로그만 저장됨")
        generate_report(config, products, [], {'products_jsonl': products_path})
        return
    
    # 3. 노이즈 태깅
    logger.info("--- 단계 3: 노이즈 태깅 ---")
    reviews = apply_noise_tags(config, reviews)
    
    # 4. 저장
    logger.info("--- 단계 4: 데이터 저장 ---")
    paths = save_data(config, products=products, reviews=reviews)
    
    # 5. 리포트 생성
    logger.info("--- 단계 5: 리포트 생성 ---")
    report_path = generate_report(config, products, reviews, paths)
    
    logger.info("=== 파이프라인 완료 ===")
    logger.info(f"- 상품: {len(products)}개")
    logger.info(f"- 리뷰: {len(reviews)}개")
    logger.info(f"- 리포트: {report_path}")


def main():
    """CLI 진입점"""
    parser = argparse.ArgumentParser(
        description='올리브영 선크림 리뷰 수집 파이프라인'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='실행할 명령')
    
    # crawl_all 명령
    all_parser = subparsers.add_parser('crawl_all', help='전체 파이프라인 실행')
    all_parser.add_argument(
        '--top_n', type=int, default=None,
        help='리뷰 수집 대상 상품 수 (기본: config.yaml 값)'
    )
    all_parser.add_argument(
        '--config', type=str, default='config.yaml',
        help='설정 파일 경로'
    )
    
    # crawl_catalog 명령
    catalog_parser = subparsers.add_parser('crawl_catalog', help='카탈로그만 수집')
    catalog_parser.add_argument(
        '--config', type=str, default='config.yaml',
        help='설정 파일 경로'
    )
    
    # crawl_reviews 명령
    reviews_parser = subparsers.add_parser('crawl_reviews', help='리뷰만 수집')
    reviews_parser.add_argument(
        '--top_n', type=int, default=None,
        help='리뷰 수집 대상 상품 수'
    )
    reviews_parser.add_argument(
        '--products_file', type=str, default=None,
        help='카탈로그 파일명 (기본: 가장 최근 파일)'
    )
    reviews_parser.add_argument(
        '--config', type=str, default='config.yaml',
        help='설정 파일 경로'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 설정 로드
    config_path = getattr(args, 'config', 'config.yaml')
    config = load_config(config_path)
    
    # 로깅 설정
    setup_logging(config)
    
    # 명령 실행
    if args.command == 'crawl_all':
        crawl_all(config, args.top_n)
    elif args.command == 'crawl_catalog':
        crawl_catalog_only(config)
    elif args.command == 'crawl_reviews':
        crawl_reviews_only(config, args.top_n, args.products_file)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
