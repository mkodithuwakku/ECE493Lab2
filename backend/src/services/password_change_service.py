from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from services.auth_logger import AuthLogEntry, log_auth_event
from services.log_redactor import redact_credentials
from services.password_hasher import hash_password, verify_password
from services.password_policy import requirements_message, validate_password
from services.user_account_repository import UserAccountRecord, UserAccountRepository

INCORRECT_CURRENT_PASSWORD_MESSAGE = "Current password is incorrect."
MISMATCH_MESSAGE = "New password and confirmation do not match."
UPDATE_FAILURE_MESSAGE = "Password could not be updated. Please try again."
SUCCESS_MESSAGE = "Password changed successfully."


class PasswordUpdateError(RuntimeError):
    pass


@dataclass(frozen=True)
class PasswordChangeResult:
    status: str
    message: str
    requires_relogin: bool = False


class PasswordChangeService:
    def __init__(self, repository: UserAccountRepository) -> None:
        self._repository = repository

    def change_password(
        self,
        user: UserAccountRecord,
        current_password: str,
        new_password: str,
        confirm_password: str,
        trace_id: Optional[str] = None,
    ) -> PasswordChangeResult:
        if not verify_password(current_password, user.password_hash):
            return PasswordChangeResult(status="incorrect_current", message=INCORRECT_CURRENT_PASSWORD_MESSAGE)

        if new_password != confirm_password:
            return PasswordChangeResult(status="mismatch", message=MISMATCH_MESSAGE)

        if not validate_password(new_password):
            return PasswordChangeResult(status="policy_failed", message=requirements_message())

        try:
            new_hash = hash_password(new_password)
            self._repository.update_password(user.id, new_hash)
        except PasswordUpdateError:
            return PasswordChangeResult(status="update_failed", message=UPDATE_FAILURE_MESSAGE)

        log_auth_event(
            AuthLogEntry(
                event="password_change",
                user_id=user.id,
                message=redact_credentials("password_change"),
            )
        )

        return PasswordChangeResult(status="success", message=SUCCESS_MESSAGE, requires_relogin=True)
