---
title: DD Workbook Input Schema (P6)
category: deal-templates
tags: [template, schema, deal-lifecycle]
sources:
  - "[Company] - Databook (MM-DD-YY) vTemplate.xlsx"
  - "[Company] - Overland Model (MM-DD-YY) vTemplate.xlsx"
  - "[Company] - Comps (MM-DD-YY) vTemplate.xlsm"
  - "[Company] - Refi Payback Analysis (MM-DD-YY) vTemplate.xlsm"
last_updated: 2026-05-15
---

# DD Workbook Input Schema (P6)

Per-workbook input composition for the [[dd-analytical-workbooks|P6 analytical core]], expressed against [[template-input-schema]]. These are the most cell-dense templates; the bucket discipline (representative fields, not every cell) matters most here.

## Databook (.xlsx)

The normalization workspace. Composes `deal_identity`, `sources_uses`, `facility_structure` (the SUCAP pro-forma cap detail with per-tranche fees/pricing/maturity/OID/call), `pro_forma_cap`, `ebitda_build` (the reported→adjusted bridge — the canonical instance other artifacts reference), `historical_financials`, `working_capital` (quarterly DSO/DIH/DPO/CCC), `projection_cases` (seasonality + DSV downside toggle). Template-specific:

- `concentration` — Top-N customer and supplier tables (revenue / gross-profit / purchases share).
- `fin_inputs` — the quarterly P&L driver grid (variable/fixed COGS & SG&A split) feeding the bridge.

## Overland Model (.xlsx)

The projection engine — one monolithic sheet. Composes `deal_identity`, `facility_structure`, `pricing` (SOFR/LIBOR toggle + forward curve + floors), `grids` (senior/RCF/DDTL pricing grids, unused-fee, ECF-sweep), `amort_prepay`, `ddtl_governor` (the leverage-cap that throttles DDTL draws), `financial_covenants` (computed headroom), `ebitda_build` (forecast form), `projection_cases` (sponsor base / Overland flat / downside toggle), `returns`. Template-specific:

- `forecast_drivers` — per-case revenue growth, variable/fixed cost split, capex split.
- `debt_schedule` — per-tranche draw/repay/balance assumptions across the stack (revolver, 1L/2L, DDTL, HoldCo PIK, sub/pref).
- `tax_schedule` — NOL and §163(j) interest-limitation carryforwards.

The model's `ebitda_build`, `ddtl_governor`, and `financial_covenants` must stay definitionally aligned with the [[form-credit-agreement]] so headroom computed here matches the executed deal.

## Comps (.xlsm)

Valuation anchor. Composes `comparable_set`. Template-specific:

- `market_data_feed` — Capital IQ / FactSet ticker list, valuation reference date, and the analyst-curated precedent-deal list (no macros; the `.xlsm` extension only hosts the data add-in).

## Refi Payback Analysis (.xlsm)

A two-scenario differential. Template-specific:

- `refi_scenarios` — Scenario A (Wells & Overland refi) vs Scenario B (incumbent/BSL), each instantiating `facility_structure`, `pricing`, `fees`, and `sources_uses`, plus `payback` (annual interest-savings delta, incremental Scenario B fees, breakeven years over the term-SOFR curve).

## The shared spine

`ebitda_build` is *authored once in the Databook* and referenced by the Model, the screening/posting memos, and downstream monitoring. `facility_structure`, `pricing`, and `grids` flow Model → [[term-sheet-ic-input-schema|term sheet / IC summary]]. The workbooks are the system of record for the deal-terms core before it externalizes.

## Related Concepts

- [[template-input-schema]] — the canonical bucket library these `$ref`
- [[dd-analytical-workbooks]] — the structural description of the same workbooks
- [[term-sheet-ic-input-schema]] — consumes the leverage/returns/pricing outputs
- [[form-credit-agreement]] — the covenant definitions `ebitda_build` must mirror

## Sources

- `[Company] - Databook (MM-DD-YY) vTemplate.xlsx`, SUCAP / EBITDA / NWC / FinInputs
- `[Company] - Overland Model (MM-DD-YY) vTemplate.xlsx`, single-sheet block structure
- `[Company] - Comps (MM-DD-YY) vTemplate.xlsm` / `[Company] - Refi Payback Analysis (MM-DD-YY) vTemplate.xlsm`
