---
title: Arrakis Overview
category: arrakis-architecture
tags: [architecture, application]
sources:
  - arrakis_blueprint_v2_3.md
last_updated: 2026-05-13
---

# Arrakis Overview

Arrakis is the **integrated suite of purpose-built applications** that covers the full lifecycle of a private credit / direct lending investment process — from deal origination through portfolio monitoring and valuation. It is the long-arc destination this library's artifacts are designed to graduate into.

The suite is **one platform substrate plus 13 domain applications**, designed and operated by a single firm-internal development team and deployed as a cohesive platform rather than a collection of independent products. It serves the deal teams, the Investment Committee, the operations team, and post-close portfolio managers as the system of record for every consequential decision.

## What Arrakis replaces

Arrakis consolidates a fragmented landscape of commercial point solutions:

- DealCloud — pipeline management
- Ironclad / DocuSign CLM — NDA workflow
- Harvey AI — legal drafting
- Ansarada — diligence rooms
- Zeck — board collaboration
- WSO / Allvue — loan accounting
- SyndTrak / Debtdomain — syndication
- Chronograph / 73 Strings — portfolio monitoring and valuation

Consolidation eliminates the data fragmentation that occurs when each vendor maintains its own opinionated data model, and places every record under a unified governance, security, and audit regime.

## The three-layer integration architecture

All 14 components share one architecture:

1. **Private operational state.** Each application owns its operational state in a private PostgreSQL schema and never reaches into another application's database.
2. **Asynchronous events on Redpanda.** Inter-application events flow through a Redpanda event bus using versioned Avro schemas and a standard event envelope. See [[redpanda-event-bus]].
3. **Synchronous calls through Foldspace.** Synchronous inter-application calls — and all calls into the platform layer — flow through [[foldspace-substrate]] (Kong API gateway, Master Data API, Document Registry, DCA, Observatory, API Catalog, Spice).

Snowflake is the shared analytical and master data platform. Each application publishes a single canonical export of its operational state into a dedicated landing schema in [[snowflake-medallion]]'s RAW layer.

## The 14 components

See [[application-directory]] for a one-line summary of each app. The full list, in deal-lifecycle order:

**Foldspace** (platform), then **Thumper · Gom Jabbar · Gurney · Sardaukar · Mentat · Reverend Mother · Landsraad · CHOAM · Heighliner · Atreides · Stillsuit · Corrino · Melange**.

## Centralized domain topology

Arrakis sits firmly on the centralized end of the domain-topology spectrum. This is the right call for an organization that prioritizes strong control and standardization, is at the start of a new implementation, and where MDM efficiency, coherence, and shared compute resources are primary goals. A private credit firm with 14 applications, a single development team, and a shared Snowflake deployment is a textbook fit.

This does not mean Foldspace becomes a monolithic data warehouse that everyone writes to directly. It means Foldspace owns the integration substrate and master data governance layer, while each app encapsulates its own physical data model within its bounded domain.

## Why this matters for the library

Every artifact this library produces is built so it can be lifted into Arrakis without rewriting:

- Prompts have a stable cache-eligible system prefix and XML-tagged variable inputs — the exact shape Spice consumes in Arrakis. See [[spice-llm-service]].
- Skills produce structured outputs validated by Pydantic schemas — the same schemas Spice uses for output validation in Arrakis.
- Every IC-facing, legal, co-lender-facing, or AM-facing draft carries the `[DRAFT — HUMAN REVIEW REQUIRED]` watermark — the manual analog of the [[hitl-state-machine]] state `PENDING_REVIEW`.

## Related Concepts

- [[foldspace-substrate]] — the platform layer
- [[application-directory]] — the 13 domain applications
- [[snowflake-medallion]] — the shared analytical platform
- [[redpanda-event-bus]] — the asynchronous backbone
- [[spice-llm-service]] — the LLM brokering layer
- [[option-c-recommendation]] — why Arrakis is the recommended path

## Sources

- `arrakis_blueprint_v2_3.md`, Project Arrakis — Overview
