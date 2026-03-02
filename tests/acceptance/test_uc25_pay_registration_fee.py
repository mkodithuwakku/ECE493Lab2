from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.conference_payment import get_payment_status, pay_registration_fee
from models.attendee_registration import AttendeeRegistration
from models.payment_details import PaymentDetails
from models.payment_record import PaymentRecord
from services.conference_payment_service import (
    NO_PENDING_PAYMENT_MESSAGE,
    PAYMENT_ALREADY_COMPLETED_MESSAGE,
    PAYMENT_CANCELED_MESSAGE,
    PAYMENT_DECLINED_MESSAGE,
    PAYMENT_RECORD_FAILED_MESSAGE,
    PAYMENT_SUCCESS_MESSAGE,
    PAYMENT_UNAVAILABLE_MESSAGE,
    ConferencePaymentService,
    PaymentGatewayResult,
    PaymentGatewayUnavailable,
    PaymentRecordingError,
)


def test_at_uc25_01_pay_registration_successfully() -> None:
    registration = AttendeeRegistration(
        registration_id="reg-1",
        attendee_id="attendee-1",
        attendance_type_id="standard",
        status="pending_unpaid",
    )
    service = build_service(registration, gateway_mode="success")

    status, response = pay_registration_fee(service, "attendee-1", payload={"card": "ok"})

    assert status == 200
    assert response["status"] == "successful"
    assert response["message"] == PAYMENT_SUCCESS_MESSAGE
    assert response["amount"] == 150.0
    assert response["currency"] == "USD"
    assert service._registration_repository.registration.status == "paid_confirmed"

    status, response = get_payment_status(service, "attendee-1")

    assert status == 200
    assert response["registration_status"] == "paid_confirmed"
    assert response["payment_status"] == "successful"


def test_at_uc25_02_attendee_not_logged_in_then_logs_in() -> None:
    registration = AttendeeRegistration(
        registration_id="reg-1",
        attendee_id="attendee-1",
        attendance_type_id="standard",
        status="pending_unpaid",
    )
    service = build_service(registration, gateway_mode="success")

    status, response = pay_registration_fee(service, None, payload=None)

    assert status == 401
    assert response["redirect_to"] == "/login"

    status, response = pay_registration_fee(service, "attendee-1", payload={})

    assert status == 200
    assert response["status"] == "successful"


def test_at_uc25_03_no_pending_registration_nothing_to_pay() -> None:
    service = build_service(None, gateway_mode="success")

    status, response = pay_registration_fee(service, "attendee-1", payload=None)

    assert status == 409
    assert response["error"] == NO_PENDING_PAYMENT_MESSAGE


def test_at_uc25_04_payment_declined_by_gateway() -> None:
    registration = AttendeeRegistration(
        registration_id="reg-1",
        attendee_id="attendee-1",
        attendance_type_id="standard",
        status="pending_unpaid",
    )
    service = build_service(registration, gateway_mode="declined")

    status, response = pay_registration_fee(service, "attendee-1", payload=None)

    assert status == 402
    assert response["error"] == PAYMENT_DECLINED_MESSAGE
    assert service._registration_repository.registration.status == "pending_unpaid"


def test_at_uc25_05_payment_canceled_by_attendee() -> None:
    registration = AttendeeRegistration(
        registration_id="reg-1",
        attendee_id="attendee-1",
        attendance_type_id="standard",
        status="pending_unpaid",
    )
    service = build_service(registration, gateway_mode="canceled")

    status, response = pay_registration_fee(service, "attendee-1", payload=None)

    assert status == 402
    assert response["error"] == PAYMENT_CANCELED_MESSAGE
    assert service._registration_repository.registration.status == "pending_unpaid"


def test_at_uc25_06_payment_gateway_unavailable() -> None:
    registration = AttendeeRegistration(
        registration_id="reg-1",
        attendee_id="attendee-1",
        attendance_type_id="standard",
        status="pending_unpaid",
    )
    service = build_service(registration, gateway_mode="unavailable")

    status, response = pay_registration_fee(service, "attendee-1", payload=None)

    assert status == 503
    assert response["error"] == PAYMENT_UNAVAILABLE_MESSAGE
    assert service._registration_repository.registration.status == "pending_unpaid"


def test_at_uc25_07_duplicate_payment_attempt_already_paid() -> None:
    registration = AttendeeRegistration(
        registration_id="reg-1",
        attendee_id="attendee-1",
        attendance_type_id="standard",
        status="paid_confirmed",
    )
    service = build_service(registration, gateway_mode="success")

    status, response = pay_registration_fee(service, "attendee-1", payload=None)

    assert status == 409
    assert response["error"] == PAYMENT_ALREADY_COMPLETED_MESSAGE


def test_at_uc25_08_fail_to_record_successful_payment() -> None:
    registration = AttendeeRegistration(
        registration_id="reg-1",
        attendee_id="attendee-1",
        attendance_type_id="standard",
        status="pending_unpaid",
    )
    service = build_service(registration, gateway_mode="success", record_fail=True)

    status, response = pay_registration_fee(service, "attendee-1", payload=None)

    assert status == 500
    assert response["error"] == PAYMENT_RECORD_FAILED_MESSAGE
    assert service._registration_repository.registration.status == "pending_unpaid"


class StubRegistrationRepository:
    def __init__(self, registration: AttendeeRegistration | None) -> None:
        self.registration = registration

    def get_registration(self, attendee_id: str) -> AttendeeRegistration | None:
        if self.registration and self.registration.attendee_id == attendee_id:
            return self.registration
        return None

    def update_status(self, registration_id: str, status: str) -> AttendeeRegistration:
        assert self.registration is not None
        self.registration = AttendeeRegistration(
            registration_id=self.registration.registration_id,
            attendee_id=self.registration.attendee_id,
            attendance_type_id=self.registration.attendance_type_id,
            status=status,
        )
        return self.registration


class StubPaymentDetailsRepository:
    def get_payment_details(self, registration: AttendeeRegistration) -> PaymentDetails:
        return PaymentDetails(amount=150.0, currency="USD", line_items=["Registration fee"])


class StubPaymentGateway:
    def __init__(self, mode: str) -> None:
        self._mode = mode

    def submit_payment(self, registration: AttendeeRegistration, payment_details: PaymentDetails, payload: dict | None) -> PaymentGatewayResult:
        if self._mode == "unavailable":
            raise PaymentGatewayUnavailable("gateway unavailable")
        if self._mode in {"declined", "canceled", "unavailable"}:
            return PaymentGatewayResult(status=self._mode)
        return PaymentGatewayResult(status="success", transaction_id="txn-1", receipt="rcpt-1")


class StubPaymentRepository:
    def __init__(self, *, fail_record: bool = False) -> None:
        self._fail_record = fail_record
        self.latest: PaymentRecord | None = None

    def record_payment(self, record):
        if self._fail_record:
            raise PaymentRecordingError("record failed")
        self.latest = record
        return record

    def get_latest_payment(self, registration_id: str):
        return self.latest


def build_service(
    registration: AttendeeRegistration | None,
    *,
    gateway_mode: str,
    record_fail: bool = False,
) -> ConferencePaymentService:
    return ConferencePaymentService(
        StubRegistrationRepository(registration),
        StubPaymentDetailsRepository(),
        StubPaymentGateway(gateway_mode),
        StubPaymentRepository(fail_record=record_fail),
    )
