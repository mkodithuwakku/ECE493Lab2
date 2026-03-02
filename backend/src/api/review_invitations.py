from __future__ import annotations

from api.review_invitation_error_mapper import map_invitation_error, map_invitation_list_error
from services.invitation_service import InvitationService


def list_invitations(
    service: InvitationService,
    reviewer_id: str | None,
    trace_id: str | None = None,
) -> tuple[int, dict | list[dict]]:
    result = service.list_pending_invitations(reviewer_id=reviewer_id, trace_id=trace_id)

    if result.status == "ok":
        return 200, [
            {
                "invitationId": invitation.id,
                "paperId": invitation.paper_id,
                "status": invitation.status,
            }
            for invitation in (result.invitations or [])
        ]

    return map_invitation_list_error(result)


def accept_invitation(
    service: InvitationService,
    invitation_id: str,
    reviewer_id: str | None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    result = service.accept_invitation(
        invitation_id=invitation_id,
        reviewer_id=reviewer_id,
        trace_id=trace_id,
    )

    if result.status == "accepted":
        return 200, {"message": result.message}

    return map_invitation_error(result)


def reject_invitation(
    service: InvitationService,
    invitation_id: str,
    reviewer_id: str | None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    result = service.reject_invitation(
        invitation_id=invitation_id,
        reviewer_id=reviewer_id,
        trace_id=trace_id,
    )

    if result.status == "rejected":
        return 200, {"message": result.message}

    return map_invitation_error(result)
