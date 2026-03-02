from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.conference_schedule_generation import (
    generate_conference_schedule,
    get_generated_conference_schedule,
)
from models.accepted_paper import AcceptedPaper
from models.conference_schedule import ConferenceSchedule
from models.scheduling_resources import SchedulingResources
from services.schedule_generation_service import (
    CONSTRAINT_VIOLATION_TEMPLATE,
    GENERATION_FAILED_MESSAGE,
    NO_ACCEPTED_PAPERS_MESSAGE,
    STORAGE_FAILED_MESSAGE,
    ScheduleGenerationError,
    ScheduleGenerationService,
    ScheduleStorageError,
)


def test_at_uc21_01_generate_conference_schedule_successfully() -> None:
    papers = [
        AcceptedPaper(submission_id="paper-1", title="Paper One"),
        AcceptedPaper(submission_id="paper-2", title="Paper Two"),
    ]
    resources = SchedulingResources(
        rooms=["Room A", "Room B"],
        time_slots=["2026-03-10T09:00", "2026-03-10T10:00"],
    )
    accepted_repo = StubAcceptedPapersRepository(papers)
    resources_repo = StubResourcesRepository(resources)
    schedule_repo = StubScheduleRepository()

    service = ScheduleGenerationService(accepted_repo, resources_repo, schedule_repo)

    status, response = generate_conference_schedule(service, "admin-1", True)

    assert status == 200
    assert response["entries"]
    assert schedule_repo.saved is not None

    status, response = get_generated_conference_schedule(service, "admin-1", True)

    assert status == 200
    assert response["entries"] == [
        {
            "submission_id": "paper-1",
            "presentation_time": "2026-03-10T09:00",
            "room_or_location": "Room A",
        },
        {
            "submission_id": "paper-2",
            "presentation_time": "2026-03-10T09:00",
            "room_or_location": "Room B",
        },
    ]


def test_at_uc21_02_no_accepted_papers_available() -> None:
    accepted_repo = StubAcceptedPapersRepository([])
    resources_repo = StubResourcesRepository(
        SchedulingResources(rooms=["Room A"], time_slots=["2026-03-10T09:00"])
    )
    schedule_repo = StubScheduleRepository()
    service = ScheduleGenerationService(accepted_repo, resources_repo, schedule_repo)

    status, response = generate_conference_schedule(service, "admin-1", True)

    assert status == 400
    assert response["message"] == NO_ACCEPTED_PAPERS_MESSAGE
    assert schedule_repo.saved is None


def test_at_uc21_03_constraints_block_generation_then_retry() -> None:
    papers = [
        AcceptedPaper(submission_id="paper-1", title="Paper One"),
        AcceptedPaper(submission_id="paper-2", title="Paper Two"),
    ]
    resources = SchedulingResources(rooms=["Room A"], time_slots=[])
    accepted_repo = StubAcceptedPapersRepository(papers)
    resources_repo = StubResourcesRepository(resources)
    schedule_repo = StubScheduleRepository()
    service = ScheduleGenerationService(accepted_repo, resources_repo, schedule_repo)

    status, response = generate_conference_schedule(service, "admin-1", True)

    assert status == 400
    assert response["message"] == CONSTRAINT_VIOLATION_TEMPLATE.format(
        constraint_type="time slots"
    )
    assert schedule_repo.saved is None

    resources_repo.resources = SchedulingResources(
        rooms=["Room A"],
        time_slots=["2026-03-10T09:00", "2026-03-10T10:00"],
    )

    status, response = generate_conference_schedule(service, "admin-1", True)

    assert status == 200
    assert response["entries"]
    assert schedule_repo.saved is not None


def test_at_uc21_04_generation_failure() -> None:
    papers = [AcceptedPaper(submission_id="paper-1", title="Paper One")]
    resources = SchedulingResources(rooms=["Room A"], time_slots=["2026-03-10T09:00"])
    accepted_repo = StubAcceptedPapersRepository(papers)
    resources_repo = StubResourcesRepository(resources)
    schedule_repo = StubScheduleRepository()
    generator = FailingGenerator()

    service = ScheduleGenerationService(
        accepted_repo,
        resources_repo,
        schedule_repo,
        schedule_generator=generator,
    )

    status, response = generate_conference_schedule(service, "admin-1", True)

    assert status == 500
    assert response["message"] == GENERATION_FAILED_MESSAGE
    assert schedule_repo.saved is None


def test_at_uc21_05_fail_to_store_generated_schedule() -> None:
    papers = [AcceptedPaper(submission_id="paper-1", title="Paper One")]
    resources = SchedulingResources(rooms=["Room A"], time_slots=["2026-03-10T09:00"])
    accepted_repo = StubAcceptedPapersRepository(papers)
    resources_repo = StubResourcesRepository(resources)
    schedule_repo = StubScheduleRepository(fail_save=True)
    service = ScheduleGenerationService(accepted_repo, resources_repo, schedule_repo)

    status, response = generate_conference_schedule(service, "admin-1", True)

    assert status == 503
    assert response["message"] == STORAGE_FAILED_MESSAGE
    assert schedule_repo.saved is None


class StubAcceptedPapersRepository:
    def __init__(self, papers: list[AcceptedPaper]) -> None:
        self._papers = papers

    def list_accepted_papers(self) -> list[AcceptedPaper]:
        return list(self._papers)


class StubResourcesRepository:
    def __init__(self, resources: SchedulingResources) -> None:
        self.resources = resources

    def get_resources(self) -> SchedulingResources:
        return self.resources


class StubScheduleRepository:
    def __init__(self, *, fail_save: bool = False) -> None:
        self._fail_save = fail_save
        self.saved: ConferenceSchedule | None = None

    def save_schedule(self, schedule: ConferenceSchedule) -> None:
        if self._fail_save:
            raise ScheduleStorageError("save failed")
        self.saved = schedule

    def get_schedule(self) -> ConferenceSchedule | None:
        return self.saved


class FailingGenerator:
    def generate(
        self,
        accepted_papers: list[AcceptedPaper],
        resources: SchedulingResources,
    ) -> ConferenceSchedule:
        raise ScheduleGenerationError("generation failed")
