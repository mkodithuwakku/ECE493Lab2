from __future__ import annotations

from services.assigned_papers_service import AssignedPapersResult


def map_assigned_papers_error(result: AssignedPapersResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "message": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "forbidden":
        return 403, {"message": result.message}
    return 500, {"message": result.message or "Assigned papers retrieval failed."}
