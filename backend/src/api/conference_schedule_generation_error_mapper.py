from __future__ import annotations

from services.schedule_generation_service import (
    ScheduleDisplayResult,
    ScheduleGenerationResult,
)


def map_schedule_generation_error(result: ScheduleGenerationResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "message": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "forbidden":
        return 403, {"message": result.message}
    if result.status in {"no_papers", "constraint"}:
        payload = {"message": result.message}
        if result.constraint_type:
            payload["constraint_type"] = result.constraint_type
        return 400, payload
    if result.status == "generation_failed":
        return 500, {"message": result.message}
    if result.status == "storage_failed":
        return 503, {"message": result.message}
    return 500, {"message": result.message or "Schedule generation failed."}


def map_schedule_display_error(result: ScheduleDisplayResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "message": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "forbidden":
        return 403, {"message": result.message}
    if result.status == "not_found":
        return 404, {"message": result.message}
    if result.status == "error":
        return 503, {"message": result.message}
    return 500, {"message": result.message or "Schedule retrieval failed."}
