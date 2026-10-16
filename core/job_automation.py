from datetime import datetime
from typing import List, Dict, Any
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from config import Config
from utils.logger import logger

class JobAutomation:
    def __init__(self, page: Page):
        self.page = page

    def take_screenshot(self, name: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = Config.SCREENSHOT_DIR / f"{name}_{timestamp}.png"
        self.page.screenshot(path=str(filepath))
        logger.info(f"Screenshot captured: {filepath.name}")
        return str(filepath)

    def navigate_and_search(self, keyword: str):
        logger.info(f"Navigating to job portal: {Config.BASE_URL}")
        try:
            self.page.goto(Config.BASE_URL, wait_until="domcontentloaded", timeout=20000)
            self.take_screenshot("portal_loaded")


            logger.info(f"Interacting with search input (query: '{keyword}')...")
            search_input = self.page.locator("#id-searchfield, input[name='q'], input[type='search']").first
            search_input.wait_for(state="visible", timeout=10000)
            
            search_input.click()
            search_input.fill("")
            search_input.type(keyword, delay=80)
            
            self.take_screenshot("form_interaction_completed")
            logger.info("Search form populated and verified.")

        except PlaywrightTimeoutError as e:
            logger.error(f"Navigation or form interaction timed out: {e}")
            self.take_screenshot("error_timeout")
            raise

    def extract_jobs(self, limit: int) -> List[Dict[str, Any]]:
        logger.info(f"Extracting up to {limit} active job postings...")
        results = []

        try:
            job_items = self.page.locator("ol.list-recent-jobs li")
            total_items = job_items.count()
            count = min(total_items, limit)
            logger.info(f"Detected {total_items} jobs on the board. Parsing top {count}...")

            for i in range(count):
                item = job_items.nth(i)

                link_elem = item.locator("span.listing-company-name a, h2 a").first
                title = link_elem.text_content().strip() if link_elem.count() > 0 else "N/A"
                href = link_elem.get_attribute("href") if link_elem.count() > 0 else ""
                full_url = f"https://www.python.org{href}" if href.startswith("/") else href

                category_elem = item.locator("span.listing-company-category a, span.listing-company-category").first
                category = category_elem.text_content().strip() if category_elem.count() > 0 else "Developer / Engineer"

                location_elem = item.locator("span.listing-location a, span.listing-location").first
                location = location_elem.text_content().strip() if location_elem.count() > 0 else "Remote"

                job_type_elem = item.locator("span.listing-job-type a, span.listing-job-type").first
                job_type = job_type_elem.text_content().strip() if job_type_elem.count() > 0 else "Full Time"

                company_display = f"{category} ({job_type})"

                results.append({
                    "title": title,
                    "company": company_display,
                    "location": location,
                    "url": full_url
                })
                logger.info(f"[{i + 1}] {title} | {company_display} | {location}")

            self.take_screenshot("extraction_completed")
            return results

        except Exception as e:
            logger.error(f"Data extraction failed: {e}")
            self.take_screenshot("error_extraction")
            raise