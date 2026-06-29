from typing import List, Dict, Any
from app.rag.chunking.semantic_splitter import SemanticSplitter
from app.rag.chunking.overlap_manager import OverlapManager
from app.rag.chunking.metadata_builder import MetadataBuilder
from app.rag.chunking.chunk_factory import ChunkFactory
from app.rag.chunking.chunk_validator import ChunkValidator
from app.core.exceptions import ChunkGenerationException
from app.core.logger import logger


class ChunkGenerator:
    """
    Coordinates semantic splitting, contextual overlap matching, and chunk object packaging.
    """
    def __init__(self, chunk_size: int = 600, overlap_size: int = 120):
        self.chunk_size = chunk_size
        self.splitter = SemanticSplitter()
        self.overlap_manager = OverlapManager(overlap_tokens=overlap_size)
        self.meta_builder = MetadataBuilder()
        self.factory = ChunkFactory()
        self.validator = ChunkValidator(min_tokens=10, max_tokens=1200)

    def generate_chunks(self, doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Segments document clean_text and returns list of chunks. Raises ChunkGenerationException."""
        try:
            text = doc.get("clean_text") or ""
            if not text.strip():
                return []

            sentences = self.splitter.split_sentences(text)
            chunks = []
            current_sentences: List[str] = []
            current_tokens = 0
            chunk_index = 0

            for sentence in sentences:
                sentence_tokens = max(1, len(sentence) // 4)

                # If adding sentence exceeds chunk threshold limit, flush chunk
                if current_tokens + sentence_tokens > self.chunk_size and current_sentences:
                    chunk_text = " ".join(current_sentences)
                    parent_doc_id = doc.get("document_id", "unknown")
                    chunk_id = self.factory.generate_chunk_id(parent_doc_id, chunk_index)

                    meta = self.meta_builder.build_metadata(
                        chunk_id, chunk_index, doc, chunk_text, len(chunk_text), current_tokens
                    )
                    stats = {
                        "character_count": len(chunk_text),
                        "token_count": current_tokens
                    }

                    chunk = self.factory.create_chunk(chunk_text, meta, stats)
                    self.validator.validate(chunk)
                    chunks.append(chunk)

                    # Extract trailing overlap text context
                    overlap_text = self.overlap_manager.get_overlap_text(current_sentences)
                    overlap_sentences = self.splitter.split_sentences(overlap_text)

                    current_sentences = overlap_sentences + [sentence]
                    current_tokens = sum(max(1, len(s) // 4) for s in current_sentences)
                    chunk_index += 1
                else:
                    current_sentences.append(sentence)
                    current_tokens += sentence_tokens

            # Process leftover lines
            if current_sentences:
                chunk_text = " ".join(current_sentences)
                parent_doc_id = doc.get("document_id", "unknown")
                chunk_id = self.factory.generate_chunk_id(parent_doc_id, chunk_index)

                meta = self.meta_builder.build_metadata(
                    chunk_id, chunk_index, doc, chunk_text, len(chunk_text), current_tokens
                )
                stats = {
                    "character_count": len(chunk_text),
                    "token_count": current_tokens
                }

                chunk = self.factory.create_chunk(chunk_text, meta, stats)
                self.validator.validate(chunk)
                chunks.append(chunk)

            return chunks
        except Exception as e:
            raise ChunkGenerationException(f"Chunking segmentation sequence failed: {str(e)}")
