# Data Model: View Conference Registration Prices (UC-02)

**Date**: 2026-02-08

## Entities

### RegistrationPrice

- **Purpose**: Price entry for a specific attendance type.
- **Fields**:
  - `id` (identifier)
  - `attendance_type` (text)
  - `amount` (currency or numeric)
  - `is_active` (boolean)

### AttendanceType

- **Purpose**: Category label used to group pricing entries.
- **Fields**:
  - `id` (identifier)
  - `name` (text)

## Relationships

- `RegistrationPrice.attendance_type` references `AttendanceType.name`.

## Validation Rules

- `attendance_type` and `amount` are required for display.
- Only active prices are eligible for display.

## State Transitions

- None defined for UC-02 (read-only view).
