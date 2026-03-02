from __future__ import annotations

from services.decision_service import DecisionResult


def map_decision_error(result: DecisionResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "message": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "forbidden":
        return 403, {"message": result.message}
    if result.status == "error":
        return 500, {"message": result.message}
    if result.status == "unavailable":
        return 503, {"message": result.message}
    return 500, {"message": result.message or "Decision retrieval failed."}
