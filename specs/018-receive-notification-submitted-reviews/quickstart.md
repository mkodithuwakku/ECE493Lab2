# Quickstart: UC-18 Receive Notification of Submitted Reviews

## Purpose
Validate editor notification delivery and review-status visibility aligned to AT-UC18.

## Preconditions
- CMS is running and accessible.
- Editor account exists and is associated with the paper.
- Reviewer accounts exist and are assigned to the paper.
- Notification system is available unless testing failure scenarios.

## Notification Delivered and Status Updated (AT-UC18-01)
1. Log in as reviewer and submit a completed review for the assigned paper.
2. Log in as editor.
3. Open notifications and locate the review submission notice.
4. Open the referenced paper in Paper Management.
5. Verify review status is updated and review content is visible as permitted.

## Multiple Reviews Submitted (AT-UC18-02)
1. Submit a review as Reviewer A.
2. Submit a review as Reviewer B for the same paper.
3. Log in as editor and check notifications.
4. Verify notifications are separate or aggregated and status reflects both submissions.

## Notification Delivery Fails (AT-UC18-03)
1. Simulate notification delivery failure.
2. Submit a review as a reviewer.
3. Log in as editor and check notifications (may be missing).
4. Open Paper Management and confirm updated review status and review visibility.

## Editor Not Logged In (AT-UC18-04)
1. While logged out, attempt to access notifications or review status directly.
2. Verify redirect to login and no review data displayed.
3. Log in as editor and verify notifications and review status are accessible.

## System Error Retrieving Notifications or Review Status (AT-UC18-05)
1. Simulate a retrieval error for notifications or review status.
2. Log in as editor and attempt to access notifications and review status.
3. Verify a clear error message is displayed and no partial or incorrect data is shown.
