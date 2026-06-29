from bs4 import BeautifulSoup
from app.core.exceptions import ContentExtractionException
from typing import Dict, Any


class ContentExtractor:
    """
    Strips noise elements (navs, footers, scripts, ads) and extracts section hierarchies,
    lists, tables, and paragraphs.
    """
    def __init__(self):
        self.noise_tags = [
            "nav", "header", "footer", "sidebar", "aside", "script", "style",
            "noscript", "iframe", "svg", "form", "button", "dialog"
        ]
        self.noise_selectors = [
            ".cookie", ".banner", ".menu", ".nav", ".footer", ".header",
            ".sidebar", ".ad-wrapper", ".advertisement", "#menu", "#nav",
            "#footer", "#header", "#sidebar"
        ]

    def extract(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extracts clean content and section hierarchy. Raises ContentExtractionException on error."""
        try:
            clean_soup = BeautifulSoup(str(soup), "html.parser")

            # Decompose noise tags
            for tag in clean_soup(self.noise_tags):
                tag.decompose()

            # Decompose noise selectors
            for selector in self.noise_selectors:
                for element in clean_soup.select(selector):
                    element.decompose()

            section_hierarchy = []
            clean_text_parts = []

            # Traverse layout nodes
            for element in clean_soup.find_all(["h1", "h2", "h3", "h4", "p", "ul", "ol", "table"]):
                text = element.get_text(strip=True)
                if not text:
                    continue

                tag_name = element.name
                if tag_name.startswith("h"):
                    section_hierarchy.append({"level": tag_name, "text": text})
                    clean_text_parts.append(f"\n{text}\n")
                elif tag_name == "p":
                    clean_text_parts.append(text)
                elif tag_name in ["ul", "ol"]:
                    items = [li.get_text(strip=True) for li in element.find_all("li") if li.get_text(strip=True)]
                    if items:
                        list_text = "\n".join([f"- {item}" for item in items])
                        clean_text_parts.append(list_text)
                elif tag_name == "table":
                    rows = []
                    for tr in element.find_all("tr"):
                        cells = [cell.get_text(strip=True) for cell in tr.find_all(["td", "th"])]
                        if cells:
                            rows.append(" | ".join(cells))
                    if rows:
                        clean_text_parts.append("\n".join(rows))

            clean_content = "\n\n".join(clean_text_parts)
            return {
                "clean_content": clean_content.strip(),
                "section_hierarchy": section_hierarchy
            }
        except Exception as e:
            raise ContentExtractionException(f"Failed to isolate content: {str(e)}")
