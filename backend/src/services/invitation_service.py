from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from models.paper_assignment import PaperAssignment
from models.review_invitation import ReviewInvitation
from models.reviewer import Reviewer
from services.authorization import is_reviewer
from services.invitation_logger import InvitationLogContext, log_invitation_event

INVITATION_ACCEPTED_MESSAGE = "Review invitation accepted."
INVITATION_REJECTED_MESSAGE = "Review invitation rejected."
INVITATION_RETRIEVAL_ERROR_MESSAGE = "Review invitations could not be retrieved."
INVITATION_RESPONSE_ERROR_MESSAGE = "Invitation response could not be processed."
INVITATION_FORBIDDEN_MESSAGE = "Review invitation access is restricted to the reviewer."
INVITATION_UNAUTHENTICATED_MESSAGE = "Please log in to respond to the invitation."
INVITATION_LIMIT_MESSAGE = "Assignment limit reached. Invitation cannot be accepted."
LOGIN_REDIRECT = "/login"


class InvitationRetrievalError(RuntimeError):
    pass


class InvitationResponseError(RuntimeError):
    pass


class InvitationRepository(Protocol):
    def list_pending(self, reviewer_id: str) -> list[ReviewInvitation]:
        ...

    def fetch_invitation(self, invitation_id: str) -> ReviewInvitation:
        ...

    def record_acceptance(self, invitation_id: str) -> None:
        ...

    def record_rejection(self, invitation_id: str) -> None:
        ...


class ReviewerRepository(Protocol):
    def fetch_reviewer(self, reviewer_id: str) -> Reviewer:
        ...


class AssignmentRepository(Protocol):
    def add_assignment(self, assignment: PaperAssignment) -> None:
        ...


class EditorNotificationService(Protocol):
    def notify_rejection(self, invitation: ReviewInvitation) -> None:
        ...

    def notify_limit(self, invitation: ReviewInvitation) -> None:
        ...


class EmailNotificationService(Protocol):
    def notify_invitation_failed(self, invitation: ReviewInvitation) -> None:
        ...


@dataclass(frozen=True)
class InvitationListResult:
    status: str
    invitations: list[ReviewInvitation] | None = None
    message: str | None = None
    redirect_to: str | None = None

    @classmethod
    def ok(cls, invitations: list[ReviewInvitation]) -> "InvitationListResult":
        return cls(status="ok", invitations=invitations)

    @classmethod
    def unauthenticated(cls) -> "InvitationListResult":
        return cls(
            status="unauthenticated",
            message=INVITATION_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def forbidden(cls) -> "InvitationListResult":
        return cls(status="forbidden", message=INVITATION_FORBIDDEN_MESSAGE)

    @classmethod
    def error(cls) -> "InvitationListResult":
        return cls(status="error", message=INVITATION_RETRIEVAL_ERROR_MESSAGE)


@dataclass(frozen=True)
class InvitationResponseResult:
    status: str
    message: str | None = None
    redirect_to: str | None = None

    @classmethod
    def accepted(cls) -> "InvitationResponseResult":
        return cls(status="accepted", message=INVITATION_ACCEPTED_MESSAGE)

    @classmethod
    def rejected(cls) -> "InvitationResponseResult":
        return cls(status="rejected", message=INVITATION_REJECTED_MESSAGE)

    @classmethod
    def limit_reached(cls) -> "InvitationResponseResult":
        return cls(status="limit", message=INVITATION_LIMIT_MESSAGE)

    @classmethod
    def unauthenticated(cls) -> "InvitationResponseResult":
        return cls(
            status="unauthenticated",
            message=INVITATION_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def forbidden(cls) -> "InvitationResponseResult":
        return cls(status="forbidden", message=INVITATION_FORBIDDEN_MESSAGE)

    @classmethod
    def error(cls) -> "InvitationResponseResult":
        return cls(status="error", message=INVITATION_RESPONSE_ERROR_MESSAGE)


class InvitationService:
    def __init__(
        self,
        invitation_repository: InvitationRepository,
        reviewer_repository: ReviewerRepository,
        assignment_repository: AssignmentRepository,
        editor_notifications: EditorNotificationService,
        email_notifications: EmailNotificationService,
    ) -> None:
        self._invitation_repository = invitation_repository
        self._reviewer_repository = reviewer_repository
        self._assignment_repository = assignment_repository
        self._editor_notifications = editor_notifications
        self._email_notifications = email_notifications

    def list_pending_invitations(
        self,
        reviewer_id: str | None,
        trace_id: Optional[str] = None,
    ) -> InvitationListResult:
        context = InvitationLogContext(invitation_id=None, reviewer_id=reviewer_id, trace_id=trace_id)

        if not reviewer_id:
            log_invitation_event("invitation_list_unauthenticated", context)
            return InvitationListResult.unauthenticated()

        try:
            invitations = self._invitation_repository.list_pending(reviewer_id)
        except InvitationRetrievalError:
            log_invitation_event(
                "invitation_list_error",
                context,
                INVITATION_RETRIEVAL_ERROR_MESSAGE,
            )
            return InvitationListResult.error()
        except Exception:
            log_invitation_event(
                "invitation_list_error",
                context,
                INVITATION_RETRIEVAL_ERROR_MESSAGE,
            )
            return InvitationListResult.error()

        log_invitation_event("invitation_list_accessed", context)
        return InvitationListResult.ok(invitations)

    def accept_invitation(
        self,
        invitation_id: str,
        reviewer_id: str | None,
        trace_id: Optional[str] = None,
    ) -> InvitationResponseResult:
        return self._respond(
            invitation_id=invitation_id,
            reviewer_id=reviewer_id,
            trace_id=trace_id,
            response="accept",
        )

    def reject_invitation(
        self,
        invitation_id: str,
        reviewer_id: str | None,
        trace_id: Optional[str] = None,
    ) -> InvitationResponseResult:
        return self._respond(
            invitation_id=invitation_id,
            reviewer_id=reviewer_id,
            trace_id=trace_id,
            response="reject",
        )

    def _respond(
        self,
        *,
        invitation_id: str,
        reviewer_id: str | None,
        trace_id: Optional[str],
        response: str,
    ) -> InvitationResponseResult:
        context = InvitationLogContext(
            invitation_id=invitation_id,
            reviewer_id=reviewer_id,
            trace_id=trace_id,
        )

        if not reviewer_id:
            log_invitation_event("invitation_unauthenticated", context)
            return InvitationResponseResult.unauthenticated()

        try:
            invitation = self._invitation_repository.fetch_invitation(invitation_id)
        except InvitationRetrievalError:
            log_invitation_event(
                "invitation_fetch_error",
                context,
                INVITATION_RESPONSE_ERROR_MESSAGE,
            )
            return InvitationResponseResult.error()
        except Exception:
            log_invitation_event(
                "invitation_fetch_error",
                context,
                INVITATION_RESPONSE_ERROR_MESSAGE,
            )
            return InvitationResponseResult.error()

        if not is_reviewer(reviewer_id, invitation.reviewer_id):
            log_invitation_event("invitation_access_denied", context, INVITATION_FORBIDDEN_MESSAGE)
            return InvitationResponseResult.forbidden()

        if invitation.email_failed:
            log_invitation_event("invitation_email_failed", context, "Invitation email failed")
            self._email_notifications.notify_invitation_failed(invitation)

        if response == "accept":
            return self._handle_accept(invitation, reviewer_id, context)

        return self._handle_reject(invitation, context)

    def _handle_accept(
        self,
        invitation: ReviewInvitation,
        reviewer_id: str,
        context: InvitationLogContext,
    ) -> InvitationResponseResult:
        try:
            reviewer = self._reviewer_repository.fetch_reviewer(reviewer_id)
        except Exception:
            log_invitation_event(
                "invitation_reviewer_error",
                context,
                INVITATION_RESPONSE_ERROR_MESSAGE,
            )
            return InvitationResponseResult.error()

        if reviewer.assignment_count >= reviewer.assignment_limit:
            log_invitation_event("invitation_limit_reached", context, INVITATION_LIMIT_MESSAGE)
            self._editor_notifications.notify_limit(invitation)
            return InvitationResponseResult.limit_reached()

        try:
            self._invitation_repository.record_acceptance(invitation.id)
            self._assignment_repository.add_assignment(
                PaperAssignment(paper_id=invitation.paper_id, reviewer_id=reviewer_id)
            )
        except InvitationResponseError:
            log_invitation_event(
                "invitation_response_error",
                context,
                INVITATION_RESPONSE_ERROR_MESSAGE,
            )
            return InvitationResponseResult.error()
        except Exception:
            log_invitation_event(
                "invitation_response_error",
                context,
                INVITATION_RESPONSE_ERROR_MESSAGE,
            )
            return InvitationResponseResult.error()

        log_invitation_event("invitation_accepted", context, INVITATION_ACCEPTED_MESSAGE)
        return InvitationResponseResult.accepted()

    def _handle_reject(
        self,
        invitation: ReviewInvitation,
        context: InvitationLogContext,
    ) -> InvitationResponseResult:
        try:
            self._invitation_repository.record_rejection(invitation.id)
            self._editor_notifications.notify_rejection(invitation)
        except InvitationResponseError:
            log_invitation_event(
                "invitation_response_error",
                context,
                INVITATION_RESPONSE_ERROR_MESSAGE,
            )
            return InvitationResponseResult.error()
        except Exception:
            log_invitation_event(
                "invitation_response_error",
                context,
                INVITATION_RESPONSE_ERROR_MESSAGE,
            )
            return InvitationResponseResult.error()

        log_invitation_event("invitation_rejected", context, INVITATION_REJECTED_MESSAGE)
        return InvitationResponseResult.rejected()
