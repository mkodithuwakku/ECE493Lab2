from __future__ import annotations

from api.schemas.registration import (
    MessageResponse,
    RegistrationSuccess,
    ValidationErrorResponse,
)
from services.registration_service import RegistrationResult, RegistrationService


def register_user(service: RegistrationService, payload: dict | None) -> tuple[int, dict]:
    payload = payload or {}
    email = payload.get("email")
    password = payload.get("password")

    result = service.register(email=email, password=password)

    if result.status == "success":
        response = RegistrationSuccess(
            message=result.message or "", redirect_to=result.redirect_to or "/login"
        )
        return 201, response.to_dict()

    if result.status == "validation_error":
        response = ValidationErrorResponse(errors=result.errors or [])
        return 400, response.to_dict()

    if result.status == "duplicate_email":
        response = MessageResponse(message=result.message or "")
        return 409, response.to_dict()

    if result.status == "password_invalid":
        response = MessageResponse(message=result.message or "")
        return 422, response.to_dict()

    response = MessageResponse(message=result.message or "")
    return 500, response.to_dict()
