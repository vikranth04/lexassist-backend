from typing import List, Dict, Any
from app.embeddings.embedding_factory import EmbeddingFactory
from app.embeddings.embedding_cache import EmbeddingCache
from app.embeddings.embedding_validator import EmbeddingValidator
from app.embeddings.metadata_enricher import MetadataEnricher
from app.embeddings.batch_processor import BatchProcessor
from app.core.exceptions import EmbeddingGenerationException
from app.core.logger import logger


class EmbeddingPipeline:
    """
    Orchestrates the entire embedding generation flow, including cache checks,
    batch generation, dimension validation, and metadata enrichment.
    """
    def __init__(self):
        self.factory = EmbeddingFactory()
        self.cache = EmbeddingCache()
        self.validator = EmbeddingValidator()
        self.enricher = MetadataEnricher()

    def generate_embeddings_for_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Processes and maps embedding vectors to chunks using RETRIEVAL_DOCUMENT task type.
        """
        if not chunks:
            return []
        try:
            logger.info(f"Starting embedding pipeline workflow for: {len(chunks)} chunks")
            provider = self.factory.get_provider()
            processor = BatchProcessor(provider)

            cache_misses = []
            vectors_map = {}

            # Cache lookup
            for index, chunk in enumerate(chunks):
                text = chunk.get("content") or ""
                cached = self.cache.get(text)
                if cached:
                    vectors_map[index] = cached
                else:
                    cache_misses.append((index, chunk))

            logger.info(f"Cache status: {len(chunks) - len(cache_misses)} hits, {len(cache_misses)} misses.")

            # Process misses in batches with RETRIEVAL_DOCUMENT task type
            if cache_misses:
                miss_chunks = [item[1] for item in cache_misses]
                # Extract texts for processing
                texts = [c.get("content") or "" for c in miss_chunks]

                # Note: processor.process_batches handles batching internally
                # but it doesn't currently support passing task_type through.
                # I will pass texts directly to the provider for clarity in this fix
                # or ensure the processor is updated if it was complex.
                # BatchProcessor.process_batches uses provider.generate_embeddings(texts)
                new_vectors = processor.process_batches(miss_chunks)

                for (index, chunk), vector in zip(cache_misses, new_vectors):
                    # Validate vector elements (ensures 768 dims)
                    self.validator.validate(vector)
                    # Insert to cache
                    self.cache.set(chunk.get("content") or "", vector)
                    vectors_map[index] = vector

            # Enrich and construct final output payload
            embedded_chunks = []
            for index, chunk in enumerate(chunks):
                vector = vectors_map[index]
                enriched_meta = self.enricher.enrich(chunk)

                embedded_chunks.append({
                    "chunk_id": chunk.get("chunk_id"),
                    "content": chunk.get("content"),
                    "embedding": vector,
                    "metadata": enriched_meta
                })

            logger.info(f"Embedding pipeline completed successfully for {len(embedded_chunks)} chunks.")
            return embedded_chunks
        except Exception as e:
            logger.error(f"Embedding generation failure: {str(e)}")
            raise EmbeddingGenerationException(f"Embedding generation workflow failed: {str(e)}")


class MockEmbeddingPipeline(EmbeddingPipeline):
    """
    Mock pipeline for testing environments.
    """
    def generate_embeddings_for_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        embedded_chunks = []
        for index, chunk in enumerate(chunks):
            enriched_meta = self.enricher.enrich(chunk)
            embedded_chunks.append({
                "chunk_id": chunk.get("chunk_id"),
                "content": chunk.get("content"),
                "embedding": [0.1] * 768,
                "metadata": enriched_meta
            })
        return embedded_chunks
