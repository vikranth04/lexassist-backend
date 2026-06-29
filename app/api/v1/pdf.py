import os
import uuid
import anyio
from fastapi import APIRouter, UploadFile, File, Depends
from app.core.dependencies import get_pdf_service, get_source_manager
from app.services.pdf_service import PDFService
from app.knowledge.source_manager import SourceManager
from app.schemas.pdf_schema import PDFUploadResponse
from app.core.exceptions import AppBaseException, ValidationException
from app.core.config import settings

router = APIRouter()


async def handle_pdf_upload(file: UploadFile, pdf_service: PDFService, source_manager: SourceManager):
    # Sanitize file name to prevent path traversal attacks
    clean_filename = os.path.basename(file.filename)
    file_ext = os.path.splitext(clean_filename)[1].lower()

    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise ValidationException(
            f"Unsupported file extension '{file_ext}'. Allowed extensions: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    upload_dir = "app/storage/uploads"
    os.makedirs(upload_dir, exist_ok=True)

    # Use UUID to prevent duplicate name collisions
    unique_prefix = uuid.uuid4().hex
    safe_filename = f"{unique_prefix}_{clean_filename}"
    file_path = os.path.join(upload_dir, safe_filename)

    try:
        # Save upload with size limit check on-the-fly inside threadpool
        def save_file_sync():
            size = 0
            max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
            with open(file_path, "wb") as buffer:
                for chunk in iter(lambda: file.file.read(8192), b""):
                    size += len(chunk)
                    if size > max_bytes:
                        raise ValidationException(
                            f"File size exceeds the maximum limit of {settings.MAX_UPLOAD_SIZE_MB} MB."
                        )
                    buffer.write(chunk)

        await anyio.to_thread.run_sync(save_file_sync)

        # Get file size
        file_size = os.path.getsize(file_path)

        # Register PDF source
        source_id = await anyio.to_thread.run_sync(
            source_manager.register_pdf, clean_filename, file_size, file_path
        )

        return {
            "success": True,
            "filename": clean_filename,
            "upload_status": "Success",
            "file_size": file_size,
            "upload_id": source_id
        }
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        if isinstance(e, AppBaseException):
            raise e
        raise AppBaseException(message=str(e), status_code=500)


@router.post(
    "/upload-pdf",
    response_model=PDFUploadResponse,
    summary="Upload PDF (Legacy)",
    description="Upload a PDF file to parse, extract metadata details.",
    deprecated=True
)
async def upload_pdf_legacy(
    file: UploadFile = File(...),
    pdf_service: PDFService = Depends(get_pdf_service),
    source_manager: SourceManager = Depends(get_source_manager)
):
    return await handle_pdf_upload(file, pdf_service, source_manager)


@router.post(
    "/pdf/upload",
    response_model=PDFUploadResponse,
    summary="Upload PDF",
    description="Upload a PDF file to parse, extract metadata details."
)
async def upload_pdf(
    file: UploadFile = File(...),
    pdf_service: PDFService = Depends(get_pdf_service),
    source_manager: SourceManager = Depends(get_source_manager)
):
    return await handle_pdf_upload(file, pdf_service, source_manager)
