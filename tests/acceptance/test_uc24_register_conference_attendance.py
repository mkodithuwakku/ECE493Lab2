from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.conference_registration import register_for_conference
from models.attendance_type import AttendanceType
from models.attendee_registration import AttendeeRegistration
from services.conference_registration_service import (
    ATTENDANCE_TYPE_UNAVAILABLE_MESSAGE,
    PAYMENT_REQUIRED_MESSAGE,
    PAYMENT_UNAVAILABLE_MESSAGE,
    REGISTRATION_CLOSED_MESSAGE,
    REGISTRATION_FAILED_MESSAGE,
    ConferenceRegistrationService,
    PaymentServiceUnavailable,
    RegistrationStorageError,
)


def test_at_uc24_01_register_for_conference_successfully() -> None:
    attendance_type = AttendanceType(id="standard", name="Standard")
    window_repo = StubRegistrationWindow(is_open=True)
    attendance_repo = StubAttendanceTypeRepository({"standard": attendance_type})
    registration_repo = StubRegistrationRepository()
    payment_policy = StubPaymentPolicy(required=True)
    payment_service = StubPaymentService()
    service = ConferenceRegistrationService(
        window_repo,
        attendance_repo,
        registration_repo,
        payment_policy,
        payment_service,
    )

    status, response = register_for_conference(
        service,
        attendee_id="attendee-1",
        payload={"attendance_type_id": "standard"},
    )

    assert status == 200
    assert response["status"] == "pending_unpaid"
    assert response["payment_required"] is True
    assert response["message"] == PAYMENT_REQUIRED_MESSAGE
    assert registration_repo.saved is not None


def test_at_uc24_02_attendee_not_logged_in_then_logs_in() -> None:
    attendance_type = AttendanceType(id="standard", name="Standard")
    service = ConferenceRegistrationService(
        StubRegistrationWindow(is_open=True),
        StubAttendanceTypeRepository({"standard": attendance_type}),
        StubRegistrationRepository(),
        StubPaymentPolicy(required=False),
        StubPaymentService(),
    )

    status, response = register_for_conference(
        service,
        attendee_id=None,
        payload={"attendance_type_id": "standard"},
    )

    assert status == 401
    assert response["redirect_to"] == "/login"

    status, response = register_for_conference(
        service,
        attendee_id="attendee-1",
        payload={"attendance_type_id": "standard"},
    )

    assert status == 200
    assert response["status"] == "registered"


def test_at_uc24_03_registration_closed() -> None:
    attendance_type = AttendanceType(id="standard", name="Standard")
    registration_repo = StubRegistrationRepository()
    service = ConferenceRegistrationService(
        StubRegistrationWindow(is_open=False),
        StubAttendanceTypeRepository({"standard": attendance_type}),
        registration_repo,
        StubPaymentPolicy(required=False),
        StubPaymentService(),
    )

    status, response = register_for_conference(
        service,
        attendee_id="attendee-1",
        payload={"attendance_type_id": "standard"},
    )

    assert status == 403
    assert response["error"] == REGISTRATION_CLOSED_MESSAGE
    assert registration_repo.saved is None


def test_at_uc24_04_invalid_or_unavailable_attendance_type() -> None:
    valid_type = AttendanceType(id="standard", name="Standard")
    invalid_type = AttendanceType(
        id="vip", name="VIP", availability_status="unavailable"
    )
    registration_repo = StubRegistrationRepository()
    service = ConferenceRegistrationService(
        StubRegistrationWindow(is_open=True),
        StubAttendanceTypeRepository({"standard": valid_type, "vip": invalid_type}),
        registration_repo,
        StubPaymentPolicy(required=False),
        StubPaymentService(),
    )

    status, response = register_for_conference(
        service,
        attendee_id="attendee-1",
        payload={"attendance_type_id": "vip"},
    )

    assert status == 400
    assert response["error"] == ATTENDANCE_TYPE_UNAVAILABLE_MESSAGE
    assert registration_repo.saved is None

    status, response = register_for_conference(
        service,
        attendee_id="attendee-1",
        payload={"attendance_type_id": "standard"},
    )

    assert status == 200
    assert response["status"] == "registered"
    assert registration_repo.saved is not None


def test_at_uc24_05_payment_service_unavailable() -> None:
    attendance_type = AttendanceType(id="standard", name="Standard")
    registration_repo = StubRegistrationRepository()
    service = ConferenceRegistrationService(
        StubRegistrationWindow(is_open=True),
        StubAttendanceTypeRepository({"standard": attendance_type}),
        registration_repo,
        StubPaymentPolicy(required=True),
        StubPaymentService(fail=True),
    )

    status, response = register_for_conference(
        service,
        attendee_id="attendee-1",
        payload={"attendance_type_id": "standard"},
    )

    assert status == 200
    assert response["status"] == "pending_unpaid"
    assert response["payment_required"] is True
    assert response["message"] == PAYMENT_UNAVAILABLE_MESSAGE
    assert response["payment_error"] is True
    assert registration_repo.saved is not None


def test_at_uc24_06_fail_to_record_registration() -> None:
    attendance_type = AttendanceType(id="standard", name="Standard")
    registration_repo = StubRegistrationRepository(fail_save=True)
    service = ConferenceRegistrationService(
        StubRegistrationWindow(is_open=True),
        StubAttendanceTypeRepository({"standard": attendance_type}),
        registration_repo,
        StubPaymentPolicy(required=False),
        StubPaymentService(),
    )

    status, response = register_for_conference(
        service,
        attendee_id="attendee-1",
        payload={"attendance_type_id": "standard"},
    )

    assert status == 500
    assert response["error"] == REGISTRATION_FAILED_MESSAGE
    assert registration_repo.saved is None


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
    def __init__(self, *, fail_save: bool = False) -> None:
        self._fail_save = fail_save
        self.saved: AttendeeRegistration | None = None

    def create_registration(self, registration: AttendeeRegistration) -> AttendeeRegistration:
        if self._fail_save:
            raise RegistrationStorageError("storage failure")
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
