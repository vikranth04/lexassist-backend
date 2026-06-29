from bs4 import BeautifulSoup
from app.core.exceptions import HTMLParsingException


class HTMLParser:
    """
    Parses HTML strings into BeautifulSoup document structures.
    """
    def parse(self, html: str) -> BeautifulSoup:
        """Parses HTML and returns a BeautifulSoup object. Raises HTMLParsingException on failures."""
        try:
            return BeautifulSoup(html, "html.parser")
        except Exception as e:
            raise HTMLParsingException(f"Failed to parse HTML string content: {str(e)}")
