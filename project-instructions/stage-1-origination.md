# Project Instruction — Stage 1 Origination (P1–P2)

This document is the project-level instruction for any Claude Desktop project that supports a Stage 1 Origination workflow — sourcing and NDA intake for non-sponsored US middle-market flow. It carries:

1. A deal-context slot to be filled at sourcing-cycle kick-off.
2. The active deliverables for the stage and the artifact-versioning convention.
3. Behavioral rules specific to the stage.
4. An **Institutional Knowledge** section embedded inline as compiled wiki content (compile date below). The reader does not need access to the underlying wiki to operate.

---

## Stage and purpose

**Stage:** 1 — Origination
**Phases:** P1 Deal Sourcing · P2 NDA Processing
**Purpose:** Convert raw thematic interest and inbound relationship flow into a screened, NDA-gated pipeline. Stage 1 is the funnel mouth: ~96% of inbound drops out before the first formal IC interaction (the 4% lead-to-close benchmark), so the leverage here is **lead enhancement**, not conversion. P1 sourcing is the deck's named binding constraint on the path to BDC-peer scale; automation at this stage is the revenue lever.

---

## Deal-context slot (fill at sourcing-cycle kick-off)

Replace each placeholder before activating this project for a specific sourcing effort or NDA cycle.

```
SOURCING THESIS / SECTOR SCOPE: {{ sector, industry, or thematic description being worked }}
RELATIONSHIP CHANNEL:          {{ WFSC / WF RM / owner-GC / advisory IB origin }}
PIPELINE SYSTEM STATE:         {{ DealCloud record id(s); Salesforce sync status }}
NAMED TARGETS (if any):        {{ companies already identified for borrower-ID }}
NDA STATUS:                    {{ none / requested / in Ontra / executed }}
ACTIVE DOCUMENT INDEX:         {{ list of currently-uploaded documents: teasers, PitchBook/Preqin/CapIQ pulls, sector notes, draft NDA ... }}
```

The deal-context slot is **required** before any artifact is produced inside this project. Skills and prompts read these values from project context.

---

## Active deliverables

| Phase | Deliverable | Cadence | Skill |
| --- | --- | --- | --- |
| P1 | Sector / sub-vertical sourcing screen + frozen `p2_borrower-identification` handoff | Per sector thesis worked | `dl-sector-screen` |
| P1 | Inbound teaser auto-parse & enrichment | Per teaser received | (future skill) |
| P1 | DealCloud / Salesforce lead sync | Per lead intake | (future skill) |
| P2 | NDA generation & execution routing | Per deal entering diligence | (future skill — route-and-track) |

This pass ships **P1 `dl-sector-screen`** only. The other rows are explicit placeholders so this instruction surfaces the full Stage 1 scope, not just the shipped skill. P2 NDA processing is a pure route-and-track workflow (Ontra execution today; Arrakis closes it with A2 Gom Jabbar) and has no skill yet.

---

## Artifact versioning

All artifacts produced inside this project follow the convention:

```
[COMPANY-OR-SECTOR]-[DELIVERABLE]-v[N]-[YYYYMMDD]
```

Examples:
- `OutsourcedFacilitiesSvcs-Sector-Screen-v1-20260515`
- `AcmeCo-NDA-v2-20260520`

Increment `N` on every revision. For a sourcing screen the date is the date the screen was worked; for a deal artifact it is the period being acted on.

---

## Behavioral rules

1. **Generate-with-review, not blanket watermark.** The `dl-sector-screen` output is an **internal sourcing handoff**, reviewed by the sourcing analyst before it feeds borrower identification. It is not IC-facing, legal, co-lender-facing, or AM-facing, so the `[DRAFT — HUMAN REVIEW REQUIRED]` watermark (CLAUDE.md rule 5) is **not** triggered for it. The draft signal is the HITL `PENDING_REVIEW` state plus the analyst-validation gate. If a Stage 1 project ever produces an IC-, legal-, co-lender-, or AM-facing artifact, that artifact **does** carry the watermark.
2. **Never silently omit.** Use the skill's existing `[unresolved: …]` / **Open Questions** marker for any factual gap. Never guess an unresolvable economic fact; never fabricate industry-level base-rate statistics.
3. **Freeze the downstream contract.** `dl-sector-screen` declares a frozen output schema so the unbuilt `p2_borrower-identification` skill can parse it. Section headers and the Pursue / Watch / Screened-Out taxonomy are stable — field names are not changed without a coordinated downstream update. This is enforced by `schemas/sector_screen_handoff.py`.
4. **Internal sourcing classification.** Stage 1 outputs are INTERNAL / CONFIDENTIAL sourcing intelligence. They are not co-lender- or LP-facing; the external redaction checklist does not apply here.
5. **HITL state tagged.** Every structured output carries `review_state: "PENDING_REVIEW"`. The sourcing analyst is the only party that may transition state.
6. **Schema-validated outputs.** The sourcing-screen handoff must validate against `schemas/sector_screen_handoff.py`. If a value cannot fit the schema, use the uncertainty marker rather than reshaping the schema.
7. **Apply the credit framework, do not cite it.** Verdicts cite the attractiveness-screen categories by name in the structured field only; narrative is analyst-grade prose with no "Porter" / "five forces" / "base rate" framing and no named academic authors.

---

## Institutional Knowledge

The four wiki pages below are embedded as compiled content from the development environment. **Compile date: 2026-05-15.** A reader operating this project in Claude Desktop does not need access to the wiki — the relevant institutional knowledge for this stage is inlined here.

When the wiki is updated, this section is recompiled by the maintainer (next compile due when any embedded page's `last_updated` is newer than the date above).

### Embedded: origination-and-screening

*Compiled from `wiki/deal-lifecycle/origination-and-screening.md` — last updated 2026-05-13.*

Stages 1–2 cover **P1 Deal Sourcing through P4 Posting Memo** — the funnel from raw lead to first formal IC interaction, where ~96% of inbound drops out.

**P1 Deal Sourcing.** Teams: WFSC · WF Relationship Managers · Company Owners/GCs · PE Sponsors · M&A/Debt-Advisory IBs. Tooling: Salesforce (WFSC) · DealCloud (direct-lending instance) · Confi Manager · PitchBook · Preqin · CapIQ · Outlook · SharePoint. Pain points: Salesforce→DealCloud sync is nightly-batch only (system trail lags email); inbound screening fully manual (no auto teaser parse/enrichment); WF RM learning curve produces inconsistent behavior; DealCloud and Confi Manager require dual entry. Opportunities: AI teaser auto-parse · DealCloud/SF auto-sync · auto-NDA generation. P1 lead enhancement is the **revenue lever** — the deck identifies P1 sourcing as the binding constraint on the path to 225 portfolio companies.

**P2 NDA Processing.** Same teams as P1; NDA execution routes through Ontra; deal entered into DealCloud. Pure **route-and-track** — no acute P2-unique pain beyond the upstream dual-entry issue and the absence of a CLM integrated with the deal-pipeline gate. Arrakis closes this with A2 Gom Jabbar, which natively gates downstream deal access on NDA execution.

**Why Stage 1–2 is the natural starting point:** structured deliverables (knowable output schema), bounded inputs (one or two source docs per phase), high repetition (~1,000+ leads/yr by 2030 — small per-deal savings compound).

### Embedded: growth-gap

*Compiled from `wiki/economics/growth-gap.md` — last updated 2026-05-13.*

The Growth Gap is the difference between the firm's status-quo trajectory and the diversification target needed to reach BDC-peer scale by YE 2030: portfolio companies 110 → 225 (+115); cumulative funded AUM $8.3B → $16.9B; 5-year cumulative fee revenue $425M → $710M (**+$285M**). At today's ~16 closes/yr the firm reaches ~110 names; the target needs ~47 closes/yr — roughly a **3× lift in qualified lead volume**.

**Binding constraint: supply, not conversion.** The firm already converts at the 4% peer benchmark; the throughput problem is upstream. The lead-enhancement lever is **P1 sourcing automation** — proprietary screens on NAICS, PitchBook, Preqin, CapIQ to mine non-sponsored flow from the WF relationship network. This is a step-change in lead *enhancement*, not a parallel lead-generation function. The fee delta is back-loaded (2028–2030 carry most of the value as the close ramp compounds). Load-bearing assumption: the ramp embeds a +2.44× lift over the 4% baseline; P1 ships H2 2026; uplift is unmeasured until ~6 months of production data — flagged as re-mark-required.

### Embedded: sector-research-screener

*Compiled from `wiki/production-skills/sector-research-screener.md` — last updated 2026-05-15.*

`dl-sector-screen` (deployed in production as `ol-industry-screener`) is the P1 sourcing skill. Given a sector/industry/thematic description it decomposes the space into 4–10 discrete sub-verticals (anchored to NAICS 4-digit groupings where economics permit), screens each against the Overland industry attractiveness framework, and emits a structured markdown handoff for downstream borrower identification.

Fixed nine-step workflow: (1) disambiguate scope — over-broad inputs get one clarifying question, a single named company is redirected to borrower-ID/posting work; (2) load the bundled attractiveness screen; (3) decompose into sub-verticals; (4) score each → **Pursue** (clears materially, viable Tier 2 population), **Watch** (clears most, flagged risks), or **Screened Out** (fails materially / no Tier 2 addressability) — rationale cites screen categories by name, web/PitchBook validates rather than scoring from training data; (5–8) for Pursue/Watch name 3–5 tier-mixed cascade anchors, map NAICS, identify trade orgs & conferences (publicly-available exhibitor lists flagged as high-yield), draft a 1–2 sentence Tier 2 thesis; (9) edge cases — oligopolies with no Tier 2 population screened out, concentrated sub-verticals get a scope caveat, unresolvable gaps go under Open Questions.

**Defining design property: a frozen output schema.** Headers and the Pursue/Watch/Screened-Out taxonomy are stable because an unbuilt `p2_borrower-identification` skill is specified to parse them. It is a **generate-with-review** shape — the analyst validates verdicts and anchors before the handoff feeds sourcing.

### Embedded: overland-credit-framework

*Compiled from `wiki/methodology/overland-credit-framework.md` — last updated 2026-05-15.*

The firm's first-principles analytical spine for non-sponsored MM underwriting. Credit analysis begins with the micro drivers of free cash flow, not a leverage multiple relative to market convention — Porter for industry structure, Mauboussin for company-level behavior and base-rate discipline.

**Industry attractiveness screen (the sourcing-side projection used by `dl-sector-screen`):** eight Porter-derived FCF signals (high entry barriers; non-discretionary/mission-critical demand; fragmented low-power buyers with switching friction; low supplier power; low substitution risk; rational pricing; low capex intensity / high FCF conversion; secular non-GDP demand drivers) plus a "Goldilocks" semi-fragmented structure (national HHI ~600–1,500, local operator concentration). The operative model is the **three-tier competitive structure**: Tier 1 national consolidators (the "second way out" acquirers), Tier 2 regional incumbents ($5–50M EBITDA — the Overland borrower), Tier 3 owner-operator tail (competitive set + tuck-in pipeline). Local fragmentation is explicitly *not* pricing risk — switching friction, service-reliability premium, compliance documentation, and relationship tenure suppress price-led churn. Genuine secular tailwinds are distinguished from cyclical recoveries. Fabricating or implying industry-level base-rate statistics is prohibited; "base rate"/"mean reversion" framing and any named academic author are barred from narrative output even when the analysis is sound.

---

## Summary

This project supports the Stage 1 Origination workflow for a sourcing thesis or NDA cycle. Fill the deal-context slot at kick-off. Use `dl-sector-screen` for P1 sourcing decomposition; the frozen `p2_borrower-identification` contract must not drift. Outputs are internal sourcing intelligence, validated against the schema, marked with `[unresolved: …]` rather than fabrication, and landing in `PENDING_REVIEW` for the sourcing analyst. The full Stage 1 scope (teaser parse, lead sync, NDA routing) is surfaced above as future placeholders.
