import os
import json
from typing import List, Dict, Any


class EmbeddingRepository:
    """
    Saves and loads generated vector embedding documents in storage/embeddings/ directory.
    """
    def __init__(self, embeddings_dir: str = "app/storage/embeddings"):
        self.embeddings_dir = embeddings_dir
        os.makedirs(self.embeddings_dir, exist_ok=True)

    def save_embeddings(self, document_id: str, embedded_chunks: List[Dict[str, Any]]) -> str:
        """Saves a document's list of embeddings to a JSON file."""
        filename = f"{document_id}_embeddings.json"
        file_path = os.path.join(self.embeddings_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(embedded_chunks, f, indent=2, ensure_ascii=False)

        return file_path

    def get_embeddings(self, document_id: str) -> List[Dict[str, Any]]:
        """Retrieves and returns the list of embeddings for a document ID."""
        filename = f"{document_id}_embeddings.json"
        file_path = os.path.join(self.embeddings_dir, filename)
        if not os.path.exists(file_path):
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
