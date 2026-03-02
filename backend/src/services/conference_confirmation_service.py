from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from models.attendee_registration import AttendeeRegistration
from models.conference_ticket import ConferenceTicket
from models.payment_confirmation import PaymentConfirmation
from models.receipt import Receipt
from services.conference_confirmation_logger import (
    ConferenceConfirmationLogContext,
    log_conference_confirmation_event,
)

CONFIRMATION_UNAUTHENTICATED_MESSAGE = "Please log in to view confirmation."
CONFIRMATION_NOT_PAID_MESSAGE = "Registration payment is not confirmed."
CONFIRMATION_FORBIDDEN_MESSAGE = "You are not authorized to access this confirmation."
CONFIRMATION_RETRIEVAL_ERROR_MESSAGE = "Confirmation details are temporarily unavailable."
RECEIPT_NOT_AVAILABLE_MESSAGE = "Receipt is not available."
LOGIN_REDIRECT = "/login"
SAFE_REDIRECT = "/registration"


class RegistrationRetrievalError(RuntimeError):
    pass


class ConfirmationRetrievalError(RuntimeError):
    pass


class TicketRetrievalError(RuntimeError):
    pass


class ReceiptRetrievalError(RuntimeError):
    pass


class RegistrationRepository(Protocol):
    def get_registration(self, attendee_id: str) -> AttendeeRegistration | None:
        ...

    def get_registration_by_id(self, registration_id: str) -> AttendeeRegistration | None:
        ...


class ConfirmationRepository(Protocol):
    def get_confirmation(self, registration_id: str) -> PaymentConfirmation | None:
        ...


class TicketRepository(Protocol):
    def get_ticket(self, registration_id: str) -> ConferenceTicket | None:
        ...


class ReceiptRepository(Protocol):
    def get_receipt(self, registration_id: str) -> Receipt | None:
        ...


@dataclass(frozen=True)
class ConfirmationResult:
    status: str
    registration: AttendeeRegistration | None = None
    confirmation: PaymentConfirmation | None = None
    ticket: ConferenceTicket | None = None
    message: str | None = None
    redirect_to: str | None = None

    @classmethod
    def unauthenticated(cls) -> "ConfirmationResult":
        return cls(
            status="unauthenticated",
            message=CONFIRMATION_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def forbidden(cls) -> "ConfirmationResult":
        return cls(
            status="forbidden",
            message=CONFIRMATION_FORBIDDEN_MESSAGE,
            redirect_to=SAFE_REDIRECT,
        )

    @classmethod
    def not_paid(cls) -> "ConfirmationResult":
        return cls(status="not_paid", message=CONFIRMATION_NOT_PAID_MESSAGE)

    @classmethod
    def retrieval_error(cls) -> "ConfirmationResult":
        return cls(status="error", message=CONFIRMATION_RETRIEVAL_ERROR_MESSAGE)

    @classmethod
    def ok(
        cls,
        registration: AttendeeRegistration,
        confirmation: PaymentConfirmation | None,
        ticket: ConferenceTicket | None,
    ) -> "ConfirmationResult":
        return cls(
            status="ok",
            registration=registration,
            confirmation=confirmation,
            ticket=ticket,
        )


@dataclass(frozen=True)
class ReceiptResult:
    status: str
    receipt: Receipt | None = None
    message: str | None = None
    redirect_to: str | None = None

    @classmethod
    def unauthenticated(cls) -> "ReceiptResult":
        return cls(
            status="unauthenticated",
            message=CONFIRMATION_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def forbidden(cls) -> "ReceiptResult":
        return cls(
            status="forbidden",
            message=CONFIRMATION_FORBIDDEN_MESSAGE,
            redirect_to=SAFE_REDIRECT,
        )

    @classmethod
    def not_paid(cls) -> "ReceiptResult":
        return cls(status="not_paid", message=CONFIRMATION_NOT_PAID_MESSAGE)

    @classmethod
    def not_available(cls) -> "ReceiptResult":
        return cls(status="not_available", message=RECEIPT_NOT_AVAILABLE_MESSAGE)

    @classmethod
    def retrieval_error(cls) -> "ReceiptResult":
        return cls(status="error", message=CONFIRMATION_RETRIEVAL_ERROR_MESSAGE)

    @classmethod
    def ok(cls, receipt: Receipt) -> "ReceiptResult":
        return cls(status="ok", receipt=receipt)


class ConferenceConfirmationService:
    def __init__(
        self,
        registration_repository: RegistrationRepository,
        confirmation_repository: ConfirmationRepository,
        ticket_repository: TicketRepository,
        receipt_repository: ReceiptRepository,
        *,
        receipt_enabled: bool = False,
    ) -> None:
        self._registration_repository = registration_repository
        self._confirmation_repository = confirmation_repository
        self._ticket_repository = ticket_repository
        self._receipt_repository = receipt_repository
        self._receipt_enabled = receipt_enabled

    def get_confirmation(
        self,
        attendee_id: str | None,
        registration_id: str | None = None,
        trace_id: Optional[str] = None,
    ) -> ConfirmationResult:
        context = ConferenceConfirmationLogContext(attendee_id=attendee_id, trace_id=trace_id)

        if not attendee_id:
            log_conference_confirmation_event("confirmation_unauthenticated", context)
            return ConfirmationResult.unauthenticated()

        try:
            registration = (
                self._registration_repository.get_registration_by_id(registration_id)
                if registration_id
                else self._registration_repository.get_registration(attendee_id)
            )
        except RegistrationRetrievalError:
            log_conference_confirmation_event(
                "confirmation_registration_error", context, CONFIRMATION_RETRIEVAL_ERROR_MESSAGE
            )
            return ConfirmationResult.retrieval_error()
        except Exception:
            log_conference_confirmation_event(
                "confirmation_registration_error", context, CONFIRMATION_RETRIEVAL_ERROR_MESSAGE
            )
            return ConfirmationResult.retrieval_error()

        if registration is None:
            return ConfirmationResult.not_paid()

        if registration.attendee_id != attendee_id:
            log_conference_confirmation_event("confirmation_forbidden", context)
            return ConfirmationResult.forbidden()

        if registration.status != "paid_confirmed":
            return ConfirmationResult.not_paid()

        try:
            confirmation = self._confirmation_repository.get_confirmation(registration.registration_id)
            ticket = self._ticket_repository.get_ticket(registration.registration_id)
        except (ConfirmationRetrievalError, TicketRetrievalError):
            log_conference_confirmation_event(
                "confirmation_retrieval_error", context, CONFIRMATION_RETRIEVAL_ERROR_MESSAGE
            )
            return ConfirmationResult.retrieval_error()
        except Exception:
            log_conference_confirmation_event(
                "confirmation_retrieval_error", context, CONFIRMATION_RETRIEVAL_ERROR_MESSAGE
            )
            return ConfirmationResult.retrieval_error()

        log_conference_confirmation_event("confirmation_viewed", context)
        return ConfirmationResult.ok(registration, confirmation, ticket)

    def get_receipt(
        self,
        attendee_id: str | None,
        registration_id: str | None = None,
        trace_id: Optional[str] = None,
    ) -> ReceiptResult:
        context = ConferenceConfirmationLogContext(attendee_id=attendee_id, trace_id=trace_id)

        if not attendee_id:
            log_conference_confirmation_event("receipt_unauthenticated", context)
            return ReceiptResult.unauthenticated()

        try:
            registration = (
                self._registration_repository.get_registration_by_id(registration_id)
                if registration_id
                else self._registration_repository.get_registration(attendee_id)
            )
        except RegistrationRetrievalError:
            log_conference_confirmation_event(
                "receipt_registration_error", context, CONFIRMATION_RETRIEVAL_ERROR_MESSAGE
            )
            return ReceiptResult.retrieval_error()
        except Exception:
            log_conference_confirmation_event(
                "receipt_registration_error", context, CONFIRMATION_RETRIEVAL_ERROR_MESSAGE
            )
            return ReceiptResult.retrieval_error()

        if registration is None:
            return ReceiptResult.not_paid()

        if registration.attendee_id != attendee_id:
            log_conference_confirmation_event("receipt_forbidden", context)
            return ReceiptResult.forbidden()

        if registration.status != "paid_confirmed":
            return ReceiptResult.not_paid()

        if not self._receipt_enabled:
            return ReceiptResult.not_available()

        try:
            receipt = self._receipt_repository.get_receipt(registration.registration_id)
        except ReceiptRetrievalError:
            log_conference_confirmation_event(
                "receipt_retrieval_error", context, CONFIRMATION_RETRIEVAL_ERROR_MESSAGE
            )
            return ReceiptResult.retrieval_error()
        except Exception:
            log_conference_confirmation_event(
                "receipt_retrieval_error", context, CONFIRMATION_RETRIEVAL_ERROR_MESSAGE
            )
            return ReceiptResult.retrieval_error()

        if receipt is None:
            return ReceiptResult.not_available()

        log_conference_confirmation_event("receipt_viewed", context)
        return ReceiptResult.ok(receipt)
