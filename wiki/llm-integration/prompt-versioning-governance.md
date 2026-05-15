---
title: Prompt Versioning and Governance
category: llm-integration
tags: [llm-integration, governance, data-product]
sources:
  - arrakis_blueprint_v2_3.md
last_updated: 2026-05-13
---

# Prompt Versioning and Governance

Prompts in Arrakis are governed with the same discipline as data products. Every prompt is a versioned record, every change goes through PR review, every classified prompt is enforced at invocation, and every prompt whose output is consumed by another app is registered as a data contract. This is what makes the prompt library auditable at the same level as the Snowflake medallion.

## Where prompts live

Prompts have two homes that stay in lockstep:

- **PostgreSQL `prompt_library` table** managed by [[spice-llm-service]]. The schema: `prompt_id`, `app_id`, `task_type`, `version`, `content`, `model`, `max_tokens`, `classification`, `created_at`, `deprecated_at`. Spice reads from this table at invocation time.
- **Git monorepo** at `shared/llm_service/prompts/`. The source of truth for change history. Production deploys synchronize the Git content into the `prompt_library` table on release.

**No live editing in production.** A prompt change is a code change — branch, PR, review, deploy. Hot-patching prompts through the database is prohibited.

## Versioning rules

Each `(app_id, task_type)` tuple has exactly one **active version** at a time. Versions are integers, monotonically increasing. The Spice authorization matrix uses `prompt_id` (which encodes the tuple) plus `version` to decide which `app_id` may invoke the prompt. Deprecated versions are retained — the `deprecated_at` timestamp marks them dormant but still queryable for audit reconstruction.

A prompt invocation always logs the exact `prompt_version` used. The AI output audit trail in `ARRAKIS_RAW.APP_EVENTS` carries the version with every record so that downstream drift analysis can attribute behavior changes to specific prompt revisions.

## Classification — the same four tiers

Every prompt is classified using the four-tier [[data-classification-tiers]] scheme that governs data:

- **RESTRICTED** — prompts that handle IC deliberation content, individual votes, fund-level economics, or firm-internal portfolio context. The pilot's compliance-certificate-parser prompt sits at the boundary (CONFIDENTIAL output but RESTRICTED context possible).
- **CONFIDENTIAL** — prompts that handle deal financials, term-sheet economics, DD findings.
- **INTERNAL** — utility prompts (search reformulation, NDA metadata extraction, workflow routing).
- **PUBLIC** — not used in this domain.

The prompt's classification governs **who can invoke it**. Spice rejects a prompt invocation from an `app_id` whose ceiling is below the prompt's classification with HTTP 403. The classification also dictates the audit-trail destination — RESTRICTED prompts log to a separate sealed audit schema with tighter access controls.

## Cross-app prompts are data contracts

Some prompts produce output that another app consumes. The canonical example: Reverend Mother's triage memo identifies focus areas that Sardaukar uses to seed its DD queue. The triage-memo prompt's structured output schema is **the contract's schema**, registered in the Data Contract Application alongside Snowflake data product contracts. Schema changes trigger DCA review and version-bump events on the contract.

This means a prompt change can break a downstream app's behavior the same way an API change can — and is governed the same way: contract version bumps, deprecation windows, consumer notification, dual-path rollout.

## What this means for the library

A prompt drafted in this development environment is built so it lands cleanly in the `prompt_library` table when the artifact graduates:

- A stable cache-eligible system prefix (the row's `content`).
- An explicit classification (RESTRICTED / CONFIDENTIAL / INTERNAL).
- A bound Pydantic schema for the structured output (the prospective DCA contract schema if the prompt is cross-app).
- An intended consumer noted in the prompt body (`<consumer>ic</consumer>`, `<consumer>co-lender</consumer>`).
- A `schema_version` in the schema docstring so the inaugural version is `1` and evolution is explicit from day one.

The same prompt then runs under Spice's brokering without rewriting — see [[spice-llm-service]] for the resilience, budget, and validation profile that wraps every invocation.

## Related Concepts

- [[spice-llm-service]] — the broker that reads from the prompt library
- [[output-validation-failure-taxonomy]] — disposition policy applied to every invocation
- [[hitl-state-machine]] — the review gate every Spice output flows into
- [[data-classification-tiers]] — the tier scheme prompts inherit
- [[library-artifact-bundle]] — how this library packages prompts for graduation

## Sources

- `arrakis_blueprint_v2_3.md`, Section 7 — Prompt Versioning, Management, and Governance
