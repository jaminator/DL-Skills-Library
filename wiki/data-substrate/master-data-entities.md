---
title: Master Data Entities
category: data-substrate
tags: [data-product, governance, architecture]
sources:
  - arrakis_blueprint_v2_3.md
last_updated: 2026-05-13
---

# Master Data Entities

The Arrakis MDM system holds **seven golden-record entities**, each owned by a specific golden-source application, governed by Foldspace's Master Data API, and historized using **SCD Type 2** so any entity's state at any prior moment can be reconstructed. This is the backbone for audit, regulatory, and LP-reporting workloads where the question "what did we know about this borrower as of Q3 close?" must be answerable.

## The seven entities

| Entity | Golden Source App | Steward | Resolution | Historization |
| --- | --- | --- | --- | --- |
| **Deal** | A1 Thumper | Deal Team | Thumper creates the Deal record; all other apps reference by `deal_id` | SCD Type 2 |
| **Company** | A3 Gurney | Relationship Manager | Gurney deduplicates; enriched from PitchBook / CapIQ via Foldspace connectors | SCD Type 2 |
| **Sponsor** | A3 Gurney | Relationship Manager | Same as Company; Sponsor is a Company subtype with `is_sponsor` flag and `fund_name` | SCD Type 2 |
| **Borrower** | A3 Gurney (pre-close) → A11 Stillsuit (post-close) | Deal Team / Ops | Gurney creates; Stillsuit takes operational ownership post-funding | SCD Type 2 |
| **Facility** | A8 CHOAM (terms) → A11 Stillsuit (operations) | Deal Team / Ops | CHOAM defines; Stillsuit becomes authoritative post-close | SCD Type 2 |
| **Contact** | A3 Gurney | Relationship Manager | Gurney deduplicates against email / phone / organization | SCD Type 2 |
| **Document** | Foldspace Document Registry | Platform Team | All apps publish to Foldspace; document entity is centrally owned | SCD Type 2 |

## SCD Type 2 mechanics

Every update to a master entity record inserts a new row with `valid_from` / `valid_to` timestamps and an `is_current` flag. The previous version's `valid_to` is set to the new version's `valid_from`. Late-arriving updates set `valid_from` to the event's logical timestamp, not the ingestion timestamp — the SCD Type 2 mechanism inherently handles temporal corrections.

## Ownership transfer protocol

Two entities have **lifecycle ownership transitions**: Borrower and Facility. When Atreides completes the funding handoff (`funding.confirmed` event written and Stillsuit acknowledges via `POST /loans/activate`), the Foldspace Master Data API automatically transitions golden-source authority:

- **Facility:** CHOAM → Stillsuit
- **Borrower:** Gurney → Stillsuit (Gurney retains read access for ongoing enrichment)

Transfer preconditions are enforced by the MDM API: target record must be `is_current = TRUE`, the receiving app must have an active data contract for the entity, no unresolved MDM conflict may be open at transfer time. Transfers emit a `master-data.ownership-transferred` event for downstream apps to observe.

## Conflict resolution

| Entity | Conflict scenario | Tie-breaker | SLA |
| --- | --- | --- | --- |
| Borrower | Gurney and Stillsuit disagree post-funding (legal name, address, classification) | Stillsuit | 4 business hours |
| Facility | CHOAM and Stillsuit disagree post-close (economics or terms) | Stillsuit (CHOAM authoritative pre-close) | 4 business hours |
| Company / Sponsor | Conflicting enrichment data | Gurney | 8 business hours |
| Contact | Auto-merge vs. manual override conflict | Gurney with data steward review | 8 business hours |

Conflict events emit to `mdm.conflict-raised`; resolutions emit to `mdm.conflict-resolved`. Losing apps must reconcile their local PostgreSQL state within 30 minutes of the resolution event — the **downstream reconciliation contract**.

## Domain invariants enforced at write time

The Master Data API rejects writes that violate domain invariants with `422 Unprocessable Entity` before persisting any record or emitting any event. Every artifact in this library that produces a master-entity payload must respect the invariants:

**Deal.** `originating_app` must be `thumper`. `status` must be in `{pipeline, active, approved, closing, funded, declined, withdrawn}`. A Deal with status `funded` may not be created directly.

**Company / Sponsor.** `legal_entity_name` non-empty. `jurisdiction` must be a valid ISO 3166-1 alpha-2 code. Deduplication on `tax_id` or (`legal_entity_name`, `jurisdiction`) tuple.

**Borrower.** All Company invariants apply. `tax_id` mandatory once `deal.status` transitions to `active`. `kyc_aml_status` ∈ `{pending, cleared, flagged, expired}`.

**Facility.** `deal_id` must reference an existing Deal with `is_current = TRUE`. `facility_type` ∈ `{revolver, term_loan, delayed_draw, bridge}`. `commitment_amount` positive. `maturity_date` after the current date. May not be created unless parent Deal status is `approved` or later.

**Contact.** At least one of `email`, `phone`, `organization_id` non-null.

**Document.** `s3_key` must follow the versioned key pattern `{type}/{deal_id}/{version_id}/{timestamp}.{ext}`.

## Why this matters for the library

Any Pydantic schema in this library that names a master entity must use the same identifier shape (UUIDs for `deal_id`, `company_id`, `facility_id`) and the same enum values. This is not aspirational — it is the only way the schema lands cleanly in `<APP>_LAND` in the [[snowflake-medallion]] when the artifact graduates into Arrakis.

## Related Concepts

- [[snowflake-medallion]] — where the MDM golden records live
- [[foldspace-substrate]] — the Master Data API host
- [[application-directory]] — the apps that own the entities

## Sources

- `arrakis_blueprint_v2_3.md`, Section 1 — Master Data Entities and Governance Ownership
