from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable

from services.auth_logger import AuthLogEntry, log_auth_event
from services.identifier_normalizer import normalize_identifier
from services.lockout_policy import (
    LockoutState,
    compute_lockout_until,
    is_locked,
    should_lock,
    within_lockout_window,
)
from services.session_manager import SessionManager
from services.user_account_repository import UserAccountRecord, UserAccountRepository

REQUIRED_FIELDS_MESSAGE = "Username/email and password are required."
INVALID_CREDENTIALS_MESSAGE = "Invalid credentials."
ACCOUNT_INACTIVE_MESSAGE = "Account is inactive. Please contact support."
SERVICE_UNAVAILABLE_MESSAGE = "Authentication service is temporarily unavailable."
CRITICAL_FAILURE_MESSAGE = "Authentication cannot be completed at this time."
LOGIN_SUCCESS_MESSAGE = "Login successful."
LOCKOUT_THRESHOLD = 5


class AuthServiceUnavailableError(RuntimeError):
    pass


@dataclass(frozen=True)
class AuthResult:
    status: str
    message: str
    remaining_attempts: int | None = None


class AuthService:
    def __init__(
        self,
        repository: UserAccountRepository,
        session_manager: SessionManager,
        verify_password: Callable[[str, str], bool],
        clock: Callable[[], datetime],
    ) -> None:
        self._repository = repository
        self._session_manager = session_manager
        self._verify_password = verify_password
        self._clock = clock

    def authenticate(self, identifier: str | None, password: str | None) -> AuthResult:
        if not identifier or not password:
            return AuthResult(status="missing_fields", message=REQUIRED_FIELDS_MESSAGE)

        now = self._clock()
        normalized = normalize_identifier(identifier)

        try:
            account = self._repository.find_by_identifier(normalized)
        except AuthServiceUnavailableError:
            return AuthResult(status="service_unavailable", message=SERVICE_UNAVAILABLE_MESSAGE)
        except Exception:
            return AuthResult(status="critical_error", message=CRITICAL_FAILURE_MESSAGE)

        if not account:
            return AuthResult(
                status="invalid_credentials",
                message=INVALID_CREDENTIALS_MESSAGE,
                remaining_attempts=LOCKOUT_THRESHOLD - 1,
            )

        lockout_state = LockoutState(
            failed_attempts=account.failed_login_attempts,
            lockout_until=account.lockout_until,
            last_failed_login_at=account.last_failed_login_at,
        )

        if account.status == "disabled":
            return AuthResult(status="disabled", message=ACCOUNT_INACTIVE_MESSAGE)

        if account.status == "locked" and is_locked(lockout_state, now):
            return AuthResult(status="locked", message=ACCOUNT_INACTIVE_MESSAGE)

        if account.status == "locked" and not is_locked(lockout_state, now):
            self._repository.clear_login_failures(account.id)
            account = UserAccountRecord(
                **{
                    **account.__dict__,
                    "status": "active",
                    "failed_login_attempts": 0,
                    "lockout_until": None,
                    "last_failed_login_at": None,
                }
            )

        try:
            valid = self._verify_password(password, account.password_hash)
        except Exception:
            log_auth_event(AuthLogEntry(event="auth_error", user_id=account.id))
            return AuthResult(status="critical_error", message=CRITICAL_FAILURE_MESSAGE)

        if not valid:
            attempts = account.failed_login_attempts
            if within_lockout_window(account.last_failed_login_at, now):
                attempts += 1
            else:
                attempts = 1

            lockout_until = account.lockout_until
            status = account.status
            if should_lock(attempts):
                lockout_until = compute_lockout_until(now)
                status = "locked"

            self._repository.update_login_failure(
                account.id,
                attempts,
                lockout_until,
                now,
                status=status,
            )
            remaining = max(0, LOCKOUT_THRESHOLD - attempts)
            return AuthResult(
                status="invalid_credentials",
                message=INVALID_CREDENTIALS_MESSAGE,
                remaining_attempts=remaining,
            )

        try:
            self._repository.clear_login_failures(account.id)
            self._session_manager.create_session(account.id)
            log_auth_event(AuthLogEntry(event="login_success", user_id=account.id))
            return AuthResult(status="success", message=LOGIN_SUCCESS_MESSAGE)
        except Exception:
            log_auth_event(AuthLogEntry(event="auth_error", user_id=account.id))
            return AuthResult(status="critical_error", message=CRITICAL_FAILURE_MESSAGE)
