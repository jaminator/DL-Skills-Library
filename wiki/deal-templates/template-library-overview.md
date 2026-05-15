---
title: Deal Template Library Overview
category: deal-templates
tags: [template, process, deal-lifecycle]
sources:
  - "[Company] - Wells & Overland Kick-Off Data Requests (MM-DD-YY) vTemplate.docx"
  - "[Company] - Overland Posting Memo (MM-DD-YY) vTemplate.docx"
  - "[Company] - Overland Model (MM-DD-YY) vTemplate.xlsx"
  - "[Company] - Wells & Overland Term Sheet (MM-DD-YY) vTemplate.docx"
  - "[Company] - Overland Closing Memo (MM-DD-YY) vTemplate.docx"
  - "[Company] - Compliance Certificate Tracker_vTemplate.xlsx"
  - "Overland Form Credit and Guaranty Agreement.docx"
last_updated: 2026-05-15
---

# Deal Template Library Overview

The firm maintains a set of standardized, blank "vTemplate" working documents — one cluster per deal-lifecycle stage — that carry an opportunity from first data request through portfolio monitoring. Each template is co-branded either **Wells & Overland** (joint co-lender / partner-bank documents shared externally with Wells Fargo) or **Overland** (firm-internal artifacts). This page is the gateway to the per-stage detail pages and to the construction patterns that recur across the set.

## The dependency chain

The templates are not independent forms; they are a pipeline where each artifact's output is the next one's input:

1. **Intake** — [[screening-templates]]: a kick-off data request collects raw financials; a backup workbook computes the analytics; the posting memo wraps them in a stoplight-rated IC recommendation; the screening deck (plus a slim sponsor addendum for revised LBO asks) takes a "continue" decision to the pre-screen IC.
2. **Analysis** — [[dd-analytical-workbooks]]: a databook normalizes target financials, a single-sheet model projects credit/leverage/coverage, comps anchor valuation, a refi-payback analysis justifies the economics.
3. **Decision & negotiation** — [[term-sheet-and-ic-templates]]: a joint diligence list scopes DD, the one-page IC summary captures the committee decision, the Wells & Overland indicative term sheet externalizes the agreed economics to the borrower.
4. **Closing & monitoring** — [[closing-and-am-templates]]: the closing memo is the underwriting-to-AM hand-off; the compliance-certificate tracker and DDTL draw calc are the recurring monitoring controls; the amendment memo is the post-close governance wrapper.

Two documents are institutional **precedent**, not per-deal fill-ins: the [[form-credit-agreement]] (the covenant source of truth) and the [[market-deal-terms-reference]] (market benchmarking for term negotiation).

## Recurring construction patterns

- **Backup workbook ↔ memo pairing.** Every narrative IC memo has a paired Excel "Backup" whose sheets mirror the memo's exhibits one-to-one (posting-memo backup ↔ posting memo; closing-memo backup ↔ closing memo). The memo is the human-readable wrapper; the workbook is the calc engine.
- **Single covenant source of truth.** The form credit agreement's financial-covenant article and EBITDA/Fixed-Charges defined-term chain is the definition baseline the closing memo digests, the compliance tracker tests against, the DDTL calc reuses, and the amendment memo revises. This is the structural backbone of the [[compliance-certificate-parser-pilot]].
- **Version conventions.** `vTemplate` marks a blank form; the posting memo carries a `vS` (pre-IC) / `vF` (post-IC, replaces the IC summary) dual-version convention; the screening memo spawns a delta-only sponsor addendum rather than a full re-issue.
- **Market-data plumbing.** Workbooks embed S&P Capital IQ and FactSet add-ins; the `.xlsm` files carry no macros — the extension exists only to host data-refresh plumbing.

## Why this matters for the library

These templates are the concrete realization of the deal lifecycle in [[deal-lifecycle-overview]]. They define the knowable output schemas that make each phase a viable automation target (see [[opportunity-shapes]]): the posting memo and IC summary are generate-with-review, the trackers and draw calc are extract-and-validate. Several externally distributed templates carry RESTRICTED content (IC deliberation, fund economics, pricing grids) and inherit the [[restricted-content-discipline]] redaction obligation.

## Related Concepts

- [[screening-templates]] — P3–P4 intake and posting cluster
- [[dd-analytical-workbooks]] — P6 analytical core
- [[term-sheet-and-ic-templates]] — P6–P11 decision and negotiation instruments
- [[closing-and-am-templates]] — P16–P19 closing and monitoring cluster
- [[form-credit-agreement]] — the covenant source of truth
- [[deal-lifecycle-overview]] — the lifecycle these templates instantiate

## Sources

- `[Company] - Wells & Overland Kick-Off Data Requests (MM-DD-YY) vTemplate.docx` and the full `raw/` template set
- `Overland Form Credit and Guaranty Agreement.docx`
