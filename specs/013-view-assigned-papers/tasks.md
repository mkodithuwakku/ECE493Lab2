---

description: "Task list for UC-13 assigned papers"
---

# Tasks: UC-13 View Assigned Papers

**Input**: Design documents from `/specs/013-view-assigned-papers/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/assigned-papers-api.yaml

**Tests**: Not requested by the spec; no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.
**Scope**: Tasks map only to UC-13 and AT-UC13-*.

## Format: `[ID] [P?] [Story] Description`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Minimal setup for UC-13 documentation and structure alignment

- [ ] T001 Confirm feature docs and paths under `specs/013-view-assigned-papers/`
- [ ] T002 [P] Align assigned-papers endpoint with contract in `specs/013-view-assigned-papers/contracts/assigned-papers-api.yaml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared logic required before user story work

- [ ] T003 [P] Define assigned paper model in `src/models/assigned_paper.py`
- [ ] T004 [P] Define reviewer model updates in `src/models/reviewer.py`
- [ ] T005 Implement assigned papers authorization utility in `src/lib/authorization.py`
- [ ] T006 Implement assigned papers retrieval error mapping in `src/lib/assigned_papers_errors.py`
- [ ] T007 [P] Add structured logging with request/trace IDs for assigned papers access and failures in `src/lib/audit_log.py`

**Checkpoint**: Foundation ready

---

## Phase 3: User Story 1 - View Assigned Papers List (Priority: P1) 🎯 MVP

**Goal**: Reviewer can view assigned papers list with identifying info and open paper detail if supported.

**Independent Test**: Assigned papers list is displayed with identifying info; selecting an entry opens the corresponding detail/review page if supported.

### Implementation for User Story 1

- [ ] T008 [P] [US1] Implement assigned papers service to list assignments in `src/services/assigned_papers_service.py`
- [ ] T009 [US1] Implement assigned papers handler in `src/lib/assigned_papers_controller.py`
- [ ] T010 [US1] Wire assigned papers route in `src/lib/routes.py`
- [ ] T011 [US1] Map identifying info for display in `src/lib/assigned_papers_presenter.py`
- [ ] T012 [US1] Add assigned papers section to reviewer view in `src/lib/reviewer_view.py`

**Checkpoint**: User Story 1 independently complete

---

## Phase 4: User Story 2 - Require Login to View Assigned Papers (Priority: P1)

**Goal**: Unauthenticated reviewers are redirected to login and can access assigned papers after login.

**Independent Test**: Accessing Assigned Papers while logged out redirects to login and resumes after login.

### Implementation for User Story 2

- [ ] T013 [US2] Enforce unauthenticated redirect to login for assigned papers in `src/lib/routes.py`

**Checkpoint**: User Story 2 independently complete

---

## Phase 5: User Story 3 - No Assigned Papers (Priority: P2)

**Goal**: Reviewer sees a clear zero-state message when no assigned papers exist.

**Independent Test**: Assigned Papers shows a clear "no assigned papers" message and no misleading placeholders.

### Implementation for User Story 3

- [ ] T014 [US3] Map zero-assignments state to user-facing message in `src/lib/assigned_papers_presenter.py`

**Checkpoint**: User Story 3 independently complete

---

## Phase 6: User Story 4 - Error Retrieving Assigned Papers (Priority: P2)

**Goal**: Retrieval errors show an error message and prevent partial/incorrect data display.

**Independent Test**: Error message is shown, no partial data displayed, and navigation remains safe.

### Implementation for User Story 4

- [ ] T015 [US4] Map retrieval error to user-facing message in `src/lib/assigned_papers_presenter.py`
- [ ] T016 [US4] Ensure safe navigation after retrieval error in `src/lib/reviewer_view.py`

**Checkpoint**: User Story 4 independently complete

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Cross-cutting concerns for UC-13

- [ ] T017 [P] Update quickstart validation notes in `specs/013-view-assigned-papers/quickstart.md`
- [ ] T018 [P] Update assigned papers access documentation in `specs/013-view-assigned-papers/spec.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Stories (Phases 3-6)**: Depend on Foundational completion
- **Polish (Phase 7)**: Depends on all user stories completion

### User Story Dependencies

- **US1 (P1)**: Depends on Foundational tasks T003–T007
- **US2 (P1)**: Depends on Foundational tasks T003–T007
- **US3 (P2)**: Depends on Foundational tasks T003–T007
- **US4 (P2)**: Depends on Foundational tasks T003–T007

### Parallel Opportunities

- Phase 1: T002 can run in parallel with T001
- Phase 2: T003, T004 can run in parallel; T005, T006, T007 can run in parallel after models are defined
- Phase 3: T008 can run in parallel with T011 once foundational utilities exist

---

## Parallel Example: User Story 1

```text
Task: "Implement assigned papers service to list assignments in src/services/assigned_papers_service.py"
Task: "Map identifying info for display in src/lib/assigned_papers_presenter.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1
2. Complete Phase 2
3. Complete Phase 3 (US1)
4. Validate against AT-UC13 scenarios

### Incremental Delivery

- Deliver US1 first, then add US2–US4 in priority order.
