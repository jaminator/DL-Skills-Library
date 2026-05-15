---
title: Screening Templates (P3–P4)
category: deal-templates
tags: [template, process, deal-lifecycle]
sources:
  - "[Company] - Wells & Overland Kick-Off Data Requests (MM-DD-YY) vTemplate.docx"
  - "[Company] - Posting Memo Backup (MM-DD-YY) vTemplate.xlsx"
  - "[Company] - Overland Posting Memo (MM-DD-YY) vTemplate.docx"
  - "[Company] - Overland Screening Memo (MM-DD-YY) vTemplate.pptx"
  - "[Company] - Overland Screening Memo [Sponsor Addendum] (MM-DD-YY) vTemplate.pptx"
last_updated: 2026-05-15
---

# Screening Templates (P3–P4)

This cluster covers the Stage 2 screening front end — from the first structured data ask through the pre-screen IC deck. It is the highest-frequency, highest-friction stretch of the lifecycle (see [[posting-memo-friction]]) and the natural generate-with-review automation target.

## The five artifacts in dependency order

**Kick-Off Data Requests (P3, .docx).** A deliberately narrow Wells & Overland request list — historical financials, historical KPIs if available, and forecast/budget — sent to the company or sponsor immediately after NDA. It has no inputs to populate (it is what the lender *sends out*); its returned data is the upstream feed for everything below. A broader [[term-sheet-and-ic-templates|diligence list]] handles later DD phases.

**Posting Memo Backup (P4, .xlsx).** The calc engine behind the posting memo. Key sheets: `SUCAP` (sources & uses, opening FCCR build, pro forma capitalization with tranche pricing/OID/call protection), `FinSum` (historical financial summary with CAGR and margins), `Detailed FinSum` (MD&A working calcs — DSO/DIH/DPO/CCC), and `Returns` (unlevered/levered MOIC/IRR with a back-leverage advance-rate matrix). Inputs: kick-off financial returns, proposed transaction terms, the SOFR curve, QoE adjustments. Outputs flow one-to-one into the posting memo's financial exhibits.

**Posting Memo (P4, .docx).** The stoplight-rated new-deal memo presented to the Posting IC for a pass / continue-diligence decision. Structure: deal header block, situation and company overview, historical financial summary, discussion & analysis (M&A vs organic, gross profit, CA EBITDA & adjustments, capex, NWC/CCC), illustrative sources & uses / pro forma cap, a credit-criteria risk matrix (concentration, cyclicality, seasonality, capex, regulatory, ESG, etc. with RR/SA scoring), and posting ratings. It carries the `vS` (pre-IC) / `vF` (post-IC) dual-version convention — the `vF` version explicitly substitutes for a separate IC summary after the meeting. Inputs: kick-off returns, CIM, the backup workbook. A "continue" decision seeds the screening memo and the formal initial DDQ/DD; the recorded IC focus areas become the diligence agenda.

**Screening Memo (P4→P7, .pptx).** The full ~40-slide IC deck built after the Posting IC for pre-screen feedback: executive/transaction summary with a sponsor-vs-Overland terms grid, company & industry overview, investment highlights/risks & mitigants, financial summary with an EBITDA-adjustment bridge, four projection cases, a second-way-out / distressed-sale-value analysis, management bios, a third-party diligence status grid, and appendices (public comps, precedent transactions, prior IC memos).

**Screening Memo Sponsor Addendum (.pptx).** A delta-only deck — only the slides a sponsor's revised LBO financing ask changes (refreshed sources & uses, EBITDA, projection cases, distressed sensitivity). Read with its parent, never standalone.

## Inputs, outputs, downstream

The cluster consumes NDA-gated company financials and a CIM; it produces a stoplight rating and an IC decision. Downstream, its outputs feed the [[dd-analytical-workbooks]] (the screening cases carry into the databook and model) and the [[term-sheet-and-ic-templates|IC summary and term sheet]]. The screening deck is RESTRICTED for any external audience (it contains the sponsor-vs-firm terms comparison and IC feedback request).

## Related Concepts

- [[posting-memo-friction]] — the P4 pain point this cluster instantiates
- [[dd-analytical-workbooks]] — the next stage that consumes screening outputs
- [[template-library-overview]] — the full template chain
- [[screening-input-schema]] — the per-template input-bucket composition for this cluster
- [[origination-and-screening]] — the lifecycle stages these templates serve
- [[opportunity-shapes]] — the generate-with-review shape these memos take

## Sources

- `[Company] - Overland Posting Memo (MM-DD-YY) vTemplate.docx`, header + posting-ratings sections
- `[Company] - Posting Memo Backup (MM-DD-YY) vTemplate.xlsx`, SUCAP / FinSum / Returns sheets
- `[Company] - Overland Screening Memo (MM-DD-YY) vTemplate.pptx`, section deck
