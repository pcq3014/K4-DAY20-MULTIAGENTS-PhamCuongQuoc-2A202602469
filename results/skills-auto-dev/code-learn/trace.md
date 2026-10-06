### Human
The test suite of the `inventory` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Assistant
I'll start by reading the skill files that could apply to this task.

### Tool call: read_file
{"file_path": "/skills/code-change-hygiene/SKILL.md", "limit": 1000}

### Tool call: read_file
{"file_path": "/skills/house-rules-first/SKILL.md", "limit": 1000}

### Tool call: read_file
{"file_path": "/skills/structured-output-validation/SKILL.md", "limit": 1000}

### Tool call: read_file
{"file_path": "/skills/work-from-given-spec/SKILL.md", "limit": 1000}

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

### Tool call: glob
{"pattern": "**/*", "path": "/workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/inventory/', '/workspace/tests/']

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/inventory/__init__.py', '/workspace/inventory/__pycache__/__init__.cpython-311.pyc', '/workspace/inventory/__pycache__/export.cpython-311.pyc', '/workspace/inventory/__pycache__/pricing.cpython-311.pyc', '/workspace/inventory/__pycache__/report.cpython-311.pyc', '/workspace/inventory/export.py', '/workspace/inventory/pricing.py', '/workspace/inventory/report.py', '/workspace/tests/__pycache__/test_report.cpython-311-pytest-9.1.1.pyc', '/workspace/tests/test_report.py']

### Tool call: read_file
{"file_path": "/workspace/README.md"}

### Tool call: read_file
{"file_path": "/workspace/CHANGELOG.md"}

### Tool call: read_file
{"file_path": "/workspace/inventory/__init__.py"}

### Tool call: read_file
{"file_path": "/workspace/inventory/pricing.py"}

### Tool result
@@ lines 1-5 of 5 @@
# inventory

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 0.3.1
- initial import

### Tool result
@@ lines 1-1 @@
System reminder: File exists but has empty contents

### Tool result
@@ lines 1-25 of 25 @@
"""Price utilities for the inventory package."""
from decimal import Decimal


def parse_price(text):
    """Convert a price string to a Decimal.

    Supported formats:
      "$1,299.50" -> Decimal("1299.50")
      "  12 "     -> Decimal("12")
      "1299.5"    -> Decimal("1299.5")
      "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
    """
    cleaned = text.strip().replace("$", "")
    return Decimal(cleaned)


def apply_discount(price, percent):
    """Return `price` after a percentage discount.

    The result is a Decimal rounded to 2 decimal places using the
    commercial rule "round half up" (0.005 -> 0.01).
    """
    discounted = price * (100 - percent) / 100
    return discounted.quantize(Decimal("0.01"))

### Tool call: read_file
{"file_path": "/workspace/inventory/export.py"}

### Tool call: read_file
{"file_path": "/workspace/inventory/report.py"}

### Tool call: read_file
{"file_path": "/workspace/tests/test_report.py"}

### Tool result
@@ lines 1-12 of 12 @@
"""Export helpers."""
from .pricing import parse_price


def to_csv_row(item):
    """Format one item as a CSV row: name,price,qty (price with 2 decimals).

    A name that contains a comma or a double quote is wrapped in double quotes,
    and every double quote inside it is doubled (RFC 4180).
    """
    price = parse_price(item["price"])
    return f'{item["name"]},{price:.2f},{item["qty"]}'

### Tool result
@@ lines 1-25 of 25 @@
"""Inventory reports."""
from decimal import Decimal

from .pricing import apply_discount, parse_price


def total_value(items):
    """Total value of `items` after per-item discounts.

    Each item is a dict: {"name": str, "price": str, "qty": int, "discount": percent (optional)}.
    """
    total = Decimal("0")
    for item in items:
        price = parse_price(item["price"])
        price = apply_discount(price, item.get("discount", 0))
        total += price * item["qty"]
    return total


def low_stock(items, threshold=5):
    """Names of the items whose quantity is strictly below `threshold`.

    The names are sorted alphabetically, ignoring case.
    """
    return [item["name"] for item in items if item["qty"] <= threshold]

### Tool result
@@ lines 1-32 of 32 @@
from decimal import Decimal

from inventory.export import to_csv_row
from inventory.pricing import apply_discount
from inventory.report import low_stock, total_value


def test_total_value_plain():
    items = [{"name": "pen", "price": "$2.50", "qty": 4}]
    assert total_value(items) == Decimal("10.00")


def test_total_value_thousands_separator():
    items = [{"name": "laptop", "price": "$1,299.50", "qty": 2}]
    assert total_value(items) == Decimal("2599.00")


def test_discount_rounding_half_up():
    assert apply_discount(Decimal("10.05"), 10) == Decimal("9.05")


def test_total_value_with_discount():
    items = [{"name": "desk", "price": "100.00", "qty": 1, "discount": 15}]
    assert total_value(items) == Decimal("85.00")


def test_low_stock_basic():
    assert low_stock([{"name": "pen", "qty": 2}, {"name": "ink", "qty": 9}]) == ["pen"]


def test_csv_row_plain_name():
    assert to_csv_row({"name": "pen", "price": "2.5", "qty": 4}) == "pen,2.50,4"

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -40; echo \"---\"; ls -a; echo \"---\"; git log --oneline -20 2>&1 | head -20"}

### Tool result
               ^^^^^^^^^^^^^^^^^^

tests/test_report.py:15: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
inventory/report.py:14: in total_value
    price = parse_price(item["price"])
            ^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

text = '$1,299.50'

    def parse_price(text):
        """Convert a price string to a Decimal.
    
        Supported formats:
          "$1,299.50" -> Decimal("1299.50")
          "  12 "     -> Decimal("12")
          "1299.5"    -> Decimal("1299.5")
          "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
        """
        cleaned = text.strip().replace("$", "")
>       return Decimal(cleaned)
               ^^^^^^^^^^^^^^^^
E       decimal.InvalidOperation: [<class 'decimal.ConversionSyntax'>]

inventory/pricing.py:15: InvalidOperation
________________________ test_discount_rounding_half_up ________________________

    def test_discount_rounding_half_up():
>       assert apply_discount(Decimal("10.05"), 10) == Decimal("9.05")
E       AssertionError: assert Decimal('9.04') == Decimal('9.05')
E        +  where Decimal('9.04') = apply_discount(Decimal('10.05'), 10)
E        +    where Decimal('10.05') = Decimal('10.05')
E        +  and   Decimal('9.05') = Decimal('9.05')

tests/test_report.py:19: AssertionError
=========================== short test summary info ============================
FAILED tests/

### Assistant
Now let me look at the failing points and write the fixes per the docstring specs.

### Tool call: write_file
{"file_path": "/workspace/inventory/pricing.py", "content": "\"\"\"Price utilities for the inventory package.\"\"\"\nfrom decimal import ROUND_HALF_UP, Decimal\n\nTWO_PLACES = Decimal(\"0.01\")\n\n\ndef parse_price(text: str) -> Decimal:\n    \"\"\"Convert a price string to a Decimal.\n\n    Supported formats:\n      \"$1,299.50\" -> Decimal(\"1299.50\")\n      \"  12 \"     -> Decimal(\"12\")\n      \"1299.5\"    -> Decimal(\"1299.5\")\n      \"(12.00)\"   -> Decimal(\"-12.00\")   # accounting style: parentheses mean negative\n    \"\"\"\n    cleaned = text.strip().replace(\"$\", \"\").replace(\",\", \"\")\n    negative = cleaned.startswith(\"(\") and cleaned.endswith(\")\")\n    if negative:\n        cleaned = cleaned[1:-1]\n    value = Decimal(cleaned.strip())\n    return -value if negative else value\n\n\ndef apply_discount(price: Decimal, percent: int) -> Decimal:\n    \"\"\"Return `price` after a percentage discount.\n\n    The result is a Decimal rounded to 2 decimal places using the\n    commercial rule \"round half up\" (0.005 -> 0.01).\n    \"\"\"\n    factor = (Decimal(100) - Decimal(percent)) / Decimal(100)\n    return (price * factor).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)\n"}

### Tool call: write_file
{"file_path": "/workspace/inventory/report.py", "content": "\"\"\"Inventory reports.\"\"\"\nfrom decimal import Decimal\n\nfrom .pricing import apply_discount, parse_price\n\n\ndef total_value(items: list[dict]) -> Decimal:\n    \"\"\"Total value of `items` after per-item discounts.\n\n    Each item is a dict: {\"name\": str, \"price\": str, \"qty\": int, \"discount\": percent (optional)}.\n    \"\"\"\n    total = Decimal(\"0\")\n    for item in items:\n        price = parse_price(item[\"price\"])\n        price = apply_discount(price, item.get(\"discount\", 0))\n        total += price * item[\"qty\"]\n    return total\n\n\ndef low_stock(items: list[dict], threshold: int = 5) -> list[str]:\n    \"\"\"Names of the items whose quantity is strictly below `threshold`.\n\n    The names are sorted alphabetically, ignoring case.\n    \"\"\"\n    names = [item[\"name\"] for item in items if item[\"qty\"] < threshold]\n    return sorted(names, key=str.lower)\n"}

### Tool result
Updated file /workspace/inventory/pricing.py

### Tool result
Updated file /workspace/inventory/report.py

### Tool call: write_file
{"content": "\"\"\"Export helpers.\"\"\"\nfrom .pricing import parse_price\n\n\ndef to_csv_row(item: dict) -> str:\n    \"\"\"Format one item as a CSV row: name,price,qty (price with 2 decimals).\n\n    A name that contains a comma or a double quote is wrapped in double quotes,\n    and every double quote inside it is doubled (RFC 4180).\n    \"\"\"\n    price = parse_price(item[\"price\"])\n    name = item[\"name\"]\n    if \",\" in name or '\"' in name:\n        name = '\"{}\"'.format(name.replace('\"', '\"\"'))\n    return f\"{name},{price:.2f},{item['qty']}\"\n", "file_path": "/workspace/inventory/export.py"}

### Tool result
Updated file /workspace/inventory/export.py

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -20"}

### Tool result
......                                                                   [100%]
6 passed in 0.02s

[Command succeeded with exit code 0]

### Assistant
All visible tests pass. Now let me verify the docstring behaviors beyond the visible tests.

### Tool call: execute
{"command": "cd workspace && python - <<'PY'\nfrom decimal import Decimal\nfrom inventory.pricing import parse_price, apply_discount\nfrom inventory.report import low_stock, total_value\nfrom inventory.export import to_csv_row\n\n# parse_price\nprint(parse_price(\"$1,299.50\"))\nprint(parse_price(\"  12 \"))\nprint(parse_price(\"1299.5\"))\nprint(parse_price(\"(12.00)\"))\nprint(parse_price(\"$1,000,000.00\"))\nprint(parse_price(\"($1,234.56)\"))\n\n# apply_discount\nprint(apply_discount(Decimal(\"10.05\"), 10))\nprint(apply_discount(Decimal(\"100.00\"), 15))\nprint(apply_discount(Decimal(\"0.125\"), 0))\nprint(apply_discount(Decimal(\"2.675\"), 0))\nprint(apply_discount(Decimal(\"10.00\"), 0))\nprint(apply_discount(Decimal(\"9.99\"), 100))\n\n# total_value\nprint(total_value([]))\nprint(total_value([{\"name\":\"pen\",\"price\":\"$2.50\",\"qty\":4}]))\n\n# low_stock\nprint(low_stock([{\"name\":\"Ink\",\"qty\":1},{\"name\":\"apple\",\"qty\":2},{\"name\":\"Zebra\",\"qty\":0}]))\nprint(low_stock([{\"name\":\"a\",\"qty\":5}]))\nprint(low_stock([{\"name\":\"a\",\"qty\":5}], threshold=5))\nprint(low_stock([{\"name\":\"a\",\"qty\":6}], threshold=5))\n\n# to_csv_row\nprint(repr(to_csv_row({\"name\":\"pen\",\"price\":\"2.5\",\"qty\":4})))\nprint(repr(to_csv_row({\"name\":'a,b',\"price\":\"2.5\",\"qty\":4})))\nprint(repr(to_csv_row({\"name\":'a\"b',\"price\":\"2.5\",\"qty\":4})))\nprint(repr(to_csv_row({\"name\":'a\"b,c',\"price\":\"2.5\",\"qty\":4})))\nprint(repr(to_csv_row({\"name\":

### Tool result
1299.50
12
1299.5
-12.00
1000000.00
-1234.56
9.05
85.00
0.13
2.68
10.00
0.00
0
10.00
['apple', 'Ink', 'Zebra']
[]
[]
[]
'pen,2.50,4'
'"a,b",2.50,4'
'"a""b",2.50,4'
'"a""b,c",2.50,4'
'plain,-12.00,4'

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && ls -a tests/ . 2>&1; echo \"---\"; find . -maxdepth 2 -name \"*.md\" -o -maxdepth 2 -name \"*.txt\" -o -maxdepth 2 -name \"*.toml\" -o -maxdepth 2 -name \"*.cfg\" -o -maxdepth 2 -name \"*.ini\" | sort"}

### Tool result
.:
.
..
.pytest_cache
CHANGELOG.md
README.md
inventory
tests

tests/:
.
..
__pycache__
test_report.py
---
./.pytest_cache/README.md
./CHANGELOG.md
./README.md

[Command succeeded with exit code 0]

### Assistant
No conventions file exists beyond the skills; I'll follow the skill's stated house conventions (annotations done, add regression tests + changelog entries).

### Tool call: write_file
{"content": "\"\"\"Regression tests for the bugs fixed in the inventory package.\"\"\"\nfrom decimal import Decimal\n\nfrom inventory.export import to_csv_row\nfrom inventory.pricing import apply_discount, parse_price\nfrom inventory.report import low_stock\n\n\ndef test_parse_price_strips_thousands_separator():\n    assert parse_price(\"$1,299.50\") == Decimal(\"1299.50\")\n\n\ndef test_parse_price_accounting_negative():\n    assert parse_price(\"(12.00)\") == Decimal(\"-12.00\")\n    assert parse_price(\"($1,234.56)\") == Decimal(\"-1234.56\")\n\n\ndef test_apply_discount_rounds_half_up():\n    assert apply_discount(Decimal(\"10.05\"), 10) == Decimal(\"9.05\")\n    assert apply_discount(Decimal(\"2.675\"), 0) == Decimal(\"2.68\")\n\n\ndef test_low_stock_is_strictly_below_threshold():\n    assert low_stock([{\"name\": \"a\", \"qty\": 5}]) == []\n\n\ndef test_low_stock_sorted_ignoring_case():\n    items = [{\"name\": \"Zebra\", \"qty\": 0}, {\"name\": \"apple\", \"qty\": 1}, {\"name\": \"Ink\", \"qty\": 2}]\n    assert low_stock(items) == [\"apple\", \"Ink\", \"Zebra\"]\n\n\ndef test_csv_row_quotes_name_with_comma_or_quote():\n    assert to_csv_row({\"name\": \"a,b\", \"price\": \"2.5\", \"qty\": 4}) == '\"a,b\",2.50,4'\n    assert to_csv_row({\"name\": 'a\"b', \"price\": \"2.5\", \"qty\": 4}) == '\"a\"\"b\",2.50,4'\n", "file_path": "/workspace/tests/test_regression.py"}

### Tool result
Updated file /workspace/tests/test_regression.py

### Tool call: edit_file
{"file_path": "/workspace/CHANGELOG.md", "old_string": "## Unreleased\n", "new_string": "## Unreleased\n- Fix `parse_price` to strip thousands separators and to handle accounting-style parentheses as negative amounts.\n- Fix `apply_discount` to round half up (commercial rounding) instead of banker's rounding.\n- Fix `low_stock` to select quantities strictly below the threshold and sort names alphabetically ignoring case.\n- Fix `to_csv_row` to quote names containing a comma or double quote per RFC 4180.\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/CHANGELOG.md'

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -10; echo \"--- compile ---\"; python -m compileall -q inventory tests && echo \"compile ok\"; echo \"--- import ---\"; python -c \"import inventory.pricing, inventory.report, inventory.export; print('import ok')\""}

### Tool result
............                                                             [100%]
12 passed in 0.04s
--- compile ---
compile ok
--- import ---
import ok

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && python -m pyflakes inventory tests 2>&1 | head; echo \"exit=$?\"; echo \"--- final files ---\"; find . -name \"*.py\" -not -path \"*/__pycache__/*\" -not -path \"./.pytest_cache/*\" | sort"}

### Tool result
/usr/local/bin/python: No module named pyflakes
exit=0
--- final files ---
./inventory/__init__.py
./inventory/export.py
./inventory/pricing.py
./inventory/report.py
./tests/test_regression.py
./tests/test_report.py

[Command succeeded with exit code 0]

### Tool call: read_file
{"file_path": "/workspace/inventory/pricing.py"}

### Tool call: read_file
{"file_path": "/workspace/inventory/report.py"}

### Tool call: read_file
{"file_path": "/workspace/inventory/export.py"}

### Tool result
@@ lines 1-31 of 31 @@
"""Price utilities for the inventory package."""
from decimal import ROUND_HALF_UP, Decimal

TWO_PLACES = Decimal("0.01")


def parse_price(text: str) -> Decimal:
    """Convert a price string to a Decimal.

    Supported formats:
      "$1,299.50" -> Decimal("1299.50")
      "  12 "     -> Decimal("12")
      "1299.5"    -> Decimal("1299.5")
      "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
    """
    cleaned = text.strip().replace("$", "").replace(",", "")
    negative = cleaned.startswith("(") and cleaned.endswith(")")
    if negative:
        cleaned = cleaned[1:-1]
    value = Decimal(cleaned.strip())
    return -value if negative else value


def apply_discount(price: Decimal, percent: int) -> Decimal:
    """Return `price` after a percentage discount.

    The result is a Decimal rounded to 2 decimal places using the
    commercial rule "round half up" (0.005 -> 0.01).
    """
    factor = (Decimal(100) - Decimal(percent)) / Decimal(100)
    return (price * factor).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)

### Tool result
@@ lines 1-26 of 26 @@
"""Inventory reports."""
from decimal import Decimal

from .pricing import apply_discount, parse_price


def total_value(items: list[dict]) -> Decimal:
    """Total value of `items` after per-item discounts.

    Each item is a dict: {"name": str, "price": str, "qty": int, "discount": percent (optional)}.
    """
    total = Decimal("0")
    for item in items:
        price = parse_price(item["price"])
        price = apply_discount(price, item.get("discount", 0))
        total += price * item["qty"]
    return total


def low_stock(items: list[dict], threshold: int = 5) -> list[str]:
    """Names of the items whose quantity is strictly below `threshold`.

    The names are sorted alphabetically, ignoring case.
    """
    names = [item["name"] for item in items if item["qty"] < threshold]
    return sorted(names, key=str.lower)

### Tool result
@@ lines 1-15 of 15 @@
"""Export helpers."""
from .pricing import parse_price


def to_csv_row(item: dict) -> str:
    """Format one item as a CSV row: name,price,qty (price with 2 decimals).

    A name that contains a comma or a double quote is wrapped in double quotes,
    and every double quote inside it is doubled (RFC 4180).
    """
    price = parse_price(item["price"])
    name = item["name"]
    if "," in name or '"' in name:
        name = '"{}"'.format(name.replace('"', '""'))
    return f"{name},{price:.2f},{item['qty']}"

### Tool call: edit_file
{"file_path": "/workspace/inventory/pricing.py", "old_string": "def apply_discount(price: Decimal, percent: int) -> Decimal:", "new_string": "def apply_discount(price: Decimal, percent: \"int | Decimal\") -> Decimal:"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/pricing.py'

### Tool call: edit_file
{"file_path": "/workspace/inventory/pricing.py", "new_string": "def apply_discount(price: Decimal, percent: int) -> Decimal:", "old_string": "def apply_discount(price: Decimal, percent: \"int | Decimal\") -> Decimal:"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/pricing.py'

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -5"}

### Tool result
............                                                             [100%]
12 passed in 0.03s

[Command succeeded with exit code 0]

### Assistant
All 12 tests pass (6 original + 6 new regression tests), and compile/import checks are clean.

## Summary of changes

**`inventory/pricing.py`**
- `parse_price`: now strips thousands separators (`"$1,299.50"` → `1299.50`) and supports accounting-style parentheses for negatives (`"(12.00)"` → `-12.00`), as the docstring specifies.
- `apply_discount`: now rounds with `ROUND_HALF_UP` to 2 decimals instead of the default banker's rounding (`ROUND_HALF_EVEN`), so `10.05 - 10% → 9.05` and `2.675 → 2.68`.
- Added return/parameter type annotations.

**`inventory/report.py`**
- `low_stock`: used `<=` (included the threshold itself); changed to strictly `<` and sorts names alphabetically ignoring case via `key=str.lower`, matching the docstring.
- Added type annotations.

**`inventory/export.py`**
- `to_csv_row`: implemented the documented RFC 4180 quoting — names containing a comma or double quote are wrapped in quotes with internal quotes doubled.
- Added type annotations.

**`tests/test_regression.py`** (new file; existing `tests/test_report.py` untouched)
- One regression test per fixed bug: thousands separator, accounting negatives, half-up rounding, strict-below threshold, case-insensitive sort, and CSV quoting.

**`CHANGELOG.md`**
- Added a bullet under `## Unreleased` for each of the four fixes.

House-rule checklist: existing tests unmodified ✔, regression tests added in `tests/` ✔, public functions annotated ✔, changelog bullets added under the required heading ✔, full suite 