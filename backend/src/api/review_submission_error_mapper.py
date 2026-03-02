from __future__ import annotations

from services.review_submission_service import ReviewSubmissionResult


def map_review_submission_error(result: ReviewSubmissionResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "message": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "forbidden":
        return 403, {"message": result.message}
    if result.status in {"missing", "invalid"}:
        return 400, {
            "message": result.message,
            "errors": result.errors or [],
        }
    if result.status == "duplicate":
        return 409, {"message": result.message}
    if result.status == "error":
        return 500, {"message": result.message}
    return 500, {"message": result.message or "Review submission failed."}
