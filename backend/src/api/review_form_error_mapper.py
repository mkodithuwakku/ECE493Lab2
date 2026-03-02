from __future__ import annotations

from services.review_form_service import ReviewFormResult


def map_review_form_error(result: ReviewFormResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "message": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "forbidden":
        return 403, {"message": result.message}
    if result.status == "manuscript_unavailable":
        return 404, {"message": result.message}
    if result.status == "error":
        return 503, {"message": result.message}
    return 500, {"message": result.message or "Review form access failed."}
