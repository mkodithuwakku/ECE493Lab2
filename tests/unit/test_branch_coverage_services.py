from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from models.assigned_paper import AssignedPaper
from models.attendee_registration import AttendeeRegistration
from models.conference_schedule import ConferenceSchedule
from models.final_decision import FinalDecision
from models.paper_metadata import PaperMetadata
from models.paper_submission import PaperSubmission
from models.review_form import ReviewForm
from models.review_status import ReviewStatus
from models.review_submission import ReviewSubmission
from services.additional_review_request_service import (
    AdditionalReviewRequestService,
    ReviewRequestRepository,
    ReviewRequestStorageError,
)
from services.assigned_papers_service import (
    AssignedPapersRepository,
    AssignedPapersRetrievalError,
    AssignedPapersService,
    AssignedPapersResult,
)
from services.auth_service import AuthResult, AuthService, AuthServiceUnavailableError
from services.conference_configuration_service import (
    ConferenceConfigurationService,
    ConfigurationRetrievalError,
    ConfigurationSaveError,
)
from services.conference_configuration_validation import ConferenceConfigurationValidator
from services.conference_confirmation_service import (
    ConferenceConfirmationService,
    ConfirmationRetrievalError,
    ReceiptRetrievalError,
    RegistrationRetrievalError,
    TicketRetrievalError,
)
from services.conference_payment_service import (
    ConferencePaymentService,
    PaymentGatewayResult,
    PaymentGatewayUnavailable,
    PaymentRecordingError,
    RegistrationRetrievalError as PaymentRegistrationRetrievalError,
)
from services.conference_registration_service import (
    ConferenceRegistrationService,
    PaymentServiceUnavailable,
    RegistrationStorageError,
    RegistrationWindowError,
)
from services.decision_service import DecisionDataUnavailableError, DecisionRetrievalError, DecisionService
from services.draft_service import DraftService, DraftStorageError
from services.draft_validation import DraftValidationError, DraftValidator
from services.file_validation import validate_file
from services.final_decision_service import (
    FinalDecisionAccessService,
    FinalDecisionService,
    FinalDecisionStorageError,
    NotificationDeliveryError,
    ReviewStatusError,
    ReviewStatusRepository,
)
from services.invitation_service import (
    InvitationRepository,
    InvitationRetrievalError,
    InvitationListResult,
    InvitationService,
    ReviewerRepository,
)
from services.lockout_policy import LockoutState, compute_lockout_until, is_locked
from services.log_redactor import (
    redact_credentials,
    redact_draft_payload,
    redact_metadata_payload,
    redact_upload_metadata,
)
from services.metadata_service import MetadataRepository, MetadataService
from services.metadata_validation import MetadataValidator
from services.metadata_validation import MetadataValidationError
from services.password_hasher import verify_password
from services.registration_validation import validate_registration
from services.review_form_service import ReviewFormService, ManuscriptRetrievalError, ReviewFormRetrievalError
from services.review_notification_service import (
    NotificationRetrievalError,
    ReviewNotificationService,
    ReviewStatusRetrievalError,
)
from services.review_submission_service import ReviewSubmissionService, ReviewSubmissionStorageError
from services.review_submission_validation import ReviewValidationResult, ReviewValidator
from services.reviewer_assignment_service import (
    AssignmentStorageError,
    NotificationDeliveryError as AssignmentNotificationError,
    ReviewerAssignmentService,
)
from services.schedule_generation_service import (
    AcceptedPapersRetrievalError,
    ScheduleGenerationError,
    ScheduleGenerationService,
    ScheduleRetrievalError,
    ScheduleStorageError,
    SchedulingResourcesRetrievalError,
)
from services.schedule_publication_service import (
    NotificationDeliveryError as PublicationNotificationError,
    SchedulePublicationError,
    SchedulePublicationService,
    ScheduleStatusUpdateError,
)
from services.schedule_service import ScheduleRepository, ScheduleRetrievalError, ScheduleService, SubmissionRetrievalError
from services.user_account_repository import UserAccountRecord
from services.session_manager import SessionManager
from services.identifier_normalizer import normalize_identifier


class StubReviewRequestRepository:
    def __init__(self, *, fail: bool = False, fail_generic: bool = False) -> None:
        self.fail = fail
        self.fail_generic = fail_generic

    def record_request(self, paper_id: str, reviewer_ids: list[str]) -> None:
        if self.fail:
            raise ReviewRequestStorageError("fail")
        if self.fail_generic:
            raise Exception("fail")


def test_additional_review_request_branches() -> None:
    service = AdditionalReviewRequestService(StubReviewRequestRepository())
    assert service.request_reviews("p1", ["r1"], None, True).status == "unauthenticated"
    assert service.request_reviews("p1", ["r1"], "e1", False).status == "forbidden"
    assert service.request_reviews("p1", [], "e1", True).status == "invalid"
    service = AdditionalReviewRequestService(StubReviewRequestRepository(fail=True))
    assert service.request_reviews("p1", ["r1"], "e1", True).status == "error"
    service = AdditionalReviewRequestService(StubReviewRequestRepository(fail_generic=True))
    assert service.request_reviews("p1", ["r1"], "e1", True).status == "error"


class StubAssignedPapersRepository:
    def __init__(self, *, fail: bool = False, fail_generic: bool = False, papers=None) -> None:
        self.fail = fail
        self.fail_generic = fail_generic
        self.papers = papers or []

    def list_assigned(self, reviewer_id: str):
        if self.fail:
            raise AssignedPapersRetrievalError("fail")
        if self.fail_generic:
            raise Exception("fail")
        return self.papers


def test_assigned_papers_branches() -> None:
    service = AssignedPapersService(StubAssignedPapersRepository())
    assert service.list_assigned_papers(None).status == "unauthenticated"
    service = AssignedPapersService(StubAssignedPapersRepository(fail=True))
    assert service.list_assigned_papers("r1").status == "error"
    service = AssignedPapersService(StubAssignedPapersRepository(fail_generic=True))
    assert service.list_assigned_papers("r1").status == "error"
    service = AssignedPapersService(StubAssignedPapersRepository(papers=[]))
    assert service.list_assigned_papers("r1").status == "empty"
    service = AssignedPapersService(
        StubAssignedPapersRepository(papers=[AssignedPaper(paper_id="p1", title="t")])
    )
    assert service.list_assigned_papers("r1").status == "ok"


class StubUserAccountRepository:
    def __init__(self, account: UserAccountRecord | None, *, fail: str | None = None) -> None:
        self.account = account
        self.fail = fail
        self.clear_called = False
        self.fail_update = False

    def find_by_identifier(self, identifier: str):
        if self.fail == "unavailable":
            raise AuthServiceUnavailableError("fail")
        if self.fail == "error":
            raise Exception("fail")
        return self.account

    def update_login_failure(self, user_id, attempts, lockout_until, last_failed_login_at, status=None):
        self.account = UserAccountRecord(
            id=user_id,
            username="u",
            email="e",
            password_hash="hash",
            status=status or "active",
            failed_login_attempts=attempts,
            lockout_until=lockout_until,
            last_failed_login_at=last_failed_login_at,
        )

    def clear_login_failures(self, user_id: str) -> None:
        if self.fail_update:
            raise Exception("fail")
        self.clear_called = True


class StubSessionManager(SessionManager):
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.created = False

    def create_session(self, user_id: str) -> None:
        if self.fail:
            raise Exception("fail")
        self.created = True


def test_auth_service_branches() -> None:
    clock = lambda: datetime(2026, 1, 1, 0, 0, 0)
    service = AuthService(StubUserAccountRepository(None), StubSessionManager(), lambda p, h: True, clock)
    assert service.authenticate(None, None).status == "missing_fields"

    service = AuthService(
        StubUserAccountRepository(None, fail="unavailable"),
        StubSessionManager(),
        lambda p, h: True,
        clock,
    )
    assert service.authenticate("u", "p").status == "service_unavailable"

    service = AuthService(
        StubUserAccountRepository(None, fail="error"),
        StubSessionManager(),
        lambda p, h: True,
        clock,
    )
    assert service.authenticate("u", "p").status == "critical_error"

    service = AuthService(StubUserAccountRepository(None), StubSessionManager(), lambda p, h: True, clock)
    assert service.authenticate("u", "p").status == "invalid_credentials"

    disabled = UserAccountRecord(
        id="u1",
        username="u",
        email="e",
        password_hash="hash",
        status="disabled",
        failed_login_attempts=0,
    )
    service = AuthService(StubUserAccountRepository(disabled), StubSessionManager(), lambda p, h: True, clock)
    assert service.authenticate("u", "p").status == "disabled"

    locked = UserAccountRecord(
        id="u1",
        username="u",
        email="e",
        password_hash="hash",
        status="locked",
        failed_login_attempts=5,
        lockout_until=clock() + timedelta(minutes=10),
        last_failed_login_at=clock(),
    )
    service = AuthService(StubUserAccountRepository(locked), StubSessionManager(), lambda p, h: True, clock)
    assert service.authenticate("u", "p").status == "locked"

    unlocked = UserAccountRecord(
        id="u1",
        username="u",
        email="e",
        password_hash="hash",
        status="locked",
        failed_login_attempts=5,
        lockout_until=clock() - timedelta(minutes=1),
        last_failed_login_at=clock() - timedelta(minutes=2),
    )
    repo = StubUserAccountRepository(unlocked)
    service = AuthService(repo, StubSessionManager(), lambda p, h: False, clock)
    result = service.authenticate("u", "p")
    assert result.status == "invalid_credentials"
    assert repo.clear_called is True

    def failing_verify(p, h):
        raise Exception("fail")

    service = AuthService(StubUserAccountRepository(unlocked), StubSessionManager(), failing_verify, clock)
    assert service.authenticate("u", "p").status == "critical_error"

    valid_account = UserAccountRecord(
        id="u1",
        username="u",
        email="e",
        password_hash="hash",
        status="active",
        failed_login_attempts=0,
    )
    repo = StubUserAccountRepository(valid_account)
    service = AuthService(repo, StubSessionManager(), lambda p, h: True, clock)
    assert service.authenticate("u", "p").status == "success"

    repo = StubUserAccountRepository(valid_account)
    repo.fail_update = True
    service = AuthService(repo, StubSessionManager(), lambda p, h: True, clock)
    assert service.authenticate("u", "p").status == "critical_error"

    service = AuthService(StubUserAccountRepository(valid_account), StubSessionManager(fail=True), lambda p, h: True, clock)
    assert service.authenticate("u", "p").status == "critical_error"


def test_conference_configuration_branches() -> None:
    class Repo:
        def __init__(self, *, fail_get=False, fail_save=False, fail_save_generic=False):
            self.fail_get = fail_get
            self.fail_save = fail_save
            self.fail_save_generic = fail_save_generic
            self.config = None

        def get_configuration(self):
            if self.fail_get == "specific":
                raise ConfigurationRetrievalError("fail")
            if self.fail_get == "generic":
                raise Exception("fail")
            return self.config

        def save_configuration(self, config):
            if self.fail_save:
                raise ConfigurationSaveError("fail")
            if self.fail_save_generic:
                raise Exception("fail")
            self.config = config

    repo = Repo(fail_get="specific")
    service = ConferenceConfigurationService(repo)
    assert service.get_configuration(None, True).status == "unauthenticated"
    assert service.get_configuration("a1", False).status == "forbidden"
    assert service.get_configuration("a1", True).status == "error"

    repo = Repo(fail_get="generic")
    service = ConferenceConfigurationService(repo)
    assert service.get_configuration("a1", True).status == "error"

    repo = Repo()
    service = ConferenceConfigurationService(repo)
    result = service.update_configuration(
        payload={"submissionDeadline": "", "reviewDeadline": "x", "conferenceStartDate": "x", "conferenceEndDate": "x"},
        admin_id="a1",
        is_admin=True,
    )
    assert result.status == "invalid"

    repo = Repo(fail_save=True)
    service = ConferenceConfigurationService(repo)
    result = service.update_configuration(
        payload={
            "submissionDeadline": "2026-01-01T00:00:00",
            "reviewDeadline": "2026-01-02T00:00:00",
            "conferenceStartDate": "2026-01-03T00:00:00",
            "conferenceEndDate": "2026-01-04T00:00:00",
        },
        admin_id="a1",
        is_admin=True,
    )
    assert result.status == "save_error"

    repo = Repo(fail_save_generic=True)
    service = ConferenceConfigurationService(repo)
    result = service.update_configuration(
        payload={
            "submissionDeadline": "2026-01-01T00:00:00",
            "reviewDeadline": "2026-01-02T00:00:00",
            "conferenceStartDate": "2026-01-03T00:00:00",
            "conferenceEndDate": "2026-01-04T00:00:00",
        },
        admin_id="a1",
        is_admin=True,
    )
    assert result.status == "save_error"


def test_conference_configuration_validation_branches() -> None:
    validator = ConferenceConfigurationValidator()
    result = validator.validate({"submissionDeadline": 1})
    assert result.status == "error"
    result = validator.validate(
        {
            "submissionDeadline": "2026-01-02T00:00:00",
            "reviewDeadline": "2026-01-01T00:00:00",
            "conferenceStartDate": "2026-01-03T00:00:00",
            "conferenceEndDate": "2026-01-02T00:00:00",
        }
    )
    assert result.status == "error"


class StubRegistrationRepository:
    def __init__(self, registration: AttendeeRegistration | None, other=None, *, fail=False, fail_generic=False):
        self.registration = registration
        self.other = other or {}
        self.fail = fail
        self.fail_generic = fail_generic

    def get_registration(self, attendee_id: str):
        if self.fail:
            raise RegistrationRetrievalError("fail")
        if self.fail_generic:
            raise Exception("fail")
        if self.registration and self.registration.attendee_id == attendee_id:
            return self.registration
        for reg in self.other.values():
            if reg.attendee_id == attendee_id:
                return reg
        return None

    def get_registration_by_id(self, registration_id: str):
        if self.fail:
            raise RegistrationRetrievalError("fail")
        if self.fail_generic:
            raise Exception("fail")
        if self.registration and self.registration.registration_id == registration_id:
            return self.registration
        return self.other.get(registration_id)


class StubConfirmationRepository:
    def __init__(self, confirmation=None, *, fail=False):
        self.confirmation = confirmation
        self.fail = fail

    def get_confirmation(self, registration_id: str):
        if self.fail:
            raise ConfirmationRetrievalError("fail")
        return self.confirmation


class StubTicketRepository:
    def __init__(self, ticket=None, *, fail=False):
        self.ticket = ticket
        self.fail = fail

    def get_ticket(self, registration_id: str):
        if self.fail:
            raise TicketRetrievalError("fail")
        return self.ticket


class StubReceiptRepository:
    def __init__(self, receipt=None, *, fail=False):
        self.receipt = receipt
        self.fail = fail

    def get_receipt(self, registration_id: str):
        if self.fail:
            raise ReceiptRetrievalError("fail")
        return self.receipt


def test_conference_confirmation_branches() -> None:
    paid = AttendeeRegistration(
        registration_id="reg-1",
        attendee_id="a1",
        attendance_type_id=None,
        status="paid_confirmed",
    )
    service = ConferenceConfirmationService(
        StubRegistrationRepository(paid),
        StubConfirmationRepository(None),
        StubTicketRepository(None),
        StubReceiptRepository(None),
        receipt_enabled=False,
    )
    assert service.get_confirmation(None).status == "unauthenticated"
    assert service.get_receipt(None).status == "unauthenticated"

    service = ConferenceConfirmationService(
        StubRegistrationRepository(paid, fail=True),
        StubConfirmationRepository(None),
        StubTicketRepository(None),
        StubReceiptRepository(None),
        receipt_enabled=False,
    )
    assert service.get_confirmation("a1").status == "error"
    assert service.get_receipt("a1").status == "error"

    other = AttendeeRegistration(
        registration_id="reg-2",
        attendee_id="a2",
        attendance_type_id=None,
        status="paid_confirmed",
    )
    service = ConferenceConfirmationService(
        StubRegistrationRepository(paid, {"reg-2": other}),
        StubConfirmationRepository(None),
        StubTicketRepository(None),
        StubReceiptRepository(None),
        receipt_enabled=True,
    )
    assert service.get_confirmation("a1", registration_id="reg-2").status == "forbidden"
    assert service.get_receipt("a1", registration_id="reg-2").status == "forbidden"

    unpaid = AttendeeRegistration(
        registration_id="reg-3",
        attendee_id="a1",
        attendance_type_id=None,
        status="pending_unpaid",
    )
    service = ConferenceConfirmationService(
        StubRegistrationRepository(unpaid),
        StubConfirmationRepository(None),
        StubTicketRepository(None),
        StubReceiptRepository(None),
        receipt_enabled=True,
    )
    assert service.get_confirmation("a1").status == "not_paid"
    assert service.get_receipt("a1").status == "not_paid"

    service = ConferenceConfirmationService(
        StubRegistrationRepository(paid),
        StubConfirmationRepository(None, fail=True),
        StubTicketRepository(None),
        StubReceiptRepository(None),
        receipt_enabled=True,
    )
    assert service.get_confirmation("a1").status == "error"

    service = ConferenceConfirmationService(
        StubRegistrationRepository(paid),
        StubConfirmationRepository(None),
        StubTicketRepository(None, fail=True),
        StubReceiptRepository(None),
        receipt_enabled=True,
    )
    assert service.get_confirmation("a1").status == "error"

    service = ConferenceConfirmationService(
        StubRegistrationRepository(paid),
        StubConfirmationRepository(None),
        StubTicketRepository(None),
        StubReceiptRepository(None),
        receipt_enabled=False,
    )
    assert service.get_receipt("a1").status == "not_available"

    service = ConferenceConfirmationService(
        StubRegistrationRepository(paid),
        StubConfirmationRepository(None),
        StubTicketRepository(None),
        StubReceiptRepository(None, fail=True),
        receipt_enabled=True,
    )
    assert service.get_receipt("a1").status == "error"


class StubPaymentRegistrationRepository:
    def __init__(self, registration: AttendeeRegistration | None, *, fail=False, fail_generic=False):
        self.registration = registration
        self.fail = fail
        self.fail_generic = fail_generic

    def get_registration(self, attendee_id: str):
        if self.fail:
            raise PaymentRegistrationRetrievalError("fail")
        if self.fail_generic:
            raise Exception("fail")
        if self.registration and self.registration.attendee_id == attendee_id:
            return self.registration
        return None

    def update_status(self, registration_id: str, status: str):
        assert self.registration is not None
        self.registration = AttendeeRegistration(
            registration_id=self.registration.registration_id,
            attendee_id=self.registration.attendee_id,
            attendance_type_id=self.registration.attendance_type_id,
            status=status,
        )
        return self.registration


class StubPaymentDetailsRepository:
    def get_payment_details(self, registration: AttendeeRegistration):
        from models.payment_details import PaymentDetails

        return PaymentDetails(amount=99.0, currency="USD", line_items=None)


class StubPaymentGateway:
    def __init__(self, mode: str):
        self.mode = mode

    def submit_payment(self, registration, payment_details, payload):
        if self.mode == "exception":
            raise Exception("fail")
        if self.mode == "unavailable":
            raise PaymentGatewayUnavailable("fail")
        if self.mode in {"declined", "canceled", "unavailable"}:
            return PaymentGatewayResult(status=self.mode)
        return PaymentGatewayResult(status="success", transaction_id="t", receipt=None)


class StubPaymentRepository:
    def __init__(self, *, fail=False, fail_generic=False):
        self.fail = fail
        self.fail_generic = fail_generic
        self.latest = None

    def record_payment(self, record):
        if self.fail:
            raise PaymentRecordingError("fail")
        if self.fail_generic:
            raise Exception("fail")
        self.latest = record
        return record

    def get_latest_payment(self, registration_id: str):
        return self.latest


def test_conference_payment_branches() -> None:
    registration = AttendeeRegistration(
        registration_id="reg-1",
        attendee_id="a1",
        attendance_type_id=None,
        status="pending_unpaid",
    )
    service = ConferencePaymentService(
        StubPaymentRegistrationRepository(registration, fail=True),
        StubPaymentDetailsRepository(),
        StubPaymentGateway("success"),
        StubPaymentRepository(),
    )
    assert service.pay_registration_fee(None, payload=None).status == "unauthenticated"
    assert service.pay_registration_fee("a1", payload=None).status == "no_pending"

    service = ConferencePaymentService(
        StubPaymentRegistrationRepository(registration, fail_generic=True),
        StubPaymentDetailsRepository(),
        StubPaymentGateway("success"),
        StubPaymentRepository(),
    )
    assert service.pay_registration_fee("a1", payload=None).status == "no_pending"

    service = ConferencePaymentService(
        StubPaymentRegistrationRepository(None),
        StubPaymentDetailsRepository(),
        StubPaymentGateway("success"),
        StubPaymentRepository(),
    )
    assert service.pay_registration_fee("a1", payload=None).status == "no_pending"

    paid = AttendeeRegistration(
        registration_id="reg-2",
        attendee_id="a1",
        attendance_type_id=None,
        status="paid_confirmed",
    )
    service = ConferencePaymentService(
        StubPaymentRegistrationRepository(paid),
        StubPaymentDetailsRepository(),
        StubPaymentGateway("success"),
        StubPaymentRepository(),
    )
    assert service.pay_registration_fee("a1", payload=None).status == "already_paid"

    other = AttendeeRegistration(
        registration_id="reg-3",
        attendee_id="a1",
        attendance_type_id=None,
        status="registered",
    )
    service = ConferencePaymentService(
        StubPaymentRegistrationRepository(other),
        StubPaymentDetailsRepository(),
        StubPaymentGateway("success"),
        StubPaymentRepository(),
    )
    assert service.pay_registration_fee("a1", payload=None).status == "no_pending"

    service = ConferencePaymentService(
        StubPaymentRegistrationRepository(registration),
        StubPaymentDetailsRepository(),
        StubPaymentGateway("declined"),
        StubPaymentRepository(),
    )
    assert service.pay_registration_fee("a1", payload=None).status == "declined"

    service = ConferencePaymentService(
        StubPaymentRegistrationRepository(registration),
        StubPaymentDetailsRepository(),
        StubPaymentGateway("canceled"),
        StubPaymentRepository(),
    )
    assert service.pay_registration_fee("a1", payload=None).status == "canceled"

    service = ConferencePaymentService(
        StubPaymentRegistrationRepository(registration),
        StubPaymentDetailsRepository(),
        StubPaymentGateway("unavailable"),
        StubPaymentRepository(),
    )
    assert service.pay_registration_fee("a1", payload=None).status == "unavailable"

    service = ConferencePaymentService(
        StubPaymentRegistrationRepository(registration),
        StubPaymentDetailsRepository(),
        StubPaymentGateway("exception"),
        StubPaymentRepository(),
    )
    assert service.pay_registration_fee("a1", payload=None).status == "unavailable"

    service = ConferencePaymentService(
        StubPaymentRegistrationRepository(registration),
        StubPaymentDetailsRepository(),
        StubPaymentGateway("success"),
        StubPaymentRepository(fail=True),
    )
    assert service.pay_registration_fee("a1", payload=None).status == "record_failed"

    service = ConferencePaymentService(
        StubPaymentRegistrationRepository(registration),
        StubPaymentDetailsRepository(),
        StubPaymentGateway("success"),
        StubPaymentRepository(fail_generic=True),
    )
    assert service.pay_registration_fee("a1", payload=None).status == "record_failed"

    service = ConferencePaymentService(
        StubPaymentRegistrationRepository(registration),
        StubPaymentDetailsRepository(),
        StubPaymentGateway("success"),
        StubPaymentRepository(),
    )
    assert service.pay_registration_fee("a1", payload=None).status == "success"

    status_result = service.get_payment_status(None)
    assert status_result.status == "unauthenticated"

    status_result = service.get_payment_status("missing")
    assert status_result.status == "found"

    payment_repo = StubPaymentRepository()
    from models.payment_record import PaymentRecord

    payment_repo.latest = PaymentRecord(payment_id="p1", registration_id="reg-1", status="successful")
    service = ConferencePaymentService(
        StubPaymentRegistrationRepository(registration),
        StubPaymentDetailsRepository(),
        StubPaymentGateway("success"),
        payment_repo,
    )
    status_result = service.get_payment_status("a1")
    assert status_result.payment.status == "successful"


def test_conference_registration_branches() -> None:
    class WindowRepo:
        def __init__(self, *, is_open=True, fail=False, fail_generic=False):
            self.is_open_value = is_open
            self.fail = fail
            self.fail_generic = fail_generic

        def is_open(self):
            if self.fail:
                raise RegistrationWindowError("fail")
            if self.fail_generic:
                raise Exception("fail")
            return self.is_open_value

    class AttendanceRepo:
        def __init__(self, types=None):
            self.types = types or {}

        def get_attendance_type(self, attendance_type_id: str):
            return self.types.get(attendance_type_id)

    class RegRepo:
        def __init__(self, *, fail=False):
            self.fail = fail
            self.saved = None

        def create_registration(self, registration):
            if self.fail:
                raise RegistrationStorageError("fail")
            self.saved = registration
            return registration

        def get_registration(self, attendee_id: str):
            return self.saved

    class PaymentPolicy:
        def __init__(self, required: bool):
            self.required = required

        def is_payment_required(self, attendance_type_id):
            return self.required

    class PaymentService:
        def __init__(self, *, fail=False, fail_generic=False):
            self.fail = fail
            self.fail_generic = fail_generic

        def start_payment(self, registration):
            if self.fail:
                raise PaymentServiceUnavailable("fail")
            if self.fail_generic:
                raise Exception("fail")

    attendance = AttendanceRepo({"t1": type("T", (), {"availability_status": "available"})()})
    service = ConferenceRegistrationService(
        WindowRepo(is_open=False),
        attendance,
        RegRepo(),
        PaymentPolicy(False),
        PaymentService(),
    )
    assert service.register_attendee("a1", "t1").status == "closed"

    service = ConferenceRegistrationService(
        WindowRepo(fail=True),
        attendance,
        RegRepo(),
        PaymentPolicy(False),
        PaymentService(),
    )
    assert service.register_attendee("a1", "t1").status == "storage_error"

    service = ConferenceRegistrationService(
        WindowRepo(fail_generic=True),
        attendance,
        RegRepo(),
        PaymentPolicy(False),
        PaymentService(),
    )
    assert service.register_attendee("a1", "t1").status == "storage_error"

    attendance = AttendanceRepo({"bad": type("T", (), {"availability_status": "unavailable"})()})
    service = ConferenceRegistrationService(
        WindowRepo(),
        attendance,
        RegRepo(),
        PaymentPolicy(False),
        PaymentService(),
    )
    assert service.register_attendee("a1", "bad").status == "invalid_type"

    reg_repo = RegRepo(fail=True)
    service = ConferenceRegistrationService(
        WindowRepo(),
        AttendanceRepo({"t1": type("T", (), {"availability_status": "available"})()}),
        reg_repo,
        PaymentPolicy(False),
        PaymentService(),
    )
    assert service.register_attendee("a1", "t1").status == "storage_error"

    reg_repo = RegRepo()
    service = ConferenceRegistrationService(
        WindowRepo(),
        AttendanceRepo({"t1": type("T", (), {"availability_status": "available"})()}),
        reg_repo,
        PaymentPolicy(True),
        PaymentService(fail=True),
    )
    assert service.register_attendee("a1", "t1").status == "payment_unavailable"

    service = ConferenceRegistrationService(
        WindowRepo(),
        AttendanceRepo({"t1": type("T", (), {"availability_status": "available"})()}),
        reg_repo,
        PaymentPolicy(True),
        PaymentService(fail_generic=True),
    )
    assert service.register_attendee("a1", "t1").status == "payment_unavailable"

    service = ConferenceRegistrationService(
        WindowRepo(),
        AttendanceRepo({"t1": type("T", (), {"availability_status": "available"})()}),
        reg_repo,
        PaymentPolicy(True),
        PaymentService(),
    )
    assert service.register_attendee("a1", "t1").status == "pending_unpaid"


def test_decision_service_branches() -> None:
    class Repo:
        def __init__(self, submission=None, fail=None):
            self.submission = submission
            self.fail = fail

        def fetch_submission(self, submission_id):
            if self.fail == "retrieval":
                raise DecisionRetrievalError("fail")
            if self.fail == "unavailable":
                raise DecisionDataUnavailableError("fail")
            if self.fail == "other":
                raise Exception("fail")
            return self.submission

    submission = PaperSubmission(
        id="s1",
        author_ids=["a1"],
        decision_status="recorded",
        decision_value="accept",
    )
    service = DecisionService(Repo(submission))
    assert service.get_decision("s1", None).status == "unauthenticated"
    assert service.get_decision("s1", "a2").status == "forbidden"
    assert service.get_decision("s1", "a1").status == "recorded"

    submission2 = PaperSubmission(
        id="s2",
        author_ids=["a1"],
        decision_status="not_recorded",
        decision_value=None,
    )
    service = DecisionService(Repo(submission2))
    assert service.get_decision("s2", "a1").status == "not_recorded"

    service = DecisionService(Repo(fail="retrieval"))
    assert service.get_decision("s1", "a1").status == "error"

    service = DecisionService(Repo(fail="unavailable"))
    assert service.get_decision("s1", "a1").status == "unavailable"

    service = DecisionService(Repo(fail="other"))
    assert service.get_decision("s1", "a1").status == "unavailable"


def test_draft_service_branches() -> None:
    class Repo:
        def __init__(self, *, fail=False):
            self.fail = fail

        def save_draft(self, submission_id, draft):
            if self.fail:
                raise DraftStorageError("fail")

    class Validator:
        def __init__(self, result=None, *, error=False):
            self.result = result
            self.error = error

        def validate(self, payload):
            if self.error:
                raise DraftValidationError("fail")
            return self.result

    validator = Validator(error=True)
    service = DraftService(Repo(), validator=validator)
    assert service.save_draft("s1", {}).status == "validation_error"

    invalid = type("V", (), {"status": "invalid", "message": None, "data": None, "complete": False})()
    service = DraftService(Repo(), validator=Validator(result=invalid))
    assert service.save_draft("s1", {}).status == "invalid"

    missing = type(
        "V", (), {"status": "missing_minimum", "message": None, "data": None, "complete": False}
    )()
    service = DraftService(Repo(), validator=Validator(result=missing))
    assert service.save_draft("s1", {}).status == "missing_minimum"

    missing_data = type("V", (), {"status": "ok", "message": None, "data": None, "complete": False})()
    service = DraftService(Repo(), validator=Validator(result=missing_data))
    assert service.save_draft("s1", {}).status == "validation_error"

    ok = type(
        "V",
        (),
        {"status": "ok", "message": None, "data": {"title": "t"}, "complete": True},
    )()
    service = DraftService(Repo(fail=True), validator=Validator(result=ok))
    assert service.save_draft("s1", {}).status == "storage_error"

    service = DraftService(Repo(), validator=Validator(result=ok))
    assert service.save_draft("s1", {}).draft_status == "complete"

    ok_incomplete = type(
        "V",
        (),
        {"status": "missing_minimum", "message": None, "data": {"title": "t"}, "complete": False},
    )()
    service = DraftService(Repo(), validator=Validator(result=ok_incomplete))
    assert service.save_draft("s1", {}, save_anyway=True).draft_status == "incomplete"


def test_draft_validation_branches() -> None:
    validator = DraftValidator()
    result = validator.validate({"title": "", "abstract": "", "authors": []})
    assert result.status == "missing_minimum"
    result = validator.validate({"title": 123, "abstract": "", "authors": []})
    assert result.status == "missing_minimum"
    result = validator.validate({"title": "<bad>", "abstract": "ok", "authors": ["a"]})
    assert result.status == "invalid"


def test_file_validation_branches() -> None:
    assert validate_file("file", 10).valid is False


def test_final_decision_service_branches() -> None:
    class DecisionRepo:
        def __init__(
            self,
            *,
            has=False,
            fail_has=False,
            fail_save=False,
            fail_save_generic=False,
            decision=None,
        ):
            self.has = has
            self.fail_has = fail_has
            self.fail_save = fail_save
            self.fail_save_generic = fail_save_generic
            self.decision = decision

        def has_decision(self, paper_id: str) -> bool:
            if self.fail_has:
                raise Exception("fail")
            return self.has

        def save_decision(self, decision):
            if self.fail_save:
                raise FinalDecisionStorageError("fail")
            if self.fail_save_generic:
                raise Exception("fail")
            self.decision = decision

        def get_decision(self, paper_id: str):
            return self.decision

    class ReviewRepo(ReviewStatusRepository):
        def __init__(self, *, status=None, fail=False, fail_generic=False):
            self.status = status
            self.fail = fail
            self.fail_generic = fail_generic

        def get_status(self, paper_id: str):
            if self.fail:
                raise Exception("fail")
            if self.fail_generic:
                raise Exception("fail")
            return self.status

    class Notifier:
        def __init__(self, *, fail=False):
            self.fail = fail

        def send_decision(self, paper_id: str, decision: str):
            if self.fail:
                raise NotificationDeliveryError("fail")

    service = FinalDecisionService(DecisionRepo(), ReviewRepo(status={"reviewsReceived": 1, "reviewersAssigned": 1}))
    assert service.record_decision(None, "accept", None, True).status == "unauthenticated"
    assert service.record_decision("p1", "accept", "e1", False).status == "forbidden"
    assert service.record_decision("p1", "maybe", "e1", True).status == "invalid"

    service = FinalDecisionService(DecisionRepo(has=True), ReviewRepo(status={"reviewsReceived": 1, "reviewersAssigned": 1}))
    assert service.record_decision("p1", "accept", "e1", True).status == "duplicate"

    service = FinalDecisionService(DecisionRepo(), ReviewRepo(status={"reviewsReceived": 0, "reviewersAssigned": 2}))
    assert service.record_decision("p1", "accept", "e1", True).status == "incomplete"

    service = FinalDecisionService(DecisionRepo(fail_save=True), ReviewRepo(status={"reviewsReceived": 2, "reviewersAssigned": 2}))
    assert service.record_decision("p1", "accept", "e1", True).status == "error"

    service = FinalDecisionService(
        DecisionRepo(fail_save_generic=True),
        ReviewRepo(status={"reviewsReceived": 2, "reviewersAssigned": 2}),
    )
    assert service.record_decision("p1", "accept", "e1", True).status == "error"

    service = FinalDecisionService(
        DecisionRepo(),
        ReviewRepo(status={"reviewsReceived": 2, "reviewersAssigned": 2}),
        Notifier(fail=True),
    )
    result = service.record_decision("p1", "accept", "e1", True)
    assert result.status == "success"
    assert result.warning is not None

    service = FinalDecisionService(
        DecisionRepo(),
        ReviewRepo(status=type("S", (), {"reviews_received": 2, "reviewers_assigned": 2})()),
    )
    assert service.record_decision("p1", "accept", "e1", True).status == "success"


def test_invitation_service_branches() -> None:
    from models.review_invitation import ReviewInvitation
    from models.reviewer import Reviewer
    from services.invitation_service import InvitationRetrievalError, InvitationResponseError

    class InvitationRepo(InvitationRepository):
        def __init__(self, invitation: ReviewInvitation, *, fail_list=False, fail_fetch=False, fail_generic=False, fail_response=False):
            self.invitation = invitation
            self.fail_list = fail_list
            self.fail_fetch = fail_fetch
            self.fail_generic = fail_generic
            self.fail_response = fail_response

        def list_pending(self, reviewer_id):
            if self.fail_list:
                raise InvitationRetrievalError("fail")
            if self.fail_generic:
                raise Exception("fail")
            return [self.invitation]

        def fetch_invitation(self, invitation_id):
            if self.fail_fetch:
                raise InvitationRetrievalError("fail")
            if self.fail_generic:
                raise Exception("fail")
            return self.invitation

        def record_acceptance(self, invitation_id):
            if self.fail_response:
                raise InvitationResponseError("fail")

        def record_rejection(self, invitation_id):
            if self.fail_response:
                raise InvitationResponseError("fail")

    class ReviewerRepo(ReviewerRepository):
        def __init__(self, reviewer: Reviewer | None, *, fail=False):
            self.reviewer = reviewer
            self.fail = fail

        def fetch_reviewer(self, reviewer_id):
            if self.fail:
                raise Exception("fail")
            return self.reviewer

    class AssignmentRepo:
        def add_assignment(self, assignment):
            return None

    class EditorNotifications:
        def notify_limit(self, invitation):
            return None

        def notify_rejection(self, invitation):
            return None

    class EmailNotifications:
        def notify_invitation_failed(self, invitation):
            return None

    invitation = ReviewInvitation(id="inv1", paper_id="p1", reviewer_id="r1", email_failed=True)
    service = InvitationService(
        InvitationRepo(invitation),
        ReviewerRepo(Reviewer(id="r1", assignment_count=0, assignment_limit=1)),
        AssignmentRepo(),
        EditorNotifications(),
        EmailNotifications(),
    )
    assert service.list_pending_invitations(None).status == "unauthenticated"
    assert service.list_pending_invitations("r1").status == "ok"

    service = InvitationService(
        InvitationRepo(invitation, fail_list=True),
        ReviewerRepo(Reviewer(id="r1", assignment_count=0, assignment_limit=1)),
        AssignmentRepo(),
        EditorNotifications(),
        EmailNotifications(),
    )
    assert service.list_pending_invitations("r1").status == "error"

    service = InvitationService(
        InvitationRepo(invitation, fail_generic=True),
        ReviewerRepo(Reviewer(id="r1", assignment_count=0, assignment_limit=1)),
        AssignmentRepo(),
        EditorNotifications(),
        EmailNotifications(),
    )
    assert service.list_pending_invitations("r1").status == "error"

    service = InvitationService(
        InvitationRepo(invitation, fail_fetch=True),
        ReviewerRepo(Reviewer(id="r1", assignment_count=0, assignment_limit=1)),
        AssignmentRepo(),
        EditorNotifications(),
        EmailNotifications(),
    )
    assert service.accept_invitation("inv1", "r1").status == "error"

    invitation_other = ReviewInvitation(id="inv2", paper_id="p1", reviewer_id="other")
    service = InvitationService(
        InvitationRepo(invitation_other),
        ReviewerRepo(Reviewer(id="r1", assignment_count=0, assignment_limit=1)),
        AssignmentRepo(),
        EditorNotifications(),
        EmailNotifications(),
    )
    assert service.accept_invitation("inv2", "r1").status == "forbidden"

    service = InvitationService(
        InvitationRepo(invitation),
        ReviewerRepo(Reviewer(id="r1", assignment_count=1, assignment_limit=1)),
        AssignmentRepo(),
        EditorNotifications(),
        EmailNotifications(),
    )
    assert service.accept_invitation("inv1", "r1").status == "limit"

    service = InvitationService(
        InvitationRepo(invitation, fail_response=True),
        ReviewerRepo(Reviewer(id="r1", assignment_count=0, assignment_limit=2)),
        AssignmentRepo(),
        EditorNotifications(),
        EmailNotifications(),
    )
    assert service.accept_invitation("inv1", "r1").status == "error"

    service = InvitationService(
        InvitationRepo(invitation),
        ReviewerRepo(None, fail=True),
        AssignmentRepo(),
        EditorNotifications(),
        EmailNotifications(),
    )
    assert service.accept_invitation("inv1", "r1").status == "error"

    service = InvitationService(
        InvitationRepo(invitation),
        ReviewerRepo(Reviewer(id="r1", assignment_count=0, assignment_limit=2)),
        AssignmentRepo(),
        EditorNotifications(),
        EmailNotifications(),
    )
    assert service.accept_invitation("inv1", "r1").status == "accepted"

    service = InvitationService(
        InvitationRepo(invitation, fail_response=True),
        ReviewerRepo(Reviewer(id="r1", assignment_count=0, assignment_limit=2)),
        AssignmentRepo(),
        EditorNotifications(),
        EmailNotifications(),
    )
    assert service.reject_invitation("inv1", "r1").status == "error"

    service = InvitationService(
        InvitationRepo(invitation),
        ReviewerRepo(Reviewer(id="r1", assignment_count=0, assignment_limit=2)),
        AssignmentRepo(),
        EditorNotifications(),
        EmailNotifications(),
    )
    assert service.reject_invitation("inv1", "r1").status == "rejected"


def test_lockout_policy_branches() -> None:
    now = datetime(2026, 1, 1)
    state = LockoutState(failed_attempts=5, lockout_until=now + timedelta(minutes=5), last_failed_login_at=now)
    assert is_locked(state, now) is True
    assert compute_lockout_until(now) > now
    assert is_locked(LockoutState(0, None, None), now) is False
    from services.lockout_policy import should_lock, within_lockout_window

    assert should_lock(0) is False
    assert within_lockout_window(None, now) is False
    assert within_lockout_window(now, now) is True


def test_log_redactor_branches() -> None:
    assert redact_credentials("password=secret") == "[redacted]=secret" or "[redacted]" in redact_credentials("password=secret")
    assert redact_upload_metadata(None) is None
    assert redact_upload_metadata("x") == "[redacted]"
    assert redact_metadata_payload(None) is None
    assert redact_metadata_payload("x") == "[redacted]"
    assert redact_draft_payload(None) is None
    assert redact_draft_payload("x") == "[redacted]"


def test_metadata_validation_branches() -> None:
    validator = MetadataValidator()
    result = validator.validate({})
    assert result.status == "missing_fields"
    result = validator.validate(
        {
            "author_names": ["a"],
            "affiliations": ["x"],
            "contact_email": "bad-email",
            "abstract": "a",
            "keywords": ["k"],
            "paper_source": "src",
        }
    )
    assert result.status == "invalid_fields"


def test_password_hasher_branches() -> None:
    assert verify_password("pass", "invalid") is False


def test_registration_validation_branch() -> None:
    result = validate_registration("", "")
    assert result.errors


def test_review_form_service_branches() -> None:
    class AssignRepo:
        def __init__(self, *, assigned=True, fail=False):
            self.assigned = assigned
            self.fail = fail

        def is_assigned(self, reviewer_id, paper_id):
            if self.fail:
                raise Exception("fail")
            return self.assigned

    class ManuscriptRepo:
        def __init__(self, *, has=True, fail=False, fail_generic=False):
            self.has = has
            self.fail = fail
            self.fail_generic = fail_generic

        def has_manuscript(self, paper_id):
            if self.fail:
                raise ManuscriptRetrievalError("fail")
            if self.fail_generic:
                raise Exception("fail")
            return self.has

    class FormRepo:
        def __init__(self, *, fail=False, fail_generic=False):
            self.fail = fail
            self.fail_generic = fail_generic

        def fetch_review_form(self, paper_id):
            if self.fail:
                raise ReviewFormRetrievalError("fail")
            if self.fail_generic:
                raise Exception("fail")
            return ReviewForm(paper_id=paper_id, title="t", form_fields={}, manuscript_link=None)

    service = ReviewFormService(AssignRepo(), FormRepo(), ManuscriptRepo())
    assert service.get_review_form("p1", None).status == "unauthenticated"

    service = ReviewFormService(AssignRepo(fail=True), FormRepo(), ManuscriptRepo())
    assert service.get_review_form("p1", "r1").status == "error"

    service = ReviewFormService(AssignRepo(assigned=False), FormRepo(), ManuscriptRepo())
    assert service.get_review_form("p1", "r1").status == "forbidden"

    service = ReviewFormService(AssignRepo(), FormRepo(), ManuscriptRepo(fail=True))
    assert service.get_review_form("p1", "r1").status == "manuscript_unavailable"

    service = ReviewFormService(AssignRepo(), FormRepo(), ManuscriptRepo(fail_generic=True))
    assert service.get_review_form("p1", "r1").status == "manuscript_unavailable"

    service = ReviewFormService(AssignRepo(), FormRepo(), ManuscriptRepo(has=False))
    assert service.get_review_form("p1", "r1").status == "manuscript_unavailable"

    service = ReviewFormService(AssignRepo(), FormRepo(fail=True), ManuscriptRepo())
    assert service.get_review_form("p1", "r1").status == "error"

    service = ReviewFormService(AssignRepo(), FormRepo(fail_generic=True), ManuscriptRepo())
    assert service.get_review_form("p1", "r1").status == "error"

    service = ReviewFormService(AssignRepo(), FormRepo(), ManuscriptRepo())
    assert service.get_review_form("p1", "r1").status == "ok"


def test_review_notification_service_branches() -> None:
    class Repo:
        def __init__(self, *, fail=False, fail_generic=False):
            self.fail = fail
            self.fail_generic = fail_generic

        def list_notifications(self, editor_id):
            if self.fail:
                raise NotificationRetrievalError("fail")
            if self.fail_generic:
                raise Exception("fail")
            return []

        def store_notification(self, notification):
            return None

        def get_status(self, paper_id):
            if self.fail:
                raise ReviewStatusRetrievalError("fail")
            if self.fail_generic:
                raise Exception("fail")
            return ReviewStatus(paper_id=paper_id, reviews_received=1, reviewers_assigned=1, review_details=[])

        def save_status(self, status):
            return None

    class Sender:
        def __init__(self, *, fail=False):
            self.fail = fail

        def send(self, notification):
            from services.review_notification_service import NotificationDeliveryError

            if self.fail:
                raise NotificationDeliveryError("fail")

    service = ReviewNotificationService(Repo(), Repo(), Sender())
    assert service.list_notifications(None, True).status == "unauthenticated"
    assert service.list_notifications("e1", False).status == "forbidden"
    assert service.list_notifications("e1", True).status == "ok"

    service = ReviewNotificationService(Repo(fail=True), Repo(), Sender())
    assert service.list_notifications("e1", True).status == "error"

    service = ReviewNotificationService(Repo(fail_generic=True), Repo(), Sender())
    assert service.list_notifications("e1", True).status == "error"

    service = ReviewNotificationService(Repo(), Repo(), Sender())
    assert service.get_review_status("p1", None, True).status == "unauthenticated"
    assert service.get_review_status("p1", "e1", False).status == "forbidden"
    assert service.get_review_status("p1", "e1", True).status == "ok"

    service = ReviewNotificationService(Repo(), Repo(fail=True), Sender())
    assert service.get_review_status("p1", "e1", True).status == "error"

    service = ReviewNotificationService(Repo(), Repo(fail_generic=True), Sender())
    assert service.get_review_status("p1", "e1", True).status == "error"


def test_review_submission_service_branches() -> None:
    class Repo:
        def __init__(self, *, fail=False, fail_generic=False):
            self.fail = fail
            self.fail_generic = fail_generic
            self.saved = None

        def save_submission(self, review):
            if self.fail:
                raise ReviewSubmissionStorageError("fail")
            if self.fail_generic:
                raise Exception("fail")
            self.saved = review

        def has_submission(self, reviewer_id, paper_id):
            return False

    class ReviewerRepo:
        def __init__(self, *, assigned=True, fail=False):
            self.assigned = assigned
            self.fail = fail

        def is_assigned(self, reviewer_id, paper_id):
            if self.fail:
                raise Exception("fail")
            return self.assigned

    class Validator(ReviewValidator):
        def validate(self, payload):
            return super().validate(payload)

    service = ReviewSubmissionService(ReviewerRepo(), Repo(), Validator())
    assert service.submit_review("p1", None, {}).status == "unauthenticated"

    service = ReviewSubmissionService(ReviewerRepo(assigned=False), Repo(), Validator())
    assert service.submit_review("p1", "r1", {}).status == "forbidden"

    service = ReviewSubmissionService(ReviewerRepo(fail=True), Repo(), Validator())
    assert service.submit_review("p1", "r1", {}).status == "error"

    service = ReviewSubmissionService(ReviewerRepo(), Repo(), Validator())
    assert service.submit_review("p1", "r1", {}).status == "missing"

    payload = {"overall_score": 4, "comments": "ok"}
    service = ReviewSubmissionService(ReviewerRepo(), Repo(fail=True), Validator())
    assert service.submit_review("p1", "r1", payload).status == "error"

    service = ReviewSubmissionService(ReviewerRepo(), Repo(fail_generic=True), Validator())
    assert service.submit_review("p1", "r1", payload).status == "error"


def test_review_submission_validation_branches() -> None:
    validator = ReviewValidator()
    result = validator.validate({"overall_score": "bad", "comments": "x"})
    assert result.status == "invalid"
    result = validator.validate({"overall_score": 5})
    assert result.status == "missing"


def test_review_submission_service_additional_branches() -> None:
    class Repo:
        def __init__(self, *, duplicate=False, fail_duplicate=False):
            self.duplicate = duplicate
            self.fail_duplicate = fail_duplicate

        def has_submission(self, reviewer_id, paper_id):
            if self.fail_duplicate:
                raise Exception("fail")
            return self.duplicate

        def save_submission(self, review):
            return None

    class ReviewerRepo:
        def is_assigned(self, reviewer_id, paper_id):
            return True

    service = ReviewSubmissionService(ReviewerRepo(), Repo(duplicate=True), ReviewValidator())
    assert service.submit_review("p1", "r1", {"overall_score": 4, "comments": "ok"}).status == "duplicate"

    service = ReviewSubmissionService(ReviewerRepo(), Repo(fail_duplicate=True), ReviewValidator())
    assert service.submit_review("p1", "r1", {"overall_score": 4, "comments": "ok"}).status == "error"

    service = ReviewSubmissionService(ReviewerRepo(), Repo(), ReviewValidator())
    assert service.submit_review("p1", "r1", {"overall_score": "bad", "comments": "ok"}).status == "invalid"


def test_reviewer_assignment_service_branches() -> None:
    class AssignmentRepo:
        def __init__(self, *, fail=False):
            self.fail = fail

        def is_assigned(self, reviewer_id, paper_id):
            return False

        def save_assignment(self, assignment):
            if self.fail:
                raise AssignmentStorageError("fail")

    class ReviewerDirectory:
        def find_reviewer(self, reviewer_id):
            return {"id": reviewer_id} if reviewer_id != "missing" else None

        def is_valid_identifier(self, reviewer_id):
            return reviewer_id != "invalid"

    class LimitRepo:
        def at_limit(self, reviewer_id):
            return reviewer_id == "limited"

    class Notifier:
        def __init__(self, *, fail=False):
            self.fail = fail

        def send_invitation(self, reviewer_id, paper_id):
            if self.fail:
                raise AssignmentNotificationError("fail")

    service = ReviewerAssignmentService(AssignmentRepo(), ReviewerDirectory(), LimitRepo(), Notifier())
    assert service.assign_reviewers("p1", ["r1"], None, True).status == "unauthenticated"
    assert service.assign_reviewers("p1", ["r1"], "e1", False).status == "forbidden"
    assert service.assign_reviewers("p1", ["invalid"], "e1", True).status == "invalid"
    assert service.assign_reviewers("p1", ["missing"], "e1", True).status == "invalid"
    assert service.assign_reviewers("p1", ["limited"], "e1", True).status == "limit"

    service = ReviewerAssignmentService(AssignmentRepo(fail=True), ReviewerDirectory(), LimitRepo(), Notifier())
    assert service.assign_reviewers("p1", ["r1"], "e1", True).status == "error"

    service = ReviewerAssignmentService(AssignmentRepo(), ReviewerDirectory(), LimitRepo(), Notifier(fail=True))
    assert service.assign_reviewers("p1", ["r1"], "e1", True).status == "notification_failed"

    class AssignmentRepoDup(AssignmentRepo):
        def is_assigned(self, reviewer_id, paper_id):
            return True

    service = ReviewerAssignmentService(AssignmentRepoDup(), ReviewerDirectory(), LimitRepo(), Notifier())
    assert service.assign_reviewers("p1", ["r1"], "e1", True).status == "duplicate"


def test_schedule_generation_service_branches() -> None:
    class AcceptedRepo:
        def __init__(self, *, fail=False, fail_generic=False, papers=None):
            self.fail = fail
            self.fail_generic = fail_generic
            self.papers = papers or []

        def list_accepted_papers(self):
            if self.fail:
                raise AcceptedPapersRetrievalError("fail")
            if self.fail_generic:
                raise Exception("fail")
            return self.papers

    class ResourcesRepo:
        def __init__(self, *, fail=False, fail_generic=False, resources=None):
            self.fail = fail
            self.fail_generic = fail_generic
            self.resources = resources

        def get_resources(self):
            if self.fail:
                raise SchedulingResourcesRetrievalError("fail")
            if self.fail_generic:
                raise Exception("fail")
            return self.resources

    class ScheduleRepo:
        def __init__(self, *, fail=False, fail_generic=False):
            self.fail = fail
            self.fail_generic = fail_generic
            self.saved = None

        def save_schedule(self, schedule):
            if self.fail:
                raise ScheduleStorageError("fail")
            if self.fail_generic:
                raise Exception("fail")
            self.saved = schedule

        def get_schedule(self):
            if self.fail:
                raise ScheduleRetrievalError("fail")
            if self.fail_generic:
                raise Exception("fail")
            return self.saved

    class Generator:
        def __init__(self, *, fail=False, fail_generic=False):
            self.fail = fail
            self.fail_generic = fail_generic

        def generate(self, accepted_papers, resources):
            if self.fail:
                raise ScheduleGenerationError("fail")
            if self.fail_generic:
                raise Exception("fail")
            return ConferenceSchedule(status="unpublished", entries=[])

    service = ScheduleGenerationService(
        AcceptedRepo(fail=True),
        ResourcesRepo(resources=None),
        ScheduleRepo(),
    )
    assert service.generate_schedule("a1", True).status == "generation_failed"

    service = ScheduleGenerationService(
        AcceptedRepo(fail_generic=True),
        ResourcesRepo(resources=None),
        ScheduleRepo(),
    )
    assert service.generate_schedule("a1", True).status == "generation_failed"

    service = ScheduleGenerationService(
        AcceptedRepo(papers=[]),
        ResourcesRepo(resources=None),
        ScheduleRepo(),
    )
    assert service.generate_schedule("a1", True).status == "no_papers"

    service = ScheduleGenerationService(
        AcceptedRepo(papers=[type("P", (), {"submission_id": "p1"})()]),
        ResourcesRepo(fail=True, resources=None),
        ScheduleRepo(),
    )
    assert service.generate_schedule("a1", True).status == "generation_failed"

    service = ScheduleGenerationService(
        AcceptedRepo(papers=[type("P", (), {"submission_id": "p1"})()]),
        ResourcesRepo(fail_generic=True, resources=None),
        ScheduleRepo(),
    )
    assert service.generate_schedule("a1", True).status == "generation_failed"

    resources = type("R", (), {"rooms": [], "time_slots": []})()
    service = ScheduleGenerationService(
        AcceptedRepo(papers=[type("P", (), {"submission_id": "p1"})()]),
        ResourcesRepo(resources=resources),
        ScheduleRepo(),
    )
    assert service.generate_schedule("a1", True).status == "constraint"

    resources = type("R", (), {"rooms": ["r"], "time_slots": ["t"]})()
    service = ScheduleGenerationService(
        AcceptedRepo(papers=[type("P", (), {"submission_id": "p1"})()]),
        ResourcesRepo(resources=resources),
        ScheduleRepo(),
        schedule_generator=Generator(fail=True),
    )
    assert service.generate_schedule("a1", True).status == "generation_failed"

    service = ScheduleGenerationService(
        AcceptedRepo(papers=[type("P", (), {"submission_id": "p1"})()]),
        ResourcesRepo(resources=resources),
        ScheduleRepo(),
        schedule_generator=Generator(fail_generic=True),
    )
    assert service.generate_schedule("a1", True).status == "generation_failed"

    service = ScheduleGenerationService(
        AcceptedRepo(papers=[type("P", (), {"submission_id": "p1"})()]),
        ResourcesRepo(resources=resources),
        ScheduleRepo(fail=True),
    )
    assert service.generate_schedule("a1", True).status == "storage_failed"

    service = ScheduleGenerationService(
        AcceptedRepo(papers=[type("P", (), {"submission_id": "p1"})()]),
        ResourcesRepo(resources=resources),
        ScheduleRepo(fail_generic=True),
    )
    assert service.generate_schedule("a1", True).status == "storage_failed"

    service = ScheduleGenerationService(
        AcceptedRepo(papers=[type("P", (), {"submission_id": "p1"})()]),
        ResourcesRepo(resources=resources),
        ScheduleRepo(),
    )
    assert service.generate_schedule("a1", True).status == "generated"

    assert service.get_generated_schedule(None, True).status == "unauthenticated"
    assert service.get_generated_schedule("a1", False).status == "forbidden"
    assert service.get_generated_schedule("a1", True).status == "found"

    service = ScheduleGenerationService(
        AcceptedRepo(papers=[type("P", (), {"submission_id": "p1"})()]),
        ResourcesRepo(resources=resources),
        ScheduleRepo(fail=True),
    )
    assert service.get_generated_schedule("a1", True).status == "error"

    service = ScheduleGenerationService(
        AcceptedRepo(papers=[type("P", (), {"submission_id": "p1"})()]),
        ResourcesRepo(resources=resources),
        ScheduleRepo(),
    )
    assert service.get_generated_schedule("a1", True).status == "not_found"


class StubScheduleRepo(ScheduleRepository):
    def __init__(self, *, fail=False, fail_generic=False, schedule=None):
        self.fail = fail
        self.fail_generic = fail_generic
        self.schedule = schedule

    def fetch_schedule(self):
        if self.fail:
            raise ScheduleRetrievalError("fail")
        if self.fail_generic:
            raise Exception("fail")
        return self.schedule


class StubSubmissionRepo:
    def __init__(self, submission=None, *, fail=False, fail_generic=False):
        self.submission = submission
        self.fail = fail
        self.fail_generic = fail_generic

    def fetch_submission(self, submission_id):
        if self.fail:
            raise SubmissionRetrievalError("fail")
        if self.fail_generic:
            raise Exception("fail")
        return self.submission


def test_schedule_service_branches() -> None:
    schedule = ConferenceSchedule(status="unpublished", entries=[])
    submission = PaperSubmission(
        id="s1",
        author_ids=["a1"],
        decision_status="recorded",
        decision_value="accept",
    )
    service = ScheduleService(StubScheduleRepo(schedule=schedule), StubSubmissionRepo(submission=submission))
    assert service.get_schedule("s1", None).status == "unauthenticated"

    service = ScheduleService(StubScheduleRepo(), StubSubmissionRepo(fail=True))
    assert service.get_schedule("s1", "a1").status == "error"

    service = ScheduleService(StubScheduleRepo(), StubSubmissionRepo(fail_generic=True))
    assert service.get_schedule("s1", "a1").status == "error"

    service = ScheduleService(StubScheduleRepo(fail=True), StubSubmissionRepo(submission=submission))
    assert service.get_schedule("s1", "a1").status == "error"

    service = ScheduleService(StubScheduleRepo(fail_generic=True), StubSubmissionRepo(submission=submission))
    assert service.get_schedule("s1", "a1").status == "error"

    service = ScheduleService(StubScheduleRepo(schedule=schedule), StubSubmissionRepo(submission=submission))
    assert service.get_schedule("s1", "a1").status == "unpublished"

    published = ConferenceSchedule(status="published", entries=[])
    service = ScheduleService(StubScheduleRepo(schedule=published), StubSubmissionRepo(submission=submission))
    assert service.get_schedule("s1", "a1").status == "published"

    schedule_with_entry = ConferenceSchedule(
        status="published",
        entries=[type("E", (), {"submission_id": "s1"})()],
    )
    service = ScheduleService(StubScheduleRepo(schedule=schedule_with_entry), StubSubmissionRepo(submission=submission))
    result = service.get_schedule("s1", "a1")
    assert result.status == "published" and result.warning is None

    service = ScheduleService(StubScheduleRepo(schedule=published), StubSubmissionRepo(submission=submission))
    assert service.get_schedule("s1", "a2").status == "forbidden"


def test_schedule_publication_service_branches() -> None:
    class ScheduleRepo:
        def __init__(self, schedule=None, *, fail=False, fail_generic=False, fail_update=False, fail_update_generic=False):
            self.schedule = schedule
            self.fail = fail
            self.fail_generic = fail_generic
            self.fail_update = fail_update
            self.fail_update_generic = fail_update_generic

        def get_schedule(self):
            if self.fail:
                raise Exception("fail")
            if self.fail_generic:
                raise Exception("fail")
            return self.schedule

        def set_published(self, schedule, admin_id):
            if self.fail_update:
                raise ScheduleStatusUpdateError("fail")
            if self.fail_update_generic:
                raise Exception("fail")
            return ConferenceSchedule(
                status="published",
                entries=schedule.entries,
                is_finalized=schedule.is_finalized,
                is_approved=schedule.is_approved,
            )

    class Publisher:
        def __init__(self, *, fail=False, fail_generic=False):
            self.fail = fail
            self.fail_generic = fail_generic

        def publish(self, schedule):
            if self.fail:
                raise SchedulePublicationError("fail")
            if self.fail_generic:
                raise Exception("fail")

    class Notifier:
        def __init__(self, *, fail=False, fail_generic=False):
            self.fail = fail
            self.fail_generic = fail_generic

        def notify_publication(self, schedule):
            if self.fail:
                raise PublicationNotificationError("fail")
            if self.fail_generic:
                raise Exception("fail")

    schedule = ConferenceSchedule(status="unpublished", entries=[], is_finalized=True, is_approved=True)
    service = SchedulePublicationService(ScheduleRepo(schedule), Publisher(), Notifier())
    assert service.publish_schedule(None, True).status == "unauthenticated"
    assert service.publish_schedule("a1", False).status == "forbidden"

    service = SchedulePublicationService(ScheduleRepo(None), Publisher(), Notifier())
    assert service.publish_schedule("a1", True).status == "not_found"

    schedule_not_ready = ConferenceSchedule(status="unpublished", entries=[], is_finalized=False, is_approved=True)
    service = SchedulePublicationService(ScheduleRepo(schedule_not_ready), Publisher(), Notifier())
    assert service.publish_schedule("a1", True).status == "not_ready"

    service = SchedulePublicationService(ScheduleRepo(schedule), Publisher(fail=True), Notifier())
    assert service.publish_schedule("a1", True).status == "publish_failed"

    service = SchedulePublicationService(ScheduleRepo(schedule), Publisher(fail_generic=True), Notifier())
    assert service.publish_schedule("a1", True).status == "publish_failed"

    service = SchedulePublicationService(ScheduleRepo(schedule, fail_update=True), Publisher(), Notifier())
    assert service.publish_schedule("a1", True).status == "status_update_failed"

    service = SchedulePublicationService(ScheduleRepo(schedule, fail_update_generic=True), Publisher(), Notifier())
    assert service.publish_schedule("a1", True).status == "status_update_failed"

    service = SchedulePublicationService(ScheduleRepo(schedule), Publisher(), Notifier(fail=True))
    assert service.publish_schedule("a1", True).status == "published_with_warning"

    service = SchedulePublicationService(ScheduleRepo(schedule), Publisher(), Notifier(fail_generic=True))
    assert service.publish_schedule("a1", True).status == "published_with_warning"

    service = SchedulePublicationService(ScheduleRepo(schedule, fail=True), Publisher(), Notifier())
    assert service.publish_schedule("a1", True).status == "error"

    service = SchedulePublicationService(ScheduleRepo(schedule, fail_generic=True), Publisher(), Notifier())
    assert service.publish_schedule("a1", True).status == "error"


def test_metadata_service_branches() -> None:
    class SubmissionRepo:
        def __init__(self, *, finalized=False):
            self.finalized = finalized

        def is_finalized(self, submission_id):
            return self.finalized

    class Repo(MetadataRepository):
        def __init__(self, *, fail=False):
            self.fail = fail

        def save_metadata(self, submission_id, metadata):
            if self.fail:
                from services.metadata_service import MetadataStorageError

                raise MetadataStorageError("fail")

    service = MetadataService(SubmissionRepo(finalized=True), Repo(), MetadataValidator())
    assert service.save_metadata("s1", {}).status == "locked"

    service = MetadataService(SubmissionRepo(), Repo(), MetadataValidator())
    assert service.save_metadata("s1", {"title": ""}).status == "missing_fields"

    service = MetadataService(SubmissionRepo(), Repo(), MetadataValidator())
    assert (
        service.save_metadata(
            "s1",
            {
                "author_names": ["a"],
                "affiliations": ["x"],
                "contact_email": "bad-email",
                "abstract": "a",
                "keywords": ["k"],
                "paper_source": "src",
            },
        ).status
        == "invalid_fields"
    )

    class Validator:
        def __init__(self, *, fail=False, result=None):
            self.fail = fail
            self.result = result

        def validate(self, payload):
            if self.fail:
                from services.metadata_validation import MetadataValidationError

                raise MetadataValidationError("fail")
            return self.result

    service = MetadataService(SubmissionRepo(), Repo(), Validator(fail=True))
    assert service.save_metadata("s1", {"title": "t"}).status == "validation_error"

    bad = type("V", (), {"status": "ok", "message": None, "metadata": None})()
    service = MetadataService(SubmissionRepo(), Repo(), Validator(result=bad))
    assert service.save_metadata("s1", {"title": "t"}).status == "validation_error"

    service = MetadataService(SubmissionRepo(), Repo(fail=True), MetadataValidator())
    result = service.save_metadata(
        "s1",
        {
            "author_names": ["a"],
            "affiliations": ["x"],
            "contact_email": "a@example.com",
            "abstract": "a",
            "keywords": ["k"],
            "paper_source": "src",
        },
    )
    assert result.status == "storage_error"

    service = MetadataService(SubmissionRepo(), Repo(), MetadataValidator())
    result = service.save_metadata(
        "s1",
        {
            "author_names": ["a"],
            "affiliations": ["x"],
            "contact_email": "a@example.com",
            "abstract": "a",
            "keywords": ["k"],
            "paper_source": "src",
        },
    )
    assert result.status == "success"




def test_review_submission_validator_missing_branches() -> None:
    validator = ReviewValidator()
    result = validator.validate({"overall_score": 4, "comments": ""})
    assert result.status == "missing"


def test_schedule_generation_constraint_time_slots() -> None:
    resources = type("R", (), {"rooms": ["r"], "time_slots": ["t1"]})()
    papers = [type("P", (), {"submission_id": "p1"})(), type("P", (), {"submission_id": "p2"})()]
    service = ScheduleGenerationService(
        type("A", (), {"list_accepted_papers": lambda self: papers})(),
        type("R", (), {"get_resources": lambda self: resources})(),
        type("S", (), {"save_schedule": lambda self, schedule: None, "get_schedule": lambda self: schedule})(),
    )
    assert service.generate_schedule("a1", True).status == "constraint"


def test_conference_registration_additional_branches() -> None:
    class WindowRepo:
        def is_open(self):
            return True

    class AttendanceRepo:
        def get_attendance_type(self, attendance_type_id: str):
            return None

    class RegRepo:
        def create_registration(self, registration):
            return registration

        def get_registration(self, attendee_id: str):
            return None

    class PaymentPolicy:
        def is_payment_required(self, attendance_type_id):
            return False

    class PaymentService:
        def start_payment(self, registration):
            return None

    service = ConferenceRegistrationService(WindowRepo(), AttendanceRepo(), RegRepo(), PaymentPolicy(), PaymentService())
    assert service.register_attendee(None, None).status == "unauthenticated"
    assert service.get_registration_status(None).status == "unauthenticated"
    assert service.get_registration_status("a1").status == "not_found"


def test_assigned_papers_service_empty_branch() -> None:
    class Repo:
        def list_assigned(self, reviewer_id):
            return []

    service = AssignedPapersService(Repo())
    assert service.list_assigned_papers("r1").status == "empty"


def test_auth_service_error_branches() -> None:
    now = datetime(2026, 1, 1)

    class Repo:
        def find_by_identifier(self, identifier):
            return UserAccountRecord(
                id="u1",
                identifier="u1",
                password_hash="hash",
                status="active",
                failed_login_attempts=0,
                lockout_until=None,
                last_failed_login_at=None,
            )

        def clear_login_failures(self, user_id):
            return None

        def update_login_failure(self, *args, **kwargs):
            return None

    class BadSessionManager:
        def create_session(self, user_id):
            raise Exception("fail")

    def bad_verify(password, password_hash):
        raise Exception("fail")

    class DummySessionManager:
        def create_session(self, user_id):
            return None

    service = AuthService(Repo(), DummySessionManager(), bad_verify, lambda: now)
    assert service.authenticate("u1", "pw").status == "critical_error"

    service = AuthService(Repo(), BadSessionManager(), lambda a, b: True, lambda: now)
    assert service.authenticate("u1", "pw").status == "critical_error"


def test_conference_configuration_validation_error() -> None:
    class Repo:
        def save_configuration(self, config):
            return None

        def get_configuration(self):
            return None

    class Validator:
        def validate(self, payload):
            return type("R", (), {"status": "invalid", "errors": ["bad"]})()

    service = ConferenceConfigurationService(Repo(), Validator())
    assert service.update_configuration({}, "a1", True).status == "invalid"


def test_conference_confirmation_additional_branches() -> None:
    class RegRepo:
        def __init__(self, registration):
            self.registration = registration

        def get_registration(self, attendee_id):
            return self.registration

        def get_registration_by_id(self, registration_id):
            return self.registration

    class ConfirmRepo:
        def get_confirmation(self, registration_id):
            return "c1"

    class TicketRepo:
        def get_ticket(self, registration_id):
            return "t1"

    class ReceiptRepo:
        def __init__(self, receipt=None):
            self.receipt = receipt

        def get_receipt(self, registration_id):
            return self.receipt

    service = ConferenceConfirmationService(
        RegRepo(None),
        ConfirmRepo(),
        TicketRepo(),
        ReceiptRepo(None),
        receipt_enabled=True,
    )
    assert service.get_confirmation("a1").status == "not_paid"

    paid = AttendeeRegistration(
        registration_id="reg-1",
        attendee_id="a1",
        attendance_type_id=None,
        status="paid_confirmed",
    )
    service = ConferenceConfirmationService(
        RegRepo(paid),
        ConfirmRepo(),
        TicketRepo(),
        ReceiptRepo(None),
        receipt_enabled=True,
    )
    assert service.get_receipt("a1").status == "not_available"


def test_conference_payment_status_registration_missing() -> None:
    class RegRepo:
        def get_registration(self, attendee_id):
            return None

        def update_status(self, registration_id, status):
            return None

    class PaymentRepo:
        def get_latest_payment(self, registration_id):
            return None

        def record_payment(self, payment):
            return payment

    class DetailsRepo:
        def get_payment_details(self, registration):
            return type("D", (), {"amount": 10, "currency": "USD", "line_items": []})()

    class Gateway:
        def submit_payment(self, registration, payment_details, payload):
            return PaymentGatewayResult(status="unavailable")

    service = ConferencePaymentService(RegRepo(), PaymentRepo(), DetailsRepo(), Gateway())
    result = service.get_payment_status("a1")
    assert result.status == "found"
    assert result.registration is not None


def test_conference_registration_payment_unavailable() -> None:
    class WindowRepo:
        def is_open(self):
            return True

    class AttendanceRepo:
        def get_attendance_type(self, attendance_type_id):
            return None

    class RegRepo:
        def create_registration(self, registration):
            return registration

        def get_registration(self, attendee_id):
            return None

    class PaymentPolicy:
        def is_payment_required(self, attendance_type_id):
            return True

    class PaymentService:
        def start_payment(self, registration):
            raise PaymentServiceUnavailable("fail")

    service = ConferenceRegistrationService(
        WindowRepo(), AttendanceRepo(), RegRepo(), PaymentPolicy(), PaymentService()
    )
    assert service.register_attendee("a1", None).status == "payment_unavailable"
    assert service.get_registration_status("a1").status == "not_found"


def test_draft_validation_error_paths() -> None:
    validator = DraftValidator()
    result = validator.validate(
        {"title": "t", "abstract": "a", "authors": ["a"], "contact_email": "bad"}
    )
    assert result.status == "invalid"
    result = validator.validate(
        {"title": "<t>", "abstract": "a", "authors": ["a"], "contact_email": "a@b.com"}
    )
    assert result.status == "invalid"

    class BadStr:
        def __str__(self):
            raise Exception("fail")

    try:
        validator.validate({"authors": [BadStr()]})
        assert False
    except DraftValidationError:
        assert True


def test_invitation_service_email_failed_and_reject_error() -> None:
    from models.review_invitation import ReviewInvitation
    from models.reviewer import Reviewer
    from services.invitation_service import InvitationResponseError

    class InvitationRepo:
        def __init__(self, invitation, *, fail_reject=False):
            self.invitation = invitation
            self.fail_reject = fail_reject

        def list_pending(self, reviewer_id):
            return [self.invitation]

        def fetch_invitation(self, invitation_id):
            return self.invitation

        def record_acceptance(self, invitation_id):
            return None

        def record_rejection(self, invitation_id):
            if self.fail_reject:
                raise InvitationResponseError("fail")

    class ReviewerRepo:
        def fetch_reviewer(self, reviewer_id):
            return Reviewer(id=reviewer_id, assignment_count=0, assignment_limit=1)

    class AssignmentRepo:
        def add_assignment(self, assignment):
            return None

    class EditorNotifications:
        def notify_limit(self, invitation):
            return None

        def notify_rejection(self, invitation):
            raise Exception("fail")

    class EmailNotifications:
        def notify_invitation_failed(self, invitation):
            return None

    invitation = ReviewInvitation(
        id="inv1",
        paper_id="p1",
        reviewer_id="r1",
        email_failed=True,
    )
    service = InvitationService(
        InvitationRepo(invitation, fail_reject=True),
        ReviewerRepo(),
        AssignmentRepo(),
        EditorNotifications(),
        EmailNotifications(),
    )
    assert service.accept_invitation("inv1", "r1").status == "accepted"
    assert service.reject_invitation("inv1", "r1").status == "error"


def test_metadata_validation_additional_branches() -> None:
    validator = MetadataValidator()
    result = validator.validate(
        {
            "author_names": ["a"],
            "affiliations": ["x"],
            "contact_email": "a@b.com",
            "abstract": "a" * 3001,
            "keywords": ["k"],
            "paper_source": "src",
        }
    )
    assert result.status == "invalid_fields"
    result = validator.validate(
        {
            "author_names": ["a"],
            "affiliations": ["x"],
            "contact_email": "a@b.com",
            "abstract": "a",
            "keywords": ["k"] * 11,
            "paper_source": "src",
        }
    )
    assert result.status == "invalid_fields"
    result = validator.validate(
        {
            "author_names": ["<bad>"],
            "affiliations": ["x"],
            "contact_email": "a@b.com",
            "abstract": "a",
            "keywords": ["k"],
            "paper_source": "src",
        }
    )
    assert result.status == "invalid_fields"


def test_registration_validation_password_branch() -> None:
    result = validate_registration("a@b.com", "short")
    assert result.password_invalid is True


def test_review_notification_record_error_branch() -> None:
    class NotificationRepo:
        def store_notification(self, notification):
            return None

    class StatusRepo:
        def get_status(self, paper_id):
            raise ReviewStatusRetrievalError("fail")

        def save_status(self, status):
            return None

    class Sender:
        def send(self, notification):
            return None

    service = ReviewNotificationService(NotificationRepo(), StatusRepo(), Sender())
    result = service.record_review_submission("p1", "r1", 1)
    assert result.status == "ok"


def test_review_submission_validation_error_branch() -> None:
    class Validator:
        def validate(self, payload):
            return ReviewValidationResult(status="other")

    class Repo:
        def has_submission(self, reviewer_id, paper_id):
            return False

        def save_submission(self, submission):
            return None

    class ReviewerRepo:
        def is_assigned(self, reviewer_id, paper_id):
            return True

    service = ReviewSubmissionService(ReviewerRepo(), Repo(), Validator())
    assert service.submit_review("p1", "r1", {"overall_score": 4, "comments": "ok"}).status == "error"


def test_reviewer_assignment_notification_failed() -> None:
    class AssignmentRepo:
        def is_assigned(self, reviewer_id, paper_id):
            return False

        def save_assignment(self, assignment):
            return None

    class ReviewerDirectory:
        def is_valid_identifier(self, reviewer_id):
            return True

        def find_reviewer(self, reviewer_id):
            return {"id": reviewer_id}

    class LimitRepo:
        def at_limit(self, reviewer_id):
            return False

    class NotificationService:
        def send_invitation(self, reviewer_id, paper_id):
            raise AssignmentNotificationError("fail")

    service = ReviewerAssignmentService(
        AssignmentRepo(), ReviewerDirectory(), LimitRepo(), NotificationService()
    )
    assert service.assign_reviewers("p1", ["r1"], "e1", True).status == "notification_failed"


def test_schedule_generation_additional_constraints() -> None:
    resources = type("R", (), {"rooms": [], "time_slots": ["t1"]})()
    papers = [type("P", (), {"submission_id": "p1"})()]
    service = ScheduleGenerationService(
        type("A", (), {"list_accepted_papers": lambda self: papers})(),
        type("R", (), {"get_resources": lambda self: resources})(),
        type("S", (), {"save_schedule": lambda self, schedule: None, "get_schedule": lambda self: schedule})(),
    )
    assert service.generate_schedule("a1", True).status == "constraint"

    resources = type("R", (), {"rooms": ["r"], "time_slots": ["t1"]})()
    papers = [
        type("P", (), {"submission_id": "p1"})(),
        type("P", (), {"submission_id": "p2"})(),
    ]
    service = ScheduleGenerationService(
        type("A", (), {"list_accepted_papers": lambda self: papers})(),
        type("R", (), {"get_resources": lambda self: resources})(),
        type("S", (), {"save_schedule": lambda self, schedule: None, "get_schedule": lambda self: schedule})(),
    )
    assert service.generate_schedule("a1", True).status == "constraint"


def test_schedule_publication_success_branch() -> None:
    class ScheduleRepo:
        def __init__(self, schedule):
            self.schedule = schedule

        def get_schedule(self):
            return self.schedule

        def set_published(self, schedule, admin_id):
            return schedule

    class Publisher:
        def publish(self, schedule):
            return None

    class Notifier:
        def notify_publication(self, schedule):
            return None

    schedule = ConferenceSchedule(status="unpublished", entries=[], is_finalized=True, is_approved=True)
    service = SchedulePublicationService(ScheduleRepo(schedule), Publisher(), Notifier())
    assert service.publish_schedule("a1", True).status == "published"


def test_assigned_papers_result_forbidden_branch() -> None:
    result = AssignedPapersResult.forbidden()
    assert result.status == "forbidden"


def test_auth_service_lockout_branches() -> None:
    now = datetime(2026, 1, 1, 12, 0, 0)

    class Repo:
        def find_by_identifier(self, identifier):
            return UserAccountRecord(
                id="u1",
                username="u1",
                email="u1@example.com",
                password_hash="hash",
                status="active",
                failed_login_attempts=4,
                lockout_until=None,
                last_failed_login_at=now,
            )

        def clear_login_failures(self, user_id):
            return None

        def update_login_failure(self, *args, **kwargs):
            self.updated = True

    class DummySessionManager:
        def create_session(self, user_id):
            return None

    service = AuthService(Repo(), DummySessionManager(), lambda a, b: False, lambda: now)
    result = service.authenticate("u1", "pw")
    assert result.status == "invalid_credentials"


def test_conference_configuration_unauthenticated_branch() -> None:
    class Repo:
        def save_configuration(self, config):
            return None

        def get_configuration(self):
            return None

    service = ConferenceConfigurationService(Repo(), ConferenceConfigurationValidator())
    assert service.update_configuration({}, None, True).status == "unauthenticated"


def test_conference_confirmation_generic_exceptions() -> None:
    class RegRepo:
        def get_registration(self, attendee_id):
            raise Exception("fail")

        def get_registration_by_id(self, registration_id):
            raise Exception("fail")

    class ConfirmRepo:
        def get_confirmation(self, registration_id):
            raise Exception("fail")

    class TicketRepo:
        def get_ticket(self, registration_id):
            raise Exception("fail")

    class ReceiptRepo:
        def get_receipt(self, registration_id):
            raise Exception("fail")

    service = ConferenceConfirmationService(RegRepo(), ConfirmRepo(), TicketRepo(), ReceiptRepo(), receipt_enabled=True)
    assert service.get_confirmation("a1").status == "error"

    class RegRepo2:
        def get_registration(self, attendee_id):
            return AttendeeRegistration(
                registration_id="reg-1",
                attendee_id=attendee_id,
                attendance_type_id=None,
                status="paid_confirmed",
            )

        def get_registration_by_id(self, registration_id):
            return self.get_registration("a1")

    service = ConferenceConfirmationService(RegRepo2(), ConfirmRepo(), TicketRepo(), ReceiptRepo(), receipt_enabled=True)
    assert service.get_confirmation("a1").status == "error"
    assert service.get_receipt("a1").status == "error"


def test_conference_payment_gateway_unavailable_branch() -> None:
    class RegRepo:
        def get_registration(self, attendee_id):
            return AttendeeRegistration(
                registration_id="reg-1",
                attendee_id=attendee_id,
                attendance_type_id=None,
                status="pending_unpaid",
            )

        def update_status(self, registration_id, status):
            return AttendeeRegistration(
                registration_id=registration_id,
                attendee_id="a1",
                attendance_type_id=None,
                status=status,
            )

    class PaymentRepo:
        def record_payment(self, payment):
            return payment

        def get_latest_payment(self, registration_id):
            return None

    class DetailsRepo:
        def get_payment_details(self, registration):
            return type("D", (), {"amount": 10, "currency": "USD", "line_items": []})()

    class Gateway:
        def submit_payment(self, registration, payment_details, payload):
            return PaymentGatewayResult(status="unavailable")

    service = ConferencePaymentService(RegRepo(), DetailsRepo(), Gateway(), PaymentRepo())
    assert service.pay_registration_fee("a1", {"method": "card"}).status == "unavailable"


def test_conference_registration_storage_exception_branch() -> None:
    class WindowRepo:
        def is_open(self):
            return True

    class AttendanceRepo:
        def get_attendance_type(self, attendance_type_id):
            return None

    class RegRepo:
        def create_registration(self, registration):
            raise Exception("fail")

        def get_registration(self, attendee_id):
            return AttendeeRegistration(
                registration_id="reg-1",
                attendee_id=attendee_id,
                attendance_type_id=None,
                status="registered",
            )

    class PaymentPolicy:
        def is_payment_required(self, attendance_type_id):
            return False

    class PaymentService:
        def start_payment(self, registration):
            return None

    service = ConferenceRegistrationService(
        WindowRepo(), AttendanceRepo(), RegRepo(), PaymentPolicy(), PaymentService()
    )
    assert service.register_attendee("a1", None).status == "storage_error"
    assert service.get_registration_status("a1").status == "found"


def test_draft_validation_extra_branches() -> None:
    validator = DraftValidator()
    result = validator.validate({"title": "t", "abstract": "a", "authors": ["<bad>"]})
    assert result.status == "invalid"
    result = validator.validate({"title": "t", "abstract": "a", "authors": "a,b"})
    assert result.status in {"valid", "missing_minimum"}
    result = validator.validate({"title": "t", "abstract": "a", "authors": 123})
    assert result.status in {"valid", "missing_minimum"}
    result = validator.validate({"title": "t", "abstract": "a", "authors": ["a", "\x01"]})
    assert result.status == "invalid"
    result = validator.validate({"title": "t", "abstract": "a", "authors": ["a", "\x7f"]})
    assert result.status == "invalid"


def test_final_decision_service_additional_branches() -> None:
    class DecisionRepo:
        def __init__(self, *, has=False, fail_save=False, fail_save_generic=False, decision=None):
            self.has = has
            self.fail_save = fail_save
            self.fail_save_generic = fail_save_generic
            self.decision = decision

        def has_decision(self, paper_id):
            return self.has

        def save_decision(self, decision):
            if self.fail_save:
                raise FinalDecisionStorageError("fail")
            if self.fail_save_generic:
                raise Exception("fail")

        def get_decision(self, paper_id):
            return self.decision

    class StatusRepo:
        def __init__(self, *, status=None, fail=False, fail_generic=False):
            self.status = status
            self.fail = fail
            self.fail_generic = fail_generic

        def get_status(self, paper_id):
            if self.fail:
                raise ReviewStatusError("fail")
            if self.fail_generic:
                raise Exception("fail")
            return self.status

    class Sender:
        def __init__(self, *, fail=False):
            self.fail = fail

        def send_decision(self, paper_id, decision):
            if self.fail:
                raise NotificationDeliveryError("fail")

    service = FinalDecisionService(DecisionRepo(has=True), StatusRepo(status={"reviewsReceived": 1, "reviewersAssigned": 1}))
    assert service.record_decision("p1", "accept", "e1", True).status == "duplicate"

    service = FinalDecisionService(DecisionRepo(), StatusRepo(fail=True))
    assert service.record_decision("p1", "accept", "e1", True).status == "error"

    service = FinalDecisionService(DecisionRepo(), StatusRepo(status={"reviewsReceived": 0, "reviewersAssigned": 1}))
    assert service.record_decision("p1", "accept", "e1", True).status == "incomplete"

    service = FinalDecisionService(DecisionRepo(fail_save=True), StatusRepo(status={"reviewsReceived": 1, "reviewersAssigned": 1}))
    assert service.record_decision("p1", "accept", "e1", True).status == "error"

    service = FinalDecisionService(DecisionRepo(), StatusRepo(status={"reviewsReceived": 1, "reviewersAssigned": 1}), Sender(fail=True))
    assert service.record_decision("p1", "accept", "e1", True).warning

    result = FinalDecisionService._extract_review_counts(object())
    assert result == (0, 0)


def test_final_decision_access_service_branches() -> None:
    class DecisionRepo:
        def __init__(self, decision=None, fail=False):
            self.decision = decision
            self.fail = fail

        def has_decision(self, paper_id):
            return False

        def save_decision(self, decision):
            return None

        def get_decision(self, paper_id):
            if self.fail:
                raise Exception("fail")
            return self.decision

    class SubmissionRepo:
        def __init__(self, *, submission=None, fail=False):
            self.submission = submission
            self.fail = fail

        def fetch_submission(self, paper_id):
            if self.fail:
                raise Exception("fail")
            return self.submission

    service = FinalDecisionAccessService(DecisionRepo(), SubmissionRepo(fail=True))
    assert service.get_decision("p1", "a1").status == "error"

    submission = PaperSubmission(id="p1", author_ids=["a1"], decision_status="recorded", decision_value="accept")
    service = FinalDecisionAccessService(DecisionRepo(decision=None), SubmissionRepo(submission=submission))
    assert service.get_decision("p1", "a1").decision_status == "undecided"

    service = FinalDecisionAccessService(DecisionRepo(decision=FinalDecision("p1", "accepted", "e1")), SubmissionRepo(submission=submission))
    assert service.get_decision("p1", "a1").decision_status == "accepted"

    service = FinalDecisionAccessService(DecisionRepo(), SubmissionRepo(submission=submission))
    assert service.get_decision("p1", None).status == "unauthenticated"
    assert service.get_decision("p1", "other").status == "forbidden"


def test_invitation_service_additional_error_branches() -> None:
    from models.review_invitation import ReviewInvitation
    from models.reviewer import Reviewer

    class InvitationRepo:
        def __init__(self, invitation, *, fail_fetch=False, fail_generic=False, fail_accept_generic=False):
            self.invitation = invitation
            self.fail_fetch = fail_fetch
            self.fail_generic = fail_generic
            self.fail_accept_generic = fail_accept_generic

        def list_pending(self, reviewer_id):
            return [self.invitation]

        def fetch_invitation(self, invitation_id):
            if self.fail_fetch:
                raise InvitationRetrievalError("fail")
            if self.fail_generic:
                raise Exception("fail")
            return self.invitation

        def record_acceptance(self, invitation_id):
            if self.fail_accept_generic:
                raise Exception("fail")

        def record_rejection(self, invitation_id):
            raise Exception("fail")

    class ReviewerRepo:
        def fetch_reviewer(self, reviewer_id):
            return Reviewer(id=reviewer_id, assignment_count=0, assignment_limit=10)

    class AssignmentRepo:
        def add_assignment(self, assignment):
            return None

    class EditorNotifications:
        def notify_limit(self, invitation):
            return None

        def notify_rejection(self, invitation):
            return None

    class EmailNotifications:
        def notify_invitation_failed(self, invitation):
            return None

    invitation = ReviewInvitation(id="inv1", paper_id="p1", reviewer_id="r1", email_failed=False)
    service = InvitationService(InvitationRepo(invitation, fail_generic=True), ReviewerRepo(), AssignmentRepo(), EditorNotifications(), EmailNotifications())
    assert service.accept_invitation("inv1", "r1").status == "error"
    assert service.accept_invitation("inv1", None).status == "unauthenticated"

    service = InvitationService(InvitationRepo(invitation, fail_accept_generic=True), ReviewerRepo(), AssignmentRepo(), EditorNotifications(), EmailNotifications())
    assert service.accept_invitation("inv1", "r1").status == "error"
    assert service.reject_invitation("inv1", "r1").status == "error"

    assert InvitationListResult.forbidden().status == "forbidden"


def test_metadata_validation_exception_and_normalize_branches() -> None:
    class BadStr:
        def __str__(self):
            raise Exception("fail")

    try:
        MetadataValidator().validate({"author_names": [BadStr()]})
        assert False
    except MetadataValidationError:
        assert True

    validator = MetadataValidator()
    result = validator.validate(
        {
            "author_names": "a,b",
            "affiliations": "x",
            "contact_email": "a@b.com",
            "abstract": "a",
            "keywords": 123,
            "paper_source": "src",
        }
    )
    assert result.status == "valid"

    result = validator.validate(
        {
            "author_names": ["a"],
            "affiliations": ["x"],
            "contact_email": "a@b.com",
            "abstract": "a",
            "keywords": ["k"],
            "paper_source": "<bad>",
        }
    )
    assert result.status == "invalid_fields"


def test_registration_validation_letter_only_password() -> None:
    result = validate_registration("a@b.com", "abcdefgh")
    assert result.password_invalid is True


def test_reviewer_assignment_additional_branches() -> None:
    class AssignmentRepo:
        def is_assigned(self, reviewer_id, paper_id):
            return False

        def save_assignment(self, assignment):
            raise Exception("fail")

    class ReviewerDirectory:
        def is_valid_identifier(self, reviewer_id):
            return True

        def find_reviewer(self, reviewer_id):
            return {"id": reviewer_id}

    class LimitRepo:
        def at_limit(self, reviewer_id):
            return False

    class NotificationService:
        def send_invitation(self, reviewer_id, paper_id):
            return None

    service = ReviewerAssignmentService(
        AssignmentRepo(), ReviewerDirectory(), LimitRepo(), NotificationService()
    )
    assert service.assign_reviewers("p1", [], "e1", True).status == "invalid"
    assert service.assign_reviewers("p1", ["r1"], "e1", True).status == "error"


def test_schedule_generation_auth_branches() -> None:
    service = ScheduleGenerationService(
        type("A", (), {"list_accepted_papers": lambda self: []})(),
        type("R", (), {"get_resources": lambda self: None})(),
        type("S", (), {"save_schedule": lambda self, schedule: None, "get_schedule": lambda self: None})(),
    )
    assert service.generate_schedule(None, True).status == "unauthenticated"
    assert service.generate_schedule("a1", False).status == "forbidden"


def test_schedule_generation_retrieval_error_branch() -> None:
    class Repo:
        def get_schedule(self):
            raise ScheduleRetrievalError("fail")

    service = ScheduleGenerationService(
        type("A", (), {"list_accepted_papers": lambda self: []})(),
        type("R", (), {"get_resources": lambda self: None})(),
        Repo(),
    )
    assert service.get_generated_schedule("a1", True).status == "error"


def test_schedule_publication_retrieval_error_branch() -> None:
    from services.schedule_publication_service import ScheduleRetrievalError as PubScheduleRetrievalError

    class ScheduleRepo:
        def get_schedule(self):
            raise PubScheduleRetrievalError("fail")

    class Publisher:
        def publish(self, schedule):
            return None

    class Notifier:
        def notify_publication(self, schedule):
            return None

    service = SchedulePublicationService(ScheduleRepo(), Publisher(), Notifier())
    assert service.publish_schedule("a1", True).status == "error"


def test_conference_confirmation_receipt_registration_exception_and_none() -> None:
    class RegRepo:
        def get_registration(self, attendee_id):
            raise Exception("fail")

        def get_registration_by_id(self, registration_id):
            raise Exception("fail")

    class ReceiptRepo:
        def get_receipt(self, registration_id):
            return None

    service = ConferenceConfirmationService(RegRepo(), None, None, ReceiptRepo(), receipt_enabled=True)
    assert service.get_receipt("a1").status == "error"

    class RegRepo2:
        def get_registration(self, attendee_id):
            return None

        def get_registration_by_id(self, registration_id):
            return None

    service = ConferenceConfirmationService(RegRepo2(), None, None, ReceiptRepo(), receipt_enabled=True)
    assert service.get_receipt("a1").status == "not_paid"


def test_draft_validation_authors_none_branch() -> None:
    validator = DraftValidator()
    result = validator.validate({"title": "t", "abstract": "a", "authors": None})
    assert result.status == "missing_minimum"


def test_final_decision_service_review_status_generic_error() -> None:
    class DecisionRepo:
        def has_decision(self, paper_id):
            return False

        def save_decision(self, decision):
            return None

        def get_decision(self, paper_id):
            return None

    class StatusRepo:
        def get_status(self, paper_id):
            raise Exception("fail")

    service = FinalDecisionService(DecisionRepo(), StatusRepo())
    assert service.record_decision("p1", "accept", "e1", True).status == "error"


def test_final_decision_access_decision_error_branch() -> None:
    class DecisionRepo:
        def has_decision(self, paper_id):
            return False

        def save_decision(self, decision):
            return None

        def get_decision(self, paper_id):
            raise Exception("fail")

    class SubmissionRepo:
        def fetch_submission(self, paper_id):
            return PaperSubmission(id="p1", author_ids=["a1"], decision_status="recorded", decision_value="accept")

    service = FinalDecisionAccessService(DecisionRepo(), SubmissionRepo())
    assert service.get_decision("p1", "a1").status == "error"


def test_metadata_validation_control_chars() -> None:
    validator = MetadataValidator()
    result = validator.validate(
        {
            "author_names": ["a"],
            "affiliations": ["x"],
            "contact_email": "a@b.com",
            "abstract": "\x01",
            "keywords": ["k"],
            "paper_source": "src",
        }
    )
    assert result.status == "invalid_fields"
    result = validator.validate(
        {
            "author_names": ["a"],
            "affiliations": ["x"],
            "contact_email": "a@b.com",
            "abstract": "a",
            "keywords": ["k"],
            "paper_source": "\x7f",
        }
    )
    assert result.status == "invalid_fields"


def test_registration_validation_invalid_email() -> None:
    result = validate_registration("bad-email", "password1")
    assert "Email format is invalid." in result.errors


def test_schedule_generation_retrieval_error_branch_specific() -> None:
    from services.schedule_generation_service import ScheduleRetrievalError as GenScheduleRetrievalError

    class Repo:
        def get_schedule(self):
            raise GenScheduleRetrievalError("fail")

    service = ScheduleGenerationService(
        type("A", (), {"list_accepted_papers": lambda self: []})(),
        type("R", (), {"get_resources": lambda self: None})(),
        Repo(),
    )
    assert service.get_generated_schedule("a1", True).status == "error"
