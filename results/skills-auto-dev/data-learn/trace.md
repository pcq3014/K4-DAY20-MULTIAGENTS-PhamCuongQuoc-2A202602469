### Human
Analyse the sales data in `workspace/sales.csv` (see `workspace/README.md` for the column descriptions).

Write a file `workspace/answer.json` with exactly these keys, plus whatever the Acme reporting conventions require:

- `north_q1_revenue` (number): sum of `amount` of the orders in region North placed in the first quarter of 2024, that is from 2024-01-01 00:00 UTC up to and including 2024-03-31 23:59:59 UTC.
- `north_q1_orders` (integer): number of distinct orders counted in `north_q1_revenue`.
- `top_region` (string): the region (North, South, East or West) with the highest total `amount` over the whole file.
- `missing_amount_orders` (integer): number of distinct orders whose amount is missing.
- `duplicate_rows_removed` (integer): number of duplicate rows you removed.

Orders with a missing amount must not be added to any revenue.
Your output files are also checked by Acme's review bot against the Acme reporting conventions.
When you are done, reply with a short summary of how you cleaned the data.


### Assistant
I'll start by reading the skill files that could apply to this task.

### Tool call: read_file
{"file_path": "/skills/house-rules-first/SKILL.md", "limit": 1000}

### Tool call: read_file
{"file_path": "/skills/structured-output-validation/SKILL.md", "limit": 1000}

### Tool call: read_file
{"file_path": "/skills/work-from-given-spec/SKILL.md", "limit": 1000}

### Tool call: read_file
{"file_path": "/skills/code-change-hygiene/SKILL.md", "limit": 1000}

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

### Tool call: ls
{"path": "/workspace"}

### Tool call: read_file
{"file_path": "/workspace/README.md", "limit": 200}

### Tool result
['/workspace/README.md', '/workspace/sales.csv']

### Tool result
@@ lines 1-8 of 8 @@
# sales.csv - data dictionary

| column | description |
|---|---|
| order_id | order identifier. The same order may appear more than once because of re-exports; keep one row per order_id. |
| date | when the order was placed. Three formats occur: `YYYY-MM-DD` and `DD/MM/YYYY` (a date only, meaning 00:00 UTC of that day) and an ISO-8601 timestamp with a UTC offset such as `2024-02-03T21:30:00-05:00`. |
| region | sales region (North, South, East, West). Spelling and capitalisation are not consistent. |
| amount | order amount in USD. The value `-999` means the amount is unknown (missing). |

### Tool call: read_file
{"file_path": "/workspace/sales.csv", "limit": 200}

### Tool result
@@ lines 1-102 of 102 @@
order_id,date,region,amount
S-1090,2024-03-05T16:15:00+00:00,west,591.39
S-1022,09/02/2024,NORTH,379.22
S-1005,2024-05-26T12:30:00-05:00,West ,513.84
S-1020,2024-02-23, North,-999
S-1014,10/06/2024,west,335.88
S-1010,16/04/2024, East,145.97
S-1002,20/06/2024, South,-999
S-1076,2024-03-20, South,346.27
S-1032,2024-01-07T23:15:00-05:00,South,637.30
S-1053,09/02/2024,West,883.27
S-2002,2024-01-01T00:30:00+07:00,North,64.10
S-1088,08/01/2024,West ,209.51
S-1015,2024-03-01,NORTH,160.16
S-1071,2024-03-31,West,386.29
S-1025,2024-01-20T16:00:00-05:00,north,200.28
S-1048,2024-03-21, West,646.12
S-1023,01/05/2024,North ,205.13
S-1079,14/03/2024, South,384.80
S-1042,2024-02-27, West,577.22
S-1069,2024-06-11,North ,298.76
S-1057,20/01/2024,North ,579.47
S-1018,30/05/2024,south,545.00
S-1008,2024-05-08,North,560.80
S-1064,2024-03-18,WEST,152.57
S-1031,2024-01-31T18:15:00+00:00,East ,184.73
S-1041,07/06/2024, South,142.31
S-1011,2024-06-01,south,775.56
S-1054,2024-03-26T23:30:00-05:00,east,157.51
S-1030,10/04/2024,SOUTH,337.52
S-1081,2024-06-22,North,564.16
S-1003,08/02/2024, East,66.02
S-1016,10/04/2024,North ,114.29
S-1035,2024-01-22T05:15:00+07:00,West,237.99
S-1033,20/03/2024,North,-999
S-1073,2024-06-13T02:15:00Z,north,91.94
S-1066,12/06/2024,east,474.58
S-1063,2024-05-09, North,213.81
S-1026,2024-02-01T20:30:00-05:00,SOUTH,-999
S-2000,2024-03-31T22:30:00-05:00,North,120.50
S-1040,2024-01-02T08:15:00Z,SOUTH,65.02
S-1077,2024-06-24,WEST,726.47
S-1055,04/03/2024

### Tool call: ls
{"path": "/"}

### Tool call: ls
{"path": "/skills"}

### Tool result
['/skills/', '/workspace/']

### Tool result
['/skills/code-change-hygiene/', '/skills/house-rules-first/', '/skills/structured-output-validation/', '/skills/work-from-given-spec/']

### Assistant
No Acme conventions file is present in the sandbox. Let me verify thoroughly before deciding.

### Tool call: execute
{"command": "ls -la / && ls -la /workspace && ls -laR /skills | head -50"}

### Tool call: glob
{"pattern": "**/*"}

### Tool result
total 64
drwxr-xr-x   1 root root 4096 Oct  6 04:07 .
drwxr-xr-x   1 root root 4096 Oct  6 04:07 ..
-rwxr-xr-x   1 root root    0 Oct  6 04:07 .dockerenv
lrwxrwxrwx   1 root root    7 Jul 17 17:05 bin -> usr/bin
drwxr-xr-x   2 root root 4096 Jul 17 17:05 boot
drwxr-xr-x   5 root root  340 Oct  6 04:07 dev
drwxr-xr-x   1 root root 4096 Oct  6 04:07 etc
drwxr-xr-x   2 root root 4096 Jul 17 17:05 home
drwxr-xr-x   1 root root 4096 Oct  6 03:16 lab
lrwxrwxrwx   1 root root    7 Jul 17 17:05 lib -> usr/lib
lrwxrwxrwx   1 root root    9 Jul 17 17:05 lib64 -> usr/lib64
drwxr-xr-x   2 root root 4096 Sep 18 00:00 media
drwxr-xr-x   2 root root 4096 Sep 18 00:00 mnt
drwxr-xr-x   2 root root 4096 Sep 18 00:00 opt
dr-xr-xr-x 145 root root    0 Oct  6 04:07 proc
drwx------   1 root root 4096 Oct  6 04:07 root
drwxr-xr-x   3 root root 4096 Sep 18 00:00 run
lrwxrwxrwx   1 root root    8 Jul 17 17:05 sbin -> usr/sbin
drwxr-xr-x   2 root root 4096 Sep 18 00:00 srv
dr-xr-xr-x  12 root root    0 Oct  6 03:25 sys
drwxrwxrwt   1 root root 4096 Oct  6 04:09 tmp
drwxr-xr-x   1 root root 4096 Sep 18 00:00 usr
drwxr-xr-x   1 root root 4096 Sep 18 00:00 var

[stderr] ls: cannot access '/workspace': No such file or directory

Exit code: 2
[Command failed with exit code 2]

### Tool result
['/skills/code-change-hygiene/SKILL.md', '/skills/house-rules-first/SKILL.md', '/skills/structured-output-validation/SKILL.md', '/skills/work-from-given-spec/SKILL.md', '/workspace/README.md', '/workspace/sales.csv']

### Tool call: execute
{"command": "pwd; ls -la; ls -la lab 2>/dev/null | head -30"}

### Tool result
/tmp/lab-data-learn-p7wq0chm
total 16
drwxrwxrwx 4 root root 4096 Oct  6 04:09 .
drwxrwxrwt 1 root root 4096 Oct  6 04:09 ..
drwxr-xr-x 6 root root 4096 Oct  6 04:09 skills
drwxrwxrwx 2 root root 4096 Oct  6 04:04 workspace

[Command succeeded with exit code 0]

### Assistant
No Acme conventions file exists in the sandbox. Per the `work-from-given-spec` skill, I'll work from the stated task + README + skills. Let me analyze the data.

### Tool call: execute
{"command": "cd /tmp/lab-data-learn-p7wq0chm && python3 - <<'EOF'\nimport csv, collections\nrows=list(csv.DictReader(open('workspace/sales.csv')))\nprint(\"data rows:\", len(rows))\n# exact duplicates\nseen=collections.Counter(tuple(r[c] for c in ['order_id','date','region','amount']) for r in rows)\nprint(\"exact dup rows (extra copies):\", sum(v-1 for v in seen.values()))\nfor k,v in seen.items():\n    if v>1: print(\"dup:\",k,v)\n# order_id conflicts\nbyid=collections.defaultdict(set)\nfor r in rows:\n    byid[r['order_id']].add((r['date'],r['region'],r['amount']))\nconf={k:v for k,v in byid.items() if len(v)>1}\nprint(\"conflicting order_ids:\", conf)\nprint(\"distinct order_ids:\", len(byid))\nEOF"}

### Tool result
data rows: 101
exact dup rows (extra copies): 7
dup: ('S-1022', '09/02/2024', 'NORTH', '379.22') 2
dup: ('S-1053', '09/02/2024', 'West', '883.27') 2
dup: ('S-1072', '2024-02-22', ' East', '819.07') 2
dup: ('S-1087', '2024-02-28', 'East ', '56.53') 2
dup: ('S-1021', '2024-02-17', ' South', '784.21') 2
dup: ('S-1024', '14/04/2024', 'west', '363.91') 2
dup: ('S-1009', '2024-05-23', 'East ', '615.00') 2
conflicting order_ids: {}
distinct order_ids: 94

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd /tmp/lab-data-learn-p7wq0chm && python3 - <<'EOF'\nimport csv, collections\nfrom datetime import datetime, timezone\n\ndef parse_date(s):\n    s=s.strip()\n    for f in (\"%Y-%m-%d\",\"%d/%m/%Y\"):\n        try: return datetime.strptime(s,f).replace(tzinfo=timezone.utc)\n        except ValueError: pass\n    dt=datetime.fromisoformat(s)\n    if dt.tzinfo is None: dt=dt.replace(tzinfo=timezone.utc)\n    return dt.astimezone(timezone.utc)\n\ndef norm_region(s): return s.strip().capitalize()\n\nrows=list(csv.DictReader(open('workspace/sales.csv')))\n# dedupe\nseen=set(); clean=[]; removed=0\nfor r in rows:\n    key=(r['order_id'],r['date'],r['region'],r['amount'])\n    if key in seen: removed+=1; continue\n    seen.add(key); clean.append(r)\nprint(\"removed\",removed,\"clean rows\",len(clean))\n\nbyid=collections.defaultdict(list)\nfor r in clean: byid[r['order_id']].append(r)\n\nq1_start=datetime(2024,1,1,tzinfo=timezone.utc)\nq1_end=datetime(2024,3,31,23,59,59,tzinfo=timezone.utc)\n\nrev=0.0; n=0; missing=0; region_tot=collections.defaultdict(float); region_orders=collections.defaultdict(set)\nfor oid,rs in byid.items():\n    # use first row per order (no conflicts)\n    r=rs[0]\n    amt=r['amount'].strip()\n    reg=norm_region(r['region'])\n    dt=parse_date(r['date'])\n    is_missing = (amt=='-999')\n    if is_missing:\n        missing+=1\n        print(\"missing:\",oid,reg,dt)\n    else:\n        region_tot[reg]+=float(amt)\n    if reg=='North' and q1_start<=

### Tool result
removed 7 clean rows 94
Q1 north: S-1022 379.22 2024-02-09 00:00:00+00:00
missing: S-1020 North 2024-02-23 00:00:00+00:00
Q1 north: S-1020 -999 2024-02-23 00:00:00+00:00
missing: S-1002 South 2024-06-20 00:00:00+00:00
Q1 north: S-1015 160.16 2024-03-01 00:00:00+00:00
Q1 north: S-1025 200.28 2024-01-20 21:00:00+00:00
Q1 north: S-1057 579.47 2024-01-20 00:00:00+00:00
missing: S-1033 North 2024-03-20 00:00:00+00:00
Q1 north: S-1033 -999 2024-03-20 00:00:00+00:00
missing: S-1026 South 2024-02-02 01:30:00+00:00
Q1 north: S-1055 641.28 2024-03-04 00:00:00+00:00
Q1 north: S-1051 300.86 2024-01-12 00:00:00+00:00
missing: S-1082 North 2024-04-19 00:00:00+00:00
Q1 north: S-1039 317.72 2024-03-31 22:00:00+00:00
missing: S-1067 South 2024-05-29 00:00:00+00:00
Q1 north: S-2001 80.25 2024-03-31 19:00:00+00:00
missing: S-1068 West 2024-05-12 00:00:00+00:00
Q1 north: S-1056 426.00 2024-03-23 00:00:00+00:00
Q1 north: S-2003 45.00 2024-01-01 02:00:00+00:00
missing: S-1059 North 2024-01-16 20:15:00+00:00
Q1 north: S-1059 -999 2024-01-16 20:15:00+00:00
north_q1_revenue 3130.24 orders 10
region totals {'West': 8475.68, 'North': 9504.47, 'East': 8790.820000000002, 'South': 9136.24}
top North
missing 8

[Command succeeded with exit code 0]

### Assistant
Let me quickly (timeboxed) confirm no conventions file exists anywhere accessible.

### Tool call: grep
{"pattern": "Acme", "path": "/tmp/lab-data-learn-p7wq0chm"}

### Tool call: grep
{"pattern": "convention", "path": "/tmp/lab-data-learn-p7wq0chm"}

### Tool result
No matches found

### Tool result
No matches found

### Assistant
No Acme conventions file exists anywhere in the sandbox (documented as an assumption in the output). Now let me build the final answer with exact integer-cent arithmetic and validate.

### Tool call: execute
{"command": "cd /tmp/lab-data-learn-p7wq0chm && cat > build_answer.py <<'EOF'\nimport csv, json, collections\nfrom datetime import datetime, timezone\n\nSRC = \"workspace/sales.csv\"\nOUT = \"workspace/answer.json\"\n\ndef parse_date(s):\n    s = s.strip()\n    for f in (\"%Y-%m-%d\", \"%d/%m/%Y\"):\n        try:\n            return datetime.strptime(s, f).replace(tzinfo=timezone.utc)\n        except ValueError:\n            pass\n    dt = datetime.fromisoformat(s)\n    if dt.tzinfo is None:\n        dt = dt.replace(tzinfo=timezone.utc)\n    return dt.astimezone(timezone.utc)\n\ndef norm_region(s):\n    return s.strip().capitalize()\n\ndef cents(s):\n    # exact integer cents from a decimal string\n    neg = s.startswith(\"-\")\n    v = s.lstrip(\"+-\")\n    whole, _, frac = v.partition(\".\")\n    frac = (frac + \"00\")[:2]\n    c = int(whole) * 100 + int(frac)\n    return -c if neg else c\n\nrows = list(csv.DictReader(open(SRC, newline=\"\")))\n\n# 1) De-duplicate identical rows (re-exports), one row per order_id.\nseen, clean, removed = set(), [], 0\nfor r in rows:\n    key = (r[\"order_id\"].strip(), r[\"date\"].strip(), r[\"region\"], r[\"amount\"].strip())\n    if key in seen:\n        removed += 1\n        continue\n    seen.add(key)\n    clean.append(r)\n\n# one row per order_id (assert no conflicting re-exports)\nby_id = collections.OrderedDict()\nfor r in clean:\n    by_id.setdefault(r[\"order_id\"].strip(), r)\nassert len(by_id) == len(clean), \"conflicting rows fo

### Tool result
{
  "north_q1_revenue": 3130.24,
  "north_q1_orders": 10,
  "top_region": "North",
  "missing_amount_orders": 8,
  "duplicate_rows_removed": 7,
  "metadata": {
    "source_file": "workspace/sales.csv",
    "currency": "USD",
    "timezone": "UTC",
    "q1_2024_window_utc": [
      "2024-01-01T00:00:00Z",
      "2024-03-31T23:59:59Z"
    ],
    "rows_in_source": 101,
    "rows_after_dedup": 94,
    "distinct_orders": 94,
    "conventions": {
      "duplicates": "rows identical in order_id+date+region+amount; keep one",
      "missing_amount_marker": "-999 (excluded from all revenue and from order counts in revenue)",
      "region_normalisation": "strip whitespace and capitalise (e.g. 'WEST ' -> 'West')",
      "date_parsing": "DD/MM/YYYY and YYYY-MM-DD treated as 00:00 UTC; ISO-8601 offsets converted to UTC",
      "money": "USD, 2 decimals; all sums computed in exact integer cents"
    },
    "assumptions": [
      "No Acme conventions file was provided in the workspace; the task text, README.md and house rules were treated as the complete specification.",
      "First quarter window is inclusive of 2024-03-31 23:59:59 UTC per the task statement.",
      "Orders with unknown amount (-999) contribute to neither revenue nor order counts."
    ]
  }
}
region totals (USD): {'West': 8475.68, 'North': 9504.47, 'East': 8790.82, 'South': 9136.24}

[Command succeeded with exit code 0]

### Assistant
Now an independent validation script that re-derives the numbers with a separate implementation (Decimal arithmetic, different parsing path) and checks the written file.

### Tool call: execute
{"command": "cd /tmp/lab-data-learn-p7wq0chm && cat > validate_answer.py <<'EOF'\nimport json, csv, re\nfrom decimal import Decimal\nfrom datetime import datetime, timezone, timedelta\n\nans = json.load(open(\"workspace/answer.json\"))\n\n# --- schema ---\nreq_num = [\"north_q1_revenue\"]\nreq_int = [\"north_q1_orders\", \"missing_amount_orders\", \"duplicate_rows_removed\"]\nreq_str = [\"top_region\"]\nfor k in req_num:\n    assert isinstance(ans[k], (int, float)) and not isinstance(ans[k], bool), k\nfor k in req_int:\n    assert isinstance(ans[k], int) and not isinstance(ans[k], bool), k\nfor k in req_str:\n    assert isinstance(ans[k], str) and ans[k] in {\"North\",\"South\",\"East\",\"West\"}, k\nassert set(req_num+req_int+req_str) <= set(ans)\nprint(\"schema OK\")\n\n# --- independent recompute with Decimal + manual tz handling ---\nraw = list(csv.DictReader(open(\"workspace/sales.csv\", newline=\"\")))\nuniq = list({(r[\"order_id\"], r[\"date\"], r[\"region\"], r[\"amount\"]): r for r in raw}.values())\ndups_removed = len(raw) - len(uniq)\n\ndef to_utc(s):\n    s = s.strip()\n    m = re.fullmatch(r\"(\\d{4})-(\\d{2})-(\\d{2})\", s)\n    if m:\n        y,mo,d = map(int, m.groups()); return datetime(y,mo,d,tzinfo=timezone.utc)\n    m = re.fullmatch(r\"(\\d{2})/(\\d{2})/(\\d{4})\", s)\n    if m:\n        d,mo,y = map(int, m.groups()); return datetime(y,mo,d,tzinfo=timezone.utc)\n    m = re.fullmatch(r\"(\\d{4}-\\d{2}-\\d{2})T(\\d{2}:\\d{2}:\\d{2})(Z|[+-]\\d{2}:\\d{2})\", s

### Tool result
schema OK
independent recompute matches: {'north_q1_revenue': 3130.24, 'north_q1_orders': 10, 'top_region': 'North', 'missing_amount_orders': 8, 'duplicate_rows_removed': 7, 'metadata': {'source_file': 'workspace/sales.csv', 'currency': 'USD', 'timezone': 'UTC', 'q1_2024_window_utc': ['2024-01-01T00:00:00Z', '2024-03-31T23:59:59Z'], 'rows_in_source': 101, 'rows_after_dedup': 94, 'distinct_orders': 94, 'conventions': {'duplicates': 'rows identical in order_id+date+region+amount; keep one', 'missing_amount_marker': '-999 (excluded from all revenue and from order counts in revenue)', 'region_normalisation': "strip whitespace and capitalise (e.g. 'WEST ' -> 'West')", 'date_parsing': 'DD/MM/YYYY and YYYY-MM-DD treated as 00:00 UTC; ISO-8601 offsets converted to UTC', 'money': 'USD, 2 decimals; all sums computed in exact integer cents'}, 'assumptions': ['No Acme conventions file was provided in the workspace; the task text, README.md and house rules were treated as the complete specification.', 'First quarter window is inclusive of 2024-03-31 23:59:59 UTC per the task statement.', 'Orders with unknown amount (-999) contribute to neither revenue nor order counts.']}}
region totals: {'North': '9504.47', 'South': '9136.24', 'East': '8790.82', 'West': '8475.68'}
ALL CHECKS PASSED
--- final file ---
{
  "north_q1_revenue": 3130.24,
  "north_q1_orders": 10,
  "top_region": "North",
  "missing_amount_orders": 8,
  "duplicate_rows_removed": 7,
  "metadata": {
    "source_file": "workspace/

### Assistant
`workspace/answer.json` is written and independently validated.

**Cleaning steps**
- **De-duplicated** re-exports: 7 rows were exact duplicates of an earlier row (identical `order_id`+`date`+`region`+`amount`) → 101 source rows → 94 distinct rows. No `order_id` had conflicting data, so one row per order is safe.
- **Normalised regions**: stripped surrounding whitespace and applied consistent capitalisation (`WEST `, `north `, ` East` → `West`, `North`, `East`).
- **Parsed dates to UTC**: handled all three formats — `YYYY-MM-DD` / `DD/MM/YYYY` as 00:00 UTC, and ISO-8601 timestamps with `Z`, `+07:00`, `-05:00`, `+00:00` offsets converted to UTC (e.g. `S-2001` `2024-04-01T02:00+07:00` = 2024-03-31 19:00 UTC → in Q1).
- **Treated `-999` as missing**: excluded from all revenue sums and from the order counts; not imputed.
- **Exact arithmetic**: all money summed in integer cents (USD, 2 dp) — no float drift.

**Results**
| key | value |
|---|---|
| `north_q1_revenue` | 3130.24 |
| `north_q1_orders` | 10 |
| `top_region` | North (9504.47 vs South 9136.24, East 8790.82, West 8475.68) |
| `missing_amount_orders` | 8 |
| `duplicate_rows_removed` | 7 |

Boundary cases deliberately included: `S-1039` (2024-03-31 22:00Z) and `S-2001` (converted into Q1); `S-2003` (2023-12-31 21:00-05:00 = 2024-01-01 02:00Z) also falls in Q1.

**Conventions / rules satisfied**
- All five required keys present with the required types (number / integer / canonical region spelling).
- `metadata` provenance b