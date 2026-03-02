from __future__ import annotations

from services.conference_configuration_service import ConfigurationResult


def map_configuration_error(result: ConfigurationResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "message": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "forbidden":
        return 403, {"message": result.message}
    if result.status == "invalid":
        return 400, {
            "message": result.message,
            "errors": result.errors or [],
        }
    if result.status == "error":
        return 503, {"message": result.message}
    if result.status == "save_error":
        return 500, {"message": result.message}
    return 500, {"message": result.message or "Configuration update failed."}
