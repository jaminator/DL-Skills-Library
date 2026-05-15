# Project Instruction — Stage 2 Screening (P3–P4)

This document is the project-level instruction for any Claude Desktop project that supports a Stage 2 Screening workflow on a specific screened opportunity. It carries:

1. A deal-context slot to be filled at screening kick-off.
2. The active deliverables for the stage and the artifact-versioning convention.
3. Behavioral rules specific to the stage — including the **P4 posting-memo watermark carve-out**.
4. An **Institutional Knowledge** section embedded inline as compiled wiki content (compile date below). The reader does not need access to the underlying wiki to operate.

---

## Stage and purpose

**Stage:** 2 — Screening
**Phases:** P3 Kick-Off DDQ · P4 Posting Memo
**Purpose:** Take an NDA-gated opportunity through the kick-off data request and the first formal Investment Committee interaction. P4 produces the posting memo + backup that lands in the IC for a **post / no-post** decision. P4 is the **highest-yield single pain point in the lifecycle** — most opportunities are declined here, yet every one still carries the full memo-drafting cost, so the leverage is collapsing first-draft time without skipping the structured IC input.

---

## Deal-context slot (fill at screening kick-off)

Replace each placeholder before activating this project for a specific opportunity.

```
COMPANY:                  {{ legal entity name }}
GICS / SECTOR:            {{ industry classification + sub-vertical }}
SOURCING HANDOFF:         {{ originating dl-sector-screen verdict / cascade anchor, if applicable }}
LTM EBITDA (with source): {{ value }} as of {{ period }} per {{ CIM / QoE / model }}
INDICATIVE STRUCTURE:     {{ commitment ($), TL/RCF/DDTL, indicative pricing, leverage }}
DDQ STATUS:               {{ kick-off data request sent / responses in / gaps outstanding }}
ACTIVE DOCUMENT INDEX:    {{ list of currently-uploaded documents: CIM/CIP, QoE, kick-off DDQ responses, financials, sector screen, posting memo template, backup template ... }}
```

The deal-context slot is **required** before any artifact is produced inside this project. Skills and prompts read these values from project context.

---

## Active deliverables

| Phase | Deliverable | Cadence | Skill |
| --- | --- | --- | --- |
| P3 | Kick-off data requests — outbound `.docx` | Per opportunity entering screening (post-NDA) | `dl-ddq-kickoff` |
| P3 | Standardized data book | Per opportunity (heavy primary-materials pre-work) | (future skill — see watchpoint) |
| P4 | Posting memo — narrative `.docx` | Per screened opportunity | `dl-memo-posting` |
| P4 | Posting memo backup — quantitative `.xlsx` | Per screened opportunity (feeds the memo's financial exhibits) | `dl-memo-posting-backup` |

This stage now ships the **P3 kick-off data request** (`dl-ddq-kickoff`) and the **P4 pair** (`dl-memo-posting` + `dl-memo-posting-backup`). P3 runs first, immediately post-NDA: it sends the borrower/debt-advisor the narrow data ask whose returned data is the upstream feed for the P4 pair (and the later databook and model). The P4 pair is the narrative/quantitative split of a *single* deliverable — the `.xlsx` outputs flow one-to-one into the `.docx` financial exhibits. The P3 standardized-databook row remains a future placeholder.

**Documented fragmentation watchpoint.** If Stage 2 later gains the standardized-databook skill (joining `dl-ddq-kickoff` on the P3 side), split this file into `stage-2a-kickoff.md` + `stage-2b-posting-memo.md`. The databook deliverable carries heavy non-sponsored primary-materials ETL/data-cleaning pre-work — the fragmentation trigger (many phases × many deliverables × heavy per-deliverable sub-processes). Not split today: P3 currently has one lightweight skill (`dl-ddq-kickoff`, an outbound one-pager with no heavy pre-work) and P4 is a single deliverable pair, so the file stays cohesive.

---

## Artifact versioning

All artifacts produced inside this project follow the convention:

```
[COMPANY]-[DELIVERABLE]-v[N]-[YYYYMMDD]
```

Examples:
- `Acme-Posting-Memo-v1-20260515`
- `Acme-Posting-Memo-Backup-v2-20260518`

Increment `N` on every revision. The date is the operative LTM/period the financing is sized against, not the date of action. The posting-memo skill's own draft-state filename suffix (`vS` + the "Pending Overland IC Feedback" default) is preserved as the in-document draft signal — see Behavioral rule 1.

---

## Behavioral rules

1. **Watermark obligation and the `.docx` carve-out (D-2).** The posting memo is IC-facing and the kick-off data request is borrower/debt-advisor-facing, so the `[DRAFT — HUMAN REVIEW REQUIRED]` watermark obligation (CLAUDE.md rule 5) applies to both deliverables. **However, the watermark is NOT injected into the Word body.** `dl-memo-posting` and `dl-ddq-kickoff` populate their bundled Word templates *in place* via their scripts, preserving auto-numbering, list styling, and (for the kick-off) the two footnotes; injecting a banner into the `.docx` body would alter the proven production artifact — and the kick-off is sent to an external party, where a banner would be doubly inappropriate. The draft state is instead signalled by **(a)** the skills' existing `vS` draft-filename suffix, **(b)** for the posting memo, the "Pending Overland IC Feedback" default in the recommendation/next-steps section, and **(c)** the HITL `PENDING_REVIEW` state on the structured output. The watermark proper is applied at the HITL/PENDING_REVIEW layer (and becomes the rendered review banner in Arrakis), not in the Word body. The backup `.xlsx` likewise carries no injected banner — its draft state is the `PENDING_REVIEW` state on the extraction-summary schema.
2. **Never silently omit.** Use `[INSUFFICIENT DATA — <what is missing>]` (and the skills' own `TBD (source)` convention) for any required field the inputs do not support. Never fabricate; **blank ≠ zero** in the backup (zeros corrupt growth/CAGR formulas).
3. **CA EBITDA is the only EBITDA label** in the narrative — never "Adjusted" or "Diligence Adjusted." No posting-team follow-ups anywhere in the memo (it reports facts; it never assigns tasks or prescribes diligence). No speculation or conditional hedging — flag deviation magnitude and direction, not causes.
4. **Protect every formula in the backup.** The backup skill writes input cells only, behind a mandatory pre-write `is_formula` gate; detailed FinSum and Returns tabs are off-limits. Intentional formula modifications (M2, CAGR columns, K2-first date anchor) are logged as intentional in the extraction summary.
5. **Classification — and the P3 outbound exception.** The P4 posting memo and backup are internal deal-team / IC-facing (CONFIDENTIAL, possibly RESTRICTED if portfolio context is cited); they are not co-lender- or LP-facing, so that external redaction checklist does not apply to them. **The P3 kick-off data request is different: it is sent *out* to the borrower / debt advisor.** It must therefore carry no firm-internal economics, no IC deliberation content, no individual IC votes, and no other portfolio context — apply the outbound redaction checklist before it is sent. A pure data ask inherently contains none of that; the rule is to keep it that way (request only borrower data; never echo Overland return thresholds, designated criteria, or fund economics into the list).
6. **HITL state tagged.** Every structured output carries `review_state: "PENDING_REVIEW"`. The posting-team / IC reviewer is the only party that may transition state.
7. **Schema-validated outputs.** The kick-off structured output validates against `schemas/kickoff_data_request.py`; the narrative content validates against `schemas/posting_memo_content.py`; the backup extraction summary validates against `schemas/posting_memo_backup_extraction.py`. If a value cannot fit the schema, use `[INSUFFICIENT DATA]` rather than reshaping the schema.
8. **Apply the credit framework, do not cite it.** D&A, strengths, and considerations apply the base-rate evidence hierarchy; never fabricate industry base rates; never name academic/practitioner authors in memo output even when the analysis is sound.

---

## Institutional Knowledge

The embedded sections below are compiled content from the development environment. **Compile date: 2026-05-15.** A reader operating this project in Claude Desktop does not need access to the wiki — the relevant institutional knowledge for this stage is inlined here.

When the wiki is updated, this section is recompiled by the maintainer (next compile due when any embedded page's `last_updated` is newer than the date above).

### Embedded: origination-and-screening

*Compiled from `wiki/deal-lifecycle/origination-and-screening.md` — last updated 2026-05-13.*

**P3 Kick-Off DDQ.** Teams: WFSC · WF RMs · Company/Owner · OL Underwriting · OL IC. Tooling: DealCloud · SharePoint · Excel/Word · Outlook. Pain points: no DDQ item-lifecycle tracker (status across iterations is ad hoc); no central searchable repository for CIMs, QoEs, expert transcripts across CB. Opportunities: auto-DDQ generation · standardized data book.

**P4 Posting Memo.** Same teams/tooling. *Highest-yield single pain point in the lifecycle.* Pain points: posting-memo credit process consumes significant time with high rejection rate; no IC posting-meeting minutes (summary built post hoc from memory); kick-off DDQ pain points propagate into P4 because the memo inputs are the DDQ outputs. Opportunity: **AI posting memo draft** — the flagship Stage-2 opportunity and the recommended pilot for the initial library build. Stage 1–2 are the natural first-build targets: structured deliverables, bounded inputs, high repetition.

### Embedded: posting-memo-friction

*Compiled from `wiki/pain-points/posting-memo-friction.md` — last updated 2026-05-13.*

The posting memo is the first formal IC interaction for a screened opportunity. It pairs a **stoplight risk rating** (categorical Green/Amber/Red across business quality, financial profile, industry/market, sponsor-or-management, structure/leverage) and a **narrative credit memo** (company overview, transaction overview, credit highlights, credit risks, summary recommendation). It lands in the IC for a post / no-post decision; most opportunities end here.

Two flagged frictions: **(1)** "Posting memo credit process consumes significant time with high rejection rate" — a screening output rejected most of the time still carries the full drafting cost; the opportunity is to *collapse first-draft time*, not skip the memo. **(2)** "No IC posting meeting minutes; summary built post hoc from memory" — no real-time capture of IC reasoning; conditional approvals may not propagate, declined-deal pattern analysis is impossible, audit trail is weak. Friction 2 is downstream (an IC-meeting-capture / A7-class workflow); the library's P4 work targets friction 1. A good P4 draft validates against a Pydantic schema, carries the watermark obligation, marks gaps with `[INSUFFICIENT DATA — …]`, and ports cleanly into the Arrakis A6 Reverend Mother memo workflow.

### Embedded: posting-memo-automation

*Compiled from `wiki/production-skills/posting-memo-automation.md` — last updated 2026-05-15.*

The P4 deliverable is automated by a **coupled pair** split along the narrative/quantitative seam.

**`dl-memo-posting` (production: `overland-posting-memo`) — the narrative.** Populates the bundled Word template *in place* via `scripts/populate_memo.py`, preserving auto-numbering and run-level bold/italic — returns a populated `.docx`, not a regenerated document. Drafts twelve mapped sections (deal header, situation/company overview, financial headline, six-bullet D&A, sources-&-uses note, 15-item risk-flags grid, five strengths, five considerations, recommendation with color rating, designated criteria). Discipline: "CA EBITDA" is the only EBITDA label; no posting-team follow-ups anywhere; no speculation/conditional hedging; anchor to the operative LTM period, `TBD (source)` rather than fabricate; strengths ordered macro→micro; considerations framed for a senior secured lender.

**`dl-memo-posting-backup` (production: `populating-posting-memo-backup`) — the calc engine.** Extracts CIM/CIP financials with openpyxl into the `FinSum`/`SUCAP` tabs, **writing input cells only and protecting every formula** (mandatory pre-write `is_formula` gate; detailed FinSum and Returns tabs off-limits). Conventions: **K2-first date anchor** (K2 = last actual FYE, G2 = `EOMONTH(K2,−48)`, H–K cascade by formula, M2/CAGR modified only when projections/empty anchors require it and logged as intentional); **blank ≠ zero**; mandatory user gate before reading any CIM (close date, target cash, SOFR, cash taxes — asked in one message); bespoke-deal escalation (HoldCo/PIK/seller notes/preferred/earn-outs halt for confirmation).

**Shared Overland structuring policy** (reusable institutional knowledge): Overland RCF Funding Rule (funded RCF at close = Overland RCF commitment − CIM RCF commitment, increment deducted from CIM TL); DDTL Proactive Sizing (size to 20% of TL+DDTL even if the CIM omits a DDTL); owner-equity plug (F14 = total uses − funded debt); default tranche pricing; FCCR Tier 1/Tier 2 addback discipline (default strips all addbacks to reported EBITDA; override P12 to retain only genuine Tier 2 normalizations). **Why a pair, not one skill:** the memo is generate-with-review (prose judgment, watermark obligation); the backup is extract-and-validate (deterministic cell mapping under formula protection). Each carries the discipline its shape needs.

### Embedded: overland-credit-framework

*Compiled from `wiki/methodology/overland-credit-framework.md` — last updated 2026-05-15.*

The firm's first-principles analytical spine for non-sponsored MM underwriting; credit analysis begins with the micro drivers of free cash flow, not a leverage multiple relative to market convention.

**Credit quality screen.** Industry-level: genuine secular tailwinds (demographic/regulatory/technological/infrastructure, distinguished from cyclical recoveries); acyclical or only modestly cyclical demand; fragmented structure where the borrower is a larger regional/national provider vs. sub-regional and mom-and-pop operators, with credible strategic acquirers at scale as a "second way out." Company-level: demand-driver quality in strict priority (contractual recurring > reoccurring behavioral > non-discretionary break-fix; project/transactional/discretionary flagged); concentration discipline (caution >10% of revenue, material risk >20–25% absent protection); 2–3 yr revenue/GP/EBITDA trend; target margins (gross 30–40%+, EBITDA 12–20%+) with mean-reversion skepticism applied *above* the upper end too; limited capex/NWC intensity with **FCF — not EBITDA — modeled as the debt-service metric**; credit-accretive DDTL use case (strong roll-up pipeline = quality signal; unanchored accordion = risk).

**Base-rate evidence hierarchy** (governs D&A and considerations in the memo): any external benchmarking must be grounded in **Tier 1** public comps with observable metrics, **Tier 2** user-provided base rates, or **Tier 3** comp/precedent data embedded in the CIM/QoE. Absent all three, default to internal historical benchmarking — measure against the fullest available company history (including recessionary periods), flag step-changes, frame strictly relative to the company's own history with no invented external distribution. Fabricating or implying industry-level base-rate statistics is prohibited; "base rate"/"mean reversion" framing and any named author are barred from memo output even when the analysis is sound.

### Embedded: kick-off downstream-pre-seeding map

*Compiled from `wiki/deal-templates/screening-input-schema.md`, `wiki/deal-templates/dd-workbook-input-schema.md`, and `skills/dl-ddq-kickoff/reference/kpi-frameworks.md` — last updated 2026-05-15.*

The P3 kick-off ask is engineered so its returned data drops directly into the artifacts that follow it — that is *why* it is shaped the way it is. Each request has a named downstream consumer:

- **Quarterly internal IS/BS/CF** (computed range) → databook quarterly P&L driver grid (`fin_inputs`).
- **LTM income statement + bridge to consolidated EBITDA** → posting-memo backup LTM anchor and EBITDA build (`ltm_anchor`, `ebitda_build`).
- **Top-N customer / supplier concentration** → databook concentration tables; posting-memo Customers/Suppliers bullets and the Concentration risk flag.
- **Maintenance vs. growth capex split** → Overland model capex driver; posting-memo Capex D&A bullet.
- **NWC build (by FY and quarter)** → databook working-capital block (DSO/DIH/DPO/CCC).
- **Existing debt & debt-like items + earn-out/deferred schedule** → sources & uses, pro-forma cap, the payment-bomb screen.
- **Add-on cohort history + consideration structure** (buy-and-build) → DDTL governor sizing and the roll-up base-rate read.
- **Borrower-specific KPI block** → posting-memo Company Overview / D&A demand-driver characterization and the industry attractiveness read.

The kick-off itself populates only the `data_request_periods` bucket (it has no economics — it is what the lender *sends out*); it is the upstream feed for every downstream bucket. The borrower-specific KPI block is derived by reasoning from the NAICS/GICS classification through the Overland credit framework's demand-driver-quality, growth-quality, and operating-leverage dimensions, constrained to plausibly off-the-shelf metrics.

---

## Summary

This project supports the Stage 2 Screening workflow on a single screened opportunity. Fill the deal-context slot at kick-off. Run `dl-ddq-kickoff` first, immediately post-NDA, to send the borrower/debt-advisor the data ask; its returned data is the upstream feed for the `dl-memo-posting` + `dl-memo-posting-backup` P4 pair (the `.xlsx` feeds the `.docx` financial exhibits) and the later databook/model. The watermark obligation applies to the IC-facing memo and the outbound kick-off but is **not injected into the Word/Excel body** (D-2 carve-out, rule 1): draft state is the `vS` filename, the posting memo's "Pending Overland IC Feedback" default, and the HITL `PENDING_REVIEW` state. The P3 kick-off is outbound to an external party — apply the outbound redaction checklist (rule 5); the P4 outputs are internal and that checklist does not apply to them. Every output validates against its schema, uses `[INSUFFICIENT DATA]` rather than fabrication, applies the credit framework without citing it, and lands in `PENDING_REVIEW` for the human reviewer. The P3 standardized-databook deliverable remains a future placeholder with a recorded fragmentation watchpoint.
