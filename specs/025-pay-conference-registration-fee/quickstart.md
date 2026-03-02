# Quickstart: Pay Conference Registration Fee (UC-25)

## Purpose
Validate UC-25 behavior in the existing CMS environment using AT-UC25-* acceptance tests.

## Prerequisites
- CMS is running and accessible.
- Attendee credentials available.
- Attendee has a pending/unpaid registration.
- Payment gateway configured for success/decline/cancel/timeout simulations.
- Ability to simulate storage failure after gateway success.

## Validate Acceptance Tests

Execute the following acceptance tests from `GeneratedTestSuites.md`:
- AT-UC25-01
- AT-UC25-02
- AT-UC25-03
- AT-UC25-04
- AT-UC25-05
- AT-UC25-06
- AT-UC25-07
- AT-UC25-08

## Expected Outcomes
- Payment succeeds and updates registration to paid/confirmed.
- Unauthenticated users are redirected to login.
- No pending payment blocks payment initiation.
- Declines, cancellations, and gateway unavailability leave registration unpaid/pending.
- Recording failures after gateway success show an error and keep registration unpaid/pending.
