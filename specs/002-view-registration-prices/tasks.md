---

description: "Task list for UC-02 View Conference Registration Prices"
---

# Tasks: View Conference Registration Prices (UC-02)

**Input**: Design documents from `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/002-view-registration-prices/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Tests are OPTIONAL and not explicitly requested in the spec; no test tasks are listed.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Confirm backend structure exists at /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/backend/src/
- [ ] T002 Confirm frontend structure exists at /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/frontend/src/
- [ ] T003 [P] Create UC-02 contract reference at /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/002-view-registration-prices/contracts/uc-02-pricing.openapi.yaml (if not already present)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Define backend response schemas for pricing in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/backend/src/api/schemas/pricing.py
- [ ] T005 [P] Define frontend response types for pricing in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/frontend/src/services/pricing_types.ts
- [ ] T006 Establish pricing message constants for UC-02 in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/frontend/src/services/pricing_messages.ts

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - View Conference Registration Prices (Priority: P1) 🎯 MVP

**Goal**: A guest can view registration prices by attendance type with correct messages for all UC-02 flows.

**Independent Test**: Visiting the pricing page/section shows complete prices, or the correct UC-02 message for no data, partial data, or retrieval error.

### Implementation for User Story 1

- [ ] T007 [P] [US1] Create AttendanceType model in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/backend/src/models/attendance_type.py
- [ ] T008 [P] [US1] Create RegistrationPrice model in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/backend/src/models/registration_price.py
- [ ] T009 [US1] Implement pricing retrieval service in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/backend/src/services/pricing_service.py (depends on T007, T008)
- [ ] T010 [US1] Implement pricing API endpoint in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/backend/src/api/pricing.py
- [ ] T011 [P] [US1] Implement pricing client in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/frontend/src/services/pricing_client.ts
- [ ] T012 [P] [US1] Implement pricing UI component in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/frontend/src/components/pricing_section.tsx
- [ ] T013 [US1] Implement pricing page/section integration in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/frontend/src/pages/pricing.tsx
- [ ] T014 [US1] Handle UC-02 empty/partial/error messages in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/frontend/src/pages/pricing.tsx

**Checkpoint**: User Story 1 should be functional and independently testable

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T015 [P] Validate success criteria traceability to AT-UC02-* in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/002-view-registration-prices/spec.md
- [ ] T016 [P] Align quickstart steps with UC-02 flow in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/002-view-registration-prices/quickstart.md
- [ ] T017 Validate contracts are consistent with behavior in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/002-view-registration-prices/contracts/uc-02-pricing.openapi.yaml

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: Depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on User Story 1 completion

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - no dependencies on other stories

### Within User Story 1

- Models before services
- Services before endpoints
- Client/services before UI integration

### Parallel Opportunities

- T007 and T008 can run in parallel
- T011 and T012 can run in parallel

---

## Parallel Example: User Story 1

```text
Task: "Create AttendanceType model in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/backend/src/models/attendance_type.py"
Task: "Create RegistrationPrice model in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/backend/src/models/registration_price.py"

Task: "Implement pricing client in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/frontend/src/services/pricing_client.ts"
Task: "Implement pricing UI component in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/frontend/src/components/pricing_section.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Validate UC-02 scenarios using quickstart steps
