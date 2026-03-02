from __future__ import annotations

from services.password_change_service import PasswordChangeResult


def map_password_change_result(result: PasswordChangeResult) -> tuple[int, dict]:
    if result.status == "incorrect_current":
        return 401, {"message": result.message}
    if result.status == "policy_failed":
        return 422, {"message": result.message}
    if result.status == "mismatch":
        return 422, {"message": result.message}
    if result.status == "update_failed":
        return 500, {"message": result.message}
    return 500, {"message": result.message}
