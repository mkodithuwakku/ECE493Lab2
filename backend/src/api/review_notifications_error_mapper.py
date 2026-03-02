from __future__ import annotations

from services.review_notification_service import NotificationListResult, ReviewStatusResult


def map_notification_error(result: NotificationListResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "message": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "forbidden":
        return 403, {"message": result.message}
    return 503, {"message": result.message}


def map_review_status_error(result: ReviewStatusResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "message": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "forbidden":
        return 403, {"message": result.message}
    return 503, {"message": result.message}
