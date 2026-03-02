from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Protocol

from models.notification import Notification
from models.review_status import ReviewDetail, ReviewStatus
from services.review_notification_logger import (
    ReviewNotificationLogContext,
    log_review_notification_event,
)

NOTIFICATION_UNAUTHENTICATED_MESSAGE = "Please log in to view notifications."
NOTIFICATION_FORBIDDEN_MESSAGE = "You are not authorized to view notifications."
NOTIFICATION_RETRIEVAL_ERROR_MESSAGE = "Notifications cannot be retrieved at this time."
REVIEW_STATUS_RETRIEVAL_ERROR_MESSAGE = "Review status cannot be retrieved at this time."
LOGIN_REDIRECT = "/login"


class NotificationRetrievalError(RuntimeError):
    pass


class ReviewStatusRetrievalError(RuntimeError):
    pass


class NotificationDeliveryError(RuntimeError):
    pass


class NotificationRepository(Protocol):
    def list_notifications(self, editor_id: str) -> list[Notification]:
        ...

    def store_notification(self, notification: Notification) -> None:
        ...


class ReviewStatusRepository(Protocol):
    def get_status(self, paper_id: str) -> ReviewStatus:
        ...

    def save_status(self, status: ReviewStatus) -> None:
        ...


class NotificationSender(Protocol):
    def send(self, notification: Notification) -> None:
        ...


@dataclass(frozen=True)
class NotificationListResult:
    status: str
    notifications: list[Notification] | None = None
    message: str | None = None
    redirect_to: str | None = None

    @classmethod
    def ok(cls, notifications: list[Notification]) -> "NotificationListResult":
        return cls(status="ok", notifications=notifications)

    @classmethod
    def unauthenticated(cls) -> "NotificationListResult":
        return cls(
            status="unauthenticated",
            message=NOTIFICATION_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def forbidden(cls) -> "NotificationListResult":
        return cls(status="forbidden", message=NOTIFICATION_FORBIDDEN_MESSAGE)

    @classmethod
    def error(cls) -> "NotificationListResult":
        return cls(status="error", message=NOTIFICATION_RETRIEVAL_ERROR_MESSAGE)


@dataclass(frozen=True)
class ReviewStatusResult:
    status: str
    review_status: ReviewStatus | None = None
    message: str | None = None
    redirect_to: str | None = None

    @classmethod
    def ok(cls, review_status: ReviewStatus) -> "ReviewStatusResult":
        return cls(status="ok", review_status=review_status)

    @classmethod
    def unauthenticated(cls) -> "ReviewStatusResult":
        return cls(
            status="unauthenticated",
            message=NOTIFICATION_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def forbidden(cls) -> "ReviewStatusResult":
        return cls(status="forbidden", message=NOTIFICATION_FORBIDDEN_MESSAGE)

    @classmethod
    def error(cls) -> "ReviewStatusResult":
        return cls(status="error", message=REVIEW_STATUS_RETRIEVAL_ERROR_MESSAGE)


@dataclass(frozen=True)
class ReviewSubmissionRecordResult:
    status: str
    notification_failed: bool = False

    @classmethod
    def ok(cls) -> "ReviewSubmissionRecordResult":
        return cls(status="ok")

    @classmethod
    def notification_failed(cls) -> "ReviewSubmissionRecordResult":
        return cls(status="ok", notification_failed=True)


class ReviewNotificationService:
    def __init__(
        self,
        notification_repository: NotificationRepository,
        review_status_repository: ReviewStatusRepository,
        notification_sender: NotificationSender,
    ) -> None:
        self._notification_repository = notification_repository
        self._review_status_repository = review_status_repository
        self._notification_sender = notification_sender

    def record_review_submission(
        self,
        paper_id: str,
        reviewer_id: str,
        reviewers_assigned: int,
        content_summary: str | None = None,
        submitted_at: str | None = None,
        editor_id: str | None = None,
    ) -> ReviewSubmissionRecordResult:
        submitted_at = submitted_at or datetime.now(tz=timezone.utc).isoformat()

        try:
            status = self._review_status_repository.get_status(paper_id)
            details = list(status.review_details)
            reviews_received = status.reviews_received
        except ReviewStatusRetrievalError:
            details = []
            reviews_received = 0
        except Exception:
            details = []
            reviews_received = 0

        details.append(
            ReviewDetail(
                reviewer_id=reviewer_id,
                submitted_at=submitted_at,
                content_summary=content_summary,
            )
        )
        new_status = ReviewStatus(
            paper_id=paper_id,
            reviews_received=reviews_received + 1,
            reviewers_assigned=reviewers_assigned,
            review_details=details,
        )
        self._review_status_repository.save_status(new_status)

        notification = Notification(
            id=f"notif-{paper_id}-{reviewer_id}-{reviews_received + 1}",
            paper_id=paper_id,
            type="review_submitted",
            created_at=submitted_at,
            editor_id=editor_id,
        )
        self._notification_repository.store_notification(notification)

        try:
            self._notification_sender.send(notification)
        except NotificationDeliveryError:
            return ReviewSubmissionRecordResult.notification_failed()

        return ReviewSubmissionRecordResult.ok()

    def list_notifications(
        self,
        editor_id: str | None,
        is_editor: bool,
        trace_id: Optional[str] = None,
    ) -> NotificationListResult:
        context = ReviewNotificationLogContext(paper_id=None, editor_id=editor_id, trace_id=trace_id)

        if not editor_id:
            log_review_notification_event("review_notification_unauthenticated", context)
            return NotificationListResult.unauthenticated()

        if not is_editor:
            log_review_notification_event("review_notification_forbidden", context)
            return NotificationListResult.forbidden()

        try:
            notifications = self._notification_repository.list_notifications(editor_id)
        except NotificationRetrievalError:
            log_review_notification_event(
                "review_notification_retrieval_error",
                context,
                NOTIFICATION_RETRIEVAL_ERROR_MESSAGE,
            )
            return NotificationListResult.error()
        except Exception:
            log_review_notification_event(
                "review_notification_retrieval_error",
                context,
                NOTIFICATION_RETRIEVAL_ERROR_MESSAGE,
            )
            return NotificationListResult.error()

        log_review_notification_event("review_notification_listed", context)
        return NotificationListResult.ok(notifications)

    def get_review_status(
        self,
        paper_id: str,
        editor_id: str | None,
        is_editor: bool,
        trace_id: Optional[str] = None,
    ) -> ReviewStatusResult:
        context = ReviewNotificationLogContext(paper_id=paper_id, editor_id=editor_id, trace_id=trace_id)

        if not editor_id:
            log_review_notification_event("review_status_unauthenticated", context)
            return ReviewStatusResult.unauthenticated()

        if not is_editor:
            log_review_notification_event("review_status_forbidden", context)
            return ReviewStatusResult.forbidden()

        try:
            status = self._review_status_repository.get_status(paper_id)
        except ReviewStatusRetrievalError:
            log_review_notification_event(
                "review_status_retrieval_error",
                context,
                REVIEW_STATUS_RETRIEVAL_ERROR_MESSAGE,
            )
            return ReviewStatusResult.error()
        except Exception:
            log_review_notification_event(
                "review_status_retrieval_error",
                context,
                REVIEW_STATUS_RETRIEVAL_ERROR_MESSAGE,
            )
            return ReviewStatusResult.error()

        log_review_notification_event("review_status_accessed", context)
        return ReviewStatusResult.ok(status)
