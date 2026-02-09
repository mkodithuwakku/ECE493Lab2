# Research: Log In to the System (UC-04)

**Date**: 2026-02-08

## Decision: Reuse existing CMS stack

**Rationale**: UC-04 is a standard login workflow and does not require new
languages or frameworks beyond the existing CMS baseline.

**Alternatives considered**:
- Separate auth microservice for login (rejected: unnecessary for UC-04 scope).

## Decision: Web application architecture (frontend + backend)

**Rationale**: UC-04 is accessed via a browser; a frontend login form backed by
backend authentication and account state checks aligns with standard CMS patterns.

**Alternatives considered**:
- Single-process monolith without separation (rejected: reduces clarity between
  UI handling and auth enforcement).

## Decision: Use existing test framework for AT-UC04-* cases

**Rationale**: Acceptance tests define observable outcomes; using the existing
framework avoids introducing new tooling and keeps focus on UC-04 behaviors.

**Alternatives considered**:
- New acceptance test tooling (rejected: unnecessary for a single use case).
