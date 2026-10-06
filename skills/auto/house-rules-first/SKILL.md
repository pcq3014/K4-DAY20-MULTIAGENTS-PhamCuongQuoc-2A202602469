---
name: house-rules-first
description: Use when a task or feedback lists RULE/house conventions or explicit acceptance criteria.
---
- Treat every RULE/acceptance line as a hard requirement, not a hint.
- Read all of them before writing code or data.
- Do not search the filesystem, network, or hidden files for secret conventions; the stated rules are sufficient.
- Turn each rule into a checklist item: required file, field, unit, format, ordering, or behavior.
- Follow exact names, casing, units, order, and schemas even when they differ from your preferred convention.
- If a rule names a required artifact or format, produce that artifact explicitly.
- If a rule requires metadata, include the exact metadata object/fields specified.
- If a rule requires money as integer cents, never emit floats or formatted currency strings.
- If a rule requires clean/structured output, write it as a separate file in the workspace.
- Before finishing, re-read every RULE line and verify it against the produced work.
- Report which rules were satisfied; do not leave them implicit.
