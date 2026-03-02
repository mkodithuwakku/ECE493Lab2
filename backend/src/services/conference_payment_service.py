from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from models.attendee_registration import AttendeeRegistration
from models.payment_details import PaymentDetails
from models.payment_record import PaymentRecord
from services.conference_payment_logger import (
    ConferencePaymentLogContext,
    log_conference_payment_event,
)

PAYMENT_UNAUTHENTICATED_MESSAGE = "Please log in to pay the registration fee."
NO_PENDING_PAYMENT_MESSAGE = "No payment is required for your registration."
PAYMENT_ALREADY_COMPLETED_MESSAGE = "Payment has already been completed."
PAYMENT_DECLINED_MESSAGE = "Payment was declined. Please retry."
PAYMENT_CANCELED_MESSAGE = "Payment was canceled."
PAYMENT_UNAVAILABLE_MESSAGE = "Payment service is unavailable. Please try again later."
PAYMENT_SUCCESS_MESSAGE = "Payment completed successfully."
PAYMENT_RECORD_FAILED_MESSAGE = "Payment was successful, but could not be recorded."
LOGIN_REDIRECT = "/login"


class RegistrationRetrievalError(RuntimeError):
    pass


class PaymentGatewayUnavailable(RuntimeError):
    pass


class PaymentRecordingError(RuntimeError):
    pass


class RegistrationRepository(Protocol):
    def get_registration(self, attendee_id: str) -> AttendeeRegistration | None:
        ...

    def update_status(self, registration_id: str, status: str) -> AttendeeRegistration:
        ...


class PaymentDetailsRepository(Protocol):
    def get_payment_details(self, registration: AttendeeRegistration) -> PaymentDetails:
        ...


class PaymentGateway(Protocol):
    def submit_payment(
        self, registration: AttendeeRegistration, payment_details: PaymentDetails, payload: dict | None
    ) -> "PaymentGatewayResult":
        ...


class PaymentRepository(Protocol):
    def record_payment(self, record: PaymentRecord) -> PaymentRecord:
        ...

    def get_latest_payment(self, registration_id: str) -> PaymentRecord | None:
        ...


@dataclass(frozen=True)
class PaymentGatewayResult:
    status: str
    transaction_id: str | None = None
    receipt: str | None = None


@dataclass(frozen=True)
class PaymentResult:
    status: str
    registration: AttendeeRegistration | None = None
    payment: PaymentRecord | None = None
    payment_details: PaymentDetails | None = None
    message: str | None = None
    redirect_to: str | None = None

    @classmethod
    def unauthenticated(cls) -> "PaymentResult":
        return cls(
            status="unauthenticated",
            message=PAYMENT_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def no_pending(cls) -> "PaymentResult":
        return cls(status="no_pending", message=NO_PENDING_PAYMENT_MESSAGE)

    @classmethod
    def already_paid(cls) -> "PaymentResult":
        return cls(status="already_paid", message=PAYMENT_ALREADY_COMPLETED_MESSAGE)

    @classmethod
    def declined(cls) -> "PaymentResult":
        return cls(status="declined", message=PAYMENT_DECLINED_MESSAGE)

    @classmethod
    def canceled(cls) -> "PaymentResult":
        return cls(status="canceled", message=PAYMENT_CANCELED_MESSAGE)

    @classmethod
    def unavailable(cls) -> "PaymentResult":
        return cls(status="unavailable", message=PAYMENT_UNAVAILABLE_MESSAGE)

    @classmethod
    def record_failed(cls) -> "PaymentResult":
        return cls(status="record_failed", message=PAYMENT_RECORD_FAILED_MESSAGE)

    @classmethod
    def success(
        cls,
        registration: AttendeeRegistration,
        payment: PaymentRecord,
        payment_details: PaymentDetails,
    ) -> "PaymentResult":
        return cls(
            status="success",
            registration=registration,
            payment=payment,
            payment_details=payment_details,
            message=PAYMENT_SUCCESS_MESSAGE,
        )


@dataclass(frozen=True)
class PaymentStatusResult:
    status: str
    registration: AttendeeRegistration | None = None
    payment: PaymentRecord | None = None
    message: str | None = None
    redirect_to: str | None = None

    @classmethod
    def unauthenticated(cls) -> "PaymentStatusResult":
        return cls(
            status="unauthenticated",
            message=PAYMENT_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def found(cls, registration: AttendeeRegistration, payment: PaymentRecord | None) -> "PaymentStatusResult":
        return cls(status="found", registration=registration, payment=payment)


class ConferencePaymentService:
    def __init__(
        self,
        registration_repository: RegistrationRepository,
        payment_details_repository: PaymentDetailsRepository,
        payment_gateway: PaymentGateway,
        payment_repository: PaymentRepository,
    ) -> None:
        self._registration_repository = registration_repository
        self._payment_details_repository = payment_details_repository
        self._payment_gateway = payment_gateway
        self._payment_repository = payment_repository

    def pay_registration_fee(
        self,
        attendee_id: str | None,
        payload: dict | None,
        trace_id: Optional[str] = None,
    ) -> PaymentResult:
        context = ConferencePaymentLogContext(attendee_id=attendee_id, trace_id=trace_id)

        if not attendee_id:
            log_conference_payment_event("payment_unauthenticated", context)
            return PaymentResult.unauthenticated()

        try:
            registration = self._registration_repository.get_registration(attendee_id)
        except RegistrationRetrievalError:
            log_conference_payment_event("payment_registration_error", context)
            return PaymentResult.no_pending()
        except Exception:
            log_conference_payment_event("payment_registration_error", context)
            return PaymentResult.no_pending()

        if registration is None:
            return PaymentResult.no_pending()

        if registration.status == "paid_confirmed":
            return PaymentResult.already_paid()

        if registration.status != "pending_unpaid":
            return PaymentResult.no_pending()

        payment_details = self._payment_details_repository.get_payment_details(registration)

        try:
            gateway_result = self._payment_gateway.submit_payment(
                registration, payment_details, payload
            )
        except PaymentGatewayUnavailable:
            log_conference_payment_event("payment_gateway_unavailable", context)
            return PaymentResult.unavailable()
        except Exception:
            log_conference_payment_event("payment_gateway_unavailable", context)
            return PaymentResult.unavailable()

        if gateway_result.status == "declined":
            return PaymentResult.declined()
        if gateway_result.status == "canceled":
            return PaymentResult.canceled()
        if gateway_result.status == "unavailable":
            return PaymentResult.unavailable()

        payment_record = PaymentRecord(
            payment_id=f"pay-{registration.registration_id}",
            registration_id=registration.registration_id,
            status="successful",
            transaction_id=gateway_result.transaction_id,
            receipt=gateway_result.receipt,
        )

        try:
            recorded = self._payment_repository.record_payment(payment_record)
            updated = self._registration_repository.update_status(
                registration.registration_id, "paid_confirmed"
            )
        except PaymentRecordingError:
            log_conference_payment_event("payment_record_failed", context)
            return PaymentResult.record_failed()
        except Exception:
            log_conference_payment_event("payment_record_failed", context)
            return PaymentResult.record_failed()

        log_conference_payment_event("payment_success", context)
        return PaymentResult.success(updated, recorded, payment_details)

    def get_payment_status(
        self,
        attendee_id: str | None,
        trace_id: Optional[str] = None,
    ) -> PaymentStatusResult:
        context = ConferencePaymentLogContext(attendee_id=attendee_id, trace_id=trace_id)

        if not attendee_id:
            log_conference_payment_event("payment_unauthenticated", context)
            return PaymentStatusResult.unauthenticated()

        registration = self._registration_repository.get_registration(attendee_id)
        if registration is None:
            return PaymentStatusResult.found(
                AttendeeRegistration(
                    registration_id="unknown",
                    attendee_id=attendee_id,
                    attendance_type_id=None,
                    status="pending_unpaid",
                ),
                None,
            )

        payment = self._payment_repository.get_latest_payment(registration.registration_id)
        return PaymentStatusResult.found(registration, payment)
