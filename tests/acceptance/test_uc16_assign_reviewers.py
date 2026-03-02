from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.reviewer_assignment import assign_reviewers
from services.reviewer_assignment_service import (
    ASSIGNMENT_DUPLICATE_MESSAGE,
    ASSIGNMENT_FORBIDDEN_MESSAGE,
    ASSIGNMENT_LIMIT_MESSAGE,
    ASSIGNMENT_NOTIFICATION_FAILED_MESSAGE,
    ASSIGNMENT_STORAGE_ERROR_MESSAGE,
    ASSIGNMENT_SUCCESS_TEMPLATE,
    ASSIGNMENT_UNAUTHENTICATED_MESSAGE,
    INVALID_REVIEWER_MESSAGE,
    REVIEWER_NOT_FOUND_MESSAGE,
    AssignmentStorageError,
    NotificationDeliveryError,
    ReviewerAssignmentService,
)


def test_at_uc16_01_assign_one_reviewer_success() -> None:
    bundle = build_service()

    status, response = assign_reviewers(
        bundle.service,
        "paper-1",
        editor_id="editor-1",
        is_editor=True,
        payload={"reviewerIds": ["reviewer-1"]},
    )

    assert status == 200
    assert response["message"] == ASSIGNMENT_SUCCESS_TEMPLATE.format(paper_id="paper-1")
    assert response["reviewerIds"] == ["reviewer-1"]
    assert bundle.assignment_repository.saved == [("paper-1", "reviewer-1")]


def test_at_uc16_02_assign_multiple_reviewers_success() -> None:
    bundle = build_service()

    status, response = assign_reviewers(
        bundle.service,
        "paper-1",
        editor_id="editor-1",
        is_editor=True,
        payload={"reviewerIds": ["reviewer-1", "reviewer-2"]},
    )

    assert status == 200
    assert response["reviewerIds"] == ["reviewer-1", "reviewer-2"]
    assert ("paper-1", "reviewer-1") in bundle.assignment_repository.saved
    assert ("paper-1", "reviewer-2") in bundle.assignment_repository.saved


def test_at_uc16_03_editor_not_logged_in_or_not_authorized() -> None:
    bundle = build_service()

    status, response = assign_reviewers(
        bundle.service,
        "paper-1",
        editor_id=None,
        is_editor=False,
        payload={"reviewerIds": ["reviewer-1"]},
    )

    assert status == 401
    assert response["message"] == ASSIGNMENT_UNAUTHENTICATED_MESSAGE

    status, response = assign_reviewers(
        bundle.service,
        "paper-1",
        editor_id="user-1",
        is_editor=False,
        payload={"reviewerIds": ["reviewer-1"]},
    )

    assert status == 403
    assert response["message"] == ASSIGNMENT_FORBIDDEN_MESSAGE


def test_at_uc16_04_reviewer_invalid_or_not_found() -> None:
    bundle = build_service(valid_identifiers=False)

    status, response = assign_reviewers(
        bundle.service,
        "paper-1",
        editor_id="editor-1",
        is_editor=True,
        payload={"reviewerIds": ["invalid-email"]},
    )

    assert status == 400
    assert response["message"] == INVALID_REVIEWER_MESSAGE

    bundle = build_service(reviewer_exists=False)

    status, response = assign_reviewers(
        bundle.service,
        "paper-1",
        editor_id="editor-1",
        is_editor=True,
        payload={"reviewerIds": ["reviewer-missing"]},
    )

    assert status == 400
    assert response["message"] == REVIEWER_NOT_FOUND_MESSAGE


def test_at_uc16_05_duplicate_assignment() -> None:
    bundle = build_service(duplicate=True)

    status, response = assign_reviewers(
        bundle.service,
        "paper-1",
        editor_id="editor-1",
        is_editor=True,
        payload={"reviewerIds": ["reviewer-1"]},
    )

    assert status == 409
    assert response["message"] == ASSIGNMENT_DUPLICATE_MESSAGE


def test_at_uc16_06_assignment_limit_reached() -> None:
    bundle = build_service(at_limit=True)

    status, response = assign_reviewers(
        bundle.service,
        "paper-1",
        editor_id="editor-1",
        is_editor=True,
        payload={"reviewerIds": ["reviewer-1"]},
    )

    assert status == 422
    assert response["message"] == ASSIGNMENT_LIMIT_MESSAGE


def test_at_uc16_07_notification_delivery_failure() -> None:
    bundle = build_service(notification_fail=True)

    status, response = assign_reviewers(
        bundle.service,
        "paper-1",
        editor_id="editor-1",
        is_editor=True,
        payload={"reviewerIds": ["reviewer-1"]},
    )

    assert status == 502
    assert response["message"] == ASSIGNMENT_NOTIFICATION_FAILED_MESSAGE
    assert ("paper-1", "reviewer-1") in bundle.assignment_repository.saved


def test_at_uc16_08_storage_failure() -> None:
    bundle = build_service(fail_storage=True)

    status, response = assign_reviewers(
        bundle.service,
        "paper-1",
        editor_id="editor-1",
        is_editor=True,
        payload={"reviewerIds": ["reviewer-1"]},
    )

    assert status == 500
    assert response["message"] == ASSIGNMENT_STORAGE_ERROR_MESSAGE
    assert bundle.assignment_repository.saved == []


class StubAssignmentRepository:
    def __init__(self, *, duplicate: bool = False, fail_storage: bool = False) -> None:
        self._duplicate = duplicate
        self._fail_storage = fail_storage
        self.saved: list[tuple[str, str]] = []

    def is_assigned(self, reviewer_id: str, paper_id: str) -> bool:
        return self._duplicate

    def save_assignment(self, assignment) -> None:
        if self._fail_storage:
            raise AssignmentStorageError("storage failure")
        self.saved.append((assignment.paper_id, assignment.reviewer_id))


class StubReviewerDirectory:
    def __init__(self, *, exists: bool = True, valid_identifier: bool = True) -> None:
        self._exists = exists
        self._valid_identifier = valid_identifier

    def is_valid_identifier(self, reviewer_id: str) -> bool:
        return self._valid_identifier

    def find_reviewer(self, reviewer_id: str) -> dict | None:
        if not self._exists:
            return None
        return {"id": reviewer_id}


class StubReviewerLimitRepository:
    def __init__(self, *, at_limit: bool = False) -> None:
        self._at_limit = at_limit

    def at_limit(self, reviewer_id: str) -> bool:
        return self._at_limit


class StubNotificationService:
    def __init__(self, *, fail: bool = False) -> None:
        self._fail = fail

    def send_invitation(self, reviewer_id: str, paper_id: str) -> None:
        if self._fail:
            raise NotificationDeliveryError("notification failure")


class ServiceBundle:
    def __init__(self, service: ReviewerAssignmentService) -> None:
        self.service = service
        self.assignment_repository: StubAssignmentRepository = service._assignment_repository  # type: ignore[attr-defined]


def build_service(
    *,
    duplicate: bool = False,
    valid_identifiers: bool = True,
    reviewer_exists: bool = True,
    at_limit: bool = False,
    notification_fail: bool = False,
    fail_storage: bool = False,
) -> ServiceBundle:
    assignment_repository = StubAssignmentRepository(
        duplicate=duplicate,
        fail_storage=fail_storage,
    )
    reviewer_directory = StubReviewerDirectory(
        exists=reviewer_exists,
        valid_identifier=valid_identifiers,
    )
    reviewer_limit_repository = StubReviewerLimitRepository(at_limit=at_limit)
    notification_service = StubNotificationService(fail=notification_fail)
    service = ReviewerAssignmentService(
        assignment_repository=assignment_repository,
        reviewer_directory=reviewer_directory,
        reviewer_limit_repository=reviewer_limit_repository,
        notification_service=notification_service,
    )
    return ServiceBundle(service)
