import os
import json
from typing import Dict, Any, Optional


class DocumentRepository:
    """
    Saves and retrieves structured document JSON files in storage/processed directory.
    """
    def __init__(self, processed_dir: str = "app/storage/processed"):
        self.processed_dir = processed_dir
        os.makedirs(self.processed_dir, exist_ok=True)

    def save_document(self, document: Dict[str, Any]) -> str:
        """Saves a structured document as a JSON file and returns the file path."""
        source_id = document.get("source_id", "unknown")
        doc_id = document.get("document_id", "unknown")
        filename = f"{source_id}_{doc_id}.json"
        file_path = os.path.join(self.processed_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(document, f, indent=2, ensure_ascii=False)

        return file_path

    def get_document(self, source_id: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Loads and returns a structured document by source ID and document ID."""
        filename = f"{source_id}_{doc_id}.json"
        file_path = os.path.join(self.processed_dir, filename)
        if not os.path.exists(file_path):
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
