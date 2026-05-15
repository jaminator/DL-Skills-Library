---
title: DD Analytical Workbooks (P6)
category: deal-templates
tags: [template, process, deal-lifecycle]
sources:
  - "[Company] - Databook (MM-DD-YY) vTemplate.xlsx"
  - "[Company] - Overland Model (MM-DD-YY) vTemplate.xlsx"
  - "[Company] - Comps (MM-DD-YY) vTemplate.xlsm"
  - "[Company] - Refi Payback Analysis (MM-DD-YY) vTemplate.xlsm"
last_updated: 2026-05-15
---

# DD Analytical Workbooks (P6)

Four Excel workbooks form the Stage 3 / P6 Initial DD analytical core. They are the engine room behind every IC memo from pre-screen onward: the databook normalizes the target's financials, the model projects the credit, comps anchor valuation, and the refi-payback analysis justifies the economics. None contains VBA macros — the `.xlsm` extension on two of them exists only to host Capital IQ / FactSet data-refresh plumbing.

## Databook (.xlsx)

The structured analytical workspace that recasts target historicals into the firm's standard credit lens. Ten sheets: `SUCAP` (sources & uses / pro forma capitalization, anchoring the workbook's named ranges), `Top Customer` / `Top Supplier` (concentration), `HistFin` (+ charts), `EBITDA` (reported→adjusted bridge with diligence and pro forma adjustments), `NWC` (quarterly DSO/DIH/DPO/CCC), `Seasonality`, `DSV` (distressed-sale-value downside toggle), and `FinInputs`. Inputs: audited and management financials, the QoE report (drives EBITDA and diligence adjustments), CIM/projections, customer & supplier billing detail. Iterative calculation is enabled for financing-fee/interest circularity.

## Overland Model (.xlsx)

The versioned LBO/credit projection model — a single deliberately monolithic `Model` sheet navigated by print areas. Logical blocks: sources & uses, forecast drivers (variable/fixed COGS & SG&A split), revenue/EBITDA buildup, a cash-tax schedule with NOL and 163(j) interest-limitation carryforwards, a full debt schedule (revolver, 1L/2L term loan, DDTL, HoldCo PIK, subordinated/preferred), amortization and excess-cash-flow-sweep grids, a leverage governor capping DDTL draws, RCF/senior pricing grids, a leverage & coverage summary, and a SOFR/LIBOR toggle with forward curves. It is scenario-driven via a case toggle (sponsor base, Overland flat, Overland downside). Inputs: the databook (adjusted EBITDA, NWC, capex), management projections, proposed structure and pricing, forward rate curves, tax assumptions. It defines the financeable quantum, pricing grid, and covenant headroom.

## Comps (.xlsm)

Trading (public) and transaction (precedent) comparable analysis. Sheets: hidden Capital IQ helper/cache sheets, `Public Comparables` (share-price performance, EV/EBITDA, EV/EBITDA-capex, EV/Revenue, margin, summary stats), and `Precedent Trx` (target/acquiror, sponsor-vs-strategic acquisition type, TEV/EBITDA, leases-incl/excl). Inputs: the Capital IQ feed plus an analyst-curated peer set and precedent-deal list, cross-checked against target LTM financials from the databook.

## Refi Payback Analysis (.xlsm)

A compact single-sheet two-scenario differential model: Scenario A (the Wells & Overland refi) versus Scenario B (incumbent / existing / BSL alternative). It rolls up structure, a fees-and-expenses summary, an all-in interest summary over term SOFR, liquidity, and a payback analysis (annual interest-savings delta, incremental Scenario B fees, breakeven payback period in years). Inputs: the model's debt quantum and pricing, the proposed fee schedule, the alternative's terms, and the term SOFR curve.

## Inputs, outputs, downstream

The cluster consumes QoE, CIM, audited and management financials, and market data. It produces normalized financials, a credit projection, a valuation range, and a refi-economics justification. Downstream, these flow into the [[term-sheet-and-ic-templates|IC summary and term sheet]] (leverage, FCCR, returns, pricing), the [[screening-templates|screening and posting memos]], and ultimately the closing-stage [[closing-and-am-templates|baseline]]. The model's leverage and EBITDA definitions must stay consistent with the [[form-credit-agreement]] so covenant headroom computed here matches the executed agreement.

## Related Concepts

- [[screening-templates]] — upstream cluster that seeds the projection cases
- [[term-sheet-and-ic-templates]] — consumes leverage, returns, and pricing outputs
- [[form-credit-agreement]] — the covenant definitions the model must mirror
- [[term-sheet-and-commitment]] — the lifecycle stages this DD core serves
- [[dd-workbook-input-schema]] — the per-workbook input-bucket composition for this cluster
- [[template-library-overview]] — the full template chain

## Sources

- `[Company] - Databook (MM-DD-YY) vTemplate.xlsx`, sheet inventory
- `[Company] - Overland Model (MM-DD-YY) vTemplate.xlsx`, single-sheet block structure
- `[Company] - Comps (MM-DD-YY) vTemplate.xlsm` / `[Company] - Refi Payback Analysis (MM-DD-YY) vTemplate.xlsm`
