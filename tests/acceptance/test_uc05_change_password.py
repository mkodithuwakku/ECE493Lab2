from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.password.change_password_controller import change_password
from services.password_change_service import (
    INCORRECT_CURRENT_PASSWORD_MESSAGE,
    MISMATCH_MESSAGE,
    SUCCESS_MESSAGE,
    UPDATE_FAILURE_MESSAGE,
    PasswordChangeService,
    PasswordUpdateError,
)
from services.password_hasher import hash_password
from services.password_policy import requirements_message
from services.session_manager import SessionManager
from services.user_account_repository import UserAccountRecord, UserAccountRepository


class StubSessionManager(SessionManager):
    def __init__(self) -> None:
        self.terminated: list[str] = []

    def create_session(self, user_id: str):
        raise NotImplementedError

    def terminate_all_sessions(self, user_id: str) -> None:
        self.terminated.append(user_id)


class StubUserAccountRepository(UserAccountRepository):
    def __init__(self, user: UserAccountRecord, *, fail_on_update: bool = False) -> None:
        self.user = user
        self.fail_on_update = fail_on_update
        self.updated_hash: str | None = None

    def find_by_identifier(self, identifier: str):
        raise NotImplementedError

    def update_password(self, user_id: str, password_hash: str) -> None:
        if self.fail_on_update:
            raise PasswordUpdateError("update failed")
        self.updated_hash = password_hash

    def update_login_failure(self, user_id, attempts, lockout_until, last_failed_login_at, status=None):
        raise NotImplementedError

    def clear_login_failures(self, user_id: str) -> None:
        raise NotImplementedError


def build_user(password: str) -> UserAccountRecord:
    return UserAccountRecord(
        id="u1",
        username="user",
        email="user@example.com",
        password_hash=hash_password(password),
        status="active",
        failed_login_attempts=0,
        lockout_until=None,
        last_failed_login_at=None,
    )


def test_at_uc05_01_change_password_success() -> None:
    user = build_user("OldPass!1")
    repo = StubUserAccountRepository(user)
    service = PasswordChangeService(repo)
    session_manager = StubSessionManager()

    status, payload = change_password(
        service,
        session_manager,
        user,
        {
            "current_password": "OldPass!1",
            "new_password": "NewPass!1",
            "confirm_password": "NewPass!1",
        },
    )

    assert status == 200
    assert payload["message"] == SUCCESS_MESSAGE
    assert payload["requires_relogin"] is True
    assert session_manager.terminated == ["u1"]
    assert repo.updated_hash is not None


def test_at_uc05_02_incorrect_current_password() -> None:
    user = build_user("OldPass!1")
    repo = StubUserAccountRepository(user)
    service = PasswordChangeService(repo)
    session_manager = StubSessionManager()

    status, payload = change_password(
        service,
        session_manager,
        user,
        {
            "current_password": "WrongPass!1",
            "new_password": "NewPass!1",
            "confirm_password": "NewPass!1",
        },
    )

    assert status == 401
    assert payload["message"] == INCORRECT_CURRENT_PASSWORD_MESSAGE
    assert session_manager.terminated == []


def test_at_uc05_03_password_policy_failure() -> None:
    user = build_user("OldPass!1")
    repo = StubUserAccountRepository(user)
    service = PasswordChangeService(repo)
    session_manager = StubSessionManager()

    status, payload = change_password(
        service,
        session_manager,
        user,
        {
            "current_password": "OldPass!1",
            "new_password": "short",
            "confirm_password": "short",
        },
    )

    assert status == 422
    assert payload["message"] == requirements_message()
    assert session_manager.terminated == []


def test_at_uc05_04_confirmation_mismatch() -> None:
    user = build_user("OldPass!1")
    repo = StubUserAccountRepository(user)
    service = PasswordChangeService(repo)
    session_manager = StubSessionManager()

    status, payload = change_password(
        service,
        session_manager,
        user,
        {
            "current_password": "OldPass!1",
            "new_password": "NewPass!1",
            "confirm_password": "NewPass!2",
        },
    )

    assert status == 422
    assert payload["message"] == MISMATCH_MESSAGE
    assert session_manager.terminated == []


def test_at_uc05_05_update_failure() -> None:
    user = build_user("OldPass!1")
    repo = StubUserAccountRepository(user, fail_on_update=True)
    service = PasswordChangeService(repo)
    session_manager = StubSessionManager()

    status, payload = change_password(
        service,
        session_manager,
        user,
        {
            "current_password": "OldPass!1",
            "new_password": "NewPass!1",
            "confirm_password": "NewPass!1",
        },
    )

    assert status == 500
    assert payload["message"] == UPDATE_FAILURE_MESSAGE
    assert session_manager.terminated == []
