from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from models.conference_configuration import ConferenceConfiguration
from services.conference_configuration_logger import (
    ConferenceConfigurationLogContext,
    log_conference_configuration_event,
)
from services.conference_configuration_validation import (
    ConferenceConfigurationValidator,
    ValidationResult,
)

CONFIG_UNAUTHENTICATED_MESSAGE = "Please log in to access conference configuration."
CONFIG_FORBIDDEN_MESSAGE = "You are not authorized to modify conference configuration."
CONFIG_RETRIEVAL_ERROR_MESSAGE = "Conference configuration cannot be loaded."
CONFIG_SAVE_ERROR_MESSAGE = "Conference configuration could not be saved."
CONFIG_SUCCESS_MESSAGE = "Conference configuration updated successfully."
LOGIN_REDIRECT = "/login"


class ConfigurationRetrievalError(RuntimeError):
    pass


class ConfigurationSaveError(RuntimeError):
    pass


class ConferenceConfigurationRepository(Protocol):
    def get_configuration(self) -> ConferenceConfiguration:
        ...

    def save_configuration(self, config: ConferenceConfiguration) -> None:
        ...


@dataclass(frozen=True)
class ConfigurationResult:
    status: str
    configuration: ConferenceConfiguration | None = None
    message: str | None = None
    errors: list[str] | None = None
    redirect_to: str | None = None

    @classmethod
    def ok(cls, config: ConferenceConfiguration) -> "ConfigurationResult":
        return cls(status="ok", configuration=config)

    @classmethod
    def unauthenticated(cls) -> "ConfigurationResult":
        return cls(
            status="unauthenticated",
            message=CONFIG_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def forbidden(cls) -> "ConfigurationResult":
        return cls(status="forbidden", message=CONFIG_FORBIDDEN_MESSAGE)

    @classmethod
    def retrieval_error(cls) -> "ConfigurationResult":
        return cls(status="error", message=CONFIG_RETRIEVAL_ERROR_MESSAGE)

    @classmethod
    def validation_error(cls, errors: list[str]) -> "ConfigurationResult":
        return cls(status="invalid", message="Validation failed.", errors=errors)

    @classmethod
    def save_error(cls) -> "ConfigurationResult":
        return cls(status="save_error", message=CONFIG_SAVE_ERROR_MESSAGE)

    @classmethod
    def saved(cls, config: ConferenceConfiguration) -> "ConfigurationResult":
        return cls(status="saved", configuration=config, message=CONFIG_SUCCESS_MESSAGE)


class ConferenceConfigurationService:
    def __init__(
        self,
        repository: ConferenceConfigurationRepository,
        validator: ConferenceConfigurationValidator | None = None,
    ) -> None:
        self._repository = repository
        self._validator = validator or ConferenceConfigurationValidator()

    def get_configuration(
        self,
        admin_id: str | None,
        is_admin: bool,
        trace_id: Optional[str] = None,
    ) -> ConfigurationResult:
        context = ConferenceConfigurationLogContext(admin_id=admin_id, trace_id=trace_id)

        if not admin_id:
            log_conference_configuration_event("conference_config_unauthenticated", context)
            return ConfigurationResult.unauthenticated()

        if not is_admin:
            log_conference_configuration_event(
                "conference_config_forbidden", context, CONFIG_FORBIDDEN_MESSAGE
            )
            return ConfigurationResult.forbidden()

        try:
            config = self._repository.get_configuration()
        except ConfigurationRetrievalError:
            log_conference_configuration_event(
                "conference_config_retrieval_error",
                context,
                CONFIG_RETRIEVAL_ERROR_MESSAGE,
            )
            return ConfigurationResult.retrieval_error()
        except Exception:
            log_conference_configuration_event(
                "conference_config_retrieval_error",
                context,
                CONFIG_RETRIEVAL_ERROR_MESSAGE,
            )
            return ConfigurationResult.retrieval_error()

        log_conference_configuration_event("conference_config_loaded", context)
        return ConfigurationResult.ok(config)

    def update_configuration(
        self,
        payload: dict | None,
        admin_id: str | None,
        is_admin: bool,
        trace_id: Optional[str] = None,
    ) -> ConfigurationResult:
        context = ConferenceConfigurationLogContext(admin_id=admin_id, trace_id=trace_id)

        if not admin_id:
            log_conference_configuration_event("conference_config_unauthenticated", context)
            return ConfigurationResult.unauthenticated()

        if not is_admin:
            log_conference_configuration_event(
                "conference_config_forbidden", context, CONFIG_FORBIDDEN_MESSAGE
            )
            return ConfigurationResult.forbidden()

        payload = payload or {}
        validation = self._validator.validate(payload)
        if validation.status != "ok":
            log_conference_configuration_event(
                "conference_config_validation_error", context, "; ".join(validation.errors)
            )
            return ConfigurationResult.validation_error(validation.errors)

        config = ConferenceConfiguration(
            submission_deadline=payload["submissionDeadline"],
            review_deadline=payload["reviewDeadline"],
            conference_start_date=payload["conferenceStartDate"],
            conference_end_date=payload["conferenceEndDate"],
        )

        try:
            self._repository.save_configuration(config)
        except ConfigurationSaveError:
            log_conference_configuration_event(
                "conference_config_save_error", context, CONFIG_SAVE_ERROR_MESSAGE
            )
            return ConfigurationResult.save_error()
        except Exception:
            log_conference_configuration_event(
                "conference_config_save_error", context, CONFIG_SAVE_ERROR_MESSAGE
            )
            return ConfigurationResult.save_error()

        log_conference_configuration_event("conference_config_saved", context)
        return ConfigurationResult.saved(config)
