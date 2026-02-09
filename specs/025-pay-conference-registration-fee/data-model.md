# Data Model: Pay Conference Registration Fee

## Entities

### Payment
- **Description**: Record of a payment attempt for a conference registration.
- **Key Fields**:
  - `id` (unique payment identifier)
  - `registration_id`
  - `status` (successful | declined | canceled | failed)
  - `amount`
  - `currency` (optional if single currency)
  - `processed_at` (timestamp)

### RegistrationStatus
- **Description**: Indicates whether a registration is paid/confirmed or pending/unpaid.
- **Key Fields**:
  - `registration_id`
  - `status` (pending_unpaid | paid_confirmed)
  - `updated_at` (timestamp)

### PaymentDetails
- **Description**: Amount due and fee details shown prior to payment submission.
- **Key Fields**:
  - `registration_id`
  - `amount_due`
  - `fee_breakdown` (optional)

## Validation Rules

- Payment can only be initiated for `RegistrationStatus = pending_unpaid`.
- Successful gateway confirmation requires updating status to `paid_confirmed`.
- If recording payment fails, status remains `pending_unpaid`.

## State Transitions

- `pending_unpaid` → `paid_confirmed` on successful payment recording.
- `pending_unpaid` remains if payment is declined, canceled, unavailable, or recording fails.
