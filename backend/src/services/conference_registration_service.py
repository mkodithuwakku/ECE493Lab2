from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from models.attendance_type import AttendanceType
from models.attendee_registration import AttendeeRegistration
from services.conference_registration_logger import (
    ConferenceRegistrationLogContext,
    log_conference_registration_event,
)

REGISTRATION_UNAUTHENTICATED_MESSAGE = "Please log in to register for the conference."
REGISTRATION_CLOSED_MESSAGE = "Registration is closed."
ATTENDANCE_TYPE_UNAVAILABLE_MESSAGE = "Selected attendance type is unavailable."
REGISTRATION_SUCCESS_MESSAGE = "Conference registration completed successfully."
PAYMENT_REQUIRED_MESSAGE = "Registration saved. Please proceed to payment."
PAYMENT_UNAVAILABLE_MESSAGE = "Payment could not be completed at this time."
REGISTRATION_FAILED_MESSAGE = "Registration could not be saved."
LOGIN_REDIRECT = "/login"


class RegistrationWindowError(RuntimeError):
    pass


class RegistrationStorageError(RuntimeError):
    pass


class PaymentServiceUnavailable(RuntimeError):
    pass


class RegistrationWindowRepository(Protocol):
    def is_open(self) -> bool:
        ...


class AttendanceTypeRepository(Protocol):
    def get_attendance_type(self, attendance_type_id: str) -> AttendanceType | None:
        ...


class RegistrationRepository(Protocol):
    def create_registration(self, registration: AttendeeRegistration) -> AttendeeRegistration:
        ...

    def get_registration(self, attendee_id: str) -> AttendeeRegistration | None:
        ...


class PaymentPolicy(Protocol):
    def is_payment_required(self, attendance_type_id: str | None) -> bool:
        ...


class PaymentService(Protocol):
    def start_payment(self, registration: AttendeeRegistration) -> None:
        ...


@dataclass(frozen=True)
class RegistrationResult:
    status: str
    registration: AttendeeRegistration | None = None
    message: str | None = None
    payment_required: bool = False
    redirect_to: str | None = None

    @classmethod
    def unauthenticated(cls) -> "RegistrationResult":
        return cls(
            status="unauthenticated",
            message=REGISTRATION_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def closed(cls) -> "RegistrationResult":
        return cls(status="closed", message=REGISTRATION_CLOSED_MESSAGE)

    @classmethod
    def invalid_type(cls) -> "RegistrationResult":
        return cls(status="invalid_type", message=ATTENDANCE_TYPE_UNAVAILABLE_MESSAGE)

    @classmethod
    def storage_error(cls) -> "RegistrationResult":
        return cls(status="storage_error", message=REGISTRATION_FAILED_MESSAGE)

    @classmethod
    def registered(cls, registration: AttendeeRegistration) -> "RegistrationResult":
        return cls(
            status="registered",
            registration=registration,
            message=REGISTRATION_SUCCESS_MESSAGE,
            payment_required=False,
        )

    @classmethod
    def pending_payment(cls, registration: AttendeeRegistration) -> "RegistrationResult":
        return cls(
            status="pending_unpaid",
            registration=registration,
            message=PAYMENT_REQUIRED_MESSAGE,
            payment_required=True,
        )

    @classmethod
    def payment_unavailable(cls, registration: AttendeeRegistration) -> "RegistrationResult":
        return cls(
            status="payment_unavailable",
            registration=registration,
            message=PAYMENT_UNAVAILABLE_MESSAGE,
            payment_required=True,
        )


@dataclass(frozen=True)
class RegistrationStatusResult:
    status: str
    registration: AttendeeRegistration | None = None
    message: str | None = None
    redirect_to: str | None = None

    @classmethod
    def unauthenticated(cls) -> "RegistrationStatusResult":
        return cls(
            status="unauthenticated",
            message=REGISTRATION_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def found(cls, registration: AttendeeRegistration) -> "RegistrationStatusResult":
        return cls(status="found", registration=registration)

    @classmethod
    def not_found(cls) -> "RegistrationStatusResult":
        return cls(status="not_found", message="Registration not found.")


class ConferenceRegistrationService:
    def __init__(
        self,
        window_repository: RegistrationWindowRepository,
        attendance_repository: AttendanceTypeRepository,
        registration_repository: RegistrationRepository,
        payment_policy: PaymentPolicy,
        payment_service: PaymentService,
    ) -> None:
        self._window_repository = window_repository
        self._attendance_repository = attendance_repository
        self._registration_repository = registration_repository
        self._payment_policy = payment_policy
        self._payment_service = payment_service

    def register_attendee(
        self,
        attendee_id: str | None,
        attendance_type_id: str | None,
        trace_id: Optional[str] = None,
    ) -> RegistrationResult:
        context = ConferenceRegistrationLogContext(attendee_id=attendee_id, trace_id=trace_id)

        if not attendee_id:
            log_conference_registration_event("registration_unauthenticated", context)
            return RegistrationResult.unauthenticated()

        try:
            if not self._window_repository.is_open():
                log_conference_registration_event(
                    "registration_closed",
                    context,
                    REGISTRATION_CLOSED_MESSAGE,
                )
                return RegistrationResult.closed()
        except RegistrationWindowError:
            log_conference_registration_event(
                "registration_window_error",
                context,
                REGISTRATION_FAILED_MESSAGE,
            )
            return RegistrationResult.storage_error()
        except Exception:
            log_conference_registration_event(
                "registration_window_error",
                context,
                REGISTRATION_FAILED_MESSAGE,
            )
            return RegistrationResult.storage_error()

        if attendance_type_id:
            attendance_type = self._attendance_repository.get_attendance_type(attendance_type_id)
            if attendance_type is None or attendance_type.availability_status != "available":
                log_conference_registration_event(
                    "registration_invalid_type",
                    context,
                    ATTENDANCE_TYPE_UNAVAILABLE_MESSAGE,
                )
                return RegistrationResult.invalid_type()

        payment_required = self._payment_policy.is_payment_required(attendance_type_id)
        status = "pending_unpaid" if payment_required else "registered"

        registration = AttendeeRegistration(
            registration_id=f"reg-{attendee_id}",
            attendee_id=attendee_id,
            attendance_type_id=attendance_type_id,
            status=status,
        )

        try:
            stored = self._registration_repository.create_registration(registration)
        except RegistrationStorageError:
            log_conference_registration_event(
                "registration_storage_error",
                context,
                REGISTRATION_FAILED_MESSAGE,
            )
            return RegistrationResult.storage_error()
        except Exception:
            log_conference_registration_event(
                "registration_storage_error",
                context,
                REGISTRATION_FAILED_MESSAGE,
            )
            return RegistrationResult.storage_error()

        if payment_required:
            try:
                self._payment_service.start_payment(stored)
            except PaymentServiceUnavailable:
                log_conference_registration_event(
                    "registration_payment_unavailable",
                    context,
                    PAYMENT_UNAVAILABLE_MESSAGE,
                )
                return RegistrationResult.payment_unavailable(stored)
            except Exception:
                log_conference_registration_event(
                    "registration_payment_unavailable",
                    context,
                    PAYMENT_UNAVAILABLE_MESSAGE,
                )
                return RegistrationResult.payment_unavailable(stored)

            log_conference_registration_event("registration_payment_required", context)
            return RegistrationResult.pending_payment(stored)

        log_conference_registration_event("registration_success", context)
        return RegistrationResult.registered(stored)

    def get_registration_status(
        self,
        attendee_id: str | None,
        trace_id: Optional[str] = None,
    ) -> RegistrationStatusResult:
        context = ConferenceRegistrationLogContext(attendee_id=attendee_id, trace_id=trace_id)

        if not attendee_id:
            log_conference_registration_event("registration_unauthenticated", context)
            return RegistrationStatusResult.unauthenticated()

        registration = self._registration_repository.get_registration(attendee_id)
        if registration is None:
            return RegistrationStatusResult.not_found()

        return RegistrationStatusResult.found(registration)
