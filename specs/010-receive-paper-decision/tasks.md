---

description: "Task list for UC-10 decision viewing"
---

# Tasks: UC-10 Receive Paper Acceptance or Rejection Decision

**Input**: Design documents from `/specs/010-receive-paper-decision/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/decision-api.yaml

**Tests**: Not requested by the spec; no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.
**Scope**: Tasks map only to UC-10 and AT-UC10-*.

## Format: `[ID] [P?] [Story] Description`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Minimal setup for UC-10 documentation and structure alignment

- [ ] T001 Confirm feature docs and paths under `specs/010-receive-paper-decision/`
- [ ] T002 [P] Align decision endpoint path naming with contract in `specs/010-receive-paper-decision/contracts/decision-api.yaml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared logic required before user story work

- [ ] T003 [P] Define decision status/value enums in `src/models/decision.py`
- [ ] T004 [P] Add submission decision fields mapping in `src/models/paper_submission.py`
- [ ] T005 Implement author-ownership check utility in `src/lib/authorization.py`
- [ ] T006 Implement decision retrieval error mapping in `src/lib/decision_errors.py`
- [ ] T007 Add structured logging with request/trace IDs for decision access failures in `src/lib/audit_log.py`

**Checkpoint**: Foundation ready

---

## Phase 3: User Story 1 - Author views decision (Priority: P1) 🎯 MVP

**Goal**: Logged-in authors can view decision status/value for their submission with correct access control and error states.

**Independent Test**: An author can view Accepted/Rejected, see “not yet available” when no decision exists, get redirected when unauthenticated, and receive explicit error messaging on retrieval failure.

### Implementation for User Story 1

- [ ] T008 [P] [US1] Implement decision service to fetch decision status/value in `src/services/decision_service.py`
- [ ] T009 [US1] Enforce author-only access using authorization utility in `src/services/decision_service.py`
- [ ] T010 [US1] Implement decision API handler in `src/lib/decision_controller.py`
- [ ] T011 [US1] Wire decision route to handler in `src/lib/routes.py`
- [ ] T012 [US1] Enforce unauthenticated redirect to login in `src/lib/routes.py`
- [ ] T013 [US1] Map "not recorded" to user-facing status in `src/lib/decision_presenter.py`
- [ ] T014 [US1] Map retrieval error to user-facing message in `src/lib/decision_presenter.py`
- [ ] T015 [US1] Map critical failure to "data unavailable" message in `src/lib/decision_presenter.py`
- [ ] T016 [US1] Add decision section to submissions page view in `src/lib/submissions_view.py`

**Checkpoint**: User Story 1 independently complete

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Cross-cutting concerns for UC-10

- [ ] T017 [P] Update quickstart validation notes in `specs/010-receive-paper-decision/quickstart.md`
- [ ] T018 [P] Update decision access documentation in `specs/010-receive-paper-decision/spec.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Story 1 (Phase 3)**: Depends on Foundational completion
- **Polish (Phase 4)**: Depends on User Story 1 completion

### User Story Dependencies

- **US1 (P1)**: Depends on Foundational tasks T003–T007

### Parallel Opportunities

- Phase 1: T002 can run in parallel with T001
- Phase 2: T003, T004 can run in parallel; T005, T006, T007 can run in parallel after model fields are defined
- Phase 3: T008 can run in parallel with T012 once foundational utilities exist

---

## Parallel Example: User Story 1

```text
Task: "Implement decision service to fetch decision status/value in src/services/decision_service.py"
Task: "Map \"not recorded\" to user-facing status in src/lib/decision_presenter.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1
2. Complete Phase 2
3. Complete Phase 3 (US1)
4. Validate against AT-UC10 scenarios

### Incremental Delivery

- Deliver US1 as the sole story; no further stories in this scope.
