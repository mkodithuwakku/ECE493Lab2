from __future__ import annotations

from services.final_decision_service import DecisionViewResult, FinalDecisionResult


def map_final_decision_error(result: FinalDecisionResult) -> tuple[int, dict]:
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
    if result.status == "incomplete":
        return 400, {"message": result.message}
    if result.status == "error":
        return 500, {"message": result.message}
    return 500, {"message": result.message or "Final decision failed."}


def map_final_decision_view_error(result: DecisionViewResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "message": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "forbidden":
        return 403, {"message": result.message}
    return 503, {"message": result.message}
