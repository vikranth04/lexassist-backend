from playwright.sync_api import sync_playwright
from app.core.exceptions import WebsiteUnavailableException
from app.core.logger import logger


class HTMLDownloader:
    """
    Downloads fully rendered HTML using Playwright.
    Supports JavaScript-heavy websites such as React, Angular and Vue.
    """

    def __init__(self, timeout: int = 30000):
        self.timeout = timeout

    def download(self, url: str) -> str:
        try:
            logger.info(f"Downloading rendered content from: {url}")

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)

                page = browser.new_page()

                page.goto(
                    url,
                    wait_until="networkidle",
                    timeout=self.timeout
                )

                html = page.content()

                browser.close()

                return html

        except Exception as e:
            logger.error(f"Download failed for URL '{url}': {str(e)}")
            raise WebsiteUnavailableException(
                f"Website '{url}' is unavailable: {str(e)}"
            )