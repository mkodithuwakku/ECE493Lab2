# Quickstart: Log In to the System (UC-04)

**Date**: 2026-02-08

## Purpose

Validate the UC-04 login flow for registered users.

## Steps

1. Start the existing CMS application using the project’s standard run steps.
2. Open a web browser and navigate to the CMS login page.
3. Submit valid username or email plus password for an active account and confirm
   redirect to the personalized homepage with no error message. (AT-UC04-01)
4. Submit the form with missing username/email or missing password and verify the
   required-fields message and no authentication. (AT-UC04-02)
5. Submit incorrect credentials and verify the authentication failure message
   includes remaining attempts count and denies login. (AT-UC04-03)
6. Trigger five failed attempts within 15 minutes and confirm the account is
   locked; verify login is blocked and an account inactive message appears.
   (AT-UC04-04)
7. Wait 15 minutes and verify the account auto-unlocks, allowing login with
   valid credentials. (Clarification)
8. Simulate authentication service or database outage and confirm the temporary
   system issue message and no login. (AT-UC04-05)
9. Simulate a critical authentication failure and confirm the "cannot be
   completed" message, no session creation, and no redirect. (AT-UC04-06)
