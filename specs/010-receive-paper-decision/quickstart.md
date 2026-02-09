# Quickstart: UC-10 Receive Paper Acceptance or Rejection Decision

## Purpose
Validate that authors can view final decisions for their submissions and that error and access states behave as specified in AT-UC10.

## Preconditions
- CMS is running and accessible.
- An author account exists with at least one submission.
- A final decision may or may not be recorded for the submission, depending on the test.

## Happy Path (AT-UC10-01)
1. Log in as the author.
2. Navigate to My Submissions.
3. Select the submitted paper.
4. Verify the decision displays as Accepted or Rejected for the selected submission.

## Not Yet Available (AT-UC10-02)
1. Log in as the author.
2. Navigate to My Submissions and select the paper with no recorded decision.
3. Verify the system indicates the decision is not yet available and does not show a decision value.

## Not Logged In (AT-UC10-03)
1. Navigate directly to the submissions or decision page without logging in.
2. Verify the system redirects to login and does not reveal decision data.

## Retrieval Error (AT-UC10-04)
1. Log in as the author.
2. Induce a decision retrieval error.
3. Verify an error message is shown and no partial/incorrect decision is displayed.

## Critical Failure (AT-UC10-05)
1. Log in as the author.
2. Induce a critical backend/database failure.
3. Verify the system reports decision data unavailable and shows no decision result.
