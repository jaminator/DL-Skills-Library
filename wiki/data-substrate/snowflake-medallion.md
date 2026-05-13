---
title: Snowflake Medallion (RAW / CURATED / CONSUMPTION)
category: data-substrate
tags: [data-product, architecture]
sources:
  - arrakis_blueprint_v2_3.md
last_updated: 2026-05-13
---

# Snowflake Medallion (RAW / CURATED / CONSUMPTION)

The Arrakis analytical platform uses the standard Bronze / Silver / Gold layering pattern — called **RAW / CURATED / CONSUMPTION** in the blueprint — implemented in three Snowflake databases. Every application that produces structured state passes through an explicit RAW landing schema before curation, and one pipeline owns one application's full state export.

## The three databases

| Database | Layer | Purpose |
| --- | --- | --- |
| `ARRAKIS_RAW` | Bronze | Raw landing data: event payloads from Redpanda, external API payloads (CapIQ, PitchBook, AlphaSights), document intake metadata, and one landing schema per application. |
| `ARRAKIS_CURATED` | Silver | Cleansed, normalized per-domain entities: DEALS, COMPANIES, FACILITIES, DD_ACTIVITY, FINANCIAL_DATA, LOAN_EVENTS, IC_ACTIVITY, NDA_ACTIVITY, TERMS_ACTIVITY, etc. |
| `ARRAKIS_CONSUMPTION` | Gold | Consumption-ready views: MDM (golden records), DEAL_PIPELINE, PORTFOLIO_ANALYTICS, COVENANT_TRACKING, VALUATION_OUTPUTS, IC_AUDIT, LP_REPORTING, NDA_COMPLIANCE, CLOSING_STATUS, DATA_QUALITY. |

## RAW landing schemas — one per application

The principle: **one pipeline per application state**. Each app gets exactly one landing schema, and the pipeline from that landing schema branches into the relevant curated schemas.

The 16 RAW schemas:

- `APP_EVENTS` — raw event payloads from Redpanda (via Snowpipe Streaming)
- `EXTERNAL_FEEDS` — raw API payloads (CapIQ, PitchBook, AlphaSights, NAICS)
- `DOCUMENT_METADATA` — raw document intake records
- `THUMPER_LAND`, `GOM_JABBAR_LAND`, `GURNEY_LAND`, `SARDAUKAR_LAND`, `MENTAT_LAND`, `REVEREND_MOTHER_LAND`, `LANDSRAAD_LAND`, `CHOAM_LAND`, `HEIGHLINER_LAND`, `ATREIDES_LAND`, `STILLSUIT_LAND`, `CORRINO_LAND`, `MELANGE_LAND` — one per domain app

## Materialization

Snowflake **Dynamic Tables** are the primary mechanism for automating Silver → Gold materialization for analytical workloads (covenant calculations, portfolio metrics). Snowflake **Streams + Tasks** are preferred for event-driven propagation (e.g., tailing the loan events stream to trigger covenant recalculation).

The **MDM system** sits between Silver and Gold: curated schemas hold per-domain entities; the MDM schema in consumption holds the deduplicated, cross-reconciled golden records. See [[master-data-entities]].

## Time travel and fail-safe retention

| Database | TIME_TRAVEL | FAIL_SAFE | Why |
| --- | --- | --- | --- |
| `ARRAKIS_RAW` | 14 days | 7 days | Replay window for Observatory anomaly investigation; covers two weekly reporting cycles plus the 7-day Redpanda retention margin. |
| `ARRAKIS_CURATED` | 7 days | 7 days | Derived from RAW and recomputable; 7 days supports short-term debugging of dbt model errors. |
| `ARRAKIS_CONSUMPTION` | 90 days | 7 days | Regulatory, audit, and LP reporting workloads need point-in-time queries (e.g., "what did COVENANT_TRACKING show as of Q3 close?"). Requires Snowflake Enterprise Edition. |

Retention settings are applied via schemachange migrations and enforced as a CI/CD blocking check.

## Why this matters for the library

Every Pydantic schema produced by this library is built to land in a Snowflake RAW landing schema without translation. When a skill or prompt produces a structured output:

- **Field naming** uses snake_case (Snowflake convention).
- **Types** are JSON-serializable Python primitives.
- **Required vs. optional** is explicit at the field level (Pydantic `Optional`).
- **No nested unstructured blobs** that would need parsing downstream — everything Snowflake-queryable.

This is the operational meaning of the portability principle: a schema written in the development environment of this library, validated locally during a pilot, lands cleanly in `<APP>_LAND` in Arrakis with zero translation work.

## Related Concepts

- [[master-data-entities]] — golden records that populate the MDM schema
- [[redpanda-event-bus]] — Snowpipe Streaming source for `APP_EVENTS`
- [[foldspace-substrate]] — the integration layer fronting Snowflake
- [[data-classification-tiers]] — every column carries a classification tag

## Sources

- `arrakis_blueprint_v2_3.md`, Section 1 — Snowflake Landing Zone Structure
