from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.review_invitations import accept_invitation, list_invitations, reject_invitation
from models.review_invitation import ReviewInvitation
from models.reviewer import Reviewer
from services.invitation_service import (
    INVITATION_ACCEPTED_MESSAGE,
    INVITATION_LIMIT_MESSAGE,
    INVITATION_RESPONSE_ERROR_MESSAGE,
    INVITATION_REJECTED_MESSAGE,
    INVITATION_UNAUTHENTICATED_MESSAGE,
    LOGIN_REDIRECT,
    InvitationResponseError,
    InvitationRetrievalError,
    InvitationService,
)


def test_at_uc12_01_accept_invitation_success() -> None:
    invitation = ReviewInvitation(
        id="inv-1",
        paper_id="paper-1",
        reviewer_id="reviewer-1",
        status="pending",
    )
    reviewer = Reviewer(id="reviewer-1", assignment_count=0, assignment_limit=2)
    bundle = build_service(
        invitations=[invitation],
        reviewer=reviewer,
    )

    status, response = accept_invitation(bundle.service, "inv-1", "reviewer-1")

    assert status == 200
    assert response["message"] == INVITATION_ACCEPTED_MESSAGE
    assert bundle.assignment_repository.assignments == [("paper-1", "reviewer-1")]
    assert bundle.invitation_repository.accepted == ["inv-1"]


def test_at_uc12_02_reject_invitation_success() -> None:
    invitation = ReviewInvitation(
        id="inv-1",
        paper_id="paper-1",
        reviewer_id="reviewer-1",
        status="pending",
    )
    reviewer = Reviewer(id="reviewer-1", assignment_count=0, assignment_limit=2)
    bundle = build_service(
        invitations=[invitation],
        reviewer=reviewer,
    )

    status, response = reject_invitation(bundle.service, "inv-1", "reviewer-1")

    assert status == 200
    assert response["message"] == INVITATION_REJECTED_MESSAGE
    assert bundle.assignment_repository.assignments == []
    assert bundle.invitation_repository.rejected == ["inv-1"]
    assert bundle.editor_notifications.rejections == ["inv-1"]


def test_at_uc12_03_email_failure_still_allows_response() -> None:
    invitation = ReviewInvitation(
        id="inv-1",
        paper_id="paper-1",
        reviewer_id="reviewer-1",
        status="pending",
        email_failed=True,
    )
    reviewer = Reviewer(id="reviewer-1", assignment_count=0, assignment_limit=2)
    bundle = build_service(
        invitations=[invitation],
        reviewer=reviewer,
    )

    list_status, list_response = list_invitations(bundle.service, "reviewer-1")
    status, response = accept_invitation(bundle.service, "inv-1", "reviewer-1")

    assert list_status == 200
    assert list_response[0]["invitationId"] == "inv-1"
    assert status == 200
    assert response["message"] == INVITATION_ACCEPTED_MESSAGE
    assert bundle.email_notifications.failures == ["inv-1"]


def test_at_uc12_04_unauthenticated_redirect() -> None:
    invitation = ReviewInvitation(
        id="inv-1",
        paper_id="paper-1",
        reviewer_id="reviewer-1",
        status="pending",
    )
    reviewer = Reviewer(id="reviewer-1", assignment_count=0, assignment_limit=2)
    bundle = build_service(
        invitations=[invitation],
        reviewer=reviewer,
    )

    status, response = list_invitations(bundle.service, None)

    assert status == 401
    assert response["message"] == INVITATION_UNAUTHENTICATED_MESSAGE
    assert response["redirect_to"] == LOGIN_REDIRECT


def test_at_uc12_05_assignment_limit_reached() -> None:
    invitation = ReviewInvitation(
        id="inv-1",
        paper_id="paper-1",
        reviewer_id="reviewer-1",
        status="pending",
    )
    reviewer = Reviewer(id="reviewer-1", assignment_count=3, assignment_limit=3)
    bundle = build_service(
        invitations=[invitation],
        reviewer=reviewer,
    )

    status, response = accept_invitation(bundle.service, "inv-1", "reviewer-1")

    assert status == 400
    assert response["message"] == INVITATION_LIMIT_MESSAGE
    assert bundle.assignment_repository.assignments == []
    assert bundle.editor_notifications.limits == ["inv-1"]


def test_at_uc12_06_response_recording_error() -> None:
    invitation = ReviewInvitation(
        id="inv-1",
        paper_id="paper-1",
        reviewer_id="reviewer-1",
        status="pending",
    )
    reviewer = Reviewer(id="reviewer-1", assignment_count=0, assignment_limit=2)
    bundle = build_service(
        invitations=[invitation],
        reviewer=reviewer,
        fail_response=True,
    )

    status, response = accept_invitation(bundle.service, "inv-1", "reviewer-1")

    assert status == 500
    assert response["message"] == INVITATION_RESPONSE_ERROR_MESSAGE
    assert bundle.assignment_repository.assignments == []
    assert bundle.invitation_repository.accepted == []


class StubInvitationRepository:
    def __init__(
        self,
        invitations: list[ReviewInvitation],
        *,
        fail_list: bool = False,
        fail_response: bool = False,
    ) -> None:
        self._invitations = {inv.id: inv for inv in invitations}
        self._fail_list = fail_list
        self._fail_response = fail_response
        self.accepted: list[str] = []
        self.rejected: list[str] = []

    def list_pending(self, reviewer_id: str) -> list[ReviewInvitation]:
        if self._fail_list:
            raise InvitationRetrievalError("list failed")
        return [
            inv
            for inv in self._invitations.values()
            if inv.reviewer_id == reviewer_id and inv.status == "pending"
        ]

    def fetch_invitation(self, invitation_id: str) -> ReviewInvitation:
        invitation = self._invitations[invitation_id]
        return invitation

    def record_acceptance(self, invitation_id: str) -> None:
        if self._fail_response:
            raise InvitationResponseError("accept failed")
        self.accepted.append(invitation_id)

    def record_rejection(self, invitation_id: str) -> None:
        if self._fail_response:
            raise InvitationResponseError("reject failed")
        self.rejected.append(invitation_id)


class StubReviewerRepository:
    def __init__(self, reviewer: Reviewer) -> None:
        self._reviewer = reviewer

    def fetch_reviewer(self, reviewer_id: str) -> Reviewer:
        return self._reviewer


class StubAssignmentRepository:
    def __init__(self) -> None:
        self.assignments: list[tuple[str, str]] = []

    def add_assignment(self, assignment) -> None:
        self.assignments.append((assignment.paper_id, assignment.reviewer_id))


class StubEditorNotifications:
    def __init__(self) -> None:
        self.rejections: list[str] = []
        self.limits: list[str] = []

    def notify_rejection(self, invitation: ReviewInvitation) -> None:
        self.rejections.append(invitation.id)

    def notify_limit(self, invitation: ReviewInvitation) -> None:
        self.limits.append(invitation.id)


class StubEmailNotifications:
    def __init__(self) -> None:
        self.failures: list[str] = []

    def notify_invitation_failed(self, invitation: ReviewInvitation) -> None:
        self.failures.append(invitation.id)


class ServiceBundle:
    def __init__(self, service: InvitationService) -> None:
        self.service = service
        self.invitation_repository: StubInvitationRepository = service._invitation_repository  # type: ignore[attr-defined]
        self.assignment_repository: StubAssignmentRepository = service._assignment_repository  # type: ignore[attr-defined]
        self.editor_notifications: StubEditorNotifications = service._editor_notifications  # type: ignore[attr-defined]
        self.email_notifications: StubEmailNotifications = service._email_notifications  # type: ignore[attr-defined]


def build_service(
    *,
    invitations: list[ReviewInvitation],
    reviewer: Reviewer,
    fail_response: bool = False,
) -> ServiceBundle:
    invitation_repository = StubInvitationRepository(
        invitations,
        fail_response=fail_response,
    )
    reviewer_repository = StubReviewerRepository(reviewer)
    assignment_repository = StubAssignmentRepository()
    editor_notifications = StubEditorNotifications()
    email_notifications = StubEmailNotifications()
    service = InvitationService(
        invitation_repository=invitation_repository,
        reviewer_repository=reviewer_repository,
        assignment_repository=assignment_repository,
        editor_notifications=editor_notifications,
        email_notifications=email_notifications,
    )
    return ServiceBundle(service)
