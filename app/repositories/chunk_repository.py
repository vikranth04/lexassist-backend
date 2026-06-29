import os
import json
from typing import List, Dict, Any


class ChunkRepository:
    """
    Saves and retrieves chunk files in storage/chunks/ directory.
    """
    def __init__(self, chunks_dir: str = "app/storage/chunks"):
        self.chunks_dir = chunks_dir
        os.makedirs(self.chunks_dir, exist_ok=True)

    def save_chunks(self, document_id: str, chunks: List[Dict[str, Any]]) -> str:
        """Saves a document's list of chunks to a JSON file."""
        filename = f"{document_id}_chunks.json"
        file_path = os.path.join(self.chunks_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)

        return file_path

    def get_chunks(self, document_id: str) -> List[Dict[str, Any]]:
        """Retrieves and returns the list of chunks for a document ID."""
        filename = f"{document_id}_chunks.json"
        file_path = os.path.join(self.chunks_dir, filename)
        if not os.path.exists(file_path):
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
