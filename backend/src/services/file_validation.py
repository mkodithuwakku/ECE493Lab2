from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

SUPPORTED_EXTENSIONS = {".pdf", ".doc", ".docx", ".tex"}
MAX_UPLOAD_BYTES = 50 * 1024 * 1024


@dataclass(frozen=True)
class FileValidationResult:
    valid: bool
    message: str | None = None


def validate_file(filename: str, size_bytes: int) -> FileValidationResult:
    extension = _extension(filename)
    if extension not in SUPPORTED_EXTENSIONS:
        formats = "PDF, Word, LaTeX"
        return FileValidationResult(
            valid=False,
            message=f"Unsupported file format. Accepted formats: {formats}.",
        )

    if size_bytes > MAX_UPLOAD_BYTES:
        return FileValidationResult(
            valid=False,
            message="File exceeds maximum size of 50 MB.",
        )

    return FileValidationResult(valid=True)


def _extension(filename: str) -> str:
    if "." not in filename:
        return ""
    return "." + filename.rsplit(".", 1)[-1].lower()
