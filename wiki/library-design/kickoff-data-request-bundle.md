---
title: Kick-Off Data Request Bundle (P3)
category: library-design
tags: [process, opportunity, application, schema]
sources:
  - deal_lifecycle_automation_051326_vJA.pdf
  - arrakis_blueprint_v2_3.md
  - "[Company] - Wells & Overland Kick-Off Data Requests (MM-DD-YY) vTemplate.docx"
last_updated: 2026-05-15
---

# Kick-Off Data Request Bundle (P3)

The second library build (push-2), and the first **upstream** deliverable: the Stage 2 / P3 Kick-Off Data Requests one-pager `dl-ddq-kickoff`. It is built to the [[library-artifact-bundle]] pattern and is the data feed for the [[posting-memo-automation|P4 posting-memo pair]] — P3 sends the ask, the returned data populates P4, the databook, and the model.

## Why P3 next

P3 is the natural predecessor to the validated P4 work: the kick-off ask is *what the lender sends out*, and its returned data is the upstream feed for everything in [[screening-templates]]. Automating it front-loads every downstream artifact and closes the kick-off DDQ pain point flagged in [[origination-and-screening]] (no item-lifecycle tracker; DDQ friction propagates into P4). It is a lightweight outbound one-pager with no heavy primary-materials pre-work, so it ships as a single skill without triggering the Stage-2 fragmentation watchpoint (which fires only when the heavy standardized-databook skill also lands).

## What the bundle built

| Artifact | Path | Role |
| --- | --- | --- |
| Skill | `skills/dl-ddq-kickoff/SKILL.md` | Orientation → period math → standard set + stock cuts → framework-grounded KPI block → populate. `ddq` domain (pre-existing in the registry — no CLAUDE.md edit). |
| Skill scripts (2) | `scripts/compute_periods.py`, `scripts/populate_kickoff.py` | A deterministic FYE-aware period engine and an in-place template populator that preserves the `NumberList1`/`Bullet2` styling and both footnotes. |
| Skill references (2) | `reference/kpi-frameworks.md`, `reference/population-mechanics.md` | The framework→request-archetype map + worked sector library; the content-dict and list-injection mechanics. |
| Prompt | `prompts/stage-2-screening/P3-kickoff-data-requests.md` | Cache-eligible system prefix + semantic XML inputs; carries the outbound redaction line because the artifact is borrower-facing. |
| Project instruction | `project-instructions/stage-2-screening.md` (amended) | P3 row added; the P3 outbound-classification exception and a compiled downstream-pre-seeding IK embed inlined. |
| Pydantic schema | `schemas/kickoff_data_request.py` | `KickoffDataRequest` — a superset of the script content dict with sector + per-KPI provenance for Arrakis lineage; `schema_version = 1`; HITL `PENDING_REVIEW`. |

## Construction notes

The bundle exercises the **degrees-of-freedom split** from `Skills_Best_Practices.md`: period math and population are low-freedom (scripted, deterministic), the borrower-specific KPI block is high-freedom (framework-grounded judgment with a worked sector library). It inherits the **D-2 watermark carve-out** from [[posting-memo-automation]] — the outbound `.docx` body carries no banner; the draft signal is the `vS` filename plus the `PENDING_REVIEW` state. The schema documents a no-drift **projection** to the script's content dict, cross-validated by execution.

## Validation outcome

Execution-based (the bundle ships scripts, unlike the inspection-only [[compliance-certificate-parser-pilot]]). All four artifact checks and three functional evaluations passed — HVAC roll-up, SaaS (compliance N/A, ARR KPI shift), and an industrials manufacturer on a non-calendar FYE (FYE-aware quarter labeling). See `docs/pilot-validation.md` → Push-2 Validation.

## Arrakis target

Graduates into the Foldspace screening application (the same app as the P4 pair, see [[application-directory]]): `KickoffDataRequest` is the Spice output validator and the `SCREENING_LAND` data product; `<sector_classification>`/`<system_date>` map to MCP tool calls; the watermark becomes the rendered review banner with `review_state = "PENDING_REVIEW"` in [[hitl-state-machine]].

## Related Concepts

- [[library-artifact-bundle]] — the construction pattern this build follows
- [[posting-memo-automation]] — the P4 pair this bundle feeds; source of the D-2 carve-out
- [[screening-templates]] — the P3–P4 cluster and the kick-off's upstream role
- [[screening-input-schema]] — the `data_request_periods` bucket this populates
- [[compliance-certificate-parser-pilot]] — the first (inspection-only) library build
- [[skill-naming-convention]] — the `dl-ddq-kickoff` naming rule
- [[restricted-content-discipline]] — the outbound redaction obligation this artifact carries

## Sources

- `deal_lifecycle_automation_051326_vJA.pdf`, Stage 2 P3 kick-off DDQ pain points
- `arrakis_blueprint_v2_3.md`, Foldspace screening application
- `[Company] - Wells & Overland Kick-Off Data Requests (MM-DD-YY) vTemplate.docx`, the populated template
