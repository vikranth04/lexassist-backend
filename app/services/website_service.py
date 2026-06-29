import time
from typing import List, Dict, Any, Optional
from app.scraper.website_scraper import WebsiteScraper
from app.repositories.file_repository import FileRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.vector_repository import VectorRepository
from app.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from app.rag.chunking.chunking_pipeline import ChunkingPipeline
from app.embeddings.embedding_pipeline import EmbeddingPipeline
from app.core.logger import logger
from app.core.exceptions import AppBaseException


class WebsiteService:
    """
    Orchestrates website crawling, content extraction, preprocessing, chunking,
    embedding, and vector indexing.
    """
    def __init__(
        self,
        file_repo: FileRepository,
        doc_repo: DocumentRepository,
        preprocessing_pipeline: PreprocessingPipeline,
        chunking_pipeline: ChunkingPipeline,
        embedding_pipeline: EmbeddingPipeline,
        vector_repo: VectorRepository
    ):
        self.scraper = WebsiteScraper()
        self.file_repo = file_repo
        self.doc_repo = doc_repo
        self.preprocessing_pipeline = preprocessing_pipeline
        self.chunking_pipeline = chunking_pipeline
        self.embedding_pipeline = embedding_pipeline
        self.vector_repo = vector_repo

    def crawl_and_index_website(self, url: str, source_id: str) -> Dict[str, Any]:
        """
        Runs the full end-to-end website indexing pipeline:
        Scrape -> Preprocess -> Chunk -> Embed -> Vector Index
        """
        start_time = time.time()
        logger.info(f"Starting end-to-end indexing for website: {url} (Source: {source_id})")

        try:
            # 1. Scrape Website
            logger.info(f"Stage 1/5: Website scraping started for {url}")
            raw_documents = self.scraper.scrape(url, source_id)
            logger.info(f"Pages crawled: {len(raw_documents)}")

            if not raw_documents:
                logger.warning(f"Scraper returned 0 pages for URL: {url}")
                return {
                    "success": True,
                    "message": "Crawl completed but no content was found.",
                    "website": url,
                    "pages_crawled": 0,
                    "chunks_created": 0,
                    "vectors_indexed": 0,
                    "processing_time": f"{round(time.time() - start_time, 2)} seconds"
                }

            # 2. Save Raw Documents (Existing functionality)
            for doc in raw_documents:
                self.doc_repo.save_document(doc)

            all_chunks = []

            # 3. Preprocess and Chunk each page
            logger.info(f"Stage 2/5 & 3/5: Preprocessing and Chunking {len(raw_documents)} pages...")
            for raw_doc in raw_documents:
                # Ensure document_id is present for pipeline compatibility
                raw_doc["document_id"] = raw_doc.get("page_id")

                # Preprocess
                normalized_doc = self.preprocessing_pipeline.process(raw_doc)

                # Chunk
                # Note: chunking_pipeline.process expects a document with 'document_id' and 'clean_text' (from preprocessing)
                # But looking at chunking_pipeline.py, it uses ChunkGenerator which might expect 'clean_content'?
                # Let's verify ChunkGenerator.

                # We'll pass the normalized_doc which has 'clean_text'
                page_chunks = self.chunking_pipeline.process(normalized_doc)
                all_chunks.extend(page_chunks)

            if not all_chunks:
                logger.warning(f"No chunks generated from {len(raw_documents)} pages.")
                return {
                    "success": True,
                    "message": "Indexing completed but no text chunks were generated.",
                    "website": url,
                    "pages_crawled": len(raw_documents),
                    "chunks_created": 0,
                    "vectors_indexed": 0,
                    "processing_time": f"{round(time.time() - start_time, 2)} seconds"
                }

            # 4. Generate Embeddings
            logger.info(f"Stage 4/5: Generating embeddings for {len(all_chunks)} chunks...")
            embedded_chunks = self.embedding_pipeline.generate_embeddings_for_chunks(all_chunks)
            logger.info(f"Embeddings generated: {len(embedded_chunks)}")

            # 5. Vector Indexing
            logger.info(f"Stage 5/5: Indexing vectors into ChromaDB...")
            vectors_indexed = self.vector_repo.save_vectors(embedded_chunks)
            logger.info(f"Vectors indexed: {vectors_indexed}")

            # 6. Finalize Metadata
            content_length = sum(len(d.get("clean_content", "")) for d in raw_documents)
            self.file_repo.save_file_metadata(source_id, {
                "id": source_id,
                "url": url,
                "content_length": content_length,
                "type": "website",
                "chunks_count": len(all_chunks),
                "indexed_at": float(time.time())
            })

            end_time = time.time()
            processing_duration = round(end_time - start_time, 2)

            logger.info(f"Website indexing successful: {url}. Processed {len(raw_documents)} pages into {len(all_chunks)} chunks in {processing_duration}s.")

            return {
                "success": True,
                "message": "Website indexed successfully into vector store.",
                "website": url,
                "pages_crawled": len(raw_documents),
                "chunks_created": len(all_chunks),
                "vectors_indexed": vectors_indexed,
                "processing_time": f"{processing_duration} seconds"
            }

        except Exception as e:
            logger.error(f"Website indexing pipeline failed for {url}: {str(e)}")
            if isinstance(e, AppBaseException):
                raise e
            raise AppBaseException(message=f"Website indexing failed: {str(e)}", status_code=500)

    def index_website(self, url: str, source_id: str):
        """Helper to invoke crawler using generated source ID."""
        return self.crawl_and_index_website(url, source_id)
