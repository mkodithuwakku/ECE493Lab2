<!--
Sync Impact Report
- Version change: 0.1.0 -> 0.2.0
- Modified principles: None
- Added sections: None
- Removed sections: None
- Modified sections: Development Workflow & Quality Gates
- Templates requiring updates:
  - updated: .specify/templates/plan-template.md
  - updated: .specify/templates/spec-template.md
  - updated: .specify/templates/tasks-template.md
  - pending: .specify/templates/commands/*.md (directory not found)
- Follow-up TODOs: None
-->
# Conference Management System (CMS) Constitution

## Core Principles

### I. User-Value Slices First
Every feature MUST be planned and delivered as independent, user-valued slices.
- Each feature spec MUST define prioritized user stories with independent tests.
- Each user story MUST be implementable, demoable, and testable on its own.
- Cross-story dependencies MUST be explicit and justified in the plan.
Rationale: Small, independent slices reduce integration risk and enable incremental delivery.

### II. Explicit Interfaces & Contracts
All externally visible behavior MUST be specified as contracts before implementation.
- Public endpoints, UI flows, and integrations MUST have documented inputs, outputs,
  and error behaviors.
- Breaking contract changes MUST include a version bump and a migration plan.
- Data schemas shared across components MUST be versioned and backwards compatible
  unless a migration plan is approved.
Rationale: Contracts prevent accidental breakage and make integration predictable.

### III. Spec-Driven Test Discipline
Testing requirements are dictated by the feature spec and enforced in execution.
- If the spec requires tests, those tests MUST be written first and must fail
  before implementation begins.
- Each user story MUST have at least one independent acceptance scenario.
- All required tests MUST pass before merge or release.
Rationale: Test discipline preserves correctness and supports safe iteration.

### IV. Security & Privacy First
Security and privacy are non-negotiable for all non-public system capabilities.
- All authenticated flows MUST enforce authorization with least privilege.
- Sensitive data (PII, credentials, payment data) MUST be protected in storage and
  transit, and MUST NOT appear in logs.
- Administrative actions MUST be auditable.
Rationale: The CMS handles user accounts and payments, requiring strong safeguards.

### V. Operational Visibility & Error Clarity
The system MUST be observable and failure modes MUST be explicit.
- Structured logging with request/trace identifiers is REQUIRED for critical flows.
- User-facing errors MUST be clear and actionable; internal failures MUST be logged.
- Failures MUST degrade gracefully without corrupting data.
Rationale: Clear visibility reduces support burden and speeds incident resolution.

## Security & Privacy Requirements

- Authentication is REQUIRED for all non-public actions.
- Authorization roles MUST include at least: Administrator, Author, Attendee, Guest.
- Passwords MUST be stored using a modern, salted hash.
- Payment handling MUST use a vetted gateway; sensitive card data MUST NOT be stored.
- Audit logs MUST capture administrator actions that affect schedules, accounts,
  pricing, and publication status.

## Development Workflow & Quality Gates

- Every feature MUST have a spec (`spec.md`), plan (`plan.md`), and tasks list
  (`tasks.md`) before implementation starts.
- The source of truth for requirements is `GeneratedUseCases.md` (UC-01 to UC-26)
  and the source of truth for acceptance tests is `GeneratedTestSuites.md`
  (AT-UCxx-yy). Work MUST be scoped to the selected use case and its matching
  `AT-UCxx-*` tests only.
- A dedicated git branch per use case is REQUIRED with the name `uc-XX`.
- The plan MUST include a Constitution Check with explicit pass/fail gates.
- Breaking changes MUST include a migration plan and a versioning note.
- Code review is REQUIRED for all merges to mainline branches.
- Updates to contracts and user-facing behavior MUST update specs and tests.

## Governance

- This constitution supersedes all other project guidelines.
- Amendments require a documented proposal, approval by project maintainers, and
  a version bump aligned to semantic versioning (MAJOR/MINOR/PATCH).
- Compliance MUST be reviewed in feature specs, implementation plans, and task
  lists before work proceeds.

**Version**: 0.2.0 | **Ratified**: 2026-02-08 | **Last Amended**: 2026-02-08
