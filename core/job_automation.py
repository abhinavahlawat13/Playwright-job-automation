import urllib.parse
from datetime import datetime
from typing import List, Dict, Any
from playwright.sync_api import Page
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

    def _handle_cloudflare_if_present(self):
        """Waits for security verification check to resolve if triggered."""
        cf_detected = (
            "verification" in self.page.title().lower()
            or self.page.locator("text=Performing security verification").count() > 0
            or self.page.locator("#challenge-running").count() > 0
        )
        if cf_detected:
            logger.info("Cloudflare challenge detected. Waiting 7 seconds for verification...")
            self.page.wait_for_timeout(7000)

    def navigate_and_search(self, keyword: str):
        encoded_keyword = urllib.parse.quote_plus(keyword)
        target_url = f"{Config.BASE_URL}/remote-jobs/search?term={encoded_keyword}"
        
        logger.info(f"Navigating to target: {target_url}")
        try:
            self.page.goto(target_url, wait_until="domcontentloaded", timeout=20000)
            self._handle_cloudflare_if_present()
            self.page.wait_for_load_state("networkidle")
            self.take_screenshot("search_page_loaded")
        except Exception as e:
            logger.warning(f"Initial load notice: {e}. Checking security challenge state...")
            self._handle_cloudflare_if_present()

    def extract_jobs(self, limit: int) -> List[Dict[str, Any]]:
        logger.info(f"Extracting up to {limit} listings...")
        results = []

        try:
            job_links = self.page.locator("a[href*='/remote-jobs/']")
            total_links = job_links.count()
            logger.info(f"Detected {total_links} job anchors on page.")

            seen_urls = set()
            idx = 0

            while len(results) < limit and idx < total_links:
                link = job_links.nth(idx)
                idx += 1

                href = link.get_attribute("href") or ""
                if not href or href in seen_urls or href.endswith(("/remote-jobs", "/remote-jobs/")):
                    continue

                full_url = href if href.startswith("http") else f"{Config.BASE_URL}{href}"
                seen_urls.add(href)

                card = link.locator("xpath=./ancestor::li[1]")
                container = card if card.count() > 0 else link

                title = "N/A"
                for sel in ["span.title", "h3", ".title"]:
                    el = container.locator(sel).first
                    if el.count() > 0 and el.is_visible():
                        title = el.text_content().strip()
                        break

                company = "N/A"
                for sel in ["span.company", ".company"]:
                    el = container.locator(sel).first
                    if el.count() > 0 and el.is_visible():
                        company = el.text_content().strip()
                        break

                region = "N/A"
                for sel in ["span.region", ".region"]:
                    el = container.locator(sel).first
                    if el.count() > 0 and el.is_visible():
                        region = el.text_content().strip()
                        break

                results.append({
                    "title": title,
                    "company": company,
                    "location": region,
                    "url": full_url
                })

            logger.info(f"Extracted {len(results)} valid job records.")
            self.take_screenshot("extraction_completed")
            return results

        except Exception as e:
            logger.error(f"Error during job extraction: {e}")
            self.take_screenshot("error_extraction")
            raise