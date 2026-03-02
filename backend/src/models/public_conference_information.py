from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PublicConferenceInformation:
    id: str
    content: str
    is_public: bool = True
