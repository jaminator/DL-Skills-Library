# Push-2 Plan — `dl-ddq-kickoff` Kick-Off Data Requests Bundle

Status: PLAN (approved scope for the push-2 build checkpoint). This document is
the design contract; the build is a separate checkpoint executed against it.

Author context: session-start anchors and best-practices files re-read; template
structure in `raw/` inspected directly. Conforms to `docs/anthropic/Skills_Best_Practices.md`,
`docs/anthropic/Prompting_Best_Practices.md`, the four-artifact bundle pattern
([[library-artifact-bundle]]), and the `dl-<domain>-<action-or-subtype>` naming
rule ([[skill-naming-convention]]).

---

## 1. Objective

Build the four-artifact bundle that populates the
`[Company] - Wells & Overland Kick-Off Data Requests (MM-DD-YY) vTemplate.docx`
one-pager from preliminary, post-NDA borrower information (teaser, Wells Fargo /
company email color, post-NDA desktop research, PitchBook, the sector
classification handoff) and returns the populated `.docx` — not a regenerated
document — ready for the deal team to send to the company or debt advisor.

The deliverable's purpose is to front-load the data that downstream artifacts
need: it pre-seeds the posting memo + backup, the databook (`FinInputs`
quarterly grid, Top-N concentration cuts), and the Overland model (budget +
long-range forecast), and it adds borrower-specific KPI cuts derived from the
NAICS/GICS classification and the Overland frameworks.

## 2. Naming, lifecycle placement, shape

| Property | Value | Source of truth |
| --- | --- | --- |
| Skill name | `dl-ddq-kickoff` | CLAUDE.md domain registry (literal example for `ddq`); no new domain |
| Lifecycle | Stage 2 / P3 Kick-Off Data Requests | [[screening-templates]] ("Kick-Off Data Requests (P3, .docx)") |
| Shape | generate-with-review over a deterministic period-math core | [[opportunity-shapes]] |
| Arrakis target | Foldspace screening application (same app as the P4 pair) | [[application-directory]] |
| Consumer | borrower / debt advisor (outbound), seeding internal screening | [[library-artifact-bundle]] |

No CLAUDE.md edit and no new domain registration are required — `ddq` and
`dl-ddq-kickoff` already exist in the registry.

## 3. The four artifacts

### 3.1 Skill — `skills/dl-ddq-kickoff/`

```
skills/dl-ddq-kickoff/
├── SKILL.md
├── assets/
│   └── kickoff-data-requests-template.docx   # copied byte-identical from raw/
├── scripts/
│   ├── compute_periods.py                    # deterministic date engine
│   └── populate_kickoff.py                   # in-place template population
└── reference/
    ├── kpi-frameworks.md                     # framework→request map + sector library
    └── population-mechanics.md               # content-dict schema, run snippet, list-injection rules
```

**`SKILL.md` (≤500 lines, third-person description naming what + when).** Body
structure:

- *Orientation*: deliverable is a populated `.docx`; never regenerate; one-page
  hard ceiling; `TBD`/`[INSUFFICIENT DATA — …]` discipline.
- *Step 1 — Period math (low freedom).* Run `scripts/compute_periods.py` with
  the system date, optional borrower fiscal-year-end, optional history-year
  override (default 3), optional forecast horizon. The script emits the period
  strings; Claude does not compute dates by hand.
- *Step 2 — Standard request set (deterministic).* The always-included lines:
  3-FY audited financials; LTM income statement + bridge to consolidated
  EBITDA; quarterly internal IS/BS/CF for the computed range; quarterly existing
  loan reporting & compliance certificates **only if** the borrower has an
  existing commercial-bank or direct-lending facility and reports regularly
  (else mark the line N/A — do not delete the template line); current-FY budget;
  long-range forecast over the model horizon. Plus the every-borrower "stock
  cuts": Top-1 / Top-10 customer and supplier concentration; maintenance vs.
  growth capex split; NWC build; existing debt & debt-like items remaining
  post-close with go-forward cash payouts (earn-out / deferred-consideration
  "payment-bomb" screen); and, when buy-and-build, add-on history (LTM at close
  vs. current per cohort) and add-on consideration structure (upfront cash,
  seller/deferred notes, earnouts, rollover equity — informs the DDTL governor).
- *Step 3 — Borrower-specific KPI block (high freedom, framework-grounded).*
  Reason from the NAICS/GICS classification + business description through the
  Overland industry attractiveness screen, credit-quality screen, and FCF
  decomposition sequence to derive the KPI requests a management team in that
  industry would track in the normal course. Constraint: request only
  plausibly "off-the-shelf" data; do not request bespoke analyses. Detail and
  the worked sector library live in `reference/kpi-frameworks.md`.
- *Step 4 — Populate.* Build the content dict, run
  `scripts/populate_kickoff.py`, return the deal-named draft `.docx`.
- *Anti-patterns* (consolidated, no new behavior).

**`reference/kpi-frameworks.md`** (Contents section; ≥100 lines): a map from
each Overland framework dimension to the data-request archetype it implies
(demand-driver quality → recurring/reoccurring/break-fix revenue cuts;
concentration discipline → Top-N customer/supplier; operating leverage →
fixed/variable cost split; capital intensity → maintenance/growth capex;
ownership/workout → existing debt-like items & consideration structure), the
downstream-consumer rationale (which databook/model/posting-memo field each
request pre-seeds, cross-referencing [[dd-workbook-input-schema]] and
[[screening-input-schema]]), and a worked sector library with **residential
HVAC services roll-up** as the canonical few-shot (lead conversion, ticket
volume & average ticket by service line and by job type, technician retention,
4-wall P&L by brand/branch, OEM rebate income & purchases, add-on cohort
organic-growth and consideration structure, capex splits, post-close debt-like
payouts) plus 2–3 contrasting sector sketches.

**`reference/population-mechanics.md`**: content-dict schema pointer, the run
snippet, the list-injection rules (new KPI lines inserted under the *Historical
KPIs* header preserving numId 9 / `Bullet2` / `NumberList1` styles), the
placeholder-substitution contract, and the one-page line-budget check.

**Degrees of freedom**: low for period math and population (fragile, must be
consistent — scripted), high for the KPI block (context-dependent — text
instructions + worked examples). Matches the Skills best-practices guidance.

### 3.2 Prompt — `prompts/stage-2-screening/P3-kickoff-data-requests.md`

Two zones per [[library-artifact-bundle]]:

- **System prefix (cache-eligible)**: role (non-sponsored MM underwriting deal
  team preparing the post-NDA data ask), the Overland framework lens summary,
  the off-the-shelf constraint, the one-page ceiling, uncertainty handling
  (`[INSUFFICIENT DATA — <what is missing>]` if classification absent — do not
  guess sector KPIs), the output contract (populated `.docx`), and — because
  the artifact is outbound to the borrower/debt advisor — the inline redaction
  checklist line from [[restricted-content-discipline]] (the list must reveal
  no firm-internal economics, IC content, or portfolio context; a data ask
  inherently carries none, but the line is mandatory for external-facing
  prompts).
- **Variable inputs (per-invocation, semantic XML)**: `<teaser>`,
  `<email_color>`, `<desktop_research>`, `<pitchbook_excerpt>`,
  `<sector_classification>` (the frozen handoff: NAICS, GICS sector / industry
  group / industry / sub-industry — see `schemas/sector_screen_handoff.py`),
  `<system_date>`, `<fiscal_year_end>` (optional), `<existing_lender_status>`
  (optional), `<forecast_horizon>` (optional).

### 3.3 Project instruction — amend `project-instructions/stage-2-screening.md`

The stage-2 project instruction already exists (built in push-1 for the P4
pair). **Amend, do not duplicate** (one PI per stage): add the P3 Kick-Off
Data Requests row to the active-deliverables table mapping it to
`dl-ddq-kickoff`, and add to the Institutional Knowledge section an inline,
compile-dated embed of the downstream-pre-seeding rationale (the request →
downstream-field map) so the PI runs in Claude Desktop without filesystem
access.

### 3.4 Pydantic schema — `schemas/kickoff_data_request.py`

`KickoffDataRequest` (snake_case, JSON-serializable primitives, required vs.
optional explicit, one-line field descriptions, `schema_version: int = 1`,
HITL defaults `review_state: Literal["PENDING_REVIEW"]`,
`requires_human_review: bool = True`; module docstring names P3 / Foldspace
screening app / `_LAND` tier / `PENDING_REVIEW`). Fields:

- `company_name: str`
- `fiscal_year_end: str` (e.g., `"12-31"`; default calendar)
- `audited_range`, `ltm_anchor`, `quarterly_range`, `budget_fy`,
  `forecast_range: str` (the computed period strings)
- `naics_code: str`, `gics_sector/industry_group/industry/sub_industry: str`
- `compliance_cert_applicable: bool`
- `standard_requests: list[str]`
- `borrower_kpi_requests: list[KpiRequest]` where `KpiRequest` =
  `{ label: str, rationale: str, downstream_target: str }`
- watermark/HITL fields per the bundle pattern.

Cross-validate: every content-dict key the script consumes appears in the
schema and vice versa (no drift), per the bundle rule.

## 4. Deterministic period engine (`compute_periods.py`)

Inputs: `system_date`, optional `fiscal_year_end` (default `12-31`), optional
`history_years` (default **3** — the standard kick-off look-back per
[[screening-templates]]), optional `forecast_years` (default **5** — typical
model horizon; configurable, justified, not a voodoo constant).

Logic:

1. Apply a 30-day close buffer to `system_date`; the most recent *completed*
   fiscal quarter end on/before `(system_date − 30 days)` is the LTM anchor.
   Example: `2026-05-28 → 2026-04-28 → most recent FQE = 2026-03-31 →`
   LTM `3/26`, quarter `Q1'26`.
2. Last completed FY = the FY whose FYE precedes the anchor; audited range =
   `FY'(YY−history_years+1)–'(YY)` … i.e., last 3 FYs.
3. Quarterly internal-FS range and compliance-cert range = `FY'(YY−2) –
   Q[X]'(YY of anchor)`.
4. Budget FY = current (in-progress) FY; forecast range = budget FY →
   `+forecast_years`.
5. Honor non-calendar `fiscal_year_end` (label quarters off the borrower's
   fiscal calendar, not calendar quarters).

Output: a JSON dict of the exact placeholder-replacement strings. Errors
handled in-script (invalid date, malformed FYE → explicit message, no punt).

## 5. Population mechanic (`populate_kickoff.py`)

Mirrors `dl-memo-posting/scripts/populate_memo.py` discipline:

- Edit `assets/kickoff-data-requests-template.docx` **in place**; never
  regenerate (regeneration strips list numbering and styles).
- Substitute the bracket placeholders (`FY'[YY]`, `LTM [M/YY]`, `Q[X]'[YY]`,
  etc.) inside existing runs, preserving run/paragraph formatting.
- Insert standard "stock-cut" lines and the borrower-specific KPI lines as new
  list paragraphs under the correct header, cloning the existing list
  paragraph's `pPr` (numId 9 / `Bullet2` / `NumberList1`) so numbering and
  indentation are preserved.
- If `compliance_cert_applicable` is false, suffix the existing compliance-cert
  line with ` — N/A (no existing reporting facility)` rather than deleting it.
- Save a deal-named copy with a `vS` draft suffix:
  `<Company>_-_Wells_&_Overland_Kick-Off_Data_Requests_<MM-DD-YY>_vS.docx`.
- One-page enforcement: cap borrower-specific KPI lines at a configurable
  **`MAX_KPI_LINES = 14`** (justified: the template body + standard set + 14
  terse noun-phrase KPI lines fit one page at the template's styling; the value
  is documented, not magic) and emit a verbose error listing the overflow if
  exceeded so Claude can tighten before resending.

## 6. Watermark / HITL handling (D-2 carve-out, inherited from `dl-memo-posting`)

The kick-off list is an **outbound Word document**; injecting
`[DRAFT — HUMAN REVIEW REQUIRED]` body text would corrupt the artifact sent to
the borrower/debt advisor. Per the established `dl-memo-posting` carve-out, the
HITL signal is carried by (a) the `vS` draft filename suffix and (b) the
`PENDING_REVIEW` HITL state with `requires_human_review = true` recorded around
the artifact. At Arrakis graduation the watermark becomes a rendered review
banner outside the `.docx`. The reviewer must approve before the list is sent.

## 7. Anti-patterns to encode

- Do not request data that is not plausibly off-the-shelf (bespoke analyses
  belong in the later DD list, not the kick-off ask).
- Do not request quarterly granularity except where downstream-warranted (the
  databook `FinInputs` quarterly grid); annual is the default elsewhere.
- Never fabricate periods — all dates come from `compute_periods.py`.
- Never exceed one page; tighten KPI phrasing rather than spilling.
- Do not inject watermark text into the `.docx` body; do not regenerate the
  document.
- `[INSUFFICIENT DATA — sector classification not provided]` if no NAICS/GICS
  and no usable business description — do not guess the sector KPI set.

## 8. Evaluations (built before extensive docs, per best practices)

1. **Residential HVAC services roll-up, post-NDA** — the canonical few-shot;
   expects the full HVAC KPI block, add-on cohort + consideration requests,
   3-FY + Q1'26 periods from a 5/28/2026 system date.
2. **SaaS borrower, no existing debt, calendar FY** — compliance-cert line
   marked N/A; KPI block shifts to ARR/NRR/gross & net retention/CAC payback/
   logo concentration; no add-on cohort block.
3. **Industrials manufacturer, non-calendar FYE (3/31), existing BSL loan** —
   tests FYE-aware quarter labeling, compliance-cert line active, raw-material/
   commodity-exposure and backlog KPI cuts.

Each eval states expected period strings, expected standard set, and expected
KPI archetypes.

## 9. Build sequence (push-2 execution checkpoint)

1. Copy template into `skills/dl-ddq-kickoff/assets/` byte-identical from
   `raw/` (raw/ never modified).
2. Write `compute_periods.py`; self-test against the three eval system dates.
3. Write `populate_kickoff.py`; verify in-place styles/numbering preserved.
4. Write `reference/kpi-frameworks.md` and `reference/population-mechanics.md`.
5. Write `SKILL.md`; verify ≤500 lines, references one level deep, forward
   slashes, third-person description.
6. Write `schemas/kickoff_data_request.py`; cross-validate against the
   content-dict.
7. Write `prompts/stage-2-screening/P3-kickoff-data-requests.md`.
8. Amend `project-instructions/stage-2-screening.md` (P3 row + IK embed).
9. Run the three evaluations; record results in `docs/pilot-validation.md`
   (append a push-2 section).
10. Wiki UPDATE + LINT: add a `production-skills`/`library-design` page or
    extend the inventory to record `dl-ddq-kickoff`; reconcile `index.md`
    page count and `wiki/log.md`; update `progress.json` with a `push-2`
    checkpoint and a bundle entry.
11. Commit (`feat: dl-ddq-kickoff kick-off data-request bundle`) and
    `git push origin main` per CLAUDE.md rule 11 (artifact-coding checkpoint +
    wiki LINT both trigger the push).

## 10. Out of scope for push-2

- The downstream sector-classification skill/prompt that produces the NAICS/
  GICS handoff (consumed here as a given input; already partially served by
  `dl-sector-screen` / `sector_screen_handoff.py`).
- The later, broader DD list (`dl-ddq-initial` / `-followup` / `-gap`).
- A formal `dist/` build pipeline (manual self-containment verification only).
