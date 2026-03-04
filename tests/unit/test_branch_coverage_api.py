from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.assigned_papers_error_mapper import map_assigned_papers_error
from api.conference_configuration_error_mapper import map_configuration_error
from api.conference_confirmation_error_mapper import map_confirmation_error, map_receipt_error
from api.conference_payment import get_payment_status, pay_registration_fee
from api.conference_payment_error_mapper import (
    map_conference_payment_error,
    map_payment_status_error,
)
from api.conference_registration import get_registration_status, register_for_conference
from api.conference_registration_error_mapper import (
    map_conference_registration_error,
    map_registration_status_error,
)
from api.conference_schedule_generation import get_generated_conference_schedule
from api.conference_schedule_generation_error_mapper import (
    map_schedule_display_error,
    map_schedule_generation_error,
)
from api.conference_schedule_publication_error_mapper import map_schedule_publication_error
from api.final_decision import get_final_decision, record_final_decision
from api.final_decision_error_mapper import map_final_decision_error, map_final_decision_view_error
from api.final_decision_review_requests import request_additional_reviews
from api.final_decision_review_requests_error_mapper import map_review_request_error
from api.login.login_controller import LoginRequest, handle_login
from api.login.login_error_mapper import map_auth_result
from api.password.change_password_controller import change_password
from api.password.change_password_error_mapper import map_password_change_result
from api.review_form_access import get_review_form
from api.review_form_error_mapper import map_review_form_error
from api.review_invitation_error_mapper import map_invitation_error, map_invitation_list_error
from api.review_invitations import accept_invitation, list_invitations, reject_invitation
from api.review_notifications_error_mapper import map_notification_error, map_review_status_error
from api.review_submission_error_mapper import map_review_submission_error
from api.reviewer_assignment_error_mapper import map_assignment_error
from api.submissions.decision_error_mapper import map_decision_error
from api.submissions.draft_error_mapper import map_draft_result
from api.submissions.metadata_error_mapper import map_metadata_result
from api.submissions.manuscript_upload_controller import upload_manuscript
from api.submissions.schedule_error_mapper import map_schedule_error
from api.submissions.upload_error_mapper import map_upload_result
from services.auth_service import AuthResult, AuthService
from services.conference_payment_service import ConferencePaymentService, PaymentResult, PaymentStatusResult
from services.conference_registration_service import ConferenceRegistrationService, RegistrationResult, RegistrationStatusResult
from services.final_decision_service import DecisionViewResult, FinalDecisionResult
from services.invitation_service import InvitationListResult, InvitationResponseResult
from services.review_form_service import ReviewFormResult
from services.review_notification_service import NotificationListResult, ReviewStatusResult
from services.review_submission_service import ReviewSubmissionResult
from services.reviewer_assignment_service import AssignmentResult
from services.schedule_generation_service import (
    ScheduleDisplayResult,
    ScheduleGenerationResult,
)
from services.schedule_publication_service import PublicationResult
from services.session_manager import SessionManager


@dataclass
class DummyResult:
    status: str
    message: str | None = None
    redirect_to: str | None = None
    errors: list[str] | None = None
    constraint_type: str | None = None


def test_assigned_papers_error_default() -> None:
    status, payload = map_assigned_papers_error(DummyResult(status="unknown", message="x"))
    assert status == 500
    assert payload["message"] == "x"


def test_configuration_error_default() -> None:
    status, payload = map_configuration_error(DummyResult(status="unknown", message=None))
    assert status == 500
    assert "Configuration update failed" in payload["message"]


def test_confirmation_error_branches() -> None:
    status, payload = map_confirmation_error(DummyResult(status="unauthenticated", message="m"))
    assert status == 401
    status, payload = map_confirmation_error(DummyResult(status="forbidden", message="m"))
    assert status == 403
    status, payload = map_confirmation_error(DummyResult(status="not_paid", message="m"))
    assert status == 400
    status, payload = map_confirmation_error(DummyResult(status="error", message="m"))
    assert status == 503
    status, payload = map_confirmation_error(DummyResult(status="other", message=None))
    assert status == 500


def test_receipt_error_branches() -> None:
    status, payload = map_receipt_error(DummyResult(status="unauthenticated", message="m"))
    assert status == 401
    status, payload = map_receipt_error(DummyResult(status="forbidden", message="m"))
    assert status == 403
    status, payload = map_receipt_error(DummyResult(status="not_paid", message="m"))
    assert status == 400
    status, payload = map_receipt_error(DummyResult(status="not_available", message="m"))
    assert status == 404
    status, payload = map_receipt_error(DummyResult(status="error", message="m"))
    assert status == 503
    status, payload = map_receipt_error(DummyResult(status="other", message=None))
    assert status == 500


def test_conference_payment_error_branches() -> None:
    status, payload = map_conference_payment_error(DummyResult(status="unauthenticated", message="m"))
    assert status == 401
    status, payload = map_conference_payment_error(DummyResult(status="no_pending", message="m"))
    assert status == 409
    status, payload = map_conference_payment_error(DummyResult(status="already_paid", message="m"))
    assert status == 409
    status, payload = map_conference_payment_error(DummyResult(status="declined", message="m"))
    assert status == 402
    status, payload = map_conference_payment_error(DummyResult(status="canceled", message="m"))
    assert status == 402
    status, payload = map_conference_payment_error(DummyResult(status="unavailable", message="m"))
    assert status == 503
    status, payload = map_conference_payment_error(DummyResult(status="record_failed", message="m"))
    assert status == 500
    status, payload = map_conference_payment_error(DummyResult(status="other", message=None))
    assert status == 500


def test_conference_registration_error_branches() -> None:
    status, payload = map_conference_registration_error(
        DummyResult(status="unauthenticated", message="m")
    )
    assert status == 401
    status, payload = map_conference_registration_error(DummyResult(status="closed", message="m"))
    assert status == 403
    status, payload = map_conference_registration_error(
        DummyResult(status="invalid_type", message="m")
    )
    assert status == 400
    status, payload = map_conference_registration_error(
        DummyResult(status="storage_error", message="m")
    )
    assert status == 500
    status, payload = map_conference_registration_error(DummyResult(status="other", message=None))
    assert status == 500


def test_schedule_generation_error_branches() -> None:
    status, payload = map_schedule_generation_error(
        DummyResult(status="unauthenticated", message="m")
    )
    assert status == 401
    status, payload = map_schedule_generation_error(DummyResult(status="forbidden", message="m"))
    assert status == 403
    status, payload = map_schedule_generation_error(
        DummyResult(status="no_papers", message="m")
    )
    assert status == 400
    status, payload = map_schedule_generation_error(
        DummyResult(status="constraint", message="m", constraint_type=None)
    )
    assert status == 400 and "constraint_type" not in payload
    status, payload = map_schedule_generation_error(
        DummyResult(status="constraint", message="m", constraint_type="rooms")
    )
    assert payload["constraint_type"] == "rooms"
    status, payload = map_schedule_generation_error(
        DummyResult(status="generation_failed", message="m")
    )
    assert status == 500
    status, payload = map_schedule_generation_error(
        DummyResult(status="storage_failed", message="m")
    )
    assert status == 503
    status, payload = map_schedule_generation_error(DummyResult(status="other", message=None))
    assert status == 500


def test_schedule_display_error_branches() -> None:
    status, _ = map_schedule_display_error(DummyResult(status="unauthenticated", message="m"))
    assert status == 401
    status, _ = map_schedule_display_error(DummyResult(status="forbidden", message="m"))
    assert status == 403
    status, _ = map_schedule_display_error(DummyResult(status="not_found", message="m"))
    assert status == 404
    status, _ = map_schedule_display_error(DummyResult(status="error", message="m"))
    assert status == 503
    status, _ = map_schedule_display_error(DummyResult(status="other", message=None))
    assert status == 500


def test_schedule_publication_error_branches() -> None:
    status, _ = map_schedule_publication_error(DummyResult(status="unauthenticated", message="m"))
    assert status == 401
    status, _ = map_schedule_publication_error(DummyResult(status="forbidden", message="m"))
    assert status == 403
    status, _ = map_schedule_publication_error(DummyResult(status="not_ready", message="m"))
    assert status == 400
    status, _ = map_schedule_publication_error(DummyResult(status="not_found", message="m"))
    assert status == 400
    status, _ = map_schedule_publication_error(DummyResult(status="error", message="m"))
    assert status == 503
    status, _ = map_schedule_publication_error(DummyResult(status="publish_failed", message="m"))
    assert status == 500
    status, _ = map_schedule_publication_error(
        DummyResult(status="status_update_failed", message="m")
    )
    assert status == 503
    status, _ = map_schedule_publication_error(DummyResult(status="other", message=None))
    assert status == 500


def test_final_decision_error_branches() -> None:
    status, _ = map_final_decision_error(DummyResult(status="unauthenticated", message="m"))
    assert status == 401
    status, _ = map_final_decision_error(DummyResult(status="forbidden", message="m"))
    assert status == 403
    status, _ = map_final_decision_error(DummyResult(status="invalid", message="m", errors=["e"]))
    assert status == 400
    status, _ = map_final_decision_error(DummyResult(status="notification_failed", message="m"))
    assert status == 500
    status, _ = map_final_decision_error(DummyResult(status="error", message="m"))
    assert status == 500
    status, _ = map_final_decision_error(DummyResult(status="other", message=None))
    assert status == 500


def test_final_decision_review_request_error_branches() -> None:
    status, _ = map_review_request_error(DummyResult(status="unauthenticated", message="m"))
    assert status == 401
    status, _ = map_review_request_error(DummyResult(status="forbidden", message="m"))
    assert status == 403
    status, _ = map_review_request_error(DummyResult(status="invalid", message="m"))
    assert status == 400
    status, _ = map_review_request_error(DummyResult(status="error", message="m"))
    assert status == 500
    status, _ = map_review_request_error(DummyResult(status="other", message=None))
    assert status == 500


def test_auth_error_mapper_default() -> None:
    status, _ = map_auth_result(AuthResult(status="other", message="m"))
    assert status == 500


def test_change_password_error_mapper_default() -> None:
    status, _ = map_password_change_result(DummyResult(status="other", message="m"))
    assert status == 500


def test_review_error_mappers_defaults() -> None:
    status, _ = map_review_form_error(DummyResult(status="other", message="m"))
    assert status == 500
    status, _ = map_invitation_error(DummyResult(status="other", message="m"))
    assert status == 500
    status, _ = map_notification_error(DummyResult(status="other", message="m"))
    assert status == 503
    status, _ = map_review_status_error(DummyResult(status="other", message="m"))
    assert status == 503
    status, _ = map_review_submission_error(DummyResult(status="other", message="m"))
    assert status == 500
    status, _ = map_assignment_error(DummyResult(status="other", message="m"))
    assert status == 500


def test_review_invitation_list_error_default() -> None:
    status, _ = map_invitation_list_error(DummyResult(status="other", message="m"))
    assert status == 500


def test_submission_error_mappers_defaults() -> None:
    status, _ = map_decision_error(DummyResult(status="other", message="m"))
    assert status == 500
    status, _ = map_draft_result(DummyResult(status="other", message="m"))
    assert status == 500
    status, _ = map_metadata_result(DummyResult(status="other", message="m"))
    assert status == 500
    status, _ = map_schedule_error(DummyResult(status="other", message="m"))
    assert status == 500
    status, _ = map_upload_result(DummyResult(status="other", message="m"))
    assert status == 500


def test_login_request_and_controller_missing_fields() -> None:
    req = LoginRequest(identifier=None, password=None)
    assert req.identifier is None
    service = DummyAuthService(AuthResult(status="missing_fields", message="err"))
    status, payload = handle_login(service, payload={})
    assert status == 400
    assert "errors" in payload


def test_change_password_controller_success_branch() -> None:
    class DummySessionManager:
        def __init__(self):
            self.terminated = False

        def terminate_all_sessions(self, user_id):
            self.terminated = True

    class DummyService:
        def change_password(self, *, user, current_password, new_password, confirm_password):
            return DummyResult(status="success", message="ok")

    user = type("User", (), {"id": "u1"})()
    status, payload = change_password(
        DummyService(),
        DummySessionManager(),
        user,
        {"current_password": "old", "new_password": "new", "confirm_password": "new"},
    )
    assert status == 200
    assert payload["message"] == "ok"


def test_review_form_access_branch() -> None:
    class DummyForm:
        paper_id = "p1"
        title = "Title"
        form_fields = {"q": "a"}
        manuscript_link = "http://example.com"

    class DummyService:
        def get_review_form(self, paper_id, reviewer_id, trace_id=None):
            return ReviewFormResult.ok(DummyForm())

    status, payload = get_review_form(DummyService(), "paper", "reviewer")
    assert status == 200
    assert payload["paperId"] == "p1"
    assert payload["manuscriptLink"] == "http://example.com"


def test_review_invitations_branch() -> None:
    class DummyService:
        def accept_invitation(self, invitation_id, reviewer_id, trace_id=None):
            return InvitationResponseResult.accepted()

        def list_pending_invitations(self, reviewer_id, trace_id=None):
            return InvitationListResult.ok([])

    status, payload = accept_invitation(DummyService(), "inv-1", "rev")
    assert status == 200
    assert payload["message"]

    status, payload = list_invitations(DummyService(), "rev")
    assert status == 200 and payload == []


def test_final_decision_controller_branches() -> None:
    class DummyService:
        def record_decision(self, *args, **kwargs):
            return FinalDecisionResult.success(paper_id="p1", decision="accept")

    status, payload = record_final_decision(
        DummyService(), paper_id="p1", editor_id="e1", is_editor=True, payload={"decisionValue": "accept"}
    )
    assert status == 200
    assert "message" in payload


def test_final_decision_review_request_controller_success() -> None:
    class DummyService:
        def request_reviews(self, *args, **kwargs):
            return DummyResult(status="success", message="ok")

    status, payload = request_additional_reviews(
        DummyService(), paper_id="p1", editor_id="e1", is_editor=True, payload={"reviewerIds": ["r1"]}
    )
    assert status == 200
    assert payload["message"] == "ok"


def test_conference_payment_branches_without_receipt() -> None:
    class DummyPayment:
        payment_id = "p1"
        status = "successful"
        receipt = None

    class DummyDetails:
        amount = 10.0
        currency = "USD"
        line_items = None

    class DummyResult:
        status = "success"
        registration = object()
        payment = DummyPayment()
        payment_details = DummyDetails()
        message = "ok"

    class DummyService:
        def pay_registration_fee(self, *args, **kwargs):
            return DummyResult()

    status, payload = pay_registration_fee(DummyService(), "a1", payload=None)
    assert status == 200
    assert "receipt" not in payload
    assert "line_items" not in payload

    class DummyStatusResult:
        status = "found"
        registration = type("R", (), {"registration_id": "r1", "status": "pending_unpaid"})()
        payment = None

    class DummyService2:
        def get_payment_status(self, *args, **kwargs):
            return DummyStatusResult()

    status, payload = get_payment_status(DummyService2(), "a1")
    assert status == 200
    assert payload["payment_status"] == "failed"


def test_conference_registration_branches_payload_none() -> None:
    class DummyResult:
        status = "registered"
        registration = type(
            "R", (), {"registration_id": "r1", "status": "registered"}
        )()
        message = "ok"
        payment_required = False

    class DummyService:
        def register_attendee(self, *args, **kwargs):
            return DummyResult()

    status, payload = register_for_conference(DummyService(), "a1", payload=None)
    assert status == 200
    assert payload["status"] == "registered"

    class DummyStatus:
        status = "found"
        registration = type(
            "R", (), {"registration_id": "r1", "status": "pending_unpaid"}
        )()

    class DummyService2:
        def get_registration_status(self, *args, **kwargs):
            return DummyStatus()

    status, payload = get_registration_status(DummyService2(), "a1")
    assert status == 200
    assert payload["payment_required"] is True


def test_schedule_generation_display_error_default() -> None:
    class DummyService:
        def get_generated_schedule(self, *args, **kwargs):
            return ScheduleDisplayResult(status="other", message="m")

    status, _ = get_generated_conference_schedule(DummyService(), "a1", True)
    assert status == 500


class DummyAuthService(AuthService):
    def __init__(self, result: AuthResult) -> None:
        self._result = result

    def authenticate(self, identifier, password):
        return self._result


def test_assigned_papers_error_branches() -> None:
    status, payload = map_assigned_papers_error(
        DummyResult(status="unauthenticated", message="m", redirect_to=None)
    )
    assert status == 401
    assert payload["redirect_to"] == "/login"
    status, _ = map_assigned_papers_error(DummyResult(status="forbidden", message="m"))
    assert status == 403


def test_conference_payment_success_details() -> None:
    from models.attendee_registration import AttendeeRegistration
    from models.payment_details import PaymentDetails
    from models.payment_record import PaymentRecord
    from services.conference_payment_service import PaymentResult

    class DummyService:
        def pay_registration_fee(self, attendee_id, payload, trace_id=None):
            registration = AttendeeRegistration(
                registration_id="reg-1",
                attendee_id="a1",
                attendance_type_id="t1",
                status="pending_unpaid",
            )
            payment = PaymentRecord(
                payment_id="pay-1",
                registration_id="reg-1",
                status="successful",
                transaction_id="txn",
                receipt="r1",
            )
            details = PaymentDetails(amount=100, currency="USD", line_items=["base"])
            return PaymentResult.success(registration, payment, details)

    status, payload = pay_registration_fee(DummyService(), "a1", {"method": "card"})
    assert status == 200
    assert payload["receipt"] == "r1"
    assert payload["amount"] == 100
    assert payload["line_items"] == ["base"]


def test_payment_status_found_no_payment() -> None:
    from models.attendee_registration import AttendeeRegistration
    from services.conference_payment_service import PaymentStatusResult

    class DummyService:
        def get_payment_status(self, attendee_id, trace_id=None):
            registration = AttendeeRegistration(
                registration_id="reg-1",
                attendee_id=attendee_id,
                attendance_type_id="t1",
                status="pending_unpaid",
            )
            return PaymentStatusResult.found(registration, None)

    status, payload = get_payment_status(DummyService(), "a1")
    assert status == 200
    assert payload["payment_status"] == "failed"


def test_payment_status_error_mapper_branches() -> None:
    from services.conference_payment_service import PaymentStatusResult

    status, _ = map_payment_status_error(PaymentStatusResult.unauthenticated())
    assert status == 401
    status, _ = map_payment_status_error(PaymentStatusResult(status="error", message="m"))
    assert status == 500


def test_registration_status_error_mapper_branches() -> None:
    from services.conference_registration_service import RegistrationStatusResult

    status, _ = map_registration_status_error(RegistrationStatusResult.unauthenticated())
    assert status == 401
    status, _ = map_registration_status_error(RegistrationStatusResult.not_found())
    assert status == 404
    status, _ = map_registration_status_error(
        RegistrationStatusResult(status="error", message="m")
    )
    assert status == 500


def test_final_decision_warning_response() -> None:
    class DummyService:
        def record_decision(self, **kwargs):
            return FinalDecisionResult.notification_failed("p1", "accepted")

    status, payload = record_final_decision(
        DummyService(), "p1", "e1", True, {"decisionValue": "accept"}
    )
    assert status == 200
    assert "warning" in payload


def test_final_decision_error_mapper_more_branches() -> None:
    status, _ = map_final_decision_error(DummyResult(status="duplicate", message="m"))
    assert status == 409
    status, _ = map_final_decision_error(DummyResult(status="incomplete", message="m"))
    assert status == 400
    status, _ = map_final_decision_error(DummyResult(status="error", message="m"))
    assert status == 500


def test_final_decision_review_request_success() -> None:
    class DummyService:
        def request_reviews(self, **kwargs):
            return type("R", (), {"status": "success", "message": "ok"})()

    status, payload = request_additional_reviews(
        DummyService(), "p1", "e1", True, {"reviewerIds": ["r1"]}
    )
    assert status == 200
    assert payload["message"] == "ok"


def test_change_password_missing_fields() -> None:
    class DummyService:
        def change_password(self, **kwargs):
            return DummyResult(status="success", message="ok")

    class DummySessionManager:
        def terminate_all_sessions(self, user_id):
            return None

    user = type("User", (), {"id": "u1"})()
    status, payload = change_password(DummyService(), DummySessionManager(), user, {})
    assert status == 400
    assert "errors" in payload


def test_review_form_access_without_link() -> None:
    class DummyForm:
        paper_id = "p1"
        title = "Title"
        form_fields = {"q": "a"}
        manuscript_link = None

    class DummyService:
        def get_review_form(self, paper_id, reviewer_id, trace_id=None):
            return ReviewFormResult.ok(DummyForm())

    status, payload = get_review_form(DummyService(), "paper", "reviewer")
    assert status == 200
    assert "manuscriptLink" not in payload


def test_review_invitation_error_mapper_branches() -> None:
    status, _ = map_invitation_error(InvitationResponseResult.unauthenticated())
    assert status == 401
    status, _ = map_invitation_error(InvitationResponseResult.forbidden())
    assert status == 403
    status, _ = map_invitation_error(InvitationResponseResult.limit_reached())
    assert status == 400


def test_review_invitations_reject_branch() -> None:
    class DummyService:
        def reject_invitation(self, invitation_id, reviewer_id, trace_id=None):
            return InvitationResponseResult.rejected()

    status, payload = reject_invitation(DummyService(), "inv-1", "rev")
    assert status == 200
    assert payload["message"]


def test_review_notifications_error_mapper_branches() -> None:
    status, _ = map_notification_error(
        NotificationListResult(status="unauthenticated", message="m")
    )
    assert status == 401
    status, _ = map_notification_error(NotificationListResult(status="forbidden", message="m"))
    assert status == 403
    status, _ = map_review_status_error(ReviewStatusResult(status="unauthenticated", message="m"))
    assert status == 401
    status, _ = map_review_status_error(ReviewStatusResult(status="forbidden", message="m"))
    assert status == 403


def test_decision_error_mapper_branches() -> None:
    status, _ = map_decision_error(DummyResult(status="unauthenticated", message="m"))
    assert status == 401
    status, _ = map_decision_error(DummyResult(status="forbidden", message="m"))
    assert status == 403
    status, _ = map_decision_error(DummyResult(status="error", message="m"))
    assert status == 500
    status, _ = map_decision_error(DummyResult(status="unavailable", message="m"))
    assert status == 503


def test_draft_error_mapper_branches() -> None:
    status, _ = map_draft_result(DummyResult(status="invalid", message="m"))
    assert status == 400
    status, _ = map_draft_result(DummyResult(status="missing_minimum", message="m"))
    assert status == 409


def test_metadata_error_mapper_branches() -> None:
    status, _ = map_metadata_result(DummyResult(status="missing_fields", message="m"))
    assert status == 400
    status, _ = map_metadata_result(DummyResult(status="invalid_fields", message="m"))
    assert status == 400
    status, _ = map_metadata_result(DummyResult(status="locked", message="m"))
    assert status == 409
    status, _ = map_metadata_result(DummyResult(status="validation_error", message="m"))
    assert status == 500
    status, _ = map_metadata_result(DummyResult(status="storage_error", message="m"))
    assert status == 500


def test_schedule_error_mapper_branches() -> None:
    status, _ = map_schedule_error(DummyResult(status="unauthenticated", message="m"))
    assert status == 401
    status, _ = map_schedule_error(DummyResult(status="forbidden", message="m"))
    assert status == 403
    status, _ = map_schedule_error(DummyResult(status="error", message="m"))
    assert status == 500


def test_manuscript_upload_missing_fields() -> None:
    class DummyService:
        def upload(self, **kwargs):
            return DummyResult(status="success", message="ok")

    status, payload = upload_manuscript(DummyService(), "s1", {"filename": "x"})
    assert status == 400
    assert "required" in payload["message"]


def test_conference_payment_missing_details_branch() -> None:
    class DummyPayment:
        payment_id = "pay-1"
        status = "successful"
        receipt = None

    class DummyResult:
        status = "success"
        registration = object()
        payment = DummyPayment()
        payment_details = None
        message = "ok"

    class DummyService:
        def pay_registration_fee(self, attendee_id, payload, trace_id=None):
            return DummyResult()

    status, payload = pay_registration_fee(DummyService(), "a1", {"method": "card"})
    assert status == 200
    assert "amount" not in payload


def test_payment_status_error_path_controller() -> None:
    class DummyService:
        def get_payment_status(self, attendee_id, trace_id=None):
            return PaymentStatusResult.unauthenticated()

    status, _ = get_payment_status(DummyService(), None)
    assert status == 401


def test_get_registration_status_error_path() -> None:
    class DummyService:
        def get_registration_status(self, attendee_id, trace_id=None):
            return RegistrationStatusResult.not_found()

    status, _ = get_registration_status(DummyService(), "a1")
    assert status == 404


def test_final_decision_view_error_mapper() -> None:
    status, _ = map_final_decision_view_error(
        DecisionViewResult(status="unauthenticated", message="m", redirect_to=None)
    )
    assert status == 401
    status, _ = map_final_decision_view_error(
        DecisionViewResult(status="forbidden", message="m")
    )
    assert status == 403
    status, _ = map_final_decision_view_error(DecisionViewResult(status="error", message="m"))
    assert status == 503


def test_get_final_decision_error_path() -> None:
    class DummyService:
        def get_decision(self, paper_id, author_id, trace_id=None):
            return DecisionViewResult.unauthenticated()

    status, _ = get_final_decision(DummyService(), "p1", None)
    assert status == 401


def test_final_decision_review_request_error_path() -> None:
    class DummyService:
        def request_reviews(self, **kwargs):
            return type("R", (), {"status": "error", "message": "m"})()

    status, _ = request_additional_reviews(DummyService(), "p1", "e1", True, {"reviewerIds": []})
    assert status == 500


def test_invitation_list_error_mapper_unauth() -> None:
    status, _ = map_invitation_list_error(
        InvitationListResult(status="unauthenticated", message="m", redirect_to=None)
    )
    assert status == 401


def test_invitation_list_error_mapper_forbidden() -> None:
    status, _ = map_invitation_list_error(InvitationListResult(status="forbidden", message="m"))
    assert status == 403


def test_reject_invitation_error_branch() -> None:
    class DummyService:
        def reject_invitation(self, invitation_id, reviewer_id, trace_id=None):
            return InvitationResponseResult.error()

    status, _ = reject_invitation(DummyService(), "inv-1", "rev")
    assert status == 500


def test_draft_error_mapper_storage_error_branch() -> None:
    status, _ = map_draft_result(DummyResult(status="storage_error", message="m"))
    assert status == 500


def test_draft_error_mapper_validation_error_branch() -> None:
    status, _ = map_draft_result(DummyResult(status="validation_error", message="m"))
    assert status == 500
