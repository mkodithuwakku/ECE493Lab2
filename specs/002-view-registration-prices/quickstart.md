# Quickstart: View Conference Registration Prices (UC-02)

**Date**: 2026-02-08

## Purpose

Validate the UC-02 pricing view behavior for guests.

## Steps

1. Start the existing CMS application using the project’s standard run steps.
2. Open a web browser and navigate to the CMS website URL.
3. Select the option/link to view conference registration prices.
4. Verify the pricing page/section displays complete prices by attendance type
   when data is available. (AT-UC02-01)
5. Validate the alternate/error states by preparing the system state and
   reloading the pricing view:
   - Show “registration prices not currently available” when no pricing data
     exists. (AT-UC02-02)
   - Show a temporary system issue message when retrieval fails. (AT-UC02-03)
   - Show available prices with a warning about incomplete details when pricing
     data is partial. (AT-UC02-04)
