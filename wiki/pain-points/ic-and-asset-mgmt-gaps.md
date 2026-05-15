---
title: IC and Asset Management Gaps
category: pain-points
tags: [pain-point, governance, process]
sources:
  - deal_lifecycle_automation_051326_vJA.pdf
last_updated: 2026-05-13
---

# IC and Asset Management Gaps

Two of the deck's three highest-acuity pain-point clusters are **the Investment Committee process** (P7 Pre-Screen IC, P11 Commitment IC) and **Asset Management** (P17–P19). Both are governance gaps as much as workflow gaps — the deck flags several of them as audit and regulatory exposures today, not just operational inconveniences.

## The IC gaps

### No IC vote / approval system of record

There is no system that records who voted, when, and on what. Decisions live in meeting outputs, email confirmations, and post-hoc summaries. The deck calls this out as an audit and regulatory exposure that compounds as the book scales.

### No IC posting meeting minutes; summary built post hoc from memory

Even at the lighter-weight P4 posting IC, no real-time minutes are captured. The summary is reconstructed after the fact, which means conditional comments and rationale may be lost.

### No documentation for conditional leverage approvals with bandwidth

When the IC approves a deal with conditions (e.g., "approved up to 5.5× total leverage; require re-approval if structure moves above"), the conditional bandwidth is not formally documented. Re-approvals when terms move outside the bandwidth happen informally over email.

### Informal IC re-approvals via email

A direct consequence of the previous gap. There is no system gate between IC approval and fund release, which the deck frames as audit and regulatory exposure.

### IC summary slide created post meeting and ad hoc from memory

The same friction as the posting IC: summary deck built after the fact rather than captured live.

## The Asset Management gaps

### Chronograph not fully utilized as source of truth

Chronograph is the intended portfolio system of record, but the upstream-to-Chronograph data pipe is incomplete. Monitoring features go unused; the source-of-truth pattern degrades.

### Manual Excel mark-to-market valuations

Mark-to-market is done in Excel. The deck flags this against the broader industry direction (Apollo's commitment to daily NAV marks) as a place where SEC scrutiny is increasing. Manual marks are also less defensible in audit.

### Compliance certificates frequently contain CFO arithmetic errors; OL catches manually

Compliance certs come in with errors that the AM team catches by hand. There is no automated parser, no schema validation, no comparison against the credit agreement's specific definitions. This is the most acute extract-and-validate target in Asset Management.

### DDTL draws approved over email; no compliance verification tracked

Delayed-draw term loan draws are approved informally. The deck flags this as a governance gap: draws are conditional (no default or EoD, pro forma leverage within covenant, permitted use of proceeds) but those conditions are not enforced at funding.

### Inconsistent UW to AM handoff at close; databook may not reach Chronograph

The transition between underwriting and asset management is not consistently structured. The databook — the canonical analytical workspace built during DD — may not propagate to Chronograph, which means AM starts cold on the deal it inherits.

## Root cause: governance lacks instrumentation

These pain points share a single underlying shape: **the workflow exists, but no system holds the audit trail**. The IC meets and decides; AM monitors and reports. But neither the decision nor the monitoring is captured in a queryable form. The deck explicitly frames this as a foundation-control gap that exists independent of the [[growth-gap]] — the controls are required at any portfolio size (30, 110, or 225 names) and become more acute as the book scales.

The Arrakis response splits these gaps across three apps:

- **A7 Landsraad** captures IC deliberations: real-time annotation, sealed pre-meeting voting, append-only decision audit trail, automated minutes generation.
- **A12 Corrino** automates portfolio monitoring: covenant calculations, financial statement ingestion, compliance certificate parsing, early-warning risk scoring.
- **A13 Melange** formalizes valuation: stage-gate fair-value workflow, roll-forward automation, IPEV / ASC 820 compliance framework.

See [[application-directory]].

## What this means for the library

The IC and AM gaps are the **second-highest-leverage** library targets after the [[posting-memo-friction]] pilot, because:

1. They affect every deal and every reporting period (not just the screening funnel).
2. The output shapes are well-defined (IC minutes, compliance certificate validation report, mark-to-market triage).
3. The Pydantic schemas are tight (vote records, covenant calculations, fair-value entries).

The pilot's success pattern transfers directly into these phases.

## Related Concepts

- [[pain-point-register]] — full friction map
- [[term-sheet-and-commitment]] — Stage 3–4 detail
- [[closing-and-asset-management]] — Stage 5–6 detail
- [[foundation-controls]] — the governance investments these gaps drive
- [[application-directory]] — the Arrakis apps that close these gaps

## Sources

- `deal_lifecycle_automation_051326_vJA.pdf`, slides 05, 09
