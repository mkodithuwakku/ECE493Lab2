from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.review_form_access import get_review_form
from models.review_form import ReviewForm
from services.review_form_service import (
    MANUSCRIPT_UNAVAILABLE_MESSAGE,
    REVIEW_FORM_FORBIDDEN_MESSAGE,
    REVIEW_FORM_RETRIEVAL_ERROR_MESSAGE,
    REVIEW_FORM_UNAUTHENTICATED_MESSAGE,
    LOGIN_REDIRECT,
    ManuscriptRetrievalError,
    ReviewFormRetrievalError,
    ReviewFormService,
)


def test_at_uc14_01_access_review_form_success() -> None:
    service = build_service(
        assigned=True,
        manuscript_available=True,
        form=ReviewForm(
            paper_id="paper-1",
            title="Neural Systems",
            form_fields=[{"id": "q1", "label": "Score"}],
            manuscript_link="/papers/paper-1/manuscript",
        ),
    )

    status, response = get_review_form(service, "paper-1", "reviewer-1")

    assert status == 200
    assert response["paperId"] == "paper-1"
    assert response["title"] == "Neural Systems"
    assert response["formFields"][0]["id"] == "q1"
    assert response["manuscriptLink"] == "/papers/paper-1/manuscript"


def test_at_uc14_02_unauthenticated_redirect() -> None:
    service = build_service(
        assigned=True,
        manuscript_available=True,
        form=ReviewForm(
            paper_id="paper-1",
            title="Neural Systems",
            form_fields=[],
        ),
    )

    status, response = get_review_form(service, "paper-1", None)

    assert status == 401
    assert response["message"] == REVIEW_FORM_UNAUTHENTICATED_MESSAGE
    assert response["redirect_to"] == LOGIN_REDIRECT


def test_at_uc14_03_unassigned_paper_forbidden() -> None:
    service = build_service(
        assigned=False,
        manuscript_available=True,
        form=ReviewForm(
            paper_id="paper-1",
            title="Neural Systems",
            form_fields=[],
        ),
    )

    status, response = get_review_form(service, "paper-1", "reviewer-1")

    assert status == 403
    assert response["message"] == REVIEW_FORM_FORBIDDEN_MESSAGE


def test_at_uc14_04_manuscript_unavailable() -> None:
    service = build_service(
        assigned=True,
        manuscript_available=False,
        form=ReviewForm(
            paper_id="paper-1",
            title="Neural Systems",
            form_fields=[],
        ),
    )

    status, response = get_review_form(service, "paper-1", "reviewer-1")

    assert status == 404
    assert response["message"] == MANUSCRIPT_UNAVAILABLE_MESSAGE


def test_at_uc14_05_review_form_retrieval_error() -> None:
    service = build_service(
        assigned=True,
        manuscript_available=True,
        form=ReviewForm(
            paper_id="paper-1",
            title="Neural Systems",
            form_fields=[],
        ),
        fail_form=True,
    )

    status, response = get_review_form(service, "paper-1", "reviewer-1")

    assert status == 503
    assert response["message"] == REVIEW_FORM_RETRIEVAL_ERROR_MESSAGE


class StubAssignmentRepository:
    def __init__(self, assigned: bool) -> None:
        self._assigned = assigned

    def is_assigned(self, reviewer_id: str, paper_id: str) -> bool:
        return self._assigned


class StubManuscriptRepository:
    def __init__(self, available: bool, *, fail: bool = False) -> None:
        self._available = available
        self._fail = fail

    def has_manuscript(self, paper_id: str) -> bool:
        if self._fail:
            raise ManuscriptRetrievalError("missing manuscript")
        return self._available


class StubReviewFormRepository:
    def __init__(self, form: ReviewForm, *, fail: bool = False) -> None:
        self._form = form
        self._fail = fail

    def fetch_review_form(self, paper_id: str) -> ReviewForm:
        if self._fail:
            raise ReviewFormRetrievalError("form unavailable")
        return self._form


def build_service(
    *,
    assigned: bool,
    manuscript_available: bool,
    form: ReviewForm,
    fail_form: bool = False,
) -> ReviewFormService:
    return ReviewFormService(
        assignment_repository=StubAssignmentRepository(assigned),
        form_repository=StubReviewFormRepository(form, fail=fail_form),
        manuscript_repository=StubManuscriptRepository(manuscript_available),
    )
