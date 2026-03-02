from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.login.login_controller import handle_login
from services.auth_service import (
    ACCOUNT_INACTIVE_MESSAGE,
    CRITICAL_FAILURE_MESSAGE,
    INVALID_CREDENTIALS_MESSAGE,
    LOGIN_SUCCESS_MESSAGE,
    REQUIRED_FIELDS_MESSAGE,
    SERVICE_UNAVAILABLE_MESSAGE,
    AuthService,
    AuthServiceUnavailableError,
)
from services.session_manager import Session, SessionManager
from services.user_account_repository import UserAccountRecord, UserAccountRepository


class StubUserAccountRepository(UserAccountRepository):
    def __init__(self, account: UserAccountRecord | None, *, fail_on_lookup: bool = False) -> None:
        self._account = account
        self._fail_on_lookup = fail_on_lookup
        self.failures: list[tuple[str, int, datetime | None]] = []
        self.clears: list[str] = []

    def find_by_identifier(self, identifier: str) -> UserAccountRecord | None:
        if self._fail_on_lookup:
            raise AuthServiceUnavailableError("auth store down")
        return self._account

    def update_login_failure(
        self,
        user_id: str,
        attempts: int,
        lockout_until: datetime | None,
        last_failed_login_at: datetime | None,
        status: str | None = None,
    ) -> None:
        self.failures.append((user_id, attempts, lockout_until))
        if self._account:
            self._account = UserAccountRecord(
                **{
                    **self._account.__dict__,
                    "failed_login_attempts": attempts,
                    "lockout_until": lockout_until,
                    "last_failed_login_at": last_failed_login_at,
                    "status": status or self._account.status,
                }
            )

    def clear_login_failures(self, user_id: str) -> None:
        self.clears.append(user_id)


class StubSessionManager(SessionManager):
    def __init__(self) -> None:
        self.sessions: list[Session] = []

    def create_session(self, user_id: str) -> Session:
        session = Session(id="s1", user_id=user_id, created_at=datetime.now(timezone.utc))
        self.sessions.append(session)
        return session


def build_service(account: UserAccountRecord | None, *, fail_on_lookup: bool = False, verify_ok: bool = True):
    repo = StubUserAccountRepository(account, fail_on_lookup=fail_on_lookup)
    session_manager = StubSessionManager()
    service = AuthService(
        repository=repo,
        session_manager=session_manager,
        verify_password=lambda password, password_hash: verify_ok,
        clock=lambda: datetime.now(timezone.utc),
    )
    return service, repo, session_manager


def test_at_uc04_01_success_login_redirect() -> None:
    account = UserAccountRecord(
        id="u1",
        username="user",
        email="user@example.com",
        password_hash="hash",
        status="active",
        failed_login_attempts=0,
        lockout_until=None,
    )
    service, repo, session_manager = build_service(account, verify_ok=True)

    status, payload = handle_login(service, {"identifier": "user", "password": "pass"})

    assert status == 200
    assert payload["message"] == LOGIN_SUCCESS_MESSAGE
    assert payload["redirect_to"] == "/home"
    assert len(session_manager.sessions) == 1


def test_at_uc04_02_missing_fields() -> None:
    service, _, _ = build_service(None)

    status, payload = handle_login(service, {"identifier": "", "password": ""})

    assert status == 400
    assert payload["errors"] == [REQUIRED_FIELDS_MESSAGE]


def test_at_uc04_03_invalid_credentials_remaining_attempts() -> None:
    account = UserAccountRecord(
        id="u1",
        username="user",
        email="user@example.com",
        password_hash="hash",
        status="active",
        failed_login_attempts=0,
        lockout_until=None,
    )
    service, repo, _ = build_service(account, verify_ok=False)

    status, payload = handle_login(service, {"identifier": "user", "password": "wrong"})

    assert status == 401
    assert payload["message"] == INVALID_CREDENTIALS_MESSAGE
    assert payload["remaining_attempts"] == 4
    assert repo.failures


def test_at_uc04_04_locked_account() -> None:
    account = UserAccountRecord(
        id="u1",
        username="user",
        email="user@example.com",
        password_hash="hash",
        status="locked",
        failed_login_attempts=5,
        lockout_until=datetime.now(timezone.utc) + timedelta(minutes=5),
    )
    service, _, _ = build_service(account, verify_ok=True)

    status, payload = handle_login(service, {"identifier": "user", "password": "pass"})

    assert status == 403
    assert payload["message"] == ACCOUNT_INACTIVE_MESSAGE
    assert payload["status"] == "locked"


def test_at_uc04_05_service_unavailable() -> None:
    account = UserAccountRecord(
        id="u1",
        username="user",
        email="user@example.com",
        password_hash="hash",
        status="active",
        failed_login_attempts=0,
        lockout_until=None,
    )
    service, _, _ = build_service(account, fail_on_lookup=True)

    status, payload = handle_login(service, {"identifier": "user", "password": "pass"})

    assert status == 503
    assert payload["message"] == SERVICE_UNAVAILABLE_MESSAGE


def test_at_uc04_06_critical_failure() -> None:
    account = UserAccountRecord(
        id="u1",
        username="user",
        email="user@example.com",
        password_hash="hash",
        status="active",
        failed_login_attempts=0,
        lockout_until=None,
    )

    def failing_verify(password: str, password_hash: str) -> bool:
        raise Exception("boom")

    repo = StubUserAccountRepository(account)
    session_manager = StubSessionManager()
    service = AuthService(
        repository=repo,
        session_manager=session_manager,
        verify_password=failing_verify,
        clock=lambda: datetime.now(timezone.utc),
    )

    status, payload = handle_login(service, {"identifier": "user", "password": "pass"})

    assert status == 500
    assert payload["message"] == CRITICAL_FAILURE_MESSAGE
    assert len(session_manager.sessions) == 0
