from __future__ import annotations

from api.conference_registration_error_mapper import (
    map_conference_registration_error,
    map_registration_status_error,
)
from services.conference_registration_service import ConferenceRegistrationService


def register_for_conference(
    service: ConferenceRegistrationService,
    attendee_id: str | None,
    payload: dict | None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    attendance_type_id = None
    if payload:
        attendance_type_id = payload.get("attendance_type_id")

    result = service.register_attendee(
        attendee_id=attendee_id,
        attendance_type_id=attendance_type_id,
        trace_id=trace_id,
    )

    if result.status in {"registered", "pending_unpaid", "payment_unavailable"} and result.registration:
        registration = result.registration
        response = {
            "registration_id": registration.registration_id,
            "status": registration.status,
            "message": result.message,
            "payment_required": result.payment_required,
        }
        if result.status == "payment_unavailable":
            response["payment_error"] = True
        return 200, response

    return map_conference_registration_error(result)


def get_registration_status(
    service: ConferenceRegistrationService,
    attendee_id: str | None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    result = service.get_registration_status(attendee_id=attendee_id, trace_id=trace_id)

    if result.status == "found" and result.registration:
        registration = result.registration
        return 200, {
            "registration_id": registration.registration_id,
            "status": registration.status,
            "payment_required": registration.status == "pending_unpaid",
        }

    return map_registration_status_error(result)
