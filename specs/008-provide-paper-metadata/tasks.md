---

description: "Task list for UC-08 paper metadata implementation"
---

# Tasks: Provide Paper Metadata (UC-08)

**Input**: Design documents from `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/008-provide-paper-metadata/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Not requested in the feature specification; no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.
**Scope**: Tasks map to UC-08 and acceptance tests AT-UC08-* only.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize shared modules used across metadata stories

- [ ] T001 Create metadata validation helper in backend/src/services/metadata_validation.ts
- [ ] T002 [P] Create metadata API client wrapper in frontend/src/services/metadata_client.ts
- [ ] T003 [P] Create metadata logging utility in backend/src/services/metadata_logger.ts
- [ ] T004 [P] Create log redaction helper in backend/src/services/log_redactor.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core building blocks needed by all user stories

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Create submission repository abstraction in backend/src/services/submission_repository.ts
- [ ] T006 [P] Create metadata repository abstraction in backend/src/services/metadata_repository.ts
- [ ] T007 [P] Create metadata error mapper in backend/src/api/submissions/metadata_error_mapper.ts
- [ ] T008 Register metadata route/controller in backend/src/api/submissions/metadata_controller.ts
- [ ] T009 Ensure auth/authorization middleware protects metadata endpoint in backend/src/api/submissions/metadata_controller.ts

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Save Paper Metadata Successfully (Priority: P1) 🎯 MVP

**Goal**: Validate and store required metadata with confirmation

**Independent Test**: AT-UC08-01

### Implementation for User Story 1

- [ ] T010 [US1] Implement validation + storage + update in backend/src/services/metadata_service.ts
- [ ] T011 [US1] Integrate structured logging + redaction in backend/src/services/metadata_service.ts
- [ ] T012 [US1] Enforce final-submission lock in backend/src/services/metadata_service.ts
- [ ] T013 [US1] Implement success response in backend/src/api/submissions/metadata_controller.ts
- [ ] T014 [P] [US1] Implement metadata form submit + success handling in frontend/src/pages/MetadataPage.tsx
- [ ] T015 [US1] Wire metadata API call in frontend/src/services/metadata_client.ts
- [ ] T016 [P] [US1] Block metadata edits after final submission in frontend/src/pages/MetadataPage.tsx

**Checkpoint**: User Story 1 is independently functional

---

## Phase 4: User Story 2 - Missing Required Metadata Fields (Priority: P2)

**Goal**: Return summary error message for missing fields

**Independent Test**: AT-UC08-02

### Implementation for User Story 2

- [ ] T017 [US2] Add missing-field detection in backend/src/services/metadata_validation.ts
- [ ] T018 [US2] Return missing-fields error in backend/src/api/submissions/metadata_controller.ts
- [ ] T019 [P] [US2] Display summary error message for missing fields in frontend/src/pages/MetadataPage.tsx

**Checkpoint**: User Story 2 is independently functional

---

## Phase 5: User Story 3 - Invalid Metadata Information (Priority: P2)

**Goal**: Return summary validation error for invalid metadata

**Independent Test**: AT-UC08-03

### Implementation for User Story 3

- [ ] T020 [US3] Add invalid-field detection in backend/src/services/metadata_validation.ts
- [ ] T021 [US3] Return invalid-metadata error in backend/src/api/submissions/metadata_controller.ts
- [ ] T022 [P] [US3] Display summary validation error in frontend/src/pages/MetadataPage.tsx

**Checkpoint**: User Story 3 is independently functional

---

## Phase 6: User Story 4 - System Fails to Validate Metadata (Priority: P2)

**Goal**: Handle internal validation errors without storing metadata

**Independent Test**: AT-UC08-04

### Implementation for User Story 4

- [ ] T023 [US4] Map validation failure in backend/src/services/metadata_service.ts
- [ ] T024 [US4] Return validation failure message in backend/src/api/submissions/metadata_controller.ts
- [ ] T025 [P] [US4] Display validation failure message in frontend/src/pages/MetadataPage.tsx

**Checkpoint**: User Story 4 is independently functional

---

## Phase 7: User Story 5 - System Fails to Store Metadata (Priority: P3)

**Goal**: Report storage failure and do not store metadata

**Independent Test**: AT-UC08-05

### Implementation for User Story 5

- [ ] T026 [US5] Map storage failure in backend/src/services/metadata_service.ts
- [ ] T027 [US5] Return storage failure response in backend/src/api/submissions/metadata_controller.ts
- [ ] T028 [P] [US5] Display storage failure message in frontend/src/pages/MetadataPage.tsx

**Checkpoint**: User Story 5 is independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Finish cross-cutting updates and documentation alignment

- [ ] T029 [P] Align API contract in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/008-provide-paper-metadata/contracts/uc-08-metadata.openapi.yaml
- [ ] T030 [P] Update quickstart notes for metadata error handling in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/008-provide-paper-metadata/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup completion; blocks all user stories
- **User Stories (Phase 3+)**: Depend on Foundational completion; can proceed in priority order or parallel
- **Polish (Phase 8)**: Depends on all selected user stories

### User Story Dependencies

- **US1 (P1)**: Starts after Foundational; no dependencies on other stories
- **US2 (P2)**: Starts after Foundational; independent of US1
- **US3 (P2)**: Starts after Foundational; independent of US1/US2
- **US4 (P2)**: Starts after Foundational; independent of US1/US2/US3
- **US5 (P3)**: Starts after Foundational; independent of other stories

### Parallel Opportunities

- Within Phase 1: T001 and T002 can run in parallel
- Within Phase 2: T004 and T005 can run in parallel
- Within each story: frontend and backend tasks marked [P] can run in parallel
- Across stories: any story can run in parallel after Phase 2 if staffing allows

---

## Parallel Example: User Story 1

```bash
Task: "Implement metadata form submit + success handling in frontend/src/pages/MetadataPage.tsx"
Task: "Wire metadata API call in frontend/src/services/metadata_client.ts"
```

## Parallel Example: User Story 2

```bash
Task: "Add missing-field detection in backend/src/services/metadata_validation.ts"
Task: "Display summary error message for missing fields in frontend/src/pages/MetadataPage.tsx"
```

## Parallel Example: User Story 3

```bash
Task: "Add invalid-field detection in backend/src/services/metadata_validation.ts"
Task: "Display summary validation error in frontend/src/pages/MetadataPage.tsx"
```

## Parallel Example: User Story 4

```bash
Task: "Map validation failure in backend/src/services/metadata_service.ts"
Task: "Display validation failure message in frontend/src/pages/MetadataPage.tsx"
```

## Parallel Example: User Story 5

```bash
Task: "Map storage failure in backend/src/services/metadata_service.ts"
Task: "Display storage failure message in frontend/src/pages/MetadataPage.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Validate AT-UC08-01 independently

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 → Validate independently → Demo
3. US2 → Validate independently → Demo
4. US3 → Validate independently → Demo
5. US4 → Validate independently → Demo
6. US5 → Validate independently → Demo

### Parallel Team Strategy

1. Team completes Setup + Foundational
2. After Foundation:
   - Dev A: US1
   - Dev B: US2/US3
   - Dev C: US4/US5
3. Merge stories after independent validation
