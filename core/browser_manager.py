from contextlib import contextmanager
from playwright.sync_api import sync_playwright, Browser, Page
from config import Config
from utils.logger import logger

class BrowserManager:
    @staticmethod
    @contextmanager
    def get_page():
        with sync_playwright() as p:
            logger.info(f"Launching Browser (Headless={Config.HEADLESS})...")
            browser: Browser = p.chromium.launch(headless=Config.HEADLESS)
            page: Page = browser.new_page()
            page.set_default_timeout(20000)

            try:
                yield page
            finally:
                logger.info("Closing browser session cleanly.")
                browser.close()