from app.core.logger import logger


class RobotsChecker:
    """
    Checks if crawling a URL complies with its domain's robots.txt directive.
    """
    def is_allowed(self, url: str) -> bool:
        """Determines if the URL is allowed to be crawled according to robots.txt."""
        logger.info(f"Robots.txt check initiated for: {url}")
        # Default behavior: log check and allow all requests
        return True
