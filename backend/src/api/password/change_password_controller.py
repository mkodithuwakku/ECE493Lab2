from __future__ import annotations

from api.password.change_password_error_mapper import map_password_change_result
from services.password_change_service import PasswordChangeResult, PasswordChangeService
from services.user_account_repository import UserAccountRecord


def change_password(
    service: PasswordChangeService,
    session_manager,
    user: UserAccountRecord,
    payload: dict | None,
) -> tuple[int, dict]:
    payload = payload or {}
    current_password = payload.get("current_password")
    new_password = payload.get("new_password")
    confirm_password = payload.get("confirm_password")

    if not current_password or not new_password or not confirm_password:
        return 400, {"errors": ["Current password, new password, and confirmation are required."]}

    result = service.change_password(
        user=user,
        current_password=current_password,
        new_password=new_password,
        confirm_password=confirm_password,
    )

    if result.status == "success":
        session_manager.terminate_all_sessions(user.id)
        return 200, {"message": result.message, "requires_relogin": True}

    return map_password_change_result(result)
