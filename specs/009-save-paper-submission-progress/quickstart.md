# Quickstart: UC-09 Save Paper Submission Progress

## Goal
Validate the save-draft flow against AT-UC09-01 through AT-UC09-04.

## Prerequisites
- CMS is running and accessible
- Author account exists and is authenticated
- Author has started a paper submission

## Scenarios

### AT-UC09-01 Save Submission Progress Successfully
1. Enter valid submission data including minimum fields (title, abstract, one author).
2. Select save.
3. Expect validation success, draft saved, confirmation message.

### AT-UC09-02 Invalid Submission Data Prevents Save
1. Enter invalid submission data.
2. Select save.
3. Expect validation error messages and no draft saved.

### AT-UC09-03 Required Minimum Draft Information Missing
1. Leave out minimum draft fields.
2. Select save.
3. Expect warning with save/cancel choice.
4. Choose save anyway and expect draft stored as incomplete.

### AT-UC09-04 System Fails to Store Draft
1. Simulate storage failure while saving.
2. Expect save failure message and no draft stored.
