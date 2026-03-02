from __future__ import annotations

from services.invitation_service import InvitationListResult, InvitationResponseResult


def map_invitation_list_error(result: InvitationListResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "message": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "forbidden":
        return 403, {"message": result.message}
    return 500, {"message": result.message or "Invitation retrieval failed."}


def map_invitation_error(result: InvitationResponseResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "message": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "forbidden":
        return 403, {"message": result.message}
    if result.status == "limit":
        return 400, {"message": result.message}
    return 500, {"message": result.message or "Invitation response failed."}
