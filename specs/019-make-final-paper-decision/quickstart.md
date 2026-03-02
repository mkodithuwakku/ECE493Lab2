# Quickstart: UC-19 Make Final Paper Decision

## Purpose
Validate final decision workflows and error handling aligned to AT-UC19.

## Preconditions
- CMS is running and accessible.
- Editor account exists and is authorized.
- Author account exists for target papers.
- Papers exist with required reviews complete or incomplete as needed.

## Record Final Decision: Accept (AT-UC19-01)
1. Log in as editor.
2. Navigate to Paper Management and select a paper with completed reviews.
3. Open the Final Decision interface.
4. Select **Accept** and submit.
5. Verify confirmation message and decision status recorded.
6. Log in as the author and verify decision is visible in the portal.

## Record Final Decision: Reject (AT-UC19-02)
1. Log in as editor.
2. Select a paper with completed reviews.
3. Open Final Decision and select **Reject**.
4. Submit and verify confirmation message.
5. Log in as author and verify decision is visible in the portal.

## Reviews Incomplete: Block Decision (AT-UC19-03)
1. Log in as editor.
2. Select a paper with incomplete reviews.
3. Attempt to submit Accept or Reject.
4. Verify decision is blocked and pending-reviews message is shown.

## Request Additional Reviews (AT-UC19-04)
1. Log in as editor.
2. Select a paper eligible for additional reviews.
3. Choose **Request Additional Reviews** and select reviewers.
4. Confirm request and verify no final decision is recorded.

## Editor Not Logged In / Not Authorized (AT-UC19-05)
1. Attempt to access Final Decision while logged out and verify redirect to login.
2. Log in as non-editor and attempt to access Final Decision.
3. Verify access denied and no decision recorded.

## Decision Notification Fails (AT-UC19-06)
1. Simulate notification failure.
2. Log in as editor and record a final decision.
3. Verify confirmation message.
4. Log in as author and verify decision is visible in portal despite notification failure.

## Fail to Store Final Decision (AT-UC19-07)
1. Simulate storage failure during decision recording.
2. Log in as editor and submit a final decision.
3. Verify error message and no decision recorded.
4. Log in as author and confirm no decision visible.
