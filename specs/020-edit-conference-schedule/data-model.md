# Data Model: UC-20 Edit Conference Schedule

## Entities

### Administrator
- id (unique)
- name
- email
- role (administrator)

### ConferenceConfiguration
- id (unique)
- submission_deadline
- review_deadline
- conference_start_date
- conference_end_date
- updated_at
- updated_by_admin_id

## Relationships
- Administrator 0..* ConferenceConfiguration (updates)

## Validation Rules
- Required configuration fields must be present.
- Date relationships must be valid: submission_deadline < review_deadline < conference_start_date <= conference_end_date.
- Invalid values or relationships block save and return field-level errors.
- Retrieval failures return error state without partial data.
- Save failures do not persist changes.
