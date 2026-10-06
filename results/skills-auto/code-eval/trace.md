### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Assistant
I'll start by reading the skill files that apply to this task.

### Tool call: read_file
{"file_path": "/skills/code-change-hygiene/SKILL.md", "limit": 1000}

### Tool call: read_file
{"file_path": "/skills/house-rules-first/SKILL.md", "limit": 1000}

### Tool result
@@ lines 1-13 of 13 @@
---
name: code-change-hygiene
description: Use when fixing bugs or adding behavior to a code package with house test/changelog conventions.
---
- Never modify existing test files; treat them as read-only specifications.
- If tests are needed, add new test files in the required location rather than editing originals.
- Add one regression test per bug fixed in the required regression-test file, and make it pass.
- Add type annotations to every public function parameter and return value.
- Add a changelog bullet for each fix under the required heading and in the required format.
- Run the full test suite plus an import/compile check before finishing.
- Keep edits scoped to the package and functions needed; avoid unrelated refactors.
- Verify no original test file changed and no required artifact is missing.
- Do not stop after tests pass if the house rules also require annotations, regression tests, or changelog entries.

### Tool result
@@ lines 1-15 of 15 @@
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

### Tool call: read_file
{"file_path": "/skills/structured-output-validation/SKILL.md", "limit": 1000}

### Tool call: read_file
{"file_path": "/skills/work-from-given-spec/SKILL.md", "limit": 1000}

### Tool result
@@ lines 1-15 of 15 @@
---
name: structured-output-validation
description: Use when producing structured data/log outputs that must match a specified schema, units, or file layout.
---
- Enumerate every required output file and every required field before parsing input.
- Parse and normalize inputs once, then reuse the same cleaned data for all answers and outputs.
- Write final artifacts to the expected workspace location, not only to scratch directories.
- Validate by loading each output with the same parser a grader would use.
- Check existence, schema, field types, units, counts, distinctness, sorting, and canonical spellings.
- Convert all timestamps to UTC and emit them in the required string format.
- Emit money values in the required unit, such as integer cents, consistently in every file.
- Include the required metadata/provenance block exactly; omit extra fields if they violate the schema.
- Reconcile summary answers with the detailed output rows so they cannot contradict each other.
- Before finishing, run an independent validation script over the written files.
- Do not treat a chat summary as a deliverable; the files are the deliverable.

### Tool result
@@ lines 1-11 of 11 @@
---
name: work-from-given-spec
description: Use when a task seems to require hidden conventions or when you are tempted to search the environment for rules.
---
- Treat the task statement, visible files, and stated house rules as the complete specification.
- Do not grep the whole filesystem, web-search, or probe unrelated paths for hidden conventions.
- Do not wait for a conventions file, review-bot rule, or external authority that is not provided.
- If a detail is missing, pick the most standard, defensible interpretation and document it in the output.
- Produce a best-effort required artifact early, then refine it; do not let exploration block output.
- Timebox any environment investigation to a few minutes; if it fails, stop and implement from requirements.
- Prefer exact arithmetic and deterministic parsing over guessing or rounding shortcuts.

### Tool call: ls
{"path": "/workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool call: ls
{"path": "/workspace/bookings"}

### Tool call: ls
{"path": "/workspace/tests"}

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py']

### Tool result
['/workspace/tests/__pycache__/', '/workspace/tests/test_bookings.py']

### Tool call: read_file
{"file_path": "/workspace/README.md", "limit": 200}

### Tool call: read_file
{"file_path": "/workspace/CHANGELOG.md", "limit": 200}

### Tool result
@@ lines 1-5 of 5 @@
# bookings

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 1.4.2
- initial import

### Tool call: read_file
{"file_path": "/workspace/bookings/__init__.py", "limit": 200}

### Tool call: read_file
{"file_path": "/workspace/bookings/billing.py", "limit": 400}

### Tool result
@@ lines 1-1 of 1 @@
__version__ = "1.4.2"

### Tool result
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)

### Tool call: read_file
{"file_path": "/workspace/bookings/calendar_export.py", "limit": 400}

### Tool call: read_file
{"file_path": "/workspace/bookings/schedule.py", "limit": 400}

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

### Tool result
@@ lines 1-17 of 17 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    slots.append(slot)
    return slots

### Tool call: read_file
{"file_path": "/workspace/bookings/timeutil.py", "limit": 400}

### Tool call: read_file
{"file_path": "/workspace/tests/test_bookings.py", "limit": 400}

### Tool result
@@ lines 1-19 of 19 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
    if not m:
        raise ValueError(f"bad duration: {text!r}")
    return int(m.group(1)) * 60 + int(m.group(2))

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -30"}

### Tool result

    def parse_duration(text):
        """Convert a duration string to whole minutes (int).
    
        Supported formats:
          "1h30m" -> 90
          "2h"    -> 120
          "45m"   -> 45
          "1:30"  -> 90
          "45"    -> 45    # a bare number means minutes
        Surrounding whitespace is ignored.
        """
        m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
        if not m:
>           raise ValueError(f"bad duration: {text!r}")
E           ValueError: bad duration: '2h'

bookings/timeutil.py:18: ValueError
________________________ test_billable_blocks_rounds_up ________________________

    def test_billable_blocks_rounds_up():
>       assert billable_blocks(20) == 2
E       assert 1 == 2
E        +  where 1 = billable_blocks(20)

tests/test_bookings.py:10: AssertionError
=========================== short test summary info ============================
FAILED tests/test_bookings.py::test_total_minutes_mixed_formats - ValueError:...
FAILED tests/test_bookings.py::test_billable_blocks_rounds_up - assert 1 == 2
2 failed, 1 passed in 0.08s

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && ls -la && ls -la tests bookings && ls -la .. 2>/dev/null | head -30"}

### Tool result
total 28
drwxrwxrwx 5 root   root    4096 Oct  6 04:53 .
drwxrwxrwx 4 root   root    4096 Oct  6 04:53 ..
drwxrwxrwx 3 nobody nogroup 4096 Oct  6 04:53 .pytest_cache
-rw-rw-rw- 1 root   root      54 Oct  6 04:04 CHANGELOG.md
-rw-rw-rw- 1 root   root     118 Oct  6 04:04 README.md
drwxrwxrwx 3 root   root    4096 Oct  6 04:04 bookings
drwxrwxrwx 3 root   root    4096 Oct  6 04:04 tests
bookings:
total 32
drwxrwxrwx 3 root root 4096 Oct  6 04:04 .
drwxrwxrwx 5 root root 4096 Oct  6 04:53 ..
-rw-rw-rw- 1 root root   22 Oct  6 04:04 __init__.py
drwxrwxrwx 2 root root 4096 Oct  6 04:04 __pycache__
-rw-rw-rw- 1 root root  333 Oct  6 04:04 billing.py
-rw-rw-rw- 1 root root  211 Oct  6 04:04 calendar_export.py
-rw-rw-rw- 1 root root  467 Oct  6 04:04 schedule.py
-rw-rw-rw- 1 root root  513 Oct  6 04:04 timeutil.py

tests:
total 16
drwxrwxrwx 3 root root 4096 Oct  6 04:04 .
drwxrwxrwx 5 root root 4096 Oct  6 04:53 ..
drwxrwxrwx 2 root root 4096 Oct  6 04:04 __pycache__
-rw-rw-rw- 1 root root  371 Oct  6 04:04 test_bookings.py
total 16
drwxrwxrwx 4 root root 4096 Oct  6 04:53 .
drwxrwxrwt 1 root root 4096 Oct  6 04:53 ..
drwxr-xr-x 6 root root 4096 Oct  6 04:53 skills
drwxrwxrwx 5 root root 4096 Oct  6 04:53 workspace

[Command succeeded with exit code 0]

### Assistant
No hidden conventions; visible tests + docstrings are the spec. Let me check the Python version and environment.

### Tool call: execute
{"command": "cd workspace && python --version && python -m pytest --version && ls .pytest_cache"}

### Tool result
Python 3.12.15
pytest 9.1.1
CACHEDIR.TAG
README.md
v

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && cat .pytest_cache/v/cache/nodeids 2>/dev/null; echo \"---\"; cat .pytest_cache/v/cache/lastfailed 2>/dev/null"}

### Tool result
[
  "tests/test_bookings.py::test_add_slot_single_call",
  "tests/test_bookings.py::test_billable_blocks_rounds_up",
  "tests/test_bookings.py::test_total_minutes_mixed_formats"
]---
{
  "tests/test_bookings.py::test_total_minutes_mixed_formats": true,
  "tests/test_bookings.py::test_billable_blocks_rounds_up": true
}
[Command succeeded with exit code 0]

### Assistant
Now I understand the bugs. Let me fix the source modules.

### Tool call: write_file
{"file_path": "/workspace/bookings/timeutil.py", "content": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\n\n# \"1h30m\" / \"90m\" style units, with each unit optional as a whole.\n_HOURS_MINUTES_RE = re.compile(r\"(\\d+)h(\\d+)m\")\n_HOURS_RE = re.compile(r\"(\\d+)h\")\n_MINUTES_RE = re.compile(r\"(\\d+)m\")\n# Clock style, e.g. \"1:30\" (minutes are 0-59).\n_CLOCK_RE = re.compile(r\"(\\d+):([0-5]?\\d)\")\n# A bare number is minutes.\n_BARE_RE = re.compile(r\"(\\d+)\")\n\n\ndef parse_duration(text: str) -> int:\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    if not isinstance(text, str):\n        raise ValueError(f\"bad duration: {text!r}\")\n    cleaned = text.strip()\n    for pattern in (_HOURS_MINUTES_RE, _HOURS_RE, _MINUTES_RE, _CLOCK_RE, _BARE_RE):\n        m = pattern.fullmatch(cleaned)\n        if not m:\n            continue\n        if pattern is _HOURS_MINUTES_RE:\n            return int(m.group(1)) * 60 + int(m.group(2))\n        if pattern is _HOURS_RE:\n            return int(m.group(1)) * 60\n        if pattern is _MINUTES_RE:\n            return int(m.group(1))\n        if pattern is _CLOCK_RE:\n            return int(m.group(1)) * 60 + int(m.group(2))\n        return int(m.group(1))\n    raise ValueErr

### Tool call: write_file
{"file_path": "/workspace/bookings/billing.py", "content": "\"\"\"Billing rules.\"\"\"\n\n\ndef billable_blocks(minutes: int, block: int = 15) -> int:\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    if minutes < 0:\n        raise ValueError(f\"minutes must be >= 0, got {minutes!r}\")\n    if block <= 0:\n        raise ValueError(f\"block must be > 0, got {block!r}\")\n    # Exact integer ceiling of minutes / block.\n    return (minutes + block - 1) // block\n"}

### Tool result
Updated file /workspace/bookings/timeutil.py

### Tool result
Updated file /workspace/bookings/billing.py

### Tool call: write_file
{"content": "\"\"\"Schedule helpers.\"\"\"\nfrom typing import Hashable, Iterable\n\nfrom .timeutil import parse_duration\n\n\ndef total_minutes(durations: Iterable[str]) -> int:\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(d) for d in durations)\n\n\ndef add_slot(slot: Hashable, slots: Iterable[Hashable] = ()) -> list:\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    return list(slots) + [slot]\n", "file_path": "/workspace/bookings/schedule.py"}

### Tool call: write_file
{"content": "\"\"\"Calendar export.\"\"\"\nfrom .timeutil import parse_duration\n\n\ndef slot_end(start_minute: int, duration_text: str) -> int:\n    \"\"\"Minute of the day at which a slot ends.\"\"\"\n    return start_minute + parse_duration(duration_text)\n", "file_path": "/workspace/bookings/calendar_export.py"}

### Tool result
Updated file /workspace/bookings/schedule.py

### Tool result
Updated file /workspace/bookings/calendar_export.py

### Tool call: read_file
{"file_path": "/workspace/bookings/schedule.py"}

### Tool result
@@ lines 1-18 of 18 @@
"""Schedule helpers."""
from typing import Hashable, Iterable

from .timeutil import parse_duration


def total_minutes(durations: Iterable[str]) -> int:
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot: Hashable, slots: Iterable[Hashable] = ()) -> list:
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    return list(slots) + [slot]

### Tool call: edit_file
{"file_path": "/workspace/bookings/schedule.py", "old_string": "from typing import Hashable, Iterable\n\nfrom .timeutil import parse_duration\n\n\ndef total_minutes(durations: Iterable[str]) -> int:\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(d) for d in durations)\n\n\ndef add_slot(slot: Hashable, slots: Iterable[Hashable] = ()) -> list:", "new_string": "from typing import Iterable\n\nfrom .timeutil import parse_duration\n\n\ndef total_minutes(durations: Iterable[str]) -> int:\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(d) for d in durations)\n\n\ndef add_slot(slot: object, slots: Iterable[object] = ()) -> list[object]:"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/schedule.py'

### Assistant
Now run the suite and an independent check of the docstring spec.

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -10"}

### Tool result
...                                                                      [100%]
3 passed in 0.02s

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && python - <<'PY'\nfrom bookings.timeutil import parse_duration\nfrom bookings.billing import billable_blocks\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.calendar_export import slot_end\n\n# parse_duration docstring spec\ncases = {(\"1h30m\",90),(\"2h\",120),(\"45m\",45),(\"1:30\",90),(\"45\",45),\n         (\" 1h30m \",90),(\"0m\",0),(\"0\",0),(\"2:05\",125),(\"1h0m\",60)}\nfor text, want in cases:\n    got = parse_duration(text)\n    assert got == want and isinstance(got, int), (text, got, want)\nfor bad in [\"\", \"banana\", \"1h30\", \"h\", \"1:75\", \"1h-2m\", None, 90, \"-5\"]:\n    try:\n        parse_duration(bad)\n    except ValueError:\n        pass\n    else:\n        raise AssertionError(f\"expected ValueError for {bad!r}\")\n\n# billable_blocks spec\nassert billable_blocks(16) == 2\nassert billable_blocks(0) == 0\nassert billable_blocks(15) == 1\nassert billable_blocks(30) == 2\nassert billable_blocks(31) == 3\nassert billable_blocks(45) == 3\nassert billable_blocks(20) == 2\nassert billable_blocks(90, 60) == 2\nassert billable_blocks(61, 60) == 2\nfor bad in (-1, -15):\n    try: billable_blocks(bad)\n    except ValueError: pass\n    else: raise AssertionError(\"expected ValueError\")\n\n# add_slot no shared state / new list\nassert add_slot(\"a\") == [\"a\"]\nassert add_slot(\"b\") == [\"b\"]\nassert add_slot(\"b\", [\"a\"]) == [\"a\", \"b\"]\nbase = [\"x\"]\nout = add_slot(\"y\", base)\nassert out == [\"x\", 

### Tool result
all spec checks passed

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && python -m compileall -q bookings && python -c \"import bookings.billing, bookings.timeutil, bookings.schedule, bookings.calendar_export; print('import ok')\""}

### Tool result
import ok

[Command succeeded with exit code 0]

### Assistant
Now the house rules require regression tests and a changelog entry. Let me check whether any location is hinted at.

### Tool call: grep
{"pattern": "regress", "path": "/workspace"}

### Tool result
No matches found

### Tool call: write_file
{"content": "\"\"\"Regression tests for fixed bugs in the `bookings` package.\"\"\"\nimport pytest\n\nfrom bookings.billing import billable_blocks\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.timeutil import parse_duration\n\n\ndef test_parse_duration_accepts_all_documented_formats():\n    assert parse_duration(\"1h30m\") == 90\n    assert parse_duration(\"2h\") == 120\n    assert parse_duration(\"45m\") == 45\n    assert parse_duration(\"1:30\") == 90\n    assert parse_duration(\"45\") == 45\n    assert parse_duration(\" 2h \") == 120\n\n\ndef test_parse_duration_rejects_malformed_input():\n    with pytest.raises(ValueError):\n        parse_duration(\"banana\")\n    with pytest.raises(ValueError):\n        parse_duration(\"1h30\")\n\n\ndef test_billable_blocks_rounds_partial_block_up():\n    assert billable_blocks(16) == 2\n    assert billable_blocks(15) == 1\n    assert billable_blocks(0) == 0\n\n\ndef test_billable_blocks_rejects_negative_minutes():\n    with pytest.raises(ValueError):\n        billable_blocks(-1)\n\n\ndef test_add_slot_calls_do_not_share_state():\n    assert add_slot(\"a\") == [\"a\"]\n    assert add_slot(\"b\") == [\"b\"]\n\n\ndef test_add_slot_returns_new_list_and_keeps_original():\n    original = [\"x\"]\n    result = add_slot(\"y\", original)\n    assert result == [\"x\", \"y\"]\n    assert original == [\"x\"]\n    assert result is not original\n\n\ndef test_total_minutes_supports_mixed_duration_formats():\n    assert total_mi

### Tool result
Updated file /workspace/tests/test_regressions.py

### Tool call: edit_file
{"file_path": "/workspace/CHANGELOG.md", "old_string": "## Unreleased\n\n## 1.4.2", "new_string": "## Unreleased\n- Fix `parse_duration`: support `\"2h\"`, `\"45m\"`, `\"1:30\"` and bare-minute forms, not only `\"1h30m\"`.\n- Fix `billable_blocks`: round a partial block up (ceiling) instead of to nearest, and raise `ValueError` for negative minutes.\n\n## 1.4.2"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/CHANGELOG.md'

### Tool call: edit_file
{"file_path": "/workspace/CHANGELOG.md", "new_string": "- Fix `billable_blocks`: round a partial block up (ceiling) instead of to nearest, and raise `ValueError` for negative minutes.\n- Fix `add_slot`: return a new list per call instead of mutating a shared default argument.", "old_string": "- Fix `billable_blocks`: round a partial block up (ceiling) instead of to nearest, and raise `ValueError` for negative minutes."}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/CHANGELOG.md'

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -5 && echo \"--- compileall ---\" && python -m compileall -q bookings && echo ok"}

### Tool result
..........                                                               [100%]
10 passed in 0.03s
--- compileall ---
ok

[Command succeeded with exit code 0]

### Tool call: read_file
{"file_path": "/workspace/CHANGELOG.md"}

### Tool call: read_file
{"file_path": "/workspace/tests/test_bookings.py"}

### Tool result
@@ lines 1-9 of 9 @@
# Changelog

## Unreleased
- Fix `parse_duration`: support `"2h"`, `"45m"`, `"1:30"` and bare-minute forms, not only `"1h30m"`.
- Fix `billable_blocks`: round a partial block up (ceiling) instead of to nearest, and raise `ValueError` for negative minutes.
- Fix `add_slot`: return a new list per call instead of mutating a shared default argument.

## 1.4.2
- initial import

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -5 && echo \"=== docstring examples ===\" && python - <<'PY'\nimport inspect\nfrom bookings import billing, schedule, timeutil, calendar_export\n\n# parse_duration docstring examples\nassert timeutil.parse_duration(\"1h30m\") == 90\nassert timeutil.parse_duration(\"2h\") == 120\nassert timeutil.parse_duration(\"45m\") == 45\nassert timeutil.parse_duration(\"1:30\") == 90\nassert timeutil.parse_duration(\"45\") == 45\n# billable_blocks docstring example\nassert billing.billable_blocks(16) == 2\ntry:\n    billing.billable_blocks(-1)\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError\n# add_slot docstring example\nassert schedule.add_slot(\"a\") == [\"a\"]\nassert schedule.add_slot(\"b\") == [\"b\"]\n# calendar_export\nassert calendar_export.slot_end(60, \"2h\") == 180\nprint(\"docstring spec ok\")\n\n# annotations present on public functions\nfor mod in (billing, schedule, timeutil, calendar_export):\n    for name, fn in vars(mod).items():\n        if inspect.isfunction(fn) and fn.__module__ == mod.__name__:\n            hints = fn.__annotations__\n            sig = inspect.signature(fn)\n            assert \"return\" in hints, (mod.__name__, name, \"missing return hint\")\n            for p in sig.parameters:\n                assert p in hints, (mod.__name__, name, p, \"missing param hint\")\nprint(\"annotations ok\")\nPY"}

### Tool result
..........                                                               [100%]
10 passed in 0.03s
=== docstring examples ===
docstring spec ok
annotations ok

[Command succeeded with exit code 0]

### Tool call: read_file
{"file_path": "/workspace/bookings/timeutil.py"}

### Tool call: read_file
{"file_path": "/workspace/bookings/billing.py"}

### Tool result
@@ lines 1-41 of 41 @@
"""Time helpers for the bookings package."""
import re

# "1h30m" / "90m" style units, with each unit optional as a whole.
_HOURS_MINUTES_RE = re.compile(r"(\d+)h(\d+)m")
_HOURS_RE = re.compile(r"(\d+)h")
_MINUTES_RE = re.compile(r"(\d+)m")
# Clock style, e.g. "1:30" (minutes are 0-59).
_CLOCK_RE = re.compile(r"(\d+):([0-5]?\d)")
# A bare number is minutes.
_BARE_RE = re.compile(r"(\d+)")


def parse_duration(text: str) -> int:
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    if not isinstance(text, str):
        raise ValueError(f"bad duration: {text!r}")
    cleaned = text.strip()
    for pattern in (_HOURS_MINUTES_RE, _HOURS_RE, _MINUTES_RE, _CLOCK_RE, _BARE_RE):
        m = pattern.fullmatch(cleaned)
        if not m:
            continue
        if pattern is _HOURS_MINUTES_RE:
            return int(m.group(1)) * 60 + int(m.group(2))
        if pattern is _HOURS_RE:
            return int(m.group(1)) * 60
        if pattern is _MINUTES_RE:
            return int(m.group(1))
        if pattern is _CLOCK_RE:
            return int(m.group(1)) * 60 + int(m.group(2))
        return int(m.group(1))
    raise ValueError(f"bad duration: {text!r}")

### Tool result
@@ lines 1-16 of 16 @@
"""Billing rules."""


def billable_blocks(minutes: int, block: int = 15) -> int:
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    if minutes < 0:
        raise ValueError(f"minutes must be >= 0, got {minutes!r}")
    if block <= 0:
        raise ValueError(f"block must be > 0, got {block!r}")
    # Exact integer ceiling of minutes / block.
    return (minutes + block - 1) // block

### Assistant
Let me simplify `timeutil.py` into a single clean regex for readability.

### Tool call: write_file
{"content": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\n\n# One alternative per documented form: \"1h30m\", \"2h\", \"45m\", \"1:30\", \"45\".\n_DURATION_RE = re.compile(\n    r\"(?P<hours>\\d+)h(?P<minutes>\\d+)m\"\n    r\"|(?P<hours_only>\\d+)h\"\n    r\"|(?P<minutes_only>\\d+)m\"\n    r\"|(?P<clock_hours>\\d+):(?P<clock_minutes>[0-5]?\\d)\"\n    r\"|(?P<bare>\\d+)\"\n)\n\n\ndef parse_duration(text: str) -> int:\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    if not isinstance(text, str):\n        raise ValueError(f\"bad duration: {text!r}\")\n    match = _DURATION_RE.fullmatch(text.strip())\n    if match is None:\n        raise ValueError(f\"bad duration: {text!r}\")\n    if match[\"hours\"] is not None:\n        return int(match[\"hours\"]) * 60 + int(match[\"minutes\"])\n    if match[\"clock_hours\"] is not None:\n        return int(match[\"clock_hours\"]) * 60 + int(match[\"clock_minutes\"])\n    if match[\"hours_only\"] is not None:\n        return int(match[\"hours_only\"]) * 60\n    if match[\"minutes_only\"] is not None:\n        return int(match[\"minutes_only\"])\n    return int(match[\"bare\"])\n", "file_path": "/workspace/bookings/timeutil.py"}

### Tool result
Updated file /workspace/bookings/timeutil.py

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -5 && python - <<'PY'\nfrom bookings.timeutil import parse_duration\ncases = {(\"1h30m\",90),(\"2h\",120),(\"45m\",45),(\"1:30\",90),(\"45\",45),(\" 2h \",120),(\"0m\",0),(\"0\",0),(\"2:05\",125),(\"1h0m\",60),(\"10:00\",600)}\nfor t,w in cases: assert parse_duration(t)==w, (t, parse_duration(t), w)\nfor bad in [\"\",\"banana\",\"1h30\",\"h\",\"1:75\",\"1h-2m\",None,90,\"-5\",\":30\",\"1h30m45\"]:\n    try: parse_duration(bad)\n    except ValueError: pass\n    else: raise AssertionError(bad)\nprint(\"timeutil spec ok\")\nPY"}

### Tool result
..........                                                               [100%]
10 passed in 0.03s
timeutil spec ok

[Command succeeded with exit code 0]