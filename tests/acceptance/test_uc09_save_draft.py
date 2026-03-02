from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.submissions.save_draft_controller import save_draft
from models.submission_draft import SubmissionDraft
from services.draft_repository import DraftRepository
from services.draft_service import (
    INCOMPLETE_MESSAGE,
    STORAGE_FAILURE_MESSAGE,
    SUCCESS_MESSAGE,
    DraftService,
    DraftStorageError,
)
from services.draft_validation import (
    INVALID_DATA_PREFIX,
    MISSING_MINIMUM_MESSAGE,
    DraftValidationError,
    DraftValidator,
)


def test_at_uc09_01_save_draft_success() -> None:
    repository = StubDraftRepository()
    service = DraftService(repository)

    payload = valid_payload()
    status, response = save_draft(service, "sub-1", {"data": payload})

    assert status == 200
    assert response["message"] == SUCCESS_MESSAGE
    assert response["status"] == "complete"
    assert repository.saved[0][0] == "sub-1"
    assert repository.saved[0][1].complete is True


def test_at_uc09_02_invalid_submission_data() -> None:
    repository = StubDraftRepository()
    service = DraftService(repository)

    payload = valid_payload()
    payload["contact_email"] = "invalid-email"

    status, response = save_draft(service, "sub-1", {"data": payload})

    assert status == 400
    assert response["message"].startswith(INVALID_DATA_PREFIX)
    assert repository.saved == []


def test_at_uc09_03_missing_minimum_fields_save_anyway() -> None:
    repository = StubDraftRepository()
    service = DraftService(repository)

    payload = {
        "title": "",
        "abstract": "",
        "authors": [],
        "contact_email": "author@example.com",
    }

    status, response = save_draft(service, "sub-1", {"data": payload})

    assert status == 409
    assert response["message"] == MISSING_MINIMUM_MESSAGE
    assert repository.saved == []

    status, response = save_draft(
        service,
        "sub-1",
        {"data": payload, "save_anyway": True},
    )

    assert status == 200
    assert response["message"] == INCOMPLETE_MESSAGE
    assert response["status"] == "incomplete"
    assert repository.saved[0][1].complete is False


def test_at_uc09_04_storage_failure() -> None:
    repository = StubDraftRepository(fail=True)
    service = DraftService(repository)

    status, response = save_draft(service, "sub-1", {"data": valid_payload()})

    assert status == 500
    assert response["message"] == STORAGE_FAILURE_MESSAGE
    assert repository.saved == []


def valid_payload() -> dict:
    return {
        "title": "Paper Title",
        "abstract": "Abstract text",
        "authors": ["Author One"],
        "contact_email": "author@example.com",
    }


class StubDraftRepository(DraftRepository):
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.saved: list[tuple[str, SubmissionDraft]] = []

    def save_draft(self, submission_id: str, draft: SubmissionDraft) -> None:
        if self.fail:
            raise DraftStorageError("storage failure")
        self.saved.append((submission_id, draft))


class FailingValidator(DraftValidator):
    def validate(self, payload: dict):  # type: ignore[override]
        raise DraftValidationError("validation failure")
