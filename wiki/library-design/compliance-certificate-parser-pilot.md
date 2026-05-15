---
title: Compliance Certificate Parser Pilot (P17)
category: library-design
tags: [pilot, opportunity, application, process]
sources:
  - deal_lifecycle_automation_051326_vJA.pdf
  - arrakis_blueprint_v2_3.md
last_updated: 2026-05-13
---

# Compliance Certificate Parser Pilot (P17)

The library's first end-to-end vertical slice. The pilot targets **P17 Portfolio Monitoring** in Stage 6 — Asset Management, building a complete artifact bundle (skill + prompt + project instruction + Pydantic schema) for the **compliance certificate parser** workflow. The pilot validates that the [[library-artifact-bundle]] construction pattern works on the extract-and-validate shape (see [[opportunity-shapes]]) and graduates cleanly into [[arrakis-overview]]'s A12 Corrino app.

## Why P17 was chosen

The deck recommends **P4 Posting Memo** as the pilot (see [[posting-memo-friction]]). The pilot built here is P17 instead, for five reasons:

- **Acuter governance gap.** Compliance-cert friction is a [[foundation-controls]] item — audit / regulatory exposure today. Closing it benefits the firm at any portfolio size, not contingent on the [[growth-gap]].
- **Cleaner shape.** Extract-and-validate is the most architecturally constrained of the three [[opportunity-shapes]] — the Pydantic schema does most of the lifting, so the pattern shows through unobstructed.
- **Bounded inputs.** Compliance certificate (5–10 pages) plus covenant excerpts (20–40 pages), optionally the prior period's cert. Smaller RAG envelope than a memo build.
- **High repetition.** Every facility produces a cert quarterly. The audit-error dividend scales with name count.
- **Reusable taxonomy.** The covenant-types and CFO-error-patterns reference files are durable institutional knowledge — reused by every downstream covenant-related skill (DDTL draw verification, amendment impact analysis, lender consent screening).

P4 remains the highest-yield single pain point and is the recommended **next** build — same construction pattern, generate-with-review shape.

## What the pilot built

| Artifact | Path | Role |
| --- | --- | --- |
| Skill (markdown) | `skills/dl-compcert-review/SKILL.md` | The procedural workflow: parse → locate definitions → recompute → compare → flag → assemble. Named under the `dl-<domain>-<action-or-subtype>` convention (domain `compcert`, action `review`), third-person description, ≤500 line body. |
| Skill references (2 files) | `skills/dl-compcert-review/reference/covenant-types.md`, `cfo-error-patterns.md` | The two durable institutional taxonomies that the skill consults — covenant types and their definitional patterns; recurring CFO arithmetic-error shapes. |
| Prompt | `prompts/stage-6-asset-management/P17-compliance-certificate-parser.md` | The cache-eligible system prefix + semantic XML inputs. Output Contract specifies the JSON schema inline; HITL watermark on the output template. |
| Project instruction | `project-instructions/stage-6-asset-management.md` | Stage-6 behavioral rules, deal-context slot, deliverable cadence, and four embedded wiki pages compiled inline so the artifact runs without filesystem access. |
| Pydantic schema | `schemas/compliance_certificate_validation.py` | `ComplianceCertificateValidation` — 11 outer fields, 12 inner `CovenantCalculation` fields. Snake_case, JSON-serializable primitives, `schema_version = 1`, HITL state defaulting to `PENDING_REVIEW`. |

## Validation outcome

The pilot passed all four self-validation checks documented in `docs/pilot-validation.md` (Phase 4):

1. **Prompt** — stable cache-eligible system prefix, semantic XML inputs, `[INSUFFICIENT DATA]` marker, `[DRAFT — HUMAN REVIEW REQUIRED]` watermark, quote-grounded retrieval discipline.
2. **Skill** — gerund-named `name`, third-person `description` (574/1024 chars), body 121/500 lines, references one level deep, no path leakage, anti-patterns section present.
3. **Project instruction** — header, deal-context slot, deliverables table, eight behavioral rules, versioning convention, four wiki pages embedded inline with compile-date markers. Runs without filesystem access.
4. **Pydantic schema** — parses cleanly; snake_case; JSON-serializable types; required-vs-optional explicit; `schema_version` declared; HITL state default; module docstring names phase, Arrakis target, landing tier.

No drift between the prompt's Output Contract and the schema.

## Arrakis target

The pilot graduates into **A12 Corrino** (see [[application-directory]]) in Phase 4 of the Arrakis build (weeks 51–68):

- The **Pydantic schema** lands as the output validator in the Spice prompt-library row for the `corrino.compliance_certificate_validation` task (see [[prompt-versioning-governance]]).
- The **stable system prefix** is the cache-eligible `content` field of that row.
- The **variable XML inputs** map to MCP tool calls — `get_facility_terms`, `extract_financial_data`, `get_document`. See [[mcp-tool-catalog]].
- The **HITL watermark** becomes Corrino's "AI Draft — Pending Review" banner; the `review_state = "PENDING_REVIEW"` field is the matching state in [[hitl-state-machine]].
- Structured output lands in `ARRAKIS_RAW.CORRINO_LAND.compliance_certificate_validations` in the [[snowflake-medallion]] without translation.
- The two skill reference files lift directly into the Corrino prompt-library as task-specific reference documents.

## Recommended next builds

In order of leverage (per [[ic-and-asset-mgmt-gaps]] and [[opportunity-register]]):

1. **P17 RCF / DDTL draw verification** — same extract-and-validate shape, smaller scope, closes the related "DDTL draws approved over email; no compliance verification tracked" pain point.
2. **P18 mark-to-market triage** — generate-with-review pattern, exercises the second of the three [[opportunity-shapes]].
3. **P4 posting memo draft** — the originally-recommended pilot. Generate-with-review with bounded upstream context. High-frequency phase.

Each follow-on reuses the [[library-artifact-bundle]] this pilot validated.

## Related Concepts

- [[library-artifact-bundle]] — the abstract pattern this pilot proves
- [[opportunity-shapes]] — extract-and-validate, the shape this pilot exercises
- [[closing-and-asset-management]] — Stage 6 detail (P17–P19)
- [[ic-and-asset-mgmt-gaps]] — the AM friction this pilot addresses
- [[portco-coverage-workbook]] — the standing workbook whose Covenant Input this pilot automates
- [[application-directory]] — A12 Corrino, the Arrakis target

## Sources

- `deal_lifecycle_automation_051326_vJA.pdf`, slides 05, 09 (compliance cert pain point, foundation controls)
- `arrakis_blueprint_v2_3.md`, A12 Corrino — Portfolio Monitoring
