from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from models.attendance_type import AttendanceType
from models.attendee_registration import AttendeeRegistration
from services.conference_registration_service import (
    ATTENDANCE_TYPE_UNAVAILABLE_MESSAGE,
    PAYMENT_UNAVAILABLE_MESSAGE,
    REGISTRATION_CLOSED_MESSAGE,
    ConferenceRegistrationService,
    PaymentServiceUnavailable,
)


def test_register_attendee_requires_authentication() -> None:
    service = build_service()

    result = service.register_attendee(attendee_id=None, attendance_type_id=None)

    assert result.status == "unauthenticated"


def test_register_attendee_blocks_when_registration_closed() -> None:
    service = build_service(is_open=False)

    result = service.register_attendee(attendee_id="attendee-1", attendance_type_id=None)

    assert result.status == "closed"
    assert result.message == REGISTRATION_CLOSED_MESSAGE


def test_register_attendee_rejects_unavailable_type() -> None:
    service = build_service(
        attendance_types={
            "vip": AttendanceType(
                id="vip", name="VIP", availability_status="unavailable"
            )
        }
    )

    result = service.register_attendee(attendee_id="attendee-1", attendance_type_id="vip")

    assert result.status == "invalid_type"
    assert result.message == ATTENDANCE_TYPE_UNAVAILABLE_MESSAGE


def test_register_attendee_handles_payment_unavailable() -> None:
    service = build_service(payment_required=True, payment_fail=True)

    result = service.register_attendee(attendee_id="attendee-1", attendance_type_id=None)

    assert result.status == "payment_unavailable"
    assert result.message == PAYMENT_UNAVAILABLE_MESSAGE
    assert result.payment_required is True


def build_service(
    *,
    is_open: bool = True,
    attendance_types: dict[str, AttendanceType] | None = None,
    payment_required: bool = False,
    payment_fail: bool = False,
) -> ConferenceRegistrationService:
    return ConferenceRegistrationService(
        StubRegistrationWindow(is_open=is_open),
        StubAttendanceTypeRepository(attendance_types or {}),
        StubRegistrationRepository(),
        StubPaymentPolicy(required=payment_required),
        StubPaymentService(fail=payment_fail),
    )


class StubRegistrationWindow:
    def __init__(self, *, is_open: bool) -> None:
        self._is_open = is_open

    def is_open(self) -> bool:
        return self._is_open


class StubAttendanceTypeRepository:
    def __init__(self, types: dict[str, AttendanceType]) -> None:
        self._types = types

    def get_attendance_type(self, attendance_type_id: str) -> AttendanceType | None:
        return self._types.get(attendance_type_id)


class StubRegistrationRepository:
    def __init__(self) -> None:
        self.saved: AttendeeRegistration | None = None

    def create_registration(self, registration: AttendeeRegistration) -> AttendeeRegistration:
        self.saved = registration
        return registration

    def get_registration(self, attendee_id: str) -> AttendeeRegistration | None:
        if self.saved and self.saved.attendee_id == attendee_id:
            return self.saved
        return None


class StubPaymentPolicy:
    def __init__(self, *, required: bool) -> None:
        self._required = required

    def is_payment_required(self, attendance_type_id: str | None) -> bool:
        return self._required


class StubPaymentService:
    def __init__(self, *, fail: bool = False) -> None:
        self._fail = fail

    def start_payment(self, registration: AttendeeRegistration) -> None:
        if self._fail:
            raise PaymentServiceUnavailable("payment unavailable")
