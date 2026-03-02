from __future__ import annotations

from services.reviewer_assignment_service import AssignmentResult


def map_assignment_error(result: AssignmentResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "message": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "forbidden":
        return 403, {"message": result.message}
    if result.status == "invalid":
        return 400, {"message": result.message}
    if result.status == "duplicate":
        return 409, {"message": result.message}
    if result.status == "limit":
        return 422, {"message": result.message}
    if result.status == "error":
        return 500, {"message": result.message}
    return 500, {"message": result.message or "Reviewer assignment failed."}
