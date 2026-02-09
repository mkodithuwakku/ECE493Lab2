# Feature Specification: Make Final Paper Decision

**Feature Branch**: `019-make-final-paper-decision`  
**Created**: 2026-02-09  
**Status**: Draft  
**Input**: User description: "Make Final Paper Decision (UC-19)"

## Use Case Scope *(mandatory)*

- **Use Case**: UC-19 - Make Final Paper Decision
- **Acceptance Tests**: AT-UC19-01, AT-UC19-02, AT-UC19-03, AT-UC19-04, AT-UC19-05, AT-UC19-06, AT-UC19-07

## Clarifications

### Session 2026-02-09

- Q: Should editors be allowed to revise a final decision after it’s recorded? → A: Lock decision after submission.
- Q: Should non-editor users be blocked at the decision interface entirely, or allowed to view the interface in read-only mode? → A: Block access entirely (redirect/deny).
- Q: Should authors see the final decision immediately after it’s recorded, or only after a notification is successfully delivered? → A: Immediate portal visibility after recording.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Record Final Decision (Priority: P1)

An editor records a final accept or reject decision for a paper with all required reviews completed, and the author can view the decision in the portal.

**Why this priority**: This is the core goal of UC-19 and enables the conference to finalize paper outcomes.

**Independent Test**: Can be tested by recording an accept or reject decision on a fully reviewed paper and verifying the author can view the decision.

**Acceptance Scenarios**:

1. **Given** a paper with completed required reviews and no prior final decision, **When** the editor submits an **Accept** decision, **Then** the decision is recorded and visible to the author.
2. **Given** a paper with completed required reviews and no prior final decision, **When** the editor submits a **Reject** decision, **Then** the decision is recorded and visible to the author.

---

### User Story 2 - Block Decision When Reviews Incomplete (Priority: P2)

If required reviews are incomplete, the system blocks final decision submission and informs the editor.

**Why this priority**: Prevents premature decisions and preserves review integrity.

**Independent Test**: Can be tested by attempting to submit a decision for a paper with incomplete reviews and verifying the block and message.

**Acceptance Scenarios**:

1. **Given** a paper with incomplete required reviews, **When** the editor attempts to submit a final decision, **Then** the system blocks submission and displays a pending-reviews message.

---

### User Story 3 - Request Additional Reviews Instead of Final Decision (Priority: P2)

An editor can request additional reviews from the decision interface instead of finalizing a decision.

**Why this priority**: Enables editors to obtain more feedback when current reviews are insufficient.

**Independent Test**: Can be tested by requesting additional reviews from a paper’s decision interface and verifying the request is recorded and the paper remains undecided.

**Acceptance Scenarios**:

1. **Given** a paper eligible for additional review requests, **When** the editor selects **Request Additional Reviews**, **Then** the request is recorded and no final decision is stored.

---

### User Story 4 - Authorization Required for Final Decisions (Priority: P3)

Only authenticated editors can access the final decision interface and submit decisions.

**Why this priority**: Protects decision authority and prevents unauthorized changes.

**Independent Test**: Can be tested by attempting access while logged out or as a non-editor and verifying access is denied.

**Acceptance Scenarios**:

1. **Given** the user is not logged in, **When** they attempt to access the final decision interface, **Then** they are redirected to login and cannot submit a decision.
2. **Given** the user is logged in as a non-editor, **When** they attempt to submit a final decision, **Then** access is denied and no decision is recorded.

---

### User Story 5 - Decision Visible Even If Notification Fails (Priority: P3)

If decision notification delivery fails, the decision is still recorded and visible to the author in the portal.

**Why this priority**: Ensures authors can see outcomes even when notifications fail.

**Independent Test**: Can be tested by recording a decision during notification failure and verifying the author can still view the decision.

**Acceptance Scenarios**:

1. **Given** notification delivery fails during decision submission, **When** the editor submits a final decision, **Then** the decision is recorded and visible to the author in the portal.

---

### User Story 6 - Error on Decision Storage Failure (Priority: P3)

If the system cannot store a final decision, the editor is informed and no decision is recorded.

**Why this priority**: Prevents false success and ensures clarity on decision state.

**Independent Test**: Can be tested by simulating storage failure and verifying an error message and no recorded decision.

**Acceptance Scenarios**:

1. **Given** a storage failure occurs, **When** the editor submits a final decision, **Then** the system shows an error message and the paper remains undecided.

### Edge Cases

- What happens when a paper already has a recorded final decision?
- What happens when an editor attempts to change a recorded final decision?
- How does the system handle decision submission when reviews become incomplete due to late changes?
- What happens when notification delivery fails but the author is offline?
- How does the system behave if the editor abandons the decision after seeing a storage error?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST allow an authenticated editor to select and submit a final **Accept** decision for a paper with completed required reviews.
- **FR-002**: The system MUST allow an authenticated editor to select and submit a final **Reject** decision for a paper with completed required reviews.
- **FR-003**: The system MUST record the final decision in the system and update the paper’s decision status.
- **FR-004**: The author MUST be able to view the recorded final decision for their paper in the portal immediately after recording.
- **FR-005**: The system MUST block final decision submission when required reviews are incomplete and display a pending-reviews message indicating the decision cannot be recorded until reviews are complete.
- **FR-006**: The system MUST allow the editor to request additional reviews instead of submitting a final decision and keep the paper undecided.
- **FR-007**: The system MUST restrict final decision access to authenticated editors and deny access to unauthorized users (block interface entirely for non-editors).
- **FR-008**: If decision notification delivery fails, the system MUST still record the decision and make it visible to the author in the portal.
- **FR-009**: If the system cannot store the final decision, it MUST display an error message and MUST NOT record the decision.
- **FR-010**: The system MUST provide the editor with a confirmation message when a final decision is successfully recorded, including the decision value and paper identifier.
- **FR-011**: Once recorded, a final decision MUST be locked from further edits.

### Key Entities *(include if feature involves data)*

- **Paper**: Submitted manuscript with review completion status and decision status.
- **Review**: Evaluation submitted for a paper that determines decision eligibility.
- **Decision**: Final accept/reject outcome recorded for a paper.
- **Editor**: User role authorized to make final decisions.
- **Author**: User role that views decision outcomes for their submissions.
- **Notification**: Message indicating a final decision outcome to the author.

## Assumptions & Dependencies

- Review submission and review completion status are provided by existing review workflows.
- Decision viewing in the author portal is available for recorded decisions.
- Requesting additional reviews uses the existing reviewer assignment workflow.
- Final decisions are not revised within this use case once recorded.
- Once recorded, final decisions are locked and cannot be edited.

## Interfaces & Contracts *(mandatory)*

- **Final Decision Interface**: Inputs are selected paper and decision choice; outputs are recorded decision, confirmation message, or error.
- **Decision Status View (Author Portal)**: Inputs are authenticated author access and paper selection; outputs are decision status for the paper.
- **Additional Review Request Flow**: Inputs are editor request and selected reviewers; outputs are recorded reviewer requests and paper remains undecided.
- **Decision Notification**: Outputs are author notifications of decisions; errors include notification delivery failure.

## Security & Privacy Considerations *(mandatory)*

- **AuthN/AuthZ**: Only authenticated editors can submit decisions; authors can view decisions only for their own papers.
- **Sensitive Data**: Decision outcomes are visible only to authorized users; error messages avoid exposing internal system details.
- **Auditability**: Final decision submissions and notification failures are recorded for traceability.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of final decision submissions for papers with completed reviews result in a recorded decision and confirmation message.
- **SC-002**: 100% of recorded decisions are visible to the correct author in the portal.
- **SC-003**: 100% of attempts to decide with incomplete reviews are blocked with a pending-reviews message.
- **SC-004**: 100% of unauthorized decision access attempts are denied.
- **SC-005**: When notification delivery fails, 100% of decisions remain visible to authors in the portal.
- **SC-006**: When storage failures are simulated, 100% of attempts show an error and do not record a decision.
