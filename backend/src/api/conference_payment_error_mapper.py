from __future__ import annotations

from services.conference_payment_service import PaymentResult, PaymentStatusResult


def map_conference_payment_error(result: PaymentResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "error": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status in {"no_pending", "already_paid"}:
        return 409, {"error": result.message}
    if result.status in {"declined", "canceled"}:
        return 402, {"error": result.message}
    if result.status == "unavailable":
        return 503, {"error": result.message}
    if result.status == "record_failed":
        return 500, {"error": result.message}
    return 500, {"error": result.message or "Payment failed."}


def map_payment_status_error(result: PaymentStatusResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "error": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    return 500, {"error": result.message or "Payment status unavailable."}
