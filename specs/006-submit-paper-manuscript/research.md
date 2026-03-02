# Research: Submit a Paper Manuscript (UC-06)

**Date**: 2026-02-08

## Decision: Reuse existing CMS stack

**Rationale**: UC-06 is a standard manuscript upload workflow and does not
require new languages or frameworks beyond the existing CMS baseline.

**Alternatives considered**:
- Separate upload microservice (rejected: unnecessary for UC-06 scope).

## Decision: Web application architecture (frontend + backend)

**Rationale**: UC-06 is accessed via a browser; a frontend upload UI backed by
backend validation and storage aligns with standard CMS patterns.

**Alternatives considered**:
- Single-process monolith without separation (rejected: reduces clarity between
  UI handling and storage enforcement).

## Decision: Use existing test framework for AT-UC07-* cases

**Rationale**: Acceptance tests define observable outcomes; using the existing
framework avoids introducing new tooling and keeps focus on UC-06 behaviors.

**Alternatives considered**:
- New acceptance test tooling (rejected: unnecessary for a single use case).
