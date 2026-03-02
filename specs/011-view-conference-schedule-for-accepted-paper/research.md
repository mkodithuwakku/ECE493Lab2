# Research: UC-11 View Conference Schedule for Accepted Paper

## Decisions

- Decision: Use the existing CMS stack (language, framework, and test tooling already in the project).
  Rationale: Project guidelines require the existing CMS stack; no codebase details indicate a change is needed.
  Alternatives considered: Introducing a new stack or framework (rejected; violates constraints).

- Decision: Use the existing CMS schedule/submissions data store for schedule visibility.
  Rationale: UC-11 relies on published schedules and submission linkage; existing CMS stores schedules/submissions.
  Alternatives considered: New schedule store (rejected; out of scope).

- Decision: Treat this as a web application flow within the CMS.
  Rationale: UC-11 and AT-UC11 tests describe author navigation in the CMS UI.
  Alternatives considered: Standalone schedule portal (rejected; not in scope).
