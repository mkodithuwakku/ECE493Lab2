# Quickstart: UC-15 Submit Completed Paper Review

## Purpose
Validate review submission behavior and error handling in line with AT-UC15.

## Preconditions
- CMS is running and accessible.
- Reviewer account exists.
- Reviewer is assigned to the target paper unless testing unauthorized flows.

## Submit Review Successfully (AT-UC15-01)
1. Log in as reviewer.
2. Navigate to Assigned Papers.
3. Select an assigned paper and open the review form.
4. Enter valid values for all required fields.
5. Submit the review.
6. Verify confirmation message and review status reflects submission.

## Reviewer Not Logged In (AT-UC15-02)
1. Attempt to access or submit the review form while logged out.
2. Verify redirect to login and no submission accepted.
3. Log in and access the review form normally.

## Paper Not Assigned to Reviewer (AT-UC15-03)
1. Log in as reviewer.
2. Attempt to access/submit a review for an unassigned paper.
3. Verify access is blocked with a generic authorization error and no review stored.

## Missing Required Review Fields (AT-UC15-04)
1. Log in as reviewer with assigned paper.
2. Leave required fields blank and submit.
3. Verify validation errors identify specific missing fields and submission is rejected.
4. Fill required fields and resubmit successfully.

## Invalid Review Field Values (AT-UC15-05)
1. Log in as reviewer with assigned paper.
2. Enter invalid field values and submit.
3. Verify validation errors identify specific invalid fields and submission is rejected.
4. Correct values and resubmit successfully.

## Duplicate Submission (AT-UC15-06)
1. Submit a valid review.
2. Attempt to submit again.
3. Verify submission is blocked with “Review already submitted.” and no duplicate stored.

## Storage Failure (AT-UC15-07)
1. Log in as reviewer with assigned paper.
2. Enter valid values and submit during a storage failure.
3. Verify error message and no review stored.
