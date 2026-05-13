---
title: Pain Point Register
category: pain-points
tags: [pain-point, process]
sources:
  - Overland_Deal_Lifecycle_Automation_051326_vJA.pdf
last_updated: 2026-05-13
---

# Pain Point Register

The deal lifecycle deck identifies **23 pain points** distributed across all six stages. Friction concentrates in **P4 Posting Memo, the IC process (P7 / P11), and Asset Management (P17–P19)**. Most pain points trace to one of three root causes: manual workflows, system-of-record gaps, or dual-entry across DealCloud, Confi Manager, and Chronograph.

## Friction by stage

### Stage 1 — Origination (P1–P2)

- Salesforce-to-DealCloud sync is nightly batch only — leads arrive over email, system trails do not.
- All inbound screening is manual; no automated teaser parse or enrichment at intake.
- WFSC relationship managers are still climbing a learning curve, producing inconsistent lending and process behavior.
- DealCloud and Confi Manager require dual entry on overlapping fields.

### Stage 2 — Screening (P3–P4)

- **Posting memo credit process consumes significant time with high rejection rate.** This is the highest-yield single pain point in the lifecycle. See [[posting-memo-friction]].
- No IC posting meeting minutes; the post-meeting summary is built post hoc from memory.
- No central searchable repository for CIMs, QoEs, and expert transcripts across CB.

### Stage 3 — Term Sheet (P5–P8)

- No DDQ item lifecycle tracker — status across iterations is ad hoc.
- Informal IC re-approvals happen via email when terms move beyond the approved bandwidth.
- Term negotiation is tracked ad hoc with no structured redline or version history.
- IC summary slides are created post-meeting from memory; no real-time capture.

### Stage 4 — Commitment (P9–P12)

- No IC vote / approval system of record. See [[ic-and-asset-mgmt-gaps]].
- No documentation for conditional leverage approvals with bandwidth.
- No automated extract of final terms from the executed credit agreement.
- No deal closing diligence platform; redline tracking is fully manual.

### Stage 5 — Closing (P13–P16)

- Commitment book is tracked in ad hoc Excel; no syndication management system.
- WF inexperience with DDTL / direct lending pushes administrative burden onto Overland.
- No closing checklist tracking; KYC repository is fully manual.
- Inconsistent UW-to-AM handoff at close — the databook may not reach Chronograph.

### Stage 6 — Asset Management (P17–P19)

- Chronograph is not fully utilized as the source of truth; monitoring features go unused.
- Mark-to-market valuations are manual Excel.
- Compliance certificates frequently contain CFO arithmetic errors that Overland catches manually.
- DDTL draws are approved over email; no compliance verification is tracked.

## Gap typology

The deck classifies each pain point as a **technology gap** (system missing or under-used) or a **process gap** (workflow not codified). Most P4 / IC / AM friction is process-and-technology compound — the workflow exists but is not instrumented, and no system holds the audit trail.

## Why this matters for the library

Pain points dictate the order in which skills and prompts are built. The pilot phase selection (see [[option-c-recommendation]] and the project's pilot decision) prioritizes a phase where the friction is acute, the deliverable is structured, and the upstream inputs are reasonably scoped — which is why **P4 Posting Memo** is the recommended pilot. Any future build phase should start by re-reading the pain points for that phase before drafting the skill.

## Related Concepts

- [[posting-memo-friction]] — P4 acute case
- [[ic-and-asset-mgmt-gaps]] — IC and AM gaps
- [[opportunity-register]] — the automation responses
- [[deal-lifecycle-overview]] — the spine these pains map onto

## Sources

- `Overland_Deal_Lifecycle_Automation_051326_vJA.pdf`, slide 05
