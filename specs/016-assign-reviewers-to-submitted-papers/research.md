# Research: UC-16 Assign Reviewers to Submitted Papers

## Decisions

- Decision: Use existing CMS stack and web UI flow for reviewer assignment.
  Rationale: Project guidelines require the existing CMS stack and UC-16 is UI-driven.
  Alternatives considered: Create a separate reviewer assignment service (rejected due to scope/stack constraints).

- Decision: Use existing CMS assignments/reviewer data store to validate eligibility, store assignments, and update reviewer lists.
  Rationale: Existing stores already track submissions, reviewers, and assignments; reuse avoids duplication.
  Alternatives considered: Create a new assignment subsystem (rejected due to unnecessary complexity).

- Decision: On notification failure, record the assignment and inform the editor of delivery failure.
  Rationale: Aligns with UC-16 clarification and preserves assignment state.
  Alternatives considered: Roll back assignment on notification failure (rejected to avoid losing successful assignments).
