import os
import json
from typing import Dict, Any, Optional


class NormalizedDocumentRepository:
    """
    Saves and retrieves preprocessed/normalized JSON documents in storage/normalized/ directory.
    """
    def __init__(self, normalized_dir: str = "app/storage/normalized"):
        self.normalized_dir = normalized_dir
        os.makedirs(self.normalized_dir, exist_ok=True)

    def save_normalized_document(self, document: Dict[str, Any]) -> str:
        """Saves a normalized document representation to a JSON file."""
        source_id = document.get("source_id", "unknown")
        doc_id = document.get("document_id", "unknown")
        filename = f"{source_id}_{doc_id}_normalized.json"
        file_path = os.path.join(self.normalized_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(document, f, indent=2, ensure_ascii=False)

        return file_path

    def get_normalized_document(self, source_id: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a normalized document by source ID and document ID."""
        filename = f"{source_id}_{doc_id}_normalized.json"
        file_path = os.path.join(self.normalized_dir, filename)
        if not os.path.exists(file_path):
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
