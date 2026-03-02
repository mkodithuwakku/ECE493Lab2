from __future__ import annotations

from services.conference_registration_service import RegistrationResult, RegistrationStatusResult


def map_conference_registration_error(result: RegistrationResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "error": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "closed":
        return 403, {"error": result.message}
    if result.status == "invalid_type":
        return 400, {"error": result.message}
    if result.status == "storage_error":
        return 500, {"error": result.message}
    return 500, {"error": result.message or "Registration failed."}


def map_registration_status_error(result: RegistrationStatusResult) -> tuple[int, dict]:
    if result.status == "unauthenticated":
        return 401, {
            "error": result.message,
            "redirect_to": result.redirect_to or "/login",
        }
    if result.status == "not_found":
        return 404, {"error": result.message}
    return 500, {"error": result.message or "Registration lookup failed."}
