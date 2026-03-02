from __future__ import annotations

from services.schedule_publication_service import PublicationResult


def map_schedule_publication_error(result: PublicationResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "message": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "forbidden":
        return 403, {"message": result.message}
    if result.status in {"not_ready", "not_found"}:
        return 400, {"message": result.message}
    if result.status == "error":
        return 503, {"message": result.message}
    if result.status == "publish_failed":
        return 500, {"message": result.message}
    if result.status == "status_update_failed":
        return 503, {"message": result.message}
    return 500, {"message": result.message or "Publication failed."}
