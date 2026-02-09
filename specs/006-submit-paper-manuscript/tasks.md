---

description: "Task list for UC-06 manuscript upload implementation"
---

# Tasks: Submit a Paper Manuscript (UC-06)

**Input**: Design documents from `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/006-submit-paper-manuscript/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Not requested in the feature specification; no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.
**Scope**: Tasks map to UC-06 and acceptance tests AT-UC07-* only.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize shared modules used across manuscript upload stories

- [ ] T001 Create upload logging utility for manuscript uploads in backend/src/services/upload_logger.ts
- [ ] T002 [P] Create file validation helper in backend/src/services/file_validation.ts
- [ ] T003 [P] Create manuscript upload API client wrapper in frontend/src/services/manuscript_client.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core building blocks needed by all user stories

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create submission repository abstraction in backend/src/services/submission_repository.ts
- [ ] T005 [P] Create file storage service wrapper in backend/src/services/file_storage_service.ts
- [ ] T006 [P] Create log redaction helper for upload metadata in backend/src/services/log_redactor.ts
- [ ] T007 Create upload error mapper in backend/src/api/submissions/upload_error_mapper.ts

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Upload Manuscript Successfully (Priority: P1) 🎯 MVP

**Goal**: Upload a valid manuscript file and associate it with the current submission

**Independent Test**: AT-UC07-01

### Implementation for User Story 1

- [ ] T008 [US1] Implement upload validation + store association in backend/src/services/manuscript_upload_service.ts
- [ ] T009 [US1] Implement upload controller success response in backend/src/api/submissions/manuscript_upload_controller.ts
- [ ] T010 [P] [US1] Implement upload UI submit + success handling in frontend/src/pages/ManuscriptUploadPage.tsx
- [ ] T011 [US1] Wire upload API call in frontend/src/services/manuscript_client.ts

**Checkpoint**: User Story 1 is independently functional

---

## Phase 4: User Story 2 - Reject Unsupported File Format (Priority: P2)

**Goal**: Reject unsupported formats with acceptable format error

**Independent Test**: AT-UC07-02

### Implementation for User Story 2

- [ ] T012 [US2] Add unsupported-format handling in backend/src/services/file_validation.ts
- [ ] T013 [US2] Return unsupported-format error in backend/src/api/submissions/manuscript_upload_controller.ts
- [ ] T014 [P] [US2] Display unsupported-format error in frontend/src/pages/ManuscriptUploadPage.tsx

**Checkpoint**: User Story 2 is independently functional

---

## Phase 5: User Story 3 - Reject File Exceeding Size Limit (Priority: P2)

**Goal**: Reject oversized files with size restriction error

**Independent Test**: AT-UC07-03

### Implementation for User Story 3

- [ ] T015 [US3] Add size limit validation in backend/src/services/file_validation.ts
- [ ] T016 [US3] Return size restriction error in backend/src/api/submissions/manuscript_upload_controller.ts
- [ ] T017 [P] [US3] Display size restriction error in frontend/src/pages/ManuscriptUploadPage.tsx

**Checkpoint**: User Story 3 is independently functional

---

## Phase 6: User Story 4 - Handle Upload Interruption (Priority: P2)

**Goal**: Detect interrupted uploads and allow retry without association

**Independent Test**: AT-UC07-04

### Implementation for User Story 4

- [ ] T018 [US4] Detect upload interruption in backend/src/services/manuscript_upload_service.ts
- [ ] T019 [US4] Return upload interruption error in backend/src/api/submissions/manuscript_upload_controller.ts
- [ ] T020 [P] [US4] Display interruption error and retry option in frontend/src/pages/ManuscriptUploadPage.tsx

**Checkpoint**: User Story 4 is independently functional

---

## Phase 7: User Story 5 - Handle Storage Failure (Priority: P3)

**Goal**: Report storage failure and do not associate file

**Independent Test**: AT-UC07-05

### Implementation for User Story 5

- [ ] T021 [US5] Map storage failure to error in backend/src/services/manuscript_upload_service.ts
- [ ] T022 [US5] Return storage failure response in backend/src/api/submissions/manuscript_upload_controller.ts
- [ ] T023 [P] [US5] Display storage failure message in frontend/src/pages/ManuscriptUploadPage.tsx

**Checkpoint**: User Story 5 is independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Finish cross-cutting updates and documentation alignment

- [ ] T024 [P] Align API contract in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/006-submit-paper-manuscript/contracts/uc-06-manuscript-upload.openapi.yaml
- [ ] T025 [P] Update quickstart notes for upload error handling in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/006-submit-paper-manuscript/quickstart.md
- [ ] T026 Add log redaction coverage in backend/src/services/upload_logger.ts

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

- Within Phase 1: T002 and T003 can run in parallel
- Within Phase 2: T005 and T006 can run in parallel
- Within each story: frontend and backend tasks marked [P] can run in parallel
- Across stories: any story can run in parallel after Phase 2 if staffing allows

---

## Parallel Example: User Story 1

```bash
Task: "Implement upload UI submit + success handling in frontend/src/pages/ManuscriptUploadPage.tsx"
Task: "Wire upload API call in frontend/src/services/manuscript_client.ts"
```

## Parallel Example: User Story 2

```bash
Task: "Add unsupported-format handling in backend/src/services/file_validation.ts"
Task: "Display unsupported-format error in frontend/src/pages/ManuscriptUploadPage.tsx"
```

## Parallel Example: User Story 3

```bash
Task: "Add size limit validation in backend/src/services/file_validation.ts"
Task: "Display size restriction error in frontend/src/pages/ManuscriptUploadPage.tsx"
```

## Parallel Example: User Story 4

```bash
Task: "Detect upload interruption in backend/src/services/manuscript_upload_service.ts"
Task: "Display interruption error and retry option in frontend/src/pages/ManuscriptUploadPage.tsx"
```

## Parallel Example: User Story 5

```bash
Task: "Map storage failure to error in backend/src/services/manuscript_upload_service.ts"
Task: "Display storage failure message in frontend/src/pages/ManuscriptUploadPage.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Validate AT-UC07-01 independently

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
