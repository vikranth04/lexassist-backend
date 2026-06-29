class PageFilter:
    """
    Filters crawling candidates to skip non-informational pages (e.g., cookie banners, privacy terms).
    """
    def __init__(self):
        self.ignored_patterns = [
            "/login", "/register", "/privacy", "/terms", "/cookie", "/admin", "/search", "/404"
        ]

    def should_ignore(self, url: str) -> bool:
        """Returns True if the URL contains any ignored path pattern."""
        url_lower = url.lower()
        return any(pattern in url_lower for pattern in self.ignored_patterns)
