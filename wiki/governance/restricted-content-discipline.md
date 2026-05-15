---
title: RESTRICTED-Content Discipline
category: governance
tags: [governance, policy, process]
sources:
  - arrakis_blueprint_v2_3.md
  - deal_lifecycle_automation_051326_vJA.pdf
last_updated: 2026-05-13
---

# RESTRICTED-Content Discipline

Any artifact in this library that is intended for **co-lender or LP distribution** carries an explicit redaction obligation. The discipline is encoded as a checklist that appears inline in the prompt, and the obligation is verified by the reviewer at the [[hitl-state-machine]] gate.

## What is RESTRICTED

Per [[data-classification-tiers]], the RESTRICTED tier covers the four categories that **must never appear** in external-facing output:

1. **Fund-level economics above the co-lender tranche.** Fund waterfalls, GP economics, carried interest splits, and any figure that describes Centerbridge's fund-level position rather than the loan economics.
2. **IC deliberation content.** Discussion text from the IC, conditional approval reasoning, internal debate over structure or pricing.
3. **Individual IC votes.** Vote records, dissenters' positions, abstentions.
4. **firm-internal portfolio context.** Comparison to other CB credits, cross-strategy allocation discussion, exposure limits, sleeve composition.

What **is** permissible to share externally:

- The deal economics at the co-lender tranche level (commitment, pricing, structure).
- The credit thesis as it appears in the executed credit agreement and the externally-distributed memo.
- Aggregated portfolio statistics published in LP reporting (with their normal cadence and gating).
- Public-record information (filings, press releases, ratings).

## The redaction checklist line

Every external-facing prompt in this library contains a redaction checklist line in the system prefix, immediately before the structured output template. The canonical text:

```
REDACTION CHECKLIST — Before producing the output, verify that none of the
following appears: (a) fund-level economics above the co-lender tranche;
(b) IC deliberation content; (c) individual IC votes; (d) Centerbridge-
internal portfolio context. If any of these would appear in the output,
emit [INSUFFICIENT DATA — REDACTION REQUIRED] in that field and surface a
note to the reviewer instead of generating the content.
```

The checklist is **not a guarantee of redaction** — it is a forcing function for the model to surface a flag rather than silently leak. The HITL reviewer is the actual enforcement layer.

## What "external-facing" means here

External-facing artifacts include:

- Co-lender memos, co-lender DD response packs, syndication marketing materials.
- LP reports and quarterly portfolio commentary distributed to investors.
- Borrower portal content (post-close reporting calendars, amendment notices to borrowers).
- Documents handed to external counsel, advisors, or service providers under engagement letters.

Internal-facing artifacts (IC posting memo, IC commitment memo, internal committee minutes, portfolio risk reviews) do **not** carry the redaction checklist because they are explicitly RESTRICTED-permitted destinations. They still carry the `[DRAFT — HUMAN REVIEW REQUIRED]` watermark.

## Reviewer obligation

A reviewer of an external-facing draft must explicitly confirm the redaction checklist before approving. The override audit record (see [[hitl-state-machine]]) for an external-facing draft includes a Boolean `redaction_verified` field; rejection of an APPROVED transition without `redaction_verified = TRUE` is a platform-level enforcement.

## What this means for prompt construction

A prompt that produces an external-facing artifact:

1. Includes the redaction checklist line verbatim in the system prefix.
2. Names the intended consumer explicitly (`<consumer>co-lender</consumer>` or `<consumer>lp</consumer>`).
3. Sets the structured output's classification ceiling to CONFIDENTIAL (no RESTRICTED fields).
4. Uses `[INSUFFICIENT DATA — REDACTION REQUIRED]` for any field that would otherwise carry RESTRICTED content.

A prompt that produces an internal-facing artifact:

1. Omits the redaction checklist line.
2. Names the intended consumer (`<consumer>ic</consumer>`, `<consumer>asset-management</consumer>`, etc.).
3. May include RESTRICTED fields when the consumer is permitted to see them.

The discrimination between internal and external happens at the prompt level, not at the skill level. A single skill may be invoked for either consumer; the prompt embedded in the project instruction does the routing.

## Related Concepts

- [[data-classification-tiers]] — the tier scheme this discipline enforces
- [[hitl-state-machine]] — the review gate that verifies redaction
- [[spice-llm-service]] — Spice's audit trail records `redaction_verified`

## Sources

- `arrakis_blueprint_v2_3.md`, Section 5.5 (classification) and Section 7 (HITL review)
- `deal_lifecycle_automation_051326_vJA.pdf`, slide 09 (foundation controls)
