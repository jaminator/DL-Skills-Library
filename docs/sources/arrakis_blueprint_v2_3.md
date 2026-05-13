# Project Arrakis: Full Architecture Blueprint

**Version:** 2.3 (Working Draft)
**Status:** Published
**Published:** 2026-04-28

---

## Project Arrakis — Overview

### What Is Arrakis?

Arrakis is an integrated suite of purpose-built applications covering the full lifecycle of a private credit / direct lending investment process — from deal origination through portfolio monitoring and valuation. The suite is designed and operated by a single firm-internal development team and is deployed as a cohesive platform rather than a collection of independent products. It serves the firm's deal teams, Investment Committee, operations team, and post-close portfolio managers as the system of record for every consequential decision in the deal lifecycle.

The suite replaces a fragmented landscape of commercial point solutions — DealCloud for pipeline management, Ironclad and DocuSign CLM for NDA workflow, Harvey AI for legal drafting, Ansarada for diligence rooms, Zeck for board collaboration, WSO and Allvue for loan accounting, SyndTrak and Debtdomain for syndication, Chronograph and 73 Strings for portfolio monitoring and valuation — with a single firm-owned platform built on a shared data substrate. Consolidation eliminates the data fragmentation that occurs when each commercial vendor maintains its own opinionated data model, and it places every record under a unified governance, security, and audit regime.

All fourteen applications are unified by a three-layer integration architecture. Each application owns its operational state in a private PostgreSQL schema and never reaches into another application's database. Inter-application asynchronous events flow through a Redpanda event bus using versioned Avro schemas and a standard event envelope. Synchronous inter-application calls — and all calls into the platform layer — flow through Foldspace, the firm's centralized integration substrate. Foldspace fronts a Kong API gateway, the Master Data API governing the firm's golden records, the Foldspace Document Registry, the Data Contract Application (DCA), the Foldspace Observatory for data quality monitoring, the Foldspace API Catalog, and the Spice LLM service that brokers every Claude API call across the suite.

Snowflake is the shared analytical and master data platform. Each application publishes a single canonical export of its operational state into a dedicated landing schema in Snowflake's RAW (Bronze) layer. From there, curated data products are materialized in CURATED (Silver), and consumption-ready views are materialized in CONSUMPTION (Gold). The MDM golden records, IC audit trail, portfolio analytics, covenant tracking, and LP reporting outputs all live in this consumption tier. Every data product is governed by a registered data contract in the DCA, classified under a four-tier sensitivity scheme, and continuously monitored by the Observatory.

Foldspace is the management landing zone — the centralized substrate for data governance, master data, document registry, LLM integration, and platform observability. It is not a monolithic data warehouse that all apps write into; rather, it owns the governance, integration, and shared platform services, while each application encapsulates its own physical data model within its bounded domain.

### Application Directory

The fourteen applications, in deal-lifecycle order, are:

1. **Foldspace** — Platform infrastructure layer: API gateway substrate (Kong), Master Data API, document registry, Data Contract Authority (DCA), Foldspace Observatory, and the Spice LLM service. All 13 domain applications communicate with Foldspace exclusively through Kong and never interact directly with the shared Snowflake or PostgreSQL infrastructure outside their own domain.

2. **Thumper** — Deal origination and pipeline management. Thumper creates the canonical Deal record that all other applications reference by `deal_id`, making it the golden source for the Deal master entity.

3. **Gom Jabbar** — NDA workflow management: counterparty intake, dynamic approval routing, NDA execution, post-signature obligation tracking, and bulk NDA operations for multi-deal scenarios.

4. **Gurney** — Deal CRM and relationship intelligence: company, sponsor, and contact record management; interaction history logging; ethical wall enforcement; and PitchBook/CapIQ enrichment via the external data connector framework.

5. **Sardaukar** — Due diligence workflow engine: DD queue management, Q&A tracking, AI-assisted document classification, pgvector-powered similar-question retrieval, and milestone tracking with Gantt-view visualization.

6. **Mentat** — Financial modeling platform: multi-scenario analysis, Monte Carlo simulation, sensitivity tornado charts, multi-dimensional calculation engine, and full model version control with audit lineage from document receipt to model output.

7. **Reverend Mother** — Credit memo drafting: LLM-assisted section authoring via the Spice service, structured block-editor frontend (Lexical), S3-backed version control, and memo handoff to the IC session.

8. **Landsraad** — IC deliberation platform: real-time collaborative annotation via WebSocket/Redis pub-sub, pre-meeting sealed voting, IC decision recording to an append-only audit trail, and automated minutes generation.

9. **CHOAM** — Deal economics and term sheet management: term negotiation, credit agreement redlining, pgvector-backed precedent library, AI-assisted multi-document analysis, and post-execution obligation tracking.

10. **Heighliner** — Syndication and agency management: co-lender deal site with hard tenant isolation, allocation management, amendment/consent voting, AI-assisted co-lender DD responses, and a post-close borrower reporting portal.

11. **Atreides** — Closing workflow: structured closing checklist, KYC/AML compliance gating, maker-checker approval for funds flow changes, and the two-phase funding confirmation handoff to Stillsuit.

12. **Stillsuit** — Loan administration: payment processing, amendment management, covenant delivery tracking, agent notice processing, cash reconciliation, and the authoritative post-close loan ledger. Stillsuit becomes the golden source for the Borrower and Facility master entities upon funding.

13. **Corrino** — Portfolio monitoring: covenant calculation and headroom tracking, financial statement ingestion, early-warning risk scoring, performance dashboards, and LP/board reporting output via Snowflake.

14. **Melange** — Valuation: fair value workflow with stage-gate approval, roll-forward automation, comparable company selection, IPEV/ASC 820 compliance framework, credit-specific DCF engine, and LP valuation schedule generation.

### How the Blueprint Was Developed

The blueprint was designed from first principles using *Data Management at Scale* (2nd Edition) as its foundational framework. Specific guidance drawn from that text shapes the centralized domain topology appropriate for a firm with a single development team, the polyglot persistence strategy with PostgreSQL for operational state and Snowflake for the shared analytical platform, the Bronze/Silver/Gold (RAW/CURATED/CONSUMPTION) data layering pattern, MDM golden-record governance with append-only conflict resolution, formal data contract management through a deployed DCA, and operational observability across freshness, volume, schema, lineage, and quality dimensions.

The blueprint extends that foundation with domain-specific best practices drawn from a curated set of software engineering reference texts covering distributed systems design, event-driven microservices, API design and resilience, architectural patterns with Python, Kubernetes production operations, security engineering, machine-learning system design, and test-driven development. Each external pattern is integrated into Arrakis-specific decisions — outbox semantics, schema compatibility policy, async Unit of Work, four-layer service architecture, optimistic concurrency, resource tier classification, NetworkPolicy segmentation, prompt caching, RAG retrieval quality, MCP tool governance, and so on — rather than imported as a standalone convention. Where reference patterns conflict with the blueprint's centralized topology or single-team operating model, the blueprint's decisions hold.

The result is a single, authoritative reference document that serves both as the complete architectural specification for the suite and as the primary context document for AI-assisted software development sessions using Claude Code Agent Teams. Every entity has an owner, every column has a classification, every contract has an SLA, and every consequential workflow has a runbook.

---

## 1. Foundation Layer — Foldspace

This section establishes the platform substrate on which every Arrakis application runs: the topology choice, the persistence stack, the Snowflake landing zone, master data governance, the integration layer, and the event bus. Every other section of the blueprint depends on the components defined here.

### Philosophy: Centralized Domain Topology on a Shared Platform

Among the spectrum of domain topologies — from fully federated to fully centralized — the centralized domain topology is the appropriate choice for organizations that prioritize strong control and standardization, are at the start of a new implementation, and where MDM efficiency, coherence, and shared compute resources are primary goals. A private credit firm with 14 applications, a single development team, and a shared Snowflake deployment is a textbook fit. Within this topology, a data management landing zone provides all supervisory capabilities — data catalog, data lineage, the API catalog, MDM services, central metadata repositories — under unified governance. Foldspace is that management landing zone.

This does not mean Foldspace becomes a monolithic data warehouse that everyone writes to directly. It means Foldspace owns the integration substrate and master data governance layer, while each app owns its own operational state in PostgreSQL and publishes read-optimized data products upward to Snowflake. Each team encapsulates its physical data model within its domain boundaries — the opposite of throwing raw data over the fence.

### Polyglot Persistence Strategy

No single database handles all workloads optimally. The Arrakis persistence stack and the reasoning for each component:

**Snowflake (Primary Data Platform — Analytics, MDM, Data Products)**

- All structured analytical data, data products, and consumption-ready views live here
- Master data golden records, IC audit trail, portfolio metrics, valuation outputs, covenant calculations
- Snowflake Streams + Tasks + Dynamic Tables power automated data product refresh throughout the suite
- Snowflake RBAC (Row Access Policies, Column Masking) enforces data governance at the platform level
- Snowflake Cortex LLM functions provide lightweight AI summarization close to the data

**PostgreSQL (Operational Transactional Store — Per-App)**

- Each application gets its own PostgreSQL schema (or isolated database in a shared RDS/Cloud SQL instance) for its operational state — workflow queues, task management, annotation records, loan ledger entries, voting records
- ACID guarantees, row-level locking, and real-time writes are required for Gom Jabbar's NDA negotiation state, Sardaukar's DD queue mutations, Landsraad's annotation/vote writes, and Stillsuit's payment ledger
- PostgreSQL is explicitly not a data distribution layer — it is each app's private inner-architecture database
- All apps use an outbox pattern: every state-changing write also appends a row to a local `outbox_events` table, which a lightweight relay process tails and publishes to Redpanda

**Transaction Isolation Level Guidance:**

PostgreSQL's default read committed isolation is sufficient for the majority of Arrakis application writes — single-row inserts, append-only event logging, and outbox writes — because these patterns do not involve read-then-write cycles on shared mutable state. However, three categories of operations require stronger isolation:

| Category | Affected Apps | Isolation Requirement | Rationale |
|---|---|---|---|
| Balance-affecting writes (payment application, balance adjustment) | Stillsuit | SERIALIZABLE (SSI) | A concurrent payment receipt and amendment against the same facility could produce an incorrect running balance if both read the balance, compute independently, and write back. PostgreSQL's SSI detects this conflict at commit time and aborts one transaction for retry. |
| Allocation-constrained writes (commitment updates that must sum to facility size) | Heighliner | SERIALIZABLE (SSI) | Two co-lender commitment updates submitted concurrently could individually pass the "total ≤ facility committed amount" check but together exceed it. SSI prevents this write-skew anomaly. |
| Multi-row gating writes (checklist completion that gates a downstream action) | Atreides | REPEATABLE READ (minimum) | Closing task resolution reads the full checklist state to determine whether all items are complete before allowing the funding confirmation workflow to proceed. Snapshot isolation ensures the checklist state is consistent within the transaction. |

All other PostgreSQL writes across the suite (outbox appends, append-only event inserts, SCD Type 2 inserts) operate safely at read committed. Application code must handle serialization failures (PostgreSQL error code `40001`) with automatic retry — the Foldspace client library exposes a `with_retry(max_attempts=3)` wrapper for serializable transactions.

**Outbox relay failure handling.** Each application's outbox relay process must implement the following failure disposition:

1. **Transient failures** (Redpanda broker unreachable, connection timeout): Retry with exponential backoff (initial 1s, max 60s, jitter). The relay must not advance its position in the `outbox_events` table until the event is confirmed published (at-least-once guarantee). The relay logs each retry attempt with `{app_id, outbox_event_id, attempt_count, error_class}` via structlog.
2. **Poison events** (Avro serialization failure, schema registry rejection, payload exceeding Redpanda's configured `max.message.bytes`): After 3 failed attempts, the relay moves the event to a `dead_letter_events` table in the application's PostgreSQL schema. The dead-letter table schema mirrors `outbox_events` with additional columns: `failure_reason`, `failed_at`, `retry_count`. The relay emits a `data-quality.gate-failed` event to the `data-quality.gate-failed` Redpanda topic (using a minimal, pre-validated Avro envelope that cannot itself fail serialization) to alert the Observatory. The relay then advances past the poison event to avoid blocking subsequent events.
3. **Relay lag monitoring**: Each relay process exposes a Prometheus gauge metric `outbox_relay_lag_seconds` measuring the age of the oldest unprocessed event in `outbox_events`. A Grafana alert fires when lag exceeds 5 minutes (warning) or 15 minutes (critical, pages on-call engineer). This metric is distinct from the Observatory's data product freshness monitoring, which operates at the Snowflake level.
4. **Recovery**: Dead-letter events are reviewed manually by the owning app team. After root cause resolution, events can be replayed from the dead-letter table back into the outbox by an operator script (`scripts/replay_dead_letters.py`), which re-validates the Avro schema before re-insertion.

**Redis (Caching, Session Management, Real-Time Pub/Sub)**

- API response caching (deal metadata, entity lookups, permission checks) — materially reduces Snowflake query costs for frequently accessed master data
- Session tokens and JWT validation cache for the auth layer
- Real-time pub/sub for Landsraad's collaborative features (annotation presence, live section navigation, vote broadcast) — Redis pub/sub is the right tool for ephemeral real-time messaging that does not require durability
- Celery task queue backend for async LLM drafting jobs in Reverend Mother, Mentat, and CHOAM

**Redpanda (Event Bus — Inter-App Event Streaming)**

- Kafka-compatible, single-binary, zero-ZooKeeper, operationally far simpler than Apache Kafka — the right call for a team that should not spend cycles operating Kafka clusters
- All cross-application events flow through Redpanda topics
- Event payload schemas versioned using Apache Avro, registered in a Redpanda Schema Registry
- Snowflake's Kafka connector (Snowpipe Streaming or the Kafka connector) tails Redpanda topics directly, landing raw events into the Snowflake RAW landing zone in near-real-time

**Idempotent consumer contract.** Every Redpanda event published via the outbox pattern carries an `event_id` field (the `outbox_event_id` from the originating application's outbox table, included in the Avro payload). Every application-level consumer must enforce idempotency using this `event_id` end-to-end:

1. Each consuming application maintains a `processed_events` table in its PostgreSQL schema: `{event_id UUID PRIMARY KEY, topic VARCHAR, processed_at TIMESTAMPTZ}`.
2. Before processing an incoming event, the consumer checks for the `event_id` in `processed_events`. If present, the event is acknowledged (offset committed) and skipped.
3. The business-logic write and the `processed_events` INSERT are performed within the same PostgreSQL transaction, ensuring atomicity — the event is marked as processed if and only if the business effect was committed.
4. The `processed_events` table is pruned periodically (retain 7 days by default) to bound storage. Pruning is safe because Redpanda's retention window (see topic retention policy) determines the maximum redelivery window.

This pattern does not apply to Snowpipe Streaming ingestion into `ARRAKIS_RAW.APP_EVENTS`, which uses Snowflake's built-in exactly-once ingestion guarantee via channel offsets.

**Document Storage (S3/GCS)**

- Binary documents (CIMs, credit agreements, NDA PDFs, financial model exports) stored in object storage with versioned keys
- Foldspace maintains a document metadata registry in Snowflake (`document_id`, `deal_id`, version, S3 key, uploader, timestamp, classification)
- Pre-signed URL access pattern: apps never store object storage credentials, they request time-limited pre-signed URLs from the Foldspace document API

### Snowflake Landing Zone Structure

The Bronze/Silver/Gold layering — called RAW/CURATED/CONSUMPTION in this architecture — is the foundational design pattern for data product architectures. A data lakehouse approach is the best practice for enabling teams to build data products: each data domain provider ingests data into its respective data lake services through a set of pipelines it manages, owns, and operates. Mapped to Snowflake databases and schemas:

```
ARRAKIS_RAW (Snowflake Database — "Bronze")
│
├── SCHEMA: APP_EVENTS              ← Raw event payloads from Redpanda (via Snowpipe)
├── SCHEMA: EXTERNAL_FEEDS          ← Raw API payloads: Cap IQ, PitchBook, AlphaSights, etc.
├── SCHEMA: DOCUMENT_METADATA       ← Raw document intake records
├── SCHEMA: THUMPER_LAND            ← Raw deal/pipeline state exports
├── SCHEMA: GOM_JABBAR_LAND         ← Raw NDA workflow state exports
├── SCHEMA: GURNEY_LAND             ← Raw CRM/contact state exports
├── SCHEMA: SARDAUKAR_LAND          ← Raw DD queue state exports
├── SCHEMA: MENTAT_LAND             ← Raw financial model outputs
├── SCHEMA: REVEREND_MOTHER_LAND    ← Raw memo draft and section exports
├── SCHEMA: LANDSRAAD_LAND          ← Raw IC session, annotation, vote exports
├── SCHEMA: CHOAM_LAND              ← Raw term/agreement state exports
├── SCHEMA: HEIGHLINER_LAND         ← Raw syndication, allocation, agency state exports
├── SCHEMA: ATREIDES_LAND           ← Raw closing task and funds flow exports
├── SCHEMA: STILLSUIT_LAND          ← Raw loan ledger event exports
├── SCHEMA: CORRINO_LAND            ← Raw portfolio monitoring state exports
└── SCHEMA: MELANGE_LAND            ← Raw valuation workflow state exports

ARRAKIS_CURATED (Snowflake Database — "Silver")
│
├── SCHEMA: DEALS                   ← Cleansed, normalized deal entities
├── SCHEMA: COMPANIES               ← Cleansed company/sponsor/borrower entities
├── SCHEMA: CONTACTS                ← Cleansed contact entities
├── SCHEMA: FACILITIES              ← Cleansed facility and tranche records
├── SCHEMA: DOCUMENTS               ← Document registry (metadata only)
├── SCHEMA: DD_ACTIVITY             ← Normalized diligence question/response log
├── SCHEMA: FINANCIAL_DATA          ← Normalized financial statement data
├── SCHEMA: LOAN_EVENTS             ← Normalized payment, amendment, covenant events
├── SCHEMA: IC_ACTIVITY             ← Normalized annotation, vote, decision records
├── SCHEMA: NDA_ACTIVITY            ← Normalized NDA workflow and execution records
├── SCHEMA: TERMS_ACTIVITY          ← Normalized term sheet negotiation and agreement records
├── SCHEMA: SYNDICATION_ACTIVITY    ← Normalized co-lender allocation, commitment records
├── SCHEMA: CLOSING_ACTIVITY        ← Normalized closing task and funding confirmation records
├── SCHEMA: MEMO_ACTIVITY           ← Normalized memo draft, section, and review records
└── SCHEMA: EXTERNAL_MARKET         ← Cleaned/enriched external market data

ARRAKIS_CONSUMPTION (Snowflake Database — "Gold")
│
├── SCHEMA: MDM                     ← Golden records: Deal, Company, Sponsor, Borrower,
│                                     Facility, Contact, Document (authoritative master data)
├── SCHEMA: DEAL_PIPELINE           ← Deal lifecycle views for origination BI
├── SCHEMA: PORTFOLIO_ANALYTICS     ← Portfolio composition, performance, concentration
├── SCHEMA: COVENANT_TRACKING       ← Rolling covenant calculations, headroom views
├── SCHEMA: VALUATION_OUTPUTS       ← Fair value determinations by position and period
├── SCHEMA: IC_AUDIT                ← Immutable IC decision and voting audit trail
├── SCHEMA: SYNDICATION             ← Co-lender allocation and commitment tracking
├── SCHEMA: LP_REPORTING            ← LP/board reporting outputs (Melange outputs)
├── SCHEMA: NDA_COMPLIANCE          ← NDA obligation tracking and compliance status
├── SCHEMA: CLOSING_STATUS          ← Closing checklist progress and funding status
└── SCHEMA: DATA_QUALITY            ← Data quality scores and SLA metrics per data product
```

Every application that produces structured state passes through an explicit RAW landing schema before curation. The principle of "one pipeline per application state" applies: each app gets exactly one landing schema, and the pipeline from that landing schema branches into the relevant curated schemas. The CURATED layer holds normalized per-domain entities (DEALS, NDA_ACTIVITY, TERMS_ACTIVITY, SYNDICATION_ACTIVITY, CLOSING_ACTIVITY, MEMO_ACTIVITY, etc.) needed to support the full deal lifecycle. The CONSUMPTION layer adds operational reporting schemas (NDA_COMPLIANCE, CLOSING_STATUS) and the DATA_QUALITY schema, which stores quality score time series for the Foldspace Observatory (Section 5).

The MDM system feeds into a source the data warehouse team uses to populate dimension tables and plays an interim role between the Silver and Gold layers: curated schemas hold per-domain entities, and the MDM schema in consumption holds the deduplicated, cross-reconciled golden records.

Snowflake Dynamic Tables are the primary mechanism for automating Silver → Gold materialization for analytical workloads (covenant calculations, portfolio metrics). Snowflake Streams + Tasks are preferred for event-driven propagation (e.g., tailing the loan events stream to trigger covenant recalculation).

**Snowflake TIME_TRAVEL and FAIL_SAFE retention policy:**

| Database | TIME_TRAVEL Retention | FAIL_SAFE | Rationale |
|---|---|---|---|
| ARRAKIS_RAW | 14 days | 7 days (Snowflake default) | Raw landing data must be available for replay and investigation when the Observatory detects freshness or volume anomalies. 14 days covers two full weekly reporting cycles and aligns with the 7-day Redpanda event retention window plus margin for delayed discovery. |
| ARRAKIS_CURATED | 7 days | 7 days | Curated data is derived from RAW and can be recomputed. 7-day TIME_TRAVEL supports short-term debugging of transformation errors in dbt models without the storage cost of longer retention on a frequently refreshed tier. |
| ARRAKIS_CONSUMPTION | 90 days | 7 days | Consumption-layer data serves regulatory, audit, and LP reporting workloads. 90-day TIME_TRAVEL enables point-in-time queries for quarterly close processes (e.g., "what did the COVENANT_TRACKING schema show as of Q3 close?") and satisfies audit reconstruction requirements. The IC_AUDIT schema is additionally protected by append-only immutability. (Note: 90-day TIME_TRAVEL requires Snowflake Enterprise Edition or higher; confirm provisioning with infrastructure lead before publishing.) |

These retention settings are applied via schemachange migration scripts (`ALTER DATABASE ... SET DATA_RETENTION_TIME_IN_DAYS`) and enforced in the CI/CD pipeline as a blocking check: any schemachange migration that reduces TIME_TRAVEL below the defined minimum for its tier is rejected.

### Master Data Entities and Governance Ownership

The MDM system contains the golden records together with their lineage and the full history of how they got to that point. For Arrakis, the master entities, their originating golden-source applications, and their historization strategies are:

| Entity | Golden Source App | MDM Steward | Resolution Strategy | Historization |
|---|---|---|---|---|
| Deal | Thumper (origination) | Deal Team | Thumper creates Deal record; all other apps reference by `deal_id` | SCD Type 2 |
| Company | Gurney (CRM) | Relationship Manager | Gurney deduplicates; enriched from PitchBook/Cap IQ via Foldspace | SCD Type 2 |
| Sponsor | Gurney | Relationship Manager | Same as Company; Sponsor is a Company subtype | SCD Type 2 |
| Borrower | Gurney (pre-close) / Stillsuit (post-close) | Deal Team / Ops | Gurney creates; Stillsuit takes operational ownership post-funding | SCD Type 2 |
| Facility | CHOAM (terms) → Stillsuit (operations) | Deal Team / Ops | CHOAM defines; Stillsuit becomes authoritative post-close | SCD Type 2 |
| Contact | Gurney | Relationship Manager | Gurney deduplicates against email/phone/organization | SCD Type 2 |
| Document | Foldspace Document Registry | Platform Team | All apps publish to Foldspace; document entity is centrally owned | SCD Type 2 |

All master data entities use SCD Type 2 historization. Every update to a master entity record inserts a new row with `valid_from` / `valid_to` timestamps and an `is_current` flag. The previous version's `valid_to` is set to the new version's `valid_from`. This enables point-in-time reconstruction of any entity's state — critical for audit, regulatory, and LP reporting purposes where the question "what did we know about this borrower as of Q3 close?" must be answerable.

#### Golden-Source Ownership Transfer Protocol

The two master data entities with lifecycle ownership transitions — Borrower and Facility — require an explicit transfer event to move golden-source authority between applications. The Foldspace Master Data API enforces the following protocol:

**Triggering Events:**

- **Facility:** When Atreides completes the funding handoff (`funding_confirmation` record written successfully and Stillsuit acknowledges via `POST /loans/activate`), the Foldspace Master Data API automatically transitions Facility golden-source authority from CHOAM to Stillsuit. The trigger is the existing `funding.confirmed` event — no new event source is required, but the MDM API must subscribe to this event and execute the authority transfer as a side effect.
- **Borrower:** Same trigger. Upon successful funding confirmation, Borrower golden-source authority transfers from Gurney to Stillsuit. Gurney retains read access and continues to publish enrichment data (e.g., PitchBook/Cap IQ updates), but the MDM conflict resolution tie-breaker shifts to Stillsuit per the existing conflict protocol.

**Transfer Validation Preconditions** (enforced by MDM API before accepting the transfer):

- The target entity's current SCD Type 2 record must have `is_current = TRUE` and must pass referential integrity checks (valid `deal_id`, `facility_id`).
- The receiving app (Stillsuit) must have an active data contract (DCA `status = active`) for the entity's data product.
- No unresolved MDM conflict (`status = open`) may exist for the entity at transfer time. If an open conflict exists, the transfer is blocked and an alert is raised.

**Transfer Execution:**

1. The MDM API writes a new SCD Type 2 row with `golden_source_app` updated to the receiving app and `transfer_event_id` referencing the triggering `funding.confirmed` event.
2. The MDM API emits a `master-data.ownership-transferred` event to Redpanda with payload `{entity_type, entity_id, from_app, to_app, transfer_event_id, effective_at}`.
3. The MDM conflict resolution rules for the entity are updated: the tie-breaker app changes from the originating app to the receiving app (i.e., Stillsuit becomes authoritative for Borrower and Facility conflicts post-transfer, per the existing conflict protocol table).

**Reversal:** Ownership transfers are not reversible through the API. If an operational error requires reverting authority (e.g., a funding unwind), the platform team must execute a manual correction with a runbook entry and a `master-data.ownership-corrected` event for audit.

#### MDM Conflict Resolution Protocol

| Entity | Conflict Scenario | Tie-Breaker | Resolution SLA | Logging |
|---|---|---|---|---|
| Borrower | Gurney and Stillsuit disagree on legal name, address, or classification post-funding | Stillsuit (as post-close system of record) | 4 business hours | Conflict event emitted to Redpanda topic `mdm.conflict-raised`; resolution event emitted to `mdm.conflict-resolved`; both written to `ARRAKIS_RAW.APP_EVENTS` with `conflict_id`, `entity_type`, `conflicting_apps`, `resolution`, `resolver_user_id` |
| Facility | CHOAM and Stillsuit disagree on facility economics or terms post-close | Stillsuit (authoritative post-close); CHOAM retains authority pre-close | 4 business hours | Same logging pattern |
| Company / Sponsor | Multiple apps submit conflicting enrichment data | Gurney (golden source) | 8 business hours | Same logging pattern; data steward review required |
| Contact | Deduplication conflict between auto-merge and manual override | Gurney (with data steward manual review) | 8 business hours | Same logging pattern |

All master data writes go through a Foldspace Master Data API — apps never write directly to the Snowflake MDM schema. The Master Data API performs deduplication checks, assigns canonical entity IDs, and emits `master-data-updated` events to Redpanda.

#### Downstream Reconciliation Contract

When the MDM Conflict Resolution Protocol resolves a conflict, the losing app must reconcile its local PostgreSQL state with the resolved golden record. The following contract applies to all apps that participate in MDM conflict scenarios:

1. **Subscription Requirement:** Every app named as a potential conflict participant in the MDM Conflict Resolution Protocol table must subscribe to the `mdm.conflict-resolved` Redpanda topic and implement a handler for conflicts involving its entity types.
2. **Reconciliation Handler Behavior:** Upon receiving a `mdm.conflict-resolved` event where the app is the losing party (`resolution.losing_app == self`), the handler must:
   - Fetch the resolved golden record from the Foldspace Master Data API (`GET /foldspace/v1/master-data/{entity_type}/{entity_id}`).
   - Update the app's local PostgreSQL record to align with the resolved fields. The update must go through the app's standard domain model write path (service layer → repository → UoW) to ensure local business rules and audit logging are preserved.
   - Emit a local `master-data.locally-reconciled` event to the app's outbox with `{entity_type, entity_id, conflict_id, reconciled_fields[], reconciled_at}`.
3. **Reconciliation SLA:** The losing app must complete local reconciliation within 30 minutes of the `mdm.conflict-resolved` event timestamp. The Foldspace Observatory monitors reconciliation lag as a freshness dimension on the losing app's master data consumption.
4. **Reconciliation Failure Handling:** If the local update fails (e.g., the resolved value violates a local constraint), the handler must not silently drop the event. Instead, it must write a `master-data.reconciliation-failed` event to its outbox with `{conflict_id, entity_type, entity_id, failure_reason}` and alert the data steward. The entity remains in a reconciliation-pending state in the app's local store until manual resolution.

#### Master Data API — Domain Invariants by Entity

The Foldspace Master Data API enforces the following domain invariants at write time, implemented as Pydantic validators on the request models in `foldspace/api/master_data/validators.py`. A write that violates any invariant is rejected with `422 Unprocessable Entity` before the record is persisted or any event is emitted.

**Deal:**
- `deal_id` must be a valid UUID.
- `originating_app` must be `thumper` (only Thumper may create Deal records).
- `deal_name` must be non-empty and ≤ 255 characters.
- `status` must be in the canonical deal status enum (`{pipeline, active, approved, closing, funded, declined, withdrawn}`).
- A Deal with status `funded` may not be created directly — it must transition through the status lifecycle.

**Company / Sponsor:**
- `legal_entity_name` must be non-empty.
- `jurisdiction` must be a valid ISO 3166-1 alpha-2 code.
- Deduplication check: if a Company with matching `tax_id` or matching (`legal_entity_name`, `jurisdiction`) tuple already exists and `is_current = TRUE`, the write is treated as an update, not a create. New `company_id` assignment is blocked.
- Sponsor is validated as a Company subtype; the `is_sponsor` flag and `fund_name` field are required for Sponsor records.

**Borrower:**
- All Company invariants apply (Borrower is a Company subtype in the MDM model).
- `tax_id` is required (nullable for pipeline-stage deals only when `deal.status = 'pipeline'`; becomes mandatory when `deal.status` transitions to `active`).
- `kyc_aml_status` must be in `{pending, cleared, flagged, expired}`.

**Facility:**
- `deal_id` must reference an existing Deal with `is_current = TRUE`.
- `facility_type` must be in `{revolver, term_loan, delayed_draw, bridge}`.
- `commitment_amount` must be positive.
- `currency` must be a valid ISO 4217 code.
- `maturity_date` must be after the current date at creation time.
- A Facility may not be created unless the parent Deal's status is `approved` or later.

**Contact:**
- At least one of `email`, `phone`, or `organization_id` must be non-null (deduplication requires at least one matchable field).
- `email`, if present, must be a valid email format.

**Document:**
- `document_type` must be in the canonical document type enum.
- `s3_key` must be non-empty and must follow the versioned key pattern `{type}/{deal_id}/{version_id}/{timestamp}.{ext}`.
- `deal_id` must reference an existing Deal.

### Integration Layer Architecture

#### Internal API Gateway — Kong (OSS)

Kong as the API gateway in front of all Foldspace endpoints provides authentication/JWT validation, rate limiting, request logging, API versioning, and the plugin ecosystem for OAuth2. Kong is mature OSS, well-supported, and avoids the cost of AWS API Gateway at scale. All 13 apps communicate with Foldspace exclusively through Kong — they never make direct database connections to Snowflake or PostgreSQL outside their own domain.

#### Foldspace Client Library — Resilience Defaults

The shared `foldspace_client` Python library (located at `shared/foldspace_client/`) is the sole permitted mechanism for app-to-Foldspace synchronous API calls. All 13 domain apps import this client; no app may use raw `httpx` or `requests` to call Foldspace endpoints directly. The client enforces the following resilience defaults, derived from the SLA targets registered in the API Catalog:

| Parameter | Default | Override | Rationale |
|---|---|---|---|
| Connect timeout | 1s | Per-endpoint via API Catalog | Fail fast on unreachable Foldspace; pick a default timeout for everything |
| Read timeout | Endpoint SLA p95 × 2 (e.g., 1s for a 500ms SLA) | Per-endpoint | Allows headroom above normal latency without waiting indefinitely |
| Retry policy | 2 retries with exponential backoff (base 500ms, jitter ±100ms) on 503/504 only | Per-endpoint | Retries only on transient errors; 4xx errors fail immediately |
| Overall operation budget | 5s (user-facing) / 30s (background task) | Per-callsite | Set a timeout for the overall operation, and abort if exceeded |
| Connection pool | Separate `httpx.AsyncClient` per Foldspace endpoint category (MDM, Documents, IC, Funding, Deal Context) | Not overridable | Bulkhead isolation: a slow MDM call cannot exhaust connections needed for funding |
| Circuit breaker | Opens after 5 consecutive failures within 120s; half-open after 60s; 1 probe request | Per-endpoint | Funding handoff already uses 3/60s/30s (Section 3); general endpoints use a less aggressive default |

The client logs every timeout, retry, and circuit-breaker state transition to structlog with `endpoint_uri`, `app_id`, `deal_id`, and `trace_id` fields. Circuit breaker state changes also emit a `foldspace-client.circuit-state-changed` metric to Prometheus for Grafana alerting.

When a circuit breaker is open, the client raises `FoldspaceCircuitOpenError` with a `retry_after_seconds` attribute. Each app's service layer must handle this error explicitly — the handling strategy (queue-for-retry, show degraded UI, alert operator) is documented in the app's operational runbook.

#### Foldspace API Catalog

APIs are treated as products with formal API contracts and API discoverability. The Foldspace API Catalog is a named Foldspace component — a PostgreSQL-backed FastAPI service — that stores for every endpoint:

| Field | Description |
|---|---|
| `endpoint_uri` | Full URI path (e.g., `/foldspace/v1/funding-confirmed`) |
| `version` | Current major.minor version (e.g., `v1.2`) |
| `owner_app` | The application that owns and maintains this endpoint |
| `consuming_apps` | List of applications with registered consumption contracts |
| `sla_p95_latency_ms` | p95 latency target in milliseconds |
| `sla_availability` | Availability target (e.g., `99.9%`) |
| `deprecation_status` | `active`, `deprecated`, or `sunset` |
| `deprecation_notice_date` | Date deprecation was announced (minimum 90-day notice) |
| `sunset_date` | Date after which the endpoint will be decommissioned |
| `pydantic_schema_ref` | Reference to the Pydantic model in `shared/schemas/` |
| `is_external` | Boolean flag for external API products (CapIQ, PitchBook, etc.) |
| `error_schema_ref` | Reference to the standard Foldspace error response Pydantic model in `shared/schemas/errors.py` |

External connectors (CapIQConnector, PitchBookConnector, AlphaSightsConnector, GLGConnector, NAICSConnector, ChronographConnector) are registered in the API Catalog as external API products with the same version and SLA metadata as internal endpoints. This places external integrations under the same SLA accountability as internal endpoints.

#### Standard Error Response Contract

All Foldspace API endpoints return errors using a single Pydantic model registered at `shared/schemas/errors.py`:

```python
class FoldspaceError(BaseModel):
    status: int                  # HTTP status code (mirrored in body for client convenience)
    error_code: str              # Machine-readable code scoped to Foldspace (e.g., "FUNDING_DUPLICATE_IDEM
    message: str                 # Human-readable summary safe for logging (no PII, no stack traces)
    detail: str | None = None    # Optional extended explanation for 4xx errors
    trace_id: str                # OpenTelemetry trace ID for cross-service correlation
    timestamp: datetime          # UTC ISO-8601 timestamp of the error occurrence
```

Rules: (a) Every 4xx and 5xx response from a Foldspace endpoint must conform to this model. (b) The `error_code` field uses a dot-namespaced vocabulary maintained in `shared/schemas/error_codes.py` — Claude Code must select from this vocabulary, never invent ad hoc codes. (c) The `message` field must never contain deal financials, borrower PII, or stack traces; the `detail` field is stripped by Kong before any response crosses the Heighliner tenant boundary. (d) 5xx responses omit the `detail` field entirely to avoid leaking internal state.

#### API Endpoint SLA Conformance — Observatory Dimension

| Dimension | What Is Monitored | Alert Threshold | Implementation |
|---|---|---|---|
| API SLA | p95 latency and error rate per Foldspace API endpoint registered in the API Catalog | p95 latency exceeds `sla_p95_latency_ms` from the API Catalog for three consecutive 5-minute windows; error rate (5xx / total) exceeds 1% sustained over 5 minutes; availability drops below `sla_availability` in any rolling 24-hour window | A Prometheus recording rule computes per-endpoint p95 latency and error rate from prometheus-fastapi-instrumentator histograms. The Observatory polls these recording rules every 5 minutes, compares against the API Catalog's SLA targets (fetched from the Catalog API), and writes breach records to `ARRAKIS_CONSUMPTION.DATA_QUALITY` with `dimension = 'api_sla'`. Breach events are emitted to Redpanda on the existing `data-quality.sla-breach` topic. The same four-tier escalation path (Slack → PagerDuty → platform lead → head of technology) applies. |

The Observatory's API SLA dimension (Section 5.4) continuously validates actual endpoint performance against these targets; breaches follow the standard Observatory escalation path.

### External Integration Connector Framework

Point-to-point integrations are avoided in favor of treating APIs as products. The external connector architecture uses an abstract `BaseConnector` Python class that standardizes:

- Authentication (OAuth2, API key, JWT)
- Rate limiting and retry logic (exponential backoff)
- Response normalization to Arrakis canonical schemas
- Error handling and dead-letter logging to Snowflake

Concrete connectors: `CapIQConnector`, `PitchBookConnector`, `AlphaSightsConnector`, `GLGConnector`, `NAICSConnector`, `ChronographConnector`. New integrations require only a new connector class — no structural rework. Each connector must register its external API in the API Catalog upon deployment.

#### BaseConnector Resilience Profile

Every concrete connector inherits the following resilience defaults from `BaseConnector`, configurable per-connector via environment variables:

| Parameter | Default | Description |
|---|---|---|
| `max_retries` | 3 | Maximum retry attempts per request before the call is marked as failed. Retries use exponential backoff with jitter (base 1s, multiplier 2×, jitter ±500ms). Only 429 (rate limited) and 5xx responses trigger retries; 4xx client errors do not. |
| `request_timeout_s` | 30 | Per-request timeout in seconds. Includes connection establishment and response read. |
| `total_timeout_s` | 120 | Total timeout budget for a single logical operation including all retries. Prevents unbounded retry chains when backoff intervals accumulate. |
| `circuit_breaker_threshold` | 5 | Consecutive failures within `circuit_breaker_window_s` that trip the breaker to OPEN state. |
| `circuit_breaker_window_s` | 120 | Sliding window for counting consecutive failures. |
| `circuit_breaker_recovery_s` | 60 | Time in OPEN state before transitioning to HALF-OPEN and allowing a single probe request. |
| `rate_limit_rps` | Connector-specific | Maximum outbound requests per second to the external provider. Connectors calling metered APIs (CapIQ, PitchBook) must set this to the provider's contractual rate limit minus a 10% safety margin. |

When the circuit breaker is OPEN, the connector immediately returns a structured error (using the standard `FoldspaceError` model) with `error_code = "EXTERNAL_PROVIDER_CIRCUIT_OPEN"` and logs a structlog warning with `{connector_name, provider, circuit_state, deal_id}`. The failed request payload is written to the connector's dead-letter table in Snowflake (`ARRAKIS_RAW.EXTERNAL_FEEDS.dead_letter_{connector_name}`) for manual replay after provider recovery. The circuit breaker state for each connector is exposed as a Prometheus gauge (`foldspace_connector_circuit_state{connector="..."}`) for Observatory and Grafana alerting.

#### BaseConnector Observability Contract

Every concrete connector inherits the following observability requirements from `BaseConnector`:

**Metrics** (exposed via prometheus-fastapi-instrumentator or a dedicated Prometheus collector on the Foldspace backend):

- `foldspace_connector_requests_total{connector, provider, endpoint, status_class}` — counter of outbound requests, labeled by HTTP status class (2xx, 4xx, 5xx).
- `foldspace_connector_request_duration_seconds{connector, provider, endpoint}` — histogram of request durations (including retries).
- `foldspace_connector_circuit_state{connector, provider}` — gauge: 0 = CLOSED, 1 = HALF-OPEN, 2 = OPEN.
- `foldspace_connector_rate_limit_remaining{connector, provider}` — gauge tracking the provider's `X-RateLimit-Remaining` header value (where available).

**Structured Logs** (via `structlog`, extending the mandatory field set): every outbound call logs `{connector_name, provider, endpoint, http_method, http_status, latency_ms, retry_attempt, deal_id, trace_id}`. Failed calls additionally log `{error_code, circuit_state, dead_letter_written}`.

**Traces** (via OpenTelemetry SDK): each outbound HTTP call creates a child span under the calling Foldspace operation's trace, with span attributes `{connector.name, connector.provider, http.method, http.status_code, http.url}`. This ensures Jaeger traces show external API latency as a distinct segment of the end-to-end request path.

The Observatory's API SLA dimension consumes the connector-level Prometheus metrics to detect provider degradation. A Grafana dashboard ("External Provider Health") displays per-connector rate, error rate, p95 latency, circuit breaker state, and rate-limit headroom. This dashboard is added to the five existing SLA monitoring dashboards specified in Section 6.3.

### MCP Server — Foldspace MCP

A Python MCP server (`foldspace-mcp`) exposes structured tools to Claude for agentic drafting workflows. Tools include: `get_deal_context(deal_id)`, `search_documents(deal_id, query)`, `get_financial_metrics(company_id, period)`, `get_dd_findings(deal_id)`, `get_facility_terms(facility_id)`, `get_portfolio_position(facility_id)`. This server runs as a sidecar process during Claude Code agentic tasks and is also the production interface used by Reverend Mother, CHOAM, and Mentat when invoking Claude. (Expanded tool catalog detailed in Section 7.)

### Event Bus — Redpanda

Core topic taxonomy:

- `deal.created` / `deal.stage-changed` / `deal.closed`
- `nda.received` / `nda.executed` / `nda.expired` / `nda.obligation-flagged`
- `triage-memo.completed`
- `ic.submitted` / `ic.approved` / `ic.conditions-set` / `ic.session-closed`
- `terms.agreed` / `ca.executed`
- `syndication.allocation-updated` / `syndication.commitment-confirmed`
- `closing.task-completed` / `funding.confirmed`
- `loan.payment-received` / `loan.amendment-executed` / `loan.covenant-breach`
- `loan.agent-notice-received` / `loan.reconciliation-discrepancy`
- `document.uploaded` / `document.executed`
- `financial-data.received` / `financial-data.validated`
- `valuation.cycle-initiated` / `valuation.approved` / `valuation.published`
- `mdm.conflict-raised` / `mdm.conflict-resolved`
- `master-data-updated`
- `master-data.ownership-transferred` / `master-data.ownership-corrected`
- `master-data.locally-reconciled` / `master-data.reconciliation-failed`
- `data-quality.sla-breach` / `data-quality.gate-failed`
- `data-quality.upstream-breach-active` / `data-quality.upstream-breach-resolved`
- `data-contract.approved` / `data-contract.deprecated` / `data-contract.revoked`
- `data-contract.version-created` / `data-contract.major-version-created`
- `data-contract.review-triggered` / `data-contract.status-changed`

All topics use structured Avro schemas. Consumer groups are per-application. Snowpipe Streaming tails all topics into `ARRAKIS_RAW.APP_EVENTS`. The topic taxonomy includes events for NDA obligations (Gom Jabbar feature parity with Ironclad obligation management), syndication state changes (Heighliner feature parity with Debtdomain/SyndTrak allocation tracking), agent notices (Stillsuit feature parity with WSO agent notice processing), data quality alerts (Foldspace Observatory), and MDM conflict resolution events.

**Topic retention and compaction policy.** All Redpanda topics follow one of two retention profiles:

| Profile | Applicable Topics | Retention | Compaction | Rationale |
|---|---|---|---|---|
| Event retention | All workflow and activity event topics: `deal.*`, `nda.*`, `triage-memo.*`, `ic.*`, `terms.*`, `syndication.*`, `closing.*`, `funding.*`, `loan.*`, `document.*`, `financial-data.*`, `valuation.*`, `data-quality.*`, `master-data.ownership-transferred`, `master-data.ownership-corrected`, `master-data.locally-reconciled`, `master-data.reconciliation-failed`, `data-contract.approved`, `data-contract.deprecated`, `data-contract.revoked`, `data-contract.version-created`, `data-contract.major-version-created`, `data-contract.review-triggered`, `data-contract.status-changed`, `data-quality.upstream-breach-active`, `data-quality.upstream-breach-resolved` | 7 days (time-based) | Disabled | These topics contain immutable event facts. 7-day retention provides sufficient replay window for Snowpipe recovery, consumer reprocessing after failure, and dead-letter replay. Events older than 7 days are available in `ARRAKIS_RAW.APP_EVENTS` (Snowflake) for historical access. |
| Compacted entity state | `master-data-updated`, `mdm.conflict-raised`, `mdm.conflict-resolved` | Indefinite (log-compacted) | Enabled (keyed on `entity_type` + `entity_id`) | These topics represent the current state of master data entities. Log compaction retains only the latest event per entity key, enabling new consumers to bootstrap a full MDM snapshot from the compacted log without querying Snowflake. |

Topic-level configuration is applied via the Redpanda admin API during Helm chart deployment and enforced in the CI/CD pipeline. Any new topic must declare its retention profile in its Avro schema registration metadata.

**Schema Compatibility Mode.** The Redpanda Schema Registry enforces FULL compatibility as the global default for all subjects. FULL compatibility (the union of forward and backward compatibility) ensures that (a) consumers using an older schema version can read events produced with a newer schema, and (b) consumers using a newer schema can read events produced with an older schema. This is the strongest guarantee and the appropriate default for a financial-services event bus where schema changes must not break any of the 13 consuming applications or the Snowpipe Streaming connector. Per-topic compatibility overrides (e.g., relaxing to BACKWARD for high-churn internal topics) require explicit approval from the data steward and registration in the DCA as a contract amendment. The CI/CD pipeline validates schema compatibility before any producer deployment (see Section 6.1).

**Outbox relay producer configuration** (all 13 apps): The relay process that publishes outbox events to Redpanda must use the following producer settings:

- `acks=all` — the producer waits for all in-sync replicas to acknowledge the write before marking the outbox row as published. This prevents data loss if the Redpanda leader crashes immediately after accepting the write.
- `enable.idempotence=true` — the producer attaches sequence numbers to each record, allowing the broker to deduplicate retries. This eliminates duplicate events caused by network timeouts during relay publishing.
- `delivery.timeout.ms=120000` (2 minutes) — sets the upper bound on total time for a produce request including retries, providing a bounded failure window before the relay falls back to the dead-letter path.
- `max.in.flight.requests.per.connection=5` — required maximum when idempotence is enabled; preserves ordering guarantees per partition.

**Topic-level reliability configuration** (all 28 topics): Each Redpanda topic is created with `replication.factor=3` and `min.insync.replicas=2`. This ensures that committed events survive any single-broker failure and that the producer receives an error (rather than silently losing data) if fewer than two replicas are available. Topics carrying financial events (prefixed `loan.*`, `funding.*`, `closing.*`) and governance events (`ic.*`, `mdm.*`) are flagged as critical in the Redpanda topic configuration and subject to alerting if ISR count drops below 3.

**Consumer group operational baseline** (all 13 apps): Each application's Redpanda consumer must adhere to the following configuration:

- `partition.assignment.strategy=cooperative-sticky` — uses cooperative (incremental) rebalancing to avoid full stop-the-world pauses when consumers restart, scale, or deploy. This is critical in a 14-service cluster where rolling deployments are frequent.
- `enable.auto.commit=false` — offsets are committed explicitly by the application after successful processing, aligning with the idempotent consumer contract. This prevents committed offsets from advancing past unprocessed records.
- `auto.offset.reset=earliest` — when a consumer group encounters an invalid or absent committed offset, it reads from the beginning of the partition rather than skipping to the latest. In a financial system, missing events is worse than reprocessing (which the idempotent consumer contract handles safely).
- `session.timeout.ms=30000` (30 seconds) — balances timely failure detection with tolerance for GC pauses and transient network issues.
- `heartbeat.interval.ms=10000` (10 seconds) — ensures three heartbeats per session timeout window, the recommended minimum.
- `max.poll.interval.ms=300000` (5 minutes) — accommodates consumers that perform Snowflake writes or Foldspace API calls within their processing loop.

These values are codified as a shared `RedpandaConsumerConfig` Pydantic model in the Foldspace client library, ensuring consistency across all 13 applications. Per-app overrides require justification in the app's `CLAUDE.md` and registration as a deviation in the DCA.

**Partition key strategy.** Every Redpanda topic uses a deterministic partition key derived from the primary business entity it represents. Topics within the same entity domain use the same key and identical partition count to enable copartitioned consumption without repartitioning.

| Topic Category | Partition Key | Partition Count | Rationale |
|---|---|---|---|
| `deal.*` | `deal_id` | 12 | All deal lifecycle events ordered per deal |
| `nda.*` | `deal_id` | 12 | NDA events copartitioned with deal events for Gom Jabbar processing |
| `triage-memo.completed` | `deal_id` | 12 | Memo tied to deal; copartitioned with deal topics |
| `ic.*` | `deal_id` | 12 | IC workflow copartitioned with deal lifecycle |
| `terms.*`, `ca.*` | `deal_id` | 12 | Terms and credit agreement events copartitioned with deal lifecycle |
| `syndication.*` | `deal_id` | 12 | Syndication allocation ordered per deal |
| `closing.*`, `funding.*` | `deal_id` | 12 | Closing and funding events copartitioned with deal lifecycle |
| `loan.*` | `facility_id` | 12 | Post-close loan servicing events ordered per facility for Stillsuit and Corrino |
| `document.*` | `deal_id` | 12 | Document events copartitioned with deal lifecycle |
| `financial-data.*` | `company_id` | 6 | Financial data ordered per company for Mentat processing |
| `valuation.*` | `deal_id` | 12 | Valuation events copartitioned with deal lifecycle |
| `mdm.*` | `entity_type:entity_id` | 6 | MDM events ordered per master entity |
| `master-data-updated` | `entity_type:entity_id` | 6 | Copartitioned with MDM conflict topics |
| `data-quality.*` | `data_product_id` | 3 | Low-volume operational events; ordering per data product |

The partition count of 12 for deal-centric topics accommodates the current 13-application consumer base with headroom for scaling. The Snowpipe Streaming connector uses a dedicated consumer group with all partitions assigned, consuming from all topics into `ARRAKIS_RAW.APP_EVENTS`. Partition counts must not be changed after initial topic creation without a coordinated migration plan, as key-to-partition mapping changes when partition count changes.

**Observatory — Event Bus Lag Dimension.** The Foldspace Observatory adds a sixth monitoring dimension covering Redpanda consumer group health:

| Dimension | What Is Monitored | Alert Threshold | Implementation |
|---|---|---|---|
| Event Bus Lag | Consumer offset lag per consumer group per topic partition | Lag exceeds 1,000 events for >5 minutes OR lag growth rate is positive for >10 consecutive measurements | Observatory polls the Redpanda Admin API (`/v1/consumer/offsets`) every 60 seconds, computes per-group lag, writes measurements to `ARRAKIS_CONSUMPTION.DATA_QUALITY`, and emits `data-quality.sla-breach` event to Redpanda if threshold is exceeded |

**Lag alert routing:** Event bus lag alerts follow the same escalation path as existing Observatory alerts (Slack → PagerDuty → platform lead → head of technology). The alert payload includes `consumer_group`, `topic`, `partition`, `current_lag`, `lag_velocity` (events/minute growth rate), and `estimated_catchup_minutes` at current processing rate.

**Snowpipe Streaming connector lag:** The Snowpipe Streaming consumer group (which tails all topics into `ARRAKIS_RAW.APP_EVENTS`) is monitored as a dedicated consumer group. Lag on this group directly predicts Snowflake freshness SLA breaches and is treated as a leading indicator for the existing freshness dimension.

**Grafana dashboard:** A "Redpanda Consumer Health" dashboard is added to the existing Observatory dashboard set (Section 6.4), showing per-group lag time series, lag velocity, and rebalance event overlays.

**Breaking schema change deployment procedure.** When a schema change cannot satisfy FULL compatibility (as detected by the schema compatibility gate), the following dual-stream migration pattern applies:

1. **Create a new topic:** The producer creates a new topic with the naming convention `{original_topic}.v{N}` (e.g., `deal.created.v2`). The new schema is registered under the new topic's subject in the Schema Registry.
2. **Dual-publish:** The producer application is updated to publish events to both the original topic (using the old schema) and the new topic (using the new schema) simultaneously. This is implemented in the outbox relay by writing two rows to the outbox table per business event during the migration window.
3. **Consumer migration:** Each consuming application migrates to the new topic on its own release schedule. The migration is tracked in the DCA as a contract amendment, with a defined migration deadline (default: 30 days from dual-publish start).
4. **Snowpipe Streaming update:** The Snowpipe Streaming connector is updated to tail the new topic into `ARRAKIS_RAW.APP_EVENTS` alongside the original. Deduplication in the Bronze→Silver gate (using `event_id` from the standard envelope) prevents duplicate records.
5. **Original topic deprecation:** Once all consumers and the Snowpipe connector have migrated, the original topic is marked as deprecated. After the topic's retention period expires and all consumer groups have confirmed zero lag, the topic is deleted.
6. **Runbook:** Every breaking schema change requires a runbook in `docs/runbooks/` (per Section 8 `CLAUDE.md` convention item 10) documenting the migration plan, consumer list, timeline, and rollback procedure.

## 2. Data Product Design

This section specifies the data product owned by each application: what state it owns operationally, what it consumes, what it publishes, the historization strategy, classification, consumer list, and the quality gates at each tier transition. The aim is to give every Snowflake table a clear owner, a clear lifecycle, and a clear quality contract.

The foundational principle: no raw data. Data providers must model and serve data in such a way that it offers a best-in-class user experience and encapsulates the physical data model within domain boundaries. Each app owns its PostgreSQL inner state and publishes read-optimized, semantically clean data products to Snowflake landing schemas, from which the curated and consumption layers are built.

Each data product carries an explicit historization strategy, formal output port definitions (schema, SLA, quality SLA), data quality gates at Bronze→Silver and Silver→Gold transitions, a data classification tier, and a consuming app dependency list. One pipeline per application state: each app's full PostgreSQL operational state is exported through a single pipeline that branches into multiple output schemas at the curated layer. There are no separate pipelines for individual data products from the same app.

**Late-arriving event handling policy.** Events are classified as "late" when they arrive after the reporting period boundary to which they logically belong. Handling varies by historization strategy:

| Historization Strategy | Late-Arrival Handling | Rationale |
|---|---|---|
| Append-only | No special handling required. Late-arriving events are appended with their actual `event_timestamp` (when the event occurred) and `ingested_at` (when the pipeline processed it). Consumers querying by `event_timestamp` will see the event in its correct logical position; consumers querying by `ingested_at` will see it in its arrival order. Both timestamps are required fields in all append-only landing schemas. | Append-only logs are inherently tolerant of late arrivals — the event is simply a new row regardless of when it arrives. |
| Snapshot (YYYYMMDD) | Late-arriving data that pertains to a prior period triggers a restatement snapshot: a new snapshot row with the corrected values, tagged with `is_restated = TRUE`, `original_snapshot_date`, and `restated_at`. The prior snapshot is not modified (immutability preserved). The Silver→Gold gate validates that restated snapshots carry both the original and restated timestamps. The `ARRAKIS_CONSUMPTION` Dynamic Table for affected products (e.g., `COVENANT_TRACKING`, `VALUATION_OUTPUTS`) must use `COALESCE(restated_snapshot, original_snapshot)` logic to surface the most current values while preserving audit history. | Financial reporting and LP outputs require both the original and corrected views. Restatement-by-new-row preserves auditability while ensuring downstream consumers see current data. |
| SCD Type 2 | No special handling beyond the existing SCD Type 2 mechanism. A late-arriving update inserts a new version row with `valid_from` set to the event's logical timestamp (not the ingestion timestamp), and the prior row's `valid_to` is adjusted accordingly. The SCD Type 2 mechanism inherently handles temporal corrections. | SCD Type 2 is designed for exactly this case — retroactive state corrections are modeled as version chain adjustments. |

A data product's freshness SLA is measured against `ingested_at`, not `event_timestamp`. Late-arriving events do not retroactively breach the freshness SLA of the period they logically belong to — they are measured as timely if ingested within the SLA window of their arrival.

**Standard event envelope.** Every Avro event published to Redpanda must include a common envelope wrapping the domain-specific payload. The envelope is defined as a shared Avro record (`arrakis.common.EventEnvelope`) registered in the Schema Registry:

```json
{
  "type": "record",
  "name": "EventEnvelope",
  "namespace": "arrakis.common",
  "fields": [
    {"name": "event_id", "type": "string",
     "doc": "UUID v4, unique per event instance. Used for idempotent consumer deduplication."},
    {"name": "event_type", "type": "string",
     "doc": "Dot-delimited topic name, e.g. 'deal.created'. Enables filtering within APP_EVENTS."},
    {"name": "event_time", "type": "long",
     "logicalType": "timestamp-millis",
     "doc": "UTC timestamp of the business event occurrence (not relay publish time)."},
    {"name": "source_app", "type": "string",
     "doc": "Producing application name, e.g. 'thumper', 'sardaukar'. Matches app_id in structlog."},
    {"name": "deal_id", "type": ["null", "string"], "default": null,
     "doc": "Primary deal context. Null only for entity-level events (mdm.*, master-data-updated)."},
    {"name": "trace_id", "type": "string",
     "doc": "OpenTelemetry trace ID propagated from the originating API request."},
    {"name": "correlation_id", "type": "string",
     "doc": "Business correlation ID linking related events across apps (e.g., a deal lifecycle)."},
    {"name": "schema_version", "type": "int",
     "doc": "Monotonically increasing version of this event's domain-specific payload schema."},
    {"name": "payload", "type": "bytes",
     "doc": "Avro-serialized domain-specific payload. Schema identified by subject in the registry."}
  ]
}
```

The envelope is implemented as a Pydantic v2 `EventEnvelope` base class in the Foldspace client library. All 13 apps inherit from this class when constructing outbox events. The `event_time` field uses the PostgreSQL transaction timestamp (not wall-clock time at relay publish), preserving accurate event ordering through deterministic processing.

**Outbox serialization strategy — before-the-fact.** All 13 applications must Avro-serialize the event payload and validate it against the registered schema before writing to the `outbox_events` table. The serialization and outbox INSERT occur within the same PostgreSQL transaction as the business write. If serialization fails (schema incompatibility, missing required field, type mismatch), the entire transaction rolls back — the business write does not proceed, and no invalid event enters the outbox. This ensures that every row in the outbox table is a valid, pre-serialized Avro record ready for relay publishing without further transformation.

The `outbox_events` table schema includes a `payload_bytes` column (BYTEA) storing the pre-serialized Avro payload alongside the routing metadata (`target_topic`, `partition_key`, `schema_id`). The relay process publishes `payload_bytes` directly to Redpanda without re-serialization, eliminating a class of relay-time failures.

In the Foldspace client library, this is enforced by the `OutboxWriter.emit(event: EventEnvelope)` method, which performs Avro serialization via the `fastavro` library, validates against the cached schema, and executes the INSERT within the caller's database transaction context. A serialization failure raises `SchemaValidationError`, which the application must handle (typically by logging the error with full context and returning a 422 to the caller).

### Data Product Specifications by Application

#### Thumper — Deal Origination

| Attribute | Specification |
|---|---|
| Owns (PostgreSQL) | Pipeline stages, deal records, origination activity log, BDC filing ingests, competitor intelligence records |
| Consumes from Foldspace | MDM: Company, Sponsor, Contact; External: PitchBook, Cap IQ |
| Publishes to Foldspace | Deal entity (created/updated), origination event log, competitor intelligence records |
| Snowflake Automation | Stream on `THUMPER_LAND.deals` → Task updates `CURATED.DEALS` |
| Output Port: `THUMPER_LAND.*` | Schema: Avro-validated deal state export; Refresh SLA: 5-minute lag from PostgreSQL write; Quality SLA: 99.5% completeness on required fields; Freshness: ≤15 minutes from operational write |
| Historization | Deal entity: SCD Type 2 (master entity). Origination activity log: Append-only (event records). Competitor intelligence: Append-only (event records). BDC filing snapshots: Snapshot (YYYYMMDD partitioned) |
| Data Classification | Deal metadata: INTERNAL. Competitor intelligence: INTERNAL. Deal financial details (EV, pricing): CONFIDENTIAL |
| Consuming Apps | Gom Jabbar (deal reference), Sardaukar (deal context), Reverend Mother (memo inputs), Mentat (deal economics), CHOAM (deal reference), Heighliner (syndication context), Atreides (closing reference), Corrino (deal metadata), Melange (deal metadata) |
| Bronze→Silver Gate | Schema validation against `DealStateSchema` Pydantic model; null checks on `deal_id`, `deal_name`, `sponsor_id`, `stage`; referential integrity to MDM entity IDs for `sponsor_id` and `company_id` |
| Silver→Gold Gate | Business rule validation: deal stage must be in canonical stage enum; deduplication confirmation on `deal_id`; SLA freshness check (curated record within 30 minutes of raw) |

#### Gom Jabbar — NDA Workflow

| Attribute | Specification |
|---|---|
| Owns (PostgreSQL) | NDA document versions, negotiation turn log, approval records, execution status, deal permissions, NDA obligation tracking records, counterparty metadata extraction records |
| Consumes from Foldspace | MDM: Deal, Company, Sponsor; Documents: NDA templates |
| Publishes to Foldspace | NDA execution records, deal permission grants, NDA obligation status, NDA metadata extraction results |
| Snowflake Automation | Stream on `GOM_JABBAR_LAND.nda_records` → updates `CURATED.NDA_ACTIVITY` and `CURATED.DOCUMENTS` |
| Output Port: `GOM_JABBAR_LAND.*` | Refresh SLA: 5-minute lag; Quality SLA: 100% completeness on `deal_id`, `counterparty_id`, `execution_status`; Freshness: ≤10 minutes |
| Historization | NDA execution records: Append-only (immutable audit events). NDA obligation tracking: Append-only (obligation status changes are events). Deal permission grants: Append-only (grants are immutable events; revocations are new records) |
| Data Classification | NDA terms and counterparty identity: CONFIDENTIAL. NDA execution status: INTERNAL. Individual NDA negotiation positions: RESTRICTED |
| Consuming Apps | Thumper (deal access gating), Sardaukar (DD permission confirmation), Reverend Mother (deal permission check), all downstream apps (deal permission grants) |
| Bronze→Silver Gate | Schema validation; null checks on `deal_id`, `nda_id`, `counterparty_id`; referential integrity to MDM `deal_id` and `company_id` |
| Silver→Gold Gate | Business rule: NDA status must be in canonical status enum; obligation due dates must be future-dated at creation; freshness ≤15 minutes |

#### Gurney — Relationship Intelligence

| Attribute | Specification |
|---|---|
| Owns (PostgreSQL) | Contact profiles, organization records, interaction history, coverage assignments, follow-up tasks, activity capture log |
| Consumes from Foldspace | MDM: Deal, Company; Thumper: deal origination data; External: PitchBook, Cap IQ (enrichment) |
| Publishes to Foldspace | Contact and organization golden records (fed to MDM), interaction history, relationship maps |
| Snowflake Automation | Dynamic Table on contact deduplication; Stream triggers MDM update events |
| Output Port: `GURNEY_LAND.*` | Refresh SLA: 10-minute lag; Quality SLA: 99% completeness on `contact_id`, `org_id`, `email`; Freshness: ≤20 minutes |
| Historization | Contact profiles: SCD Type 2 (master entity). Organization records: SCD Type 2 (master entity). Interaction history: Append-only (events). Coverage assignments: SCD Type 2 (slowly-changing assignments) |
| Data Classification | Contact PII (email, phone, address): CONFIDENTIAL. Interaction history: INTERNAL. Coverage assignments: INTERNAL |
| Consuming Apps | Thumper (contact lookup), Gom Jabbar (counterparty contacts), Sardaukar (expert contacts), Reverend Mother (relationship context for memos), CHOAM (counterparty contacts) |
| Bronze→Silver Gate | Schema validation; null checks on `contact_id`, `org_id`; email format validation; referential integrity to MDM `company_id` |
| Silver→Gold Gate | Deduplication confirmation (fuzzy match on name+email+org); freshness ≤30 minutes |

#### Sardaukar — Diligence Workflow

| Attribute | Specification |
|---|---|
| Owns (PostgreSQL) | DD queue items, question/response log, expert call schedule, data request log, audit trail, AI-suggested similar question index |
| Consumes from Foldspace | MDM: Deal; Reverend Mother: triage memo focus areas; Mentat: processed financial data |
| Publishes to Foldspace | DD findings summary, resolved/open item status, expert call transcripts |
| Snowflake Automation | Stream on DD queue → Task flags overdue items; Dynamic Table aggregates resolution status |
| Output Port: `SARDAUKAR_LAND.*` | Refresh SLA: 5-minute lag; Quality SLA: 99% completeness on `deal_id`, `dd_item_id`, `status`; Freshness: ≤15 minutes |
| Historization | DD queue items: Append-only (status transitions are events). Question/response log: Append-only (immutable audit). Expert call transcripts: Append-only |
| Data Classification | DD questions and responses: CONFIDENTIAL. Expert call transcripts: CONFIDENTIAL. DD status summary: INTERNAL |
| Consuming Apps | Mentat (financial data packages), Reverend Mother (DD findings for memo), Landsraad (DD status for IC review), Heighliner (DD status for co-lender) |
| Bronze→Silver Gate | Schema validation; null checks on `deal_id`, `dd_item_id`; referential integrity to MDM `deal_id`; document reference integrity |
| Silver→Gold Gate | Status must be in canonical enum; overdue flag calculation correct; freshness ≤20 minutes |

#### Mentat — Financial Modeling

| Attribute | Specification |
|---|---|
| Owns (PostgreSQL) | Model versions, scenario parameters, financial input tables, model outputs, data book versions, assumption distribution definitions, sensitivity analysis results |
| Consumes from Foldspace | MDM: Deal, Company, Facility; Sardaukar: financial data packages; CHOAM: facility terms |
| Publishes to Foldspace | Financial model outputs, data book (versioned), key metrics (leverage, coverage, returns), Monte Carlo simulation results, sensitivity analysis outputs |
| Snowflake Automation | Dynamic Table on model outputs for downstream consumption; Stream triggers recalculation on new inputs |
| Output Port: `MENTAT_LAND.*` | Refresh SLA: triggered on new input data (event-driven); Quality SLA: 99.9% completeness on model output required fields; Freshness: ≤30 minutes from input receipt |
| Historization | Model outputs: Snapshot (YYYYMMDD + model_version) (period-stamped). Data book versions: Snapshot (YYYYMMDD + version). Scenario parameters: Append-only (each parameter set is a versioned event). Sensitivity results: Snapshot (YYYYMMDD + model_version) |
| Data Classification | Model outputs (leverage, returns, pricing): CONFIDENTIAL. Scenario parameters: CONFIDENTIAL. Data book: CONFIDENTIAL (contains deal-level financials) |
| Consuming Apps | Reverend Mother (data book for memo), Landsraad (financial metrics for IC), CHOAM (model refresh on terms change), Heighliner (data book for co-lender), Corrino (model-derived metrics), Melange (model outputs for valuation) |
| Bronze→Silver Gate | Schema validation; null checks on `deal_id`, `model_version`, `output_type`; referential integrity to MDM `deal_id` and `facility_id`; numeric range validation on financial ratios |
| Silver→Gold Gate | Model version integrity (version chain is unbroken); leverage/coverage ratios within plausible bounds; freshness ≤45 minutes from input |

#### Reverend Mother — Memo Drafting

| Attribute | Specification |
|---|---|
| Owns (PostgreSQL) | Memo draft versions, section-level content, human edits, export records, AI draft / final comparison records |
| Consumes from Foldspace | MDM: Deal, Company; Sardaukar: DD findings; Mentat: data book; CHOAM: agreed terms |
| Publishes to Foldspace | Finalized memo versions (triage + IC + co-lender), memo sections as structured data, AI draft vs. final approved delta records |
| Snowflake Automation | Stream on memo publication → updates `CURATED.MEMO_ACTIVITY` and `CURATED.DOCUMENTS` |
| Output Port: `REVEREND_MOTHER_LAND.*` | Refresh SLA: event-driven on memo publication; Quality SLA: 100% completeness on `deal_id`, `memo_id`, `memo_type`, `version`; Freshness: ≤10 minutes from publication |
| Historization | Memo draft versions: Append-only (each version is an immutable record). Section edits: Append-only (edit events). Export records: Append-only |
| Data Classification | IC memo content: RESTRICTED. Triage memo content: CONFIDENTIAL. Co-lender memo content: CONFIDENTIAL (but deliberately excludes RESTRICTED IC deliberation data). AI draft vs. final deltas: RESTRICTED |
| Consuming Apps | Landsraad (finalized IC memo for presentation), Heighliner (co-lender memo), CHOAM (memo terms sections) |
| Bronze→Silver Gate | Schema validation; null checks on all required fields; document reference integrity to S3 keys; referential integrity to MDM `deal_id` |
| Silver→Gold Gate | Memo type in canonical enum; version chain integrity; freshness ≤15 minutes |

#### Landsraad — IC Deliberation

| Attribute | Specification |
|---|---|
| Owns (PostgreSQL) | Memo render state, per-member annotations, votes, conditions, decision log, pre-vote records, engagement analytics, automated minutes records |
| Consumes from Foldspace | MDM: Deal; Reverend Mother: finalized memos; CHOAM: current terms |
| Publishes to Foldspace | IC decisions (immutable), conditions, per-member votes, deal outcome, engagement analytics, automated minutes — all to `IC_AUDIT` schema |
| Snowflake Automation | Snowflake append-only table with TIME TRAVEL for immutability; no Dynamic Tables (never recomputed) |
| Output Port: `LANDSRAAD_LAND.*` | Refresh SLA: real-time on session close; Quality SLA: 100% completeness (no partial IC records); Freshness: ≤5 minutes from session close |
| Historization | IC decisions: Append-only (immutable — the most governance-critical historization choice in the suite). Annotations: Append-only. Votes: Append-only. Conditions: Append-only. Engagement analytics: Snapshot (per session) |
| Data Classification | Individual member votes (pre-reveal): RESTRICTED. IC decision outcome: CONFIDENTIAL. Annotations: RESTRICTED. Engagement analytics: RESTRICTED. Automated minutes: CONFIDENTIAL |
| Consuming Apps | CHOAM (IC-approved terms and conditions), Foldspace `IC_AUDIT` (audit trail), Melange (IC decision history for valuation context) |
| Bronze→Silver Gate | Schema validation; null checks on `ic_session_id`, `deal_id`, `decision`; referential integrity to MDM `deal_id`; vote count equals session member count |
| Silver→Gold Gate | Decision is in canonical enum; all votes present before decision is finalized; immutability check (no UPDATE detected); freshness ≤10 minutes |

#### CHOAM — Deal Economics

| Attribute | Specification |
|---|---|
| Owns (PostgreSQL) | Term sheet versions, negotiation turn log, redlines, credit agreement versions, precedent library, obligation tracking records |
| Consumes from Foldspace | MDM: Deal, Facility; Landsraad: IC-approved conditions; Mentat: model refresh requests |
| Publishes to Foldspace | Agreed terms (facility economics), executed agreement versions, market precedents, precedent library entries, obligation status |
| Snowflake Automation | Stream on `CHOAM_LAND.agreed_terms` → Dynamic Table refreshes `CURATED.FACILITIES` |
| Output Port: `CHOAM_LAND.*` | Refresh SLA: event-driven on terms agreement; Quality SLA: 100% completeness on `deal_id`, `facility_id`, `terms_version`; Freshness: ≤10 minutes |
| Historization | Term sheet versions: Append-only (each version is immutable). Negotiation turn log: Append-only. Credit agreement versions: Append-only. Precedent library: SCD Type 2 (evolving reference data). Obligation status: Append-only (status change events) |
| Data Classification | Credit agreement economics (pricing, fees, covenants): CONFIDENTIAL. Negotiation positions: RESTRICTED. Precedent library (anonymized): INTERNAL |
| Consuming Apps | Mentat (terms for model refresh), Reverend Mother (terms for memo update), Stillsuit (executed CA for loan activation), Heighliner (terms for co-lender visibility), Atreides (executed CA for closing) |
| Bronze→Silver Gate | Schema validation; null checks on required fields; referential integrity to MDM `deal_id` and `facility_id`; numeric validation on pricing fields |
| Silver→Gold Gate | Terms version chain integrity; pricing within plausible bounds; freshness ≤15 minutes |

#### Heighliner — Syndication & Agency

| Attribute | Specification |
|---|---|
| Owns (PostgreSQL) | Co-lender DD questions, allocation tracking, co-lender commitments, post-close reporting packages, amendment/consent voting records, financial reporting calendar, deal site configurations |
| Consumes from Foldspace | MDM: Deal, Facility; Reverend Mother: co-lender memo; Mentat: data book; Stillsuit: post-close borrower reports |
| Publishes to Foldspace | Syndication allocations, co-lender commitments, agency notifications, amendment voting results, borrower reporting status |
| Snowflake Automation | Dynamic Table on allocation availability (real-time remaining commitment) |
| Output Port: `HEIGHLINER_LAND.*` | Refresh SLA: 5-minute lag; Quality SLA: 99.9% on `deal_id`, `facility_id`, `colender_id`, `allocation_amount`; Freshness: ≤15 minutes |
| Historization | Allocation records: Append-only (each allocation change is an event). Commitments: Append-only. Amendment voting: Append-only (immutable vote records). Reporting calendar: SCD Type 2 (schedule changes tracked). Deal site configuration: SCD Type 2 |
| Data Classification | Firm's total allocation and economics above co-lender tranche: RESTRICTED. Co-lender commitment amounts: CONFIDENTIAL (scoped to co-lender's own view). Borrower reporting packages: CONFIDENTIAL. Amendment voting: CONFIDENTIAL |
| Consuming Apps | Stillsuit (co-lender position data for agency admin), Corrino (syndication analytics), Melange (co-lender allocation for valuation) |
| Bronze→Silver Gate | Schema validation; null checks on required fields; referential integrity to MDM `deal_id`, `facility_id`; allocation amounts sum to facility size |
| Silver→Gold Gate | Allocation consistency check (total ≤ facility committed amount); freshness ≤20 minutes |

#### Atreides — Closing Workflow

| Attribute | Specification |
|---|---|
| Owns (PostgreSQL) | Closing task checklist, funds flow records, wire instruction templates, funding confirmation log, KYC/AML compliance records, maker-checker approval log |
| Consumes from Foldspace | MDM: Deal, Facility; CHOAM: executed CA; Stillsuit: (handoff target) |
| Publishes to Foldspace | Closing task completion records, funds flow statement, funding confirmation event |
| Snowflake Automation | Stream on `ATREIDES_LAND.closing_tasks` → Dynamic Table tracks % completion |
| Output Port: `ATREIDES_LAND.*` | Refresh SLA: real-time on task completion; Quality SLA: 100% completeness on `deal_id`, `facility_id`, `task_id`, `status`; Freshness: ≤5 minutes |
| Historization | Closing tasks: Append-only (each task status change is an event). Funds flow records: Append-only (immutable financial records). Wire instructions: SCD Type 2 (template changes tracked). Funding confirmation: Append-only (immutable — this is the capital deployment event). KYC/AML records: Append-only |
| Data Classification | Funds flow statement: RESTRICTED. Wire instructions: RESTRICTED. Funding confirmation: CONFIDENTIAL. Closing task status: INTERNAL. KYC/AML records: CONFIDENTIAL |
| Consuming Apps | Stillsuit (closing package for loan activation — highest-blast-radius handoff) |
| Bronze→Silver Gate | Schema validation; null checks on all required fields; referential integrity to MDM `deal_id` and `facility_id`; funds flow amount validation (non-negative, within facility commitment) |
| Silver→Gold Gate | All checklist items resolved before funding confirmation; funds flow amounts reconcile to facility commitment; freshness ≤10 minutes |

#### Stillsuit — Loan Administration

| Attribute | Specification |
|---|---|
| Owns (PostgreSQL) | Facility/tranche ledger, payment schedule, payment receipts, amendment/waiver records, compliance certificate delivery log, agent notice processing log, cash/position reconciliation records, income recognition records |
| Consumes from Foldspace | MDM: Deal, Facility, Borrower; Atreides: closing package |
| Publishes to Foldspace | Loan events (payments, amendments, breaches), facility master data (authoritative post-close), compliance delivery status, agent notice processing status, reconciliation discrepancy alerts |
| Snowflake Automation | Snowflake Streams on `STILLSUIT_LAND.loan_events` are the primary feed for Corrino — highest-value automation in the suite |
| Output Port: `STILLSUIT_LAND.*` | Refresh SLA: ≤5 minutes from payment processing; Quality SLA: 100% completeness on `facility_id`, `event_type`, `amount`, `effective_date`; Freshness: ≤10 minutes |
| Historization | Loan events (payments, amendments, notices): Append-only (immutable financial audit records). Facility/tranche ledger: SCD Type 2 (master entity — balance and terms evolve). Payment schedule: SCD Type 2 (schedule adjustments tracked). Compliance certificate log: Append-only. Reconciliation records: Append-only |
| Data Classification | Payment amounts and balances: CONFIDENTIAL. Amendment terms: CONFIDENTIAL. Facility economics (margin, fees): CONFIDENTIAL (masked for Borrower role). Agent notices: CONFIDENTIAL. Reconciliation discrepancies: RESTRICTED |
| Consuming Apps | Corrino (loan events — second-highest-blast-radius contract), Melange (loan data for valuation), Heighliner (post-close reporting) |
| Bronze→Silver Gate | Schema validation; null checks on all required fields; referential integrity to MDM `facility_id` and `borrower_id`; payment amount non-negative; date format validation |
| Silver→Gold Gate | Double-entry validation (debits = credits); balance reconciliation against expected schedule; freshness ≤15 minutes |

#### Corrino — Portfolio Monitoring

| Attribute | Specification |
|---|---|
| Owns (PostgreSQL) | Borrower financial statement ingests, covenant calculation results, alerting configuration, reporting delivery log, data validation results, AI extraction results |
| Consumes from Foldspace | MDM: Facility, Borrower; Stillsuit: loan events; External: Chronograph |
| Publishes to Foldspace | Portfolio analytics views, covenant headroom metrics, risk migration data — fed to `PORTFOLIO_ANALYTICS` and `COVENANT_TRACKING` |
| Snowflake Automation | Dynamic Tables for rolling covenant recalculations; Snowflake Tasks for alerting on covenant proximity |
| Output Port: `CORRINO_LAND.*` | Refresh SLA: daily for standard monitoring; event-driven for covenant breach alerts; Quality SLA: 99.9% completeness; Freshness: ≤1 hour for standard metrics, ≤15 minutes for breach alerts |
| Historization | Covenant calculation results: Snapshot (YYYYMMDD) (period-stamped). Portfolio analytics: Snapshot (YYYYMMDD). Risk migration data: Snapshot (YYYYMMDD). Alerting events: Append-only. Financial statement ingests: Append-only |
| Data Classification | Covenant calculations: CONFIDENTIAL. Portfolio analytics (position-level): CONFIDENTIAL. Portfolio aggregates: INTERNAL. Risk migration: CONFIDENTIAL. Borrower financial statements: CONFIDENTIAL |
| Consuming Apps | Melange (portfolio performance for valuation — feeds `VALUATION_OUTPUTS`), LP reporting aggregates |
| Bronze→Silver Gate | Schema validation; null checks on required fields; referential integrity to MDM `facility_id`; covenant ratio numeric validation; financial statement period alignment |
| Silver→Gold Gate | Covenant headroom calculations verified against raw inputs; portfolio totals reconcile to position-level data; freshness ≤2 hours |

#### Melange — Valuation

| Attribute | Specification |
|---|---|
| Owns (PostgreSQL) | Valuation workflow state, comparable data inputs, fair value determinations by period, valuation approval chain records, roll-forward automation state |
| Consumes from Foldspace | MDM: Facility; Stillsuit: loan data; Corrino: portfolio performance; External: market comp data |
| Publishes to Foldspace | Fair value outputs by position and period, valuation basis documentation — fed to `VALUATION_OUTPUTS` |
| Snowflake Automation | Dynamic Table for period-over-period valuation delta tracking |
| Output Port: `MELANGE_LAND.*` | Refresh SLA: quarterly cycle (event-driven on `valuation.cycle-initiated`); Quality SLA: 100% completeness on all valuation output fields; Freshness: ≤4 hours from approval |
| Historization | Fair value outputs: Snapshot (YYYYMMDD — period-stamped, partitioned by valuation date). Comparable selections: Snapshot (YYYYMMDD). Approval chain: Append-only (immutable governance records). Roll-forward state: Snapshot (YYYYMMDD + cycle_id) |
| Data Classification | Fair value determinations: CONFIDENTIAL. Comparable selections: INTERNAL. Valuation methodology rationale: CONFIDENTIAL. LP-facing valuation reports: CONFIDENTIAL (scoped). Published LP reports: PUBLIC (anonymized aggregates only) |
| Consuming Apps | `LP_REPORTING` (Foldspace consumption schema), board reporting, external auditor access (read-only, scoped) |
| Bronze→Silver Gate | Schema validation; null checks on required fields; referential integrity to MDM `facility_id`; fair value numeric validation (non-negative, within plausible bounds for asset class) |
| Silver→Gold Gate | Approval chain complete (all required approvers signed off); valuation date matches reporting period; comparable set non-empty; freshness ≤8 hours |

## 3. Inter-App Integration Patterns

This section specifies which integration mechanism is used for each cross-application interaction in the suite. The choice between async events, synchronous APIs, and Snowflake-native data flow is not stylistic — it reflects the consistency, latency, and durability requirements of each handoff.

### General Pattern Selection

A sharp distinction separates the integration patterns: data distribution patterns are for asynchronous, read-optimized sharing, while application integration patterns are for speed and stronger consistency. APIs excel for strongly consistent reads and directly invoking commands; asynchronous communication is more resilient and cost-effective when there is no time criticality. This gives three pattern categories for Arrakis:

- **Snowflake Streams/Dynamic Tables** — for analytics and BI data propagation (Stillsuit → Corrino, Corrino → Melange) — highest-throughput, lowest-latency for read-heavy workloads.
- **Redpanda Events (async)** — for workflow handoffs that don't require synchronous acknowledgment (Reverend Mother → Sardaukar, IC approved → CHOAM trigger).
- **Foldspace REST API (sync)** — for point-of-record writes requiring strong consistency (Atreides → Stillsuit funding handoff, Landsraad writing IC decisions).

### API-as-Product Specifications for Critical Foldspace Endpoints

Every Foldspace API endpoint carries a version number, deprecation policy, and documented SLA. The following table specifies the highest-consequence endpoints:

| Endpoint | Version | Owner | SLA (p95 Latency / Availability) | Deprecation Policy | Consuming Apps |
|---|---|---|---|---|---|
| `POST /foldspace/v1/funding-confirmed` | v1.0 | Foldspace (Atreides handoff) | 500ms / 99.99% | 90-day notice; parallel support for v1 through v2 lifecycle | Atreides → Stillsuit |
| `POST /foldspace/v1/ic-decisions` | v1.0 | Foldspace (Landsraad write) | 200ms / 99.99% | 90-day notice | Landsraad |
| `POST /foldspace/v1/master-data/{entity}` | v1.0 | Foldspace MDM | 150ms / 99.95% | 90-day notice | All 13 apps |
| `GET /foldspace/v1/deal-context/{deal_id}` | v1.0 | Foldspace MDM | 100ms / 99.9% | 90-day notice | All 13 apps |
| `POST /foldspace/v1/documents` | v1.0 | Foldspace Doc Registry | 300ms / 99.9% | 90-day notice | Reverend Mother, CHOAM, Gom Jabbar |
| `POST /foldspace/v1/ic-sessions` | v1.0 | Landsraad (direct API) | 200ms / 99.9% | 90-day notice | Reverend Mother → Landsraad |

### Critical Handoff Analysis

#### Atreides → Stillsuit (Handoff from Closing to Loan Admin Upon Funding)

**Pattern:** Foldspace API call (sync, two-phase) — hardened with idempotency, circuit-breaker, and versioned schema.

This is the most consequential handoff in the suite — the moment capital leaves the fund. The pattern is a synchronous, two-phase handoff:

1. Atreides calls `POST /foldspace/v1/funding-confirmed` with the full closing package `{deal_id, facility_records[], funds_flow_statement, wire_confirmations[], executed_ca_document_id}`. Foldspace validates the package for completeness and writes a `funding_confirmation` record.
2. Foldspace then calls Stillsuit's `POST /loans/activate` endpoint with the closing package, and Stillsuit must acknowledge success before Foldspace returns 200 to Atreides. Only after this full round-trip does Atreides mark the deal as Funded.

**Idempotency enforcement:** Every funding confirmation request must carry an `idempotency_key` (UUID generated by Atreides at the start of the funding workflow). Foldspace stores the idempotency key in a `funding_idempotency` table. If a duplicate key is received, Foldspace returns the original response without re-executing the handoff. This prevents the catastrophic double-activation scenario where a network retry causes two loan activations.

**Circuit-breaker pattern:** The Foldspace-to-Stillsuit call is wrapped in a circuit breaker (implemented via the `circuitbreaker` Python library or equivalent). The breaker opens after 3 consecutive failures within a 60-second window, enters half-open state after 30 seconds, and allows a single probe request. When open, Foldspace immediately returns a `503 Service Unavailable` to Atreides with a `Retry-After` header and alerts the operations team via PagerDuty. This makes failure isolation explicit and bounded rather than relying on timeout-only handling.

**Versioned request schema:** The `FundingConfirmedRequest` Pydantic model is versioned in `shared/schemas/funding/`. The endpoint guarantees backward-compatibility across one major version: when v2 is released, v1 payloads continue to be accepted for a minimum of 90 days. Schema version is included in the request header (`X-Arrakis-Schema-Version`).

**Mandatory chaos engineering test suite:** Before Phase 4 production, a dedicated two-week hardening sprint must execute: Stillsuit timeout injection (verify circuit breaker opens), Redpanda broker failure injection (verify event replay), PostgreSQL connection pool exhaustion simulation (verify graceful degradation), and double-submission injection (verify idempotency key enforcement). Test results are documented in the `docs/runbooks/funding_handoff_chaos_report.md` runbook.

**Failure handling:** If Stillsuit returns an error or the circuit breaker is open, Foldspace holds the funding confirmation in a pending state, alerts the operations team, and Atreides does not mark the deal funded. This prevents the catastrophic scenario of a wire being sent but the loan not being on the books.

#### Sardaukar → Mentat (Financial Data Routing from DD)

**Pattern:** Redpanda event + Snowflake Stream

When Sardaukar receives a financial data package (management-provided financials, third-party diligence outputs), it: (1) writes the raw document reference and structured metadata to its PostgreSQL operational store, (2) routes extracted structured data to `ARRAKIS_RAW.SARDAUKAR_LAND`, and (3) emits a `financial-data.received` event to Redpanda with payload `{deal_id, data_package_id, data_type, snowflake_ref}`. Mentat subscribes to this topic, fetches the structured data from the Snowflake curated layer, and ingests it as new model inputs. A Snowflake Stream on `ARRAKIS_CURATED.FINANCIAL_DATA` triggers a Snowflake Task that notifies Mentat's model orchestration layer of new inputs. Special consideration: Mentat must version-control every model state change that was triggered by a new data input, ensuring full audit lineage from document receipt to model output.

#### Reverend Mother → Sardaukar (Triage Memo Seeding the DD Queue)

**Pattern:** Redpanda event

When a triage memo is finalized and approved for handoff, Reverend Mother emits `triage-memo.completed` with a structured payload containing: `{deal_id, memo_id, credit_focus_areas: [{theme, description, priority}], data_gaps: [{item, rationale}]}`. The credit focus areas are extracted by Claude as a structured JSON list during the drafting process. Sardaukar subscribes to this topic, auto-populates the DD queue with initial items derived from the focus areas, and generates a first-pass DDQ. Dependency: Claude's extraction of focus areas must use a validated Pydantic schema so Sardaukar can reliably parse and import them — this is a critical contract boundary that must be enforced at the schema registry level.

#### Reverend Mother → Landsraad (Memo Handoff and Rendering)

**Pattern:** Foldspace API call (sync) + Redpanda event

Reverend Mother calls the Foldspace Document API to register the finalized memo version (assigning a canonical `document_id`, storing the binary to S3, recording structured section metadata to Snowflake). It then calls the Landsraad API directly to initiate a new IC session (`POST /ic-sessions` with `{deal_id, memo_document_id, committee_members[], stage}`). Landsraad fetches memo section content from the document store and renders it. A `ic-session.opened` event is emitted to Redpanda to notify permissioned IC members. The direct API call is warranted here because IC session creation is a strongly consistent, transactional operation — a memo cannot be "half-submitted" to the committee.

#### Landsraad → Foldspace (IC Decisions, Conditions, Audit Trail)

**Pattern:** Foldspace API call (sync), append-only write

This is the most governance-critical write in the entire suite. When an IC decision is recorded (approved, approved-with-conditions, deferred, declined), Landsraad calls `POST /foldspace/v1/ic-decisions` synchronously. The Foldspace IC Decisions API writes to a PostgreSQL `ic_decisions` table designed as append-only (no UPDATE, no DELETE — enforced at the application layer and documented at the database layer with trigger guards), and simultaneously streams the record to `ARRAKIS_RAW.APP_EVENTS` and ultimately to `ARRAKIS_CONSUMPTION.IC_AUDIT`.

**Immutability enforcement:** Snowflake's FAIL SAFE and TIME TRAVEL on the `IC_AUDIT` schema provide platform-level protection. The PostgreSQL table uses a trigger to reject any UPDATE or DELETE, returning an error. Records can only be superseded by new records with an `amendment_of` foreign key — the original is never modified.

#### Landsraad → CHOAM (IC-Approved Terms Triggering Term Sheet)

**Pattern:** Redpanda event

When IC approves with recommended terms, Landsraad emits `ic.approved` with payload `{deal_id, ic_session_id, recommended_terms: {...}, conditions: [{description, owner, due_date}]}`. CHOAM subscribes and auto-populates the firm's standard term sheet template from the `recommended_terms` payload. This is async because CHOAM does not need to respond before Landsraad completes its workflow.

#### CHOAM → Mentat + Reverend Mother (Agreed Terms Updating Model and Memo)

**Pattern:** Redpanda fan-out event

When CHOAM records agreed terms after a term sheet negotiation turn, it emits `terms.agreed` to Redpanda. Both Mentat and Reverend Mother subscribe to this same topic (fan-out). Mentat refreshes its model's deal economics inputs and reruns affected scenarios. Reverend Mother marks the IC memo as requiring a terms refresh and (if configured) triggers a Claude re-draft of the terms section. This fan-out pattern avoids CHOAM needing to know about Mentat and Reverend Mother — it simply publishes a fact, and interested consumers act on it. Versioning discipline is critical: both Mentat and Reverend Mother must tag their outputs with the `terms_version_id` from the event payload for audit lineage.

#### Stillsuit → Corrino (Loan-Level Data Feed for Portfolio Monitoring)

**Pattern:** Snowflake Streams — the clearest Snowflake-native integration in the suite

Stillsuit writes all loan events (payments, amendments, covenant deliveries) to `ARRAKIS_RAW.STILLSUIT_LAND.loan_events`. A Snowflake Stream on this table feeds a Snowflake Task that incrementally processes new events into `ARRAKIS_CURATED.LOAN_EVENTS`. A Dynamic Table on the curated events layer maintains a rolling materialized view of position-level loan state in `ARRAKIS_CONSUMPTION.PORTFOLIO_ANALYTICS`. Corrino reads exclusively from the consumption layer — it has no direct connection to Stillsuit's PostgreSQL. This is clean separation of the operational and analytical planes.

#### Corrino → Melange (Portfolio Performance Data for Valuation)

**Pattern:** Snowflake Dynamic Tables — pure Snowflake-native

Melange reads `ARRAKIS_CONSUMPTION.PORTFOLIO_ANALYTICS` and `ARRAKIS_CONSUMPTION.COVENANT_TRACKING` directly. No events, no API calls. The Dynamic Table refresh schedule aligns with valuation cycle cadence (typically quarterly, with ad hoc on-demand refresh). Melange's valuation workflow queries these tables, enriches with market comparable data from `ARRAKIS_CURATED.EXTERNAL_MARKET`, and writes fair value outputs back to `ARRAKIS_CONSUMPTION.VALUATION_OUTPUTS`.

### Data Contract Registration Requirement

Every inter-app data exchange described above must have a registered data contract in the DCA (Section 5) before the consuming app's Snowflake read permissions are provisioned. No new inter-app integration may ship to staging without a registered contract.

---

## 4. Application Architecture

This section establishes the standard internal architecture every FastAPI application uses, the asynchronous Unit of Work pattern, the per-application feature parity deltas against commercial equivalents being replaced, and the cross-cutting concerns of optimistic concurrency, model translation at golden-source boundaries, and Kubernetes health checks.

### Standard Internal Architecture for FastAPI Applications

All FastAPI-backed applications (Thumper, Gom Jabbar, Gurney, Sardaukar, Mentat, Reverend Mother, Landsraad, CHOAM, Heighliner, Atreides, Stillsuit, Melange, and Foldspace itself) follow a four-layer internal architecture based on the ports-and-adapters pattern. This standardization ensures the outbox pattern operates consistently across all 13 apps and makes the codebase navigable for a single development team maintaining the full suite.

Each app's `backend/` directory is organized as:

```
backend/
├── domain/                 # Domain model: entities, value objects, aggregate roots, domain events
│   ├── model.py            # Aggregate roots and entities with business rules
│   └── events.py           # Domain event dataclasses (e.g., NDAExecuted, PaymentReceived)
├── adapters/
│   ├── repository.py       # AbstractRepository + SQLAlchemy implementation
│   └── orm.py              # SQLAlchemy classical mapping (ORM depends on model, not reverse)
├── service_layer/
│   ├── unit_of_work.py     # AbstractUnitOfWork + SQLAlchemy implementation
│   ├── handlers.py         # Command and event handlers (one handler per use case)
│   └── messagebus.py       # In-process message bus: dispatches domain events to handlers
├── entrypoints/
│   ├── api.py              # FastAPI route definitions (thin — delegates to service layer)
│   └── event_consumer.py   # Redpanda consumer entrypoint (delegates to service layer)
└── outbox.py               # Outbox append logic, invoked by UoW on commit
```

Key constraints: (1) FastAPI route handlers must not contain business logic — they extract request parameters, call a service-layer handler, and return a response. (2) The Unit of Work wraps each service-layer operation in a single PostgreSQL transaction; the outbox append occurs within this same transaction, guaranteeing atomicity between domain state change and event publication intent. (3) Domain events are collected on aggregate root instances (e.g., `self.events.append(NDAExecuted(...))`); the UoW's `commit()` method dispatches collected events to the in-process message bus after the database commit succeeds. (4) The in-process message bus is not Celery — it is a synchronous dispatcher within the request lifecycle for side-effect handlers (e.g., logging, cache invalidation, secondary outbox writes). Long-running work (LLM drafting, report generation) is dispatched to Celery as before.

**Async Unit of Work convention.** All FastAPI applications in the Arrakis suite must implement the Unit of Work pattern as an async context manager, adapting the synchronous UoW pattern to the async-first stack:

The abstract UoW contract (defined as a `typing.Protocol` per the abstraction mechanism convention) requires: `async def __aenter__(self) -> Self`, `async def __aexit__(self, *args) -> None`, `async def commit(self) -> None`, and `async def rollback(self) -> None`. The `__aexit__` method calls `rollback()` if `commit()` has not been called, ensuring no partial writes escape.

The concrete implementation wraps SQLAlchemy `AsyncSession`. The `__aenter__` method creates an `AsyncSession` from the app's `async_sessionmaker` and instantiates repository instances bound to that session. The `__aexit__` method closes the session. Repository methods (`get`, `add`, `list`) are `async def` and use `await session.execute(...)`.

Service-layer functions accept the UoW as a parameter (injected via FastAPI `Depends()`) and use `async with uow:` to bracket the transactional scope:

```python
async def approve_ic_decision(
    decision_id: str,
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> ICDecisionResult:
    async with uow:
        decision = await uow.ic_decisions.get(decision_id)
        decision.approve(...)            # domain logic — synchronous
        await uow.commit()
    return ICDecisionResult.from_entity(decision)
```

Domain model methods (entity and aggregate operations) remain synchronous — they contain no I/O. Only repository access and UoW commit/rollback are async. This preserves the testability benefit of the UoW pattern: unit tests use a synchronous `FakeUnitOfWork` that requires no event loop.

### Feature Parity Updates by Application

The blueprint specifies the domain model and technical architecture for each application; this subsection documents the feature deltas against the commercial equivalents Arrakis is designed to replace, anchored to specific named features from the commercial platforms and the implementation approach within the existing tech stack.

#### Gom Jabbar — NDA Workflow (vs. Ironclad, DocuSign CLM)

**Existing Architecture (preserved):** FastAPI + PostgreSQL state machine. React frontend for sequential approval flow with document preview.

**Feature Parity Delta:**

| Feature | Commercial Source | Implementation |
|---|---|---|
| Dynamic Approval Routing | Ironclad: rule-based routing by deal size, contract type, risk tier | Configurable routing rules engine in PostgreSQL (`nda_routing_rules` table); FastAPI middleware evaluates rules on NDA submission and routes to correct approver chain. Rules editable via admin UI. |
| Auto-Extraction of NDA Metadata | Ironclad: AI extracts 190+ metadata fields; DocuSign CLM: clause identification | Claude (via Spice) extracts counterparty name, governing law, expiration date, restricted activities, territory from uploaded NDA PDF. Output validated against `NDAMetadataSchema` Pydantic model. Extracted metadata stored in PostgreSQL and published to `GOM_JABBAR_LAND`. |
| Obligation Tracking | Ironclad: post-signature obligation management; DocuSign CLM: obligation alerts | PostgreSQL `nda_obligations` table tracks post-execution commitments |

#### Sardaukar — Diligence Workflow (vs. Ansarada, Asana)

**Feature Parity Delta:**

| Feature | Commercial Source | Implementation |
|---|---|---|
| Q&A with AI-Suggested Similar Questions | Ansarada: AI suggests similar previously asked questions | pgvector on PostgreSQL stores embeddings of all historical DD Q&A pairs. On new question submission, nearest-neighbor search retrieves top-3 similar prior questions with answers. Displayed inline in the DD queue UI. Closes Ansarada's duplicate-reduction feature. |
| Document Auto-Classification (Smart Sort) | Ansarada: AI classifies documents into folder structures | Claude (via Spice) classifies uploaded DD documents by type (financial statement, legal opinion, management presentation, compliance certificate) and routes to appropriate DD queue category. |
| Timeline/Gantt View | Asana: visual project schedule with dependencies | React frontend component using a Gantt library (frappe-gantt or react-gantt-timeline) displaying DD workstream dependencies and milestones. |
| Automated Reminders & Submission Tracking | Ansarada: automatic reminders for outstanding items; Asana: deadline notifications | Celery beat scheduler sends reminder notifications at configurable intervals for overdue DD items and outstanding data requests. |
| Milestone Tracking | Asana: project milestones | PostgreSQL `dd_milestones` table tracks major DD checkpoints (e.g., "Management Presentation Complete," "Financial Model Received," "Legal DD Complete"). Status published to Snowflake for deal progress dashboards. |

#### Mentat — Financial Modeling (vs. Oracle Crystal Ball, Quantrix, Alteryx)

**Existing Architecture (preserved):** FastAPI backend + Snowflake + Python computational layer. Streamlit frontend for scenario exploration.

**Feature Parity Delta:**

| Feature | Commercial Source | Implementation |
|---|---|---|
| Monte Carlo Simulation | Oracle Crystal Ball: thousands of scenario iterations | Python engine using NumPy random sampling with configurable assumption distributions (normal, lognormal, triangular, uniform, beta). Runs N iterations (configurable, default 10,000) across model inputs. Output: probability-weighted distribution of key metrics (IRR, MOIC, debt yield, leverage). Closes Crystal Ball's core capability. |
| Assumption Distribution Definitions | Oracle Crystal Ball: 20+ distribution types calibrated to data | `assumption_distributions` PostgreSQL table stores per-variable distribution type and parameters. Supports calibration from historical data via scipy.stats.fit(). |
| Sensitivity Analysis (Tornado Charts) | Oracle Crystal Ball: ranks inputs by output variance contribution | Python sensitivity engine varies each input ±1σ while holding others constant; calculates output variance contribution. Output rendered as tornado chart in Streamlit. |
| Overlay Charts for Scenario Comparison | Oracle Crystal Ball: side-by-side distribution comparison | Streamlit Plotly overlay chart showing base, upside, downside, and stress case probability distributions on single axes. |
| Multi-Dimensional Calculation Engine | Quantrix: range-based calculations across dimensions | Model structure supports named dimensions (period, scenario, facility, tranche). Calculations defined at dimension level, not cell level. Implemented as NumPy array operations across dimension axes. |
| Dependency Inspector | Quantrix: formula audit trail | Model dependency graph stored in PostgreSQL. React frontend visualizes calculation chain from any output back to source inputs using a DAG visualization (React Flow). |
| Fuzzy Matching for Entity Reconciliation | Alteryx: near-duplicate entity matching | Python rapidfuzz library for matching company names across data sources (management-provided financials vs. MDM records). Threshold-based auto-match with manual review for low-confidence matches. |

#### Landsraad — IC Deliberation (vs. Zeck)

**Existing Architecture (preserved):** React + FastAPI + WebSocket Layer. Redis pub/sub for real-time collaboration.

**Feature Parity Delta:**

| Feature | Commercial Source | Implementation |
|---|---|---|
| Pre-Vote (Director Pre-Voting) | Zeck: cast votes before live meeting | PostgreSQL `ic_pre_votes` table stores pre-meeting votes with `submitted_at` timestamp. Pre-votes are sealed (not visible to other members) until the chair opens the session. Closes Zeck's flagship meeting-efficiency feature. |
| Automated Minutes Generation | Zeck: AI-powered minutes from meeting record | Claude (via Spice) generates structured minutes from the session's annotation log, vote records, conditions, and decision. Output validated against `ICMinutesSchema`. Human review required before finalization. Minutes stored in `ARRAKIS_CONSUMPTION.IC_AUDIT`. |
| Digitized Minutes Book | Zeck: searchable repository of all minutes | Snowflake `IC_AUDIT.minutes` table serves as the persistent, searchable minutes repository. Full-text search via Snowflake SEARCH optimization service. |
| Engagement Analytics | Zeck: tracks member reading engagement | WebSocket server logs section-view events per member (`{member_id, section_id, view_start, view_end}`). Aggregated into per-member engagement scores visible to IC chair after session close. |
| Smart Agendas | Zeck: structured agenda optimized for pre-reading | PostgreSQL `ic_agenda` table structures session into consent items (pre-voteable), discussion items, and action items. Agenda builder in React admin UI. |

#### CHOAM — Deal Economics (vs. Ironclad, Harvey AI)

**Existing Architecture (preserved):** FastAPI + PostgreSQL. React frontend with Lexical block editor for redlining.

**Feature Parity Delta:**

| Feature | Commercial Source | Implementation |
|---|---|---|
| Precedent Library (Knowledge Vault) | Harvey AI: Vault document intelligence repository | PostgreSQL + pgvector store of historical credit agreement provisions, organized by clause type, deal characteristics, and market period. Semantic search via embeddings. Claude references precedents when drafting new provisions. Closes Harvey's Vault capability. |
| Deep Analysis | Harvey AI: multi-source agentic reasoning | Claude (via Spice) with MCP tools performs multi-document analysis across the precedent library, current deal documents, and market data to identify risks and suggest negotiation positions. |
| Obligation Management | Ironclad: post-execution obligation tracking | PostgreSQL `ca_obligations` table tracks post-signing obligations (financial reporting deadlines, compliance certificate delivery, covenant test dates). Snowflake Task generates alerts for approaching deadlines. |
| Citation Grounding | Harvey AI: all outputs include source citations | Claude outputs include structured citations `{source_document_id, section, page}` for every referenced provision or precedent. Citations validated against document registry before display. |

#### Heighliner — Syndication & Agency (vs. Debtdomain, SyndTrak)

**Existing Architecture (preserved):** FastAPI + PostgreSQL. React frontend with separate co-lender and borrower namespaces.

**Feature Parity Delta:**

| Feature | Commercial Source | Implementation |
|---|---|---|
| Real Joint Book-Running | SyndTrak: co-arranger information-sharing controls | PostgreSQL `joint_book_config` table defines information-sharing levels between co-arrangers per deal. API middleware scopes data visibility based on co-arranger role. Closes SyndTrak's joint bookrunning gap. |
| Amendment/Consent Voting | SyndTrak: structured electronic voting workflow; Debtdomain: amendment tools | PostgreSQL `amendment_votes` table with append-only vote records. React voting UI for co-lenders. Aggregation and threshold calculation automated. |
| Financial Reporting Calendar | Debtdomain: integrated financial monitoring calendar | PostgreSQL `reporting_calendar` table with borrower reporting obligations. Celery beat generates automated reminder emails to borrowers approaching deadlines. |
| AI-Assisted Co-Lender DD Responses | Arrakis-native (gap: no commercial equivalent fully addresses this) | Claude (via Spice) drafts responses to co-lender DD questions using `search_deal_documents` MCP tool. Human review required before sending. New MCP tool: `get_colender_dd_context(deal_id, question_id)`. |
| Investor Intelligence | SyndTrak: market feedback capture | PostgreSQL `investor_feedback` table captures co-lender appetite, commentary, and commitment signals during syndication. Published to `HEIGHLINER_LAND` for analytics. |
| Deal Site Templates | Debtdomain: pre-configured site templates | PostgreSQL `deal_site_templates` table stores standard site configurations by deal type. Auto-applied on new syndication site creation. |
| Multi-Currency Support | Debtdomain/SyndTrak: multi-currency facilities | PostgreSQL supports multi-currency facility records. FX conversion rates sourced from external market data feed. Allocation and commitment tracking in facility currency and reporting currency. |

#### Atreides — Closing Workflow (vs. Allvue Onboarding)

**Existing Architecture (preserved):** FastAPI + PostgreSQL task manager. React frontend with closing checklist.

**Feature Parity Delta:**

| Feature | Commercial Source | Implementation |
|---|---|---|
| KYC/AML Compliance Integration | Allvue Passthrough: KYC/AML in onboarding workflow | `KYCConnector` extending `BaseConnector` integrates with external KYC/AML provider API. Compliance status stored in PostgreSQL `kyc_records` table. Closing checklist blocks funding until KYC clearance confirmed. |
| Maker-Checker Approval | Allvue: dual-control approval for data modifications | PostgreSQL `maker_checker_log` table enforces two-person approval on funds flow modifications and wire instruction changes. Second approver must be a different user than the initiator. |
| Automated Closing Stage Notifications | Allvue: automated communications at key stages | Celery task triggered on closing task completion events sends notifications to relevant stakeholders (deal team, legal, ops) at configurable milestones (e.g., CA executed, funds flow approved, wires confirmed). |

#### Stillsuit — Loan Administration (vs. WSO, Allvue Investment Accounting)

**Existing Architecture (preserved):** FastAPI + PostgreSQL operational ledger. React frontend for loan administration.

**Feature Parity Delta:**

| Feature | Commercial Source | Implementation |
|---|---|---|
| Agent Notice Processing | WSO: AI-categorized agent notices; Allvue: notice management | PostgreSQL `agent_notices` table with structured notice types (rate reset, rollover, paydown, amendment). Claude (via Spice) categorizes and extracts structured data from incoming agent notices (email/PDF). Output validated against `AgentNoticeSchema`. Closes WSO's core agent processing capability. |
| Cash & Position Reconciliation | WSO: daily matching against agent/custodian; Allvue: automated reconciliation | Daily Celery task matches PostgreSQL position records against agent bank statements (ingested via `AgencyConnector`). Discrepancies written to `reconciliation_discrepancies` table and `loan.reconciliation-discrepancy` event emitted to Redpanda. |
| Multi-Currency Accounting | WSO/Allvue: multi-currency transaction processing | PostgreSQL supports multi-currency facility records with FX translation. Income and principal tracked in facility currency; reporting in fund base currency with gain/loss recognition. |
| Income Recognition & Allocation | Allvue: automatic income allocation to investor level | Python accounting engine handles interest income, PIK accrual, OID amortization, and EIR calculation. Results published to Snowflake for LP reporting. |
| Hypothetical Trade Analysis | WSO Compliance Insights: model compliance impact before execution | FastAPI endpoint `POST /loans/hypothetical-trade` accepts proposed position change and returns projected compliance test results (concentration limits, rating distribution) without committing the change. |

#### Corrino — Portfolio Monitoring (vs. Chronograph GP, 73 Strings Monitor/Extract)

**Existing Architecture (preserved):** Streamlit in Snowflake dashboards. Snowflake Dynamic Tables for covenant recalculation.

**Feature Parity Delta:**

| Feature | Commercial Source | Implementation |
|---|---|---|
| Automated Financial Data Collection | Chronograph: automated borrower data requests | FastAPI endpoint `POST /data-requests` generates and emails structured data request forms to borrowers. Submission status tracked in PostgreSQL `data_requests` table. Celery beat sends automated reminders. Closes Chronograph's core data collection capability. |
| AI-Powered Document Extraction | 73 Strings 73 Extract: 99% accuracy extraction; Chronograph: ML-enabled source document data | Claude (via Spice) + Snowflake Cortex for structured extraction of financial statements and compliance certificates from uploaded PDFs. Dual extraction path: Cortex for tabular data already near Snowflake, Claude for complex/unstructured documents. New MCP tool: `extract_financial_data(document_id, extraction_template)`. |
| Compliance Certificate Parser | 73 Strings: specialized compliance certificate extraction | Claude (via Spice) with a specialized prompt template extracts covenant metrics from non-standard compliance certificate PDFs. Output validated against `CovenantCertificateSchema`. |
| Real-Time Data Validation & Variance Checking | Chronograph: real-time variance detection | Snowflake Task on incoming financial data compares against prior period values. Variance >20% from 30-day rolling average triggers `data-quality.sla-breach` alert event. |
| AutoFill / Push-Button Reporting | Chronograph: one-click data insertion into Word/PPT/Excel | Python `python-docx` + `python-pptx` template engine fills tagged placeholders in Word and PowerPoint templates with current portfolio data from Snowflake. Exposed via FastAPI endpoint `POST /reports/autofill`. |
| Predictive Risk Modeling | 73 Strings: AI-powered predictive risk signals | Python scikit-learn model trained on historical covenant breach patterns, financial trend deterioration, and sector stress indicators. Generates early-warning risk scores per borrower. Published as Snapshot data product. |

#### Melange — Valuation (vs. Chronograph Valuations, 73 Strings 73 Value)

**Existing Architecture (preserved):** FastAPI backend + Snowflake. Streamlit interface for valuation review.

**Feature Parity Delta:**

| Feature | Commercial Source | Implementation |
|---|---|---|
| Valuation Workflow Management | Chronograph: stage-gate routing with assignees/deadlines | PostgreSQL `valuation_workflow` table with configurable stage-gate steps (data collection → analysis → review → approval → publication). Each stage has assigned roles, deadlines, and required sign-offs. React admin UI for workflow configuration. Closes Chronograph's core workflow governance capability. |
| Roll-Forward Automation | Chronograph: prior period carry with automated updates | Python engine copies prior-period valuation model, auto-updates financial inputs from latest Corrino data, refreshes comparable set from market data, and flags inputs requiring manual review. Reduces quarterly cycle setup from hours to minutes. |
| Comparable Company Selection & Benchmarking | Chronograph/73 Strings: public comp selection tools | PostgreSQL `comparable_sets` table stores selected public comparables per position. External market data feed provides current trading multiples. Benchmarking calculations automated in Python. |
| Multi-Level Approval Governance | Chronograph/73 Strings: approval layers and governance controls | PostgreSQL `valuation_approvals` table enforces sequential approval chain (analyst → portfolio manager → valuation committee). Segregation of duties enforced (preparer ≠ first approver). |
| IPEV & ASC 820 Compliance | Chronograph/73 Strings: standards alignment | Valuation methodology framework codifies IPEV Valuation Guidelines and ASC 820 requirements. Each valuation output carries methodology classification (Market Approach, Income Approach, Transaction Price). Audit trail documents compliance with selected methodology. |
| Capital Structure Modeling | 73 Strings: complex capital structures and waterfall analysis | Python engine models multi-tranche capital structures with liquidation preferences, PIK instruments, and convertible features. Waterfall analysis under multiple exit scenarios. |
| LP & Board Reporting Outputs | Chronograph/73 Strings: automated reporting | Python template engine generates LP-facing valuation schedules and board reporting packages from approved valuation data. Integrated with Corrino's AutoFill infrastructure. |
| Credit-Specific Valuation Module | 73 Strings 73 Value Credit: yield-based DCF and spread approaches | Python DCF engine with credit-specific methodologies: yield-to-maturity analysis, market spread comparison, recovery rate modeling. Handles PIK, delayed draw, and revolving facilities. |

### Application-Class Architectures

#### Document Drafting Apps — Reverend Mother, CHOAM

**Backend:** FastAPI (Python). FastAPI's async support is essential here — LLM drafting calls are long-running and must not block the server. Background task queues (Celery + Redis) manage draft generation jobs; the frontend polls for completion or receives a WebSocket notification when the draft is ready.

**Frontend:** React. Memo drafting and credit agreement redlining require rich text editing (a structured block editor like Lexical or TipTap), section-level navigation, version-comparison views (showing diffs between draft versions), and inline comment threads. React with Lexical gives full control over document rendering and editing UX.

**Document versioning:** Every draft version is stored in S3 with an immutable key (`memo/{deal_id}/{version_id}/{timestamp}.json`). Version metadata (version number, creator, timestamp, parent version, status) is persisted to PostgreSQL and replicated to Foldspace's document registry.

#### Workflow and Task Management Apps — Sardaukar, Atreides, Gom Jabbar

**Backend:** FastAPI + PostgreSQL. These apps are fundamentally state machines: an NDA is in one of [Received, Under Review, Redlines Sent, Countersigned]; a DD item is in one of [Open, Pending Response, Answered, Closed]. PostgreSQL's ACID guarantees and rich constraint/trigger model make it the right operational store for workflow state.

**Frontend:** React. Sardaukar's DD queue needs a Kanban-style or priority-queue view with drill-down to question/response threads; Atreides' closing checklist is a structured task manager with assignment and completion state; Gom Jabbar's NDA workflow is a sequential approval flow with document preview. All three require drag-and-drop, inline editing, or file upload — React is the right choice.

#### Optimistic Concurrency Control

All aggregate root tables in write-contended apps must include a `version` integer column, incremented on every state-changing write. The service layer issues updates with a version guard:

```sql
UPDATE dd_items SET status = :new_status, version = version + 1, updated_at = NOW()
WHERE id = :item_id AND version = :expected_version;
```

If zero rows are affected, the service layer raises a `ConcurrencyConflictError`, and the entrypoint returns `409 Conflict` with a `Retry-After: 0` header, signaling the client to re-fetch and retry. This pattern applies to the following aggregate root tables:

| App | Aggregate Root Table(s) | Contention Scenario |
|---|---|---|
| Sardaukar | `dd_items`, `dd_milestones` | Multiple analysts updating DD queue items for the same deal |
| Atreides | `closing_tasks`, `maker_checker_log` | Deal team and ops concurrently completing closing checklist items |
| Gom Jabbar | `nda_workflows` | Parallel approval routing decisions on the same NDA |
| Stillsuit | `loan_positions`, `agent_notices` | Concurrent payment processing and amendment execution on the same facility |
| Heighliner | `syndication_allocations`, `amendment_votes` | Multiple co-lenders submitting allocation updates or amendment votes simultaneously |

The `version` column is indexed and included in the outbox event payload so downstream consumers can detect out-of-order processing. Apps that are read-heavy with infrequent writes (Corrino, Mentat, Melange) or append-only (Landsraad IC decisions) do not require optimistic locking — their concurrency is managed by Snowflake Dynamic Tables or immutability constraints respectively.

#### CRM and Relationship Management — Thumper, Gurney

**Backend:** FastAPI + PostgreSQL. Gurney is the firm's operational CRM. The relationship graph is best modeled in PostgreSQL with proper foreign keys and indexes rather than in Snowflake.

**Frontend:** React. A CRM interface with contact profiles, organization hierarchies, interaction timelines, and deal relationship maps is richer than Streamlit can deliver. Graph visualization (React Flow or D3.js) for Gurney's relationship mapping view. Thumper's pipeline view — a funnel/stage visualization across all active deals — similarly benefits from a custom React component.

#### Loan Operations and Administration — Stillsuit

**Backend:** FastAPI + PostgreSQL as primary operational ledger. Stillsuit is the system of record for all post-close loan activity. It requires ACID transactions, row-level locking, and point-in-time query capability.

**Frontend:** React. Loan administration interfaces — payment schedules, balance sheets, amendment tracking, compliance certificate delivery — require tabular data management with inline editing, file attachment, and audit trail views.

### Master Data Translation at Ownership Transfer Boundaries

#### Facility Model Translation: CHOAM (Terms) → Stillsuit (Operations)

The Foldspace Master Data API implements a translation layer for the Facility entity at the ownership transfer boundary. When Stillsuit activates a loan (triggered by the funding confirmation handoff), the closing package includes CHOAM's terms-oriented Facility representation. The MDM API translates this into Stillsuit's operations-oriented Facility representation using the following field mapping, implemented as a Pydantic model-to-model transformer in `shared/schemas/facility/translation.py`:

| CHOAM Field (Terms Model) | Stillsuit Field (Operations Model) | Translation Rule |
|---|---|---|
| `commitment_amount` | `original_commitment` | Direct copy; immutable after activation |
| `pricing_grid[]` (spread tiers by leverage) | `current_applicable_margin` | Resolve to initial margin using Day 1 leverage ratio from closing package |
| `fee_schedule[]` (upfront, commitment, admin) | `fee_ledger_entries[]` | Expand each fee into a ledger entry with `accrual_start`, `frequency`, `amount` |
| `covenant_definitions[]` | `covenant_schedule[]` | Map each covenant to a monitoring schedule with `test_frequency`, `first_test_date`, `threshold` |
| `maturity_date` | `maturity_date` | Direct copy |
| `facility_type` (revolver / term / delayed-draw) | `facility_type` | Direct copy; determines draw-down and repayment behavior in Stillsuit |
| `currency` | `currency` | Direct copy |
| `day_count_convention` | `day_count_convention` | Direct copy; critical for interest accrual calculations |
| `payment_frequency` | `payment_schedule_template` | Expand into a full payment schedule from activation date through maturity |

**Validation at Translation Time:** The translation layer must validate that all required CHOAM fields are present and non-null before producing the Stillsuit model. If translation fails (e.g., missing `day_count_convention`), the loan activation is rejected with a `422 Unprocessable Entity` response, and the closing package is held in pending state per the existing funding handoff failure handling.

**Versioning:** The translation mapping is versioned alongside the `FundingConfirmedRequest` schema in `shared/schemas/funding/`. Changes to the mapping require a new schema version and follow the existing 90-day backward-compatibility guarantee.

#### Borrower Model Translation: Gurney (Relationship) → Stillsuit (Operations)

The Foldspace Master Data API implements a translation layer for the Borrower entity at the ownership transfer boundary. At loan activation, Stillsuit receives Borrower identity data derived from Gurney's golden record. The MDM API translates Gurney's relationship-oriented model into Stillsuit's operations-oriented model using the following field mapping, implemented as a Pydantic transformer in `shared/schemas/borrower/translation.py`:

| Gurney Field (Relationship Model) | Stillsuit Field (Operations Model) | Translation Rule |
|---|---|---|
| `legal_entity_name` | `legal_entity_name` | Direct copy |
| `organization.tax_id` | `tax_id` | Direct copy; required for regulatory reporting |
| `organization.jurisdiction` | `jurisdiction_of_formation` | Direct copy |
| `organization.address` | `registered_address` | Direct copy; used for notice delivery |
| `primary_contact` (from contact graph) | `authorized_signatory` | Requires explicit designation — not auto-copied from Gurney's primary contact. Deal team must confirm signatory via the closing checklist (Atreides) |
| `kyc_status` (from Gom Jabbar NDA/KYC flow) | `kyc_aml_status` | Mapped from Gom Jabbar's status enum to Stillsuit's compliance enum |
| `pitchbook_enrichment`, `capiq_enrichment` | (not transferred) | Enrichment metadata is Gurney-internal context; Stillsuit does not consume it. This enforces least-privilege: Stillsuit receives only the operational fields required for loan servicing |
| `interaction_history`, `coverage_assignments` | (not transferred) | CRM-specific data remains within Gurney's bounded context |

**Classification Enforcement at Translation:** The translation layer applies the blueprint's data classification scheme at the field level. Fields classified as CONFIDENTIAL in Gurney (e.g., contact PII) that are not required by Stillsuit's operations model are excluded from the translation output. The DCA contract between Gurney and Stillsuit must enumerate the exact fields transferred, and the translation layer validates against this contract at runtime.

**Post-Transfer Enrichment:** After ownership transfer, Stillsuit may receive updated Borrower data from external sources (e.g., agent notices, borrower correspondence). These updates flow through the Foldspace Master Data API and are subject to the MDM Conflict Resolution Protocol (Stillsuit wins post-close). Gurney continues to publish enrichment data for the same `borrower_id`; the MDM API merges enrichment into the golden record but Stillsuit's operational fields take precedence per the conflict protocol.

### Analytics and BI Apps — Corrino, Mentat, Melange

**Corrino:** Streamlit in Snowflake. Corrino's primary function is consuming structured portfolio data from `ARRAKIS_CONSUMPTION`. The one exception: complex alerting logic should be Snowflake Tasks rather than Streamlit logic.

**Mentat:** FastAPI backend + Snowflake + Python computational layer. Streamlit frontend for scenario exploration and sensitivity analysis.

**Melange:** FastAPI backend + Snowflake. Streamlit interface for valuation review. LP report and board material generation uses the LLM service for structured narrative generation from valuation outputs.

### Presentation, Collaboration, Approval — Landsraad

React + FastAPI + WebSocket Layer. The WebSocket layer uses Redis pub/sub as the broadcast layer. Permission enforcement, immutable audit trail, and async annotation are all preserved.

### Health Check Endpoint Contract

Every FastAPI application (all 14, including Foldspace) must expose two health check endpoints, configured as Kubernetes probe targets in the app's Helm chart:

`GET /health/live` — **Liveness probe.** Returns `200 OK` with `{"status": "alive"}` if the FastAPI process is running and responsive. This endpoint must not check downstream dependencies — its sole purpose is to detect a hung or deadlocked process. If this endpoint fails, Kubernetes restarts the pod. Timeout: 3s. Failure threshold: 3 consecutive failures.

`GET /health/ready` — **Readiness probe.** Returns `200 OK` with `{"status": "ready"}` if the app can serve traffic. This endpoint verifies: (a) the PostgreSQL connection pool has at least one available connection, (b) the Redis connection is responsive (single PING), and (c) the Foldspace client's circuit breakers for critical endpoints are not all open. If any check fails, returns `503 Service Unavailable` with `{"status": "not_ready", "checks": {...}}` detailing which dependency is unavailable. When not ready, Kubernetes removes the pod from the Service endpoint list, stopping traffic routing to it without restarting it. Timeout: 5s. Failure threshold: 2 consecutive failures.

Streamlit-in-Snowflake apps (Corrino, portions of Mentat and Melange) are exempt — Snowflake manages their lifecycle. The Foldspace Observatory, DCA, and API Catalog (co-deployed with Foldspace) inherit Foldspace's health probes.

Health check responses must not include sensitive data (no connection strings, no credentials, no deal IDs). The `arrakis-base` Helm chart includes default probe configuration that all per-app charts inherit.

## 5. Governance and Observability Layer

This section describes the five named, deployed governance and observability components that enforce data contracts, define the enterprise metamodel, catalog every data product, monitor operational health, and codify the firm's data classification scheme. Every component specified here is a deployed service — not a future aspiration.

### 5.1 Data Contract Application (DCA)

The DCA plays the central role in the security architecture as the Policy Administration Point (PAP) and Policy Information Point (PIP). It is built as a first-party Foldspace component rather than purchased from a third-party security vendor — this avoids tight coupling to any specific vendor's data security application.

The DCA is a standalone FastAPI service with its own PostgreSQL schema (`foldspace_dca`), deployed as a Foldspace component. It is not embedded in Kong or any security tool.

**DCA Data Model:**

| Entity | Key Fields |
|---|---|
| `data_contracts` | `contract_id`, `provider_app`, `consumer_app`, `data_product_uri` (Snowflake schema + table/view), `schema_version`, `sla_freshness`, `sla_availability`, `allowed_usage_purpose` (enum: internal_analytics, lp_reporting, regulatory, audit), `sensitive_classifications_present` (array), `validity_start`, `validity_end`, `status` (draft, approved, active, deprecated, revoked, under_review), `approved_by`, `approved_at` |
| `contract_versions` | `version_id`, `contract_id`, `schema_version`, `change_description`, `changed_by`, `changed_at` |
| `contract_approvals` | `approval_id`, `contract_id`, `approver_role`, `approver_id`, `decision`, `decided_at`, `rationale` |

**DCA Workflow:**

1. **Creation:** A developer or data engineer creates a contract via the DCA API (`POST /dca/v1/contracts`), specifying provider app, consumer app, data product URI, schema version, SLA, and usage purpose.
2. **Approval:** The contract requires approval from the providing app's data owner and the platform team. The DCA routes the approval request and tracks status.
3. **Activation:** Upon approval, the DCA emits a `data-contract.approved` event to Redpanda. The Foldspace permission provisioning service subscribes to this event and automatically provisions the consuming app's Snowflake role with SELECT on the specified schema/table.
4. **Versioning:** Schema changes to a data product require a new contract version. The DCA enforces: the new version must be created and approved before the schema change is deployed.
5. **Enforcement:** No consuming app's Snowflake read permissions are provisioned outside the DCA workflow. Kong API gateway checks DCA contract status before routing API calls between apps.
6. **Lifecycle Event Emissions:** The DCA emits Redpanda events on every status transition and version creation, not only on approval. The following events are published to a `data-contract.*` topic namespace:

| Event | Trigger | Payload (key fields beyond `contract_id`) | Consumer Action |
|---|---|---|---|
| `data-contract.approved` | Contract approved (existing step 3) | `provider_app`, `consumer_app`, `data_product_uri`, `schema_version` | Permission provisioning service grants Snowflake SELECT |
| `data-contract.deprecated` | Status transitions to `deprecated` | `provider_app`, `consumer_app`, `data_product_uri`, `sunset_date`, `migration_uri` (optional — points to successor contract) | Consuming app receives advance notice; Observatory flags the consuming app's dependency as at-risk |
| `data-contract.revoked` | Status transitions to `revoked` | `provider_app`, `consumer_app`, `data_product_uri`, `revocation_reason` | Permission provisioning service revokes Snowflake SELECT; consuming app receives immediate alert |
| `data-contract.version-created` | New row in `contract_versions` | `provider_app`, `consumer_app`, `data_product_uri`, `old_schema_version`, `new_schema_version`, `change_description` | Consuming app team receives notification of upcoming schema change; consuming app can pre-validate compatibility |

All events use Avro schemas registered in the Redpanda Schema Registry under the `data-contract` namespace. The `data-contract.deprecated` and `data-contract.revoked` events additionally trigger a Slack notification to the consuming app team's channel (via the existing Observatory alert routing).

#### DCA Contract Semantic Versioning Policy

All DCA contracts follow semantic versioning (`MAJOR.MINOR.PATCH`). The platform team enforces the following classification when approving contract version increments:

| Change Type | Version Bump | Backward Compatible | Examples |
|---|---|---|---|
| Patch | x.y.Z → x.y.Z+1 | Yes | Updating contract metadata or description fields. Changing stakeholder or approver assignments. Correcting a data quality rule threshold without altering the rule's dimension or scope. |
| Minor | x.Y.z → x.Y+1.0 | Yes | Adding a new column to the data product with a default value or nullable constraint. Adding a new optional quality rule. Revising a data quality threshold that relaxes (not tightens) a constraint. Adding a new `allowed_usage_purpose` value. |
| Major | X.y.z → X+1.0.0 | No | Removing a column from the data product. Changing a column's data type. Renaming a column. Tightening a quality rule in a way that may reject previously valid data. Changing `sla_freshness` or `sla_availability` to a less permissive target. |

The DCA API's `POST /dca/v1/contract-versions` endpoint validates that the requested version bump matches the declared change type. A major version increment triggers a mandatory 90-day parallel support window (consistent with the API deprecation policy in Section 3). The DCA emits a `data-contract.major-version-created` event to Redpanda to alert all consuming apps listed in the contract's `consuming_apps` field.

#### DCA Contract — Extended Operational SLI Fields

The following fields are part of the `data_contracts` entity in the DCA data model. All fields are nullable to permit incremental adoption — contracts for data products with regulatory or LP reporting consumers should populate them at contract creation; other contracts may adopt them as operational maturity grows.

| Field | Type | Description |
|---|---|---|
| `sla_latency_minutes` | INTEGER NULL | Maximum allowed time in minutes between the source operational event and the data product's availability at the CONSUMPTION layer. Measured by the Observatory as the delta between `_loaded_at` in RAW and the corresponding record's appearance in CONSUMPTION. |
| `sla_retention_days` | INTEGER NULL | Minimum number of days the data product's records must be retained in the CONSUMPTION layer before archival or deletion. For regulatory data products (e.g., `IC_AUDIT`, `LP_REPORTING`), this value must be set and must equal or exceed the firm's record retention policy. |
| `sla_time_to_detect_minutes` | INTEGER NULL | Maximum allowed time in minutes between a quality or freshness breach occurring and the Observatory detecting it. Default Observatory polling interval is 15 minutes (Section 5.4); this field formalizes the contractual ceiling. |
| `sla_time_to_repair_hours` | INTEGER NULL | Maximum allowed time in hours between breach detection and breach resolution. Maps to the Observatory escalation path tiers: contracts with `sla_time_to_repair_hours ≤ 1` trigger immediate PagerDuty escalation on first breach rather than waiting the standard 30-minute threshold. |
| `sla_update_frequency` | VARCHAR NULL | Expected refresh cadence as a human-readable interval (e.g., `real-time`, `5-minute`, `daily`, `monthly`). Informational — used by the Data Contract Status Grafana dashboard for consumer expectation-setting. |

The Observatory's freshness monitoring task (Section 5.4) compares `sla_latency_minutes` against the measured end-to-end latency and `sla_time_to_detect_minutes` against the polling interval, logging any contractual ceiling violation to `ARRAKIS_CONSUMPTION.DATA_QUALITY` with `breach_type = 'sli_ceiling_exceeded'`.

### 5.2 Enterprise Metamodel

The enterprise metamodel defines the logical entities and relationships that the data catalog manages. The Arrakis enterprise metamodel, stored in the data catalog's PostgreSQL backing store:

```
Data Domain          (1) ──── owns ────►          (N) Data Product
Data Product         (1) ──── contains ──►        (N) Data Product Element
Data Product Element (N) ◄── maps to ──►          (N) Glossary Term
Data Product Element (1) ──── physically realized as ──► (N) Physical Attribute
Data Product         (1) ──── owned by ──►        (1) Application
Application          (1) ──── owned by ──►        (1) Owner (team/individual)
Data Product Element (1) ──── classified as ──►   (1) Classification
Data Product         (N) ◄── governed by ──►      (N) Data Contract
```

Domains map to the Arrakis application groupings: Origination (Thumper, Gom Jabbar, Gurney), Deal Execution (Sardaukar, Mentat, Reverend Mother, Landsraad, CHOAM), Syndication & Closing (Heighliner, Atreides), Post-Close Operations (Stillsuit, Corrino, Melange), and Platform (Foldspace).

### 5.3 Data Catalog

The data catalog is a named, deployed service. The Arrakis data catalog is implemented as an OpenMetadata instance (OSS, Apache 2.0 licensed, purpose-built for data catalogs with native Snowflake connector, lineage extraction, and classification tagging). Deployment: containerized on Kubernetes, backed by its own PostgreSQL database and Elasticsearch index.

**Population pipeline:**

- Snowflake metadata connector (OpenMetadata's native connector) extracts schema metadata from all three Snowflake databases nightly
- Classification tags are applied at column level via OpenMetadata's tag API, populated from the DCA's `sensitive_classifications_present` field
- Glossary terms are maintained by the platform team and linked to physical attributes via the metamodel
- Pipeline lineage is captured from Redpanda topic → RAW schema mappings, and table lineage from RAW → CURATED → CONSUMPTION via Snowflake Dynamic Table definitions
- Column lineage is captured for all CONSUMPTION layer attributes that feed LP reports (`LP_REPORTING` schema) or regulatory outputs, using OpenMetadata's lineage API populated by a nightly lineage extraction job that parses Dynamic Table SQL definitions
- DCA contract metadata ingestion populates custom properties on CONSUMPTION-layer table and view assets, linking each asset to its governing data contract(s) and surfacing SLA targets, consumer lists, and contract status in the catalog UI

#### DCA Contract Metadata Population in OpenMetadata

The OpenMetadata population pipeline is extended with a DCA contract ingestion job that runs nightly alongside the existing Snowflake metadata connector:

1. **Data source:** The job queries the DCA PostgreSQL schema (`foldspace_dca`) for all contracts with status `active`, `deprecated`, or `under_review`.
2. **Mapping:** For each contract, the job creates or updates a "Data Contract" custom property set on the corresponding OpenMetadata table/view asset identified by the contract's `data_product_uri`. The custom properties are:

| OpenMetadata Custom Property | DCA Source Field |
|---|---|
| `contract_id` | `data_contracts.contract_id` |
| `contract_status` | `data_contracts.status` |
| `provider_app` | `data_contracts.provider_app` |
| `consuming_apps` | `data_contracts.consuming_apps` (array) |
| `schema_version` | `data_contracts.schema_version` |
| `sla_freshness` | `data_contracts.sla_freshness` |
| `sla_availability` | `data_contracts.sla_availability` |
| `allowed_usage_purpose` | `data_contracts.allowed_usage_purpose` |
| `approved_by` | `data_contracts.approved_by` |
| `approved_at` | `data_contracts.approved_at` |

3. **Lifecycle sync:** Contracts with status `revoked` are removed from the OpenMetadata asset's custom properties. Contracts transitioning to `deprecated` update the `contract_status` property and trigger an OpenMetadata announcement on the asset (visible to catalog browsers as a deprecation banner).

### 5.4 Foldspace Observatory (Data Observability)

Data observability is implemented as a separate component monitoring freshness, volume, schema, lineage, and quality. The Foldspace Observatory is a standalone FastAPI service that monitors data product health across five dimensions:

| Dimension | What Is Monitored | Alert Threshold | Implementation |
|---|---|---|---|
| Freshness | Time since last refresh per data product (measured by `_loaded_at` timestamp in RAW/CURATED/CONSUMPTION) | Breach of data product's SLA freshness target (defined in DCA contract) | Snowflake Task runs every 15 minutes, compares `MAX(_loaded_at)` against SLA target, writes breach records to `ARRAKIS_CONSUMPTION.DATA_QUALITY` |
| Volume | Record count per data product per refresh cycle | Deviation >20% from 30-day rolling average | Snowflake Task computes rolling average and current count; deviation breaches trigger `data-quality.sla-breach` event to Redpanda |
| Schema | Column names, types, and nullability per RAW landing table | Unexpected column additions or type changes | Pre-landing schema validation in the Snowpipe ingestion layer; schema drift events emitted to Redpanda and logged to `DATA_QUALITY` |
| Lineage | End-to-end data flow from source app to consumption schema | Broken lineage (a consumption table references a curated table that has not been refreshed) | Nightly lineage validation job traces from CONSUMPTION back to RAW and flags any broken links |
| Quality | Data quality score per data product (composite of completeness, accuracy, consistency checks) | Score below defined threshold (configurable per product, default 95%) | Great Expectations suites run as Snowflake Tasks; results written to `DATA_QUALITY`; trend dashboard in Grafana |

**Alert routing:** Observatory writes all breach and anomaly records to `ARRAKIS_CONSUMPTION.DATA_QUALITY` and emits Redpanda events. A Grafana alert rule on the `DATA_QUALITY` table routes alerts to PagerDuty/OpsGenie based on severity and owning app team.

#### DATA_QUALITY Schema — Quality Check Records

Each quality gate check result written to `ARRAKIS_CONSUMPTION.DATA_QUALITY` carries a `quality_dimension` classification. The following dimension taxonomy is adopted, aligned with the EDM Council standard:

| Dimension | Definition | Arrakis Gate Mapping |
|---|---|---|
| COMPLETENESS | Required fields are non-null | Bronze→Silver: null checks on required fields |
| CONFORMITY | Values match expected type, format, and domain | Bronze→Silver: type validation, enum value set checks |
| CONSISTENCY | Values are coherent across related fields and stores | Silver→Gold: cross-entity reconciliation, double-entry validation |
| ACCURACY | Values are correct relative to business rules | Silver→Gold: business rule validation (e.g., covenant ratio bounds, non-negative payments) |
| UNIQUENESS | No duplicate records on primary key | Silver→Gold: deduplication confirmation |
| TIMELINESS | Data is available within SLA window | Observatory: freshness monitoring; Silver→Gold: SLA freshness check |
| COVERAGE | Expected records are present in the dataset | Observatory: volume anomaly detection (deviation >20% from rolling average) |

The `DATA_QUALITY` table includes the following columns for quality check records (distinct from the existing breach records for freshness, volume, schema, and lineage dimensions): `check_id` (UUID), `data_product_uri` (VARCHAR), `check_timestamp` (TIMESTAMP_NTZ), `quality_dimension` (VARCHAR — one of the seven values above), `check_name` (VARCHAR — the specific GE expectation or dbt test name), `gate_layer` (ENUM: `bronze_silver`, `silver_gold`), `result` (ENUM: `pass`, `fail`, `warn`), `detail` (VARIANT — GE/dbt result payload), `record_count_checked` (INTEGER), `failure_count` (INTEGER).

The Quality Score trend panel in the Data Product Quality Scores Grafana dashboard (Section 6.4) is extended to include a dimension breakdown heatmap showing pass/fail rates per quality dimension per data product over the trailing 30 days.

**SLA breach escalation path:**

1. First breach → Slack notification to owning app team's channel
2. Breach persists >30 minutes → PagerDuty alert to on-call engineer
3. Breach persists >2 hours → Escalation to platform team lead and data steward
4. Breach persists >4 hours → Escalation to head of technology

#### MCP Tool Usage Metrics — Observatory Dimension

The Foldspace Observatory adds an AI Tool Usage dimension to its monitoring framework, sourced from the `tool_invocations` data captured in the AI output audit trail.

| Metric | Source | Alert Threshold | Implementation |
|---|---|---|---|
| Tool invocation error rate | `tool_invocations[].result_status` aggregated per `tool_name` over rolling 1-hour window | >5% ERROR or TIMEOUT rate for any tool | Snowflake Task queries `ARRAKIS_RAW.APP_EVENTS.tool_invocations`, writes breach records to `DATA_QUALITY` |
| Tool latency p95 | `tool_invocations[].latency_ms` per `tool_name` | p95 exceeds 2× the tool's 30-day rolling p95 baseline | Snowflake Task computes rolling baseline; deviation emits `data-quality.sla-breach` to Redpanda |
| Tool invocation volume anomaly | Count of invocations per `tool_name` per hour | Deviation >50% from 7-day rolling hourly average (detects both spikes and unexpected drops) | Snowflake Task; volume drop may indicate a broken upstream workflow silently skipping tool calls |
| Stale data detection | `tool_invocations[].result_row_count` combined with upstream data product freshness from the Freshness dimension | Tool returns data whose source data product has breached its SLA freshness target | Cross-dimension correlation job; flags tools serving stale data to Claude |

Alert routing follows the existing Observatory escalation path: first breach → Slack notification to platform team, persistent >30 minutes → PagerDuty, persistent >2 hours → platform team lead. A dedicated Grafana dashboard ("AI Tool Health") surfaces all four metrics with drill-down by tool name, calling app, and time range.

#### Downstream Consumer Notification on Persistent SLA Breach

When an Observatory freshness, volume, or quality breach persists beyond 30 minutes (the PagerDuty threshold in the existing escalation path), the Observatory performs a downstream consumer lookup and emits targeted notifications:

1. **Consumer lookup:** The Observatory queries the DCA for all active contracts where the breaching data product appears as `data_product_uri`. Each contract's `consumer_app` field identifies an affected downstream application.
2. **Transitive lookup:** For each consuming app, the Observatory checks whether that app is itself a data product provider with its own DCA contracts. If so, its consumers are added to the notification set. The lookup traverses at most three levels of depth to avoid circular dependencies (sufficient for Arrakis's deepest chain: Stillsuit → Corrino → Melange → `LP_REPORTING` views).
3. **Notification event:** The Observatory emits a `data-quality.upstream-breach-active` event to Redpanda with payload: `{breach_id, breaching_data_product_uri, breach_dimension, breach_started_at, affected_consumer_app, transitive_depth}`. Each affected consumer app receives a distinct event.
4. **Consumer-side action:** Consuming apps that subscribe to `data-quality.upstream-breach-active` display a staleness warning banner in their UI (for React apps) or log the upstream breach in their operational dashboard (for Streamlit apps). No automated data suppression — human operators decide whether to proceed with stale data.
5. **Resolution notification:** When the breach is resolved, the Observatory emits `data-quality.upstream-breach-resolved` with the same `breach_id`, allowing consuming apps to clear the warning.

This notification supplements but does not replace the existing producer-oriented escalation path.

#### Observatory → DCA Persistent Breach Feedback Rule

When a data product accumulates three or more SLA breaches of the same dimension (freshness, volume, quality, or latency) within a rolling 7-day window, the Observatory triggers a DCA contract review:

1. **Trigger:** The Observatory's nightly aggregation job queries `ARRAKIS_CONSUMPTION.DATA_QUALITY` for breach records grouped by `data_product_uri` and `breach_dimension`. If any data product has ≥3 breaches of the same dimension within the trailing 7 calendar days, the job emits a `data-contract.review-triggered` event to Redpanda with payload: `{contract_id, data_product_uri, breach_dimension, breach_count, breach_window_start, breach_window_end}`.
2. **DCA action:** The DCA subscribes to `data-contract.review-triggered` and transitions the affected contract's status from `active` to `under_review`. This status change emits the standard `data-contract.status-changed` event. The contract remains enforceable — consuming apps retain their Snowflake permissions — but the `under_review` status appears on the Data Contract Status Grafana dashboard and requires explicit re-approval from the providing app's data owner and the platform team to return to `active`.
3. **Resolution:** The review must conclude within 10 business days. The outcome is one of: (a) SLA targets are revised via a new contract version (following the semantic versioning policy), (b) a remediation plan is filed and the contract is returned to `active` with a follow-up review date, or (c) the contract is deprecated if the data product can no longer meet viable SLA targets.
4. **DCA data model addition:** The status enum value `under_review` is part of the `data_contracts` entity.

### 5.5 Data Classification Scheme

A formal four-tier classification scheme governs every column in the Snowflake landing zone:

| Tier | Label | Examples | Column Masking | Required Access Scope |
|---|---|---|---|---|
| RESTRICTED | Highest sensitivity | IC deliberations, individual vote records (pre-reveal), fund economics above co-lender tranche, negotiation positions, AI draft vs. final deltas | Yes — Snowflake column masking policy applied. Data visible only to `ARRAKIS_ADMIN` and specifically permissioned roles | Deal team principals, IC chair (post-reveal), senior management |
| CONFIDENTIAL | Deal-level sensitive | Deal financial data, borrower PII, credit agreement economics, payment amounts, model outputs, valuation determinations, expert call transcripts | Yes — column masking policy applied. Masked for Co-Lender and Borrower roles | Deal team, authorized IC members, operations team |
| INTERNAL | Firm operational | Deal metadata, pipeline data, portfolio aggregates, precedent library (anonymized), coverage assignments | No masking required | All internal users with appropriate role |
| PUBLIC | Externally shareable | Anonymized market benchmarks, published LP reports, aggregate portfolio statistics | No masking required | LP portal users, external auditors, board |

**Classification enforcement architecture:**

1. Classification metadata is stored as column-level tags in the OpenMetadata data catalog
2. The DCA's contract approval workflow checks classification: if a data product contains RESTRICTED or CONFIDENTIAL columns, the contract must specify handling requirements
3. A nightly Snowflake Task reads classification metadata from the catalog API and applies/updates Snowflake column masking policies on tagged columns
4. The masking policy references the user's Snowflake role to determine visibility (e.g., `ARRAKIS_COLENDER` role sees masked values for RESTRICTED columns)

### 5.6 MDM Conflict Resolution Protocols

The conflict resolution protocol for each entity is specified in the Master Data Entities table in Section 1: conflict detection via the Foldspace Master Data API, event emission to `mdm.conflict-raised`, resolution within the defined SLA, and event emission to `mdm.conflict-resolved`. All conflicts are logged as append-only records in the data catalog.

---

## 6. DataOps and Operational Maturity

This section specifies how data quality gates are implemented at each tier transition, how the CI/CD pipeline enforces those gates as blocking stages, the runbooks every operational workflow must carry, and the Grafana dashboards that surface data product health.

### 6.1 Data Quality Gate Implementation

Data quality gates are defined at Bronze→Silver and Silver→Gold, implemented via Great Expectations or dbt tests.

**Decision: Great Expectations for Bronze→Silver; dbt tests for Silver→Gold.**

**Rationale:** Bronze→Silver gates validate raw data quality (schema conformance, null checks, referential integrity) — these are best expressed as Great Expectations validation suites that run against raw Snowflake tables. Silver→Gold gates validate business rules, deduplication, and SLA freshness — these are best expressed as dbt tests that operate alongside the dbt transformations that power Silver→Gold materialization. This split applies the right tool at each layer.

**Bronze→Silver quality gates (Great Expectations):**

- Schema validation: incoming records match the expected Avro schema registered in the Schema Registry
- Null checks: required fields per data product definition are non-null
- Referential integrity: foreign key references to MDM entity IDs (`deal_id`, `company_id`, `facility_id`) exist in `ARRAKIS_CONSUMPTION.MDM`
- Type validation: numeric fields are numeric, date fields are valid dates, enum fields are in the canonical value set

**Silver→Gold quality gates (dbt tests):**

- Business rule validation: domain-specific rules per data product (e.g., covenant ratio between 0 and 100, payment amount non-negative)
- Deduplication confirmation: no duplicate records on primary key
- SLA freshness check: curated record timestamp within defined freshness SLA of raw record
- Cross-entity consistency: amounts reconcile (e.g., loan payments sum to expected schedule)

**Quality gate failure disposition.** Quality gate failures are classified into two severity levels with distinct dispositions:

1. **Structural failures** (schema mismatch, Avro deserialization error, unexpected column type): The entire batch is rejected. No records are promoted to the next tier. The pipeline emits a `data-quality.gate-failed` event to Redpanda with `{app_id, gate_tier, failure_type: "structural", batch_id, record_count, error_detail}`. The Observatory escalation path (Section 5.4) applies. Root cause resolution — typically a schema migration or upstream code fix — is required before the pipeline retries.

2. **Record-level failures** (null check on a required field, referential integrity violation, business rule violation): Passing records are promoted to the next tier. Failing records are written to a quarantine table in the same Snowflake database: `ARRAKIS_RAW._QUARANTINE` for Bronze→Silver failures, `ARRAKIS_CURATED._QUARANTINE` for Silver→Gold failures. Each quarantine record includes: `{source_table, record_pk, gate_name, failure_reason, failed_at, batch_id}`. The pipeline emits a `data-quality.gate-failed` event with `{failure_type: "record", failed_count, total_count, failure_rate}`. If the record-level failure rate exceeds 5% of the batch, the pipeline halts entirely (treated as structural) to prevent silent data degradation.

Quarantine tables are reviewed by the owning app team. Remediated records are replayed through the pipeline by re-inserting them into the source landing schema. Quarantine records older than 30 days are archived to `ARRAKIS_RAW._QUARANTINE_ARCHIVE` and excluded from Observatory quality score calculations. Archived quarantine records remain subject to applicable regulatory and fund-level retention requirements and must not be purged before their retention obligation expires, even if older than 30 days.

**Batch volume sanity check.** Each Great Expectations suite includes an `expect_table_row_count_to_be_between` expectation that validates the current batch record count falls within a configurable range. The default bounds are: minimum 1 record (rejects empty batches), maximum 10× the 30-day rolling average record count for that landing schema (rejects anomalous volume spikes that suggest deduplication failures or upstream replay storms). Bounds are configured per app in the Great Expectations suite YAML and may be overridden for apps with legitimately variable volumes (e.g., Melange during quarterly valuation cycles). The 30-day rolling average is computed from a `_PIPELINE_STATS` table in `ARRAKIS_RAW`, populated by each pipeline run upon completion with the run's record count, target schema, and run timestamp; this provides a reliable, auditable baseline compatible with all data-loading patterns (Snowpipe, COPY INTO, dbt-driven materializations) across the 14 applications. A volume sanity failure is treated as a structural failure per the quality gate failure disposition: the entire batch is rejected and the `data-quality.gate-failed` event is emitted.

### 6.2 CI/CD Pipeline with Quality Gates

Independent CI/CD pipelines per application include quality gates as blocking stages.

```
┌──────────────┐     ┌──────────┐     ┌────────────────┐     ┌───────────────────┐
│ Code Push    │────►│ Lint     │────►│ Unit Tests     │────►│ Integration Tests │
│ (feature/*)  │     │ (ruff)   │     │ (pytest)       │     │ (docker-compose)  │
└──────────────┘     └──────────┘     └────────────────┘     └───────────────────┘
                                                                       │
                                                                       ▼
┌───────────────────────────┐         ┌──────────────────────────────────────────┐
│ Snowflake Schema          │◄────────│ DATA QUALITY GATE                        │
│ Migration (schemachange)  │         │ • Great Expectations suite against       │
│ [BLOCKING GATE]           │         │   staging Snowflake landing schema       │
└───────────────────────────┘         │ • dbt test suite against staging         │
            │                         │   curated/consumption schemas            │
            ▼                         │ [BLOCKING — PR cannot merge if           │
┌──────────────────┐                  │  quality gate fails]                     │
│ Build Docker     │                  └──────────────────────────────────────────┘
│ Image → ECR      │
└──────────────────┘
            │
            ▼
┌────────────────────┐         ┌──────────────────────┐
│ Deploy to Staging  │────────►│ Deploy to Main       │
│ (Helm upgrade)     │         │ (requires approval)  │
└────────────────────┘         └──────────────────────┘
```

**Schemachange as a blocking gate:** Snowflake schema migrations are managed by schemachange (Snowflake's open-source migration tool). No app deploy proceeds if its corresponding Snowflake migration has not been applied and validated in the staging environment. The CI pipeline checks migration status before proceeding to the Docker build stage.

**Schema compatibility gate.** A blocking stage is inserted between the integration tests stage and the existing data quality gate:

```
Integration Tests → SCHEMA COMPATIBILITY GATE [BLOCKING] → Data Quality Gate → ...
```

The schema compatibility gate performs the following checks for each Avro schema file modified in the PR:

1. **Deserialize and parse:** Validate that the modified `.avsc` file is syntactically valid Avro.
2. **Registry compatibility check:** Submit the proposed schema to the Redpanda Schema Registry's `/compatibility/subjects/{subject}/versions/latest` endpoint. The registry evaluates the proposed schema against the latest registered version using the subject's compatibility mode (FULL by default). If the registry returns `is_compatible: false`, the gate fails and the PR cannot merge.
3. **Breaking change detection:** If a schema change is intentionally breaking (requiring the dual-stream migration pattern), the developer must include a `BREAKING_SCHEMA_CHANGE.md` file in the PR that documents the migration plan. The gate checks for this file when compatibility fails and passes the PR to human review instead of auto-blocking.

The gate is implemented as a GitHub Actions step using the Redpanda Schema Registry HTTP API against the staging registry instance. Schema files are stored in each app's repository under `schemas/avro/` and version-controlled alongside application code.

**API Contract Test Stage.** A contract test stage is added to the CI/CD pipeline between the integration test stage and the data quality gate:

```
┌──────────────────┐    ┌──────────────────────────────────────────┐
│ Integration Tests│───►│ API CONTRACT TESTS                       │
│ (docker-compose) │    │ • For each Foldspace endpoint this app   │
└──────────────────┘    │   consumes: verify request/response      │
                        │   schemas match the Pydantic models      │
                        │   registered in the API Catalog          │
                        │ • For each Redpanda topic this app       │
                        │   consumes: verify Avro deserialization  │
                        │   against the registered schema          │
                        │ [BLOCKING — PR cannot merge if           │
                        │  contract test fails]                    │
                        └──────────────────────────────────────────┘
```

**Implementation:** Each consuming app maintains a `tests/contracts/` directory containing lightweight contract test files. Each contract test constructs a sample payload using the consuming app's expected Pydantic model, serializes it, and deserializes it against the producer's registered schema (fetched from `shared/schemas/`). This is a schema-compatibility check, not a live integration test — it runs without any running services and completes in seconds.

When a producer app modifies a Pydantic schema in `shared/schemas/`, the CI pipelines of all registered consuming apps (identified via the API Catalog's `consuming_apps` field) are triggered to re-run their contract tests. If any consumer's contract test fails, the producer's PR is blocked until either the schema change is made backward-compatible or the consuming apps are updated.

This complements the Avro schema compatibility check for Redpanda events by extending the same verification principle to synchronous REST API contracts.

**Intra-Service Test Pyramid.** The "Unit Tests (pytest)" CI/CD stage for each FastAPI application runs three test tiers in order, corresponding to the layering standard defined in Section 4:

**Tier 1 — Domain model tests** (`tests/unit/test_domain.py`): Exercise aggregate root methods, value object validation, and domain event emission using only in-memory Python objects. No database, no I/O, no mocks of infrastructure. These tests validate business invariants (e.g., "an NDA in state Countersigned cannot transition to Under Review," "a loan payment cannot exceed the outstanding balance"). Target: sub-second execution for the full tier.

**Tier 2 — Service layer tests** (`tests/unit/test_handlers.py`): Exercise command and event handlers using `FakeUnitOfWork` and `FakeRepository` implementations that store data in plain Python dictionaries. These tests verify use-case orchestration: correct handler routing, outbox event generation, and error handling — without touching PostgreSQL or Redis. This is the primary test tier by volume; most new feature tests are written here. Target: under 5 seconds for the full tier.

**Tier 3 — Integration tests** (`tests/integration/`): Verify ORM mappings, repository implementations against a real PostgreSQL instance (via docker-compose), and API entrypoint request/response contracts via `httpx.AsyncClient` with the real FastAPI app. These tests are intentionally thin — they confirm that the adapters layer correctly bridges the domain and infrastructure, not that business logic is correct (that is Tier 1 and 2's job). Target: under 30 seconds for the full tier.

The CI pipeline fails if any tier fails. Tier 1 and 2 run within the "Unit Tests" stage; Tier 3 runs within the "Integration Tests (docker-compose)" stage. Each app's `CLAUDE.md` documents which tier new tests for a given feature should target, with the default being Tier 2 (service layer with fakes).

### 6.3 Mandatory Runbook Index

Each data product has a documented runbook. The following runbooks are mandatory at Phase 0 launch:

| Runbook | Owner | Location | Contents |
|---|---|---|---|
| Atreides→Stillsuit Funding Handoff | Platform Team + Ops Lead | `docs/runbooks/funding_handoff.md` | Expected flow, breach escalation (Ops Lead paged at T+5min), known failure modes (Stillsuit timeout, Redpanda lag, PostgreSQL pool exhaustion), recovery procedure (manual loan activation with audit record), chaos test results |
| Corrino Covenant Breach Alert | Portfolio Analytics Team | `docs/runbooks/covenant_breach_alert.md` | Alert trigger thresholds, escalation path (PM paged immediately), false positive handling, manual override procedure |
| Stillsuit Payment Processing Failure | Operations Team | `docs/runbooks/payment_processing_failure.md` | Expected processing flow, failure detection (Grafana alert on error rate >1%), escalation path (Ops Lead paged at T+2min), manual reconciliation procedure |
| Foldspace Master Data API 5xx Surge | Platform Team | `docs/runbooks/mdm_api_5xx.md` | Expected traffic patterns, surge detection threshold (>5% 5xx rate over 5 minutes), circuit breaker behavior, manual cache invalidation, PostgreSQL connection pool recovery |
| Dead-Letter Replay Procedure | Platform Team | `docs/runbooks/dead_letter_replay.md` | Executed when Redpanda consumer lag exceeds threshold or dead-letter queue events accumulate beyond the replay window |

Additional runbooks are required before each phase ships to staging (documented in each app's `CLAUDE.md`).

### 6.4 Data Product SLA Monitoring Dashboards

Beyond application-level Prometheus/Grafana dashboards (which monitor request latency, error rates, and queue depth), the following Grafana dashboards are required for data product observability:

| Dashboard | Data Source | Panels |
|---|---|---|
| Data Product Freshness | `ARRAKIS_CONSUMPTION.DATA_QUALITY` | Freshness lag per data product (current vs. SLA target); breach history (time series); worst-offender ranking |
| Data Product Quality Scores | `ARRAKIS_CONSUMPTION.DATA_QUALITY` | Quality score trend per product (30-day rolling); gate-failure rate; top failing checks |
| Volume Anomaly Tracker | `ARRAKIS_CONSUMPTION.DATA_QUALITY` | Record count vs. 30-day rolling average per product; anomaly alert history |
| Schema Drift Monitor | `ARRAKIS_CONSUMPTION.DATA_QUALITY` | Schema change events per RAW landing table; drift-frequency by app |
| Data Contract Status | DCA PostgreSQL (direct Grafana connection) | Active contracts by provider/consumer; expiring contracts (30-day lookahead); contract approval queue depth |

## 7. LLM Integration Layer Architecture

This section specifies how every Claude API call across the suite is brokered through a single shared service (Spice), how prompts are versioned and governed, how context windows are budgeted, how outputs are validated and reviewed, and how MCP tool invocations are governed and audited. The aim is a single point of cost tracking, observability, and safety enforcement for all AI-mediated work in the suite.

### Architecture: Shared LLM Service (Spice)

All Claude API calls across the suite route through a shared internal service named Spice — a FastAPI microservice that wraps the Anthropic API. Per-app direct Claude API calls are prohibited. Centralizing LLM calls provides:

- Centralized cost tracking and billing attribution by app/deal/user
- Rate limiting and queue management across the suite
- Unified prompt versioning and retrieval
- Centralized output logging (all prompts + completions stored in Snowflake for audit and prompt improvement)
- A single point for model version upgrades

#### Spice Service Resilience Profile

Every outbound call from Spice to the Anthropic API operates under the following resilience contract:

| Parameter | Value | Rationale |
|---|---|---|
| Connection timeout | 5 s | Detect network-level failures before blocking async workers. |
| Read timeout (non-streaming) | 120 s | Accommodates long-form generation (IC memos, DDQ responses) while bounding worst-case worker hold time. |
| Read timeout (streaming) | 30 s idle between chunks | Detects stalled streams without terminating healthy long generations. |
| Retry policy | 3 attempts, exponential backoff (1 s, 2 s, 4 s) with jitter, retry on 429/5xx only | Avoids retry storms during Anthropic rate-limit windows; jitter prevents thundering herd across concurrent Celery workers. |
| Rate-limit backoff | On 429 response, respect `Retry-After` header; if absent, back off 60 s before next attempt. | Aligns with Anthropic API contract. |
| Circuit breaker | Open after 5 consecutive failures within 120 s; half-open after 60 s. | Prevents cascading failure when Anthropic API is experiencing sustained outage. When open, Spice returns a structured error to the calling app immediately rather than queuing. |
| Per-app rate budget | Configurable per `app_id` in Spice's `rate_config` table. Default: 60 requests/min per app. Suite-wide ceiling: 200 requests/min (adjustable to Anthropic tier). | Prevents a single runaway app (e.g., a batch NDA extraction job in Gom Jabbar) from starving other apps of API capacity. |

Spice exposes a `/health/anthropic` endpoint that reports the circuit breaker state and current rate-limit headroom. This endpoint is consumed by the Foldspace Observatory for the LLM availability dimension (cross-reference: Section 5.4).

#### Input Guardrails — PII Detection

Before transmitting any prompt to the Anthropic API, Spice applies a PII detection scan to the assembled prompt (system prompt + retrieved context + user input). The scan targets the following sensitive data classes relevant to private credit:

- **Personal identifiers:** Social Security Numbers, passport numbers, dates of birth
- **Financial account data:** bank account numbers, routing numbers, wire instructions, SWIFT/BIC codes
- **LP identity data:** LP names, commitment amounts, and capital account balances when combined with identifying information
- **Personal contact data:** personal email addresses, personal phone numbers, home addresses

Detection uses a combination of regex patterns (for structured identifiers like SSN, account numbers) and a lightweight NER classifier (for unstructured personal names in financial context). When PII is detected:

1. **RESTRICTED-classified prompts** (IC deliberation, deal financials): PII is masked with typed placeholders (`[SSN_1]`, `[BANK_ACCT_1]`, `[LP_NAME_1]`). A reverse PII map is held in Spice's in-memory session context (never persisted to disk or Snowflake). After Claude generates the response, Spice unmasks placeholders in the output before returning to the calling app.
2. **CONFIDENTIAL-classified prompts:** PII scan runs in log-only mode — detections are recorded in the audit trail but not masked, because masking may degrade Claude's reasoning quality on financial documents. A weekly report of CONFIDENTIAL-prompt PII detections is generated for the compliance team.
3. **INTERNAL-classified prompts:** No PII scan (utility prompts contain no deal data by definition).

PII detection metrics (scan count, detection count by class, mask count) are published to the Foldspace Observatory as a sub-dimension of the LLM availability monitor.

#### Spice Observability Metrics

The Foldspace Observatory monitors Spice as a sixth dimension — LLM Service Health — computed from the AI Output Audit Trail records flowing through the standard Bronze→Silver→Gold pipeline. Metrics are aggregated hourly, decomposable by `app_id`, `task_type`, and `prompt_version`:

| Metric | Computation | Alert Threshold | Escalation |
|---|---|---|---|
| P95 total latency | 95th percentile of `latency_ms` per `task_type` | > 30 s for extraction tasks; > 120 s for long-form drafting | PagerDuty to on-call engineer |
| Structural failure rate | % of requests where Pydantic validation failed on first attempt (before retry) | > 5% over 1-hour window | Slack alert to #spice-ops |
| Discard rate | % of outputs where human reviewer discarded the draft entirely | > 20% over 24-hour window per `task_type` | Slack alert to #spice-ops + prompt owner |
| Token cost per request | Mean (`input_tokens` × input price + `output_tokens` × output price) per `app_id` | > 2× the 30-day rolling average for any `app_id` | Slack alert to #spice-ops — potential prompt regression or runaway context |
| API error rate | % of requests returning non-2xx from Anthropic API (after retries) | > 2% over 1-hour window | PagerDuty — potential Anthropic outage |
| Circuit breaker open events | Count of transitions to OPEN state | Any occurrence | PagerDuty immediate |

Metrics are materialized as a Snowflake Dynamic Table in `ARRAKIS_CONSUMPTION.DATA_QUALITY` alongside the existing Observatory dimensions. The Observatory dashboard (Section 6.4) adds an "LLM Service Health" panel showing these metrics with time-series trend lines.

#### Model Version Upgrade Procedure

When Anthropic releases a new Claude model version, Spice follows a four-step upgrade process:

1. **Pin and evaluate.** Spice's `model` column in the `prompt_library` table pins every prompt to a specific Claude model version string (e.g., `claude-sonnet-4-20250514`). No prompt is updated to a new model version until the evaluation step completes. The team runs the full prompt evaluation suite (one representative query per `task_type`, evaluated against the quality criteria) against the new model version using a dedicated Spice staging endpoint that routes to the candidate model.
2. **Staged rollout by task criticality.** Prompts are organized into three upgrade tiers:
   - **Tier 1** (INTERNAL-classified, utility prompts): Upgraded first. Monitored for 48 hours against the Observatory's LLM Service Health metrics.
   - **Tier 2** (CONFIDENTIAL-classified, deal financial prompts): Upgraded after Tier 1 passes. Monitored for 72 hours.
   - **Tier 3** (RESTRICTED-classified, IC deliberation and compliance prompts): Upgraded last. Monitored for 1 week. Requires explicit sign-off from the compliance team before upgrade.
3. **Rollback.** If any tier's quality metrics breach the alert thresholds during its monitoring window, the affected prompts are reverted to the previous model version by updating the `model` column in `prompt_library`. Rollback is a single-row update per prompt — no code deployment required.
4. **Deprecation.** The previous model version is maintained as a fallback in Spice's configuration for 90 days after the final tier completes its monitoring window, aligning with the blueprint's 90-day API deprecation policy (Section 3). After 90 days, the fallback entry is removed.

#### Prompt Caching Strategy

Spice leverages the Anthropic API's prompt caching feature for task types where the system prompt prefix exceeds 1,024 tokens and the expected request volume exceeds 20 requests per hour. Spice structures prompts to maximize cache efficiency:

1. **Cache-stable prefix ordering.** For every API call, Spice assembles the prompt in the following order: (a) system prompt (task instructions, output format, guardrail instructions), (b) shared reference context (e.g., standard covenant definitions, template clause libraries — content that is identical across requests of the same type), (c) deal-specific retrieved context, (d) user input. Segments (a) and (b) are marked as cacheable using the Anthropic `cache_control` parameter. Segments (c) and (d) vary per request and are not cached.
2. **Applicable workflows.** The following task types are identified as cache-eligible based on high volume and long shared prefixes:
   - Corrino: financial statement extraction (quarterly batch of 50+ companies)
   - Gom Jabbar: NDA metadata extraction (batch processing up to 50 NDAs)
   - Stillsuit: agent notice categorization (daily processing of incoming notices)
   - CHOAM: precedent library search (repeated queries against the same clause library context)
3. **Cost tracking.** Spice logs `cached_input_tokens` and `non_cached_input_tokens` separately in the AI Output Audit Trail (extending the existing `input_tokens` field) to enable precise cost attribution and cache hit rate monitoring. The Observatory tracks cache hit rate as a sub-metric of the LLM Service Health dimension, with a target of ≥ 70% for cache-eligible task types.

#### Spice Request Tracing

Every Spice request propagates the calling app's OpenTelemetry `trace_id` and creates child spans for each processing stage. The following spans are mandatory for every Spice request:

| Span Name | Description | Key Attributes |
|---|---|---|
| `spice.request` | Root span for the entire Spice request lifecycle. | `app_id`, `task_type`, `deal_id`, `prompt_version`, `model` |
| `spice.pii_scan` | Input guardrail PII detection. | `pii_detections_count`, `masked_count` |
| `spice.context_assembly` | Prompt assembly including RAG retrieval and context budget enforcement. | `input_tokens_system`, `input_tokens_context`, `input_tokens_user`, `chunks_retrieved`, `chunks_after_rerank` |
| `spice.anthropic_call` | The outbound HTTP call to the Anthropic API. | `model`, `input_tokens`, `output_tokens`, `stop_reason`, `cached_input_tokens` |
| `spice.validation` | Pydantic validation and failure disposition. | `validation_result`, `retry_count` |
| `spice.mcp_tool_call` | One span per MCP tool invocation within an agentic workflow. | `tool_name`, `params`, `duration_ms`, `error_code` (if failed) |

All spans carry the standard `trace_id`, `deal_id`, `app_id`, and `user_id` attributes, consistent with the structlog convention specified in Section 8 (CLAUDE.md Conventions). Spans are exported to Jaeger via the OpenTelemetry SDK already deployed across the suite. The `spice.request` span's total duration replaces the single `latency_ms` field in the AI Output Audit Trail, providing decomposed latency visibility without altering the trail's schema.

#### Spice Request Envelope — Mandatory Caller Identity and Authorization Fields

Every Spice API request must include the following mandatory fields in the request envelope. Spice rejects any request missing a required field with HTTP 422.

```python
class SpiceRequestEnvelope(BaseModel):
    """Mandatory identity and context fields for every Spice API call."""
    # Caller identity (required)
    app_id: str                          # Calling application identifier (e.g., "reverend_mother")
    user_id: str                         # Authenticated user who initiated the action
    user_role: str                       # RBAC role of the originating user (e.g., "deal_team", "ic_member")
    deal_id: str | None                  # Deal context, if applicable (None for non-deal prompts)
    # Request context (required)
    prompt_id: str                       # prompt_library.prompt_id being invoked
    prompt_version: int                  # Explicit version from prompt_library
    task_type: str                       # Task classification (e.g., "ic_memo_draft", "ddq_generation")
    idempotency_key: str                 # UUID — prevents duplicate Claude API calls for the same user action
    # Authorization context (required)
    requested_tools: list[str] | None    # MCP tool names this session may invoke; each entry is validated against th
    data_classification_ceiling: str     # Highest classification tier this request may access (RESTRICTED, CONFIDENT
```

Spice performs the following authorization checks before forwarding to the Anthropic API: (1) `app_id` is in the set of registered Spice consumers, (2) `user_role` is authorized for the specified `task_type` per the RBAC model in Section 10, (3) each entry in `requested_tools` passes the `allowed_callers` check from the MCP tool governance metadata, and (4) `data_classification_ceiling` is compatible with the user's role-based data access scope. All fields are persisted in the AI output audit trail record alongside the prompt and completion.

#### Spice Per-Caller Authorization Policy — Prompt and Tool Access Control

Spice maintains a prompt authorization matrix stored in its PostgreSQL configuration schema (`spice_config.prompt_authorization`). This matrix maps each `prompt_id` to the set of `app_id` values permitted to invoke it.

```python
class PromptAuthorizationRule(BaseModel):
    """Stored in spice_config.prompt_authorization table."""
    prompt_id: str                       # FK to prompt_library.prompt_id
    allowed_app_ids: list[str]           # Apps permitted to invoke this prompt
    allowed_task_types: list[str]        # Task types this prompt may serve
    max_data_classification: str         # Highest classification tier this prompt may access
    requires_deal_context: bool          # If True, request must include a non-null deal_id
```

Spice enforces the following rules on every request, evaluated after the identity validation and before the PII detection: (1) `request.app_id` must appear in the prompt's `allowed_app_ids` list; violation returns HTTP 403 with error code `SPICE_UNAUTHORIZED_CALLER`. (2) `request.task_type` must appear in the prompt's `allowed_task_types`; violation returns HTTP 403 with error code `SPICE_UNAUTHORIZED_TASK`. (3) `request.data_classification_ceiling` must be ≥ the prompt's `max_data_classification`; violation returns HTTP 403 with error code `SPICE_CLASSIFICATION_MISMATCH`. (4) If `requires_deal_context` is True and `request.deal_id` is null, Spice returns HTTP 422 with error code `SPICE_MISSING_DEAL_CONTEXT`. All authorization decisions (granted and denied) are logged to the AI output audit trail with the full request envelope for compliance review. The authorization matrix is maintained as code in `shared/llm_service/config/prompt_auth.py` and deployed through the standard CI/CD pipeline.

### Prompt Versioning, Management, and Governance

Prompts are stored as versioned records in PostgreSQL (`prompt_library` table: `prompt_id`, `app_id`, `task_type`, `version`, `content`, `model`, `max_tokens`, `classification`, `created_at`, `deprecated_at`). Prompts are also version-controlled in the Git monorepo under `shared/llm_service/prompts/`.

**Prompt library governance** — extending data contract discipline to AI outputs:

- Every prompt is classified using the same four-tier data classification scheme as data products: RESTRICTED (prompts that handle IC deliberation data), CONFIDENTIAL (prompts that handle deal financials), INTERNAL (utility prompts), PUBLIC (none)
- Prompt changes require a PR and deploy like any code change. No live prompt editing in production
- Prompts that generate outputs consumed by other apps (e.g., Reverend Mother's triage memo focus areas consumed by Sardaukar) are registered as data contracts in the DCA — the prompt's structured output schema is the contract's schema
- AI output audit trails (prompt + completion + validation result + human edit delta) are published to `ARRAKIS_RAW.APP_EVENTS` and flow through the standard Bronze→Silver→Gold pipeline with RESTRICTED classification

### Context Window Management

Long-form drafting uses hierarchical decomposition: section-by-section drafting, RAG over deal documents via pgvector, and structured negotiation context for CHOAM redlining.

#### Context Window Budget Allocation

Spice enforces a token budget framework for every Claude API call. The budget is expressed as a fraction of the model's maximum context length and is configurable per `task_type` in the `prompt_library` table:

| Budget Segment | Default Allocation | Notes |
|---|---|---|
| System prompt | ≤ 10% | Includes role instructions, output format specification, and guardrail instructions. Shared across all tasks of the same type. |
| Retrieved context (RAG) | ≤ 60% | Deal documents, precedent clauses, financial data, DD findings retrieved via pgvector or MCP tools. Spice truncates retrieved context to fit this budget using a relevance-ranked strategy: chunks are included in descending relevance score order until the budget is exhausted. |
| Conversation / task-specific input | ≤ 15% | User instructions, negotiation history, prior draft sections for continuation tasks. |
| Output reservation | ≥ 15% | Reserved for Claude's response. `max_tokens` in the API call is set to this value. For long-form drafting tasks (IC memos, term sheets), this reservation may be increased to 30% by reducing the RAG allocation proportionally. |

Budget allocations are logged in the AI Output Audit Trail as `{input_tokens_system, input_tokens_context, input_tokens_user, max_tokens_reserved}` to enable cost attribution and context efficiency analysis. When a task's assembled prompt exceeds the total budget, Spice returns a structured error rather than silently truncating — the calling app must reduce its context request or use hierarchical decomposition (section-by-section drafting).

#### RAG Retrieval Quality Baseline

The `search_deal_documents` retrieval pipeline (backing the MCP tool of the same name and all Spice RAG operations) operates under the following specification:

**Chunking strategy.** Documents are split using recursive structural decomposition: first by section headings (credit agreement articles, memo sections, financial statement line-item groups), then by paragraph if a section exceeds the chunk size limit. Chunk size target: 512 tokens with 64-token overlap at chunk boundaries. Legal documents (credit agreements, NDAs, intercreditor agreements) use clause-level splitting aligned to numbered provision boundaries rather than fixed token counts.

**Contextual retrieval.** Each chunk is augmented with a metadata preamble containing: source document title, document type (credit agreement, financial statement, DD report, memo, NDA), `deal_id`, and a one-sentence summary of the chunk's position within the parent document. The preamble is prepended to the chunk text before embedding generation, following the contextual retrieval pattern, and stored alongside the embedding vector in pgvector.

**Retrieval and reranking.** The default retrieval pipeline is a two-stage process: (1) pgvector cosine similarity retrieves the top 3× candidate chunks (default: 30 candidates for k=10), (2) a lightweight cross-encoder reranker scores each candidate against the query and returns the top k chunks. The reranker runs as a Python function within Spice (using a small cross-encoder model) and adds < 200 ms to retrieval latency.

**Retrieval evaluation.** A quarterly retrieval quality review samples 50 recent production queries per task type, annotates retrieved chunks as relevant or not relevant, and computes context precision. Target: ≥ 80% context precision (at least 8 of 10 retrieved chunks are relevant to the query). Results are logged in the Observatory and inform chunking/embedding tuning decisions.

### Output Validation and Human-in-the-Loop

All LLM-generated outputs follow a mandatory human-review gate before any consequential action: Claude generates → Pydantic validation → "AI Draft — Pending Review" banner → human review/edit/approve → original + edits + final all persisted to Snowflake.

#### LLM Output Failure Taxonomy

Spice classifies every Claude response into one of the following disposition categories before returning to the calling app:

| Failure Mode | Detection Method | Disposition | Max Retries |
|---|---|---|---|
| Empty response | Response body contains no content blocks or all blocks are empty. | Automatic retry with same prompt. | 2 |
| Malformatted output | Response is not parseable as JSON when structured output was requested, OR Pydantic validation raises `ValidationError` on a non-nullable required field. | Automatic retry with an appended instruction: "Your previous response was malformatted. Return valid JSON matching the schema." | 2 |
| Truncated output | `stop_reason` is `max_tokens` rather than `end_turn`. | If task supports chunked generation (e.g., section-by-section memo drafting), Spice issues a continuation request. Otherwise, automatic retry with `max_tokens` increased by 50% up to the model's context limit. | 1 |
| Schema-valid but semantically degenerate | Pydantic validation passes but output fails a task-specific sanity check (e.g., extracted NDA metadata contains zero non-null fields, or covenant narrative is shorter than 50 characters). Sanity checks are registered per `task_type` in the `prompt_library` table as a `min_quality_spec` JSON column. | Route to human review with an "AI Draft — Low Confidence" banner (distinct from the standard "AI Draft — Pending Review" banner). | 0 |
| API error (non-retryable) | 400-class errors excluding 429. | Return structured error to calling app. Log to audit trail with `validation_result = 'api_error'`. | 0 |

All retry attempts are logged to the AI Output Audit Trail with `validation_result` reflecting the failure mode and retry sequence number. The final disposition (success after retry, escalation to human, or hard failure) is recorded in the `validation_result` field. Retry token costs are attributed to the originating `app_id` and `deal_id`.

#### LLM Output Quality Evaluation Criteria

Every Claude-generated output is evaluated against the following criteria. Criteria are scored during the human review step and recorded in the AI Output Audit Trail alongside the existing fields:

| Criterion | Scoring | Applicable Task Types | Method |
|---|---|---|---|
| Structural completeness | Binary (pass/fail) | All tasks | Pydantic validation (already specified). Automated — no human input needed. |
| Factual consistency | Binary (consistent / inconsistent) | Memo drafting, DD responses, covenant narratives, co-lender DD | Human reviewer flags any statement not supported by the retrieved context or deal data. Recorded as `factual_consistency` field in the audit trail. |
| Edit severity | Categorical (none / minor / major / rewrite) | All tasks | Derived from `human_edit_delta`: none = no edits; minor = < 10% of tokens changed; major = 10–50% changed; rewrite = > 50% changed or output discarded. |
| Usefulness | Binary (used / discarded) | All tasks | Whether the human reviewer accepted the output (with or without edits) or discarded it entirely. |

**Quality trend monitoring.** The Foldspace Observatory computes the following LLM quality metrics daily, broken down by `app_id` and `task_type`, from the AI Output Audit Trail flowing through the standard Bronze→Silver→Gold pipeline:

- Structural pass rate (target: ≥ 98%)
- Factual consistency rate (target: ≥ 90% — to be calibrated after first 90 days of production data)
- Edit severity distribution (alert if "rewrite" rate exceeds 15% over a 7-day rolling window)
- Discard rate (alert if > 20% of outputs are discarded over a 7-day rolling window)

These metrics are published to the `ARRAKIS_CONSUMPTION.DATA_QUALITY` schema as an LLM quality dimension and surfaced on the Observatory dashboard alongside the existing five data observability dimensions.

#### HITL Review Workflow State Machine and Override Audit Trail

Every LLM-generated output subject to HITL review follows a defined state machine. The review state is persisted in the calling app's PostgreSQL database alongside the draft record, and the terminal state is included in the AI output audit trail written to `ARRAKIS_RAW.APP_EVENTS`.

**HITL Review States:**

```
AI_DRAFT → VALIDATION_PASSED → PENDING_REVIEW → IN_REVIEW → APPROVED | REJECTED |
REVISION_REQUESTED | ESCALATED
```

**State transition rules:** (1) `AI_DRAFT → VALIDATION_PASSED` is automatic upon Pydantic validation success; validation failure routes to the disposition policy. (2) `VALIDATION_PASSED → PENDING_REVIEW` is automatic upon UI render with the "AI Draft — Pending Review" banner. (3) `PENDING_REVIEW → IN_REVIEW` records the `reviewer_id` and `review_started_at` timestamp. (4) Terminal transitions record `reviewer_id`, `decision`, `decision_at`, and `rationale` (free text, required for `REJECTED` and `ESCALATED`). (5) `REVISION_REQUESTED` returns the output to Spice for re-generation with reviewer annotations attached as context, creating a new `AI_DRAFT` with a `parent_draft_id` link.

**Override Audit Record:**

When a reviewer edits the AI-generated output before approval, the system persists an override audit record:

```python
class HITLOverrideRecord(BaseModel):
    draft_id: str
    reviewer_id: str
    review_state: str                    # Terminal state (APPROVED, REJECTED, ESCALATED)
    sections_modified: list[str]         # Section identifiers the reviewer changed
    edit_magnitude: str                  # MINOR (cosmetic), MODERATE (substantive rewording), MAJOR (structural change or fa
    rationale: str | None                # Required for MAJOR edits and all REJECTED/ESCALATED decisions
    reviewed_at: datetime
```

Override records are included in the AI output audit trail and aggregated by the Foldspace Observatory (Section 5.4) for drift detection. An escalation threshold is defined per task type: if the MAJOR override rate for a given `prompt_id` exceeds 20% over a rolling 30-day window, the Observatory emits a `data-quality.sla-breach` event and the prompt is flagged for platform team review.

### Snowflake Cortex vs. Direct Claude API

| Use Case | Preferred Tool | Reasoning |
|---|---|---|
| IC memo drafting, DDQ generation, term sheet drafting | Direct Claude API via Spice | Long-form reasoning; context window management via RAG |
| Borrower financial statement extraction (Corrino) | Snowflake Cortex | Structured extraction close to data; avoids egress |
| Portfolio commentary summarization (LP reporting) | Snowflake Cortex | Shallow NLP; data already in Snowflake |
| Semantic search across deal documents | Direct Claude API + pgvector | Requires embedding model + vector search |
| Covenant headroom narrative alerts (Corrino) | Snowflake Cortex | Template-style generation from structured data |
| Agent notice categorization (Stillsuit) | Direct Claude API via Spice | Complex document understanding; non-standard formats |
| Compliance certificate extraction (Corrino) | Direct Claude API via Spice | Complex unstructured PDFs requiring deep reasoning |
| Co-lender DD response drafting (Heighliner) | Direct Claude API via Spice | Multi-document reasoning with RAG |
| NDA metadata extraction (Gom Jabbar) | Direct Claude API via Spice | Legal document understanding requiring precision |

### MCP Server Design — foldspace-mcp (Expanded)

**Tool catalog** (closing feature gaps identified in the gap analysis):

```python
# Deal and entity context
get_deal_context(deal_id: str) -> DealContextSchema
get_company_profile(company_id: str) -> CompanyProfileSchema
get_sponsor_profile(sponsor_id: str) -> SponsorProfileSchema
get_facility_terms(facility_id: str) -> FacilityTermsSchema

# Financial and modeling data
get_financial_metrics(company_id: str, period: str) -> FinancialMetricsSchema
get_model_outputs(deal_id: str, model_version: str = "latest") -> ModelOutputSchema
get_data_book(deal_id: str, version: str = "latest") -> DataBookSchema

# Diligence data
get_dd_findings(deal_id: str, status: str = "all") -> DDFindingsSchema
get_dd_queue(deal_id: str) -> DDQueueSchema

# Portfolio and loan data
get_portfolio_position(facility_id: str) -> PortfolioPositionSchema
get_covenant_status(facility_id: str) -> CovenantStatusSchema

# Document search
search_deal_documents(deal_id: str, query: str, k: int = 10) -> list[DocumentChunkSchema]
get_document(document_id: str) -> DocumentMetadataSchema

# IC and terms history
get_ic_decisions(deal_id: str) -> list[ICDecisionSchema]
get_negotiation_history(deal_id: str) -> NegotiationHistorySchema

# Co-lender DD support (closes Heighliner feature gap)
get_colender_dd_context(deal_id: str, question_id: str) -> ColenderDDContextSchema

# Precedent library queries (closes CHOAM feature gap vs. Harvey Vault)
search_precedent_library(clause_type: str, query: str, k: int = 5) -> list[PrecedentSchema]

# Covenant narrative generation (closes Corrino feature gap)
get_covenant_narrative_context(facility_id: str, period: str) -> CovenantNarrativeContextSchema

# Financial document extraction (closes Corrino feature gap vs. 73 Extract)
extract_financial_data(document_id: str, extraction_template: str) -> FinancialExtractionSchema

# NDA metadata extraction (closes Gom Jabbar feature gap vs. Ironclad)
extract_nda_metadata(document_id: str) -> NDAMetadataSchema

# Agent notice processing (closes Stillsuit feature gap vs. WSO)
extract_agent_notice(document_id: str) -> AgentNoticeSchema
```

All tools are read-only. Write operations go exclusively through the Foldspace REST API, not through MCP.

#### MCP Tool Error Contract

All `foldspace-mcp` tools return a standardized error schema on failure, enabling Claude to reason about failure disposition during agentic workflows:

```python
class MCPToolError(BaseModel):
    error_code: Literal[
        "NOT_FOUND",          # Requested entity does not exist
        "ACCESS_DENIED",      # Caller lacks permission for this entity
        "INVALID_PARAMS",     # Parameter validation failed (detail explains)
        "UPSTREAM_TIMEOUT",   # Snowflake or PostgreSQL query exceeded timeout
        "UPSTREAM_ERROR",     # Non-timeout upstream failure
        "RATE_LIMITED",       # Tool-level rate limit exceeded
    ]
    detail: str               # Human-readable explanation
    retryable: bool           # True for UPSTREAM_TIMEOUT, RATE_LIMITED; False otherwise
    tool_name: str            # The tool that failed
    params: dict              # The parameters that were passed (for debugging)
```

**Tool-level behavior on failure:**

| Error Code | Claude's Expected Behavior | Spice Logging |
|---|---|---|
| NOT_FOUND | Do not retry. Inform the user that the requested entity was not found. | Log at INFO — expected operational case. |
| ACCESS_DENIED | Do not retry. Inform the user that access is restricted. | Log at WARN — potential RBAC misconfiguration. |
| INVALID_PARAMS | Do not retry. Re-examine parameter values and correct if possible. | Log at WARN — potential prompt or planning defect. |
| UPSTREAM_TIMEOUT | Retry once after 5 s. If retry fails, inform the user of temporary unavailability. | Log at ERROR — feeds Observatory alerting. |
| UPSTREAM_ERROR | Do not retry. Report failure to the user. | Log at ERROR. |
| RATE_LIMITED | Wait and retry after the period specified in `detail`. | Log at WARN — feeds Observatory rate monitoring. |

All MCP tool errors are included in the AI Output Audit Trail as `tool_errors: list[MCPToolError]` appended to the existing audit schema, enabling post-hoc analysis of tool failure patterns.

#### MCP Tool Governance Metadata

Each `foldspace-mcp` tool definition carries the following governance metadata in addition to its typed Python signature:

| Metadata Field | Type | Description |
|---|---|---|
| `tool_version` | SemVer string | Current version of the tool definition (e.g., `1.0.0`). Incremented on signature change, return schema change, or data source change. |
| `allowed_callers` | list[str] | Exhaustive list of `app_ids` permitted to invoke this tool via Spice. Spice enforces this list at request time; calls from unlisted apps are rejected with HTTP 403. |
| `return_data_classification` | enum | The highest data classification tier (RESTRICTED, CONFIDENTIAL, INTERNAL, PUBLIC) present in the tool's return payload. Governs downstream masking and audit requirements. |
| `certification_status` | enum | One of CERTIFIED, PROVISIONAL, DEPRECATED. Tools in DEPRECATED status emit a structured warning in the response envelope and are removed after 90 days (aligning with the API Deprecation Policy). |
| `certified_by` | str | Identity of the engineer or reviewer who last certified the tool. |
| `certified_at` | datetime (UTC) | Timestamp of last certification event. |
| `depends_on_prompt_ids` | list[str] | Prompt library `prompt_id` values that this tool's invocation context typically requires, enabling cascade validation when prompts change. |

Example metadata for a high-sensitivity tool:

```python
# Tool metadata (stored alongside tool definition in foldspace_mcp/tools/)
TOOL_META_GET_DD_FINDINGS = ToolGovernanceMeta(
    tool_version="1.0.0",
    allowed_callers=["reverend_mother", "sardaukar", "heighliner"],
    return_data_classification="CONFIDENTIAL",
    certification_status="CERTIFIED",
    certified_by="platform-team-lead",
    certified_at="2026-03-15T14:00:00Z",
    depends_on_prompt_ids=["dd_summary_v3", "dd_triage_v2"],
)
```

Spice validates `allowed_callers` on every MCP tool invocation. The `ToolGovernanceMeta` Pydantic model is defined in `shared/schemas/mcp_governance.py` and registered in the DCA as part of the `foldspace-mcp` service contract.

### AI Output Audit Trail Integration

Every Claude-generated output is logged to `ARRAKIS_RAW.APP_EVENTS` with the schema: `{app_id, task_type, prompt_version, model, input_tokens, output_tokens, latency_ms, deal_id, output_classification, validation_result, human_edit_delta_available}`. These records flow through the standard data product pipeline (Bronze→Silver→Gold) and are registered in the DCA as a data product consumed by the data catalog for lineage tracking and the Observatory for quality monitoring.

#### Step-Level MCP Tool Invocation Lineage

The `foldspace-mcp` server instruments every tool invocation as a child span under the parent Spice OTel trace. Each tool call emits a structured `ToolInvocationRecord` that is appended to an ordered list within the session's audit trail record before it is written to `ARRAKIS_RAW.APP_EVENTS`.

```python
class ToolInvocationRecord(BaseModel):
    """Captured per MCP tool call within a single Claude session."""
    sequence_number: int                     # 1-indexed order of invocation within the session
    tool_name: str                           # e.g., "get_deal_context"
    tool_version: str                        # From tool governance metadata
    parameters: dict                         # Sanitized input parameters (PII-redacted)
    return_data_classification: str          # From governance metadata
    latency_ms: int                          # Wall-clock time for the tool call
    result_status: str                       # SUCCESS | ERROR | TIMEOUT (per error schema)
    result_row_count: int | None             # Number of records returned, if applicable
    otel_span_id: str                        # OpenTelemetry span ID for correlation with Jaeger
```

The AI output audit trail schema in `ARRAKIS_RAW.APP_EVENTS` is extended with a `tool_invocations` column (VARIANT type in Snowflake) containing the ordered array of `ToolInvocationRecord` entries. This enables Snowflake SQL queries such as: "For audit record X, which MCP tools were called, in what order, accessing what classification tiers?" — a query pattern required for regulatory audit reconstruction and prompt effectiveness analysis.

## 8. CLAUDE.md Conventions

This section specifies the conventions encoded in the root `CLAUDE.md` and per-app `CLAUDE.md` files that guide Claude Code Agent Teams during AI-assisted development. These conventions ensure that AI-generated code respects the architectural boundaries, governance rules, and operational requirements established elsewhere in the blueprint.

### Root CLAUDE.md

The root `CLAUDE.md` is the single most important file for Claude Code productivity across the entire project. It must contain:

1. **Project map:** One-paragraph summary of each app, its role in the lifecycle, and its position in the build sequence — so Claude always has orientation context.

2. **Foldspace API reference:** Concise endpoint descriptions, authentication patterns, and the canonical entity schemas (Deal, Company, Facility etc.) — this prevents Claude from inventing API shapes that don't match the actual contract.

3. **Integration patterns:** The three primary patterns (Snowflake Stream, Redpanda event, Foldspace REST API) with a decision guide for which to use when — prevents ad hoc point-to-point integrations appearing in generated code.

4. **Coding conventions:** ruff for linting, pytest for tests, structlog for logging (with required fields: `deal_id`, `app_id`, `trace_id`), Pydantic v2 for all request/response schemas, no direct Snowflake connections from app code (always via Foldspace client or Snowflake Python connector only in Foldspace itself). See also the detailed conventions below: validation layering, abstraction mechanisms, domain model typing, and exception taxonomy.

   **Validation layering convention.** All validation across Arrakis applications follows a three-tier placement model:

   *Tier 1 — Syntactic validation (entrypoint/adapter layer):* Enforced by Pydantic v2 models on all FastAPI request handlers and Redpanda event consumer deserializers. Covers field presence, type coercion, permitted value ranges, and structural well-formedness. Invalid requests are rejected before reaching the service layer. Pydantic models for event consumption must set `model_config = ConfigDict(extra="ignore")` to tolerate schema evolution (Tolerant Reader). Claude Code must define a Pydantic request model for every endpoint and consumer handler.

   *Tier 2 — Semantic validation (service layer):* Enforced as precondition checks at the top of each service function — e.g., "does the referenced deal exist?", "is this user authorized for this deal?", "has this idempotency key already been processed?" Semantic preconditions raise domain-specific exceptions (see exception taxonomy convention) and must execute within the Unit of Work context so they share the same transactional view as the business operation.

   *Tier 3 — Pragmatic validation (domain model):* Enforced by aggregate invariants and entity business rules — e.g., "a facility's commitment amount cannot exceed the facility size", "an IC vote cannot be cast after session close." These rules live inside domain model methods and raise domain exceptions. Claude Code must never place business-rule validation in the entrypoint or adapter layer.

   **Abstraction mechanism convention.** Internal abstract interfaces (repository ports, unit of work contracts, connector base types, service ports) must be defined as `typing.Protocol` subclasses rather than `abc.ABC` subclasses. This enables structural subtyping — implementations satisfy the interface by providing the required methods without inheriting from a shared base class — which simplifies testing (fakes need no inheritance), avoids metaclass conflicts, and aligns with mypy and pyright static analysis. Exception: use `abc.ABC` only when the abstraction requires runtime `isinstance()` checking or provides shared concrete methods via inheritance (e.g., a `BaseConnector` that supplies shared retry logic). When ABC is chosen for this reason, document the rationale in a docstring on the class. Claude Code must define new internal interfaces as Protocol by default.

   **Domain model typing convention.** Each application must distinguish three model roles in its codebase and use the appropriate Python construct for each:

   *Value Objects* — immutable domain concepts defined entirely by their attributes (e.g., `Money`, `DateRange`, `ClassificationTier`, `FacilityTerms`). Implemented as `@dataclass(frozen=True)` with `__eq__` derived from all fields. Use `__post_init__` for invariant enforcement (e.g., `Money` must have non-negative amount). Value objects must never carry a database primary key.

   *Entities* — domain objects with identity that persists across attribute changes (e.g., `Deal`, `Facility`, `NDAWorkflowState`). Implemented as standard classes or mutable `@dataclass` with equality based on identity (`id` field), not attribute values. Entity methods enforce aggregate-level business rules (Tier 3 validation).

   *DTOs (Data Transfer Objects)* — Pydantic `BaseModel` subclasses used exclusively at system boundaries: FastAPI request/response schemas, Spice request/response models, MCP tool return schemas, Redpanda event consumer models. DTOs must not contain business logic. Conversion between DTOs and domain objects occurs in the service layer or adapter layer, never in the domain layer.

   Claude Code must place value objects and entities in the `domain/` package and DTOs in the `adapters/` or `entrypoints/` package. Domain model classes must never import from Pydantic; Pydantic models must never enforce business rules.

   **Exception taxonomy convention.** Every Arrakis application must define its exceptions using a shared base hierarchy from the `shared/` package:

   *`ArrakisError`* — base for all application exceptions. Carries `error_code: str`, `message: str`, and optional `context: dict` for structured logging.

   *`DomainValidationError(ArrakisError)`* — syntactic or semantic precondition failure. Raised in the service layer when a precondition check fails (e.g., referenced entity not found, unauthorized access, business-rule precondition unmet). Maps to HTTP 400/404/403/422 depending on subclass. FastAPI exception handlers translate subclasses to the standardized error response envelope.

   *`ConflictError(ArrakisError)`* — domain-level invariant violation or optimistic concurrency failure. Raised inside aggregate methods or by the UoW on version mismatch. Maps to HTTP 409.

   *`IdempotentDuplicateError(ArrakisError)`* — the operation has already been performed. The handler returns the original result without re-execution. Maps to HTTP 200 (not an error to the caller). Logged at INFO level.

   *`UpstreamError(ArrakisError)`* — failure in an external dependency (Anthropic API, external connector, Foldspace API). Carries `upstream_service: str` and `upstream_status: int`. Maps to HTTP 502/503.

   All exceptions must be logged with structlog using the mandatory fields (`deal_id`, `app_id`, `trace_id`) plus the exception's `error_code`. Claude Code must use this hierarchy rather than raising bare `HTTPException` or generic `ValueError` / `RuntimeError` from service or domain code. Entrypoint-layer exception handlers in each FastAPI app translate `ArrakisError` subclasses to HTTP responses; unhandled exceptions return 500 with a correlation `trace_id` only (no internal details).

5. **LLM service conventions:** Always use Spice client, never instantiate `anthropic.Anthropic()` directly in app code, always reference a named prompt by `(app_id, task_type)`, always validate Claude output against the relevant Pydantic schema before any downstream action.

6. **Security rules:** Never log `deal_id` + financial figures in the same log line, never store Snowflake credentials in code, all secrets via AWS Secrets Manager.

7. **Data contract registration requirement.** Every new inter-app data exchange must register a contract in the DCA before shipping. The PR template includes a checkbox: "If this PR introduces a new cross-app data dependency, a DCA contract has been created and approved: [contract_id]". Claude Code must check for this in generated PRs.

8. **Data classification annotation requirement.** Every new Snowflake table must carry classification metadata at creation. The schemachange migration template includes a mandatory `COMMENT ON COLUMN` block specifying the classification tier for every column. Claude Code must generate these comments when creating new tables.

9. **Quality gate convention.** Every app's test suite must include at least one Great Expectations validation suite against its Snowflake landing schema (`tests/quality/`). Claude Code must generate a GE suite when creating a new data product.

10. **Runbook requirement.** Every high-consequence workflow (any workflow that touches financial data, modifies master data, or triggers cross-app events) must have a runbook in `docs/runbooks/` before it ships to staging. Claude Code should flag PRs that add high-consequence workflows without a corresponding runbook.

Each app-level `CLAUDE.md` inherits the root conventions and adds: the app's domain model, its Redpanda topic subscriptions and publications, its specific Snowflake schemas it reads from and writes to, its data product definitions and historization strategies, and any app-specific coding patterns.

---

## 9. Infrastructure and Deployment

This section specifies the cloud platform, secrets handling, container strategy, deployment baselines (resource tiers, security contexts, NetworkPolicies, PDBs, HPAs, graceful shutdown, rolling updates), the CI/CD pipeline, and the monitoring and observability stack that runs the suite in production.

### Cloud Provider

The firm runs Snowflake. The recommendation is AWS unless the firm has an existing Azure or GCP footprint. If AWS: EKS for container orchestration, RDS for PostgreSQL, ElastiCache for Redis, MSK (or self-managed Redpanda on EC2) for the event bus, S3 for document storage, and Secrets Manager for credential management. The Snowflake–AWS PrivateLink connection keeps all data traffic off the public internet. If Azure: AKS, Azure Database for PostgreSQL Flexible Server, Azure Cache for Redis, Azure Blob Storage.

#### Secrets Integration Pattern

Arrakis uses the External Secrets Operator (ESO) to synchronize credentials from AWS Secrets Manager into native Kubernetes Secret resources. The ESO is deployed cluster-wide during Phase 0 as part of the infrastructure Terraform/Helm provisioning.

**Configuration:**

A single `ClusterSecretStore` resource configures the ESO to authenticate against AWS Secrets Manager using IAM Roles for Service Accounts (IRSA). Per-namespace `ExternalSecret` resources define the mapping from AWS Secrets Manager paths to Kubernetes Secret keys. The `refreshInterval` for all `ExternalSecrets` is set to `1h` (secrets are not frequently rotated; hourly sync balances freshness with API cost).

**Secret naming convention** in AWS Secrets Manager:

```
arrakis/{environment}/{service}/{secret-name}
```

Examples: `arrakis/prod/foldspace/postgresql-credentials`, `arrakis/prod/spice/anthropic-api-key`, `arrakis/prod/connectors/pitchbook-api-key`.

**Consumption in Pods:** Application containers consume secrets exclusively via environment variables sourced from the ESO-managed Kubernetes Secret. No secret values may appear in Helm values files, ConfigMaps, or container image layers. The `arrakis-base` Helm chart templates reference `ExternalSecret`-managed Secrets by convention, and the CI/CD pipeline validates that no Helm values file contains keys matching the pattern `*password*`, `*secret*`, `*api_key*`, or `*token*` in plaintext.

### Container Strategy

Kubernetes (EKS/AKS). Each application is containerized as a Docker image. Helm charts per application standardize deployment. The `foldspace-mcp` server and the Spice LLM service run as shared cluster-wide deployments. Redpanda is deployed using the Redpanda Helm operator.

#### Resource Tier Classification

Every Arrakis deployment must declare Kubernetes resource requests and limits in its Helm values file. The `arrakis-base` Helm chart enforces non-empty resource declarations at template rendering time. Following the Predictable Demands pattern, memory requests must equal memory limits (Guaranteed QoS for memory), and CPU requests must be set but CPU limits should be omitted to avoid CPU throttling under burst load.

All deployments are classified into one of four resource tiers:

| Tier | CPU Request | Memory Request = Limit | Representative Deployments |
|---|---|---|---|
| Platform-Critical | 2 cpu | 4 Gi | Foldspace core, Kong, Spice |
| Workflow-Standard | 500m | 1 Gi | Thumper, Gom Jabbar, Gurney, Sardaukar, Mentat, Reverend Mother, Landsraad, CHOAM, Heighliner, Atreides, Stillsuit, Corrino, Melange |
| Governance-Service | 500m | 1 Gi | Observatory, DCA, foldspace-mcp |
| Infrastructure | Per upstream Helm chart defaults | Per upstream Helm chart defaults | Redpanda (Redpanda operator), OpenMetadata, Elasticsearch |

Tier assignments are initial baselines. Teams must profile actual consumption during Phase 0 staging load tests and adjust values before production deployment. The Vertical Pod Autoscaler (VPA) should be deployed in recommendation-only mode (`updateMode: "Off"`) to produce right-sizing guidance without disrupting running workloads.

#### Graceful Shutdown Contract

Every Arrakis FastAPI container must implement SIGTERM handling that performs an orderly drain before exit. The `arrakis-base` Helm chart sets `terminationGracePeriodSeconds` per service category:

| Service Category | Grace Period | Drain Behavior |
|---|---|---|
| Standard API services (all 13 domain apps, Foldspace, DCA, Observatory) | 45 seconds | Stop accepting new HTTP requests (uvicorn shutdown). Complete all in-flight HTTP request handlers. Flush any pending outbox relay batch to Redpanda. Close PostgreSQL and Redis connection pools. |
| Spice LLM service | 90 seconds | Stop accepting new completion requests. Allow in-flight Claude API calls to complete (Claude responses can take 30–60s for long-context drafts). Write incomplete request records to the AI output audit trail with `status = 'INTERRUPTED'`. Close connections. |
| Celery workers (Reverend Mother, CHOAM, Mentat drafting queues) | 120 seconds | Send SIGTERM to Celery worker process, which triggers warm shutdown: finish the currently executing task, do not pick up new tasks, re-queue any prefetched tasks back to Redis. If the task does not complete within 110 seconds, Celery's `--soft-time-limit` triggers a `SoftTimeLimitExceeded` exception, which the task handler catches to persist partial state. |
| foldspace-mcp | 30 seconds | Stateless read-only service; default drain is sufficient. |

Additionally, the `arrakis-base` Helm chart must configure a `preStop` lifecycle hook on all API service containers that sends an HTTP request to a local `/shutdown` endpoint, giving the FastAPI application an explicit signal independent of SIGTERM. This ensures graceful shutdown even when the container runtime's signal delivery is delayed.

#### Pod Security Context Baseline

The `arrakis-base` Helm chart must enforce the following security context on all Arrakis application containers. These settings apply to all 14 services (Foldspace + 13 domain apps), Spice, foldspace-mcp, Observatory, and DCA. Infrastructure components (Redpanda, OpenMetadata, Elasticsearch) follow their upstream Helm chart security configurations.

Container-level `securityContext` (applied to every container in the Pod spec):

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 1000
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop: ["ALL"]
```

Since `readOnlyRootFilesystem: true` prevents writes to the container filesystem, all services that require a temporary writable directory (e.g., for uvicorn's worker PID files or structlog's fallback buffer) must mount an `emptyDir` volume at `/tmp`.

**Namespace-level enforcement.** All Arrakis application namespaces must carry Pod Security Standards labels enforcing the restricted profile at the enforce level:

```yaml
metadata:
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/warn: restricted
```

This ensures that any Pod definition that violates the restricted standard is rejected at admission time, preventing accidental deployment of privileged containers.

#### NetworkPolicy Segmentation

Every Arrakis application namespace must include a default-deny ingress NetworkPolicy and a set of explicit allow rules that mirror the intended communication topology defined in the blueprint.

**Default-deny policy** (applied to every application namespace):

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector: {}
  policyTypes:
    - Ingress
```

**Explicit allow rules** (maintained per-namespace in each app's Helm chart):

| Source | Destination | Port | Rationale |
|---|---|---|---|
| Kong Pods | All domain app Pods | 8000 (FastAPI) | All API traffic must transit through Kong per Section 1 |
| Kong Pods | Foldspace core Pods | 8000 | Foldspace API access |
| Foldspace core Pods | Spice Pods | 8001 | LLM service calls from apps that invoke drafting via Foldspace |
| Spice Pods | foldspace-mcp Pods | 8002 | MCP tool invocations during agentic workflows |
| All domain app Pods | Redpanda broker Pods | 9092 | Outbox relay event publishing and consumer group subscriptions |
| Prometheus Pods | All app Pods | 9090 (/metrics) | Metrics scraping |
| All app Pods | DNS (kube-dns) | 53 (TCP/UDP) | Service discovery |

Domain app Pods must not be able to reach other domain app Pods directly. This enforces the blueprint's architectural invariant that all inter-app communication flows through either Kong (synchronous) or Redpanda (asynchronous).

The CNI plugin (AWS VPC CNI on EKS, Azure CNI on AKS) must support NetworkPolicy enforcement. For EKS, this requires enabling the VPC CNI Network Policy feature or deploying Calico as a network policy engine.

#### PodDisruptionBudget Baseline

Every Arrakis Deployment with `replicas >= 2` must have a corresponding PodDisruptionBudget. The `arrakis-base` Helm chart includes a PDB template that is automatically rendered when the replica count exceeds one.

| Service Category | PDB Setting | Effect |
|---|---|---|
| Platform-Critical (Kong, Foldspace core, Spice) | `minAvailable: 1` | At least one Pod must remain available during voluntary evictions. Prevents total service loss during node drain. |
| Financial-Critical (Stillsuit, Atreides) | `minAvailable: 1` | Protects the funding handoff and payment processing paths. Complements the circuit-breaker defined in Section 3. |
| Workflow-Standard (all other domain apps) | `maxUnavailable: 1` | Allows at most one Pod to be evicted at a time. Permits node drains to proceed while maintaining partial availability. |
| Governance-Service (Observatory, DCA, foldspace-mcp) | `maxUnavailable: 1` | Same as Workflow-Standard. Observatory and DCA are not on the real-time request path and tolerate brief partial outages. |

Services running with `replicas: 1` (acceptable during early build phases for non-critical services) do not receive a PDB, as a PDB with `minAvailable: 1` on a single-replica Deployment would block node drains indefinitely. These services accept voluntary eviction downtime until they scale to two or more replicas.

#### Horizontal Pod Autoscaler Policy

Arrakis services eligible for autoscaling must define an HPA in their Helm chart. HPA is enabled only after resource requests are baselined and validated in staging load tests. The `arrakis-base` Helm chart includes an HPA template that is conditionally rendered when `autoscaling.enabled: true` is set in the app's values file.

| Service Category | Metric | Target | Min Replicas | Max Replicas |
|---|---|---|---|---|
| Platform-Critical (Foldspace core, Kong) | CPU utilization | 60% of CPU request | 2 | 6 |
| LLM Service (Spice) | CPU utilization | 50% of CPU request | 2 | 4 |
| Workflow-Standard (13 domain apps) | CPU utilization | 70% of CPU request | 1 | 3 |
| Governance-Service (Observatory, DCA, foldspace-mcp) | Not autoscaled | — | 1 | 1 |

CPU utilization is selected as the primary metric because it has a direct linear correlation with request throughput in FastAPI services — increasing replicas distributes requests and reduces per-Pod CPU consumption. Memory is excluded as a scaling metric because FastAPI services do not exhibit memory consumption that decreases with additional replicas.

**Scale-down stabilization:** The HPA `behavior.scaleDown.stabilizationWindowSeconds` is set to `300` (5 minutes) for all services. This prevents rapid scale-down during brief load dips. Scale-up stabilization remains at the Kubernetes default (0 seconds) to ensure rapid response to load increases.

**Prerequisite:** HPA is not enabled until resource requests are baselined and the Kubernetes Metrics Server (or Prometheus Adapter for custom metrics) is deployed and validated. During Phase 0 and initial build phases, services run at fixed replica counts.

### New Infrastructure Components

**Foldspace Observatory:** Deployed as a standalone FastAPI container in the Kubernetes cluster. Depends on: Snowflake (reads `DATA_QUALITY` schema), Redpanda (emits alert events), Grafana (dashboard rendering). Resource allocation: 2 vCPU, 4GB RAM (lightweight — primarily runs scheduled queries and alert evaluations).

**Data Catalog (OpenMetadata):** Deployed as a containerized service in Kubernetes. Depends on: its own PostgreSQL database (separate schema in the shared RDS instance), Elasticsearch (for search indexing), Snowflake metadata connector. Resource allocation: 4 vCPU, 8GB RAM, 100GB EBS for Elasticsearch.

**DCA Service:** Deployed as a standalone FastAPI container. Depends on: its own PostgreSQL schema (`foldspace_dca` in the shared RDS instance), Redpanda (emits contract approval events), Kong (API gateway integration for contract-based routing checks). Resource allocation: 2 vCPU, 4GB RAM.

**API Catalog:** Co-deployed with the Foldspace backend (same FastAPI application, separate router). Backed by the Foldspace PostgreSQL schema. No additional infrastructure required.

### CI/CD

GitHub Actions (or GitLab CI) with per-application path-filtered pipelines. Pipeline stages: lint → unit tests → integration tests → data quality gate (blocking) → schemachange migration (blocking) → build Docker image → push to ECR → deploy to staging via Helm upgrade. Prompt versioning included in the Spice service's CI pipeline.

#### Deployment Strategy Baseline

The `arrakis-base` Helm chart must define an explicit rolling update strategy in the Deployment spec. Per-service overrides are permitted in individual app Helm values files, but the baseline applies to all services unless overridden.

| Parameter | Baseline Value | Rationale |
|---|---|---|
| `strategy.type` | `RollingUpdate` | Zero-downtime deployments are required for all Arrakis services. |
| `strategy.rollingUpdate.maxSurge` | 1 | Limit surge to one additional Pod to control resource consumption in a shared cluster. |
| `strategy.rollingUpdate.maxUnavailable` | 0 | No Pod may be terminated until its replacement passes readiness checks. Eliminates request-drop risk during deployment — critical for the Atreides→Stillsuit funding endpoint. |
| `spec.minReadySeconds` | 10 | Pod must report ready for at least 10 seconds before the rollout proceeds, catching fast-fail startup crashes that pass the initial readiness probe but fail shortly after. |
| `spec.revisionHistoryLimit` | 5 | Retain five previous ReplicaSets to enable rapid `kubectl rollout undo` if a deployment introduces a regression. |

**Stillsuit override:** Stillsuit's Helm values file must set `maxSurge: 0` and `maxUnavailable: 0` with `replicas >= 2`, forcing the rollout to use a one-at-a-time replacement strategy where each new Pod must pass readiness before the next old Pod is removed. This provides the strongest availability guarantee for the payment processing service, complementing the circuit-breaker and idempotency key protections defined in Section 3.

### Monitoring and Observability

- **Application metrics:** Prometheus + Grafana. Each FastAPI app exposes `/metrics` via prometheus-fastapi-instrumentator
- **Distributed tracing:** OpenTelemetry SDK → Jaeger (OSS)
- **Log aggregation:** structlog → Loki → Grafana. Every log line carries `deal_id`, `app_id`, `user_id`, `trace_id`
- **LLM observability:** Spice logs every prompt + completion to `ARRAKIS_RAW.APP_EVENTS`
- **Data product observability:** Foldspace Observatory dashboards in Grafana (Section 6.4)
- **Snowflake query monitoring:** built-in Query History + Resource Monitors
- **Event bus monitoring:** Redpanda Console (OSS)
- **Uptime and alerting:** PagerDuty/OpsGenie integrations from Grafana alert rules

## 10. Governance, Access Control, and RBAC

This section defines the role-based access control model for the suite — the user roles, the corresponding Snowflake roles and Row Access Policies, the classification-enforcement architecture that connects catalog metadata to column masking, the DCA-driven Snowflake permission provisioning, and the tenant isolation guarantees for Heighliner and Landsraad.

### RBAC Model

Governance requires clear data classifications and labels, unified data security, identity providers, and trust boundaries. In Arrakis, this is implemented at two layers: Snowflake RBAC for the data platform, and application-level JWT claims for the API layer.

Four primary user roles:

| Role | Scope | Snowflake Role | App Access |
|---|---|---|---|
| Deal Team | Full access to all deals assigned to them; no access to other deal teams' live deals | `ARRAKIS_DEAL_TEAM` — SELECT on all consumption schemas, scoped by deal via Row Access Policies | Thumper, Gurney, Gom Jabbar, Sardaukar, Mentat, Reverend Mother, CHOAM, Atreides, Stillsuit, Corrino (own deals only), Heighliner (deal team view) |
| IC Member | Read-only access to memos and supporting materials for deals they are permissioned to review; can annotate and vote in Landsraad; cannot see other IC members' votes until session closes | `ARRAKIS_IC_MEMBER` — SELECT on `IC_AUDIT`, `MDM.DEALS`, `CURATED.FINANCIAL_DATA`, `CURATED.DD_ACTIVITY` scoped by deal via Row Access Policy | Landsraad only (for deal review); read-only access to Mentat data book and Reverend Mother memos via Landsraad |
| Co-Lender | Access only to the co-lender syndication workspace for specific deals they have been invited to; no access to firm's internal deal data | `ARRAKIS_COLENDER` — SELECT on `CONSUMPTION.SYNDICATION` for permissioned deals only | Heighliner (co-lender portal) only |
| Borrower | Access only to their own facility's post-close agency portal; no access to deal economics, IC materials, or other borrowers | `ARRAKIS_BORROWER` — SELECT on `CONSUMPTION.PORTFOLIO_ANALYTICS` for their `facility_id` only | Heighliner (borrower agency portal) only |

### Snowflake Row Access Policies

```sql
CREATE OR REPLACE ROW ACCESS POLICY deal_team_scope AS (deal_id VARCHAR)
RETURNS BOOLEAN ->
    CURRENT_ROLE() IN ('ARRAKIS_ADMIN') OR
    EXISTS (
        SELECT 1 FROM ARRAKIS_CONSUMPTION.MDM.DEAL_TEAM_ASSIGNMENTS
        WHERE deal_id = deal_id
          AND team_member_email = CURRENT_USER()
          AND is_active = TRUE
    );
```

Applied to every table in CURATED and CONSUMPTION schemas carrying a `deal_id` column.

### Classification-Enforcement Architecture

The classification metadata flow from catalog to column masking policy:

1. Data engineer creates a new Snowflake table via schemachange migration, including `COMMENT ON COLUMN` with classification tier
2. OpenMetadata's Snowflake connector extracts column comments nightly and applies classification tags
3. The DCA's contract approval workflow checks: if the data product contains columns tagged RESTRICTED or CONFIDENTIAL, the contract's `sensitive_classifications_present` field must list them
4. A nightly Snowflake stored procedure reads classification tags from the catalog API and applies/updates column masking policies:

```sql
-- Example: mask facility margin for Borrower and Co-Lender roles
CREATE OR REPLACE MASKING POLICY confidential_financial_mask AS (val NUMBER)
RETURNS NUMBER ->
    CASE
        WHEN CURRENT_ROLE() IN ('ARRAKIS_ADMIN', 'ARRAKIS_DEAL_TEAM') THEN val
        ELSE NULL
    END;
```

### DCA Integration with Snowflake Permissions

When a data contract is approved in the DCA, the DCA emits a `data-contract.approved` event. The Foldspace permission provisioning service subscribes to this event and executes:

```sql
GRANT SELECT ON ARRAKIS_CONSUMPTION.{schema}.{table} TO ROLE {consumer_app_role};
```

No Snowflake SELECT permissions are granted outside this automated workflow. This ensures that data access is always backed by a registered, approved contract.

### Heighliner Tenant Isolation (Hardened)

Heighliner serves two completely separate user populations with hard tenant isolation:

**Co-lender view (pre-close):** Co-lender users are provisioned when a deal team member explicitly invites them. The invitation creates a `co_lender_access_grant` record scoped to `{deal_id, colender_org_id, expiry_date}`. All API endpoints in Heighliner's co-lender namespace check this grant table. Co-lenders see only: co-lender IC memo (separate from full IC memo), data book, financial model exports, syndication allocation tracker, and amendment/consent voting interface. Co-lenders never see: full IC memo, internal credit committee deliberations, economics above their tranche (RESTRICTED classification — masked at Snowflake column level), or other co-lenders' commitment details.

**Borrower view (post-close):** Borrower users are provisioned by the operations team after funding. Borrower users see only: their facility's compliance certificate schedule, uploaded financial statement confirmations, amendment/waiver notices, and quarterly lender call materials. They have zero visibility into other borrowers, deal economics, or portfolio-level data.

**Physical separation:** Separate FastAPI routers with separate JWT claim scopes (`heighliner:colender` vs. `heighliner:borrower`). Middleware validates that the user's `facility_id` or `deal_id` JWT claims match the requested resource on every API call.

### Landsraad — IC-Specific Controls

IC vote integrity is the highest-sensitivity access control requirement:

- **Vote confidentiality:** Individual votes stored with `revealed_at` timestamp. Withheld until chair closes deliberation. Only `ic:view-votes` permission scope sees vote details post-close.
- **Pre-vote sealing:** Pre-meeting votes are stored but invisible to all other members (including chair) until session opens and chair explicitly reveals pre-votes.
- **Immutability:** PostgreSQL trigger prevents UPDATE and DELETE on `ic_events`. Amendments require new records with `amendment_type = 'SUPERSEDES'`.
- **Audit export:** On session close, complete JSON payload written to `ARRAKIS_CONSUMPTION.IC_AUDIT` via INSERT only. 90-day Time Travel provides immutability backstop.

---

## 11. Build Sequencing

This section establishes the phased build sequence for the suite, prioritizing foundation before applications, deal-lifecycle order over arbitrary parallelism, and analytics and post-close last. The sequencing reflects both hard technical dependencies and the firm's need to deliver value early.

### Guiding Principle

Start small: generate excitement, and start with one or a few domains whose teams have bought in to the concept. Show success first, before scaling up. Sequencing priority: (1) foundation before apps, (2) the deal lifecycle flow in order, (3) analytics and post-close last.

### Build Phases

#### Phase 0 — Foldspace Foundation (Weeks 1–8)

This is the only true hard dependency: everything else builds on it.

- Snowflake databases and schemas (RAW/CURATED/CONSUMPTION) provisioned via Terraform + schemachange — including all 15 RAW landing schemas and expanded CURATED/CONSUMPTION schemas
- PostgreSQL cluster on RDS, Redis on ElastiCache, Redpanda cluster deployed
- Kong API gateway configured with base auth plugin
- Foldspace Master Data API (FastAPI): endpoints for Deal, Company, Sponsor, Contact CRUD with deduplication logic
- foldspace-mcp MCP server with read-only tools for all master data entities
- Document registry API and S3 integration
- Base connector framework (`BaseConnector` class) with the Cap IQ and PitchBook connectors
- Shared authentication service (JWT issuance, validation middleware, Snowflake Row Access Policy bootstrapping)
- Spice LLM service stub (wires up Claude API, prompt library table, basic logging to Snowflake)
- Monorepo structure, CI/CD pipelines with data quality gate stages for all shared services, base Helm charts
- DCA stub: FastAPI service deployed with PostgreSQL schema. Contract CRUD endpoints operational. Approval workflow manual (platform team approves via API). Permission provisioning automated for Snowflake GRANT execution on contract approval.
- Enterprise metamodel database: PostgreSQL schema populated with initial metamodel entities (Data Domain, Data Product, Application, Owner). Linked to the first data products (Foldspace MDM entities).
- Data catalog deployment: OpenMetadata instance deployed on Kubernetes. Snowflake metadata connector configured. Initial scan of RAW/CURATED/CONSUMPTION schemas completed. Classification tags applied to Phase 0 tables.
- Foldspace Observatory stub: FastAPI service deployed. Freshness monitoring for all Phase 0 data products. Volume anomaly detection. Grafana dashboards for Data Product Freshness and Volume Anomaly Tracker.
- API Catalog: Populated with all Phase 0 Foldspace API endpoints and external connector registrations.
- Mandatory Phase 0 runbooks: Foldspace Master Data API 5xx surge runbook written and reviewed.

#### Phase 1 — Deal Origination and Relationship Intelligence (Weeks 9–18)

Delivers immediate day-one value: the team can start managing deal pipeline and contacts.

- **Thumper:** Deal pipeline tracking, origination activity log, Desert Power BDC ingestion
- **Gurney:** CRM with contact profiles, organization records, interaction history; bidirectional integration with Thumper via Foldspace; PitchBook enrichment connector; zero-entry activity capture (Outlook connector)
- **Gom Jabbar:** NDA workflow; dynamic approval routing; NDA metadata auto-extraction; obligation tracking; template library with conditional clauses
- Data contracts registered in DCA for all Phase 1 inter-app exchanges
- Classification metadata applied to all Phase 1 Snowflake tables
- Great Expectations suites for all Phase 1 data products
- Phase 1 runbooks written

#### Phase 2 — Live Deal Workflow: Triage through IC (Weeks 19–36)

The core deal execution engine. These apps have hard sequential dependencies.

- **Reverend Mother (triage stage first** — memo drafting with Claude is the flagship use case)
- **Sardaukar** (DD queue management, seeded by Reverend Mother triage memo output; Q&A with AI-suggested similar questions; document auto-classification; timeline/Gantt view; milestone tracking)
- **Mentat** (financial model ingestion and versioning; data book creation; Snowflake integration; Monte Carlo simulation; sensitivity analysis; dependency inspector)
- **Reverend Mother (IC stage** — full memo drafting, co-lender memo, integration with Sardaukar DD findings and Mentat data book)
- **Landsraad** (IC platform — the most complex build; budget 5–6 weeks; WebSocket layer, annotation system, vote management, immutable audit trail; pre-vote capability; automated minutes generation; engagement analytics; smart agendas)
- Data contracts, classification, quality gates, and runbooks for all Phase 2 inter-app exchanges

#### Phase 3 — Terms, Closing, and Syndication (Weeks 37–50)

- **CHOAM:** Term sheet and credit agreement workflow; precedent library (knowledge vault); obligation management; citation grounding
- **Heighliner** (pre-close syndication workspace; co-lender portal; allocation tracker; real joint book-running; amendment voting; financial reporting calendar; AI-assisted co-lender DD responses)
- **Atreides:** Closing checklist and funds flow; KYC/AML integration; maker-checker approval; the Atreides → Stillsuit handoff is the most critical integration test — allocate two-week hardening sprint with chaos engineering test suite
- Data contracts, classification, quality gates, and runbooks for all Phase 3 exchanges

#### Phase 4 — Post-Close Operations and Portfolio (Weeks 51–68)

- **Stillsuit:** Loan administration ledger; the Snowflake Stream configuration feeding Corrino; agent notice processing; cash/position reconciliation; multi-currency accounting; income recognition; hypothetical trade analysis
- **Corrino:** Portfolio monitoring and covenant tracking; Streamlit-in-Snowflake dashboards; Snowflake Dynamic Tables for covenant recalculation; automated financial data collection; AI-powered document extraction; compliance certificate parser; AutoFill reporting; predictive risk modeling
- **Melange:** Valuation workflows; Corrino data consumption; LP reporting outputs; valuation workflow management; roll-forward automation; comparable selection tools; multi-level approval governance; IPEV/ASC 820 compliance; credit-specific valuation module
- **Heighliner** (post-close agency portal; borrower reporting)
- Data contracts, classification, quality gates, and runbooks for all Phase 4 exchanges

#### Phase 5 — Governance Maturity (Weeks 69–78)

This phase brings the governance infrastructure from operational to fully mature:

- **Full DCA automation:** Contract approval workflow includes automated schema compatibility checking (new schema version validated against existing consumers' expectations before approval). Self-service contract creation portal for data engineers.
- **Column lineage completion:** OpenMetadata lineage extraction expanded to column-level for all CONSUMPTION layer attributes feeding `LP_REPORTING` and regulatory outputs. Lineage graph queryable via the data catalog UI.
- **Self-service data access provisioning:** Domain users can discover data products in the catalog, request access via DCA self-service portal, and receive automated Snowflake role provisioning upon contract approval — without platform team intervention for INTERNAL classification data.
- **Observatory maturity:** All five observability dimensions fully operational. Quality score SLAs defined and enforced for every data product. Freshness and volume anomaly detection tuned (false positive rate <5%).
- **Classification audit:** Full audit of all Snowflake columns for classification completeness. Any unclassified column in CURATED or CONSUMPTION schemas is flagged and resolved.
- **Runbook completeness:** Every data product has a runbook. Runbook review cadence established (quarterly).

### Repo Structure

```
arrakis/
├── CLAUDE.md                           # Root CLAUDE.md: repo map, build commands,
│                                       # coding conventions, Foldspace API docs,
│                                       # data contract, classification, quality gate,
│                                       # and runbook requirements
├── .github/workflows/                  # Per-app CI/CD pipelines (path-filtered)
├── infrastructure/
│   ├── terraform/                      # VPC, RDS, ElastiCache, EKS, S3, ECR
│   ├── helm/                           # Per-app Helm charts + arrakis-base chart
│   └── snowflake/                      # schemachange migrations (DDL versioning)
├── shared/
│   ├── foldspace_client/               # Python client library for Foldspace API
│   │   └── CLAUDE.md                   # How to use Foldspace client in app code
│   ├── llm_service/                    # Spice: shared Claude API wrapper
│   │   ├── prompts/                    # Versioned prompt files by app/task
│   │   └── CLAUDE.md                   # Prompt writing conventions, validation patterns
│   ├── auth/                           # JWT middleware, RBAC decorators
│   ├── connectors/                     # BaseConnector + all external data connectors
│   ├── schemas/                        # Pydantic schemas for all inter-app data contracts
│   │   └── CLAUDE.md                   # How to version and extend schemas
│   └── mcp/
│       └── foldspace_mcp/              # MCP server (foldspace-mcp)
│           └── CLAUDE.md               # MCP tool catalog, how to add new tools
├── foldspace/                          # App 0: Foldspace backend
│   ├── CLAUDE.md                       # Foldspace domain model, API contract guide
│   ├── api/                            # FastAPI application
│   ├── dca/                            # Data Contract Application service
│   ├── api_catalog/                    # API Catalog router
│   ├── observatory/                    # Foldspace Observatory service
│   ├── migrations/                     # schemachange SQL migrations
│   ├── quality/                        # Great Expectations suites
│   └── tests/
├── catalog/                            # OpenMetadata deployment configuration
│   ├── docker-compose.yml              # Local catalog development
│   ├── helm/                           # Kubernetes deployment
│   └── connectors/                     # Custom metadata connectors
├── apps/
│   ├── thumper/
│   │   ├── CLAUDE.md                   # Thumper domain: pipeline stages, BDC ingestion,
│   │   │                               # data products, historization, classification
│   │   ├── backend/                    # FastAPI
│   │   ├── frontend/                   # React
│   │   ├── quality/                    # Great Expectations suites
│   │   └── tests/
│   ├── gom_jabbar/
│   ├── gurney/
│   ├── sardaukar/
│   ├── mentat/
│   ├── reverend_mother/
│   ├── landsraad/
│   ├── choam/
│   ├── heighliner/
│   ├── atreides/
│   ├── stillsuit/
│   ├── corrino/
│   └── melange/
└── docs/
    ├── architecture/                   # ADRs (Architecture Decision Records)
    ├── data_contracts/                 # Avro schemas, Pydantic models, versioning log
    ├── runbooks/                       # Operational runbooks per app
    ├── metamodel/                      # Enterprise metamodel documentation
    └── classification/                 # Data classification scheme documentation
```

### MCP Server Configuration for Development

```json
{
  "mcpServers": {
    "foldspace": {
      "command": "python",
      "args": ["-m", "arrakis.mcp.foldspace_mcp"],
      "env": {
        "FOLDSPACE_API_URL": "http://localhost:8000",
        "SNOWFLAKE_ACCOUNT": "${SNOWFLAKE_ACCOUNT}",
        "AUTH_TOKEN": "${DEV_SERVICE_TOKEN}"
      }
    },
    "snowflake": {
      "command": "uvx",
      "args": ["mcp-server-snowflake"],
      "env": { "SNOWFLAKE_ACCOUNT": "${SNOWFLAKE_ACCOUNT}" }
    },
    "postgres": {
      "command": "uvx",
      "args": ["mcp-server-postgres", "${LOCAL_POSTGRES_URL}"]
    }
  }
}
```

### A Note on Phasing and Architectural Risk

The hardest architectural decision in this entire build is the Atreides → Stillsuit funding handoff (Phase 3→4 boundary). This is the moment where software interacts with actual capital deployment. The blueprint hardens this with idempotency key enforcement, formal circuit-breaker pattern, versioned request schema with backward-compatibility guarantee, and a mandatory chaos engineering test suite (Section 3). Budget a dedicated two-week hardening sprint at the Phase 3/4 boundary specifically for this handoff.

The second highest-risk integration is Snowflake Dynamic Table latency for Corrino covenant calculations. Dynamic Tables have a configurable refresh lag (minimum ~1 minute). For daily covenant tracking this is entirely adequate. If the firm needs intraday alerting, the Dynamic Table pattern should be supplemented with a Snowflake Task on a tight schedule or real-time covenant events published to Redpanda by Stillsuit directly.

The third highest risk is the Foldspace MDM API availability. This is the single most consumed API in the suite — all 13 apps depend on it for entity resolution. A 5xx surge cascades across the entire platform. The MDM API runbook (Phase 0 mandatory) and the Observatory's freshness monitoring on MDM data products are the primary mitigations. The Redis cache in front of the MDM API provides a 15-minute read buffer during brief outages.

The overall architecture begins with a top-down decomposition of business concerns, uses business capabilities as a reference model, and builds one pipeline per application that takes the entire application state, copies it, and transforms data into user-friendly datasets. Foldspace is that shared substrate. Each app is a bounded domain. The Snowflake landing zone is the integration point. The Redpanda event bus decouples the workflows. The DCA governs every data exchange. The Observatory monitors every data product. The data catalog makes everything discoverable. Claude drafts; humans decide. Every decision is audited. Every entity has an owner. Every column has a classification. Every contract has an SLA. That is Arrakis.
