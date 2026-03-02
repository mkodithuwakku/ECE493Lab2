# Quickstart: View Public Conference Information (UC-01)

**Date**: 2026-02-08

## Purpose

Validate the UC-01 public homepage behavior for guests.

## Steps

1. Start the existing CMS application using the project’s standard run steps.
2. Open a web browser and navigate to the CMS homepage URL.
3. Verify the homepage displays public announcements and conference information
   when data is available (AT-UC01-01).
4. Validate the alternate/error states by preparing the system state and
   reloading the homepage:
   - “The website is temporarily unavailable.” when the site is unreachable
     (AT-UC01-02).
   - “No public conference information is currently available.” when no public
     information exists (AT-UC01-03).
   - “Some information could not be loaded.” when partial public information is
     loaded (AT-UC01-04).
   - “Public conference information cannot be retrieved at this time.” when
     the homepage is reachable but content load fails (AT-UC01-05).
