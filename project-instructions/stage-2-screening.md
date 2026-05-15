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
| P3 | Kick-off DDQ / data request generation | Per opportunity entering screening | (future skill) |
| P3 | Standardized data book | Per opportunity (heavy primary-materials pre-work) | (future skill — see watchpoint) |
| P4 | Posting memo — narrative `.docx` | Per screened opportunity | `dl-memo-posting` |
| P4 | Posting memo backup — quantitative `.xlsx` | Per screened opportunity (feeds the memo's financial exhibits) | `dl-memo-posting-backup` |

This pass ships the **P4 pair** (`dl-memo-posting` + `dl-memo-posting-backup`). They are the narrative/quantitative split of a *single* deliverable, not two independent deliverables — the `.xlsx` outputs flow one-to-one into the `.docx` financial exhibits. P3 rows are explicit future placeholders.

**Documented fragmentation watchpoint.** If Stage 2 later gains both the P3 auto-DDQ skill *and* the standardized-databook skill, split this file into `stage-2a-kickoff-ddq.md` + `stage-2b-posting-memo.md`. The databook deliverable carries heavy non-sponsored primary-materials ETL/data-cleaning pre-work — the fragmentation trigger (many phases × many deliverables × heavy per-deliverable sub-processes). Not split today because P3 has no skill yet and P4 is a single deliverable pair.

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

1. **Watermark obligation and the P4 `.docx` carve-out.** The posting memo is IC-facing, so the `[DRAFT — HUMAN REVIEW REQUIRED]` watermark obligation (CLAUDE.md rule 5) applies to the deliverable. **However, the watermark is NOT injected into the Word body.** `dl-memo-posting` populates the bundled Word template *in place* via its script, preserving auto-numbering and run-level formatting; injecting a banner into the `.docx` body would alter the proven production artifact. The draft state is instead signalled by **(a)** the skill's existing `vS` draft-filename suffix, **(b)** the "Pending Overland IC Feedback" default in the recommendation/next-steps section, and **(c)** the HITL `PENDING_REVIEW` state on the structured output. The watermark proper is applied at the HITL/PENDING_REVIEW layer (and becomes the rendered review banner in Arrakis), not in the Word body. The backup `.xlsx` likewise carries no injected banner — its draft state is the `PENDING_REVIEW` state on the extraction-summary schema.
2. **Never silently omit.** Use `[INSUFFICIENT DATA — <what is missing>]` (and the skills' own `TBD (source)` convention) for any required field the inputs do not support. Never fabricate; **blank ≠ zero** in the backup (zeros corrupt growth/CAGR formulas).
3. **CA EBITDA is the only EBITDA label** in the narrative — never "Adjusted" or "Diligence Adjusted." No posting-team follow-ups anywhere in the memo (it reports facts; it never assigns tasks or prescribes diligence). No speculation or conditional hedging — flag deviation magnitude and direction, not causes.
4. **Protect every formula in the backup.** The backup skill writes input cells only, behind a mandatory pre-write `is_formula` gate; detailed FinSum and Returns tabs are off-limits. Intentional formula modifications (M2, CAGR columns, K2-first date anchor) are logged as intentional in the extraction summary.
5. **Internal / CONFIDENTIAL classification.** Posting-stage outputs are deal-team and IC facing. They are not co-lender- or LP-facing; the external redaction checklist does not apply at this stage.
6. **HITL state tagged.** Every structured output carries `review_state: "PENDING_REVIEW"`. The posting-team / IC reviewer is the only party that may transition state.
7. **Schema-validated outputs.** The narrative content validates against `schemas/posting_memo_content.py`; the backup extraction summary validates against `schemas/posting_memo_backup_extraction.py`. If a value cannot fit the schema, use `[INSUFFICIENT DATA]` rather than reshaping the schema.
8. **Apply the credit framework, do not cite it.** D&A, strengths, and considerations apply the base-rate evidence hierarchy; never fabricate industry base rates; never name academic/practitioner authors in memo output even when the analysis is sound.

---

## Institutional Knowledge

The four wiki pages below are embedded as compiled content from the development environment. **Compile date: 2026-05-15.** A reader operating this project in Claude Desktop does not need access to the wiki — the relevant institutional knowledge for this stage is inlined here.

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

---

## Summary

This project supports the Stage 2 Screening workflow on a single screened opportunity. Fill the deal-context slot at kick-off. Use the `dl-memo-posting` + `dl-memo-posting-backup` pair for P4 — the `.xlsx` feeds the `.docx` financial exhibits. The watermark obligation applies to the IC-facing memo but is **not injected into the Word/Excel body** (carve-out, rule 1): draft state is the `vS` filename, the "Pending Overland IC Feedback" default, and the HITL `PENDING_REVIEW` state. Every output validates against its schema, uses `[INSUFFICIENT DATA]` rather than fabrication, applies the credit framework without citing it, and lands in `PENDING_REVIEW` for the posting-team / IC reviewer. P3 deliverables are surfaced above as future placeholders with a recorded fragmentation watchpoint.
