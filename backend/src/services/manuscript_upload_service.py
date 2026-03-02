from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from services.file_storage_service import FileStorageService, StorageError, UploadInterruptedError
from services.file_validation import FileValidationResult, validate_file
from services.submission_repository import SubmissionRepository
from services.upload_logger import UploadLogContext, log_upload_event

SUCCESS_MESSAGE = "Manuscript uploaded successfully."
UPLOAD_INTERRUPTED_MESSAGE = "Upload was interrupted. Please retry."
STORAGE_FAILURE_MESSAGE = "Unable to store manuscript. Please try again."


@dataclass(frozen=True)
class UploadResult:
    status: str
    message: str


class ManuscriptUploadService:
    def __init__(
        self,
        submission_repository: SubmissionRepository,
        storage_service: FileStorageService,
    ) -> None:
        self._submission_repository = submission_repository
        self._storage_service = storage_service

    def upload(
        self,
        submission_id: str,
        filename: str,
        size_bytes: int,
        trace_id: Optional[str] = None,
    ) -> UploadResult:
        context = UploadLogContext(submission_id=submission_id, trace_id=trace_id)
        validation = validate_file(filename, size_bytes)
        if not validation.valid:
            log_upload_event("upload_validation_failed", context, validation.message)
            return UploadResult(status="validation_failed", message=validation.message or "")

        try:
            file_id = self._storage_service.store_file(submission_id, filename, size_bytes)
            self._submission_repository.associate_manuscript(submission_id, file_id)
        except UploadInterruptedError:
            log_upload_event("upload_interrupted", context, UPLOAD_INTERRUPTED_MESSAGE)
            return UploadResult(status="interrupted", message=UPLOAD_INTERRUPTED_MESSAGE)
        except StorageError:
            log_upload_event("upload_storage_failed", context, STORAGE_FAILURE_MESSAGE)
            return UploadResult(status="storage_failed", message=STORAGE_FAILURE_MESSAGE)

        log_upload_event("upload_success", context, SUCCESS_MESSAGE)
        return UploadResult(status="success", message=SUCCESS_MESSAGE)
