# Data Model: Change User Password (UC-05)

**Date**: 2026-02-08

## Entities

### UserAccount

- **Purpose**: Stored identity for a registered user.
- **Fields**:
  - `id` (identifier)
  - `password_hash` (text, salted hash)
  - `status` (enum: active, locked, disabled)

### PasswordChangeRequest

- **Purpose**: User-submitted data to change password.
- **Fields**:
  - `current_password` (text)
  - `new_password` (text)
  - `confirm_password` (text)

### PasswordPolicy

- **Purpose**: Defines acceptable password requirements.
- **Fields**:
  - `requirements` (text list of rules)

### Session

- **Purpose**: Represents an authenticated user session.
- **Fields**:
  - `id` (identifier)
  - `user_id` (identifier)
  - `created_at` (timestamp)

## Relationships

- PasswordChangeRequest is validated against UserAccount and PasswordPolicy.
- Successful password change invalidates all Sessions for the UserAccount.

## Validation Rules

- `current_password`, `new_password`, and `confirm_password` are required.
- `new_password` must satisfy PasswordPolicy.
- `new_password` must match `confirm_password`.

## State Transitions

- UserAccount password_hash updated on successful change.
- Sessions invalidated after successful change.
