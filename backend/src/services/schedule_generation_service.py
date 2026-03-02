from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from models.accepted_paper import AcceptedPaper
from models.conference_schedule import ConferenceSchedule
from models.schedule_entry import ScheduleEntry
from models.scheduling_resources import SchedulingResources
from services.schedule_generation_logger import (
    ScheduleGenerationLogContext,
    log_schedule_generation_event,
)

GENERATE_UNAUTHENTICATED_MESSAGE = "Please log in to generate the conference schedule."
GENERATE_FORBIDDEN_MESSAGE = "You are not authorized to generate the conference schedule."
NO_ACCEPTED_PAPERS_MESSAGE = "Accepted papers are required to generate a schedule."
CONSTRAINT_VIOLATION_TEMPLATE = (
    "Schedule constraints cannot be satisfied: insufficient {constraint_type}."
)
GENERATION_FAILED_MESSAGE = "Schedule generation failed."
STORAGE_FAILED_MESSAGE = "Generated schedule could not be saved."
SCHEDULE_NOT_FOUND_MESSAGE = "No generated schedule is available."
SCHEDULE_RETRIEVAL_ERROR_MESSAGE = "Generated schedule is temporarily unavailable."
LOGIN_REDIRECT = "/login"


class AcceptedPapersRetrievalError(RuntimeError):
    pass


class SchedulingResourcesRetrievalError(RuntimeError):
    pass


class ScheduleGenerationError(RuntimeError):
    pass


class ScheduleStorageError(RuntimeError):
    pass


class ScheduleRetrievalError(RuntimeError):
    pass


class AcceptedPapersRepository(Protocol):
    def list_accepted_papers(self) -> list[AcceptedPaper]:
        ...


class SchedulingResourcesRepository(Protocol):
    def get_resources(self) -> SchedulingResources:
        ...


class ScheduleRepository(Protocol):
    def save_schedule(self, schedule: ConferenceSchedule) -> None:
        ...

    def get_schedule(self) -> ConferenceSchedule | None:
        ...


class ScheduleGenerator(Protocol):
    def generate(
        self,
        accepted_papers: list[AcceptedPaper],
        resources: SchedulingResources,
    ) -> ConferenceSchedule:
        ...


@dataclass(frozen=True)
class ScheduleGenerationResult:
    status: str
    schedule: ConferenceSchedule | None = None
    message: str | None = None
    constraint_type: str | None = None
    redirect_to: str | None = None

    @classmethod
    def generated(cls, schedule: ConferenceSchedule) -> "ScheduleGenerationResult":
        return cls(status="generated", schedule=schedule)

    @classmethod
    def unauthenticated(cls) -> "ScheduleGenerationResult":
        return cls(
            status="unauthenticated",
            message=GENERATE_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def forbidden(cls) -> "ScheduleGenerationResult":
        return cls(status="forbidden", message=GENERATE_FORBIDDEN_MESSAGE)

    @classmethod
    def no_accepted_papers(cls) -> "ScheduleGenerationResult":
        return cls(status="no_papers", message=NO_ACCEPTED_PAPERS_MESSAGE)

    @classmethod
    def constraint_violation(cls, constraint_type: str) -> "ScheduleGenerationResult":
        return cls(
            status="constraint",
            message=CONSTRAINT_VIOLATION_TEMPLATE.format(constraint_type=constraint_type),
            constraint_type=constraint_type,
        )

    @classmethod
    def generation_failed(cls) -> "ScheduleGenerationResult":
        return cls(status="generation_failed", message=GENERATION_FAILED_MESSAGE)

    @classmethod
    def storage_failed(cls) -> "ScheduleGenerationResult":
        return cls(status="storage_failed", message=STORAGE_FAILED_MESSAGE)


@dataclass(frozen=True)
class ScheduleDisplayResult:
    status: str
    schedule: ConferenceSchedule | None = None
    message: str | None = None
    redirect_to: str | None = None

    @classmethod
    def found(cls, schedule: ConferenceSchedule) -> "ScheduleDisplayResult":
        return cls(status="found", schedule=schedule)

    @classmethod
    def unauthenticated(cls) -> "ScheduleDisplayResult":
        return cls(
            status="unauthenticated",
            message=GENERATE_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def forbidden(cls) -> "ScheduleDisplayResult":
        return cls(status="forbidden", message=GENERATE_FORBIDDEN_MESSAGE)

    @classmethod
    def not_found(cls) -> "ScheduleDisplayResult":
        return cls(status="not_found", message=SCHEDULE_NOT_FOUND_MESSAGE)

    @classmethod
    def retrieval_error(cls) -> "ScheduleDisplayResult":
        return cls(status="error", message=SCHEDULE_RETRIEVAL_ERROR_MESSAGE)


class SimpleScheduleGenerator:
    def generate(
        self,
        accepted_papers: list[AcceptedPaper],
        resources: SchedulingResources,
    ) -> ConferenceSchedule:
        entries: list[ScheduleEntry] = []
        rooms = resources.rooms
        time_slots = resources.time_slots
        rooms_count = len(rooms)

        for index, paper in enumerate(accepted_papers):
            room_index = index % rooms_count
            slot_index = index // rooms_count
            entries.append(
                ScheduleEntry(
                    submission_id=paper.submission_id,
                    presentation_time=time_slots[slot_index],
                    room_or_location=rooms[room_index],
                )
            )

        return ConferenceSchedule(status="unpublished", entries=entries)


class ScheduleGenerationService:
    def __init__(
        self,
        accepted_papers_repository: AcceptedPapersRepository,
        resources_repository: SchedulingResourcesRepository,
        schedule_repository: ScheduleRepository,
        schedule_generator: ScheduleGenerator | None = None,
    ) -> None:
        self._accepted_papers_repository = accepted_papers_repository
        self._resources_repository = resources_repository
        self._schedule_repository = schedule_repository
        self._schedule_generator = schedule_generator or SimpleScheduleGenerator()

    def generate_schedule(
        self,
        admin_id: str | None,
        is_admin: bool,
        trace_id: Optional[str] = None,
    ) -> ScheduleGenerationResult:
        context = ScheduleGenerationLogContext(admin_id=admin_id, trace_id=trace_id)

        if not admin_id:
            log_schedule_generation_event("schedule_generation_unauthenticated", context)
            return ScheduleGenerationResult.unauthenticated()

        if not is_admin:
            log_schedule_generation_event(
                "schedule_generation_forbidden",
                context,
                GENERATE_FORBIDDEN_MESSAGE,
            )
            return ScheduleGenerationResult.forbidden()

        try:
            accepted_papers = self._accepted_papers_repository.list_accepted_papers()
        except AcceptedPapersRetrievalError:
            log_schedule_generation_event(
                "schedule_generation_failed",
                context,
                GENERATION_FAILED_MESSAGE,
            )
            return ScheduleGenerationResult.generation_failed()
        except Exception:
            log_schedule_generation_event(
                "schedule_generation_failed",
                context,
                GENERATION_FAILED_MESSAGE,
            )
            return ScheduleGenerationResult.generation_failed()

        if not accepted_papers:
            log_schedule_generation_event(
                "schedule_generation_no_papers",
                context,
                NO_ACCEPTED_PAPERS_MESSAGE,
            )
            return ScheduleGenerationResult.no_accepted_papers()

        try:
            resources = self._resources_repository.get_resources()
        except SchedulingResourcesRetrievalError:
            log_schedule_generation_event(
                "schedule_generation_failed",
                context,
                GENERATION_FAILED_MESSAGE,
            )
            return ScheduleGenerationResult.generation_failed()
        except Exception:
            log_schedule_generation_event(
                "schedule_generation_failed",
                context,
                GENERATION_FAILED_MESSAGE,
            )
            return ScheduleGenerationResult.generation_failed()

        constraint_type = self._constraint_violation(accepted_papers, resources)
        if constraint_type:
            message = CONSTRAINT_VIOLATION_TEMPLATE.format(constraint_type=constraint_type)
            log_schedule_generation_event(
                "schedule_generation_constraint_violation",
                context,
                message,
            )
            return ScheduleGenerationResult.constraint_violation(constraint_type)

        try:
            schedule = self._schedule_generator.generate(accepted_papers, resources)
        except ScheduleGenerationError:
            log_schedule_generation_event(
                "schedule_generation_failed",
                context,
                GENERATION_FAILED_MESSAGE,
            )
            return ScheduleGenerationResult.generation_failed()
        except Exception:
            log_schedule_generation_event(
                "schedule_generation_failed",
                context,
                GENERATION_FAILED_MESSAGE,
            )
            return ScheduleGenerationResult.generation_failed()

        try:
            self._schedule_repository.save_schedule(schedule)
        except ScheduleStorageError:
            log_schedule_generation_event(
                "schedule_generation_storage_failed",
                context,
                STORAGE_FAILED_MESSAGE,
            )
            return ScheduleGenerationResult.storage_failed()
        except Exception:
            log_schedule_generation_event(
                "schedule_generation_storage_failed",
                context,
                STORAGE_FAILED_MESSAGE,
            )
            return ScheduleGenerationResult.storage_failed()

        log_schedule_generation_event("schedule_generation_saved", context)
        return ScheduleGenerationResult.generated(schedule)

    def get_generated_schedule(
        self,
        admin_id: str | None,
        is_admin: bool,
        trace_id: Optional[str] = None,
    ) -> ScheduleDisplayResult:
        context = ScheduleGenerationLogContext(admin_id=admin_id, trace_id=trace_id)

        if not admin_id:
            log_schedule_generation_event("schedule_generation_unauthenticated", context)
            return ScheduleDisplayResult.unauthenticated()

        if not is_admin:
            log_schedule_generation_event(
                "schedule_generation_forbidden",
                context,
                GENERATE_FORBIDDEN_MESSAGE,
            )
            return ScheduleDisplayResult.forbidden()

        try:
            schedule = self._schedule_repository.get_schedule()
        except ScheduleRetrievalError:
            log_schedule_generation_event(
                "schedule_generation_retrieval_error",
                context,
                SCHEDULE_RETRIEVAL_ERROR_MESSAGE,
            )
            return ScheduleDisplayResult.retrieval_error()
        except Exception:
            log_schedule_generation_event(
                "schedule_generation_retrieval_error",
                context,
                SCHEDULE_RETRIEVAL_ERROR_MESSAGE,
            )
            return ScheduleDisplayResult.retrieval_error()

        if schedule is None:
            log_schedule_generation_event(
                "schedule_generation_missing",
                context,
                SCHEDULE_NOT_FOUND_MESSAGE,
            )
            return ScheduleDisplayResult.not_found()

        log_schedule_generation_event("schedule_generation_displayed", context)
        return ScheduleDisplayResult.found(schedule)

    @staticmethod
    def _constraint_violation(
        accepted_papers: list[AcceptedPaper],
        resources: SchedulingResources,
    ) -> str | None:
        if not resources.rooms:
            return "rooms"
        if not resources.time_slots:
            return "time slots"
        capacity = len(resources.rooms) * len(resources.time_slots)
        if capacity < len(accepted_papers):
            return "time slots"
        return None
