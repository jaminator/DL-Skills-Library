---
title: Origination and Screening (Stages 1–2)
category: deal-lifecycle
tags: [process, deal-lifecycle]
sources:
  - Overland_Deal_Lifecycle_Automation_051326_vJA.pdf
last_updated: 2026-05-13
---

# Origination and Screening (Stages 1–2)

Stages 1 and 2 cover **P1 Deal Sourcing through P4 Posting Memo** — the funnel from raw lead to the first formal IC interaction. This is where ~96% of inbound flow drops out (the 4% lead-to-close conversion benchmark). For the library, these phases are heavy on **extract-and-validate** and the first **generate-with-review** patterns; see [[opportunity-register]].

## Stage 1 — Origination

### P1 Deal Sourcing

**Teams.** WFSC · WF Relationship Managers · Company Owners / GCs · PE Sponsors · M&A / Debt Advisory IBs.

**Tooling.** Salesforce (WFSC) · DealCloud (Overland) · Confi Manager · PitchBook · Preqin · CapIQ · Outlook · SharePoint.

**Pain points.**
- Salesforce-to-DealCloud sync is nightly batch only — leads arrive over email and the system trail lags.
- Inbound screening is fully manual; no auto teaser parse or enrichment at intake.
- WF RM learning curve produces inconsistent lending and process behavior.
- DealCloud and Confi Manager require dual entry on overlapping fields.

**Opportunities.** AI teaser auto-parse · DealCloud / SF auto-sync · auto-NDA generation. The lead-enhancement opportunity here is the **revenue lever** in [[growth-gap]]; the deck identifies P1 sourcing as the binding constraint on the path to 225 portfolio companies.

### P2 NDA Processing

**Teams.** Same as P1.

**Tooling.** Same as P1; NDA execution today routes through Ontra; deal entered into DealCloud.

**Pattern.** Pure **route-and-track**. The deck flags no acute pain point unique to P2 beyond the upstream dual-entry issue and the gap that no commercial CLM (Ironclad, DocuSign CLM) integrates with the deal-pipeline gate. Arrakis closes this with [[application-directory]] entry **A2 Gom Jabbar**, which natively gates downstream deal access on NDA execution.

## Stage 2 — Screening

### P3 Kick-Off DDQ

**Teams.** WFSC · WF RMs · Company / Owner · OL Underwriting · OL IC.

**Tooling.** DealCloud · SharePoint · Excel / Word · Outlook.

**Pain points.**
- No DDQ item lifecycle tracker — status across iterations is ad hoc.
- No central searchable repository for CIMs, QoEs, and expert transcripts across CB.

**Opportunities.** Auto-DDQ generation · standardized data book.

### P4 Posting Memo

**Teams.** WFSC · WF RMs · Company / Owner · OL Underwriting · OL IC.

**Tooling.** DealCloud · SharePoint · Excel / Word · Outlook.

**Pain points.** *This is the highest-yield single pain point in the lifecycle — see [[posting-memo-friction]]:*

- **Posting memo credit process consumes significant time with high rejection rate.**
- No IC posting meeting minutes; the post-meeting summary is built post hoc from memory.
- Subsumed: the kick-off DDQ pain points propagate into P4 because the inputs to the memo are the DDQ outputs.

**Opportunities.** **AI posting memo draft** — the flagship Stage-2 opportunity. This is the recommended pilot for the initial library build.

## Why these phases are the natural starting point

The Stage 1–2 phases share three properties that make them efficient first-build targets:

1. **Structured deliverables.** A teaser, a parsed CIM, a stoplight rating, a posting memo — each has a knowable output schema.
2. **Bounded inputs.** The artifact set per phase is small (one or two source docs).
3. **High repetition.** The volume of leads (~1,000+ per year by 2030) means even small per-deal time savings compound.

Stage 3+ phases run on much larger upstream context (full DD findings, executed financial models, expert call transcripts) and are heavier RAG-style problems that benefit from being built second.

## Related Concepts

- [[deal-lifecycle-overview]] — full-lifecycle map
- [[posting-memo-friction]] — P4 detail
- [[opportunity-register]] — automation themes
- [[growth-gap]] — why P1 is the revenue lever

## Sources

- `Overland_Deal_Lifecycle_Automation_051326_vJA.pdf`, slides 04–06
