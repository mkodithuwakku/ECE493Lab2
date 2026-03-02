# Research: UC-12 Receive and Respond to Review Invitation

## Decisions

- Decision: Use the existing CMS stack (language, framework, and test tooling already in the project).
  Rationale: Project guidelines require the existing CMS stack; no codebase details indicate a change is needed.
  Alternatives considered: Introducing a new stack or framework (rejected; violates constraints).

- Decision: Use the existing CMS invitations/assignments data store for responses and assignment updates.
  Rationale: UC-12 depends on invitation state and assignment records; existing CMS stores these.
  Alternatives considered: New invitation store (rejected; out of scope).

- Decision: Treat this as a web application flow within the CMS.
  Rationale: UC-12 and AT-UC12 tests describe reviewer navigation in the CMS UI.
  Alternatives considered: Standalone invitation portal (rejected; not in scope).
