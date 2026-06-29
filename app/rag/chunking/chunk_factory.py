from typing import Dict, Any


class ChunkFactory:
    """
    Standardizes text content, statistical metrics, and metadata attributes into Chunk dictionaries.
    """
    def create_chunk(self, content: str, metadata: Dict[str, Any], statistics: Dict[str, Any]) -> Dict[str, Any]:
        """Creates and returns the standardized chunk representation dict."""
        return {
            "chunk_id": metadata.get("chunk_id"),
            "content": content,
            "statistics": statistics,
            "metadata": metadata
        }
    
    def generate_chunk_id(self, parent_id: str, index: int) -> str:
        """Helper to generate a structured unique chunk ID."""
        return f"CHK_{parent_id}_{index:03d}"
