from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class RegistrationRequest:
    email: str
    password: str


@dataclass(frozen=True)
class RegistrationSuccess:
    message: str
    redirect_to: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ValidationErrorResponse:
    errors: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {"errors": self.errors}


@dataclass(frozen=True)
class MessageResponse:
    message: str

    def to_dict(self) -> Dict[str, Any]:
        return {"message": self.message}
