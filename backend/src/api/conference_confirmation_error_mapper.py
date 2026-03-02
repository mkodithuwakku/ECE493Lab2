from __future__ import annotations

from services.conference_confirmation_service import ConfirmationResult, ReceiptResult


def map_confirmation_error(result: ConfirmationResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "error": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "forbidden":
        return 403, {
            "error": result.message,
            "redirect_to": result.redirect_to or "/registration",
        }
    if result.status == "not_paid":
        return 400, {"error": result.message}
    if result.status == "error":
        return 503, {"error": result.message}
    return 500, {"error": result.message or "Confirmation unavailable."}


def map_receipt_error(result: ReceiptResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "error": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "forbidden":
        return 403, {
            "error": result.message,
            "redirect_to": result.redirect_to or "/registration",
        }
    if result.status == "not_paid":
        return 400, {"error": result.message}
    if result.status == "not_available":
        return 404, {"error": result.message}
    if result.status == "error":
        return 503, {"error": result.message}
    return 500, {"error": result.message or "Receipt unavailable."}
