# Quickstart: Publish Conference Schedule (UC-23)

## Purpose
Validate UC-23 behavior in the existing CMS environment using AT-UC23-* acceptance tests.

## Prerequisites
- CMS is running and accessible.
- Administrator credentials available.
- Finalized and approved schedule exists for the conference.
- Ability to simulate notification and server/storage failures for negative tests.

## Validate Acceptance Tests

Execute the following acceptance tests from `GeneratedTestSuites.md`:
- AT-UC23-01
- AT-UC23-02
- AT-UC23-03
- AT-UC23-04
- AT-UC23-05
- AT-UC23-06

## Expected Outcomes
- Schedule publishes only when finalized and approved.
- Publication is visible to authors, attendees, and public guests.
- Failure cases produce generic error messages and do not publish the schedule.
- Notification failures produce warnings and are logged without rolling back publication.
