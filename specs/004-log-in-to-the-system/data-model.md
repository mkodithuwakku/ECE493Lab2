# Data Model: Log In to the System (UC-04)

**Date**: 2026-02-08

## Entities

### UserAccount

- **Purpose**: Stored identity for a registered user.
- **Fields**:
  - `id` (identifier)
  - `username` (text, unique, case-insensitive)
  - `email` (text, unique, case-insensitive)
  - `password_hash` (text)
  - `status` (enum: active, locked, disabled)
  - `failed_login_attempts` (integer)
  - `lockout_until` (timestamp, nullable)

### LoginCredentials

- **Purpose**: User-submitted data used for authentication.
- **Fields**:
  - `identifier` (text: username or email)
  - `password` (text)

### AuthenticationResult

- **Purpose**: Output of an authentication attempt.
- **Fields**:
  - `status` (enum: success, invalid_credentials, locked, disabled, service_unavailable, critical_error)
  - `remaining_attempts` (integer, nullable)
  - `message` (text)

### Session

- **Purpose**: Represents an authenticated user session when login succeeds.
- **Fields**:
  - `id` (identifier)
  - `user_id` (identifier)
  - `created_at` (timestamp)

## Relationships

- LoginCredentials are validated against UserAccount.
- Successful AuthenticationResult creates a Session for the UserAccount.

## Validation Rules

- `identifier` and `password` are required.
- Username and email comparison is case-insensitive.
- Lock account after 5 failed attempts within 15 minutes.
- Auto-unlock after 15 minutes.

## State Transitions

- `status`: active -> locked (after lockout threshold)
- `status`: locked -> active (after lockout duration)
- `status`: active -> disabled (administrative action, outside UC-04)
