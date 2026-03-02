from __future__ import annotations

from api.conference_confirmation_error_mapper import (
    map_confirmation_error,
    map_receipt_error,
)
from services.conference_confirmation_service import ConferenceConfirmationService


def get_payment_confirmation(
    service: ConferenceConfirmationService,
    attendee_id: str | None,
    registration_id: str | None = None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    result = service.get_confirmation(
        attendee_id=attendee_id,
        registration_id=registration_id,
        trace_id=trace_id,
    )

    if result.status == "ok" and result.registration:
        confirmation = result.confirmation
        ticket = result.ticket
        response = {
            "registration_id": result.registration.registration_id,
            "status": result.registration.status,
            "attendee_id": result.registration.attendee_id,
            "attendance_type_id": result.registration.attendance_type_id,
        }
        if confirmation:
            response.update(
                {
                    "amount": confirmation.amount,
                    "currency": confirmation.currency,
                    "transaction_reference_id": confirmation.transaction_reference_id,
                    "confirmed_at": confirmation.confirmed_at,
                }
            )
        if ticket:
            response.update(
                {
                    "ticket_id": ticket.ticket_id,
                    "ticket_code": ticket.ticket_code,
                    "ticket_issued_at": ticket.issued_at,
                }
            )
        return 200, response

    return map_confirmation_error(result)


def get_receipt(
    service: ConferenceConfirmationService,
    attendee_id: str | None,
    registration_id: str | None = None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    result = service.get_receipt(
        attendee_id=attendee_id,
        registration_id=registration_id,
        trace_id=trace_id,
    )

    if result.status == "ok" and result.receipt:
        receipt = result.receipt
        return 200, {
            "receipt_id": receipt.receipt_id,
            "receipt_number": receipt.receipt_number,
            "registration_id": receipt.registration_id,
            "generated_at": receipt.generated_at,
        }

    return map_receipt_error(result)
