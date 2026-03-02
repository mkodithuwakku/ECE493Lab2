from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.review_notifications import get_review_status, list_review_notifications
from models.notification import Notification
from models.review_status import ReviewStatus
from services.review_notification_service import (
    NOTIFICATION_RETRIEVAL_ERROR_MESSAGE,
    REVIEW_STATUS_RETRIEVAL_ERROR_MESSAGE,
    NOTIFICATION_UNAUTHENTICATED_MESSAGE,
    ReviewNotificationService,
    NotificationDeliveryError,
    NotificationRetrievalError,
    ReviewStatusRetrievalError,
)


def test_at_uc18_01_notification_delivered_and_status_updated() -> None:
    bundle = build_service()

    bundle.service.record_review_submission(
        paper_id="paper-1",
        reviewer_id="reviewer-1",
        reviewers_assigned=2,
        content_summary="Good work",
        editor_id="editor-1",
    )

    status, notifications = list_review_notifications(bundle.service, "editor-1", True)
    status_result, review_status = get_review_status(bundle.service, "paper-1", "editor-1", True)

    assert status == 200
    assert notifications["notifications"][0]["paperId"] == "paper-1"
    assert status_result == 200
    assert review_status["paperId"] == "paper-1"
    assert review_status["reviewsReceived"] == 1
    assert review_status["reviewDetails"][0]["contentSummary"] == "Good work"


def test_at_uc18_02_multiple_reviews_submitted() -> None:
    bundle = build_service()

    bundle.service.record_review_submission(
        paper_id="paper-1",
        reviewer_id="reviewer-1",
        reviewers_assigned=2,
        content_summary="Review A",
        editor_id="editor-1",
    )
    bundle.service.record_review_submission(
        paper_id="paper-1",
        reviewer_id="reviewer-2",
        reviewers_assigned=2,
        content_summary="Review B",
        editor_id="editor-1",
    )

    status, notifications = list_review_notifications(bundle.service, "editor-1", True)
    status_result, review_status = get_review_status(bundle.service, "paper-1", "editor-1", True)

    assert status == 200
    assert len(notifications["notifications"]) == 2
    assert status_result == 200
    assert review_status["reviewsReceived"] == 2


def test_at_uc18_03_notification_delivery_failure_still_updates_status() -> None:
    bundle = build_service(notification_fail=True)

    bundle.service.record_review_submission(
        paper_id="paper-1",
        reviewer_id="reviewer-1",
        reviewers_assigned=1,
        content_summary="Review A",
        editor_id="editor-1",
    )

    status_result, review_status = get_review_status(bundle.service, "paper-1", "editor-1", True)

    assert status_result == 200
    assert review_status["reviewsReceived"] == 1


def test_at_uc18_04_editor_not_logged_in() -> None:
    bundle = build_service()

    status, response = list_review_notifications(bundle.service, None, True)
    assert status == 401
    assert response["message"] == NOTIFICATION_UNAUTHENTICATED_MESSAGE

    status, response = get_review_status(bundle.service, "paper-1", None, True)
    assert status == 401
    assert response["message"] == NOTIFICATION_UNAUTHENTICATED_MESSAGE


def test_at_uc18_05_retrieval_error() -> None:
    bundle = build_service(fail_retrieval=True)

    status, response = list_review_notifications(bundle.service, "editor-1", True)
    assert status == 503
    assert response["message"] == NOTIFICATION_RETRIEVAL_ERROR_MESSAGE

    status, response = get_review_status(bundle.service, "paper-1", "editor-1", True)
    assert status == 503
    assert response["message"] == REVIEW_STATUS_RETRIEVAL_ERROR_MESSAGE


class StubNotificationRepository:
    def __init__(self, *, fail: bool = False) -> None:
        self._fail = fail
        self.notifications: list[Notification] = []

    def list_notifications(self, editor_id: str) -> list[Notification]:
        if self._fail:
            raise NotificationRetrievalError("fail")
        return [n for n in self.notifications if n.editor_id == editor_id]

    def store_notification(self, notification: Notification) -> None:
        self.notifications.append(notification)


class StubReviewStatusRepository:
    def __init__(self, *, fail: bool = False) -> None:
        self._fail = fail
        self.statuses: dict[str, ReviewStatus] = {}

    def get_status(self, paper_id: str) -> ReviewStatus:
        if self._fail:
            raise ReviewStatusRetrievalError("fail")
        return self.statuses[paper_id]

    def save_status(self, status: ReviewStatus) -> None:
        self.statuses[status.paper_id] = status


class StubNotificationSender:
    def __init__(self, *, fail: bool = False) -> None:
        self._fail = fail

    def send(self, notification: Notification) -> None:
        if self._fail:
            raise NotificationDeliveryError("fail")


class ServiceBundle:
    def __init__(self, service: ReviewNotificationService) -> None:
        self.service = service


def build_service(
    *,
    notification_fail: bool = False,
    fail_retrieval: bool = False,
) -> ServiceBundle:
    notification_repository = StubNotificationRepository(fail=fail_retrieval)
    review_status_repository = StubReviewStatusRepository(fail=fail_retrieval)
    notification_sender = StubNotificationSender(fail=notification_fail)
    service = ReviewNotificationService(
        notification_repository=notification_repository,
        review_status_repository=review_status_repository,
        notification_sender=notification_sender,
    )
    return ServiceBundle(service)
