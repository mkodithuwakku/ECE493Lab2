# Quickstart: Receive Payment Confirmation and Ticket (UC-26)

## Purpose
Validate UC-26 behavior in the existing CMS environment using AT-UC26-* acceptance tests.

## Prerequisites
- CMS is running and accessible.
- Attendee credentials available.
- Attendee has a paid/confirmed registration.
- Receipt functionality can be enabled/disabled.
- Ability to simulate email delivery failure and backend retrieval/generation errors.

## Validate Acceptance Tests

Execute the following acceptance tests from `GeneratedTestSuites.md`:
- AT-UC26-01
- AT-UC26-02
- AT-UC26-03
- AT-UC26-04
- AT-UC26-05
- AT-UC26-06

## Expected Outcomes
- Confirmation and ticket are viewable for paid/confirmed registrations.
- Receipt view/download works when enabled.
- Unauthenticated access is redirected to login.
- Unauthorized access to other users’ confirmations is blocked with a safe redirect.
- Unpaid/unconfirmed registrations are blocked from confirmation/receipt access.
- Retrieval/generation failures show clear errors without partial data.
