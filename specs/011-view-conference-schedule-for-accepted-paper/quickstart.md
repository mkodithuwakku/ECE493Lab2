# Quickstart: UC-11 View Conference Schedule for Accepted Paper

## Purpose
Validate that authors can view the published schedule entry for their accepted paper and that access/error states match AT-UC11.

## Preconditions
- CMS is running and accessible.
- An author account exists with an accepted paper.
- Conference schedule may be published or unpublished depending on the test.

## Happy Path (AT-UC11-01)
1. Log in as the author.
2. Navigate to My Submissions or Schedule section.
3. Select View Conference Schedule.
4. Verify the schedule shows the author’s paper with presentation time and room/location.

## Not Logged In (AT-UC11-02)
1. Attempt to access the schedule view while logged out.
2. Verify redirect to login and resume schedule view after login.

## Schedule Not Yet Published (AT-UC11-03)
1. Log in as the author.
2. Attempt to view schedule when unpublished.
3. Verify message indicating schedule is not yet published and no valid-looking schedule is shown.

## Retrieval Error (AT-UC11-04)
1. Log in as the author.
2. Induce a schedule retrieval error.
3. Verify temporary unavailability message and no partial/incorrect schedule data.

## Paper Missing From Schedule (AT-UC11-05)
1. Log in as the author.
2. View a published schedule that lacks the author’s paper entry.
3. Verify schedule displays and warning indicates the paper is not yet scheduled.
