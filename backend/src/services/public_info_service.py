from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Protocol

from api.schemas.public_info import PublicItem
from models.public_announcement import PublicAnnouncement
from models.public_conference_information import PublicConferenceInformation

WEBSITE_UNAVAILABLE_MESSAGE = "The website is temporarily unavailable."
NO_PUBLIC_INFO_MESSAGE = "No public conference information is currently available."
PARTIAL_CONTENT_MESSAGE = "Some information could not be loaded."
RETRIEVAL_ERROR_MESSAGE = "Public conference information cannot be retrieved at this time."


class WebsiteUnavailableError(RuntimeError):
    pass


class ContentRetrievalError(RuntimeError):
    pass


@dataclass(frozen=True)
class PublicFetchResult:
    items: List[PublicAnnouncement] | List[PublicConferenceInformation]
    partial: bool = False


class PublicInfoRepository(Protocol):
    def is_site_available(self) -> bool:
        ...

    def fetch_announcements(self) -> PublicFetchResult:
        ...

    def fetch_information(self) -> PublicFetchResult:
        ...


@dataclass(frozen=True)
class PublicInfoResult:
    status: str
    announcements: List[PublicItem]
    information: List[PublicItem]
    message: str | None = None
    warning: str | None = None

    @classmethod
    def ok(cls, announcements: List[PublicItem], information: List[PublicItem]) -> "PublicInfoResult":
        return cls(status="ok", announcements=announcements, information=information)

    @classmethod
    def empty(cls) -> "PublicInfoResult":
        return cls(
            status="ok",
            announcements=[],
            information=[],
            message=NO_PUBLIC_INFO_MESSAGE,
        )

    @classmethod
    def partial(
        cls, announcements: List[PublicItem], information: List[PublicItem]
    ) -> "PublicInfoResult":
        return cls(
            status="partial",
            announcements=announcements,
            information=information,
            warning=PARTIAL_CONTENT_MESSAGE,
        )

    @classmethod
    def unavailable(cls) -> "PublicInfoResult":
        return cls(
            status="unavailable",
            announcements=[],
            information=[],
            message=WEBSITE_UNAVAILABLE_MESSAGE,
        )

    @classmethod
    def error(cls) -> "PublicInfoResult":
        return cls(
            status="error",
            announcements=[],
            information=[],
            message=RETRIEVAL_ERROR_MESSAGE,
        )


class PublicInfoService:
    def __init__(self, repository: PublicInfoRepository) -> None:
        self._repository = repository

    def get_public_info(self) -> PublicInfoResult:
        if not self._repository.is_site_available():
            return PublicInfoResult.unavailable()

        try:
            announcements_result = self._repository.fetch_announcements()
            info_result = self._repository.fetch_information()
        except ContentRetrievalError:
            return PublicInfoResult.error()

        announcements = self._filter_public_announcements(announcements_result.items)
        information = self._filter_public_information(info_result.items)

        if not announcements and not information:
            return PublicInfoResult.empty()

        if announcements_result.partial or info_result.partial:
            return PublicInfoResult.partial(announcements, information)

        return PublicInfoResult.ok(announcements, information)

    @staticmethod
    def _filter_public_announcements(
        items: Iterable[PublicAnnouncement],
    ) -> List[PublicItem]:
        return [PublicItem(content=item.content) for item in items if item.is_public]

    @staticmethod
    def _filter_public_information(
        items: Iterable[PublicConferenceInformation],
    ) -> List[PublicItem]:
        return [PublicItem(content=item.content) for item in items if item.is_public]
