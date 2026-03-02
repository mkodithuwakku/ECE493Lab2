from __future__ import annotations

from services.auth_service import AuthService
from api.login.login_error_mapper import map_auth_result


class LoginRequest:
    def __init__(self, identifier: str | None, password: str | None) -> None:
        self.identifier = identifier
        self.password = password


LOGIN_REDIRECT = "/home"


def handle_login(service: AuthService, payload: dict | None) -> tuple[int, dict]:
    payload = payload or {}
    identifier = payload.get("identifier")
    password = payload.get("password")

    result = service.authenticate(identifier, password)
    if result.status == "success":
        return 200, {"message": result.message, "redirect_to": LOGIN_REDIRECT}

    return map_auth_result(result)
