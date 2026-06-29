from typing import List, Dict, Any
from app.repositories.file_repository import FileRepository
from app.repositories.vector_repository import VectorRepository


class SourceService:
    """
    Assembles, cleans, and formats citations for retrieved sources and indexed material.
    """
    def __init__(self, file_repo: FileRepository, vector_repo: VectorRepository):
        self.file_repo = file_repo
        self.vector_repo = vector_repo

    def get_formatted_sources(self) -> List[Dict[str, Any]]:
        """Retrieves and formats metadata for all indexed documents/sources."""
        files = self.file_repo.list_files()
        sources = []

        # Extract sources recorded in FileRepository
        for fid, file_meta in files.items():
            sources.append({
                "source_title": file_meta.get("filename") or file_meta.get("url") or "Unknown Source",
                "source_type": file_meta.get("type", "pdf"),
                "website_url": file_meta.get("url"),
                "page_number": 1,
                "chunk_id": fid,
                "confidence_score": 1.0
            })

        # Add any sources indexed in ChromaDB
        try:
            docs = self.vector_repo.get_all_documents()
            metadatas = docs.get("metadatas", []) or []
            ids = docs.get("ids", []) or []
            for idx, meta in enumerate(metadatas):
                if not meta:
                    continue
                source_url = meta.get("source", "")
                sources.append({
                    "source_title": meta.get("title") or source_url.split("/")[-1] or "Unknown Source",
                    "source_type": meta.get("type", "website" if source_url.startswith("http") else "pdf"),
                    "website_url": source_url if source_url.startswith("http") else None,
                    "page_number": meta.get("page_number", 1),
                    "chunk_id": ids[idx] if idx < len(ids) else f"chunk_{idx}",
                    "confidence_score": meta.get("confidence", 1.0)
                })
        except Exception:
            pass

        return sources
