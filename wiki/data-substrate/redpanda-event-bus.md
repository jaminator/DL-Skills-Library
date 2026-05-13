---
title: Redpanda Event Bus
category: data-substrate
tags: [event, architecture, data-product]
sources:
  - arrakis_blueprint_v2_3.md
last_updated: 2026-05-13
---

# Redpanda Event Bus

**Redpanda** is the asynchronous backbone of Arrakis: every cross-application event flows through Redpanda topics, every payload uses versioned Avro schemas, and every event carries a standard envelope that gives consumers idempotency, ordering, and lineage. Redpanda is Kafka-compatible, single-binary, zero-ZooKeeper — the operationally simpler call for a single-team platform. See [[arrakis-overview]].

## Core topic taxonomy

Topics are dot-namespaced and roughly mirror the deal lifecycle:

| Domain | Topics |
| --- | --- |
| Deal lifecycle | `deal.created`, `deal.stage-changed`, `deal.closed` |
| NDA | `nda.received`, `nda.executed`, `nda.expired`, `nda.obligation-flagged` |
| Triage | `triage-memo.completed` |
| IC | `ic.submitted`, `ic.approved`, `ic.conditions-set`, `ic.session-closed` |
| Terms / CA | `terms.agreed`, `ca.executed` |
| Syndication | `syndication.allocation-updated`, `syndication.commitment-confirmed` |
| Closing / Funding | `closing.task-completed`, `funding.confirmed` |
| Loans | `loan.payment-received`, `loan.amendment-executed`, `loan.covenant-breach`, `loan.agent-notice-received`, `loan.reconciliation-discrepancy` |
| Documents | `document.uploaded`, `document.executed` |
| Financial data | `financial-data.received`, `financial-data.validated` |
| Valuation | `valuation.cycle-initiated`, `valuation.approved`, `valuation.published` |
| MDM | `mdm.conflict-raised`, `mdm.conflict-resolved`, `master-data-updated`, `master-data.ownership-transferred`, `master-data.ownership-corrected`, `master-data.locally-reconciled`, `master-data.reconciliation-failed` |
| Data quality | `data-quality.sla-breach`, `data-quality.gate-failed`, `data-quality.upstream-breach-active`, `data-quality.upstream-breach-resolved` |
| Data contracts | `data-contract.approved`, `data-contract.deprecated`, `data-contract.revoked`, `data-contract.version-created`, `data-contract.major-version-created`, `data-contract.review-triggered`, `data-contract.status-changed` |

Snowpipe Streaming tails all topics into `ARRAKIS_RAW.APP_EVENTS` for analytical replay.

## Standard event envelope

Every Avro event includes a common envelope (`arrakis.common.EventEnvelope`):

```json
{
  "event_id":         "UUID v4 — unique per event, used for idempotent dedup",
  "event_type":       "Dot-delimited topic name, e.g. 'deal.created'",
  "event_time":       "PostgreSQL transaction timestamp (UTC ms)",
  "source_app":       "Producing app name (matches structlog app_id)",
  "deal_id":          "Primary deal context (null only for entity-level events)",
  "trace_id":         "OpenTelemetry trace ID propagated from origin",
  "correlation_id":   "Business correlation ID across the deal lifecycle",
  "schema_version":   "Monotonically increasing payload version",
  "payload":          "Avro-serialized domain-specific payload (bytes)"
}
```

The envelope is implemented as a Pydantic v2 base class in the Foldspace client library. All 13 apps inherit from it when constructing outbox events.

## Outbox pattern

Every state-changing write across the 13 apps appends a row to a local `outbox_events` table within the same PostgreSQL transaction as the business write. A lightweight relay process tails the outbox and publishes to Redpanda. Failure dispositions:

- **Transient failure** → exponential backoff retry, never advance position.
- **Poison event** → after 3 failed attempts, move to `dead_letter_events` and emit `data-quality.gate-failed`.
- **Lag monitoring** → `outbox_relay_lag_seconds` Prometheus gauge with Grafana alerting at 5 / 15 minute thresholds.

Crucially, the Avro payload is **serialized before** the outbox INSERT. If serialization fails, the entire transaction rolls back — no invalid event ever enters the outbox.

## Idempotent consumer contract

Every consumer enforces idempotency end-to-end using the envelope's `event_id`:

1. Each consuming app maintains a `processed_events` table: `{event_id UUID PK, topic, processed_at}`.
2. Before processing, the consumer checks for `event_id` and skips if present.
3. The business write and the `processed_events` INSERT happen in the **same PostgreSQL transaction**.
4. The table is pruned periodically (default 7 days, bounded by Redpanda's retention).

## Topic partitioning

Topics use deterministic partition keys derived from the primary business entity:

| Topic category | Partition key | Partitions |
| --- | --- | --- |
| `deal.*`, `nda.*`, `triage-memo.*`, `ic.*`, `terms.*`, `ca.*`, `syndication.*`, `closing.*`, `funding.*`, `document.*`, `valuation.*` | `deal_id` | 12 |
| `loan.*` | `facility_id` | 12 |
| `financial-data.*` | `company_id` | 6 |
| `mdm.*`, `master-data-updated` | `entity_type:entity_id` | 6 |
| `data-quality.*` | `data_product_id` | 3 |

Same key + same partition count = copartitioned consumption without repartitioning. Partition counts cannot change after topic creation without a coordinated migration.

## Schema compatibility

The Redpanda Schema Registry enforces **FULL compatibility** as the global default — both forward and backward — ensuring no consumer breaks on a producer schema change. Per-topic relaxations require data-steward approval and DCA registration. Breaking schema changes use a **dual-stream migration pattern**: new topic `{original}.v2`, dual-publish during migration window, consumers migrate per their release schedule, original deprecated after all consumers + Snowpipe migrate.

## Why this matters for the library

This library does not write events to Redpanda directly. But every Pydantic schema produced here is **the inner payload** of a future Avro envelope. Two implications:

1. **Schemas use snake_case Python primitives** that round-trip cleanly through Avro and into Snowflake VARIANT columns.
2. **Schemas declare a `schema_version` integer** in their docstring or class metadata, so when they enter the prompt library and the Spice audit trail, version evolution is explicit from day one.

## Related Concepts

- [[snowflake-medallion]] — Snowpipe destination for `APP_EVENTS`
- [[master-data-entities]] — entity events that ride the bus
- [[foldspace-substrate]] — the platform that owns the topic taxonomy
- [[application-directory]] — the 13 producers / consumers

## Sources

- `arrakis_blueprint_v2_3.md`, Section 1 — Event Bus (Redpanda) and Section 2 — Standard event envelope
