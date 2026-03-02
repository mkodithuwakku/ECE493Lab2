from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class PublicItem:
    content: str


@dataclass(frozen=True)
class PublicInfoResponse:
    status: str
    announcements: List[PublicItem]
    information: List[PublicItem]
    message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "status": self.status,
            "announcements": [asdict(item) for item in self.announcements],
            "information": [asdict(item) for item in self.information],
        }
        if self.message:
            payload["message"] = self.message
        return payload


@dataclass(frozen=True)
class PartialPublicInfoResponse:
    status: str
    announcements: List[PublicItem]
    information: List[PublicItem]
    warning: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "announcements": [asdict(item) for item in self.announcements],
            "information": [asdict(item) for item in self.information],
            "warning": self.warning,
        }


@dataclass(frozen=True)
class ErrorResponse:
    message: str

    def to_dict(self) -> Dict[str, Any]:
        return {"message": self.message}
