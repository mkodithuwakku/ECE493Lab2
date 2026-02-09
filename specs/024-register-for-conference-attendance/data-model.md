# Data Model: Register for Conference Attendance

## Entities

### AttendeeRegistration
- **Description**: Registration record linking an attendee to a conference with payment state.
- **Key Fields**:
  - `id` (unique registration identifier)
  - `attendee_id`
  - `conference_id`
  - `attendance_type_id` (optional if not used)
  - `status` (registered | pending_unpaid)
  - `registered_at` (timestamp)
- **Relationships**:
  - References an `AttendanceType` when attendance types are used.

### AttendanceType
- **Description**: Registration category available for attendee selection.
- **Key Fields**:
  - `id`
  - `name`
  - `availability_status` (available | unavailable | invalid)

### RegistrationWindow
- **Description**: Indicates whether registration is currently open.
- **Key Fields**:
  - `is_open` (boolean)
  - `opens_at` (timestamp, optional)
  - `closes_at` (timestamp, optional)

## Validation Rules

- Registration can only proceed when `RegistrationWindow.is_open = true`.
- If attendance types are used, `AttendanceType.availability_status` must be `available`.
- If payment is required and payment fails, registration status must be `pending_unpaid`.
- On storage failure, no registration record is created (or state is rolled back).

## State Transitions

- `registered` set on successful registration when payment is not required.
- `pending_unpaid` set when payment is required but not completed due to unavailability.
