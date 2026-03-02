# Quickstart: Change User Password (UC-05)

**Date**: 2026-02-08

## Purpose

Validate the UC-05 change-password flow for registered users.

## Steps

1. Start the existing CMS application using the project’s standard run steps.
2. Log in as a registered user.
3. Navigate to Account Settings or Profile and select Change Password.
4. Submit a valid current password, a new password that meets requirements, and a matching confirmation.
5. Verify “Password changed successfully.”, session termination, and ability to log in with the new password only. (AT-UC05-01)
6. Submit an incorrect current password and verify “Current password is incorrect.” and no change. (AT-UC05-02)
7. Submit a new password that violates requirements and verify “Password must be at least 8 characters and include a non-letter character.” and no change. (AT-UC05-03)
8. Submit mismatched new password and confirmation and verify “New password and confirmation do not match.” and no change. (AT-UC05-04)
9. Simulate a backend or database failure during update and verify “Password could not be updated. Please try again.” and unchanged password. (AT-UC05-05)
