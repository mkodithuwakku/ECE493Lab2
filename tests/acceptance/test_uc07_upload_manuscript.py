from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.submissions.manuscript_upload_controller import upload_manuscript
from services.file_storage_service import StorageError, UploadInterruptedError
from services.manuscript_upload_service import (
    STORAGE_FAILURE_MESSAGE,
    SUCCESS_MESSAGE,
    UPLOAD_INTERRUPTED_MESSAGE,
    ManuscriptUploadService,
)
from services.submission_repository import SubmissionRepository


def test_at_uc07_01_upload_success() -> None:
    repo = StubSubmissionRepository()
    storage = StubFileStorageService()
    service = ManuscriptUploadService(repo, storage)

    status, payload = upload_manuscript(
        service, "sub-1", {"filename": "paper.pdf", "size_bytes": 1024}
    )

    assert status == 200
    assert payload["message"] == SUCCESS_MESSAGE
    assert repo.associations == [("sub-1", "file-1")]


def test_at_uc07_02_unsupported_format() -> None:
    repo = StubSubmissionRepository()
    storage = StubFileStorageService()
    service = ManuscriptUploadService(repo, storage)

    status, payload = upload_manuscript(
        service, "sub-1", {"filename": "paper.txt", "size_bytes": 1024}
    )

    assert status == 400
    assert payload["message"] == "Unsupported file format. Accepted formats: PDF, Word, LaTeX."
    assert repo.associations == []


def test_at_uc07_03_size_limit() -> None:
    repo = StubSubmissionRepository()
    storage = StubFileStorageService()
    service = ManuscriptUploadService(repo, storage)

    status, payload = upload_manuscript(
        service, "sub-1", {"filename": "paper.pdf", "size_bytes": 60 * 1024 * 1024}
    )

    assert status == 400
    assert payload["message"] == "File exceeds maximum size of 50 MB."
    assert repo.associations == []


def test_at_uc07_04_upload_interrupted() -> None:
    repo = StubSubmissionRepository()
    storage = StubFileStorageService(interrupted=True)
    service = ManuscriptUploadService(repo, storage)

    status, payload = upload_manuscript(
        service, "sub-1", {"filename": "paper.pdf", "size_bytes": 1024}
    )

    assert status == 409
    assert payload["message"] == UPLOAD_INTERRUPTED_MESSAGE
    assert repo.associations == []


def test_at_uc07_05_storage_failure() -> None:
    repo = StubSubmissionRepository()
    storage = StubFileStorageService(fail=True)
    service = ManuscriptUploadService(repo, storage)

    status, payload = upload_manuscript(
        service, "sub-1", {"filename": "paper.pdf", "size_bytes": 1024}
    )

    assert status == 500
    assert payload["message"] == STORAGE_FAILURE_MESSAGE
    assert repo.associations == []


class StubSubmissionRepository(SubmissionRepository):
    def __init__(self) -> None:
        self.associations: list[tuple[str, str]] = []

    def associate_manuscript(self, submission_id: str, file_id: str) -> None:
        self.associations.append((submission_id, file_id))


class StubFileStorageService:
    def __init__(self, *, interrupted: bool = False, fail: bool = False) -> None:
        self.interrupted = interrupted
        self.fail = fail

    def store_file(self, submission_id: str, filename: str, size_bytes: int) -> str:
        if self.interrupted:
            raise UploadInterruptedError("interrupted")
        if self.fail:
            raise StorageError("storage failed")
        return "file-1"
