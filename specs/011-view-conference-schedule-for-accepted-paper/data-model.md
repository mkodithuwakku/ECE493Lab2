# Data Model: UC-11 View Conference Schedule for Accepted Paper

## Entities

### Author
- id (unique)
- name
- email

### PaperSubmission
- id (unique)
- title
- author_ids (one or more Author ids)
- status (enum: accepted | other)

### ConferenceSchedule
- id (unique)
- status (enum: published | unpublished)
- entries (one or more ScheduleEntry)

### ScheduleEntry
- submission_id (PaperSubmission id)
- presentation_time
- room_or_location

## Relationships
- Author 1..* PaperSubmission
- ConferenceSchedule 1..* ScheduleEntry
- PaperSubmission 0..1 ScheduleEntry (may be missing if not scheduled)

## Validation Rules
- Only accepted submissions are eligible for schedule entries.
- ScheduleEntry must include presentation_time and room_or_location when present.
- Only author_ids associated with the submission may view the schedule entry for their paper.

## State Transitions
- ConferenceSchedule status: unpublished -> published when released.
