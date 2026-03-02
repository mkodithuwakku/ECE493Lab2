---

description: "Task list for UC-11 schedule viewing"
---

# Tasks: UC-11 View Conference Schedule for Accepted Paper

**Input**: Design documents from `/specs/011-view-conference-schedule-for-accepted-paper/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/schedule-api.yaml

**Tests**: Not requested by the spec; no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.
**Scope**: Tasks map only to UC-11 and AT-UC11-*.

## Format: `[ID] [P?] [Story] Description`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Minimal setup for UC-11 documentation and structure alignment

- [ ] T001 Confirm feature docs and paths under `specs/011-view-conference-schedule-for-accepted-paper/`
- [ ] T002 [P] Align schedule endpoint naming with contract in `specs/011-view-conference-schedule-for-accepted-paper/contracts/schedule-api.yaml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared logic required before user story work

- [ ] T003 [P] Define schedule status enum in `src/models/schedule.py`
- [ ] T004 [P] Define schedule entry model in `src/models/schedule_entry.py`
- [ ] T005 [P] Add schedule linkage in `src/models/paper_submission.py`
- [ ] T006 Implement author-ownership check utility in `src/lib/authorization.py`
- [ ] T007 Implement schedule retrieval error mapping in `src/lib/schedule_errors.py`
- [ ] T008 [P] Add structured logging with request/trace IDs for schedule access and failures in `src/lib/audit_log.py`

**Checkpoint**: Foundation ready

---

## Phase 3: User Story 1 - View Published Schedule Entry (Priority: P1) 🎯 MVP

**Goal**: Logged-in authors can view the published schedule and their paper’s assigned time and room.

**Independent Test**: An author sees their paper’s schedule entry with time/room on the schedule view when the schedule is published.

### Implementation for User Story 1

- [ ] T009 [P] [US1] Implement schedule service to fetch published schedule in `src/services/schedule_service.py`
- [ ] T010 [US1] Enforce author-only access using authorization utility in `src/services/schedule_service.py`
- [ ] T011 [US1] Implement schedule API handler in `src/lib/schedule_controller.py`
- [ ] T012 [US1] Wire schedule route to handler in `src/lib/routes.py`
- [ ] T013 [US1] Map schedule entry time/room for display in `src/lib/schedule_presenter.py`
- [ ] T014 [US1] Add schedule section to submissions/schedule view in `src/lib/submissions_view.py`

**Checkpoint**: User Story 1 independently complete

---

## Phase 4: User Story 2 - Require Login to View Schedule (Priority: P1)

**Goal**: Unauthenticated users are redirected to login and can resume schedule viewing after login.

**Independent Test**: Accessing schedule view while logged out redirects to login and resumes the schedule view after login.

### Implementation for User Story 2

- [ ] T015 [US2] Enforce unauthenticated redirect to login for schedule route in `src/lib/routes.py`

**Checkpoint**: User Story 2 independently complete

---

## Phase 5: User Story 3 - Schedule Not Yet Published (Priority: P2)

**Goal**: Authors are informed when the schedule is not yet published.

**Independent Test**: When the schedule is unpublished, the system shows a “not yet published” message and no valid-looking schedule.

### Implementation for User Story 3

- [ ] T016 [US3] Map unpublished status to user-facing message in `src/lib/schedule_presenter.py`

**Checkpoint**: User Story 3 independently complete

---

## Phase 6: User Story 4 - Schedule Retrieval Error (Priority: P2)

**Goal**: Authors receive a clear temporary unavailability message when retrieval fails.

**Independent Test**: When retrieval fails, the system shows a temporary unavailability error and no partial schedule data.

### Implementation for User Story 4

- [ ] T017 [US4] Map retrieval error to user-facing message in `src/lib/schedule_presenter.py`

**Checkpoint**: User Story 4 independently complete

---

## Phase 7: User Story 5 - Paper Missing From Schedule (Priority: P2)

**Goal**: Authors are warned if their paper is missing from the schedule.

**Independent Test**: When schedule is published but missing the author’s paper entry, the system shows the schedule and a warning.

### Implementation for User Story 5

- [ ] T018 [US5] Map missing-entry condition to warning in `src/lib/schedule_presenter.py`

**Checkpoint**: User Story 5 independently complete

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Cross-cutting concerns for UC-11

- [ ] T019 [P] Update quickstart validation notes in `specs/011-view-conference-schedule-for-accepted-paper/quickstart.md`
- [ ] T020 [P] Update schedule access documentation in `specs/011-view-conference-schedule-for-accepted-paper/spec.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Stories (Phases 3-7)**: Depend on Foundational completion
- **Polish (Phase 8)**: Depends on all user stories completion

### User Story Dependencies

- **US1 (P1)**: Depends on Foundational tasks T003–T008
- **US2 (P1)**: Depends on Foundational tasks T003–T008
- **US3 (P2)**: Depends on Foundational tasks T003–T008
- **US4 (P2)**: Depends on Foundational tasks T003–T008
- **US5 (P2)**: Depends on Foundational tasks T003–T008

### Parallel Opportunities

- Phase 1: T002 can run in parallel with T001
- Phase 2: T003, T004, T005 can run in parallel; T006, T007, T008 can run in parallel after models are defined
- Phase 3: T009 can run in parallel with T013 once foundational utilities exist

---

## Parallel Example: User Story 1

```text
Task: "Implement schedule service to fetch published schedule in src/services/schedule_service.py"
Task: "Map schedule entry time/room for display in src/lib/schedule_presenter.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1
2. Complete Phase 2
3. Complete Phase 3 (US1)
4. Validate against AT-UC11 scenarios

### Incremental Delivery

- Deliver US1 first, then add US2–US5 in priority order.
