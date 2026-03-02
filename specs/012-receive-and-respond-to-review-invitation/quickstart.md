# Quickstart: UC-12 Receive and Respond to Review Invitation

## Purpose
Validate that reviewers can accept or reject invitations and that access/error states match AT-UC12.

## Preconditions
- CMS is running and accessible.
- Reviewer account exists with a valid email address.
- A pending invitation exists for the reviewer.

## Accept Invitation (AT-UC12-01)
1. Log in as the reviewer.
2. Navigate to Review Invitations.
3. Select a pending invitation and accept.
4. Verify assignment is recorded and confirmation is shown.

## Reject Invitation (AT-UC12-02)
1. Log in as the reviewer.
2. Navigate to Review Invitations.
3. Select a pending invitation and reject.
4. Verify rejection is recorded, editor is notified, and confirmation is shown.

## Email Failure (AT-UC12-03)
1. Simulate email delivery failure.
2. Log in to the CMS manually.
3. Respond to the invitation in Review Invitations.
4. Verify email failure is logged and response is recorded.

## Not Logged In (AT-UC12-04)
1. Attempt to access Review Invitations while logged out.
2. Verify redirect to login and resume after login.

## Assignment Limit (AT-UC12-05)
1. Ensure reviewer is at assignment limit.
2. Attempt to accept invitation.
3. Verify acceptance is blocked, error shown, and editor notified.

## Response Record Error (AT-UC12-06)
1. Simulate response recording error.
2. Attempt to accept or reject.
3. Verify error shown, response not saved, invitation remains pending.
