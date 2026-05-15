---
title: PortCo Coverage Workbook (Asset-Management Monitoring)
category: deal-templates
tags: [template, process, governance, risk, data-product]
sources:
  - "PortCo Coverage Template (02-26-26) vF.xlsx"
last_updated: 2026-05-15
---

# PortCo Coverage Workbook (Asset-Management Monitoring)

The PortCo Coverage workbook is the **standing, one-per-portfolio-company monitoring workspace** for Stage 6 Asset Management. Unlike the per-phase deliverables in [[closing-and-am-templates]], it is not produced once — it *persists* across the whole post-close life of a credit and is the Excel realization of what Chronograph (and, in Arrakis, [[application-directory|A12 Corrino]]) is meant to hold. It is seeded at hand-off from the closing memo and closing-memo backup, refreshed every reporting period, and reused as the launch point for any amendment.

## Sheet anatomy

- **Dashboard** — the read-only "OL Investment Dashboard" presentation layer: company identity (GICS sector/industry, FYE, ESG category), parties (CEO/CFO, owner/sponsor & fund, agent, counsel, WF origination, OL roles), the Overland Investment Summary (per-security commitment / outstanding / % total, fees, pricing, **OL valuation mark + valuation date**), capitalization summary, leverage/liquidity stack (First Lien / Senior / OpCo / Total Net Leverage incl. HoldCo, LTV, TEV/EBITDA, interest coverage), a covenant-compliance summary with period columns and % cushion, add-on M&A, OL amendment history, and recent events.
- **Financials Input** — financials on a **basis × period cube**: {Reported, Restated, Pro Forma, Budgeted} × {TTM, YTD, Monthly}, each a full P&L → Reported EBITDA → CA EBITDA → capex / FCF conversion; plus NWC detail (AR, CIE, inventory, AP, BIE, deferred revenue; DSO/DIH/DPO/CCC) and two cap tables — **Pro Forma Capitalization (Last Close)** and **(Current)** — each a full OpCo+HoldCo debt waterfall with cash-netting, equity, TEV and leverage.
- **Covenant Input** — the compliance-certificate engine: a Consolidated EBITDA build (GAAP net income → up to 50 net-income adjustments → interest/tax/D&A → up to 50 EBITDA adjustments), an "as-reported" check, Diligence/Pro-Forma adjustment split, per-adjustment Definitional/Diligence typing with individual ($ or %) and shared caps, then the **Total Net Leverage, FCCR, and Minimum-Liquidity tests each shown Reported vs Covenant with % cushion**. This is the operational, multi-period superset of the [[compliance-certificate-parser-pilot]] tracker.
- **Trade Ticket Input** — the at-close trade ticket, one block per instrument across the full stack (ABL/priority RCF, 1L TL, 1L last-out TL, 1L DDTL, 2L TL, sub notes, HoldCo notes, preferred, common): dates, tenor, facility size, OL commitment & final hold, fee schedule, floating/fixed economics, amortization, pricing grid, prepayment/call-protection schedule, equity voting/board/blocker rights.
- **Add-On Input** — platform + add-on roll-up (consideration split, LTM revenue/EBITDA, purchase multiple, blended).
- **Public / Tnx Comps Input** — CapIQ/FactSet-fed comp sets with valuation caps and high/low/avg/median stats (the valuation-mark anchors); a `veryHidden` `_CIQHiddenCacheSheet` carries the data-refresh plumbing noted in [[template-library-overview]].
- **Data Validation** — the controlled-vocabulary source (investment status, GICS, ESG 1/2/3 + exclusion subsectors, interest basis, adjustment cap and type enums).

## Upstream and downstream

**Upstream (seeds it):** the [[closing-and-am-templates|closing memo + backup]] (trade ticket, last-close cap table, parties), the [[form-credit-agreement]] §1.6 / Article 6 covenant-definition spine, and the [[dd-analytical-workbooks|databook/model]] opening historicals.

**Downstream (consumes it):** Chronograph / A12 Corrino seed at the under-instrumented hand-off the [[ic-and-asset-mgmt-gaps|databook-may-not-reach-Chronograph]] gap describes; recurring covenant monitoring; quarterly portfolio reviews feeding **valuation marks** (comps + OL mark → ASC 820 / IPEV, Arrakis A13 Melange) and **risk ratings** (leverage / cushion / recent events → an eight-dimension rating and Corrino early-warning scoring); **SEC & LP reporting** via the [[snowflake-medallion]] consumption layer; and the **amendment / upsize / incremental** path, where Add-On Input + current cap table + amendment history launch a fresh databook and the Amendment Memo `modification_delta`. The at-close trade ticket and cap also form the **Facility** master-entity payload (see [[master-data-entities]]). Several outputs (fund-level marks, OL valuation) are RESTRICTED — see [[restricted-content-discipline]].

## Related Concepts

- [[portco-coverage-input-schema]] — the per-sheet input-bucket composition
- [[closing-and-am-templates]] — the closing artifacts that seed this workbook
- [[compliance-certificate-parser-pilot]] — automates the Covenant Input control
- [[closing-and-asset-management]] — the Stage 6 lifecycle this workbook serves
- [[ic-and-asset-mgmt-gaps]] — the Chronograph hand-off gap it bridges
- [[template-library-overview]] — the full deal-template chain

## Sources

- `PortCo Coverage Template (02-26-26) vF.xlsx`, all sheets (Dashboard, Financials Input, Covenant Input, Trade Ticket Input, Add-On Input, Comps, Data Validation)
