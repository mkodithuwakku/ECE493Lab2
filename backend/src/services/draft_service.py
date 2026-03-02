from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from models.submission_draft import SubmissionDraft
from services.draft_logger import DraftLogContext, log_draft_event
from services.draft_repository import DraftRepository
from services.draft_validation import (
    DraftValidationError,
    DraftValidator,
    INVALID_DATA_PREFIX,
    MISSING_MINIMUM_MESSAGE,
)

SUCCESS_MESSAGE = "Draft saved successfully."
INCOMPLETE_MESSAGE = "Draft saved with incomplete information."
VALIDATION_FAILURE_MESSAGE = "Draft validation failed. Please retry."
STORAGE_FAILURE_MESSAGE = "Unable to save draft. Please try again."


class DraftStorageError(RuntimeError):
    pass


@dataclass(frozen=True)
class DraftSaveResult:
    status: str
    message: str
    draft_status: str | None = None


class DraftValidatorProtocol(Protocol):
    def validate(self, payload: dict) -> "DraftValidationResult":
        ...


class DraftValidationResult(Protocol):
    status: str
    message: str | None
    data: dict | None
    complete: bool


class DraftService:
    def __init__(
        self,
        draft_repository: DraftRepository,
        validator: DraftValidatorProtocol | None = None,
    ) -> None:
        self._draft_repository = draft_repository
        self._validator = validator or DraftValidator()

    def save_draft(
        self,
        submission_id: str,
        payload: dict,
        save_anyway: bool = False,
        trace_id: Optional[str] = None,
    ) -> DraftSaveResult:
        context = DraftLogContext(submission_id=submission_id, trace_id=trace_id)

        try:
            validation = self._validator.validate(payload)
        except DraftValidationError:
            log_draft_event("draft_validation_error", context, VALIDATION_FAILURE_MESSAGE)
            return DraftSaveResult(status="validation_error", message=VALIDATION_FAILURE_MESSAGE)

        if validation.status == "invalid":
            message = validation.message or (INVALID_DATA_PREFIX + "invalid submission data")
            log_draft_event("draft_invalid", context, message)
            return DraftSaveResult(status="invalid", message=message)

        if validation.status == "missing_minimum" and not save_anyway:
            message = validation.message or MISSING_MINIMUM_MESSAGE
            log_draft_event("draft_missing_minimum", context, message)
            return DraftSaveResult(status="missing_minimum", message=message)

        if validation.data is None:
            log_draft_event("draft_validation_error", context, VALIDATION_FAILURE_MESSAGE)
            return DraftSaveResult(status="validation_error", message=VALIDATION_FAILURE_MESSAGE)

        complete = validation.complete and validation.status != "missing_minimum"

        try:
            draft = SubmissionDraft(data=validation.data, complete=complete)
            self._draft_repository.save_draft(submission_id, draft)
        except DraftStorageError:
            log_draft_event("draft_storage_failed", context, STORAGE_FAILURE_MESSAGE)
            return DraftSaveResult(status="storage_error", message=STORAGE_FAILURE_MESSAGE)

        if complete:
            message = SUCCESS_MESSAGE
            status = "success"
            draft_status = "complete"
        else:
            message = INCOMPLETE_MESSAGE
            status = "success"
            draft_status = "incomplete"

        log_draft_event("draft_saved", context, message)
        return DraftSaveResult(status=status, message=message, draft_status=draft_status)
