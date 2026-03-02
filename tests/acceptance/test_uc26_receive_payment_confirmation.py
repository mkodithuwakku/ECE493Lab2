from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.conference_confirmation import get_payment_confirmation, get_receipt
from models.attendee_registration import AttendeeRegistration
from models.conference_ticket import ConferenceTicket
from models.payment_confirmation import PaymentConfirmation
from models.receipt import Receipt
from services.conference_confirmation_service import (
    CONFIRMATION_NOT_PAID_MESSAGE,
    CONFIRMATION_RETRIEVAL_ERROR_MESSAGE,
    ConferenceConfirmationService,
    ConfirmationRetrievalError,
)


def test_at_uc26_01_view_confirmation_successfully() -> None:
    registration = AttendeeRegistration(
        registration_id="reg-1",
        attendee_id="attendee-1",
        attendance_type_id="standard",
        status="paid_confirmed",
    )
    confirmation = PaymentConfirmation(
        confirmation_id="conf-1",
        registration_id="reg-1",
        amount=150.0,
        currency="USD",
        transaction_reference_id="txn-1",
        confirmed_at="2026-03-10T10:00:00",
    )
    ticket = ConferenceTicket(
        ticket_id="ticket-1",
        registration_id="reg-1",
        ticket_code="TICKET-123",
        issued_at="2026-03-10T10:01:00",
    )
    service = build_service(registration, confirmation, ticket, receipt=None, receipt_enabled=False)

    status, response = get_payment_confirmation(service, "attendee-1")

    assert status == 200
    assert response["status"] == "paid_confirmed"
    assert response["amount"] == 150.0
    assert response["ticket_code"] == "TICKET-123"

    status, response = get_payment_confirmation(service, "attendee-1")
    assert status == 200


def test_at_uc26_02_view_receipt_when_supported() -> None:
    registration = AttendeeRegistration(
        registration_id="reg-1",
        attendee_id="attendee-1",
        attendance_type_id="standard",
        status="paid_confirmed",
    )
    receipt = Receipt(
        receipt_id="receipt-1",
        registration_id="reg-1",
        receipt_number="R-1001",
        generated_at="2026-03-10T10:02:00",
    )
    service = build_service(
        registration,
        confirmation=None,
        ticket=None,
        receipt=receipt,
        receipt_enabled=True,
    )

    status, response = get_receipt(service, "attendee-1")

    assert status == 200
    assert response["receipt_number"] == "R-1001"


def test_at_uc26_03_attendee_not_logged_in_then_logs_in() -> None:
    registration = AttendeeRegistration(
        registration_id="reg-1",
        attendee_id="attendee-1",
        attendance_type_id="standard",
        status="paid_confirmed",
    )
    service = build_service(registration, confirmation=None, ticket=None, receipt=None, receipt_enabled=False)

    status, response = get_payment_confirmation(service, None)

    assert status == 401
    assert response["redirect_to"] == "/login"

    status, response = get_payment_confirmation(service, "attendee-1")

    assert status == 200


def test_at_uc26_04_registration_not_paid_or_missing() -> None:
    registration = AttendeeRegistration(
        registration_id="reg-1",
        attendee_id="attendee-1",
        attendance_type_id="standard",
        status="pending_unpaid",
    )
    service = build_service(registration, confirmation=None, ticket=None, receipt=None, receipt_enabled=False)

    status, response = get_payment_confirmation(service, "attendee-1")

    assert status == 400
    assert response["error"] == CONFIRMATION_NOT_PAID_MESSAGE


def test_at_uc26_05_access_another_users_receipt_blocked() -> None:
    registration_a = AttendeeRegistration(
        registration_id="reg-1",
        attendee_id="attendee-a",
        attendance_type_id="standard",
        status="paid_confirmed",
    )
    registration_b = AttendeeRegistration(
        registration_id="reg-2",
        attendee_id="attendee-b",
        attendance_type_id="standard",
        status="paid_confirmed",
    )
    receipt_b = Receipt(
        receipt_id="receipt-2",
        registration_id="reg-2",
        receipt_number="R-2002",
        generated_at="2026-03-10T10:02:00",
    )
    service = build_service(
        registration_a,
        confirmation=None,
        ticket=None,
        receipt=receipt_b,
        receipt_enabled=True,
        other_registrations={"reg-2": registration_b},
    )

    status, response = get_receipt(service, "attendee-a", registration_id="reg-2")

    assert status == 403
    assert response["redirect_to"] == "/registration"


def test_at_uc26_06_retrieval_error() -> None:
    registration = AttendeeRegistration(
        registration_id="reg-1",
        attendee_id="attendee-1",
        attendance_type_id="standard",
        status="paid_confirmed",
    )
    service = build_service(
        registration,
        confirmation=None,
        ticket=None,
        receipt=None,
        receipt_enabled=True,
        fail_confirmation=True,
    )

    status, response = get_payment_confirmation(service, "attendee-1")

    assert status == 503
    assert response["error"] == CONFIRMATION_RETRIEVAL_ERROR_MESSAGE


class StubRegistrationRepository:
    def __init__(
        self,
        registration: AttendeeRegistration | None,
        other: dict[str, AttendeeRegistration] | None = None,
    ) -> None:
        self._registration = registration
        self._other = other or {}

    def get_registration(self, attendee_id: str) -> AttendeeRegistration | None:
        if self._registration and self._registration.attendee_id == attendee_id:
            return self._registration
        for registration in self._other.values():
            if registration.attendee_id == attendee_id:
                return registration
        return None

    def get_registration_by_id(self, registration_id: str) -> AttendeeRegistration | None:
        if self._registration and self._registration.registration_id == registration_id:
            return self._registration
        return self._other.get(registration_id)


class StubConfirmationRepository:
    def __init__(self, confirmation: PaymentConfirmation | None, *, fail: bool = False) -> None:
        self._confirmation = confirmation
        self._fail = fail

    def get_confirmation(self, registration_id: str) -> PaymentConfirmation | None:
        if self._fail:
            raise ConfirmationRetrievalError("fail")
        if self._confirmation and self._confirmation.registration_id == registration_id:
            return self._confirmation
        return None


class StubTicketRepository:
    def __init__(self, ticket: ConferenceTicket | None) -> None:
        self._ticket = ticket

    def get_ticket(self, registration_id: str) -> ConferenceTicket | None:
        if self._ticket and self._ticket.registration_id == registration_id:
            return self._ticket
        return None


class StubReceiptRepository:
    def __init__(self, receipt: Receipt | None) -> None:
        self._receipt = receipt

    def get_receipt(self, registration_id: str) -> Receipt | None:
        if self._receipt and self._receipt.registration_id == registration_id:
            return self._receipt
        return None


def build_service(
    registration: AttendeeRegistration | None,
    confirmation: PaymentConfirmation | None,
    ticket: ConferenceTicket | None,
    receipt: Receipt | None,
    *,
    receipt_enabled: bool,
    other_registrations: dict[str, AttendeeRegistration] | None = None,
    fail_confirmation: bool = False,
) -> ConferenceConfirmationService:
    return ConferenceConfirmationService(
        StubRegistrationRepository(registration, other_registrations),
        StubConfirmationRepository(confirmation, fail=fail_confirmation),
        StubTicketRepository(ticket),
        StubReceiptRepository(receipt),
        receipt_enabled=receipt_enabled,
    )
