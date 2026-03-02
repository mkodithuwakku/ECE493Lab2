from __future__ import annotations

from services.schedule_service import ScheduleResult


def map_schedule_error(result: ScheduleResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "message": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "forbidden":
        return 403, {"message": result.message}
    if result.status == "error":
        return 500, {"message": result.message}
    return 500, {"message": result.message or "Schedule retrieval failed."}
