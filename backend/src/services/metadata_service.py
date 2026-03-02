from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from models.paper_metadata import PaperMetadata
from services.metadata_logger import MetadataLogContext, log_metadata_event
from services.metadata_repository import MetadataRepository
from services.metadata_validation import (
    INVALID_METADATA_PREFIX,
    MISSING_FIELDS_MESSAGE,
    MetadataValidationError,
    MetadataValidator,
)
from services.submission_repository import SubmissionRepository

SUCCESS_MESSAGE = "Metadata saved successfully."
VALIDATION_FAILURE_MESSAGE = "Metadata validation failed. Please retry."
STORAGE_FAILURE_MESSAGE = "Unable to save metadata. Please try again."
LOCKED_MESSAGE = "Metadata cannot be updated after final submission."


class MetadataStorageError(RuntimeError):
    pass


@dataclass(frozen=True)
class MetadataSaveResult:
    status: str
    message: str


class MetadataValidatorProtocol(Protocol):
    def validate(self, payload: dict) -> "MetadataValidationResult":
        ...


class MetadataValidationResult(Protocol):
    status: str
    message: str | None
    metadata: PaperMetadata | None


class MetadataService:
    def __init__(
        self,
        submission_repository: SubmissionRepository,
        metadata_repository: MetadataRepository,
        validator: MetadataValidatorProtocol | None = None,
    ) -> None:
        self._submission_repository = submission_repository
        self._metadata_repository = metadata_repository
        self._validator = validator or MetadataValidator()

    def save_metadata(
        self,
        submission_id: str,
        payload: dict,
        trace_id: Optional[str] = None,
    ) -> MetadataSaveResult:
        context = MetadataLogContext(submission_id=submission_id, trace_id=trace_id)

        if self._submission_repository.is_finalized(submission_id):
            log_metadata_event("metadata_locked", context, LOCKED_MESSAGE)
            return MetadataSaveResult(status="locked", message=LOCKED_MESSAGE)

        try:
            validation = self._validator.validate(payload)
        except MetadataValidationError:
            log_metadata_event("metadata_validation_error", context, VALIDATION_FAILURE_MESSAGE)
            return MetadataSaveResult(status="validation_error", message=VALIDATION_FAILURE_MESSAGE)

        if validation.status == "missing_fields":
            message = validation.message or MISSING_FIELDS_MESSAGE
            log_metadata_event("metadata_missing_fields", context, message)
            return MetadataSaveResult(status="missing_fields", message=message)

        if validation.status == "invalid_fields":
            message = validation.message or (INVALID_METADATA_PREFIX + "invalid fields")
            log_metadata_event("metadata_invalid_fields", context, message)
            return MetadataSaveResult(status="invalid_fields", message=message)

        if validation.metadata is None:
            log_metadata_event("metadata_validation_error", context, VALIDATION_FAILURE_MESSAGE)
            return MetadataSaveResult(status="validation_error", message=VALIDATION_FAILURE_MESSAGE)

        try:
            self._metadata_repository.save_metadata(submission_id, validation.metadata)
        except MetadataStorageError:
            log_metadata_event("metadata_storage_failed", context, STORAGE_FAILURE_MESSAGE)
            return MetadataSaveResult(status="storage_error", message=STORAGE_FAILURE_MESSAGE)

        log_metadata_event("metadata_saved", context, SUCCESS_MESSAGE)
        return MetadataSaveResult(status="success", message=SUCCESS_MESSAGE)
