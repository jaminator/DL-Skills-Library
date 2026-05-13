---
title: Opportunity Register
category: opportunities
tags: [opportunity, process]
sources:
  - Overland_Deal_Lifecycle_Automation_051326_vJA.pdf
last_updated: 2026-05-13
---

# Opportunity Register

The deal lifecycle deck identifies **roughly 19 automation opportunities** across the 6-stage lifecycle. They fall into three repeating shapes: **extract-and-validate** (intake side), **generate-with-review** (memo and IC side), and **route-and-track** (workflow / handoff side).

## Opportunities by stage

### Stage 1 — Origination

- AI teaser auto-parse — extract structured deal facts from inbound teasers.
- DealCloud / Salesforce auto-sync — close the nightly-batch lag.
- Auto-NDA generation — feed Gom Jabbar's auto-extraction loop.

### Stage 2 — Screening

- Auto-DDQ generation — first-pass DDQ from a parsed teaser and CIM.
- AI posting memo draft — the flagship Stage-2 opportunity; ties directly to [[posting-memo-friction]].
- Standardized data book — push extraction into a single canonical structure.

### Stage 3 — Term Sheet

- AI initial DD synthesis — compile DD findings into structured form.
- Pre-screen IC pack auto-build — assemble the IC pack from upstream artifacts.
- Term sheet auto-draft — populate the term sheet from agreed economics.

### Stage 4 — Commitment

- Follow-up DD AI summary — close gaps surfaced at pre-screen IC.
- IC memo auto-build — the Stage-4 sibling of the posting-memo opportunity, with deeper diligence inputs.
- EL / DCP doc-gen — automate exclusivity / commit-papers issuance.

### Stage 5 — Closing

- Syndication CRM auto — relationship-aware syndication tracker.
- Credit agreement redline AI — automated clause comparison vs. precedent.
- Closing memo auto-gen — populate the closing memo from upstream artifacts and executed terms.

### Stage 6 — Asset Management

- Chronograph auto-feed — close the upstream-to-Chronograph data gap.
- AI valuation triage — first-pass mark-to-market with human review.
- Amendment doc workflow — structured tracking and document generation for amendments.
- AM distribution-list auto-route — route post-close output to the right AM destinations.

## Three recurring shapes

Every opportunity above resolves to one of three skill / prompt patterns. This taxonomy guides how to think about a new build:

| Shape | What it does | Typical phases | Example |
| --- | --- | --- | --- |
| **Extract-and-validate** | Parse a document, extract structured facts, validate against a Pydantic schema, flag gaps. | P1, P2, P3, P5, P9, P14, P17 | Teaser parse, CIM extract, compliance certificate parse |
| **Generate-with-review** | Generate a draft (memo, narrative, response) from upstream structured inputs, surface to a human reviewer with a HITL banner. | P4, P7, P10, P11, P12, P16, P18 | Posting memo, IC memo, closing memo, LP commentary |
| **Route-and-track** | Maintain a workflow state machine and route artifacts to the right team or system at the right time. | P2, P5, P9, P13, P15, P19 | NDA workflow, DDQ tracker, closing checklist, amendment workflow |

The pilot build always uses one of these three shapes. The pilot phase recommendation (P4 Posting Memo) is **generate-with-review** — see [[posting-memo-friction]].

## Why three shapes matters

The shape determines the artifact set:

- Extract-and-validate skills are dominated by the **Pydantic schema** plus a focused extraction prompt with explicit `[INSUFFICIENT DATA]` handling.
- Generate-with-review skills are dominated by the **prompt** with cache-eligible system prefix, structured upstream inputs in XML tags, and a `[DRAFT — HUMAN REVIEW REQUIRED]` watermark.
- Route-and-track skills are dominated by the **project instruction** that pins state across multiple deal-lifecycle steps.

The portability rule (see [[hitl-state-machine]]) applies to all three: the same artifacts map directly into Arrakis Spice + the per-app HITL state machine without rewriting.

## Related Concepts

- [[pain-point-register]] — the friction these opportunities answer
- [[posting-memo-friction]] — flagship Stage-2 opportunity
- [[hitl-state-machine]] — review gating that every generate-with-review uses
- [[deal-lifecycle-overview]] — the spine

## Sources

- `Overland_Deal_Lifecycle_Automation_051326_vJA.pdf`, slide 06
