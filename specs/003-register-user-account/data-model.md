# Data Model: Register a New User Account (UC-03)

**Date**: 2026-02-08

## Entities

### UserAccount

- **Purpose**: Stored identity for a registered user.
- **Fields**:
  - `id` (identifier)
  - `email` (text, unique)
  - `password_hash` (text)
  - `created_at` (timestamp)

### RegistrationFormInput

- **Purpose**: User-submitted data used to create a user account.
- **Fields**:
  - `email` (text)
  - `password` (text)

## Relationships

- RegistrationFormInput is validated and then persisted as UserAccount.

## Validation Rules

- `email` is required and must be unique.
- `password` is required and must meet security requirements.

## State Transitions

- None defined for UC-03 (single create flow).
