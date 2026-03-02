from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from models.review_submission import ReviewSubmission
from services.review_submission_logger import (
    ReviewSubmissionLogContext,
    log_review_submission_event,
)
from services.review_submission_validation import (
    INVALID_FIELDS_MESSAGE,
    MISSING_FIELDS_MESSAGE,
    ReviewValidationResult,
    ReviewValidator,
)

REVIEW_SUBMISSION_SUCCESS_TEMPLATE = "Review submitted for paper {paper_id}."
REVIEW_SUBMISSION_UNAUTHENTICATED_MESSAGE = "Please log in to submit the review."
REVIEW_SUBMISSION_FORBIDDEN_MESSAGE = "You are not authorized to submit a review for this paper."
REVIEW_SUBMISSION_DUPLICATE_MESSAGE = "Review already submitted."
REVIEW_SUBMISSION_STORAGE_ERROR_MESSAGE = "Review could not be submitted. Please try again."
LOGIN_REDIRECT = "/login"


class ReviewSubmissionStorageError(RuntimeError):
    pass


class ReviewSubmissionRepository(Protocol):
    def has_submission(self, reviewer_id: str, paper_id: str) -> bool:
        ...

    def save_submission(self, submission: ReviewSubmission) -> None:
        ...


class AssignmentRepository(Protocol):
    def is_assigned(self, reviewer_id: str, paper_id: str) -> bool:
        ...


@dataclass(frozen=True)
class ReviewSubmissionResult:
    status: str
    message: str | None = None
    errors: list[str] | None = None
    redirect_to: str | None = None

    @classmethod
    def success(cls, paper_id: str) -> "ReviewSubmissionResult":
        return cls(
            status="success",
            message=REVIEW_SUBMISSION_SUCCESS_TEMPLATE.format(paper_id=paper_id),
        )

    @classmethod
    def unauthenticated(cls) -> "ReviewSubmissionResult":
        return cls(
            status="unauthenticated",
            message=REVIEW_SUBMISSION_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def forbidden(cls) -> "ReviewSubmissionResult":
        return cls(status="forbidden", message=REVIEW_SUBMISSION_FORBIDDEN_MESSAGE)

    @classmethod
    def validation_missing(cls, fields: list[str]) -> "ReviewSubmissionResult":
        message = MISSING_FIELDS_MESSAGE.format(fields=", ".join(fields))
        return cls(status="missing", message=message, errors=fields)

    @classmethod
    def validation_invalid(cls, fields: list[str]) -> "ReviewSubmissionResult":
        message = INVALID_FIELDS_MESSAGE.format(fields=", ".join(fields))
        return cls(status="invalid", message=message, errors=fields)

    @classmethod
    def duplicate(cls) -> "ReviewSubmissionResult":
        return cls(status="duplicate", message=REVIEW_SUBMISSION_DUPLICATE_MESSAGE)

    @classmethod
    def storage_error(cls) -> "ReviewSubmissionResult":
        return cls(status="error", message=REVIEW_SUBMISSION_STORAGE_ERROR_MESSAGE)


class ReviewSubmissionService:
    def __init__(
        self,
        assignment_repository: AssignmentRepository,
        submission_repository: ReviewSubmissionRepository,
        validator: ReviewValidator | None = None,
    ) -> None:
        self._assignment_repository = assignment_repository
        self._submission_repository = submission_repository
        self._validator = validator or ReviewValidator()

    def submit_review(
        self,
        paper_id: str,
        reviewer_id: str | None,
        field_values: dict | None,
        trace_id: Optional[str] = None,
    ) -> ReviewSubmissionResult:
        context = ReviewSubmissionLogContext(
            paper_id=paper_id,
            reviewer_id=reviewer_id,
            trace_id=trace_id,
        )

        if not reviewer_id:
            log_review_submission_event("review_submission_unauthenticated", context)
            return ReviewSubmissionResult.unauthenticated()

        try:
            is_assigned = self._assignment_repository.is_assigned(reviewer_id, paper_id)
        except Exception:
            log_review_submission_event(
                "review_submission_assignment_error",
                context,
                REVIEW_SUBMISSION_STORAGE_ERROR_MESSAGE,
            )
            return ReviewSubmissionResult.storage_error()

        if not is_assigned:
            log_review_submission_event(
                "review_submission_forbidden",
                context,
                REVIEW_SUBMISSION_FORBIDDEN_MESSAGE,
            )
            return ReviewSubmissionResult.forbidden()

        try:
            if self._submission_repository.has_submission(reviewer_id, paper_id):
                log_review_submission_event(
                    "review_submission_duplicate",
                    context,
                    REVIEW_SUBMISSION_DUPLICATE_MESSAGE,
                )
                return ReviewSubmissionResult.duplicate()
        except Exception:
            log_review_submission_event(
                "review_submission_duplicate_check_failed",
                context,
                REVIEW_SUBMISSION_STORAGE_ERROR_MESSAGE,
            )
            return ReviewSubmissionResult.storage_error()

        validation = self._validator.validate(field_values or {})
        if validation.status == "missing":
            fields = validation.missing_fields or []
            log_review_submission_event(
                "review_submission_missing_fields",
                context,
                MISSING_FIELDS_MESSAGE.format(fields=", ".join(fields)),
            )
            return ReviewSubmissionResult.validation_missing(fields)
        if validation.status == "invalid":
            fields = validation.invalid_fields or []
            log_review_submission_event(
                "review_submission_invalid_fields",
                context,
                INVALID_FIELDS_MESSAGE.format(fields=", ".join(fields)),
            )
            return ReviewSubmissionResult.validation_invalid(fields)
        if validation.status != "ok":
            log_review_submission_event(
                "review_submission_validation_error",
                context,
                REVIEW_SUBMISSION_STORAGE_ERROR_MESSAGE,
            )
            return ReviewSubmissionResult.storage_error()

        try:
            submission = ReviewSubmission(
                paper_id=paper_id,
                reviewer_id=reviewer_id,
                field_values=field_values or {},
            )
            self._submission_repository.save_submission(submission)
        except ReviewSubmissionStorageError:
            log_review_submission_event(
                "review_submission_storage_error",
                context,
                REVIEW_SUBMISSION_STORAGE_ERROR_MESSAGE,
            )
            return ReviewSubmissionResult.storage_error()
        except Exception:
            log_review_submission_event(
                "review_submission_storage_error",
                context,
                REVIEW_SUBMISSION_STORAGE_ERROR_MESSAGE,
            )
            return ReviewSubmissionResult.storage_error()

        log_review_submission_event(
            "review_submission_success",
            context,
            REVIEW_SUBMISSION_SUCCESS_TEMPLATE.format(paper_id=paper_id),
        )
        return ReviewSubmissionResult.success(paper_id)
