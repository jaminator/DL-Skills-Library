---
title: Application Directory (the 13 Domain Apps)
category: arrakis-architecture
tags: [architecture, application]
sources:
  - arrakis_blueprint_v2_3.md
  - deal_lifecycle_automation_051326_vJA.pdf
last_updated: 2026-05-13
---

# Application Directory (the 13 Domain Apps)

Arrakis is **one platform substrate (Foldspace) plus 13 domain applications**, in deal-lifecycle order. Each app owns a private PostgreSQL schema, publishes state to a dedicated `<APP>_LAND` schema in [[snowflake-medallion]], and communicates with other apps exclusively through the Foldspace API gateway and the Redpanda event bus. The Spice service brokers every Claude API call across the suite; the foldspace-mcp server exposes the read-only tool catalog for agentic flows. See [[arrakis-overview]] and [[foldspace-substrate]].

## The 13 apps mapped to the deal lifecycle

| # | App | Lifecycle home | What it owns |
| --- | --- | --- | --- |
| **A1** | **Thumper** | P1 (Origination) | Deal pipeline tracking, origination activity log, BDC ingestion. Creates the canonical Deal record that all other apps reference by `deal_id`. Golden source for Deal. |
| **A2** | **Gom Jabbar** | P2 (NDA Processing) | NDA workflow with dynamic approval routing, post-signature obligation tracking, AI-extracted NDA metadata, bulk NDA operations. Replaces Ironclad / DocuSign CLM. |
| **A3** | **Gurney** | All stages (CRM) | Deal CRM and relationship intelligence: company, sponsor, contact records; interaction history; ethical-wall enforcement; PitchBook / CapIQ enrichment. Golden source for Company, Sponsor, Contact (and Borrower pre-close). |
| **A4** | **Sardaukar** | P5–P10 (DD) | Diligence workflow engine: DD queue management, Q&A tracking, AI-assisted document classification, pgvector similar-question retrieval, milestone tracking with Gantt view. |
| **A5** | **Mentat** | P5–P10 (Modeling) | Financial modeling: multi-scenario, Monte Carlo, sensitivity tornado, model version control with audit lineage from document receipt to model output. |
| **A6** | **Reverend Mother** | P4, P7, P11, P16 (Memos) | Credit memo drafting via Spice: structured block-editor (Lexical) frontend, S3 version control, memo handoff to IC. **The natural Arrakis home for the [[posting-memo-friction]] pilot.** |
| **A7** | **Landsraad** | P7, P11 (IC) | IC deliberation: real-time annotation via WebSocket / Redis pub-sub, pre-meeting sealed voting, append-only decision audit trail, automated minutes generation. Closes the IC vote / minutes gap (see [[ic-and-asset-mgmt-gaps]]). |
| **A8** | **CHOAM** | P8, P12, P14 (Terms / CA) | Term sheet and credit agreement management: term negotiation, redlining, pgvector precedent library, AI-assisted multi-document analysis, post-execution obligation tracking. Golden source for Facility (pre-close). |
| **A9** | **Heighliner** | P13 (Syndication) | Syndication and agency: co-lender deal site with hard tenant isolation, allocation management, amendment / consent voting, AI-assisted co-lender DD responses, post-close borrower portal. |
| **A10** | **Atreides** | P15 (Closing) | Closing workflow: structured checklist, KYC / AML compliance gating, maker-checker approval for funds flow, two-phase funding confirmation handoff to Stillsuit. |
| **A11** | **Stillsuit** | P15+ (Loan Admin) | Loan administration: payment processing, amendments, covenant delivery tracking, agent notice processing, cash reconciliation, the authoritative post-close loan ledger. Golden source for Borrower and Facility post-close. |
| **A12** | **Corrino** | P17 (Monitoring) | Portfolio monitoring: covenant calculation and headroom tracking, financial statement ingestion, early-warning risk scoring, performance dashboards, LP / board reporting via Snowflake. |
| **A13** | **Melange** | P18 (Valuation) | Valuation: fair value with stage-gate approval, roll-forward automation, comparable selection, IPEV / ASC 820 compliance framework, credit-specific DCF engine, LP valuation schedule generation. |

## Why the names

The naming convention is Frank Herbert's *Dune*. **Foldspace** is the spice-enabled travel substrate; **Spice** is the resource that makes everything work; the 13 apps each carry a thematic tie to their function. The naming is consistent across the codebase, the Snowflake schemas (`THUMPER_LAND`, `GOM_JABBAR_LAND`, ...), the topic taxonomy, and the per-app `CLAUDE.md` files.

## Mapping the deck's A1–A13 to the blueprint

The deal lifecycle deck names the apps by function (A1 Pipeline Intelligence, A2 NDA Workflow, A3 Deal CRM, etc.). The blueprint names the same apps by their *Dune* identity. The mapping is one-to-one and order-preserving — A1 in the deck is Thumper in the blueprint, A2 is Gom Jabbar, and so on.

## Build sequence

Per the blueprint's Section 11, the apps deploy in deal-lifecycle order with foundation first:

1. **Phase 0** (Weeks 1–8): Foldspace foundation (Snowflake schemas, Redpanda, Kong, Master Data API, Spice stub, foldspace-mcp).
2. **Phase 1** (Weeks 9–18): Thumper, Gurney, Gom Jabbar.
3. **Phase 2** (Weeks 19–36): Reverend Mother (triage), Sardaukar, Mentat, Reverend Mother (IC), Landsraad.
4. **Phase 3** (Weeks 37–50): CHOAM, Heighliner (pre-close), Atreides.
5. **Phase 4** (Weeks 51–68): Stillsuit, Corrino, Melange, Heighliner (post-close).
6. **Phase 5** (Weeks 69–78): Governance maturity.

This library's pilot for P4 Posting Memo lands in Phase 2 of the Arrakis build (Reverend Mother triage stage). The pilot's prompt and schema graduate directly into the Reverend Mother prompt library and `REVEREND_MOTHER_LAND` landing schema.

## Related Concepts

- [[arrakis-overview]] — the platform context
- [[foldspace-substrate]] — the platform layer the 13 apps depend on
- [[snowflake-medallion]] — where each app's `<APP>_LAND` schema lives
- [[master-data-entities]] — golden-source ownership across apps
- [[deal-lifecycle-overview]] — the lifecycle these apps map to

## Sources

- `arrakis_blueprint_v2_3.md`, Overview (Application Directory) and Section 11 (Build Sequencing)
- `deal_lifecycle_automation_051326_vJA.pdf`, slides 22–24
