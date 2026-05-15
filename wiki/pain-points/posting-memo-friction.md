---
title: Posting Memo Friction (P4)
category: pain-points
tags: [pain-point, process, opportunity]
sources:
  - deal_lifecycle_automation_051326_vJA.pdf
last_updated: 2026-05-13
---

# Posting Memo Friction (P4)

The **P4 Posting Memo** phase is the highest-yield single pain point in the deal lifecycle. The deck flags two specific frictions that make P4 the recommended pilot for the initial library build.

## What P4 produces

The posting memo is the first formal Investment Committee interaction for a screened opportunity. It pairs:

- A **stoplight risk rating** — a categorical assessment (typically Green / Amber / Red across a fixed set of dimensions: business quality, financial profile, industry / market, sponsor or management, structure / leverage).
- A **narrative credit memo** — a structured prose document covering company overview, transaction overview, credit highlights, credit risks, and a summary recommendation.

The memo lands in the IC for a **post / no-post** decision. Most opportunities end here — the deck describes the rejection rate at this stage as high.

## The two flagged frictions

### 1. "Posting memo credit process consumes significant time with high rejection rate."

The asymmetry is the issue: a screening output that gets rejected most of the time still carries the full memo-drafting cost. Underwriters spend hours building a memo for a deal that the IC then declines in minutes. The opportunity is to **collapse first-draft time** so the rejection cost falls — not to skip the memo entirely (the IC needs the structured input) but to shrink the underwriter time per memo materially.

### 2. "No IC posting meeting minutes; summary built post hoc from memory."

After the post / no-post decision, no system captures the IC's reasoning in real time. The summary is reconstructed afterward from memory, which means:

- Conditional approvals or post-decision comments may not be propagated reliably to the underwriting team.
- Pattern analysis across declined deals is impossible — there is no searchable record of why deals got declined at posting.
- Audit trail is weak.

This second friction is downstream of the posting memo itself — addressing it requires capture inside the IC meeting, which is closer to an A7 Landsraad-class workflow. The library's pilot focuses on the **first** friction; the second is recorded here for follow-on iteration.

## Why this is the right pilot phase

P4 has three properties that make it ideal as the first end-to-end vertical slice:

1. **Two distinct output shapes in one phase.** The stoplight rating is structured (extract / classify / rate); the credit memo is narrative (generate-with-review). Building one skill that handles both exercises both pattern types in [[opportunity-register]].
2. **Bounded upstream context.** The memo draws from the CIM, the kick-off DDQ output, and any external screen (NAICS, PitchBook, CapIQ). This is a manageable RAG envelope for a first build — much smaller than a full DD-driven IC memo.
3. **High repetition.** Posting memos are the most-frequently drafted memo in the lifecycle (every screened deal gets one). Even small per-memo time savings aggregate quickly.

A successful P4 pilot also exercises the [[hitl-state-machine]] explicitly: the stoplight rating routes to a reviewer who confirms each rated dimension, and the memo body lands in the same review queue with the `[DRAFT — HUMAN REVIEW REQUIRED]` watermark.

## What "good" looks like

A well-constructed P4 pilot produces a draft that:

- Validates against a Pydantic schema (stoplight rating + structured memo sections).
- Carries the `[DRAFT — HUMAN REVIEW REQUIRED]` watermark.
- Marks data gaps explicitly with `[INSUFFICIENT DATA — <what is missing>]`.
- Ports cleanly into the Arrakis A6 Reverend Mother memo-drafting workflow without rewriting the prompt or the schema.

## Related Concepts

- [[pain-point-register]] — full friction map
- [[origination-and-screening]] — Stage 2 detail
- [[opportunity-register]] — automation responses
- [[opportunity-shapes]] — generate-with-review, the shape a P4 build would exercise
- [[compliance-certificate-parser-pilot]] — the first pilot built (P17, extract-and-validate); P4 is the recommended next build using the same [[library-artifact-bundle]]
- [[posting-memo-automation]] — the deployed production skill pair that attacks this friction in Claude Desktop today
- [[hitl-state-machine]] — review gating
- [[ic-and-asset-mgmt-gaps]] — IC minutes gap (downstream sibling friction)

## Sources

- `deal_lifecycle_automation_051326_vJA.pdf`, slides 05, 06
