from __future__ import annotations

from services.additional_review_request_service import ReviewRequestResult


def map_review_request_error(result: ReviewRequestResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "message": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "forbidden":
        return 403, {"message": result.message}
    if result.status == "invalid":
        return 400, {"message": result.message}
    return 500, {"message": result.message or "Review request failed."}
