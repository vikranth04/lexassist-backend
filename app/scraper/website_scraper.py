import uuid
from typing import Dict, Any, List, Set, Tuple
from app.scraper.url_validator import URLValidator
from app.scraper.robots_checker import RobotsChecker
from app.scraper.html_downloader import HTMLDownloader
from app.scraper.html_parser import HTMLParser
from app.scraper.content_extractor import ContentExtractor
from app.scraper.metadata_extractor import MetadataExtractor
from app.scraper.crawler import Crawler
from app.core.logger import logger


class WebsiteScraper:
    """
    Orchestrates the crawling flow: downloads page structures, cleans content blocks,
    calculates page-specific metadata, and structures information for downstream processing.
    """
    def __init__(self, max_depth: int = 2, max_pages: int = 5):
        self.url_validator = URLValidator()
        self.robots_checker = RobotsChecker()
        self.downloader = HTMLDownloader()
        self.parser = HTMLParser()
        self.content_extractor = ContentExtractor()
        self.metadata_extractor = MetadataExtractor()
        self.crawler = Crawler(max_depth=max_depth, max_pages=max_pages)

    def scrape(self, start_url: str, source_id: str) -> List[Dict[str, Any]]:
        """Crawls, extracts, and generates a list of structured document records from a website."""
        logger.info(f"Starting web scrape pipeline for: {start_url} (Source: {source_id})")

        # Validate URL scheme and safety rules
        self.url_validator.validate(start_url)
        self.robots_checker.is_allowed(start_url)

        visited: Set[str] = set()
        queue: List[Tuple[str, int]] = [(start_url, 0)]
        structured_documents: List[Dict[str, Any]] = []

        while queue and len(visited) < self.crawler.max_pages:
            url, depth = queue.pop(0)
            if url in visited:
                continue
            if depth > self.crawler.max_depth:
                continue

            try:
                visited.add(url)
                html = self.downloader.download(url)
                soup = self.parser.parse(html)

                # Clean content blocks and build heading map
                content_data = self.content_extractor.extract(soup)

                # Retrieve header, link, and length metadata
                meta = self.metadata_extractor.extract(soup, url, source_id)
                meta["content_length"] = len(content_data["clean_content"])

                page_id = f"PAGE_{uuid.uuid4().hex[:8].upper()}"

                doc = {
                    "source_id": source_id,
                    "page_id": page_id,
                    "url": url,
                    "title": meta["title"],
                    "metadata": meta,
                    "section_hierarchy": content_data["section_hierarchy"],
                    "clean_content": content_data["clean_content"],
                    "crawl_timestamp": meta["crawl_timestamp"]
                }
                structured_documents.append(doc)

                # Discover link pathways if within depth thresholds
                if depth < self.crawler.max_depth:
                    new_links = self.crawler.discover_links(soup, url)
                    for link in new_links:
                        if link not in visited:
                            queue.append((link, depth + 1))

            except Exception as e:
                logger.error(f"Failed parsing step on node '{url}': {str(e)}")

        logger.info(f"Crawl completed. Total pages ingested: {len(structured_documents)}")
        return structured_documents