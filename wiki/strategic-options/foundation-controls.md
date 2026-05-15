---
title: Foundation Controls (Required at Any Scale)
category: strategic-options
tags: [governance, policy, pain-point]
sources:
  - deal_lifecycle_automation_051326_vJA.pdf
last_updated: 2026-05-13
---

# Foundation Controls (Required at Any Scale)

The deal lifecycle deck identifies **eight foundation controls** that are required of an institutionally managed direct lending GP at any portfolio size — 30 names, 110, or 225. These are operating standards, not contingent on hitting the [[growth-gap]] target. Several are framed in the deck as audit and regulatory exposures today; the obligation to address them exists independent of the chosen strategic path.

## The eight controls

### 1. Conflicts and Cross-Strategy Allocation

Treasury allocation across the firm's fund entities — hold size, investment criteria, concentration limits, economic targets differ by SMA and fund — and across non-direct-lending Credit, PE, and RE pockets. **The logic must be systematic, defensible, and auditable.** Today, allocation lives in spreadsheets and informal practice. The Arrakis response is the [[foldspace-substrate]] master-data layer plus the per-fund allocation rules as a registered data product.

### 2. IC Approvals and Approval Tracking

No formal IC vote tracking today. Conditional approvals are undocumented. There is **no system gate between IC approval and fund release** — an audit and regulatory exposure that compounds as the book scales. See [[ic-and-asset-mgmt-gaps]]. Closed by A7 Landsraad.

### 3. Pricing, Fee Grids, and Call Protection

Are we being paid correctly? Pro rata P&I on time, pricing and unused-fee grids applied per the credit agreement, call protection collected whenever it is active and a prepayment triggers it. Today this is verified manually. Closed by A11 Stillsuit (loan administration ledger) plus A8 CHOAM (term-grid source of truth).

### 4. RCF and DDTL Draws

Draws are conditional — no default or EoD, pro forma leverage within covenant, permitted use of proceeds. **Those conditions must be enforced at funding** so the firm never wires to a borrower that technically isn't entitled to the money. Today DDTL draws are approved over email with no compliance verification tracked. Closed by A11 Stillsuit (draw verification gate) plus A12 Corrino (covenant verification).

### 5. Compliance Certs, Leverage, and ECF

Are the company's certs accurate? Leverage and ECF calculations tied to the credit agreement's specific definitions, sweeps applied at the right level, ECF allocated pro rata across tranches when owed. Today compliance certs frequently contain CFO arithmetic errors that the firm catches manually. Closed by A12 Corrino (compliance certificate parser, automated covenant calculation).

### 6. Valuation / Mark-to-Market

Portfolio marking cadence, methodology, and defensibility are under increasing SEC scrutiny. **Apollo's commitment to daily NAV marks signals where fair-value expectations for private credit are headed.** Today the firm marks in Excel. Closed by A13 Melange (stage-gate fair-value workflow, IPEV / ASC 820 framework).

### 7. PortCo Reimbursement of OOP Expenses

Systematized tracking and invoicing of rechargeable expenses (legal, diligence, monitoring) is **a fiduciary obligation, not an operational convenience**. Today this lives in spreadsheets and email threads. Addressed across A4 Sardaukar (DD expense capture) and A11 Stillsuit (loan administration accounts).

### 8. LP Reporting — Current and Prospective / SMA

Prospective LPs and SMAs increasingly want company- and loan-level transparency: waiver, consent, and amendment counts across the book; technical vs. material classification; drivers (performance, liquidity, post-close clean-up) on demand. Today this is assembled by hand each quarter. Closed by A12 Corrino + A13 Melange + the `LP_REPORTING` consumption schema in the [[snowflake-medallion]].

## One Team — a value, not yet a technological reality

The deck notes pointedly:

> One Team is a core CB value, but it is not yet a technological reality — the data across our strategies does not talk to itself. When an IP in any strategy isn't sought out, forgets a detail, or leaves the platform, their insights leave with them.

The foundation controls are the architectural answer. Build them on a common substrate and the knowledge base does not just persist — it compounds across Credit, PE, and RE, and accrues to every future deal team.

## Why this matters here

The foundation controls are **why Option A alone is insufficient**. Personal Claude libraries do not close any of the eight controls. Even the best-curated personal library can compress an underwriter's posting-memo time, but it cannot:

- Track IC votes systematically.
- Enforce conditional approvals at the fund-release gate.
- Validate compliance certs against credit-agreement definitions.
- Maintain a defensible mark-to-market workflow.

These obligations are platform-level. They require the [[option-c-recommendation]] (Arrakis) to address. This library is built so its artifacts graduate cleanly into the platform that closes them.

## Related Concepts

- [[three-options]] — A / B / C framing
- [[option-c-recommendation]] — the path that closes these controls
- [[ic-and-asset-mgmt-gaps]] — the IC and AM controls in operational terms
- [[application-directory]] — apps that close each control

## Sources

- `deal_lifecycle_automation_051326_vJA.pdf`, slide 09
