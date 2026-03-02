from __future__ import annotations

from services.auth_service import AuthResult


def map_auth_result(result: AuthResult) -> tuple[int, dict]:
    if result.status == "missing_fields":
        return 400, {"errors": [result.message]}
    if result.status == "invalid_credentials":
        return 401, {
            "message": result.message,
            "remaining_attempts": result.remaining_attempts or 0,
        }
    if result.status in {"locked", "disabled"}:
        return 403, {"message": result.message, "status": result.status}
    if result.status == "service_unavailable":
        return 503, {"message": result.message}
    if result.status == "critical_error":
        return 500, {"message": result.message}
    return 500, {"message": result.message}
