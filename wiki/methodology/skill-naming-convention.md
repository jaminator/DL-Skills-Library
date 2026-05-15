---
title: Skill Naming Convention
category: methodology
tags: [skills, conventions, naming, governance, template]
sources:
  - CLAUDE.md
  - Skills_Best_Practices.md
last_updated: 2026-05-13
---

# Skill Naming Convention

Every skill in `skills/` follows the pattern **`dl-<domain>-<action-or-subtype>`** from creation. The convention is binding from the date of this page; legacy gerund-form names (e.g., `parsing-compliance-certificates`) are migrated, not preserved. The canonical instruction lives in `CLAUDE.md`; this page is the queryable synthesis agents read.

## Why a domain prefix

Three things the prefix buys, all of which compound as the library grows past a handful of skills:

- **Slash-command discoverability in Claude Desktop.** A user typing `/dl-` surfaces every direct-lending skill at once. Typing `/dl-ddq-` narrows to the DDQ family. Typing `/dl-memo-` narrows to the memo family. Discovery becomes mechanical instead of memorial.
- **Family grouping.** Skills that share a domain segment surface together in any alphabetic listing — file explorers, autocomplete, the SKILL inventory in a Claude Desktop project, the wiki index. The [[library-artifact-bundle]] pattern produces multiple skills per domain (memo has five, databook has four, ddq has four); shared prefixes keep families visually adjacent.
- **Clear namespace separation.** A maintainer who installs third-party skills into the same workspace can distinguish at a glance which skills are part of the Direct Lending Underwriting Library and which are not. The `dl-` prefix is short enough not to be ceremonial and long enough not to collide.

## The pattern

```
dl-<domain>-<action-or-subtype>
```

- `dl-` — fixed prefix marking the skill as part of the Direct Lending Underwriting Library.
- `<domain>` — the deliverable cluster or input type the skill operates on. Drawn from the domain registry below. Shared across related skills so the family surfaces together.
- `<action-or-subtype>` — what the skill does to that domain, or which subtype of the domain it handles. Verb form (`extract`, `verify`, `synthesize`, `draft`, `screen`) or subtype noun (`customers`, `comps`, `model`, `posting`, `prescreen`).

All other constraints from `docs/anthropic/Skills_Best_Practices.md` apply unchanged: lowercase letters/numbers/hyphens only, no reserved words ("anthropic", "claude"), ≤64 characters total, description ≤1024 characters in third person, SKILL.md body ≤500 lines, references one level deep, progressive disclosure.

## Domain registry

| Domain | Meaning | Example skill names |
| --- | --- | --- |
| `teaser` | Inbound teaser parsing and enrichment | `dl-teaser-parse` |
| `criteria` | Investment-criteria screening | `dl-criteria-screen` |
| `nda` | NDA workflow | `dl-nda-extract` |
| `ddq` | Due-diligence question lists across all rounds | `dl-ddq-kickoff`, `dl-ddq-initial`, `dl-ddq-followup`, `dl-ddq-gap` |
| `financials` | GAAP normalization, addbacks, bridges | `dl-financials-normalize` |
| `databook` | Initial and updated DD databook construction | `dl-databook-customers`, `dl-databook-model`, `dl-databook-comps`, `dl-databook-assemble` |
| `expert` | Expert-call synthesis (AlphaSights, GLG) | `dl-expert-synthesize` |
| `mgmt` | Management operational due diligence | `dl-mgmt-synthesize` |
| `stoplight` | Eight-dimension risk rating | `dl-stoplight-rate` |
| `memo` | Posting, pre-screen, commitment, closing, redacted memos | `dl-memo-posting`, `dl-memo-prescreen`, `dl-memo-commitment`, `dl-memo-closing`, `dl-memo-redact` |
| `termsheet` | Term sheet drafting and revision | `dl-termsheet-draft` |
| `ca` | Credit agreement parsing | `dl-ca-extract` |
| `compcert` | Compliance certificate review (parse, recompute, flag) | `dl-compcert-review` |
| `valuation` | ASC 820 valuation narrative drafting | `dl-valuation-draft` |
| `amendment` | Amendment summarization | `dl-amendment-summarize` |
| `wiki` | Wiki-editor operations (development environment only; never compiled into distribution) | `dl-wiki-ingest`, `dl-wiki-query`, `dl-wiki-lint`, `dl-wiki-update` |

## Adding a new domain

A new domain is added **only** when a proposed skill genuinely doesn't fit any existing domain — not because a slightly different label feels more natural. Before adding, check whether an action verb on an existing domain captures the same thing (`dl-compcert-review` covers parsing, validating, and flagging a compliance certificate in one skill; a separate `parse` domain would not earn its keep).

When a new domain is justified, the maintainer records it in two places, in the same commit:

1. The domain registry in `CLAUDE.md`.
2. The domain registry table on this page.

The two tables stay in lockstep. Drift between them is a lint finding.

## Relationship to skill-authoring best practices

This naming pattern is the "action-oriented" alternative form explicitly permitted by `docs/anthropic/Skills_Best_Practices.md` (e.g., `process-pdfs`, here adapted to `dl-teaser-parse` and similar). It **sits on top of** the underlying skill-authoring standards — it never overrides them. When the two conflict, the best-practices file wins, per the conflict-resolution rule at the top of `CLAUDE.md`.

The convention applies to skills in `skills/` only. Agents in `agents/` (including the `wiki-editor`) are scoped differently and do not carry the prefix.

## Production divergence — maintainer flag

> ⚠️ The skills **deployed in Claude Desktop production** (cataloged in [[production-skill-inventory]]) do not follow this convention. `ol-industry-screener` and `ol-prompt-generator` carry an `ol-` (Overland) prefix; `overland-posting-memo` and `populating-posting-memo-backup` are freeform descriptive names. Git history shows an `ol-` convention was trialed (commits `154f7ae`, `6164d0d`) then reverted in `CLAUDE.md` and this page back to `dl-` (`ddfd5ce`), leaving the deployed fleet on a scheme different from the documented one.

The literal claim above ("Every skill in `skills/` follows the pattern") is not contradicted — `skills/` contains only `dl-compcert-review`, which conforms; the production skills are deployed Desktop assets, not repo `skills/` entries. The divergence is therefore a **governance gap**, not a page-vs-page contradiction: the convention is documented but not enforced on the live fleet. Resolution (rename the production skills to one canonical scheme, or formally adopt `ol-`/freeform and update `CLAUDE.md` + this page in lockstep) is a maintainer decision; the wiki-editor records the gap and does not reconcile it.

## Related Concepts

- [[library-artifact-bundle]] — the four-artifact construction pattern the naming convention plugs into
- [[compliance-certificate-parser-pilot]] — the first skill renamed under this convention (`dl-compcert-review`)
- [[prompt-versioning-governance]] — analogous versioning discipline for the prompt half of each bundle
- [[production-skill-inventory]] — the deployed Claude Desktop fleet that diverges from this convention (maintainer flag)

## Sources

- `CLAUDE.md`, **Skill naming convention** section
- `Skills_Best_Practices.md`, **Naming conventions** section (lowercase + hyphens, ≤64 chars, no reserved words, action-oriented alternative form)
