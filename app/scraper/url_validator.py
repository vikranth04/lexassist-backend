from urllib.parse import urlparse
from app.core.exceptions import URLValidationException


class URLValidator:
    """
    Validates URL syntax, ensures secure protocols, extracts host domains,
    and checks against path blacklists.
    """
    def __init__(self, max_depth: int = 3, blacklist: list[str] = None):
        self.max_depth = max_depth
        self.blacklist = blacklist or ["login", "register", "admin", "search", "logout", "privacy", "terms", "cookie"]

    def validate(self, url: str) -> str:
        """Validates a URL and returns the extracted domain. Raises URLValidationException on errors."""
        try:
            parsed = urlparse(url)
            if not parsed.scheme or parsed.scheme not in ["http", "https"]:
                raise URLValidationException("URL scheme must be HTTP or HTTPS.")
            if not parsed.netloc:
                raise URLValidationException("URL must contain a valid domain name.")

            path_lower = parsed.path.lower()
            for segment in self.blacklist:
                if segment in path_lower:
                    raise URLValidationException(f"URL path segment '{segment}' is blacklisted.")

            return parsed.netloc
        except URLValidationException as e:
            raise e
        except Exception as e:
            raise URLValidationException(f"Malformatted URL syntax: {str(e)}")
