# Research: Change User Password (UC-05)

**Date**: 2026-02-08

## Decision: Reuse existing CMS stack

**Rationale**: UC-05 is a standard password change workflow and does not require
new languages or frameworks beyond the existing CMS baseline.

**Alternatives considered**:
- Separate auth microservice for password change (rejected: unnecessary for UC-05 scope).

## Decision: Web application architecture (frontend + backend)

**Rationale**: UC-05 is accessed via a browser; a frontend change-password form
backed by backend validation and persistence aligns with standard CMS patterns.

**Alternatives considered**:
- Single-process monolith without separation (rejected: reduces clarity between
  UI handling and auth enforcement).

## Decision: Use existing test framework for AT-UC05-* cases

**Rationale**: Acceptance tests define observable outcomes; using the existing
framework avoids introducing new tooling and keeps focus on UC-05 behaviors.

**Alternatives considered**:
- New acceptance test tooling (rejected: unnecessary for a single use case).
