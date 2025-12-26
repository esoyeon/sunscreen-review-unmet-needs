#!/bin/bash

# Stop on error
set -e

echo "=== Sunblock Review Analysis Pipeline Start ==="

# 1. Processing
echo "[Step 3-0] Running Baseline Preprocessing..."
python -m src.processing.baseline

echo "[Step 3-0.5] Running Deduplication..."
python -m src.processing.deduplication

echo "[Step 3-1] Running Tagging..."
python -m src.processing.tagging

echo "[Step 3-2] Generating LLM Queue..."
python -m src.processing.llm_queue

# Note: Step 3-3 (LLM Batch) is skipped by default to avoid accidental costs.
# Uncomment the line below to run it.
# python -m src.processing.llm_batch

# 2. Analysis
echo "[Step 4-0] Running Join & Pivot..."
python -m src.analysis.join_pivot

echo "[Step 4-1] Generating Insight Report..."
python -m src.analysis.insight_report

# 3. Dashboard
echo "[Step 5] Building Dashboard..."
python -m src.dashboard.build_dashboard

echo "[Step 5-1] Exporting PDF..."
python -m src.dashboard.export_pdf

echo "=== Pipeline Completed Successfully ==="
