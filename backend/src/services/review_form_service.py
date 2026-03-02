from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from models.review_form import ReviewForm
from services.review_form_logger import ReviewFormLogContext, log_review_form_event

REVIEW_FORM_UNAUTHENTICATED_MESSAGE = "Please log in to access the review form."
REVIEW_FORM_FORBIDDEN_MESSAGE = "You are not authorized to access this review form."
MANUSCRIPT_UNAVAILABLE_MESSAGE = (
    "Manuscript is unavailable. Please try again later or contact support."
)
REVIEW_FORM_RETRIEVAL_ERROR_MESSAGE = "Review form could not be loaded. Please try again later."
LOGIN_REDIRECT = "/login"


class ReviewFormRetrievalError(RuntimeError):
    pass


class ManuscriptRetrievalError(RuntimeError):
    pass


class AssignmentRepository(Protocol):
    def is_assigned(self, reviewer_id: str, paper_id: str) -> bool:
        ...


class ReviewFormRepository(Protocol):
    def fetch_review_form(self, paper_id: str) -> ReviewForm:
        ...


class ManuscriptRepository(Protocol):
    def has_manuscript(self, paper_id: str) -> bool:
        ...


@dataclass(frozen=True)
class ReviewFormResult:
    status: str
    form: ReviewForm | None = None
    message: str | None = None
    redirect_to: str | None = None

    @classmethod
    def ok(cls, form: ReviewForm) -> "ReviewFormResult":
        return cls(status="ok", form=form)

    @classmethod
    def unauthenticated(cls) -> "ReviewFormResult":
        return cls(
            status="unauthenticated",
            message=REVIEW_FORM_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def forbidden(cls) -> "ReviewFormResult":
        return cls(status="forbidden", message=REVIEW_FORM_FORBIDDEN_MESSAGE)

    @classmethod
    def manuscript_unavailable(cls) -> "ReviewFormResult":
        return cls(status="manuscript_unavailable", message=MANUSCRIPT_UNAVAILABLE_MESSAGE)

    @classmethod
    def error(cls) -> "ReviewFormResult":
        return cls(status="error", message=REVIEW_FORM_RETRIEVAL_ERROR_MESSAGE)


class ReviewFormService:
    def __init__(
        self,
        assignment_repository: AssignmentRepository,
        form_repository: ReviewFormRepository,
        manuscript_repository: ManuscriptRepository,
    ) -> None:
        self._assignment_repository = assignment_repository
        self._form_repository = form_repository
        self._manuscript_repository = manuscript_repository

    def get_review_form(
        self,
        paper_id: str,
        reviewer_id: str | None,
        trace_id: Optional[str] = None,
    ) -> ReviewFormResult:
        context = ReviewFormLogContext(paper_id=paper_id, reviewer_id=reviewer_id, trace_id=trace_id)

        if not reviewer_id:
            log_review_form_event("review_form_unauthenticated", context)
            return ReviewFormResult.unauthenticated()

        try:
            is_assigned = self._assignment_repository.is_assigned(reviewer_id, paper_id)
        except Exception:
            log_review_form_event(
                "review_form_assignment_error",
                context,
                REVIEW_FORM_RETRIEVAL_ERROR_MESSAGE,
            )
            return ReviewFormResult.error()

        if not is_assigned:
            log_review_form_event("review_form_forbidden", context, REVIEW_FORM_FORBIDDEN_MESSAGE)
            return ReviewFormResult.forbidden()

        try:
            has_manuscript = self._manuscript_repository.has_manuscript(paper_id)
        except ManuscriptRetrievalError:
            log_review_form_event(
                "review_form_manuscript_unavailable",
                context,
                MANUSCRIPT_UNAVAILABLE_MESSAGE,
            )
            return ReviewFormResult.manuscript_unavailable()
        except Exception:
            log_review_form_event(
                "review_form_manuscript_unavailable",
                context,
                MANUSCRIPT_UNAVAILABLE_MESSAGE,
            )
            return ReviewFormResult.manuscript_unavailable()

        if not has_manuscript:
            log_review_form_event(
                "review_form_manuscript_unavailable",
                context,
                MANUSCRIPT_UNAVAILABLE_MESSAGE,
            )
            return ReviewFormResult.manuscript_unavailable()

        try:
            form = self._form_repository.fetch_review_form(paper_id)
        except ReviewFormRetrievalError:
            log_review_form_event(
                "review_form_retrieval_error",
                context,
                REVIEW_FORM_RETRIEVAL_ERROR_MESSAGE,
            )
            return ReviewFormResult.error()
        except Exception:
            log_review_form_event(
                "review_form_retrieval_error",
                context,
                REVIEW_FORM_RETRIEVAL_ERROR_MESSAGE,
            )
            return ReviewFormResult.error()

        log_review_form_event("review_form_accessed", context)
        return ReviewFormResult.ok(form)
