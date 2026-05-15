---
name: dl-ddq-kickoff
description: >
  Populates the Wells & Overland Kick-Off Data Requests one-pager (.docx)
  directly from preliminary post-NDA borrower information (teaser, Wells
  Fargo / company email color, post-NDA desktop research, PitchBook, and the
  NAICS/GICS sector classification), returning the populated template ready
  for the deal team to send to the company or debt advisor. Use when the user
  has cleared an NDA and asks to prepare, draft, or send the kick-off data
  request / initial data ask / kick-off DDQ for a screened opportunity ("send
  the kick-off list," "draft the data request," "prepare the P3 ask"). It
  computes the FY / LTM / quarter / budget / forecast periods deterministically,
  emits the standard financial and stock-cut request set, and derives a
  borrower-specific KPI block by reasoning from the sector classification
  through the Overland credit framework. Output is the bundled template edited
  in place via scripts/populate_kickoff.py — not a regenerated Word document.
---

# Kick-Off Data Requests — Population Guide

## STEP 0 — ORIENTATION

The deliverable is the **populated bundled `.docx`**, not a text draft and not
a regenerated document. `scripts/populate_kickoff.py` edits
`assets/kickoff-data-requests-template.docx` in place (preserving the
`NumberList1` numbering, the `Bullet2` list styling, and the two footnotes) and
saves a deal-named copy.

It is a deliberately narrow request sent days after the NDA, before any analyst
time is committed. Two hard rules govern everything below:

- **One page, always.** The template is a one-pager by design. Tighten phrasing
  rather than spilling to a second page; the script enforces a hard cap on the
  borrower-specific block.
- **Off-the-shelf only.** Request only data a competent management team in this
  industry already tracks and can export from existing systems. Anything that
  requires the company to *build* an analysis belongs in the later DD list, not
  here.

Uncertainty discipline: never fabricate a period or a sector KPI set. Use
`TBD` for a missing input that does not block the request, and
`[INSUFFICIENT DATA — <what is missing>]` when a required input is absent
(specifically: emit `[INSUFFICIENT DATA — sector classification not provided]`
for the borrower-specific block if there is no NAICS/GICS and no usable
business description — do not guess the sector KPIs).

Reference files (load as needed; one level deep):

- [`reference/kpi-frameworks.md`](reference/kpi-frameworks.md) — the
  framework→request-archetype map, the downstream-pre-seeding rationale, and
  the worked sector library (HVAC canonical few-shot + contrasts). Read before
  drafting the Step 3 block.
- [`reference/population-mechanics.md`](reference/population-mechanics.md) —
  the content-dict schema pointer, the run snippet, the placeholder-
  substitution contract, the list-injection rules, and the one-page check.
  Follow exactly in Step 4.

Workflow checklist (copy into your working response and check off):

```
Kick-Off Data Request Progress:
- [ ] Step 1: Compute periods (run scripts/compute_periods.py)
- [ ] Step 2: Assemble the standard request set + stock cuts
- [ ] Step 3: Derive the borrower-specific KPI block (framework-grounded)
- [ ] Step 4: Build the content dict and run scripts/populate_kickoff.py
- [ ] Verify: one page, periods correct, footnotes intact; return the .docx
```

## STEP 1 — PERIOD MATH (run the script; do not compute dates by hand)

Run the period engine with the system date and any borrower fiscal-calendar
overrides:

```bash
python scripts/compute_periods.py --system-date YYYY-MM-DD \
    [--fiscal-year-end MM-DD] [--history-years 3] [--forecast-years 5]
```

- `--system-date` — the date the request is being prepared (required).
- `--fiscal-year-end` — the borrower's FYE as `MM-DD`; default `12-31`. Set
  this whenever the borrower is on a non-calendar fiscal year; the engine then
  labels quarters off the borrower's fiscal calendar, not calendar quarters.
- `--history-years` — audited look-back; default **3** (the standard kick-off
  look-back).
- `--forecast-years` — long-range forecast horizon; default **5**.

Capture the JSON it prints and pass it through verbatim as
`content["periods"]`. The engine applies a 30-day close buffer so it never
requests a quarter the borrower has not yet closed. Do not edit the fragment
strings — they are the single source of truth for every period in the document.

## STEP 2 — STANDARD REQUEST SET + STOCK CUTS (deterministic)

The seven standard lines are already in the template; the script rewrites them
from the period fragments. They are always present:

1. `{audited_range}` Audited Financial Statements (last 3 FYs by default)
2. LTM `{ltm_anchor}` Income Statement & Bridge to Consolidated EBITDA
3. `{quarterly_range}` Quarterly Internal Financial Statements (IS / BS / CF)
4. `{quarterly_range}` Quarterly Existing Loan Reporting & Compliance
   Certificates
5. `{quarterly_range}` Quarterly Mgmt. KPI's
6. `{budget_fy}` Budgeted Financial Statements
7. `{forecast_range}` Long-Term Financial Statement Forecast

**Compliance-certificate line (#4).** Set `compliance_cert_applicable`:

- `true` only if the borrower has an existing commercial-bank or
  direct-lending facility and reports regularly under it. The line keeps its
  `(If Applicable)` qualifier.
- `false` otherwise (e.g., founder-owned with no funded debt, or a sponsor
  add-on with no existing reporting facility). The script suffixes the line
  ` — N/A (no existing reporting facility)`. **The line is never deleted** —
  marking it N/A documents that the absence was considered, not overlooked.

**Stock cuts (every borrower, regardless of sector)** — passed in
`stock_cut_requests`, inserted as bullets under Historical KPIs:

- Top-1 / Top-10 customer concentration (revenue %, by FY)
- Top-1 / Top-10 supplier concentration (spend %, by FY)
- Maintenance vs. growth capex split (by FY)
- Net working capital build (by FY and by quarter)
- Existing debt & debt-like items remaining post-close, with go-forward cash
  payouts (the earn-out / deferred-consideration "payment-bomb" screen)

**Buy-and-build only — add two more stock cuts** when the borrower is a
roll-up / platform doing add-on acquisitions:

- Add-on acquisition history (LTM revenue & EBITDA at close vs. current, by
  cohort) — feeds the roll-up base-rate read
- Add-on consideration structure (upfront cash, seller / deferred notes,
  earn-outs, rollover equity) — informs the DDTL governor

## STEP 3 — BORROWER-SPECIFIC KPI BLOCK (framework-grounded judgment)

Read [`reference/kpi-frameworks.md`](reference/kpi-frameworks.md) first. Then
reason from the NAICS/GICS classification and the business description through
the Overland credit framework to derive the KPI requests a management team in
this industry tracks in the normal course:

1. Name the dominant demand model in one sentence (contractual recurring /
   reoccurring behavioral / non-discretionary break-fix / project / hybrid).
2. Walk the demand-driver-quality, growth-quality, and operating-leverage
   dimensions and write the borrower-specific lines that follow for that demand
   model — terse noun phrases, each an off-the-shelf metric.
3. Layer any sector-specific concentration or risk cut the framework flags
   material (payor mix, program re-compete, raw-material exposure, etc.).
4. Apply the off-the-shelf test to every line. If management would have to
   build it rather than export it, cut it or defer it to the later DD list.

These lines are passed in `borrower_kpi_requests`. The worked sector library in
the reference file gives the canonical residential-HVAC few-shot and contrasting
SaaS / industrials / healthcare sketches — match the closest demand model and
adapt; do not copy a sketch that does not fit the borrower's model.

## STEP 4 — POPULATE THE TEMPLATE

Follow [`reference/population-mechanics.md`](reference/population-mechanics.md)
exactly: build the content dict (schema is the docstring at the top of
`scripts/populate_kickoff.py`, mirrored by `schemas/kickoff_data_request.py`),
write it to JSON, run `scripts/populate_kickoff.py <content.json> <output.docx>`,
and return the populated `.docx` via `present_files`. Name the output
`<Company>_-_Wells_&_Overland_Kick-Off_Data_Requests_<MM-DD-YY>_vS.docx`.

Verify before returning: the document is one page; the periods match the engine
output; both footnotes are intact; the compliance line is present (qualified or
N/A, never missing).

## Anti-patterns

These collect the prohibitions enforced above for at-a-glance visibility — no
new behavior.

- **Do not compute or fabricate periods by hand.** Every date comes from
  `scripts/compute_periods.py`. Never invent a quarter or shift a fiscal label.
- **Do not request data that is not plausibly off-the-shelf.** Bespoke analyses
  belong in the later DD list, not the kick-off ask.
- **Do not request quarterly granularity except where downstream-warranted**
  (the databook quarterly grid). Annual is the default elsewhere.
- **Never exceed one page.** Tighten KPI phrasing and merge related cuts rather
  than spilling; do not raise the script's `MAX_KPI_LINES` cap.
- **Do not delete the compliance-certificate line.** Mark it N/A when there is
  no existing reporting facility; never remove it.
- **Do not regenerate the Word document or inject a watermark banner into the
  `.docx` body.** It is an outbound borrower-facing artifact; the template is
  edited in place. The draft signal is the `vS` filename, not body text.
- **Do not guess the sector KPI set.** Emit
  `[INSUFFICIENT DATA — sector classification not provided]` for the
  borrower-specific block if the classification and business description are
  both absent.
- **Outbound-document discipline.** The list reveals no firm-internal economics,
  IC deliberation content, individual IC votes, or portfolio context. A data
  ask inherently carries none; keep it that way — request only borrower data.

## Degrees of freedom

Period math and template population are **low freedom** — fragile and
consistency-critical, so they are scripted and Claude does not vary them. The
standard set and stock cuts are **deterministic**. The borrower-specific KPI
block is **high freedom** — context-dependent judgment grounded in the
framework map and worked examples. This split matches the Skills
best-practices guidance on matching specificity to task fragility.

## Notes on portability into Arrakis

This skill is the Stage 2 / P3 Kick-Off Data Requests deliverable. It maps into
the Arrakis Foldspace screening application (the same app as the P4 posting-memo
pair) as the kick-off data-request generator. `scripts/compute_periods.py` and
`scripts/populate_kickoff.py` carry through unchanged;
`schemas/kickoff_data_request.py` `KickoffDataRequest` is the Arrakis-side
structured-output contract and the screening landing-tier data-product schema.
At graduation the prompt is invoked through Spice and the structured content
lands in the screening application's `_LAND` tier; no rewrite of the skill body
is required.

**Watermark obligation (D-2 carve-out, inherited from `dl-memo-posting`).** The
kick-off list is an outbound Word document sent to the borrower / debt advisor;
injecting a `[DRAFT — HUMAN REVIEW REQUIRED]` banner into the `.docx` body would
corrupt the artifact. The HITL signal is instead the `vS` draft filename suffix
plus the `PENDING_REVIEW` state with `requires_human_review = true` recorded
around the artifact. At Arrakis graduation the watermark becomes a rendered
review banner outside the `.docx`. A human reviewer must approve before the
list is sent.
