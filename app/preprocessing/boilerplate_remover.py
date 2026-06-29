from app.core.exceptions import BoilerplateRemovalException


class BoilerplateRemover:
    """
    Strips repetitive boilerplate expressions (copyrights, layout tags) from text lines.
    """
    def __init__(self):
        self.boilerplate_phrases = [
            "all rights reserved", "terms of use", "privacy policy", "cookie policy",
            "cookie settings", "powered by", "designed by", "click here", "subscribe to"
        ]

    def remove(self, text: str) -> str:
        """Removes boilerplate patterns from text blocks. Raises BoilerplateRemovalException on error."""
        try:
            lines = text.split("\n")
            filtered_lines = []

            for line in lines:
                line_lower = line.strip().lower()
                # Remove short lines containing boilerplate keywords
                is_bp = any(phrase in line_lower and len(line) < 80 for phrase in self.boilerplate_phrases)
                if not is_bp:
                    filtered_lines.append(line)

            return "\n".join(filtered_lines).strip()
        except Exception as e:
            raise BoilerplateRemovalException(f"Boilerplate cleanup failure: {str(e)}")
