# Data Model: UC-21 Generate Conference Schedule

## Entities

### Administrator
- id (unique)
- name
- email
- role (administrator)

### AcceptedPaper
- id (unique)
- title
- track
- status (accepted)

### SchedulingResources
- rooms
- time_slots
- conference_dates

### Schedule
- id (unique)
- generated_at
- generated_by_admin_id
- entries (paper_id, room, time_slot)
- status (generated)

## Relationships
- Administrator 0..* Schedule
- Schedule 1..* AcceptedPaper (assigned)

## Validation Rules
- Schedule generation requires at least one accepted paper.
- Scheduling resources must be sufficient to assign all accepted papers.
- Constraint violations prevent schedule persistence.
- Generation failures or storage failures do not create a stored schedule.
