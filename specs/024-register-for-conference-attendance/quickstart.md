# Quickstart: Register for Conference Attendance (UC-24)

## Purpose
Validate UC-24 behavior in the existing CMS environment using AT-UC24-* acceptance tests.

## Prerequisites
- CMS is running and accessible.
- Attendee credentials available.
- Registration window can be opened/closed for testing.
- Attendance types are configured (if applicable).
- Ability to simulate payment service unavailability and backend storage failures.

## Validate Acceptance Tests

Execute the following acceptance tests from `GeneratedTestSuites.md`:
- AT-UC24-01
- AT-UC24-02
- AT-UC24-03
- AT-UC24-04
- AT-UC24-05
- AT-UC24-06

## Expected Outcomes
- Registration succeeds when open and inputs are valid.
- Unauthenticated users are redirected to login.
- Registration is blocked when closed.
- Invalid/unavailable attendance types are rejected.
- Payment unavailability yields a pending/unpaid registration state and an error message.
- Storage failures yield an error message and no completed registration.
