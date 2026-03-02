from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.conference_configuration import (
    get_conference_configuration,
    update_conference_configuration,
)
from models.conference_configuration import ConferenceConfiguration
from services.conference_configuration_service import (
    CONFIG_RETRIEVAL_ERROR_MESSAGE,
    CONFIG_SAVE_ERROR_MESSAGE,
    CONFIG_UNAUTHENTICATED_MESSAGE,
    CONFIG_FORBIDDEN_MESSAGE,
    ConferenceConfigurationService,
    ConfigurationRetrievalError,
    ConfigurationSaveError,
)


def test_at_uc20_01_update_parameters_successfully() -> None:
    repository = StubConfigurationRepository(
        ConferenceConfiguration(
            submission_deadline="2026-01-01T00:00:00",
            review_deadline="2026-01-15T00:00:00",
            conference_start_date="2026-02-01T00:00:00",
            conference_end_date="2026-02-03T00:00:00",
        )
    )
    service = ConferenceConfigurationService(repository)

    status, response = update_conference_configuration(
        service,
        admin_id="admin-1",
        is_admin=True,
        payload={
            "submissionDeadline": "2026-01-05T00:00:00",
            "reviewDeadline": "2026-01-20T00:00:00",
            "conferenceStartDate": "2026-02-05T00:00:00",
            "conferenceEndDate": "2026-02-07T00:00:00",
        },
    )

    assert status == 200

    status, config = get_conference_configuration(service, "admin-1", True)
    assert status == 200
    assert config["submissionDeadline"] == "2026-01-05T00:00:00"
    assert config["reviewDeadline"] == "2026-01-20T00:00:00"


def test_at_uc20_02_admin_not_logged_in_or_not_authorized() -> None:
    repository = StubConfigurationRepository(default_config())
    service = ConferenceConfigurationService(repository)

    status, response = get_conference_configuration(service, None, True)
    assert status == 401
    assert response["message"] == CONFIG_UNAUTHENTICATED_MESSAGE

    status, response = update_conference_configuration(
        service,
        admin_id="user-1",
        is_admin=False,
        payload=valid_payload(),
    )
    assert status == 403
    assert response["message"] == CONFIG_FORBIDDEN_MESSAGE


def test_at_uc20_03_invalid_parameter_values() -> None:
    repository = StubConfigurationRepository(default_config())
    service = ConferenceConfigurationService(repository)

    status, response = update_conference_configuration(
        service,
        admin_id="admin-1",
        is_admin=True,
        payload={
            "submissionDeadline": "",
            "reviewDeadline": "invalid-date",
            "conferenceStartDate": "2026-02-01T00:00:00",
            "conferenceEndDate": "2026-02-02T00:00:00",
        },
    )

    assert status == 400
    assert response["errors"]
    assert repository.saved is None


def test_at_uc20_04_invalid_date_relationships() -> None:
    repository = StubConfigurationRepository(default_config())
    service = ConferenceConfigurationService(repository)

    status, response = update_conference_configuration(
        service,
        admin_id="admin-1",
        is_admin=True,
        payload={
            "submissionDeadline": "2026-02-10T00:00:00",
            "reviewDeadline": "2026-02-05T00:00:00",
            "conferenceStartDate": "2026-02-03T00:00:00",
            "conferenceEndDate": "2026-02-04T00:00:00",
        },
    )

    assert status == 400
    assert any("dateRelationship" in error for error in response["errors"])
    assert repository.saved is None


def test_at_uc20_05_configuration_retrieval_fails() -> None:
    repository = StubConfigurationRepository(default_config(), fail_retrieval=True)
    service = ConferenceConfigurationService(repository)

    status, response = get_conference_configuration(service, "admin-1", True)

    assert status == 503
    assert response["message"] == CONFIG_RETRIEVAL_ERROR_MESSAGE


def test_at_uc20_06_fail_to_store_updated_parameters() -> None:
    repository = StubConfigurationRepository(default_config(), fail_save=True)
    service = ConferenceConfigurationService(repository)

    status, response = update_conference_configuration(
        service,
        admin_id="admin-1",
        is_admin=True,
        payload=valid_payload(),
    )

    assert status == 500
    assert response["message"] == CONFIG_SAVE_ERROR_MESSAGE
    assert repository.saved is None


def default_config() -> ConferenceConfiguration:
    return ConferenceConfiguration(
        submission_deadline="2026-01-01T00:00:00",
        review_deadline="2026-01-10T00:00:00",
        conference_start_date="2026-02-01T00:00:00",
        conference_end_date="2026-02-02T00:00:00",
    )


def valid_payload() -> dict:
    return {
        "submissionDeadline": "2026-01-05T00:00:00",
        "reviewDeadline": "2026-01-15T00:00:00",
        "conferenceStartDate": "2026-02-05T00:00:00",
        "conferenceEndDate": "2026-02-07T00:00:00",
    }


class StubConfigurationRepository:
    def __init__(
        self,
        config: ConferenceConfiguration,
        *,
        fail_retrieval: bool = False,
        fail_save: bool = False,
    ) -> None:
        self._config = config
        self._fail_retrieval = fail_retrieval
        self._fail_save = fail_save
        self.saved: ConferenceConfiguration | None = None

    def get_configuration(self) -> ConferenceConfiguration:
        if self._fail_retrieval:
            raise ConfigurationRetrievalError("retrieval failure")
        return self._config

    def save_configuration(self, config: ConferenceConfiguration) -> None:
        if self._fail_save:
            raise ConfigurationSaveError("save failure")
        self.saved = config
        self._config = config
