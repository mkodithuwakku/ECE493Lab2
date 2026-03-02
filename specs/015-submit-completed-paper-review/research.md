# Research: UC-15 Submit Completed Paper Review

## Decisions

- Decision: Use existing CMS stack and web UI flow for review submission.
  Rationale: Project guidelines require the existing CMS stack and UC-15 is UI-driven.
  Alternatives considered: Introduce a separate review submission service (rejected due to scope/stack constraints).

- Decision: Use existing CMS submissions/reviews data store for validation, storage, and association to reviewer-paper pairs.
  Rationale: Existing stores already track submissions and assignments; reuse avoids duplication.
  Alternatives considered: Create a new review storage system (rejected due to unnecessary complexity).

- Decision: Block duplicate submissions and show a “Review already submitted” message.
  Rationale: Aligns with UC-15 clarification and prevents duplicate records.
  Alternatives considered: Treat as update (rejected to avoid expanding scope into edit/update flow).
