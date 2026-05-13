---
title: Data Classification Tiers
category: governance
tags: [governance, data-product]
sources:
  - arrakis_blueprint_v2_3.md
last_updated: 2026-05-13
---

# Data Classification Tiers

Arrakis uses a **four-tier data classification scheme** that governs every column in Snowflake, every prompt in the prompt library, every MCP tool's return payload, and every artifact this library produces. Classification determines who can see the data, what masking applies, and what audit obligations attach.

## The four tiers

| Tier | What goes here | Examples |
| --- | --- | --- |
| **RESTRICTED** | Most sensitive. Audit-grade access controls, masking when crossing tenant boundaries, no exposure to co-lenders or LPs. | IC deliberation content, individual IC votes, fund-level economics above the co-lender tranche, Centerbridge-internal portfolio context |
| **CONFIDENTIAL** | Deal-specific commercial information. Visible to deal team and approved internal consumers; redacted for external counterparties unless explicitly cleared. | Deal financials, model outputs, DD findings, term-sheet economics, borrower KYC status |
| **INTERNAL** | Non-commercially sensitive operational data. Visible to all internal users with platform access. | Workflow state, task assignments, notification routing, system metadata |
| **PUBLIC** | None in this domain. The tier exists in the scheme but is not used for Arrakis data products. | — |

## How the tiers apply

**Snowflake columns.** Every column in CURATED and CONSUMPTION schemas carries a classification tag. Row Access Policies and Column Masking enforce visibility per RBAC role.

**Prompts.** Every prompt in the prompt library is classified using the same tier scheme. Prompts that handle IC content are RESTRICTED; prompts that handle deal financials are CONFIDENTIAL; utility prompts are INTERNAL. Prompt classification governs which apps can invoke the prompt and which audit trail it writes to.

**MCP tools.** Each tool in the [[mcp-tool-catalog]] declares a `return_data_classification` (the highest tier present in its return payload). Spice enforces this against the calling app's permitted classification ceiling.

**This library's artifacts.** Every prompt, skill, project instruction, and schema in this repository inherits the same scheme. The skill's body and the prompt's system prefix carry an implicit INTERNAL classification (no live deal data). The structured outputs are typically CONFIDENTIAL when populated with real deal context.

## RESTRICTED-content discipline

Any artifact intended for **co-lender or LP distribution** explicitly excludes:

- Fund-level economics above the co-lender tranche.
- IC deliberation content.
- Individual IC votes.
- Centerbridge-internal portfolio context.

Every external-facing prompt in this library carries an inline **redaction checklist line** stating these exclusions before the structured output. See [[restricted-content-discipline]] for the full pattern and the canonical checklist text.

## How this maps in Arrakis

The classification tag travels with the data through the Bronze → Silver → Gold pipeline. Snowflake Dynamic Tables and views inherit the classification of their source columns. The Foldspace Observatory monitors classification completeness — any unclassified column in CURATED or CONSUMPTION is flagged and routed for resolution.

The same tag travels with prompts. When Spice executes a prompt, the audit-trail event in `ARRAKIS_RAW.APP_EVENTS` carries the prompt's classification, the input context's classification, and the output's classification. This enables post-hoc queries like "show every RESTRICTED prompt invocation in Q3 by reviewer."

## What to do in this library

When constructing any artifact, ask explicitly:

1. **What tier is the input?** If RESTRICTED, the prompt carries an `is_external = false` constraint and the project instruction notes the classification ceiling.
2. **What tier is the output?** A draft IC memo is RESTRICTED; a draft posting memo is CONFIDENTIAL; a co-lender DD response is CONFIDENTIAL with a hard exclusion of RESTRICTED content (see [[restricted-content-discipline]]).
3. **Who is the next consumer?** A co-lender or LP consumer triggers the redaction checklist line. An internal consumer does not.

Recording the answer to these three questions in the artifact's frontmatter (for prompts) or in the project instruction's deal-context slot makes the artifact's classification auditable from day one.

## Related Concepts

- [[restricted-content-discipline]] — the redaction checklist for external-facing artifacts
- [[spice-llm-service]] — Spice's classification enforcement
- [[mcp-tool-catalog]] — tool-level classification metadata
- [[snowflake-medallion]] — column-level classification in the medallion

## Sources

- `arrakis_blueprint_v2_3.md`, Section 5.5 (Data Classification Scheme), Section 7 (Prompt Versioning Governance)
