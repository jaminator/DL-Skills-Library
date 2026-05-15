---
title: Template Input Schema (Canonical Bucket Library)
category: deal-templates
tags: [template, schema, data-product, deal-lifecycle]
sources:
  - "[Company] - Wells & Overland Term Sheet (MM-DD-YY) vTemplate.docx"
  - "[Company] - Overland Closing Memo (MM-DD-YY) vTemplate.docx"
  - "[Company] - Overland Model (MM-DD-YY) vTemplate.xlsx"
  - "[Company] - Compliance Certificate Tracker_vTemplate.xlsx"
  - "Overland Form Credit and Guaranty Agreement.docx"
last_updated: 2026-05-15
---

# Template Input Schema (Canonical Bucket Library)

The [[template-library-overview|template set]] is not 17 independent forms — it is one deal-terms object observed from different angles. A second-pass read of every fill-in template confirms the same input categories recur: the term sheet, IC summary, closing memo, tracker, draw calc, and amendment memo are largely *projections of one shared structure*. This page defines that structure as a **canonical bucket library** — reusable schema fragments (JSON Schema `$defs` / Pydantic models) each template composes by reference rather than redefining, the construction that graduates the library into Arrakis Spice-validated outputs without rework.

## Why bucket, not map every cell

Granular workbooks have thousands of cells; enumerating them is neither stable nor portable. Each template instead maps to a small set of **logical buckets** — a cohesive input category with representative fields, not an exhaustive cell list. Buckets are shared by `$ref`; the per-cluster pages express each template as bucket ids plus any template-specific bucket.

## Canonical `$defs`

| Bucket id | Holds (representative fields) |
| --- | --- |
| `deal_identity` | borrower legal name, DBA, HQ, FYE, currency, sector/industry, founded, employees, ownership, transaction type |
| `parties` | sponsor, proposal lenders, admin agent, guarantors, collateral, bank group / co-lenders, deal team |
| `facility_structure` | total facility size; per tranche (ABL/RCF, 1L TLB, 1L DDTL, 2L, sub, HoldCo PIK, pref): global commitment, funded-at-close, currency |
| `pricing` | per-facility spread (S+bps), SOFR/LIBOR floor, OID; blended pricing on funded tranches at close |
| `grids` | leverage-tiered grids sharing one shape: pricing, unused-fee, CSA, amortization, ECF-sweep (metric, tier thresholds, value per tier) |
| `fees` | upfront/closing % by tranche (+ upfront/deferred split), unused % p.a. by tranche, ticking, admin agent fee $/yr, structuring/legal/doc |
| `commitment_maturity` | hold/commitment % per tranche, maturity & tenor per tranche, DDTL availability period (months) |
| `amort_prepay` | amortization % p.a. per tranche, call protection (102/101 HC + CoC/IPO carve-outs), mandatory prepayments, ECF sweep % + step-down thresholds |
| `ddtl_governor` | pro forma leverage test level (x TNL/1LNL), availability trigger, one-time waiver level if amended |
| `financial_covenants` | max TNL grid by quarter (+ step-downs), min FCCR grid, min liquidity, cash-netting cap, equity-cure mechanics (window, frequency caps, over-cure rule) |
| `ebitda_build` | GAAP NI → definitional exclusions → reported EBITDA → add-backs typed **Definitional / Diligence / Pro-forma** → individual & shared caps (greater-of $/%, before/after giving effect) → deemed EBITDA by quarter |
| `ltm_anchor` | LTM CA EBITDA, LTM period date, last FYE, opening net leverage, leverage-basis footnote |
| `sources_uses` | sources (debt by tranche, owner equity, cash from B/S, seller notes); uses (refinance, cash taxes, capex, txn expenses, financing fees by tranche) |
| `pro_forma_cap` | cash, total debt, total net debt, common/implied equity, total capitalization, TEV, TEV multiple |
| `historical_financials` | revenue/GP/CA-EBITDA/capex by period, margins, CAGR, segment splits |
| `working_capital` | AR, inventory, prepaid, AP, deferred rev, CIE/BIE, accrued; DSO/DIH/DPO/CCC; NWC peak/trough swing |
| `returns` | unlevered & levered MOIC/IRR, backleverage rate / advance rates, stated YTM, BDC target-leverage |
| `projection_cases` | case toggle (sponsor base / Overland flat / downside); per-case revenue growth, margins, capex, NWC, exit |
| `risk_rating` | credit-criteria matrix with RR/SA scores (concentration, cyclicality, seasonality, capex, regulatory) |
| `legal_doc_digest` | incremental/ratio/MFN baskets, permitted acquisitions/indebtedness, restricted payments, Required-Lenders definition, intercreditor & EoD triggers |
| `comparable_set` | public-comp peer tickers + market fields, precedent transactions, stats |
| `diligence_requests` | mode toggle [Initial/Follow-Up], numbered questions & data requests |
| `narrative_blocks` | situation/company/customer/supplier/operations prose, highlights & risks/mitigants, mgmt bios, second-way-out / DSV |
| `meeting_decision` | meeting type [Pre-Screen/Commitment], date, per-row deal-team recommendation, committee approval/changes, next steps, focus areas |

Two cross-cutting **patterns**, not buckets: `modification_delta` (an Original-vs-Proposed pair plus No-Change/Change flag, wrapping any bucket — the amendment memo) and `trade_ticket` (a flattened read-only view over other buckets).

## JSON-extensible shape

```json
{ "$defs": { "facility_structure": { "...": "..." }, "financial_covenants": { "...": "..." } },
  "term_sheet": { "allOf": [ {"$ref":"#/$defs/deal_identity"}, {"$ref":"#/$defs/facility_structure"},
    {"$ref":"#/$defs/pricing"}, {"$ref":"#/$defs/grids"}, {"$ref":"#/$defs/fees"},
    {"$ref":"#/$defs/financial_covenants"}, {"$ref":"#/$defs/ltm_anchor"} ] } }
```

The [[form-credit-agreement]] supplies the vocabulary for `ebitda_build`, `financial_covenants`, `ddtl_governor`, and `legal_doc_digest`; the [[market-deal-terms-reference]] calibrates their ranges. New templates extend by adding a composition entry, not inventing fields.

## Related Concepts

- [[template-library-overview]] — the template chain these schemas instrument
- [[screening-input-schema]] — P3–P4 cluster bucket composition
- [[dd-workbook-input-schema]] — P6 workbook bucket composition
- [[term-sheet-ic-input-schema]] — P6–P11 instrument bucket composition
- [[closing-am-input-schema]] — P16–P19 cluster bucket composition
- [[form-credit-agreement]] — source of the covenant/EBITDA bucket vocabulary
- [[library-artifact-bundle]] — how these schemas become Pydantic outputs

## Sources

- `[Company] - Wells & Overland Term Sheet (MM-DD-YY) vTemplate.docx` and the full `raw/` fill-in template set
- `Overland Form Credit and Guaranty Agreement.docx`, Article 1 / Article 6 (covenant vocabulary)
