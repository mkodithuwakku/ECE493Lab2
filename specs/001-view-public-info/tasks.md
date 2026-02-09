---

description: "Task list for UC-01 View Public Conference Information"
---

# Tasks: View Public Conference Information (UC-01)

**Input**: Design documents from `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/001-view-public-info/`
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
- [ ] T003 [P] Create UC-01 contract reference at /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/001-view-public-info/contracts/uc-01-public-info.openapi.yaml (if not already present)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Define backend response schemas for public info in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/backend/src/api/schemas/public_info.py
- [ ] T005 [P] Define frontend response types for public info in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/frontend/src/services/public_info_types.ts
- [ ] T006 Establish error message constants for UC-01 in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/frontend/src/services/public_info_messages.ts

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - View Public Conference Information (Priority: P1) 🎯 MVP

**Goal**: A guest can view public announcements and conference information on the homepage with correct messages for all UC-01 flows.

**Independent Test**: Visiting the CMS homepage surfaces public info or the correct UC-01 error/empty/partial message based on data and availability state.

### Implementation for User Story 1

- [ ] T007 [P] [US1] Create PublicAnnouncement model in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/backend/src/models/public_announcement.py
- [ ] T008 [P] [US1] Create PublicConferenceInformation model in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/backend/src/models/public_conference_information.py
- [ ] T009 [US1] Implement public info retrieval service in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/backend/src/services/public_info_service.py (depends on T007, T008)
- [ ] T010 [US1] Implement public homepage API endpoint in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/backend/src/api/public_info.py
- [ ] T011 [P] [US1] Implement public info client in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/frontend/src/services/public_info_client.ts
- [ ] T012 [P] [US1] Implement public info UI component in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/frontend/src/components/public_info_section.tsx
- [ ] T013 [US1] Implement homepage integration in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/frontend/src/pages/homepage.tsx
- [ ] T014 [US1] Handle UC-01 empty/partial/error messages in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/frontend/src/pages/homepage.tsx

**Checkpoint**: User Story 1 should be functional and independently testable

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T015 [P] Align quickstart steps with UC-01 flow in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/001-view-public-info/quickstart.md
- [ ] T016 Validate contracts are consistent with behavior in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/001-view-public-info/contracts/uc-01-public-info.openapi.yaml

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
Task: "Create PublicAnnouncement model in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/backend/src/models/public_announcement.py"
Task: "Create PublicConferenceInformation model in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/backend/src/models/public_conference_information.py"

Task: "Implement public info client in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/frontend/src/services/public_info_client.ts"
Task: "Implement public info UI component in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/frontend/src/components/public_info_section.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Validate UC-01 scenarios using quickstart steps
