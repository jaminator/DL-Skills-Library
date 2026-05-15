---
title: Screening Input Schema (P3–P4)
category: deal-templates
tags: [template, schema, deal-lifecycle]
sources:
  - "[Company] - Wells & Overland Kick-Off Data Requests (MM-DD-YY) vTemplate.docx"
  - "[Company] - Posting Memo Backup (MM-DD-YY) vTemplate.xlsx"
  - "[Company] - Overland Posting Memo (MM-DD-YY) vTemplate.docx"
  - "[Company] - Overland Screening Memo (MM-DD-YY) vTemplate.pptx"
  - "[Company] - Overland Screening Memo [Sponsor Addendum] (MM-DD-YY) vTemplate.pptx"
last_updated: 2026-05-15
---

# Screening Input Schema (P3–P4)

Per-template input composition for the [[screening-templates|P3–P4 screening cluster]], expressed against the canonical buckets in [[template-input-schema]]. Bucket ids are `$ref`s into that library; *template-specific* buckets are net-new and listed inline.

## Kick-Off Data Requests (.docx)

This template *sends out* — it has no economics to populate. Composes only `deal_identity` (company name) plus one template-specific bucket:

- `data_request_periods` — the FY / LTM / quarter / budget / forecast period placeholders the request enumerates.

It is the upstream feed: its returned data populates the buckets below.

## Posting Memo Backup (.xlsx)

The calc engine. Composes `deal_identity`, `sources_uses`, `facility_structure`, `pricing`, `fees`, `financial_covenants` (opening FCCR build), `ltm_anchor`, `ebitda_build`, `historical_financials`, `working_capital`, `pro_forma_cap`, `returns`. Template-specific:

- `backleverage_matrix` — Overland advance-rate / SNL grid driving the levered-returns block (a `returns` extension).

## Posting Memo (.docx)

The IC-facing wrapper. Composes `deal_identity`, `parties` (deal team, ownership/process), `ltm_anchor`, `historical_financials`, `sources_uses`, `pro_forma_cap`, `risk_rating` (the credit-criteria RR/SA matrix), `narrative_blocks`, `meeting_decision` (posting-committee rating + rater + next steps). Template-specific:

- `version_state` — the `vS` (pre-IC) / `vF` (post-IC, replaces IC summary) dual-version flag.

Most numeric buckets are *by-reference* to the backup, not re-entered — the memo carries narrative and the rating, the workbook carries math.

## Screening Memo (.pptx)

The ~40-slide IC deck. Composes the widest screening set: `deal_identity`, `parties`, `facility_structure`, `pricing`, `grids`, `fees`, `amort_prepay`, `ddtl_governor`, `financial_covenants`, `ebitda_build`, `ltm_anchor`, `historical_financials`, `working_capital`, `projection_cases` (four cases), `comparable_set`, `returns`, `narrative_blocks`. Template-specific:

- `terms_comparison` — the sponsor-vs-Overland side-by-side terms grid (two parallel instances of the deal-terms core, one per proposing side).

## Screening Memo Sponsor Addendum (.pptx)

A `modification_delta` pattern over the parent deck — only the buckets a revised LBO ask changes: `facility_structure`, `pricing`, `fees`, `sources_uses`, `projection_cases`, and the distressed-sale-value slice of `narrative_blocks`. Carries no standalone schema; it inherits the parent's and overrides the delta.

## The shared spine

`deal_identity`, `ltm_anchor`, `ebitda_build`, `historical_financials`, and `working_capital` are entered once (the backup) and *referenced* by every other artifact in the cluster. This single-source property is why P4 is a [[posting-memo-friction|high-yield generate-with-review target]]: regenerate the memo and deck from the populated backup rather than re-keying.

## Related Concepts

- [[template-input-schema]] — the canonical bucket library these `$ref`
- [[screening-templates]] — the structural description of the same cluster
- [[dd-workbook-input-schema]] — the next cluster the screening cases feed
- [[posting-memo-friction]] — the friction the shared spine removes

## Sources

- `[Company] - Posting Memo Backup (MM-DD-YY) vTemplate.xlsx`, SUCAP / FinSum / Returns
- `[Company] - Overland Screening Memo (MM-DD-YY) vTemplate.pptx`, section deck
- `[Company] - Wells & Overland Kick-Off Data Requests (MM-DD-YY) vTemplate.docx`
