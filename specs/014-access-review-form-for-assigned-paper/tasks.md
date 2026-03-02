---

description: "Task list for UC-14 Access Review Form for Assigned Paper"
---

# Tasks: UC-14 Access Review Form for Assigned Paper

**Input**: Design documents from `/specs/014-access-review-form-for-assigned-paper/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Not requested in spec; no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.
**Scope**: Tasks map to UC-14 and AT-UC14-* only.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create/confirm base directories `src/models/`, `src/services/`, `src/lib/`, `tests/contract/`, `tests/integration/`, `tests/unit/`
- [ ] T002 [P] Create feature route module placeholder in `src/lib/review_form_routes.js` and register in app router

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [ ] T003 Implement/confirm authentication guard usable by review-form routes in `src/lib/auth_guard.js`
- [ ] T004 [P] Implement/confirm standardized error response helper for auth/availability/system errors in `src/lib/error_responses.js`
- [ ] T005 [P] Implement/confirm logging hook for access denials and retrieval failures in `src/lib/audit_log.js`
- [ ] T006 [P] Define data-access interfaces for assignments, review forms, and manuscripts in `src/services/review_access_repository.js`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Open Review Form for Assigned Paper (Priority: P1) 🎯 MVP

**Goal**: Logged-in reviewer can open review form for an assigned paper with paper details and manuscript access.

**Independent Test**: As a logged-in reviewer with an assigned paper and available manuscript, opening the review form shows paper details and manuscript access without auth errors.

### Implementation for User Story 1

- [ ] T007 [P] [US1] Implement review form retrieval service in `src/services/review_form_service.js.js` (paper details + form fields)
- [ ] T008 [P] [US1] Implement manuscript access service in `src/services/manuscript_service.js.js` (available manuscript path/link)
- [ ] T009 [US1] Implement controller/handler to assemble review form page data in `src/lib/review_form_controller.js`
- [ ] T010 [US1] Wire review form route to controller in `src/lib/review_form_routes.js`
- [ ] T011 [US1] Add view/response mapping for review form page in `src/lib/review_form_view.js`

**Checkpoint**: User Story 1 is functional and independently testable

---

## Phase 4: User Story 2 - Require Login Before Access (Priority: P2)

**Goal**: Unauthenticated users are redirected to login and cannot access review content.

**Independent Test**: Direct review-form access while logged out redirects to login with no review content shown; access works after login.

### Implementation for User Story 2

- [ ] T012 [US2] Apply authentication guard to review-form routes in `src/lib/review_form_routes.js`
- [ ] T013 [US2] Implement login redirect flow for unauthenticated access in `src/lib/auth_guard.js`

**Checkpoint**: User Story 2 is functional and independently testable

---

## Phase 5: User Story 3 - Block Access to Unassigned Papers (Priority: P3)

**Goal**: Reviewers cannot access review forms for papers not assigned to them; generic authorization error shown.

**Independent Test**: Logged-in reviewer attempting to access an unassigned paper gets a generic authorization error with no content shown.

### Implementation for User Story 3

- [ ] T014 [US3] Implement assignment authorization check in `src/services/review_access_service.js`
- [ ] T015 [US3] Return generic authorization error via `src/lib/error_responses.js` when access is denied
- [ ] T016 [US3] Log authorization denial in `src/lib/audit_log.js`

**Checkpoint**: User Story 3 is functional and independently testable

---

## Phase 6: User Story 4 - Handle Missing Manuscript (Priority: P4)

**Goal**: When manuscript is unavailable, review form access is blocked with a clear message.

**Independent Test**: Logged-in reviewer opening review form for assigned paper with missing manuscript sees a clear manuscript-unavailable message and no form content.

### Implementation for User Story 4

- [ ] T017 [US4] Detect manuscript unavailability in `src/services/manuscript_service.js.js`
- [ ] T018 [US4] Block review form access on manuscript-unavailable and return message via `src/lib/error_responses.js`
- [ ] T019 [US4] Log manuscript-unavailable event in `src/lib/audit_log.js`

**Checkpoint**: User Story 4 is functional and independently testable

---

## Phase 7: User Story 5 - Handle Review Form Retrieval Failure (Priority: P5)

**Goal**: If review form retrieval fails, show a generic user-safe error and no partial data.

**Independent Test**: Simulated retrieval failure shows generic error with no partial form data displayed.

### Implementation for User Story 5

- [ ] T020 [US5] Handle review-form retrieval failures in `src/services/review_form_service.js.js`
- [ ] T021 [US5] Return generic user-safe error via `src/lib/error_responses.js`
- [ ] T022 [US5] Log review-form retrieval failure in `src/lib/audit_log.js`

**Checkpoint**: User Story 5 is functional and independently testable

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T023 [P] Update `specs/014-access-review-form-for-assigned-paper/quickstart.md` if route names or messages differ from planned behavior
- [ ] T024 [P] Run quickstart validation steps and record results in `specs/014-access-review-form-for-assigned-paper/quickstart.md`
- [ ] T025 [P] Define success-criteria measurement notes in `specs/014-access-review-form-for-assigned-paper/quickstart.md` (SC-001–SC-004)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Foundational - no dependencies on other stories
- **User Story 2 (P2)**: Starts after Foundational - no dependencies on other stories
- **User Story 3 (P3)**: Starts after Foundational - no dependencies on other stories
- **User Story 4 (P4)**: Starts after Foundational - depends on US1 services
- **User Story 5 (P5)**: Starts after Foundational - depends on US1 services

### Parallel Opportunities

- T002, T004, T005, T006 can run in parallel
- Within US1: T007 and T008 can run in parallel
- Within US3/US4/US5: service updates and logging can run in parallel if touching different files

---

## Parallel Example: User Story 1

```bash
Task: "Implement review form retrieval service in src/services/review_form_service.js.js"
Task: "Implement manuscript access service in src/services/manuscript_service.js.js"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. STOP and validate User Story 1 independently

### Incremental Delivery

1. Setup + Foundational
2. User Story 1 → validate (MVP)
3. User Story 2 → validate
4. User Story 3 → validate
5. User Story 4 → validate
6. User Story 5 → validate

