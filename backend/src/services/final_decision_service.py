from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol, Tuple

from models.final_decision import FinalDecision
from models.paper_submission import PaperSubmission
from services.authorization import is_author
from services.final_decision_logger import FinalDecisionLogContext, log_final_decision_event

FINAL_DECISION_SUCCESS_TEMPLATE = "Final decision recorded for paper {paper_id}: {decision}."
FINAL_DECISION_UNAUTHENTICATED_MESSAGE = "Please log in to record a final decision."
FINAL_DECISION_FORBIDDEN_MESSAGE = "You are not authorized to record a final decision."
FINAL_DECISION_INVALID_MESSAGE = "Invalid decision value."
FINAL_DECISION_REVIEW_INCOMPLETE_MESSAGE = "Cannot record final decision until all reviews are submitted."
FINAL_DECISION_STORAGE_ERROR_MESSAGE = "Final decision could not be saved."
FINAL_DECISION_DUPLICATE_MESSAGE = "Final decision already recorded."
FINAL_DECISION_NOTIFICATION_FAILED_MESSAGE = (
    "Decision recorded, but notification delivery failed."
)
FINAL_DECISION_VIEW_UNAUTHENTICATED_MESSAGE = "Please log in to view the decision."
FINAL_DECISION_VIEW_FORBIDDEN_MESSAGE = "You are not authorized to view this decision."
FINAL_DECISION_VIEW_UNAVAILABLE_MESSAGE = "Decision data unavailable at this time."
LOGIN_REDIRECT = "/login"


class FinalDecisionStorageError(RuntimeError):
    pass


class ReviewStatusError(RuntimeError):
    pass


class NotificationDeliveryError(RuntimeError):
    pass


class FinalDecisionRepository(Protocol):
    def has_decision(self, paper_id: str) -> bool:
        ...

    def save_decision(self, decision: FinalDecision) -> None:
        ...

    def get_decision(self, paper_id: str) -> FinalDecision | None:
        ...


class ReviewStatusRepository(Protocol):
    def get_status(self, paper_id: str) -> dict:
        ...


class SubmissionRepository(Protocol):
    def fetch_submission(self, paper_id: str) -> PaperSubmission:
        ...


class NotificationSender(Protocol):
    def send_decision(self, paper_id: str, decision: str) -> None:
        ...


@dataclass(frozen=True)
class FinalDecisionResult:
    status: str
    message: str | None = None
    redirect_to: str | None = None
    warning: str | None = None

    @classmethod
    def success(cls, paper_id: str, decision: str) -> "FinalDecisionResult":
        return cls(
            status="success",
            message=FINAL_DECISION_SUCCESS_TEMPLATE.format(paper_id=paper_id, decision=decision),
        )

    @classmethod
    def notification_failed(cls, paper_id: str, decision: str) -> "FinalDecisionResult":
        return cls(
            status="success",
            message=FINAL_DECISION_SUCCESS_TEMPLATE.format(paper_id=paper_id, decision=decision),
            warning=FINAL_DECISION_NOTIFICATION_FAILED_MESSAGE,
        )

    @classmethod
    def unauthenticated(cls) -> "FinalDecisionResult":
        return cls(
            status="unauthenticated",
            message=FINAL_DECISION_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def forbidden(cls) -> "FinalDecisionResult":
        return cls(status="forbidden", message=FINAL_DECISION_FORBIDDEN_MESSAGE)

    @classmethod
    def invalid(cls) -> "FinalDecisionResult":
        return cls(status="invalid", message=FINAL_DECISION_INVALID_MESSAGE)

    @classmethod
    def incomplete(cls) -> "FinalDecisionResult":
        return cls(status="incomplete", message=FINAL_DECISION_REVIEW_INCOMPLETE_MESSAGE)

    @classmethod
    def storage_error(cls) -> "FinalDecisionResult":
        return cls(status="error", message=FINAL_DECISION_STORAGE_ERROR_MESSAGE)

    @classmethod
    def duplicate(cls) -> "FinalDecisionResult":
        return cls(status="duplicate", message=FINAL_DECISION_DUPLICATE_MESSAGE)


@dataclass(frozen=True)
class DecisionViewResult:
    status: str
    decision_status: str | None = None
    message: str | None = None
    redirect_to: str | None = None

    @classmethod
    def ok(cls, decision_status: str) -> "DecisionViewResult":
        return cls(status="ok", decision_status=decision_status)

    @classmethod
    def unauthenticated(cls) -> "DecisionViewResult":
        return cls(
            status="unauthenticated",
            message=FINAL_DECISION_VIEW_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def forbidden(cls) -> "DecisionViewResult":
        return cls(status="forbidden", message=FINAL_DECISION_VIEW_FORBIDDEN_MESSAGE)

    @classmethod
    def unavailable(cls) -> "DecisionViewResult":
        return cls(status="error", message=FINAL_DECISION_VIEW_UNAVAILABLE_MESSAGE)


class FinalDecisionService:
    def __init__(
        self,
        decision_repository: FinalDecisionRepository,
        review_status_repository: ReviewStatusRepository,
        notification_sender: NotificationSender | None = None,
    ) -> None:
        self._decision_repository = decision_repository
        self._review_status_repository = review_status_repository
        self._notification_sender = notification_sender

    def record_decision(
        self,
        paper_id: str,
        decision_value: str | None,
        editor_id: str | None,
        is_editor: bool,
        trace_id: Optional[str] = None,
    ) -> FinalDecisionResult:
        context = FinalDecisionLogContext(paper_id=paper_id, editor_id=editor_id, trace_id=trace_id)

        if not editor_id:
            log_final_decision_event("final_decision_unauthenticated", context)
            return FinalDecisionResult.unauthenticated()

        if not is_editor:
            log_final_decision_event("final_decision_forbidden", context, FINAL_DECISION_FORBIDDEN_MESSAGE)
            return FinalDecisionResult.forbidden()

        if decision_value not in {"accept", "reject"}:
            log_final_decision_event("final_decision_invalid", context, FINAL_DECISION_INVALID_MESSAGE)
            return FinalDecisionResult.invalid()

        if self._decision_repository.has_decision(paper_id):
            log_final_decision_event("final_decision_duplicate", context, FINAL_DECISION_DUPLICATE_MESSAGE)
            return FinalDecisionResult.duplicate()

        try:
            status = self._review_status_repository.get_status(paper_id)
        except ReviewStatusError:
            log_final_decision_event(
                "final_decision_review_status_error",
                context,
                FINAL_DECISION_STORAGE_ERROR_MESSAGE,
            )
            return FinalDecisionResult.storage_error()
        except Exception:
            log_final_decision_event(
                "final_decision_review_status_error",
                context,
                FINAL_DECISION_STORAGE_ERROR_MESSAGE,
            )
            return FinalDecisionResult.storage_error()

        reviews_received, reviewers_assigned = self._extract_review_counts(status)
        if reviews_received < reviewers_assigned:
            log_final_decision_event(
                "final_decision_incomplete_reviews",
                context,
                FINAL_DECISION_REVIEW_INCOMPLETE_MESSAGE,
            )
            return FinalDecisionResult.incomplete()

        stored_decision = "accepted" if decision_value == "accept" else "rejected"
        try:
            self._decision_repository.save_decision(
                FinalDecision(
                    paper_id=paper_id,
                    decision=stored_decision,
                    editor_id=editor_id,
                )
            )
        except FinalDecisionStorageError:
            log_final_decision_event(
                "final_decision_storage_error",
                context,
                FINAL_DECISION_STORAGE_ERROR_MESSAGE,
            )
            return FinalDecisionResult.storage_error()
        except Exception:
            log_final_decision_event(
                "final_decision_storage_error",
                context,
                FINAL_DECISION_STORAGE_ERROR_MESSAGE,
            )
            return FinalDecisionResult.storage_error()

        if self._notification_sender is not None:
            try:
                self._notification_sender.send_decision(paper_id, stored_decision)
            except NotificationDeliveryError:
                log_final_decision_event(
                    "final_decision_notification_failed",
                    context,
                    FINAL_DECISION_NOTIFICATION_FAILED_MESSAGE,
                )
                return FinalDecisionResult.notification_failed(paper_id, stored_decision)

        log_final_decision_event("final_decision_success", context)
        return FinalDecisionResult.success(paper_id, stored_decision)

    @staticmethod
    def _extract_review_counts(status: object) -> Tuple[int, int]:
        if hasattr(status, "reviews_received") and hasattr(status, "reviewers_assigned"):
            return int(getattr(status, "reviews_received")), int(getattr(status, "reviewers_assigned"))
        if isinstance(status, dict):
            return int(status.get("reviewsReceived", 0)), int(status.get("reviewersAssigned", 0))
        return 0, 0


class FinalDecisionAccessService:
    def __init__(
        self,
        decision_repository: FinalDecisionRepository,
        submission_repository: SubmissionRepository,
    ) -> None:
        self._decision_repository = decision_repository
        self._submission_repository = submission_repository

    def get_decision(
        self,
        paper_id: str,
        author_id: str | None,
        trace_id: Optional[str] = None,
    ) -> DecisionViewResult:
        context = FinalDecisionLogContext(paper_id=paper_id, editor_id=author_id, trace_id=trace_id)

        if not author_id:
            log_final_decision_event("final_decision_view_unauthenticated", context)
            return DecisionViewResult.unauthenticated()

        try:
            submission = self._submission_repository.fetch_submission(paper_id)
        except Exception:
            log_final_decision_event(
                "final_decision_view_unavailable",
                context,
                FINAL_DECISION_VIEW_UNAVAILABLE_MESSAGE,
            )
            return DecisionViewResult.unavailable()

        if not is_author(author_id, submission.author_ids):
            log_final_decision_event(
                "final_decision_view_forbidden",
                context,
                FINAL_DECISION_VIEW_FORBIDDEN_MESSAGE,
            )
            return DecisionViewResult.forbidden()

        try:
            decision = self._decision_repository.get_decision(paper_id)
        except Exception:
            log_final_decision_event(
                "final_decision_view_unavailable",
                context,
                FINAL_DECISION_VIEW_UNAVAILABLE_MESSAGE,
            )
            return DecisionViewResult.unavailable()

        if decision is None:
            return DecisionViewResult.ok("undecided")

        return DecisionViewResult.ok(decision.decision)
