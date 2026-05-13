---
title: Foldspace — Platform Substrate
category: arrakis-architecture
tags: [architecture, application, governance]
sources:
  - arrakis_blueprint_v2_3.md
last_updated: 2026-05-13
---

# Foldspace — Platform Substrate

**Foldspace** is the platform infrastructure layer of [[arrakis-overview]] — the centralized substrate for data governance, master data, document registry, LLM integration, and platform observability. All 13 domain applications communicate with Foldspace exclusively through a Kong API gateway and never interact directly with the shared Snowflake or PostgreSQL infrastructure outside their own domain.

Foldspace is the **management landing zone** in the centralized-domain-topology pattern. It owns the integration substrate and master data governance layer; each app encapsulates its own physical data model within its bounded domain. Foldspace is not a monolithic data warehouse that everyone writes to.

## What Foldspace owns

| Component | Purpose |
| --- | --- |
| **Kong API Gateway** | Authentication / JWT validation, rate limiting, request logging, API versioning. All inter-app and app-to-platform calls flow through Kong. |
| **Master Data API** | Golden-record CRUD for the seven master entities. Enforces deduplication, assigns canonical IDs, emits `master-data-updated` events. See [[master-data-entities]]. |
| **Document Registry** | Centralized metadata for all binary documents (CIMs, credit agreements, NDA PDFs, model exports). Pre-signed S3 URL access pattern; no app stores object storage credentials. |
| **Data Contract Application (DCA)** | Registers, approves, and governs every data product exchange between apps. Automated Snowflake GRANT execution on contract approval. |
| **Foldspace Observatory** | Six-dimension data observability: freshness, volume, schema, lineage, quality, plus API SLA and event-bus lag. |
| **API Catalog** | Per-endpoint registration: URI, version, owner app, consuming apps, SLA targets, deprecation status, schema reference. External connectors registered alongside internal endpoints. |
| **Spice LLM Service** | The shared LLM brokering service — see [[spice-llm-service]]. |
| **foldspace-mcp** | The MCP server exposing read-only structured tools for Claude — see [[mcp-tool-catalog]]. |

## The Foldspace client library

A shared `foldspace_client` Python library is the **sole permitted mechanism** for app-to-Foldspace synchronous calls. All 13 apps import this client; raw `httpx` or `requests` direct calls to Foldspace are prohibited. The client enforces resilience defaults derived from the SLA targets in the API Catalog:

- **Connect timeout:** 1s
- **Read timeout:** endpoint SLA p95 × 2
- **Retry policy:** 2 retries with exponential backoff (base 500ms, jitter ±100ms) on 503 / 504 only
- **Operation budget:** 5s user-facing / 30s background
- **Connection pool:** Separate `httpx.AsyncClient` per Foldspace endpoint category (bulkhead isolation)
- **Circuit breaker:** Opens after 5 consecutive failures within 120s; half-open after 60s

## The standard error contract

All Foldspace API endpoints return errors using a single Pydantic model (`FoldspaceError` in `shared/schemas/errors.py`):

```python
class FoldspaceError(BaseModel):
    status: int                  # HTTP status code
    error_code: str              # Machine-readable code from a fixed vocabulary
    message: str                 # Human-readable, no PII, no stack traces
    detail: str | None = None    # Optional 4xx detail (stripped at tenant boundary)
    trace_id: str                # OpenTelemetry trace ID
    timestamp: datetime          # UTC ISO-8601
```

Every 4xx and 5xx response across the platform conforms. The `error_code` vocabulary is maintained centrally in `shared/schemas/error_codes.py` — apps must select from it, never invent ad hoc codes.

## External connector framework

External integrations (CapIQ, PitchBook, AlphaSights, GLG, NAICS, Chronograph) inherit from a `BaseConnector` Python class that standardizes authentication, rate limiting, retry logic, response normalization to canonical schemas, and dead-letter logging to Snowflake. New integrations require only a new connector class — no structural rework. Each connector registers in the API Catalog as an external API product with the same SLA accountability as internal endpoints.

## Why this matters for the library

The Foldspace contract is the boundary the artifacts in this library are designed to cross intact. When a prompt or schema graduates into Arrakis:

- The prompt enters the prompt library and is invoked by Spice through the `foldspace_client`.
- The Pydantic schema becomes the output validator that Spice runs.
- The HITL banner (`[DRAFT — HUMAN REVIEW REQUIRED]`) becomes the rendered banner on the calling app's review UI.
- The structured output lands in `<APP>_LAND` in the [[snowflake-medallion]] without translation.

## Related Concepts

- [[arrakis-overview]] — full platform context
- [[application-directory]] — the 13 domain consumers of Foldspace
- [[snowflake-medallion]] — the analytical platform Foldspace fronts
- [[spice-llm-service]] — Foldspace's LLM brokering
- [[mcp-tool-catalog]] — Foldspace's MCP tool surface
- [[master-data-entities]] — what the Master Data API governs

## Sources

- `arrakis_blueprint_v2_3.md`, Section 1 — Foundation Layer / Foldspace
