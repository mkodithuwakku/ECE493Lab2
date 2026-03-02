from __future__ import annotations

from api.conference_payment_error_mapper import (
    map_conference_payment_error,
    map_payment_status_error,
)
from services.conference_payment_service import ConferencePaymentService


def pay_registration_fee(
    service: ConferencePaymentService,
    attendee_id: str | None,
    payload: dict | None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    result = service.pay_registration_fee(
        attendee_id=attendee_id,
        payload=payload,
        trace_id=trace_id,
    )

    if result.status == "success" and result.registration and result.payment:
        response = {
            "payment_id": result.payment.payment_id,
            "status": result.payment.status,
            "message": result.message,
        }
        if result.payment.receipt:
            response["receipt"] = result.payment.receipt
        if result.payment_details:
            response["amount"] = result.payment_details.amount
            response["currency"] = result.payment_details.currency
            if result.payment_details.line_items:
                response["line_items"] = list(result.payment_details.line_items)
        return 200, response

    return map_conference_payment_error(result)


def get_payment_status(
    service: ConferencePaymentService,
    attendee_id: str | None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    result = service.get_payment_status(attendee_id=attendee_id, trace_id=trace_id)

    if result.status == "found" and result.registration:
        payment_status = "failed"
        if result.payment:
            payment_status = result.payment.status
        return 200, {
            "registration_id": result.registration.registration_id,
            "registration_status": result.registration.status,
            "payment_status": payment_status,
        }

    return map_payment_status_error(result)
