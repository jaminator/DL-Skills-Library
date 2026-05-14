---
title: Closing and Asset Management (Stages 5–6)
category: deal-lifecycle
tags: [process, deal-lifecycle, governance]
sources:
  - Overland_Deal_Lifecycle_Automation_051326_vJA.pdf
last_updated: 2026-05-13
---

# Closing and Asset Management (Stages 5–6)

Stages 5 and 6 cover **P13 Co-Lender / GP Syndication through P19 Amendments / Workout** — everything from term-sheet execution through portfolio monitoring and exit. The team composition shifts substantially: CBP Asset Management, CBP Finance, CBP Marketing & IR, and OL Co-Lenders join the core OL Underwriting / OL IC team.

## Stage 5 — Closing (P13 → P16)

### P13 Co-Lender / GP Syndication

**Teams.** OL Underwriting · OL IC · OL Co-Lenders · CBP IR · CBP Fund Finance.

**Tooling.** DealCloud · SharePoint · Word / Excel · Outlook · external VDRs (Datasite, Intralinks, Debt Domain).

### P14 Credit Agreement

**Teams.** Same as P13 plus external counsel.

**Tooling.** Same as P13.

### P15 Closing & Funding

**Teams.** Same as P13 plus WF RM / Loan Ops & Admin.

**Tooling.** Same as P13.

### P16 Closing Memo

**Teams.** OL Underwriting · OL IC · CBP Asset Management.

**Tooling.** Same as P13 plus AM distribution list.

**Pain points (4).**
- Commitment book tracked in ad hoc Excel; no syndication management system.
- WF inexperience with DDTL / direct lending pushes administrative burden onto Overland.
- No closing checklist tracking; KYC repository fully manual.
- Inconsistent UW-to-AM handoff at close; databook may not reach Chronograph.

**Opportunities (3).**
- Syndication CRM auto.
- Credit agreement redline AI.
- Closing memo auto-gen.

## Stage 6 — Asset Management (P17 → P19)

### P17 Portfolio Monitoring

**Teams.** CBP Asset Management · CBP Finance · CBP Marketing & IR · OL Underwriting · WF RM / Loan Ops & Admin.

**Tooling.** Chronograph · Excel (mark to market) · SharePoint · DealCloud · Outlook (AM distribution list).

### P18 Valuation & LP Reporting

**Teams.** Same as P17.

**Tooling.** Same as P17.

### P19 Amendments / Workout

**Teams.** Same as P17 plus CBP workout team for distressed cases.

**Tooling.** Same as P17.

**Pain points (4).**
- Chronograph not fully utilized as source of truth; monitoring features not leveraged.
- Manual Excel mark-to-market valuations.
- Compliance certs frequently contain CFO arithmetic errors; OL catches manually.
- DDTL draws approved over email; no compliance verification tracked.

**Opportunities (4).**
- Chronograph auto-feed.
- AI valuation triage.
- Amendment doc workflow.
- AM distribution list auto-route.

## Why these stages are the most under-instrumented

The deal lifecycle deck consistently flags Stages 5–6 as the most underbuilt today. Three reasons:

1. **The governance load is highest here.** Compliance certs, mark-to-market, RCF / DDTL draws, amendment tracking — these are the deck's [[foundation-controls]] and they are audit and regulatory exposures today, not just operational inconveniences.
2. **The handoff boundary is fragile.** P15–P16 is where underwriting hands off to AM. The deck describes this handoff as "inconsistent" with the **databook potentially not reaching Chronograph** — meaning AM starts cold on a deal it inherits.
3. **The vendor fit is poorest.** Chronograph is the intended portfolio system but is under-utilized. WSO and Allvue exist for loan accounting but don't integrate cleanly with upstream deal data. See [[ic-and-asset-mgmt-gaps]].

## What this means for the library

The library's actual first pilot is **P17 Compliance Certificate Parser** — see [[compliance-certificate-parser-pilot]]. P17 was chosen ahead of the deck's recommended P4 pilot because the AM friction is acute audit/regulatory exposure today and the extract-and-validate shape demonstrates the [[library-artifact-bundle]] cleanly. The **highest-yield follow-on builds** continue the closing-and-AM thread plus return upstream to P4:

- **Compliance certificate parser** (P17) — **built**. Extract covenant metrics from non-standard PDFs, validate against credit agreement definitions, flag CFO arithmetic errors before they reach Overland's manual catch.
- **RCF / DDTL draw verification** (P17) — same extract-and-validate shape, smaller scope, recommended next build.
- **Mark-to-market triage** (P18) — first-pass fair-value estimate with comparable selection, surfaced for human review. Exercises the second of the three [[opportunity-shapes]] (generate-with-review).
- **Closing memo auto-gen** (P16) — populate the closing memo from upstream artifacts (executed credit agreement terms, funds flow, KYC status).
- **P4 posting memo draft** — the originally-recommended pilot, generate-with-review shape, high-frequency phase.
- **Amendment doc workflow** (P19) — structured tracking and document generation for amendments and workouts.

Each of these uses the same construction pattern (skill + prompt + project instruction + Pydantic schema, HITL-gated, graduating into Arrakis) but targets the governance gaps that exist independent of the [[growth-gap]].

## Related Concepts

- [[deal-lifecycle-overview]] — full-lifecycle map
- [[ic-and-asset-mgmt-gaps]] — detailed friction in this stage range
- [[foundation-controls]] — governance investments at any portfolio scale
- [[application-directory]] — A9 Heighliner, A10 Atreides, A11 Stillsuit, A12 Corrino, A13 Melange
- [[compliance-certificate-parser-pilot]] — the P17 pilot built in this stage

## Sources

- `Overland_Deal_Lifecycle_Automation_051326_vJA.pdf`, slides 04–06, 09
