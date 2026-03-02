from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from models.conference_schedule import ConferenceSchedule
from models.paper_submission import PaperSubmission
from models.schedule_entry import ScheduleEntry
from services.authorization import is_author
from services.schedule_logger import ScheduleLogContext, log_schedule_event

SCHEDULE_NOT_PUBLISHED_MESSAGE = "Conference schedule is not yet published."
SCHEDULE_RETRIEVAL_ERROR_MESSAGE = "Conference schedule is temporarily unavailable."
SCHEDULE_FORBIDDEN_MESSAGE = "Schedule access is restricted to the submission author."
SCHEDULE_UNAUTHENTICATED_MESSAGE = "Please log in to view the conference schedule."
SCHEDULE_MISSING_ENTRY_WARNING = "Your accepted paper is not yet scheduled."
LOGIN_REDIRECT = "/login"


class ScheduleRetrievalError(RuntimeError):
    pass


class SubmissionRetrievalError(RuntimeError):
    pass


class ScheduleRepository(Protocol):
    def fetch_schedule(self) -> ConferenceSchedule:
        ...


class SubmissionLookupRepository(Protocol):
    def fetch_submission(self, submission_id: str) -> PaperSubmission:
        ...


@dataclass(frozen=True)
class ScheduleResult:
    status: str
    schedule_status: str | None = None
    entries: list[ScheduleEntry] | None = None
    message: str | None = None
    warning: str | None = None
    redirect_to: str | None = None

    @classmethod
    def published(
        cls,
        schedule: ConferenceSchedule,
        warning: str | None = None,
    ) -> "ScheduleResult":
        return cls(
            status="published",
            schedule_status="published",
            entries=schedule.entries,
            warning=warning,
        )

    @classmethod
    def unpublished(cls) -> "ScheduleResult":
        return cls(
            status="unpublished",
            schedule_status="unpublished",
            entries=[],
            message=SCHEDULE_NOT_PUBLISHED_MESSAGE,
        )

    @classmethod
    def unauthenticated(cls) -> "ScheduleResult":
        return cls(
            status="unauthenticated",
            message=SCHEDULE_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def forbidden(cls) -> "ScheduleResult":
        return cls(status="forbidden", message=SCHEDULE_FORBIDDEN_MESSAGE)

    @classmethod
    def retrieval_error(cls) -> "ScheduleResult":
        return cls(status="error", message=SCHEDULE_RETRIEVAL_ERROR_MESSAGE)


class ScheduleService:
    def __init__(
        self,
        schedule_repository: ScheduleRepository,
        submission_repository: SubmissionLookupRepository,
    ) -> None:
        self._schedule_repository = schedule_repository
        self._submission_repository = submission_repository

    def get_schedule(
        self,
        submission_id: str,
        user_id: str | None,
        trace_id: Optional[str] = None,
    ) -> ScheduleResult:
        context = ScheduleLogContext(user_id=user_id, trace_id=trace_id)

        if not user_id:
            log_schedule_event("schedule_unauthenticated", context)
            return ScheduleResult.unauthenticated()

        try:
            submission = self._submission_repository.fetch_submission(submission_id)
        except SubmissionRetrievalError:
            log_schedule_event(
                "schedule_submission_error",
                context,
                SCHEDULE_RETRIEVAL_ERROR_MESSAGE,
            )
            return ScheduleResult.retrieval_error()
        except Exception:
            log_schedule_event(
                "schedule_submission_error",
                context,
                SCHEDULE_RETRIEVAL_ERROR_MESSAGE,
            )
            return ScheduleResult.retrieval_error()

        if not is_author(user_id, submission.author_ids):
            log_schedule_event("schedule_access_denied", context, SCHEDULE_FORBIDDEN_MESSAGE)
            return ScheduleResult.forbidden()

        try:
            schedule = self._schedule_repository.fetch_schedule()
        except ScheduleRetrievalError:
            log_schedule_event("schedule_retrieval_error", context, SCHEDULE_RETRIEVAL_ERROR_MESSAGE)
            return ScheduleResult.retrieval_error()
        except Exception:
            log_schedule_event("schedule_retrieval_error", context, SCHEDULE_RETRIEVAL_ERROR_MESSAGE)
            return ScheduleResult.retrieval_error()

        if schedule.status == "unpublished":
            log_schedule_event("schedule_unpublished", context, SCHEDULE_NOT_PUBLISHED_MESSAGE)
            return ScheduleResult.unpublished()

        warning = None
        if not self._has_entry(schedule.entries, submission_id):
            warning = SCHEDULE_MISSING_ENTRY_WARNING
            log_schedule_event("schedule_missing_entry", context, warning)
        else:
            log_schedule_event("schedule_accessed", context)

        return ScheduleResult.published(schedule, warning=warning)

    @staticmethod
    def _has_entry(entries: list[ScheduleEntry], submission_id: str) -> bool:
        return any(entry.submission_id == submission_id for entry in entries)
