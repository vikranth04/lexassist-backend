import os
import time
from typing import Dict, Any, List
from app.pdf.pdf_parser import PDFParser
from app.repositories.file_repository import FileRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.vector_repository import VectorRepository
from app.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from app.rag.chunking.chunking_pipeline import ChunkingPipeline
from app.embeddings.embedding_pipeline import EmbeddingPipeline
from app.core.logger import logger
from app.core.exceptions import AppBaseException


class PDFService:
    """
    Orchestrates validation, loading, parsing, cleaning, metadata extraction,
    chunking, embedding, and vector indexing for PDFs.
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
        self.parser = PDFParser()
        self.file_repo = file_repo
        self.doc_repo = doc_repo
        self.preprocessing_pipeline = preprocessing_pipeline
        self.chunking_pipeline = chunking_pipeline
        self.embedding_pipeline = embedding_pipeline
        self.vector_repo = vector_repo

    def process_and_index_pdf(self, file_path: str, filename: str, source_id: str) -> Dict[str, Any]:
        """
        Runs the full end-to-end PDF indexing pipeline:
        Parse -> Preprocess -> Chunk -> Embed -> Vector Index
        """
        start_time = time.time()
        logger.info(f"Starting end-to-end indexing for PDF: {filename} (Source: {source_id})")

        try:
            # 1. Parse PDF
            logger.info(f"Stage 1/5: Parsing PDF content...")
            doc_package = self.parser.parse(file_path, source_id)

            # 2. Save Parsed Document (Existing functionality)
            self.doc_repo.save_document(doc_package)

            # 3. Preprocess and Chunk
            logger.info(f"Stage 2/5 & 3/5: Preprocessing and Chunking document...")
            # Preprocessing expects 'clean_content' but parser returns 'pages' with 'clean_text'.
            # PreprocessingPipeline handles this if 'clean_content' is missing but 'pages' is present.
            normalized_doc = self.preprocessing_pipeline.process(doc_package)

            chunks = self.chunking_pipeline.process(normalized_doc)

            if not chunks:
                logger.warning(f"No chunks generated from PDF: {filename}")
                return {
                    "success": True,
                    "filename": filename,
                    "upload_status": "Success (No content extracted)",
                    "file_size": doc_package["metadata"]["file_size"],
                    "upload_id": source_id,
                    "chunks_created": 0,
                    "vectors_indexed": 0
                }

            # 4. Generate Embeddings
            logger.info(f"Stage 4/5: Generating embeddings for {len(chunks)} chunks...")
            embedded_chunks = self.embedding_pipeline.generate_embeddings_for_chunks(chunks)

            # 5. Vector Indexing
            logger.info(f"Stage 5/5: Indexing {len(embedded_chunks)} vectors into ChromaDB...")
            vectors_indexed = self.vector_repo.save_vectors(embedded_chunks)

            # 6. Record file metadata in file registry
            self.file_repo.save_file_metadata(source_id, {
                "id": source_id,
                "filename": filename,
                "path": file_path,
                "file_size": doc_package["metadata"]["file_size"],
                "type": "pdf",
                "chunks_count": len(chunks),
                "indexed_at": float(time.time())
            })

            duration = round(time.time() - start_time, 2)
            logger.info(f"PDF indexing successful: {filename}. Processed into {len(chunks)} chunks in {duration}s.")

            return {
                "success": True,
                "filename": filename,
                "upload_status": "Success",
                "file_size": doc_package["metadata"]["file_size"],
                "upload_id": source_id,
                "chunks_created": len(chunks),
                "vectors_indexed": vectors_indexed,
                "processing_time": f"{duration} seconds"
            }

        except Exception as e:
            logger.error(f"PDF indexing pipeline failed for {filename}: {str(e)}")
            if isinstance(e, AppBaseException):
                raise e
            raise AppBaseException(message=f"PDF indexing failed: {str(e)}", status_code=500)
