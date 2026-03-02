# Research: UC-13 View Assigned Papers

## Decisions

- Decision: Use the existing CMS stack (language, framework, and test tooling already in the project).
  Rationale: Project guidelines require the existing CMS stack; no codebase details indicate a change is needed.
  Alternatives considered: Introducing a new stack or framework (rejected; violates constraints).

- Decision: Use the existing CMS assignments data store for reviewer assignment lists.
  Rationale: UC-13 depends on assigned papers data; existing CMS stores assignments.
  Alternatives considered: New assignments store (rejected; out of scope).

- Decision: Treat this as a web application flow within the CMS.
  Rationale: UC-13 and AT-UC13 tests describe reviewer navigation in the CMS UI.
  Alternatives considered: Standalone reviewer portal (rejected; not in scope).
