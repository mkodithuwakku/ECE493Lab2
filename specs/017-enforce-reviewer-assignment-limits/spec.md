# Feature Specification: Enforce Reviewer Assignment Limits

**Feature Branch**: `017-enforce-reviewer-assignment-limits`  
**Created**: 2026-02-09  
**Status**: Draft  
**Input**: User description: "Generate the specification for UC-17 only. Use UC-17 from GeneratedUseCases.md and ONLY acceptance tests AT-UC17-* from GeneratedTestSuites.md. Ignore all other use cases and tests. Do not invent requirements or flows; derive functional requirements directly from UC-17 main and extension flows and ensure each requirement is verifiable by the provided acceptance tests. Fill the “Use Case Scope” section with UC-17 and list the AT-UC17 tests used."

## Use Case Scope *(mandatory)*

- **Use Case**: UC-17 - Enforce Reviewer Assignment Limits
- **Acceptance Tests**: AT-UC17-01, AT-UC17-02, AT-UC17-03, AT-UC17-04, AT-UC17-05


## Clarifications

### Session 2026-02-09

- Q: What should the rollback/update failure message say? → A: Assignment could not be completed.


- Q: What should the error message say when assignment count cannot be retrieved? → A: Assignment cannot be completed at this time.


- Q: What should the workload-limit message say? → A: Reviewer at assignment limit.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Allow Assignment Below Limit (Priority: P1)

An editor assigns a reviewer whose workload is below the maximum limit and the assignment count is updated.

**Why this priority**: This is the primary flow that must succeed when the reviewer is eligible.

**Independent Test**: Can be fully tested by assigning a reviewer below the limit and verifying assignment and updated count.

**Acceptance Scenarios**:

1. **Given** a logged-in editor, a submitted paper, and a reviewer below the assignment limit, **When** the editor assigns the reviewer, **Then** the system allows the assignment, updates the reviewer’s assignment count, and shows confirmation.

---

### User Story 2 - Block Assignment At Limit (Priority: P2)

The system blocks assignments for reviewers already at the maximum limit.

**Why this priority**: Prevents exceeding workload caps and enforces fairness.

**Independent Test**: Can be fully tested by attempting to assign a reviewer whose count equals the limit.

**Acceptance Scenarios**:

1. **Given** a logged-in editor and a reviewer at the limit, **When** the editor attempts the assignment, **Then** the system blocks it and displays a workload-limit error message.

---

### User Story 3 - Block Assignment That Would Exceed Limit (Priority: P3)

The system blocks assignments that would cause the reviewer to exceed the limit (e.g., concurrent or batch assignments).

**Why this priority**: Ensures limit enforcement under concurrent/batch assignment conditions.

**Independent Test**: Can be fully tested by simulating assignments that would exceed the limit and verifying the blocking behavior.

**Acceptance Scenarios**:

1. **Given** a logged-in editor and a reviewer one below the limit, **When** the editor attempts assignments that would exceed the limit, **Then** the system blocks the excess assignment and shows a workload-limit message.

---

### User Story 4 - Handle Count Retrieval Failure (Priority: P4)

If the system cannot retrieve the reviewer’s assignment count, the assignment is blocked with an error.

**Why this priority**: Prevents assignments when eligibility cannot be verified.

**Independent Test**: Can be fully tested by simulating a count retrieval failure and verifying no assignment is created.

**Acceptance Scenarios**:

1. **Given** a logged-in editor and a retrieval failure, **When** the editor attempts an assignment, **Then** the system shows the error message “Assignment cannot be completed at this time.” and no assignment is created.

---

### User Story 5 - Handle Update Failure After Allowing Assignment (Priority: P5)

If the system fails while updating the assignment count after allowing the assignment, the assignment is rolled back and an error is shown.

**Why this priority**: Prevents partial or inconsistent state.

**Independent Test**: Can be fully tested by simulating update failure after allow and verifying rollback and error.

**Acceptance Scenarios**:

1. **Given** a logged-in editor and a reviewer below the limit, **When** the system fails to update/store the assignment count, **Then** the error message “Assignment could not be completed.” is shown and the assignment is rolled back to a consistent state.

---

### Edge Cases

- What happens when reviewer assignment count cannot be retrieved?
- How does the system handle assignments that would exceed the limit?
- What happens if assignment count update fails after assignment is allowed?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST retrieve the reviewer’s current assignment count before allowing assignment.
- **FR-002**: System MUST compare the current assignment count to the maximum allowed limit.
- **FR-003**: System MUST allow assignment when the reviewer is below the limit and update the reviewer’s assignment count.
- **FR-004**: System MUST block assignment when the reviewer is at the limit and display the message “Reviewer at assignment limit.”
- **FR-005**: System MUST block any assignment that would cause the reviewer to exceed the limit and display the message “Reviewer at assignment limit.”
- **FR-006**: If the system cannot retrieve the reviewer’s assignment count, System MUST display the error message “Assignment cannot be completed at this time.” and MUST NOT create the assignment.
- **FR-007**: If the system fails while updating/storing the assignment count, System MUST roll back the assignment and report the error message “Assignment could not be completed.”
- **FR-008**: System MUST ensure no inconsistent or duplicate assignment records remain after failures.

### Key Entities *(include if feature involves data)*

- **Editor**: Authorized user assigning reviewers to papers.
- **Reviewer**: User with an assignment count and limit.
- **Paper**: Submission receiving reviewer assignments.
- **Assignment**: Link between reviewer and paper.
- **Assignment Limit**: Maximum allowed assignments per reviewer.
- **Assignment Count**: Current number of assignments for a reviewer.

## Assumptions

- Assignment limits are system-configured and apply uniformly unless otherwise specified.
- Reviewer assignment occurs within the CMS reviewer assignment workflow.

## Interfaces & Contracts *(mandatory)*

- **Reviewer Assignment Limit Check**: `POST /papers/{paperId}/reviewers/limit-check` with `reviewerId` in the request body; returns allow/block decision and message. Response outcomes: 200 (allowed + count updated), 409 (workload-limit message), 422 (retrieval failure message), 500 (update failure message). See `contracts/reviewer-assignment-limit-api.yaml`.
- **Assignment Update**: If allowed, assignment is stored and reviewer count updated; failures result in rollback and error messaging.

## Security & Privacy Considerations *(mandatory)*

- **AuthN/AuthZ**: Only authenticated editors can initiate assignments that trigger limit checks.
- **Sensitive Data**: Reviewer workload/assignment count must not be exposed to unauthorized users.
- **Auditability**: Limit checks, blocks, retrieval failures, and rollback events should be observable for support and troubleshooting.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of assignments for reviewers below the limit are allowed and update the assignment count.
- **SC-002**: 100% of assignments for reviewers at the limit are blocked with a workload-limit message.
- **SC-003**: 100% of assignments that would exceed the limit are blocked with a workload-limit message.
- **SC-004**: 100% of assignment attempts during count-retrieval failures display an error and create no assignment.
- **SC-005**: 100% of assignment attempts with update/storage failure result in rollback to a consistent state and show an error.
