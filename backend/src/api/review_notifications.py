from __future__ import annotations

from api.review_notifications_error_mapper import (
    map_notification_error,
    map_review_status_error,
)
from services.review_notification_service import ReviewNotificationService


def list_review_notifications(
    service: ReviewNotificationService,
    editor_id: str | None,
    is_editor: bool,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    result = service.list_notifications(
        editor_id=editor_id,
        is_editor=is_editor,
        trace_id=trace_id,
    )

    if result.status == "ok":
        notifications = [
            {
                "notificationId": notification.id,
                "paperId": notification.paper_id,
                "type": notification.type,
                "createdAt": notification.created_at,
            }
            for notification in (result.notifications or [])
        ]
        return 200, {"notifications": notifications}

    return map_notification_error(result)


def get_review_status(
    service: ReviewNotificationService,
    paper_id: str,
    editor_id: str | None,
    is_editor: bool,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    result = service.get_review_status(
        paper_id=paper_id,
        editor_id=editor_id,
        is_editor=is_editor,
        trace_id=trace_id,
    )

    if result.status == "ok" and result.review_status:
        status = result.review_status
        return 200, {
            "paperId": status.paper_id,
            "reviewsReceived": status.reviews_received,
            "reviewersAssigned": status.reviewers_assigned,
            "reviewDetails": [
                {
                    "reviewerId": detail.reviewer_id,
                    "submittedAt": detail.submitted_at,
                    "contentSummary": detail.content_summary,
                }
                for detail in status.review_details
            ],
        }

    return map_review_status_error(result)
