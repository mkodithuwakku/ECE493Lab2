from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from services.final_decision_logger import FinalDecisionLogContext, log_final_decision_event

REVIEW_REQUEST_SUCCESS_MESSAGE = "Additional reviews requested."
REVIEW_REQUEST_UNAUTHENTICATED_MESSAGE = "Please log in to request additional reviews."
REVIEW_REQUEST_FORBIDDEN_MESSAGE = "You are not authorized to request additional reviews."
REVIEW_REQUEST_INVALID_MESSAGE = "Invalid review request."
REVIEW_REQUEST_STORAGE_ERROR_MESSAGE = "Review request could not be recorded."
LOGIN_REDIRECT = "/login"


class ReviewRequestStorageError(RuntimeError):
    pass


class ReviewRequestRepository(Protocol):
    def record_request(self, paper_id: str, reviewer_ids: list[str]) -> None:
        ...


@dataclass(frozen=True)
class ReviewRequestResult:
    status: str
    message: str | None = None
    redirect_to: str | None = None

    @classmethod
    def success(cls) -> "ReviewRequestResult":
        return cls(status="success", message=REVIEW_REQUEST_SUCCESS_MESSAGE)

    @classmethod
    def unauthenticated(cls) -> "ReviewRequestResult":
        return cls(
            status="unauthenticated",
            message=REVIEW_REQUEST_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def forbidden(cls) -> "ReviewRequestResult":
        return cls(status="forbidden", message=REVIEW_REQUEST_FORBIDDEN_MESSAGE)

    @classmethod
    def invalid(cls) -> "ReviewRequestResult":
        return cls(status="invalid", message=REVIEW_REQUEST_INVALID_MESSAGE)

    @classmethod
    def storage_error(cls) -> "ReviewRequestResult":
        return cls(status="error", message=REVIEW_REQUEST_STORAGE_ERROR_MESSAGE)


class AdditionalReviewRequestService:
    def __init__(self, repository: ReviewRequestRepository) -> None:
        self._repository = repository

    def request_reviews(
        self,
        paper_id: str,
        reviewer_ids: list[str] | None,
        editor_id: str | None,
        is_editor: bool,
        trace_id: Optional[str] = None,
    ) -> ReviewRequestResult:
        context = FinalDecisionLogContext(paper_id=paper_id, editor_id=editor_id, trace_id=trace_id)

        if not editor_id:
            log_final_decision_event("review_request_unauthenticated", context)
            return ReviewRequestResult.unauthenticated()

        if not is_editor:
            log_final_decision_event("review_request_forbidden", context, REVIEW_REQUEST_FORBIDDEN_MESSAGE)
            return ReviewRequestResult.forbidden()

        reviewer_ids = reviewer_ids or []
        if not reviewer_ids:
            log_final_decision_event("review_request_invalid", context, REVIEW_REQUEST_INVALID_MESSAGE)
            return ReviewRequestResult.invalid()

        try:
            self._repository.record_request(paper_id, reviewer_ids)
        except ReviewRequestStorageError:
            log_final_decision_event(
                "review_request_storage_error",
                context,
                REVIEW_REQUEST_STORAGE_ERROR_MESSAGE,
            )
            return ReviewRequestResult.storage_error()
        except Exception:
            log_final_decision_event(
                "review_request_storage_error",
                context,
                REVIEW_REQUEST_STORAGE_ERROR_MESSAGE,
            )
            return ReviewRequestResult.storage_error()

        log_final_decision_event("review_request_success", context)
        return ReviewRequestResult.success()
