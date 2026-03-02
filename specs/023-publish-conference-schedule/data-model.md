# Data Model: Publish Conference Schedule

## Entities

### ConferenceSchedule
- **Description**: Finalized and approved conference schedule that can be published for access by authors, attendees, and public guests.
- **Key Fields**:
  - `id` (unique schedule identifier)
  - `status` (unpublished | published)
  - `is_finalized` (boolean)
  - `is_approved` (boolean)
  - `published_at` (timestamp, optional)
- **Relationships**:
  - Referenced by publication status checks and schedule view endpoints.

### PublicationStatus
- **Description**: Derived state indicating whether a schedule is published.
- **Key Fields**:
  - `schedule_id`
  - `state` (unpublished | published)
  - `changed_at` (timestamp)
  - `changed_by` (administrator identifier)

### NotificationDeliveryResult
- **Description**: Record of notification attempt outcomes for authors and attendees.
- **Key Fields**:
  - `schedule_id`
  - `delivery_status` (success | failure)
  - `failure_reason` (optional)
  - `attempted_at` (timestamp)

## Validation Rules

- A schedule can only transition to `published` if `is_finalized = true` and `is_approved = true`.
- Unpublished schedules must remain inaccessible to intended users requiring published access.
- Notification failures do not roll back the publication status.

## State Transitions

- `unpublished` → `published` upon successful publish action and status persistence.
- `published` remains `published` after refresh/reload (no implicit rollback).
