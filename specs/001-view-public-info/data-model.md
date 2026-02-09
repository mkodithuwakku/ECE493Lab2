# Data Model: View Public Conference Information (UC-01)

**Date**: 2026-02-08

## Entities

### PublicAnnouncement

- **Purpose**: Publicly visible announcements for guest users.
- **Fields**:
  - `id` (identifier)
  - `content` (text)
  - `is_public` (boolean)

### PublicConferenceInformation

- **Purpose**: General conference information visible to guest users.
- **Fields**:
  - `id` (identifier)
  - `content` (text)
  - `is_public` (boolean)

## Relationships

- None required for UC-01.

## Validation Rules

- `content` is required for any item displayed to guests.
- Only items with `is_public = true` are eligible for display.

## State Transitions

- None defined for UC-01 (read-only view).
