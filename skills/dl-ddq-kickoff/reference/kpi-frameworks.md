# KPI Frameworks — Deriving the Borrower-Specific Request Block

## Contents

- Purpose and the off-the-shelf constraint
- Framework → request-archetype map (the seven dimensions)
- Downstream-consumer rationale (what each request pre-seeds)
- Worked sector library
  - Canonical few-shot: residential HVAC services roll-up
  - Contrast 1: vertical-market B2B SaaS
  - Contrast 2: industrials / engineered-components manufacturer
  - Contrast 3: multi-site consumer healthcare services
- How to compose the block for a new borrower

---

## Purpose and the off-the-shelf constraint

Step 3 of the skill derives a borrower-specific KPI request block by reasoning
from the NAICS/GICS classification and business description through the Overland
credit framework. This file is the framework→request map plus a worked sector
library so that derivation is grounded, not improvised.

**The binding constraint: request only plausibly off-the-shelf data.** The
kick-off list is sent days after the NDA, before any analyst time is committed.
Ask only for metrics a competent management team in that industry already tracks
in the normal course of operating the business and can export from its existing
systems (BI dashboards, ERP, the board deck, the CIM data room). Anything that
requires the company to *build* an analysis belongs in the later, broader DD
list, not here. The footnote already in the template states this verbatim:
"Any off-the-shelf KPI's monitored by the management team in the course of
normal operations." The borrower-specific block makes that footnote concrete
for this industry; it does not exceed it.

When the sector classification is absent and the business description is too
thin to infer the demand model, emit
`[INSUFFICIENT DATA — sector classification not provided]` for the block. Do
not guess a generic KPI set.

---

## Framework → request-archetype map (the seven dimensions)

Each Overland credit-framework dimension implies a class of data request. Reason
through all seven; keep the ones the business model makes material.

| # | Framework dimension (Overland credit framework) | Request archetype it implies |
|---|---|---|
| 1 | **Demand-driver quality** (contractual recurring > reoccurring behavioral > non-discretionary break-fix > project/discretionary) | Revenue split by demand-driver type; recurring/reoccurring/break-fix/project mix; contract/subscription base, renewal & retention (gross and net), backlog and book-to-bill where project-based |
| 2 | **Concentration discipline** (caution >10% of revenue, material >20–25%) | Top-1 / Top-10 customer concentration (revenue %); Top-1 / Top-10 supplier concentration (spend %); end-market / geography / product concentration |
| 3 | **Growth quality** (2–3 yr revenue/GP/EBITDA trend; price vs. volume vs. mix) | Organic vs. acquired growth; price/volume/mix decomposition; same-store / same-customer growth; cohort or vintage retention curves |
| 4 | **Operating leverage** (fixed/variable cost structure; downside EBITDA behavior) | Fixed vs. variable cost split; contribution margin by line; unit economics (revenue/cost per job, per seat, per site, per unit) |
| 5 | **Capital intensity** (maintenance vs. growth capex; FCF, not EBITDA, as the debt-service metric) | Maintenance vs. growth capex split by FY; capex as % of revenue; fleet/asset age where asset-heavy |
| 6 | **NWC behavior** (direction and seasonality of the working-capital build) | NWC build by FY and by quarter; DSO/DIH/DPO/CCC; seasonality of cash collection; unbilled / deferred-revenue balances |
| 7 | **Ownership / workout** (debt-like items, payment obligations surviving close) | Existing debt & debt-like items remaining post-close with go-forward cash payouts; earn-out / deferred-consideration schedule (the "payment-bomb" screen); for buy-and-build, add-on cohort history and consideration structure |

Dimensions 2, 5, 6 and 7 are the every-borrower **stock cuts** (always
requested, regardless of sector — they are the standard set in the skill's
Step 2). Dimensions 1, 3 and 4 generate the **borrower-specific** lines, because
how you measure demand quality, growth, and unit economics is industry-shaped.

---

## Downstream-consumer rationale (what each request pre-seeds)

The kick-off ask is engineered so the returned data drops into the artifacts
that follow it. This is why the request is shaped the way it is — every line
has a named consumer.

| Kick-off request | Pre-seeds | Downstream field (schema) |
|---|---|---|
| Quarterly internal IS/BS/CF for the computed range | Databook quarterly P&L driver grid | `fin_inputs` (DD Workbook Input Schema) |
| Top-N customer / supplier concentration | Databook concentration tables; posting-memo Customers/Suppliers bullets and Concentration risk flag | `concentration` (DD Workbook Input Schema); `risk_rating` / `narrative_blocks` (Screening Input Schema) |
| Maintenance vs. growth capex split | Overland model capex driver; posting-memo Capex D&A bullet | `forecast_drivers` (DD Workbook Input Schema); `narrative_blocks` |
| NWC build by FY and quarter | Databook working-capital block (DSO/DIH/DPO/CCC) | `working_capital` (DD Workbook Input Schema) |
| LTM income statement + bridge to consolidated EBITDA | Posting-memo backup LTM anchor and EBITDA build | `ltm_anchor`, `ebitda_build` (Screening Input Schema) |
| Existing debt & debt-like items + earn-out/deferred schedule | Sources & uses, pro-forma cap, the payment-bomb screen | `sources_uses`, `pro_forma_cap` (Screening Input Schema) |
| Add-on cohort history + consideration structure | DDTL governor sizing; roll-up base-rate analysis | `ddtl_governor`, `forecast_drivers` (DD Workbook Input Schema) |
| Borrower-specific KPI block | Posting-memo Company Overview and D&A demand-driver characterization; the industry attractiveness read | `narrative_blocks` (Screening Input Schema) |

See the wiki pages `dd-workbook-input-schema` and `screening-input-schema` for
the full bucket composition; the kick-off feeds the `data_request_periods`
bucket and is the upstream source for the rest.

---

## Worked sector library

Each entry: the demand model, then the borrower-specific KPI lines that follow
from dimensions 1/3/4 for that model. The HVAC entry is the canonical few-shot;
the contrasts show how the block shifts with the demand model.

### Canonical few-shot: residential HVAC services roll-up

NAICS 238220 (Plumbing, Heating, and Air-Conditioning Contractors); GICS
Industrials → Commercial & Professional Services. Demand model: a mix of
contractual recurring (membership/service agreements), reoccurring behavioral
(break-fix repair), and project (replacement and new-construction installs);
buy-and-build roll-up of regional operators.

Borrower-specific KPI requests:

- Lead volume, booked-job conversion rate & average ticket, by service line
  (HVAC / plumbing / electrical) and by job type (service vs. replacement vs.
  new construction) — *demand-driver quality + unit economics (1, 4)*
- Membership / service-agreement count, attach rate & renewal rate —
  *recurring-base durability (1)*
- Revenue mix: recurring (service agreements) vs. reoccurring (break-fix) vs.
  project (replacement / new construction) — *demand-driver split (1)*
- Technician headcount, billable-hour utilization & retention — *operating
  leverage and the binding capacity constraint (4)*
- 4-wall P&L by brand / branch — *contribution economics and same-store
  growth (3, 4)*
- OEM rebate income & equipment purchases by supplier — *margin quality and
  supplier concentration interaction (4)*

Plus the stock cuts (always): Top-N customer/supplier concentration,
maintenance vs. growth capex split, NWC build, post-close debt-like items, and
— because this is buy-and-build — add-on cohort history (LTM revenue & EBITDA
at close vs. current per cohort) and add-on consideration structure (upfront
cash, seller/deferred notes, earn-outs, rollover equity).

### Contrast 1: vertical-market B2B SaaS

NAICS 511210 (Software Publishers); GICS Information Technology → Software.
Demand model: contractual recurring (subscription), low capital intensity,
typically founder- or sponsor-owned, often no existing reporting facility.

Borrower-specific KPI requests:

- ARR / NRR / GRR (net and gross revenue retention), logo retention —
  *recurring-base durability (1)*
- New ARR by cohort, expansion vs. new-logo split — *growth quality (3)*
- CAC, CAC payback, magic number / sales efficiency — *unit economics (4)*
- Gross & logo concentration (Top-1 / Top-10 ARR) — *concentration (2)*
- Gross margin by revenue type (subscription vs. services vs. usage) —
  *operating leverage (4)*

The compliance-certificate line is typically marked N/A (no existing reporting
facility). No add-on cohort block unless the SaaS company is itself a roll-up.
The block shifts entirely off "jobs/tickets" onto ARR-based retention metrics —
the demand model is contractual recurring, so dimension 1 dominates.

### Contrast 2: industrials / engineered-components manufacturer

NAICS 332710 / 333xxx; GICS Industrials → Machinery or Capital Goods. Demand
model: project and OEM-program revenue, cyclical, raw-material exposed, often
with an existing bank-syndicated (BSL) facility that reports regularly.

Borrower-specific KPI requests:

- Backlog, book-to-bill & order intake by end-market / program — *demand
  visibility for project revenue (1)*
- Revenue by platform / program with program-life and re-compete dates —
  *demand durability (1, 3)*
- Volume vs. price vs. raw-material pass-through bridge — *growth quality and
  margin pass-through (3, 4)*
- Capacity utilization & on-time delivery — *operating leverage (4)*
- Raw-material / commodity exposure and hedged vs. unhedged spend — *input
  cost volatility (4)*

The compliance-certificate line is active (existing BSL facility reports
regularly). Quarter labeling follows the borrower's fiscal calendar — these
companies frequently have non-calendar fiscal-year-ends.

### Contrast 3: multi-site consumer healthcare services

NAICS 621xxx; GICS Health Care → Health Care Providers & Services. Demand model:
non-discretionary break-fix and reoccurring visit-based, payor-mix sensitive,
multi-site roll-up.

Borrower-specific KPI requests:

- Visit / procedure volume, revenue per visit & payor mix (commercial /
  Medicare / Medicaid / self-pay) — *demand-driver quality + reimbursement
  risk (1)*
- Same-clinic (de novo vs. mature) volume and revenue growth — *growth
  quality (3)*
- Provider headcount, productivity & retention — *the binding capacity
  constraint (4)*
- Site-level 4-wall P&L and contribution margin — *operating leverage (4)*
- Referral-source concentration — *concentration (2)*

Add-on cohort block applies (multi-site roll-up). Payor-mix concentration is
the sector-specific concentration cut layered on top of the standard Top-N.

---

## How to compose the block for a new borrower

1. Read the NAICS/GICS classification and business description; name the
   dominant demand model in one sentence (contractual recurring / reoccurring
   behavioral / break-fix / project / hybrid).
2. Walk dimensions 1, 3, 4 and write the borrower-specific lines for that demand
   model — terse noun phrases, each a metric management already tracks.
3. Confirm the stock cuts (dimensions 2, 5, 6, 7) and add the add-on cohort +
   consideration lines only if the business is buy-and-build.
4. Layer any sector-specific concentration or risk cut (payor mix, program
   re-compete, raw-material exposure) where the framework flags it material.
5. Apply the off-the-shelf test to every line: if management would have to
   build it rather than export it, cut it or move it to the later DD list.
6. Keep the borrower-specific block within the one-page ceiling (the script
   enforces a hard cap; tighten phrasing rather than spilling).
