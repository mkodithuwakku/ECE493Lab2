from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.public_info import get_public_info_response
from models.public_announcement import PublicAnnouncement
from models.public_conference_information import PublicConferenceInformation
from services.public_info_service import (
    ContentRetrievalError,
    NO_PUBLIC_INFO_MESSAGE,
    PARTIAL_CONTENT_MESSAGE,
    RETRIEVAL_ERROR_MESSAGE,
    WEBSITE_UNAVAILABLE_MESSAGE,
    PublicFetchResult,
    PublicInfoService,
)


class StubPublicInfoRepository:
    def __init__(
        self,
        *,
        site_available: bool = True,
        announcements=None,
        information=None,
        partial_announcements: bool = False,
        partial_information: bool = False,
        fail_on_fetch: bool = False,
    ) -> None:
        self._site_available = site_available
        self._announcements = announcements or []
        self._information = information or []
        self._partial_announcements = partial_announcements
        self._partial_information = partial_information
        self._fail_on_fetch = fail_on_fetch

    def is_site_available(self) -> bool:
        return self._site_available

    def fetch_announcements(self) -> PublicFetchResult:
        if self._fail_on_fetch:
            raise ContentRetrievalError("announcement fetch failed")
        return PublicFetchResult(
            items=self._announcements, partial=self._partial_announcements
        )

    def fetch_information(self) -> PublicFetchResult:
        if self._fail_on_fetch:
            raise ContentRetrievalError("information fetch failed")
        return PublicFetchResult(items=self._information, partial=self._partial_information)


def test_at_uc01_01_main_success() -> None:
    repository = StubPublicInfoRepository(
        announcements=[
            PublicAnnouncement(id="a1", content="Keynote announced"),
        ],
        information=[
            PublicConferenceInformation(id="i1", content="Conference overview"),
        ],
    )
    service = PublicInfoService(repository)
    status_code, payload = get_public_info_response(service)

    assert status_code == 200
    assert payload["status"] == "ok"
    assert payload["announcements"]
    assert payload["information"]


def test_at_uc01_02_website_unavailable() -> None:
    repository = StubPublicInfoRepository(site_available=False)
    service = PublicInfoService(repository)
    status_code, payload = get_public_info_response(service)

    assert status_code == 503
    assert payload["message"] == WEBSITE_UNAVAILABLE_MESSAGE


def test_at_uc01_03_no_public_information() -> None:
    repository = StubPublicInfoRepository(
        announcements=[PublicAnnouncement(id="a1", content="Hidden", is_public=False)],
        information=[],
    )
    service = PublicInfoService(repository)
    status_code, payload = get_public_info_response(service)

    assert status_code == 200
    assert payload["status"] == "ok"
    assert payload["announcements"] == []
    assert payload["information"] == []
    assert payload["message"] == NO_PUBLIC_INFO_MESSAGE


def test_at_uc01_04_partial_content_load_failure() -> None:
    repository = StubPublicInfoRepository(
        announcements=[PublicAnnouncement(id="a1", content="Keynote announced")],
        information=[PublicConferenceInformation(id="i1", content="Overview")],
        partial_information=True,
    )
    service = PublicInfoService(repository)
    status_code, payload = get_public_info_response(service)

    assert status_code == 206
    assert payload["status"] == "partial"
    assert payload["warning"] == PARTIAL_CONTENT_MESSAGE
    assert payload["announcements"]


def test_at_uc01_05_content_retrieval_error() -> None:
    repository = StubPublicInfoRepository(fail_on_fetch=True)
    service = PublicInfoService(repository)
    status_code, payload = get_public_info_response(service)

    assert status_code == 500
    assert payload["message"] == RETRIEVAL_ERROR_MESSAGE
