"""
Step 5 v2: Export PDF
Playwright script to render report/site_v2/index.html to PDF.
"""
import os
import time
import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SITE_PATH = "report/site_v2/index.html"
PDF_PATH = "report/final/suncream_unmet_needs_report_v2.pdf"

def generate_pdf():
    abs_path = os.path.abspath(SITE_PATH)
    file_url = f"file://{abs_path}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        logger.info(f"Loading {file_url}...")
        page.goto(file_url, wait_until="networkidle")
        
        # Additional wait for ECharts animations
        time.sleep(3)
        
        # Create output dir
        os.makedirs(os.path.dirname(PDF_PATH), exist_ok=True)
        
        logger.info(f"Exporting to {PDF_PATH}...")
        page.pdf(
            path=PDF_PATH,
            format="A4",
            print_background=True,
            margin={"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"}
        )
        browser.close()
        logger.info("PDF V2 Generation Completed.")

if __name__ == "__main__":
    generate_pdf()
