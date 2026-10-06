---
name: verify-artifacts-and-constraints
description: Use after making changes or writing output files, before declaring any task complete.
---
- Confirm every required file exists at the exact expected path.
- Parse JSON and CSV outputs and check required keys, headers, field types, units, and formats.
- Verify money is integer cents, timestamps are UTC in the stated format, and categorical values use canonical spelling.
- Check count and ordering rules: distinct rows, duplicates included, repeat counts, sorted entries.
- Confirm original inputs and existing test files were not modified; only allowed new files were added.
- Run the full test suite plus required regression tests; fix failures and rerun.
- Re-read the task rules one final time and mark each one satisfied or fixed.
