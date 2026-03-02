from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from models.user_account import UserAccount
from services.registration_validation import validate_registration

DUPLICATE_EMAIL_MESSAGE = "Email is already registered."
PASSWORD_REQUIREMENTS_MESSAGE = (
    "Password must be at least 8 characters and include a non-letter character."
)
STORAGE_FAILURE_MESSAGE = "Registration failed. Please try again."
SUCCESS_MESSAGE = "Registration successful."
LOGIN_REDIRECT = "/login"


class RegistrationStorageError(RuntimeError):
    pass


class RegistrationRepository(Protocol):
    def is_email_registered(self, email: str) -> bool:
        ...

    def create_user(self, email: str, password_hash: str) -> UserAccount:
        ...


@dataclass(frozen=True)
class RegistrationResult:
    status: str
    message: str | None = None
    errors: list[str] | None = None
    redirect_to: str | None = None

    @classmethod
    def success(cls) -> "RegistrationResult":
        return cls(status="success", message=SUCCESS_MESSAGE, redirect_to=LOGIN_REDIRECT)

    @classmethod
    def validation_error(cls, errors: list[str]) -> "RegistrationResult":
        return cls(status="validation_error", errors=errors)

    @classmethod
    def duplicate_email(cls) -> "RegistrationResult":
        return cls(status="duplicate_email", message=DUPLICATE_EMAIL_MESSAGE)

    @classmethod
    def password_invalid(cls) -> "RegistrationResult":
        return cls(status="password_invalid", message=PASSWORD_REQUIREMENTS_MESSAGE)

    @classmethod
    def storage_error(cls) -> "RegistrationResult":
        return cls(status="storage_error", message=STORAGE_FAILURE_MESSAGE)


class RegistrationService:
    def __init__(self, repository: RegistrationRepository) -> None:
        self._repository = repository

    def register(self, email: str | None, password: str | None) -> RegistrationResult:
        validation = validate_registration(email, password)
        if validation.errors:
            return RegistrationResult.validation_error(validation.errors)
        if validation.password_invalid:
            return RegistrationResult.password_invalid()

        assert email is not None
        assert password is not None

        if self._repository.is_email_registered(email):
            return RegistrationResult.duplicate_email()

        try:
            password_hash = hash_password(password)
            self._repository.create_user(email=email, password_hash=password_hash)
        except RegistrationStorageError:
            return RegistrationResult.storage_error()

        return RegistrationResult.success()


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120_000)
    return f"pbkdf2_sha256$120000${salt.hex()}${digest.hex()}"
