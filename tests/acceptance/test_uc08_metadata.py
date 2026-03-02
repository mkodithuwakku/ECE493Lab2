from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.submissions.metadata_controller import save_metadata
from models.paper_metadata import PaperMetadata
from services.metadata_repository import MetadataRepository
from services.metadata_service import (
    STORAGE_FAILURE_MESSAGE,
    SUCCESS_MESSAGE,
    VALIDATION_FAILURE_MESSAGE,
    MetadataService,
    MetadataStorageError,
)
from services.metadata_validation import (
    INVALID_METADATA_PREFIX,
    MISSING_FIELDS_MESSAGE,
    MetadataValidationError,
    MetadataValidator,
)
from services.submission_repository import SubmissionRepository


def test_at_uc08_01_save_metadata_success() -> None:
    submission_repo = StubSubmissionRepository()
    metadata_repo = StubMetadataRepository()
    service = MetadataService(submission_repo, metadata_repo)

    payload = valid_payload()
    status, response = save_metadata(service, "sub-1", payload)

    assert status == 200
    assert response["message"] == SUCCESS_MESSAGE
    assert metadata_repo.saved[0][0] == "sub-1"
    assert metadata_repo.saved[0][1].contact_email == "author@example.com"


def test_at_uc08_02_missing_required_fields() -> None:
    submission_repo = StubSubmissionRepository()
    metadata_repo = StubMetadataRepository()
    service = MetadataService(submission_repo, metadata_repo)

    status, response = save_metadata(service, "sub-1", {"author_names": []})

    assert status == 400
    assert response["message"] == MISSING_FIELDS_MESSAGE
    assert metadata_repo.saved == []


def test_at_uc08_03_invalid_metadata_information() -> None:
    submission_repo = StubSubmissionRepository()
    metadata_repo = StubMetadataRepository()
    service = MetadataService(submission_repo, metadata_repo)

    payload = valid_payload()
    payload["contact_email"] = "not-an-email"

    status, response = save_metadata(service, "sub-1", payload)

    assert status == 400
    assert response["message"].startswith(INVALID_METADATA_PREFIX)
    assert metadata_repo.saved == []


def test_at_uc08_04_validation_failure() -> None:
    submission_repo = StubSubmissionRepository()
    metadata_repo = StubMetadataRepository()
    service = MetadataService(
        submission_repo,
        metadata_repo,
        validator=FailingValidator(),
    )

    status, response = save_metadata(service, "sub-1", valid_payload())

    assert status == 500
    assert response["message"] == VALIDATION_FAILURE_MESSAGE
    assert metadata_repo.saved == []


def test_at_uc08_05_storage_failure() -> None:
    submission_repo = StubSubmissionRepository()
    metadata_repo = StubMetadataRepository(fail=True)
    service = MetadataService(submission_repo, metadata_repo)

    status, response = save_metadata(service, "sub-1", valid_payload())

    assert status == 500
    assert response["message"] == STORAGE_FAILURE_MESSAGE
    assert metadata_repo.saved == []


def valid_payload() -> dict:
    return {
        "author_names": ["Author One"],
        "affiliations": ["University"],
        "contact_email": "author@example.com",
        "abstract": "This is an abstract.",
        "keywords": ["ai", "systems"],
        "paper_source": "Conf 2026",
    }


class StubSubmissionRepository(SubmissionRepository):
    def __init__(self, *, finalized: bool = False) -> None:
        self.finalized = finalized

    def associate_manuscript(self, submission_id: str, file_id: str) -> None:
        return None

    def is_finalized(self, submission_id: str) -> bool:
        return self.finalized


class StubMetadataRepository(MetadataRepository):
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.saved: list[tuple[str, PaperMetadata]] = []

    def save_metadata(self, submission_id: str, metadata: PaperMetadata) -> None:
        if self.fail:
            raise MetadataStorageError("storage failure")
        self.saved.append((submission_id, metadata))


class FailingValidator(MetadataValidator):
    def validate(self, payload: dict):  # type: ignore[override]
        raise MetadataValidationError("validation failure")
