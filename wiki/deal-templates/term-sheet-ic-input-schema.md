---
title: Term Sheet and IC Input Schema (P6–P11)
category: deal-templates
tags: [template, schema, governance, deal-lifecycle]
sources:
  - "[Company] - Wells & Overland DD List (MM-DD-YY) vTemplate.docx"
  - "[Company] - Overland IC Summary (MM-DD-YY) vTemplate.pptx"
  - "[Company] - Wells & Overland Term Sheet (MM-DD-YY) vTemplate.docx"
last_updated: 2026-05-15
---

# Term Sheet and IC Input Schema (P6–P11)

Per-template input composition for the [[term-sheet-and-ic-templates|P6–P11 decision/negotiation instruments]], expressed against [[template-input-schema]]. This cluster is the clearest proof of the canonical-object thesis: the IC summary and term sheet are two renderings of one **deal-terms core**.

## Wells & Overland DD List (.docx)

A request shell. Composes `deal_identity` (header) plus one template-specific bucket:

- `diligence_requests` — `[Initial]` / `[Follow-Up]` mode toggle driving one shell across P6 and P10, with a numbered Diligence-Questions section and a numbered Data-Requests section. The substantive taxonomy is entered per engagement; the template carries none.

## Overland IC Summary (.pptx)

The single-slide decision scorecard. Composes `deal_identity`, `meeting_decision` (meeting-type toggle Pre-Screen/Commitment, date, per-row deal-team recommendation, committee approval/recommended changes, next steps, focus areas), and a **condensed projection of the deal-terms core** — `facility_structure`, `commitment_maturity`, `amort_prepay`, `pricing`, `fees`, `ddtl_governor`, `financial_covenants`, `ltm_anchor` (opening leverage) — rendered as the terms grid rows (Amount & Facility, Commitment, Maturity, Call Protection, Coupon, Amortization, Fees, DDTL Governor, Financial Covenants). No template-specific economic bucket: every term cell is a `$ref`.

## Wells & Overland Term Sheet (.docx)

The externalized offer. Composes `deal_identity`, `parties` (proposal lenders, borrower/guarantors, collateral, admin agent), `facility_structure`, `sources_uses` (the Use-of-Proceeds line items only), `pricing`, `grids` (the leverage-tiered pricing grid + `[No Pricing Grid]` toggle), `fees`, `commitment_maturity`, `amort_prepay`, `ddtl_governor`, `financial_covenants`, `ltm_anchor`. Template-specific:

- `conditions_precedent` — the CP list, including the opening-leverage-not-to-exceed CP and pending-committee-approval reference.
- `covenant_selections` — affirmative/negative covenant "customary for transactions of this type" selections and the leverage-basis footnote / confidentiality disclaimer.

## The deal-terms core

The IC summary's terms column and the term sheet's deal-term sections are field-identical: `facility_structure + pricing + grids + fees + commitment_maturity + amort_prepay + ddtl_governor + financial_covenants + ltm_anchor`. Define that union once as `deal_terms_core`; the IC summary renders it as a scorecard with `meeting_decision`, the term sheet renders it as prose with `parties + conditions_precedent`. Both should be regenerable from the [[dd-workbook-input-schema|model + databook]] — the structural argument for a single deal-terms data product, and the reason the IC summary's manual rebuild is an [[ic-and-asset-mgmt-gaps|identified gap]]. Its `meeting_decision` and `fees`/`grids` content is RESTRICTED — see [[restricted-content-discipline]].

## Related Concepts

- [[template-input-schema]] — the canonical bucket library and `deal_terms_core`
- [[term-sheet-and-ic-templates]] — the structural description of the same instruments
- [[dd-workbook-input-schema]] — where `deal_terms_core` is authored
- [[closing-am-input-schema]] — where `deal_terms_core` becomes the monitoring baseline
- [[ic-and-asset-mgmt-gaps]] — the IC-summary rebuild gap this exposes

## Sources

- `[Company] - Wells & Overland Term Sheet (MM-DD-YY) vTemplate.docx`, deal-term sections
- `[Company] - Overland IC Summary (MM-DD-YY) vTemplate.pptx`, three-table slide
- `[Company] - Wells & Overland DD List (MM-DD-YY) vTemplate.docx`, two-section shell
