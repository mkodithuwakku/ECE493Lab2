from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.review_submission import submit_review
from models.review_submission import ReviewSubmission
from services.review_submission_service import (
    REVIEW_SUBMISSION_DUPLICATE_MESSAGE,
    REVIEW_SUBMISSION_FORBIDDEN_MESSAGE,
    REVIEW_SUBMISSION_STORAGE_ERROR_MESSAGE,
    REVIEW_SUBMISSION_SUCCESS_TEMPLATE,
    REVIEW_SUBMISSION_UNAUTHENTICATED_MESSAGE,
    LOGIN_REDIRECT,
    ReviewSubmissionService,
    ReviewSubmissionStorageError,
)
from services.review_submission_validation import (
    INVALID_FIELDS_MESSAGE,
    MISSING_FIELDS_MESSAGE,
    ReviewValidationResult,
)


def test_at_uc15_01_submit_review_success() -> None:
    bundle = build_service(assigned=True)

    status, response = submit_review(
        bundle.service,
        "paper-1",
        "reviewer-1",
        {"fieldValues": {"overall_score": 5, "comments": "Great"}},
    )

    assert status == 200
    assert response["message"] == REVIEW_SUBMISSION_SUCCESS_TEMPLATE.format(paper_id="paper-1")
    assert bundle.submission_repository.saved[0].paper_id == "paper-1"
    assert bundle.submission_repository.saved[0].reviewer_id == "reviewer-1"


def test_at_uc15_02_unauthenticated_redirect() -> None:
    bundle = build_service(assigned=True)

    status, response = submit_review(
        bundle.service,
        "paper-1",
        None,
        {"fieldValues": {"overall_score": 5, "comments": "Great"}},
    )

    assert status == 401
    assert response["message"] == REVIEW_SUBMISSION_UNAUTHENTICATED_MESSAGE
    assert response["redirect_to"] == LOGIN_REDIRECT


def test_at_uc15_03_unassigned_paper_forbidden() -> None:
    bundle = build_service(assigned=False)

    status, response = submit_review(
        bundle.service,
        "paper-1",
        "reviewer-1",
        {"fieldValues": {"overall_score": 5, "comments": "Great"}},
    )

    assert status == 403
    assert response["message"] == REVIEW_SUBMISSION_FORBIDDEN_MESSAGE
    assert bundle.submission_repository.saved == []


def test_at_uc15_04_missing_required_fields() -> None:
    bundle = build_service(
        assigned=True,
        validator=StubValidator(result=ReviewValidationResult.missing(["comments"])),
    )

    status, response = submit_review(
        bundle.service,
        "paper-1",
        "reviewer-1",
        {"fieldValues": {"overall_score": 5}},
    )

    assert status == 400
    assert response["message"] == MISSING_FIELDS_MESSAGE.format(fields="comments")
    assert "comments" in response["errors"]
    assert bundle.submission_repository.saved == []


def test_at_uc15_05_invalid_field_values() -> None:
    bundle = build_service(
        assigned=True,
        validator=StubValidator(result=ReviewValidationResult.invalid(["overall_score"])),
    )

    status, response = submit_review(
        bundle.service,
        "paper-1",
        "reviewer-1",
        {"fieldValues": {"overall_score": 99, "comments": "Great"}},
    )

    assert status == 400
    assert response["message"] == INVALID_FIELDS_MESSAGE.format(fields="overall_score")
    assert "overall_score" in response["errors"]
    assert bundle.submission_repository.saved == []


def test_at_uc15_06_duplicate_submission() -> None:
    bundle = build_service(assigned=True, duplicate=True)

    status, response = submit_review(
        bundle.service,
        "paper-1",
        "reviewer-1",
        {"fieldValues": {"overall_score": 5, "comments": "Great"}},
    )

    assert status == 409
    assert response["message"] == REVIEW_SUBMISSION_DUPLICATE_MESSAGE
    assert bundle.submission_repository.saved == []


def test_at_uc15_07_storage_failure() -> None:
    bundle = build_service(assigned=True, fail_save=True)

    status, response = submit_review(
        bundle.service,
        "paper-1",
        "reviewer-1",
        {"fieldValues": {"overall_score": 5, "comments": "Great"}},
    )

    assert status == 500
    assert response["message"] == REVIEW_SUBMISSION_STORAGE_ERROR_MESSAGE
    assert bundle.submission_repository.saved == []


class StubAssignmentRepository:
    def __init__(self, assigned: bool) -> None:
        self._assigned = assigned

    def is_assigned(self, reviewer_id: str, paper_id: str) -> bool:
        return self._assigned


class StubSubmissionRepository:
    def __init__(self, *, duplicate: bool = False, fail_save: bool = False) -> None:
        self._duplicate = duplicate
        self._fail_save = fail_save
        self.saved: list[ReviewSubmission] = []

    def has_submission(self, reviewer_id: str, paper_id: str) -> bool:
        return self._duplicate

    def save_submission(self, submission: ReviewSubmission) -> None:
        if self._fail_save:
            raise ReviewSubmissionStorageError("storage failure")
        self.saved.append(submission)


class StubValidator:
    def __init__(self, result: ReviewValidationResult) -> None:
        self._result = result

    def validate(self, field_values: dict) -> ReviewValidationResult:
        return self._result


class ServiceBundle:
    def __init__(self, service: ReviewSubmissionService) -> None:
        self.service = service
        self.submission_repository: StubSubmissionRepository = service._submission_repository  # type: ignore[attr-defined]


def build_service(
    *,
    assigned: bool,
    duplicate: bool = False,
    fail_save: bool = False,
    validator: StubValidator | None = None,
) -> ServiceBundle:
    assignment_repository = StubAssignmentRepository(assigned)
    submission_repository = StubSubmissionRepository(
        duplicate=duplicate,
        fail_save=fail_save,
    )
    service = ReviewSubmissionService(
        assignment_repository=assignment_repository,
        submission_repository=submission_repository,
        validator=validator,
    )
    return ServiceBundle(service)
