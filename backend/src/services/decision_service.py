from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from models.paper_submission import PaperSubmission
from services.authorization import is_author
from services.decision_logger import DecisionLogContext, log_decision_event

DECISION_NOT_AVAILABLE_MESSAGE = "Decision is not yet available."
DECISION_RETRIEVAL_ERROR_MESSAGE = "Decision could not be retrieved. Please try again."
DECISION_DATA_UNAVAILABLE_MESSAGE = "Decision data is unavailable at this time."
DECISION_FORBIDDEN_MESSAGE = "Decision access is restricted to the submission author."
DECISION_UNAUTHENTICATED_MESSAGE = "Please log in to view the decision."
LOGIN_REDIRECT = "/login"


class DecisionRetrievalError(RuntimeError):
    pass


class DecisionDataUnavailableError(RuntimeError):
    pass


class DecisionRepository(Protocol):
    def fetch_submission(self, submission_id: str) -> PaperSubmission:
        ...


@dataclass(frozen=True)
class DecisionResult:
    status: str
    decision_status: str | None = None
    decision_value: str | None = None
    message: str | None = None
    redirect_to: str | None = None

    @classmethod
    def recorded(cls, decision_value: str) -> "DecisionResult":
        return cls(status="recorded", decision_status="recorded", decision_value=decision_value)

    @classmethod
    def not_recorded(cls) -> "DecisionResult":
        return cls(
            status="not_recorded",
            decision_status="not_recorded",
            decision_value=None,
            message=DECISION_NOT_AVAILABLE_MESSAGE,
        )

    @classmethod
    def forbidden(cls) -> "DecisionResult":
        return cls(status="forbidden", message=DECISION_FORBIDDEN_MESSAGE)

    @classmethod
    def unauthenticated(cls) -> "DecisionResult":
        return cls(
            status="unauthenticated",
            message=DECISION_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def retrieval_error(cls) -> "DecisionResult":
        return cls(status="error", message=DECISION_RETRIEVAL_ERROR_MESSAGE)

    @classmethod
    def unavailable(cls) -> "DecisionResult":
        return cls(status="unavailable", message=DECISION_DATA_UNAVAILABLE_MESSAGE)


class DecisionService:
    def __init__(self, repository: DecisionRepository) -> None:
        self._repository = repository

    def get_decision(
        self,
        submission_id: str,
        user_id: str | None,
        trace_id: Optional[str] = None,
    ) -> DecisionResult:
        context = DecisionLogContext(
            submission_id=submission_id,
            user_id=user_id,
            trace_id=trace_id,
        )

        if not user_id:
            log_decision_event("decision_unauthenticated", context)
            return DecisionResult.unauthenticated()

        try:
            submission = self._repository.fetch_submission(submission_id)
        except DecisionRetrievalError:
            log_decision_event("decision_retrieval_error", context, DECISION_RETRIEVAL_ERROR_MESSAGE)
            return DecisionResult.retrieval_error()
        except DecisionDataUnavailableError:
            log_decision_event("decision_data_unavailable", context, DECISION_DATA_UNAVAILABLE_MESSAGE)
            return DecisionResult.unavailable()
        except Exception:
            log_decision_event("decision_data_unavailable", context, DECISION_DATA_UNAVAILABLE_MESSAGE)
            return DecisionResult.unavailable()

        if not is_author(user_id, submission.author_ids):
            log_decision_event("decision_access_denied", context, DECISION_FORBIDDEN_MESSAGE)
            return DecisionResult.forbidden()

        if submission.decision_status == "recorded" and submission.decision_value:
            log_decision_event("decision_accessed", context)
            return DecisionResult.recorded(submission.decision_value)

        log_decision_event("decision_not_recorded", context)
        return DecisionResult.not_recorded()
