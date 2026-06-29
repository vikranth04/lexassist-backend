from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from app.scraper.page_filter import PageFilter
from app.scraper.url_validator import URLValidator
from app.core.logger import logger
from typing import List


class Crawler:
    """
    Crawls internal domains to discover link pathways within the same host.
    """
    def __init__(self, max_depth: int = 3, max_pages: int = 15):
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.page_filter = PageFilter()
        self.url_validator = URLValidator()

    def discover_links(self, soup: BeautifulSoup, current_url: str) -> List[str]:
        """Scans page anchor tags to locate links within the same domain."""
        links = []
        domain = urlparse(current_url).netloc

        for tag in soup.find_all("a", href=True):
            href = tag.get("href")
            # Convert to absolute URL
            absolute_url = urljoin(current_url, href)
            parsed_abs = urlparse(absolute_url)

            # Restrict crawling to original netloc host
            if parsed_abs.netloc == domain:
                if not self.page_filter.should_ignore(absolute_url):
                    try:
                        self.url_validator.validate(absolute_url)
                        links.append(absolute_url)
                    except Exception:
                        pass

        # Return unique candidate paths
        return list(set(links))
