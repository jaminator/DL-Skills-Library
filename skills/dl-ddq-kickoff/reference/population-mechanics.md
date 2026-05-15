# Population Mechanics — Step 4

## Contents

- The two-script split
- Step 4a — compute the periods
- Step 4b — build the content dict (schema pointer)
- Step 4c — run the population script
- Placeholder-substitution contract
- List-injection rules
- One-page line-budget check
- Out of scope

---

## The two-script split

Two scripts, each with one job and one source of truth:

- `scripts/compute_periods.py` owns the **dates** (the FY / LTM / quarter /
  budget / forecast fragment strings). Claude never derives these by hand.
- `scripts/populate_kickoff.py` owns the **boilerplate wording** around those
  fragments and the in-place Word edit. It builds each standard line from the
  period fragments so the request text has exactly one home.

Keeping them split means a fiscal-calendar change touches only the period
engine and a wording change touches only the population script — neither can
silently drift from the other.

---

## Step 4a — compute the periods

```bash
python scripts/compute_periods.py --system-date 2026-05-28 \
    [--fiscal-year-end MM-DD] [--history-years 3] [--forecast-years 5]
```

Capture the JSON it prints to stdout. Pass it through verbatim as
`content["periods"]` — do not edit the fragment strings.

---

## Step 4b — build the content dict (schema pointer)

The complete content-dict schema is the docstring at the top of
`scripts/populate_kickoff.py` (CONTENT JSON SCHEMA). It is mirrored
field-for-field by the `KickoffDataRequest` Pydantic model in
`schemas/kickoff_data_request.py`; that schema is the Arrakis-side
structured-output contract. Top-level keys:

- `company_name` (str) — header company placeholder
- `owner` (str | null) — the header `(Sponsor)` parenthetical; `null` removes it
- `as_of_date` (str | null) — e.g. `"May 28, 2026"`; refreshes the header DATE
  field's cached value (the field still auto-updates on open)
- `periods` (object) — the verbatim `compute_periods.py` output
- `compliance_cert_applicable` (bool) — `false` suffixes the existing
  compliance-cert line with an N/A note; the line is **never deleted**
- `stock_cut_requests` (list[str]) — the every-borrower standard cuts
- `borrower_kpi_requests` (list[str]) — the sector-specific KPI lines

---

## Step 4c — run the population script

```python
import json, subprocess
from pathlib import Path

Path("/tmp/kickoff_content.json").write_text(json.dumps(content, indent=2))
output_path = (
    "/mnt/user-data/outputs/"
    "<Company>_-_Wells_&_Overland_Kick-Off_Data_Requests_<MM-DD-YY>_vS.docx"
)
subprocess.run(
    ["python", "scripts/populate_kickoff.py",
     "/tmp/kickoff_content.json", output_path],
    check=True,
)
```

`<MM-DD-YY>` is the system/as-of date. The `vS` suffix is the draft-state
signal (the D-2 watermark carve-out — see SKILL.md). Return the output via
`present_files`.

---

## Placeholder-substitution contract

The template is a flat one-page bulleted list (no tables). The script
identifies each of the seven standard lines by a stable anchor substring of its
template text and rewrites it from the period fragments:

| Anchor substring | Rebuilt line |
|---|---|
| `Audited Financial Statements` | `{audited_range} Audited Financial Statements` |
| `Bridge to Consolidated EBITDA` | `LTM {ltm_anchor} Income Statement & Bridge to Consolidated EBITDA` |
| `Quarterly Internal Financial` | `{quarterly_range} Quarterly Internal Financial Statements (i.e., Income Statement, Balance Sheet, Cash Flow Statement)` |
| `Loan Reporting` | `{quarterly_range} Quarterly Existing Loan Reporting & Compliance Certificates` + `(If Applicable)` or the N/A note |
| `Quarterly Mgmt. KPI` | `{quarterly_range} Quarterly Mgmt. KPI's` |
| `Budgeted Financial Statements` | `{budget_fy} Budgeted Financial Statements` |
| `Long-Term Financial Statement Forecast` | `{forecast_range} Long-Term Financial Statement Forecast` |

Rules the script enforces:

- **In place, never regenerated.** The bundled template is edited and saved
  under a new name; the document is never rebuilt. Regeneration would strip the
  `NumberList1` numbering and the `Bullet2` list styling.
- **Footnotes survive.** The LTM line carries footnote 1 and the Mgmt. KPI line
  carries footnote 2. The script writes new text into the first text run only
  and leaves the `<w:footnoteReference>` run untouched, so both footnotes
  remain bound to their lines.
- **Anchor-not-found fails loudly.** If a template change removes an anchor the
  script raises rather than silently skipping a required line.
- **Compliance line is never deleted.** When `compliance_cert_applicable` is
  false the line is suffixed ` — N/A (no existing reporting facility)`; the
  request line stays in the document.

---

## List-injection rules

The standard stock-cut lines and the borrower-specific KPI lines are inserted
as new `Bullet2` sub-bullets **under the Historical KPIs section**, immediately
after the (rewritten) Quarterly Mgmt. KPI's line and before the blank
separator. Each new bullet is a deep copy of the Mgmt. KPI paragraph element,
so it inherits the `Bullet2` paragraph style and the `SubtleReference` run
style exactly; the cloned footnote run and proofErr markers are stripped from
the copy. The three `NumberList1` section headers (numId 9) are not touched —
only `Bullet2` children are added — so the `1. / 2. / 3.` numbering is
preserved.

Order of inserted lines: `stock_cut_requests` first, then
`borrower_kpi_requests`, each in list order.

---

## One-page line-budget check

`populate_kickoff.py` enforces `MAX_KPI_LINES = 14` on
`borrower_kpi_requests` (the stock cuts are not counted — they are a fixed,
known set). The value is a layout fact: the template body, the three numbered
sections, the standard set, and ~14 terse noun-phrase KPI lines fill exactly
one page at the template's styling. Exceeding it raises a verbose error listing
the overflow lines. Tighten phrasing and merge related cuts into a single
line — do not raise the cap.

---

## Out of scope

- No analyst-populated charts or tables exist in this template — it is a pure
  request list, so there is no "populated by the analyst afterward" carve-out
  (unlike the posting memo).
- The downstream sector-classification skill that produces the NAICS/GICS
  handoff is a separate artifact; this skill consumes that classification as a
  given input.
