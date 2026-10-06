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
I'll start by reading the relevant skill files and the task workspace.

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
{"file_path": "/workspace/README.md", "limit": 1000}

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
{"file_path": "/workspace/sales.csv", "limit": 1000}

### Tool call: ls
{"path": "/"}

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

### Tool result
['/skills/', '/workspace/']

### Assistant
Now let me analyze the data carefully with a script.

### Tool call: execute
{"command": "cd /workspace && python3 -c \"\nimport csv\nfrom collections import Counter, defaultdict\nrows=list(csv.DictReader(open('sales.csv')))\nprint('total rows', len(rows))\nids=[r['order_id'] for r in rows]\nc=Counter(ids)\ndups={k:v for k,v in c.items() if v>1}\nprint('order_ids appearing >1:', dups)\nprint('num extra rows', sum(v-1 for v in dups.values()))\n# check identical content per dup id\nfor k in dups:\n    variants={tuple(sorted(r.items())) for r in rows if r['order_id']==k}\n    print(k, len(variants), variants if len(variants)>1 else '')\n\"\n"}

### Tool result
[stderr] /bin/sh: 1: cd: can't cd to /workspace

Exit code: 2
[Command failed with exit code 2]

### Tool call: execute
{"command": "pwd && ls"}

### Tool result
/tmp/lab-data-learn-kcjm5jth
skills
workspace

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "python3 -c \"\nimport csv\nfrom collections import Counter\nrows=list(csv.DictReader(open('workspace/sales.csv')))\nprint('total rows', len(rows))\nc=Counter(r['order_id'] for r in rows)\ndups={k:v for k,v in c.items() if v>1}\nprint('ids with >1:', dups)\nprint('extra rows', sum(v-1 for v in dups.values()))\nfor k in dups:\n    variants={tuple(sorted(r.items())) for r in rows if r['order_id']==k}\n    print(k, 'variants:', len(variants))\n    if len(variants)>1:\n        for v in variants: print('   ', v)\n\"\n"}

### Tool result
total rows 101
ids with >1: {'S-1022': 2, 'S-1053': 2, 'S-1072': 2, 'S-1087': 2, 'S-1021': 2, 'S-1024': 2, 'S-1009': 2}
extra rows 7
S-1022 variants: 1
S-1053 variants: 1
S-1072 variants: 1
S-1087 variants: 1
S-1021 variants: 1
S-1024 variants: 1
S-1009 variants: 1

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "python3 -c \"\nimport csv\nfrom collections import Counter\nfrom datetime import datetime, timezone, timedelta\nrows=list(csv.DictReader(open('workspace/sales.csv')))\nseen=set(); clean=[]\nremoved=0\nfor r in rows:\n    if r['order_id'] in seen:\n        removed+=1; continue\n    seen.add(r['order_id']); clean.append(r)\nprint('removed', removed, 'distinct', len(clean))\ndef pd(s):\n    s=s.strip()\n    for f in ('%Y-%m-%d','%d/%m/%Y'):\n        try: return datetime.strptime(s,f).replace(tzinfo=timezone.utc)\n        except ValueError: pass\n    if s.endswith('Z'): s=s[:-1]+'+00:00'\n    return datetime.fromisoformat(s).astimezone(timezone.utc)\ndef preg(s):\n    m={'north':'North','south':'South','east':'East','west':'West'}\n    return m[s.strip().lower()]\nq1s=datetime(2024,1,1,tzinfo=timezone.utc); q1e=datetime(2024,3,31,23,59,59,tzinfo=timezone.utc)\ntot=Counter(); north=[]; missing=set()\nfor r in clean:\n    d=pd(r['date']); reg=preg(r['region']); a=float(r['amount'])\n    if a==-999: missing.add(r['order_id']); continue\n    tot[reg]+=a\n    if reg=='North' and q1s<=d<=q1e: north.append((r['order_id'],d,a))\nprint('totals', {k:round(v,2) for k,v in tot.items()})\nprint('north q1 orders', len(north), 'sum', round(sum(x[2] for x in north),2))\nprint('missing', len(missing), sorted(missing))\nfor x in sorted(north, key=lambda x:x[1]): print('  ',x)\n\"\n"}

### Tool result
removed 7 distinct 94
totals {'West': 8475.68, 'North': 9504.47, 'East': 8790.82, 'South': 9136.24}
north q1 orders 10 sum 3130.24
missing 8 ['S-1002', 'S-1020', 'S-1026', 'S-1033', 'S-1059', 'S-1067', 'S-1068', 'S-1082']
   ('S-2003', datetime.datetime(2024, 1, 1, 2, 0, tzinfo=datetime.timezone.utc), 45.0)
   ('S-1051', datetime.datetime(2024, 1, 12, 0, 0, tzinfo=datetime.timezone.utc), 300.86)
   ('S-1057', datetime.datetime(2024, 1, 20, 0, 0, tzinfo=datetime.timezone.utc), 579.47)
   ('S-1025', datetime.datetime(2024, 1, 20, 21, 0, tzinfo=datetime.timezone.utc), 200.28)
   ('S-1022', datetime.datetime(2024, 2, 9, 0, 0, tzinfo=datetime.timezone.utc), 379.22)
   ('S-1015', datetime.datetime(2024, 3, 1, 0, 0, tzinfo=datetime.timezone.utc), 160.16)
   ('S-1055', datetime.datetime(2024, 3, 4, 0, 0, tzinfo=datetime.timezone.utc), 641.28)
   ('S-1056', datetime.datetime(2024, 3, 23, 0, 0, tzinfo=datetime.timezone.utc), 426.0)
   ('S-2001', datetime.datetime(2024, 3, 31, 19, 0, tzinfo=datetime.timezone.utc), 80.25)
   ('S-1039', datetime.datetime(2024, 3, 31, 22, 0, tzinfo=datetime.timezone.utc), 317.72)

[Command succeeded with exit code 0]

### Assistant
Let me verify edge cases (boundaries, region/date parsing, precision) before writing output.

### Tool call: execute
{"command": "python3 -c \"\nimport csv\nfrom collections import Counter\nfrom datetime import datetime, timezone\nfrom decimal import Decimal, ROUND_HALF_UP\nrows=list(csv.DictReader(open('workspace/sales.csv')))\nseen=set(); clean=[]; removed=0\nfor r in rows:\n    if r['order_id'] in seen: removed+=1; continue\n    seen.add(r['order_id']); clean.append(r)\ndef pd(s):\n    s=s.strip()\n    for f in ('%Y-%m-%d','%d/%m/%Y'):\n        try: return datetime.strptime(s,f).replace(tzinfo=timezone.utc)\n        except ValueError: pass\n    if s.endswith('Z'): s=s[:-1]+'+00:00'\n    return datetime.fromisoformat(s).astimezone(timezone.utc)\nregs=Counter(r['region'].strip().lower() for r in clean)\nprint('regions:', regs)\namts=[r['amount'] for r in clean]\nbad=[a for a in amts if not a.replace('.','',1).replace('-','',1).isdigit()]\nprint('non numeric amounts:', bad)\nprint('distinct amounts == -999 count rows:', sum(1 for a in amts if float(a)==-999))\n# duplicates content check across all rows\nc=Counter(r['order_id'] for r in rows)\nprint('dup ids identical content:', all(len({tuple(sorted(x.items())) for x in rows if x['order_id']==k})==1 for k,v in c.items() if v>1))\n\" "}

### Tool result
regions: Counter({'north': 31, 'south': 24, 'east': 21, 'west': 18})
non numeric amounts: []
distinct amounts == -999 count rows: 8
dup ids identical content: True

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "ls -la workspace; ls -la ."}

### Tool result
total 16
drwxrwxrwx 2 root root 4096 Oct  6 04:04 .
drwxrwxrwx 4 root root 4096 Oct  6 04:58 ..
-rw-rw-rw- 1 root root  597 Oct  6 04:04 README.md
-rw-rw-rw- 1 root root 3646 Oct  6 04:04 sales.csv
total 16
drwxrwxrwx 4 root root 4096 Oct  6 04:58 .
drwxrwxrwt 1 root root 4096 Oct  6 04:58 ..
drwxr-xr-x 6 root root 4096 Oct  6 04:58 skills
drwxrwxrwx 2 root root 4096 Oct  6 04:04 workspace

[Command succeeded with exit code 0]

### Tool call: ls
{"path": "/skills"}

### Tool call: glob
{"pattern": "**/*", "path": "/skills"}

### Tool result
['/skills/code-change-hygiene/', '/skills/house-rules-first/', '/skills/structured-output-validation/', '/skills/work-from-given-spec/']

### Tool result
['/skills/code-change-hygiene/SKILL.md', '/skills/house-rules-first/SKILL.md', '/skills/structured-output-validation/SKILL.md', '/skills/work-from-given-spec/SKILL.md']

### Tool call: execute
{"command": "python3 -c \"\nimport csv\nfrom collections import Counter\nfrom datetime import datetime, timezone\nfrom decimal import Decimal\nrows=list(csv.DictReader(open('workspace/sales.csv')))\nseen=set(); clean=[]; removed=0\nfor r in rows:\n    if r['order_id'] in seen: removed+=1; continue\n    seen.add(r['order_id']); clean.append(r)\ndef pd(s):\n    s=s.strip()\n    for f in ('%Y-%m-%d','%d/%m/%Y'):\n        try: return datetime.strptime(s,f).replace(tzinfo=timezone.utc)\n        except ValueError: pass\n    if s.endswith('Z'): s=s[:-1]+'+00:00'\n    return datetime.fromisoformat(s).astimezone(timezone.utc)\nm={'north':'North','south':'South','east':'East','west':'West'}\nqs=datetime(2024,1,1,tzinfo=timezone.utc); qe=datetime(2024,3,31,23,59,59,tzinfo=timezone.utc)\ntot=Counter(); nq=Decimal(0); ncount=0; missing=0\nfor r in clean:\n    a=Decimal(r['amount']); reg=m[r['region'].strip().lower()]; d=pd(r['date'])\n    if a==-999: missing+=1; continue\n    tot[reg]+=a\n    if reg=='North' and qs<=d<=qe: nq+=a; ncount+=1\nprint('north_q1_revenue', nq, float(nq))\nprint('north_q1_orders', ncount)\nprint('top', max(tot.items(), key=lambda x:x[1]))\nprint('missing', missing)\nprint('dup', removed)\nprint({k:str(v) for k,v in tot.items()})\n\""}

### Tool result
north_q1_revenue 3130.24 3130.24
north_q1_orders 10
top ('North', Decimal('9504.47'))
missing 8
dup 7
{'West': '8475.68', 'North': '9504.47', 'East': '8790.82', 'South': '9136.24'}

[Command succeeded with exit code 0]

### Assistant
No conventions file exists in the workspace (only README + sales.csv), so per the house-rules/work-from-given-spec skills I'll use the stated spec and document my interpretation in a provenance block. Let me build the deliverables with a deterministic script.

### Tool call: write_file
{"file_path": "/workspace/clean_sales.py", "content": "\"\"\"Clean workspace/sales.csv and emit workspace/answer.json.\n\nCleaning rules applied (from workspace/README.md and the task statement):\n  * order_id identifies an order; re-exported duplicates are dropped so that\n    exactly one row per order_id is kept (first occurrence wins).\n  * date appears as YYYY-MM-DD, DD/MM/YYYY (date only == 00:00 UTC) or an\n    ISO-8601 timestamp with a UTC offset; everything is normalised to UTC.\n  * region spelling/casing is inconsistent; canonicalised to North/South/East/West.\n  * amount == -999 means missing/unknown; such orders never contribute revenue.\nQ1 2024 window is inclusive: 2024-01-01T00:00:00Z .. 2024-03-31T23:59:59Z.\n\"\"\"\n\nfrom __future__ import annotations\n\nimport csv\nimport json\nfrom collections import Counter\nfrom datetime import datetime, timezone\nfrom decimal import Decimal\nfrom pathlib import Path\n\nWORKSPACE = Path(__file__).resolve().parent\nSOURCE = WORKSPACE / \"sales.csv\"\nOUTPUT = WORKSPACE / \"answer.json\"\n\nMISSING_AMOUNT = Decimal(\"-999\")\nQ1_START = datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)\nQ1_END = datetime(2024, 3, 31, 23, 59, 59, tzinfo=timezone.utc)\nREGIONS = {\"north\": \"North\", \"south\": \"South\", \"east\": \"East\", \"west\": \"West\"}\n\n\ndef parse_date(raw: str) -> datetime:\n    \"\"\"Parse any of the three supported date formats into a UTC datetime.\"\"\"\n    text = raw.strip()\n    for fmt in (\"%Y-%m-%d\",

### Tool result
Updated file /workspace/clean_sales.py

### Tool call: execute
{"command": "python3 workspace/clean_sales.py"}

### Tool result
{
  "north_q1_revenue": 3130.24,
  "north_q1_orders": 10,
  "top_region": "North",
  "missing_amount_orders": 8,
  "duplicate_rows_removed": 7,
  "metadata": {
    "source_file": "workspace/sales.csv",
    "generated_at_utc": "2026-10-06T04:59:00Z",
    "rows_read": 101,
    "rows_after_dedup": 94,
    "duplicate_rows_removed": 7,
    "dedupe_key": "order_id",
    "missing_amount_marker": -999,
    "missing_amount_orders": 8,
    "currency": "USD",
    "amount_unit": "USD (decimal)",
    "timestamps_normalized_to_utc": true,
    "q1_window_utc": "2024-01-01T00:00:00Z/2024-03-31T23:59:59Z",
    "region_canonicalization": "trimmed whitespace and case-insensitive match to North/South/East/West",
    "regression_note": "revenue excludes orders with a missing amount (-999)"
  }
}

[Command succeeded with exit code 0]

### Assistant
Now an independent validation script (separate parsing path) that re-derives and checks the written file.

### Tool call: write_file
{"content": "\"\"\"Independent validation of workspace/answer.json.\n\nRe-derives every required value with a second, independent implementation and\nchecks schema, types, and consistency against the written JSON.\n\"\"\"\n\nfrom __future__ import annotations\n\nimport csv\nimport json\nimport re\nfrom datetime import datetime, timedelta, timezone\nfrom decimal import Decimal\nfrom pathlib import Path\n\nWS = Path(__file__).resolve().parent\nISO_RE = re.compile(\n    r\"^(?P<y>\\d{4})-(?P<m>\\d{2})-(?P<d>\\d{2})T(?P<H>\\d{2}):(?P<M>\\d{2}):\"\n    r\"(?P<S>\\d{2})(?P<off>Z|[+-]\\d{2}:\\d{2})$\"\n)\nDMY_RE = re.compile(r\"^(?P<d>\\d{2})/(?P<m>\\d{2})/(?P<y>\\d{4})$\")\nYMD_RE = re.compile(r\"^(?P<y>\\d{4})-(?P<m>\\d{2})-(?P<d>\\d{2})$\")\n\n\ndef to_utc(text: str) -> datetime:\n    t = text.strip()\n    if m := YMD_RE.match(t):\n        return datetime(int(m[\"y\"]), int(m[\"m\"]), int(m[\"d\"]), tzinfo=timezone.utc)\n    if m := DMY_RE.match(t):\n        return datetime(int(m[\"y\"]), int(m[\"m\"]), int(m[\"d\"]), tzinfo=timezone.utc)\n    if not (m := ISO_RE.match(t)):\n        raise ValueError(f\"unparsed date: {text!r}\")\n    base = datetime(\n        int(m[\"y\"]), int(m[\"m\"]), int(m[\"d\"]), int(m[\"H\"]), int(m[\"M\"]), int(m[\"S\"]),\n        tzinfo=timezone.utc,\n    )\n    off = m[\"off\"]\n    if off != \"Z\":\n        sign = 1 if off[0] == \"+\" else -1\n        hh, mm = int(off[1:3]), int(off[4:6])\n        base -= sign * timedelta(hours=hh, minutes=mm)\n    re

### Tool result
Updated file /workspace/validate_answer.py

### Tool call: execute
{"command": "python3 workspace/validate_answer.py && python3 -c \"import json;d=json.load(open('workspace/answer.json'));print(list(d.keys()))\""}

### Tool result
expected: {'north_q1_revenue': Decimal('3130.24'), 'north_q1_orders': 10, 'top_region': 'North', 'missing_amount_orders': 8, 'duplicate_rows_removed': 7}
VALIDATION PASSED
['north_q1_revenue', 'north_q1_orders', 'top_region', 'missing_amount_orders', 'duplicate_rows_removed', 'metadata']

[Command succeeded with exit code 0]

### Tool call: read_file
{"file_path": "/workspace/answer.json"}

### Tool result
@@ lines 1-23 of 23 @@
{
  "north_q1_revenue": 3130.24,
  "north_q1_orders": 10,
  "top_region": "North",
  "missing_amount_orders": 8,
  "duplicate_rows_removed": 7,
  "metadata": {
    "source_file": "workspace/sales.csv",
    "generated_at_utc": "2026-10-06T04:59:00Z",
    "rows_read": 101,
    "rows_after_dedup": 94,
    "duplicate_rows_removed": 7,
    "dedupe_key": "order_id",
    "missing_amount_marker": -999,
    "missing_amount_orders": 8,
    "currency": "USD",
    "amount_unit": "USD (decimal)",
    "timestamps_normalized_to_utc": true,
    "q1_window_utc": "2024-01-01T00:00:00Z/2024-03-31T23:59:59Z",
    "region_canonicalization": "trimmed whitespace and case-insensitive match to North/South/East/West",
    "regression_note": "revenue excludes orders with a missing amount (-999)"
  }
}

### Assistant
Done. Validation passed and the answer reconciles with an independently-written checker.

**Output:** `workspace/answer.json` (plus the deterministic generator `workspace/clean_sales.py` and independent checker `workspace/validate_answer.py`).

Keys in `answer.json`: `north_q1_revenue: 3130.24`, `north_q1_orders: 10`, `top_region: "North"`, `missing_amount_orders: 8`, `duplicate_rows_removed: 7`, plus a `metadata` provenance block (source file, row counts, dedupe key, missing-amount marker, currency USD, UTC window, canonicalization notes) since the reporting conventions require documenting the interpretation. No conventions file exists in the workspace, so I worked from the stated spec (per the house-rules-first / work-from-given-spec skills) and documented each decision.

**How the data was cleaned:**
- **Duplicates:** `order_id` is the order key, so re-exported duplicates were dropped keeping one row per order — 101 rows → 94 distinct orders, i.e. **7 duplicate rows removed** (all seven dup pairs/groups were byte-identical). All answers use this deduped set.
- **Dates → UTC:** parsed the three formats (`YYYY-MM-DD`, `DD/MM/YYYY` as 00:00 UTC, and ISO-8601 with offsets/`Z`) and converted every timestamp to UTC before applying the inclusive Q1 window `2024-01-01T00:00:00Z … 2024-03-31T23:59:59Z`. This correctly includes S‑2003 (`2023-12-31T21:00-05:00` → 2024‑01‑01) and S‑2001 (`2024-04-01T02:00+07:00` → 2024‑03‑31), and excludes S‑2000 (`2024-03-31T22:30-05:00` → April).
- 