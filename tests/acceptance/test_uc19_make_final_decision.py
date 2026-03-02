from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.final_decision import get_final_decision, record_final_decision
from api.final_decision_review_requests import request_additional_reviews
from models.final_decision import FinalDecision
from models.paper_submission import PaperSubmission
from services.additional_review_request_service import (
    AdditionalReviewRequestService,
    REVIEW_REQUEST_SUCCESS_MESSAGE,
)
from services.final_decision_service import (
    FINAL_DECISION_NOTIFICATION_FAILED_MESSAGE,
    FINAL_DECISION_REVIEW_INCOMPLETE_MESSAGE,
    FINAL_DECISION_STORAGE_ERROR_MESSAGE,
    FINAL_DECISION_UNAUTHENTICATED_MESSAGE,
    FINAL_DECISION_FORBIDDEN_MESSAGE,
    FinalDecisionAccessService,
    FinalDecisionService,
    FinalDecisionStorageError,
    NotificationDeliveryError,
)


def test_at_uc19_01_record_accept_decision() -> None:
    bundle = build_bundle(reviews_received=2, reviewers_assigned=2)

    status, response = record_final_decision(
        bundle.decision_service,
        "paper-1",
        editor_id="editor-1",
        is_editor=True,
        payload={"decisionValue": "accept"},
    )

    assert status == 200
    assert "accepted" in response["message"]

    view_status, view_response = get_final_decision(
        bundle.access_service,
        "paper-1",
        author_id="author-1",
    )

    assert view_status == 200
    assert view_response["decisionStatus"] == "accepted"


def test_at_uc19_02_record_reject_decision() -> None:
    bundle = build_bundle(reviews_received=2, reviewers_assigned=2)

    status, response = record_final_decision(
        bundle.decision_service,
        "paper-2",
        editor_id="editor-1",
        is_editor=True,
        payload={"decisionValue": "reject"},
    )

    assert status == 200
    assert "rejected" in response["message"]

    view_status, view_response = get_final_decision(
        bundle.access_service,
        "paper-2",
        author_id="author-2",
    )

    assert view_status == 200
    assert view_response["decisionStatus"] == "rejected"


def test_at_uc19_03_block_decision_when_reviews_incomplete() -> None:
    bundle = build_bundle(reviews_received=1, reviewers_assigned=2)

    status, response = record_final_decision(
        bundle.decision_service,
        "paper-3",
        editor_id="editor-1",
        is_editor=True,
        payload={"decisionValue": "accept"},
    )

    assert status == 400
    assert response["message"] == FINAL_DECISION_REVIEW_INCOMPLETE_MESSAGE
    assert bundle.decision_repository.saved == []


def test_at_uc19_04_request_additional_reviews() -> None:
    bundle = build_bundle(reviews_received=1, reviewers_assigned=2)

    status, response = request_additional_reviews(
        bundle.review_request_service,
        "paper-4",
        editor_id="editor-1",
        is_editor=True,
        payload={"reviewerIds": ["reviewer-1", "reviewer-2"]},
    )

    assert status == 200
    assert response["message"] == REVIEW_REQUEST_SUCCESS_MESSAGE
    assert bundle.review_request_repository.requests == [
        ("paper-4", ["reviewer-1", "reviewer-2"])
    ]
    assert bundle.decision_repository.saved == []


def test_at_uc19_05_editor_not_logged_in_or_not_authorized() -> None:
    bundle = build_bundle(reviews_received=2, reviewers_assigned=2)

    status, response = record_final_decision(
        bundle.decision_service,
        "paper-5",
        editor_id=None,
        is_editor=True,
        payload={"decisionValue": "accept"},
    )

    assert status == 401
    assert response["message"] == FINAL_DECISION_UNAUTHENTICATED_MESSAGE

    status, response = record_final_decision(
        bundle.decision_service,
        "paper-5",
        editor_id="user-1",
        is_editor=False,
        payload={"decisionValue": "accept"},
    )

    assert status == 403
    assert response["message"] == FINAL_DECISION_FORBIDDEN_MESSAGE


def test_at_uc19_06_notification_failure_decision_visible() -> None:
    bundle = build_bundle(reviews_received=2, reviewers_assigned=2, notification_fail=True)

    status, response = record_final_decision(
        bundle.decision_service,
        "paper-6",
        editor_id="editor-1",
        is_editor=True,
        payload={"decisionValue": "accept"},
    )

    assert status == 200
    assert response["warning"] == FINAL_DECISION_NOTIFICATION_FAILED_MESSAGE

    view_status, view_response = get_final_decision(
        bundle.access_service,
        "paper-6",
        author_id="author-6",
    )

    assert view_status == 200
    assert view_response["decisionStatus"] == "accepted"


def test_at_uc19_07_storage_failure() -> None:
    bundle = build_bundle(reviews_received=2, reviewers_assigned=2, fail_storage=True)

    status, response = record_final_decision(
        bundle.decision_service,
        "paper-7",
        editor_id="editor-1",
        is_editor=True,
        payload={"decisionValue": "accept"},
    )

    assert status == 500
    assert response["message"] == FINAL_DECISION_STORAGE_ERROR_MESSAGE
    assert bundle.decision_repository.saved == []


class StubDecisionRepository:
    def __init__(self, *, fail_storage: bool = False) -> None:
        self._fail_storage = fail_storage
        self.saved: list[FinalDecision] = []

    def has_decision(self, paper_id: str) -> bool:
        return any(decision.paper_id == paper_id for decision in self.saved)

    def save_decision(self, decision: FinalDecision) -> None:
        if self._fail_storage:
            raise FinalDecisionStorageError("storage failure")
        self.saved.append(decision)

    def get_decision(self, paper_id: str) -> FinalDecision | None:
        for decision in self.saved:
            if decision.paper_id == paper_id:
                return decision
        return None


class StubReviewStatusRepository:
    def __init__(self, reviews_received: int, reviewers_assigned: int) -> None:
        self._reviews_received = reviews_received
        self._reviewers_assigned = reviewers_assigned

    def get_status(self, paper_id: str) -> dict:
        return {
            "reviewsReceived": self._reviews_received,
            "reviewersAssigned": self._reviewers_assigned,
        }


class StubNotificationSender:
    def __init__(self, *, fail: bool = False) -> None:
        self._fail = fail

    def send_decision(self, paper_id: str, decision: str) -> None:
        if self._fail:
            raise NotificationDeliveryError("notification failure")


class StubSubmissionRepository:
    def __init__(self, author_map: dict[str, str]) -> None:
        self._author_map = author_map

    def fetch_submission(self, paper_id: str) -> PaperSubmission:
        author_id = self._author_map.get(paper_id, "author-1")
        return PaperSubmission(
            id=paper_id,
            author_ids=[author_id],
            decision_status="recorded",
            decision_value=None,
        )


class StubReviewRequestRepository:
    def __init__(self) -> None:
        self.requests: list[tuple[str, list[str]]] = []

    def record_request(self, paper_id: str, reviewer_ids: list[str]) -> None:
        self.requests.append((paper_id, reviewer_ids))


class ServiceBundle:
    def __init__(
        self,
        decision_service: FinalDecisionService,
        access_service: FinalDecisionAccessService,
        review_request_service: AdditionalReviewRequestService,
        decision_repository: StubDecisionRepository,
        review_request_repository: StubReviewRequestRepository,
    ) -> None:
        self.decision_service = decision_service
        self.access_service = access_service
        self.review_request_service = review_request_service
        self.decision_repository = decision_repository
        self.review_request_repository = review_request_repository


def build_bundle(
    *,
    reviews_received: int,
    reviewers_assigned: int,
    notification_fail: bool = False,
    fail_storage: bool = False,
) -> ServiceBundle:
    decision_repository = StubDecisionRepository(fail_storage=fail_storage)
    review_status_repository = StubReviewStatusRepository(
        reviews_received=reviews_received,
        reviewers_assigned=reviewers_assigned,
    )
    notification_sender = StubNotificationSender(fail=notification_fail)

    decision_service = FinalDecisionService(
        decision_repository=decision_repository,
        review_status_repository=review_status_repository,
        notification_sender=notification_sender,
    )
    access_service = FinalDecisionAccessService(
        decision_repository=decision_repository,
        submission_repository=StubSubmissionRepository(
            {
                "paper-1": "author-1",
                "paper-2": "author-2",
                "paper-6": "author-6",
            }
        ),
    )
    review_request_repository = StubReviewRequestRepository()
    review_request_service = AdditionalReviewRequestService(review_request_repository)

    return ServiceBundle(
        decision_service,
        access_service,
        review_request_service,
        decision_repository,
        review_request_repository,
    )
