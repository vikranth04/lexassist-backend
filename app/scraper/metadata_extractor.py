import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from app.core.exceptions import MetadataExtractionException
from typing import Dict, Any


class MetadataExtractor:
    """
    Extracts page metadata (title, description, language, links counter) from page layouts.
    """
    def extract(self, soup: BeautifulSoup, url: str, source_id: str) -> Dict[str, Any]:
        """Extracts and returns metadata dictionary. Raises MetadataExtractionException on error."""
        try:
            domain = urlparse(url).netloc
            title_node = soup.find("title")
            title = title_node.get_text(strip=True) if title_node else "Untitled Page"

            desc_node = soup.find("meta", attrs={"name": "description"})
            description = desc_node.get("content", "").strip() if desc_node else ""

            html_node = soup.find("html")
            language = html_node.get("lang", "en").strip() if html_node else "en"

            # Filter unique internal links to calculate link metric
            all_links = soup.find_all("a", href=True)
            internal_links = [
                a.get("href") for a in all_links
                if a.get("href").startswith("/") or domain in a.get("href")
            ]

            return {
                "source_id": source_id,
                "page_url": url,
                "domain": domain,
                "title": title,
                "description": description,
                "language": language,
                "crawl_timestamp": float(time.time()),
                "content_length": 0,  # Set by caller
                "internal_link_count": len(internal_links)
            }
        except Exception as e:
            raise MetadataExtractionException(f"Metadata extraction error: {str(e)}")
