from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.assigned_papers import list_assigned_papers
from models.assigned_paper import AssignedPaper
from services.assigned_papers_service import (
    ASSIGNED_PAPERS_EMPTY_MESSAGE,
    ASSIGNED_PAPERS_RETRIEVAL_ERROR_MESSAGE,
    ASSIGNED_PAPERS_UNAUTHENTICATED_MESSAGE,
    LOGIN_REDIRECT,
    AssignedPapersRetrievalError,
    AssignedPapersService,
)


def test_at_uc13_01_view_assigned_papers_list() -> None:
    repository = StubAssignedPapersRepository(
        papers=[AssignedPaper(paper_id="paper-1", title="Deep Learning")]
    )
    service = AssignedPapersService(repository)

    status, response = list_assigned_papers(service, "reviewer-1")

    assert status == 200
    assert response[0]["paperId"] == "paper-1"
    assert response[0]["title"] == "Deep Learning"


def test_at_uc13_02_unauthenticated_redirect() -> None:
    repository = StubAssignedPapersRepository(
        papers=[AssignedPaper(paper_id="paper-1", title="Deep Learning")]
    )
    service = AssignedPapersService(repository)

    status, response = list_assigned_papers(service, None)

    assert status == 401
    assert response["message"] == ASSIGNED_PAPERS_UNAUTHENTICATED_MESSAGE
    assert response["redirect_to"] == LOGIN_REDIRECT


def test_at_uc13_03_no_assigned_papers() -> None:
    repository = StubAssignedPapersRepository(papers=[])
    service = AssignedPapersService(repository)

    status, response = list_assigned_papers(service, "reviewer-1")

    assert status == 200
    assert response["message"] == ASSIGNED_PAPERS_EMPTY_MESSAGE
    assert response["papers"] == []


def test_at_uc13_04_retrieval_error() -> None:
    repository = StubAssignedPapersRepository(papers=[], fail=True)
    service = AssignedPapersService(repository)

    status, response = list_assigned_papers(service, "reviewer-1")

    assert status == 500
    assert response["message"] == ASSIGNED_PAPERS_RETRIEVAL_ERROR_MESSAGE


class StubAssignedPapersRepository:
    def __init__(self, papers: list[AssignedPaper], *, fail: bool = False) -> None:
        self._papers = papers
        self._fail = fail

    def list_assigned(self, reviewer_id: str) -> list[AssignedPaper]:
        if self._fail:
            raise AssignedPapersRetrievalError("retrieval failed")
        return list(self._papers)
