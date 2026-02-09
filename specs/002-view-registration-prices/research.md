# Research: View Conference Registration Prices (UC-02)

**Date**: 2026-02-08

## Decision: Reuse existing CMS stack

**Rationale**: UC-02 is a public, read-only pricing view and does not require
new languages or frameworks beyond the existing CMS baseline.

**Alternatives considered**:
- New standalone pricing service (rejected: unnecessary for UC-02 scope).

## Decision: Web application architecture (frontend + backend)

**Rationale**: UC-02 is accessed via a browser; a frontend pricing section backed
by a backend pricing retrieval aligns with standard CMS patterns.

**Alternatives considered**:
- Single-process monolith without separation (rejected: reduces clarity between
  data retrieval and UI rendering).

## Decision: Use existing test framework for AT-UC02-* cases

**Rationale**: Acceptance tests define observable outcomes; using the existing
framework avoids introducing new tooling and keeps focus on UC-02 behaviors.

**Alternatives considered**:
- New acceptance test tooling (rejected: unnecessary for a single use case).
