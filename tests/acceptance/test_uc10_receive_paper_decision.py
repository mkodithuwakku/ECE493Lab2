from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.submissions.decision_controller import get_decision
from models.paper_submission import PaperSubmission
from services.decision_service import (
    DECISION_DATA_UNAVAILABLE_MESSAGE,
    DECISION_NOT_AVAILABLE_MESSAGE,
    DECISION_RETRIEVAL_ERROR_MESSAGE,
    DECISION_UNAUTHENTICATED_MESSAGE,
    LOGIN_REDIRECT,
    DecisionDataUnavailableError,
    DecisionRetrievalError,
    DecisionService,
)


def test_at_uc10_01_view_decision_success() -> None:
    repository = StubDecisionRepository(
        submission=PaperSubmission(
            id="sub-1",
            author_ids=["author-1"],
            decision_status="recorded",
            decision_value="accepted",
        )
    )
    service = DecisionService(repository)

    status, response = get_decision(service, "sub-1", "author-1")

    assert status == 200
    assert response["decisionStatus"] == "recorded"
    assert response["decisionValue"] == "accepted"


def test_at_uc10_02_decision_not_yet_available() -> None:
    repository = StubDecisionRepository(
        submission=PaperSubmission(
            id="sub-1",
            author_ids=["author-1"],
            decision_status="not_recorded",
            decision_value=None,
        )
    )
    service = DecisionService(repository)

    status, response = get_decision(service, "sub-1", "author-1")

    assert status == 200
    assert response["decisionStatus"] == "not_recorded"
    assert response["decisionValue"] is None
    assert response["message"] == DECISION_NOT_AVAILABLE_MESSAGE


def test_at_uc10_03_unauthenticated_redirect() -> None:
    repository = StubDecisionRepository(
        submission=PaperSubmission(
            id="sub-1",
            author_ids=["author-1"],
            decision_status="recorded",
            decision_value="accepted",
        )
    )
    service = DecisionService(repository)

    status, response = get_decision(service, "sub-1", None)

    assert status == 401
    assert response["message"] == DECISION_UNAUTHENTICATED_MESSAGE
    assert response["redirect_to"] == LOGIN_REDIRECT


def test_at_uc10_04_retrieval_error() -> None:
    repository = StubDecisionRepository(fail=True)
    service = DecisionService(repository)

    status, response = get_decision(service, "sub-1", "author-1")

    assert status == 500
    assert response["message"] == DECISION_RETRIEVAL_ERROR_MESSAGE


def test_at_uc10_05_critical_failure_unavailable() -> None:
    repository = StubDecisionRepository(unavailable=True)
    service = DecisionService(repository)

    status, response = get_decision(service, "sub-1", "author-1")

    assert status == 503
    assert response["message"] == DECISION_DATA_UNAVAILABLE_MESSAGE


class StubDecisionRepository:
    def __init__(
        self,
        *,
        submission: PaperSubmission | None = None,
        fail: bool = False,
        unavailable: bool = False,
    ) -> None:
        self._submission = submission
        self._fail = fail
        self._unavailable = unavailable

    def fetch_submission(self, submission_id: str) -> PaperSubmission:
        if self._fail:
            raise DecisionRetrievalError("retrieval failure")
        if self._unavailable:
            raise DecisionDataUnavailableError("data unavailable")
        assert self._submission is not None
        return self._submission
