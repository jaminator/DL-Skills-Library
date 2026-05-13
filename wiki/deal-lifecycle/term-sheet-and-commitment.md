---
title: Term Sheet and Commitment (Stages 3–4)
category: deal-lifecycle
tags: [process, deal-lifecycle]
sources:
  - Overland_Deal_Lifecycle_Automation_051326_vJA.pdf
last_updated: 2026-05-13
---

# Term Sheet and Commitment (Stages 3–4)

Stages 3 and 4 cover **P5 Initial DDQ through P12 EL / Commit Papers** — the core deal execution engine where most underwriting effort lands. The teams expand here to include OL Underwriting, OL IC, and the company / owner counterparty in iterative DDQ cycles. The deck flags **eight pain points across these eight phases**, several of which compound (the IC-vote-tracking gap recurs across both pre-screen and commitment IC).

## Stage 3 — Term Sheet (P5 → P8)

### P5 Initial DDQ · P6 Initial DD · P7 Pre-Screen IC · P8 Term Sheet

**Teams.** WFSC · WF RMs · Company / Owner · OL Underwriting · OL IC.

**Tooling.** DealCloud · SharePoint · Excel / Word · Outlook / Teams · external VDRs (Datasite, etc.) · market intel (PitchBook, CapIQ, AlphaSense, BamSEC) · existing AI tools (Claude, Endex, BlueFlame).

**Pain points (4).**
- No DDQ item lifecycle tracker; status across iterations is ad hoc.
- Informal IC re-approvals via email when terms move beyond approved bandwidth.
- Term negotiation tracked ad hoc; no structured redline or version history.
- IC summary slide created post-meeting from memory; no real-time capture.

**Opportunities (3).**
- AI initial DD synthesis.
- Pre-screen IC pack auto-build.
- Term sheet auto-draft.

### What gets produced

- A populated **databook** (the structured analytical workspace).
- A **financial model** (versioned, but not yet locked).
- A **Pre-Screen IC memo** (the first deep-dive memo — much heavier than the P4 posting memo).
- A **term sheet** issued to the borrower.

The Pre-Screen IC memo is the natural follow-on build target after the [[posting-memo-friction]] pilot — it has the same generate-with-review shape but draws on substantially richer upstream context (full DD findings, model outputs, expert calls).

## Stage 4 — Commitment (P9 → P12)

### P9 Follow-Up DDQ · P10 Follow-Up DD · P11 Commitment IC · P12 EL / Commit Papers

**Teams.** WFSC · WF RMs · Company / Owner · OL Underwriting · OL IC.

**Tooling.** DealCloud · SharePoint · Excel / Word · Outlook / Teams · external VDRs · market intel · existing AI tools (Claude, Endex, BlueFlame, Read.ai).

**Pain points (4).**
- **No IC vote / approval system of record.** This is the most acute governance gap in the lifecycle — see [[ic-and-asset-mgmt-gaps]].
- No documentation for conditional leverage approvals with bandwidth.
- No automated extract of final terms from the executed credit agreement.
- No deal closing diligence platform; redline tracking is fully manual.

**Opportunities (3).**
- Follow-up DD AI summary.
- IC memo auto-build (Commitment IC scope).
- EL / DCP doc-gen.

### What gets produced

- A **Commitment IC memo** (the formal commitment package).
- An **IC decision** (post / no-post / conditional approval).
- An **Exclusivity Letter** or **Commitment Papers** (optional, but standard for many deals).

## Why the friction concentrates here

Stages 3–4 carry the most context per phase: the upstream artifacts (databook, model, expert call notes, prior memos, term-sheet redlines) compound, and there is no single system of record for any of them. The deck identifies this as the central place where the [[option-c-recommendation]] (Arrakis) makes the largest difference — a unified deal record (A1 Thumper), structured DD workflow (A4 Sardaukar), versioned model (A5 Mentat), and assembled IC memo (A6 Reverend Mother) eliminate the "build IC memo from memory" pattern.

## Build sequencing implication

The library's pilot (P4) is the smallest viable end-to-end vertical slice. The natural follow-on builds, in order of leverage:

1. **P11 Commitment IC memo** — same shape as P4, much richer context.
2. **P5–P10 DDQ tracker + DD synthesis** — extract-and-validate plus route-and-track combined.
3. **P8 term sheet draft** — generate-with-review with structured economics inputs.

Each follow-on follows the same construction pattern proven by the pilot.

## Related Concepts

- [[deal-lifecycle-overview]] — full-lifecycle map
- [[ic-and-asset-mgmt-gaps]] — the IC-vote-tracking gap that recurs
- [[posting-memo-friction]] — pilot phase context
- [[opportunity-register]] — automation themes

## Sources

- `Overland_Deal_Lifecycle_Automation_051326_vJA.pdf`, slides 04–06
