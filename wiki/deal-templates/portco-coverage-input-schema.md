---
title: PortCo Coverage Input Schema
category: deal-templates
tags: [template, schema, governance, data-product]
sources:
  - "PortCo Coverage Template (02-26-26) vF.xlsx"
last_updated: 2026-05-15
---

# PortCo Coverage Input Schema

Per-sheet input composition for the [[portco-coverage-workbook]], expressed against the [[template-input-schema]] canonical bucket library. The defining property of this workbook is that it **re-keys almost nothing**: it is a standing *reference holder* that composes buckets which originated upstream at closing, then layers a small set of monitoring-specific projections on top. `deal_terms_core` enters once via the [[closing-am-input-schema|closing artifacts]] and is referenced thereafter; amended values arrive as `modification_delta`.

## Per-sheet composition

**Dashboard** — a flattened read-only view (the `trade_ticket` pattern, applied at portfolio scale). Selects from `deal_identity`, `parties`, `deal_terms_core`, `pro_forma_cap`, `historical_financials`, `financial_covenants`, `comparable_set`, plus the monitoring projections below. Holds no primary inputs.

**Financials Input** — `historical_financials` projected over a **`financial_basis_matrix`**: {Reported, Restated, Pro Forma, Budgeted} × {TTM, YTD, Monthly}, each a P&L → Reported EBITDA → CA EBITDA → capex/FCF row set; plus `working_capital` (the NWC / DSO-DIH-DPO-CCC block) and a **`cap_table_snapshot`** pair — `pro_forma_cap` at Last Close vs Current (a temporal `modification_delta` over `pro_forma_cap`).

**Covenant Input** — the recurring control: `ebitda_build` (GAAP-NI → ≤50 net-income adjustments → ≤50 EBITDA adjustments, Definitional/Diligence typing, individual $/% and shared caps), `financial_covenants` *tested* (Total Net Leverage with cash-netting floor/cap, FCCR, minimum liquidity), `ltm_anchor`, plus `reporting_periods` and the load-bearing `reported_vs_covenant` dual column. This is the [[compliance-certificate-parser-pilot]] target, operationalized across many periods rather than one certificate.

**Trade Ticket Input** — the `trade_ticket` view materialized once per instrument from `facility_structure`, `pricing`, `fees`, `amort_prepay`, `grids`, and `commitment_maturity`; equity tranches add a small voting/board/blocker projection.

**Add-On Input** — a new **`add_on_summary`** bucket: platform + add-on rows (consideration split, LTM revenue/EBITDA, purchase multiple), total add-ons / total blended. Feeds the amendment/upsize databook seed.

**Public / Tnx Comps Input** — `comparable_set` (public tickers + market fields; precedent transactions; high/low/avg/median; valuation caps). Feeds **`valuation_mark`** — per-security mark + valuation date + comp-derived multiple — surfaced on the Dashboard.

**Data Validation** — the controlled-vocabulary source backing the enums in `deal_terms_core`, `esg`, and `risk_rating` (investment status, GICS sector→industry, ESG risk category + exclusion subsectors, interest basis, adjustment cap `$/%` and type `Definitional/Pre-Acquisition/Diligence/Pro-Forma`).

## New buckets introduced

This ingest adds four monitoring-specific projections to the bucket library, all compositions of existing `$defs` rather than new field inventories:

- `financial_basis_matrix` — `historical_financials` indexed by (basis, period-type).
- `cap_table_snapshot` — a Last-Close vs Current pair over `pro_forma_cap`.
- `valuation_mark` — per-security fair-value mark + date, anchored to `comparable_set`.
- `add_on_summary` — platform/add-on M&A roll-up; the amendment-databook seed.

## The shared spine

One covenant-definition source — the [[form-credit-agreement]] §1.6 / Article 6 — flows the [[closing-am-input-schema|closing digest]] → this workbook's Covenant Input → the Amendment Memo `modification_delta`, so the closing baseline, recurring tests, and amendments all compute identical math. The valuation-mark and cap-table outputs are RESTRICTED — see [[restricted-content-discipline]] — and the at-close trade-ticket/cap composition is the [[master-data-entities|Facility master-entity]] payload that graduates into the [[snowflake-medallion]] for LP/SEC reporting.

## Related Concepts

- [[portco-coverage-workbook]] — the structural description of the same workbook
- [[template-input-schema]] — the canonical bucket library this composes
- [[closing-am-input-schema]] — where `deal_terms_core` is first keyed
- [[compliance-certificate-parser-pilot]] — automates `reported_vs_covenant`
- [[form-credit-agreement]] — the single covenant-definition source

## Sources

- `PortCo Coverage Template (02-26-26) vF.xlsx`, Financials Input / Covenant Input / Trade Ticket Input / Add-On Input / Comps / Data Validation sheets
