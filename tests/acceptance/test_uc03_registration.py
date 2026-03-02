from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.registration import register_user
from models.user_account import UserAccount
from services.registration_service import (
    DUPLICATE_EMAIL_MESSAGE,
    PASSWORD_REQUIREMENTS_MESSAGE,
    STORAGE_FAILURE_MESSAGE,
    SUCCESS_MESSAGE,
    LOGIN_REDIRECT,
    RegistrationRepository,
    RegistrationStorageError,
    RegistrationService,
)


class StubRegistrationRepository(RegistrationRepository):
    def __init__(self, *, existing_emails=None, fail_on_create: bool = False) -> None:
        self.existing_emails = set(existing_emails or [])
        self.fail_on_create = fail_on_create
        self.created_users: list[UserAccount] = []

    def is_email_registered(self, email: str) -> bool:
        return email in self.existing_emails

    def create_user(self, email: str, password_hash: str) -> UserAccount:
        if self.fail_on_create:
            raise RegistrationStorageError("storage failure")
        user = UserAccount(
            id="user-1",
            email=email,
            password_hash=password_hash,
            created_at=datetime.now(timezone.utc),
        )
        self.created_users.append(user)
        self.existing_emails.add(email)
        return user


def test_at_uc03_01_main_success() -> None:
    repository = StubRegistrationRepository()
    service = RegistrationService(repository)

    status_code, payload = register_user(
        service, {"email": "user@example.com", "password": "Secure!1"}
    )

    assert status_code == 201
    assert payload["message"] == SUCCESS_MESSAGE
    assert payload["redirect_to"] == LOGIN_REDIRECT
    assert len(repository.created_users) == 1
    assert repository.created_users[0].password_hash != "Secure!1"


def test_at_uc03_02_invalid_or_incomplete_registration() -> None:
    repository = StubRegistrationRepository()
    service = RegistrationService(repository)

    status_code, payload = register_user(service, {"email": "", "password": ""})

    assert status_code == 400
    assert payload["errors"]
    assert len(repository.created_users) == 0


def test_at_uc03_03_duplicate_email() -> None:
    repository = StubRegistrationRepository(existing_emails={"user@example.com"})
    service = RegistrationService(repository)

    status_code, payload = register_user(
        service, {"email": "user@example.com", "password": "Secure!1"}
    )

    assert status_code == 409
    assert payload["message"] == DUPLICATE_EMAIL_MESSAGE
    assert len(repository.created_users) == 0


def test_at_uc03_04_password_does_not_meet_requirements() -> None:
    repository = StubRegistrationRepository()
    service = RegistrationService(repository)

    status_code, payload = register_user(
        service, {"email": "user@example.com", "password": "password"}
    )

    assert status_code == 422
    assert payload["message"] == PASSWORD_REQUIREMENTS_MESSAGE
    assert len(repository.created_users) == 0


def test_at_uc03_05_storage_failure() -> None:
    repository = StubRegistrationRepository(fail_on_create=True)
    service = RegistrationService(repository)

    status_code, payload = register_user(
        service, {"email": "user@example.com", "password": "Secure!1"}
    )

    assert status_code == 500
    assert payload["message"] == STORAGE_FAILURE_MESSAGE
    assert len(repository.created_users) == 0
