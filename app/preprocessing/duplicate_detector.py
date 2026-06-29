from app.core.exceptions import DuplicateContentException


class DuplicateDetector:
    """
    Scans and filters duplicate lines to preserve layout information.
    """
    def remove_duplicates(self, text: str) -> str:
        """Strips repeating lines from the document blocks. Raises DuplicateContentException on error."""
        try:
            lines = text.split("\n")
            seen_lines = set()
            unique_lines = []

            for line in lines:
                trimmed = line.strip()
                if trimmed:
                    # Ignore duplicate paragraphs or legal footer repetitions
                    if trimmed in seen_lines:
                        continue
                    seen_lines.add(trimmed)
                unique_lines.append(line)

            return "\n".join(unique_lines).strip()
        except Exception as e:
            raise DuplicateContentException(f"Duplicate content scanning failed: {str(e)}")
