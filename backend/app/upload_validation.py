from pathlib import Path
from zipfile import BadZipFile, ZipFile
from io import BytesIO

from fastapi import HTTPException, UploadFile, status

from app.config import settings

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


def validate_resume_upload(upload: UploadFile, content: bytes) -> None:
    filename = upload.filename or ""
    suffix = Path(filename).suffix.lower()

    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume file is empty.",
        )

    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Resume file exceeds the {settings.MAX_FILE_SIZE // (1024 * 1024)}MB limit.",
        )

    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported resume file type. Upload a PDF or DOCX file.",
        )

    if upload.content_type not in settings.ALLOWED_RESUME_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported resume MIME type. Upload a PDF or DOCX file.",
        )

    if suffix == ".pdf" and not content.startswith(b"%PDF"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid PDF file.",
        )

    if suffix == ".docx":
        try:
            with ZipFile(BytesIO(content)) as archive:
                if "[Content_Types].xml" not in archive.namelist():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid DOCX file.",
                    )
        except BadZipFile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid DOCX file.",
            )
