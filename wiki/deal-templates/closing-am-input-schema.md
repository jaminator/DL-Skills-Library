---
title: Closing and AM Input Schema (P16–P19)
category: deal-templates
tags: [template, schema, governance, risk]
sources:
  - "[Company] - Overland Closing Memo (MM-DD-YY) vTemplate.docx"
  - "[Company] - Closing Memo Backup (MM-DD-YY) vTemplate.xlsx"
  - "[Company] - Overland Amendment Memo (MM-DD-YY) vTemplate.docx"
  - "[Company] - Compliance Certificate Tracker_vTemplate.xlsx"
  - "[Company] - DDTL Draw Calc (MM-DD-YY) vTemplate.xlsx"
last_updated: 2026-05-15
---

# Closing and AM Input Schema (P16–P19)

Per-template input composition for the [[closing-and-am-templates|P16–P19 closing & monitoring cluster]], expressed against [[template-input-schema]]. This cluster takes `deal_terms_core` at its widest (closing memo) and at its tightest recurring forms (the tracker and draw calc).

## Closing Memo (.docx)

The hand-off record — nearly the full library. Composes `deal_identity`, `parties` (bank group / co-lenders, Overland role & hold, deal team), `deal_terms_core` (`facility_structure`, `pricing`, `grids`, `fees`, `commitment_maturity`, `amort_prepay`, `ddtl_governor`, `financial_covenants`, `ltm_anchor`), `sources_uses`, `pro_forma_cap`, `ebitda_build`, `historical_financials`, `returns`, `narrative_blocks`, `legal_doc_digest` (the executed-agreement digest — incremental/baskets, restricted payments, equity cure, Required-Lenders definition, intercreditor & EoD triggers, reporting cadence, deemed-EBITDA-by-quarter), `esg`. Template-specific projection:

- `trade_ticket` — the flattened key-terms exhibit (a read-only view selecting from the buckets above).

Its `financial_covenants` + `ebitda_build` + `legal_doc_digest` form the authoritative monitoring baseline.

## Closing Memo Backup (.xlsx)

The paired calc engine — six sheets mirroring the memo exhibits. Composes `sources_uses`, `pro_forma_cap`, `financial_covenants` (FCCR build at close), `grids` (the covenant-pricing/unused/amortization/ECF grids), `historical_financials`, `ebitda_build`, `returns`, `parties` (bank-group commitments table), and the `trade_ticket` view. Same memo↔backup pairing as the [[screening-input-schema|posting-memo backup]].

## Compliance Certificate Tracker (.xlsx)

The recurring control. Composes `ebitda_build` (the full per-period GAAP-NI → deemed-EBITDA build with Definitional/Diligence add-back typing and individual + shared caps), `financial_covenants` (TNL with cash-netting cap, FCCR, minimum liquidity — each *tested*), `ltm_anchor`. Template-specific:

- `reporting_periods` — the `EOMONTH`-driven period columns.
- `reported_vs_covenant` — the load-bearing dual-column audit control: borrower-stated vs independently recomputed, preserved side-by-side. This is the [[compliance-certificate-parser-pilot]] target.

## DDTL Draw Calc (.xlsx)

The draw gate. Composes `ltm_anchor`, `ebitda_build`, `sources_uses` (the draw's S&U), `pro_forma_cap`, `ddtl_governor` (the pro-forma leverage test the draw must clear). Template-specific:

- `tri_column` — the LTM → Target → Pro-Forma column structure plus add-on QoE inputs.

## Amendment Memo (.docx)

A `modification_delta` over the closing baseline. Wraps `deal_terms_core` (every term Original vs Proposed with No-Change/Change flags) plus `ebitda_build` (add-back-cap deltas), and re-runs `projection_cases`, `narrative_blocks`, and `comparable_set` (refreshed DSV / precedents). Inputs: the original closing memo + executed agreement (baseline) and the amendment request. It *resets* the baseline the tracker and draw calc test against.

## The shared spine

One covenant-definition source — the [[form-credit-agreement]] §1.6 / Article 6 — must flow through the closing digest, tracker, draw calc, and amendment delta so all four test identical math. `deal_terms_core` enters at closing and is *referenced* (never re-keyed) by every recurring control. Amended values propagate via `modification_delta`. Several artifacts here are RESTRICTED — see [[restricted-content-discipline]].

## Related Concepts

- [[template-input-schema]] — the canonical bucket library and `deal_terms_core`
- [[closing-and-am-templates]] — the structural description of the same cluster
- [[compliance-certificate-parser-pilot]] — automates `reported_vs_covenant`
- [[form-credit-agreement]] — the single covenant-definition source
- [[term-sheet-ic-input-schema]] — where `deal_terms_core` originates

## Sources

- `[Company] - Overland Closing Memo (MM-DD-YY) vTemplate.docx`, covenant + legal digest
- `[Company] - Compliance Certificate Tracker_vTemplate.xlsx`, Reported-vs-Covenant build
- `[Company] - DDTL Draw Calc (MM-DD-YY) vTemplate.xlsx` / `[Company] - Overland Amendment Memo (MM-DD-YY) vTemplate.docx`
