from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from models.assigned_paper import AssignedPaper
from services.assigned_papers_logger import AssignedPapersLogContext, log_assigned_papers_event

ASSIGNED_PAPERS_EMPTY_MESSAGE = "No assigned papers are currently available."
ASSIGNED_PAPERS_RETRIEVAL_ERROR_MESSAGE = "Assigned papers could not be retrieved."
ASSIGNED_PAPERS_UNAUTHENTICATED_MESSAGE = "Please log in to view assigned papers."
ASSIGNED_PAPERS_FORBIDDEN_MESSAGE = "Assigned papers access is restricted to the reviewer."
LOGIN_REDIRECT = "/login"


class AssignedPapersRetrievalError(RuntimeError):
    pass


class AssignedPapersRepository(Protocol):
    def list_assigned(self, reviewer_id: str) -> list[AssignedPaper]:
        ...


@dataclass(frozen=True)
class AssignedPapersResult:
    status: str
    papers: list[AssignedPaper] | None = None
    message: str | None = None
    redirect_to: str | None = None

    @classmethod
    def ok(cls, papers: list[AssignedPaper]) -> "AssignedPapersResult":
        return cls(status="ok", papers=papers)

    @classmethod
    def empty(cls) -> "AssignedPapersResult":
        return cls(status="empty", papers=[], message=ASSIGNED_PAPERS_EMPTY_MESSAGE)

    @classmethod
    def unauthenticated(cls) -> "AssignedPapersResult":
        return cls(
            status="unauthenticated",
            message=ASSIGNED_PAPERS_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def forbidden(cls) -> "AssignedPapersResult":
        return cls(status="forbidden", message=ASSIGNED_PAPERS_FORBIDDEN_MESSAGE)

    @classmethod
    def error(cls) -> "AssignedPapersResult":
        return cls(status="error", message=ASSIGNED_PAPERS_RETRIEVAL_ERROR_MESSAGE)


class AssignedPapersService:
    def __init__(self, repository: AssignedPapersRepository) -> None:
        self._repository = repository

    def list_assigned_papers(
        self,
        reviewer_id: str | None,
        trace_id: Optional[str] = None,
    ) -> AssignedPapersResult:
        context = AssignedPapersLogContext(reviewer_id=reviewer_id, trace_id=trace_id)

        if not reviewer_id:
            log_assigned_papers_event("assigned_papers_unauthenticated", context)
            return AssignedPapersResult.unauthenticated()

        try:
            papers = self._repository.list_assigned(reviewer_id)
        except AssignedPapersRetrievalError:
            log_assigned_papers_event(
                "assigned_papers_retrieval_error",
                context,
                ASSIGNED_PAPERS_RETRIEVAL_ERROR_MESSAGE,
            )
            return AssignedPapersResult.error()
        except Exception:
            log_assigned_papers_event(
                "assigned_papers_retrieval_error",
                context,
                ASSIGNED_PAPERS_RETRIEVAL_ERROR_MESSAGE,
            )
            return AssignedPapersResult.error()

        if not papers:
            log_assigned_papers_event("assigned_papers_empty", context)
            return AssignedPapersResult.empty()

        log_assigned_papers_event("assigned_papers_accessed", context)
        return AssignedPapersResult.ok(papers)
