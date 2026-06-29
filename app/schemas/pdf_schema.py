from pydantic import BaseModel


class PDFUploadResponse(BaseModel):
    success: bool
    filename: str
    upload_status: str
    file_size: int
    upload_id: str
