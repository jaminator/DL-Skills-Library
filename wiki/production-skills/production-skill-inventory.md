---
title: Production Skill Inventory
category: production-skills
tags: [skills, process, template]
sources:
  - ol-industry-screener.zip
  - ol-prompt-generator.zip
  - overland-posting-memo.zip
  - populating-posting-memo-backup.zip
last_updated: 2026-05-15
---

# Production Skill Inventory

This page catalogs the skills **actually deployed in Claude Desktop production** for the Overland Advantage underwriting team. It is distinct from [[library-artifact-bundle]] (the construction pattern) and [[compliance-certificate-parser-pilot]] (the in-repo pilot): the skills here are live, in-use assets the team invokes today, ingested as institutional knowledge of what has shipped.

## The four deployed skills

| Repo skill (production deployment name) | Lifecycle locus | Shape | Page |
| --- | --- | --- | --- |
| `dl-sector-screen` (production: `ol-industry-screener`) | P1 Deal Sourcing | generate-with-review | [[sector-research-screener]] |
| `dl-memo-posting` (production: `overland-posting-memo`) | P4 Posting Memo (narrative) | generate-with-review | [[posting-memo-automation]] |
| `dl-memo-posting-backup` (production: `populating-posting-memo-backup`) | P4 Posting Memo (quantitative) | extract-and-validate | [[posting-memo-automation]] |
| `dl-prompt-generate` (production: `ol-prompt-generator`) | Cross-cutting utility | generate-with-review | [[prompt-generator-skill]] |

## The sourcing-to-posting chain

Three of the four skills form a forward-chained workflow automating the front of [[origination-and-screening]]:

1. **`dl-sector-screen`** (production: `ol-industry-screener`) decomposes a sector into sub-verticals, scores each against the Overland attractiveness screen, and emits a structured markdown handoff (Pursue / Watch / Screened Out, with cascade anchors, NAICS, trade orgs). It declares a **downstream contract** to an unbuilt `p2_borrower-identification` skill — the schema is frozen so the next phase can parse it.
2. The P4 pair — **`dl-memo-posting`** (production: `overland-posting-memo`; the narrative `.docx`) and **`dl-memo-posting-backup`** (production: `populating-posting-memo-backup`; the calc `.xlsx`) — together produce the [[screening-templates|posting memo + backup]] deliverable that instantiates [[posting-memo-friction]]. The narrative skill drafts twelve memo sections in-place into the bundled Word template; the backup skill extracts CIM/CIP financials into the `FinSum`/`SUCAP` tabs while protecting all formulas. They share Overland's structuring policy and the [[overland-credit-framework|credit framework]] as a common analytical spine.

`dl-prompt-generate` (production: `ol-prompt-generator`) is orthogonal — a meta-skill that productizes prompt engineering itself, embedding the same credit framework so prompts it generates inherit Overland's analytical conventions.

## Construction characteristics

These skills realize the spirit of [[library-artifact-bundle]] but as **shipped Claude Desktop assets**, not the four-artifact repo bundle: each is a `SKILL.md` plus one-level-deep `references/`, with bundled `assets/` (Word/Excel templates) and `scripts/` (openpyxl / python-docx populators) where the deliverable is an Office file. Each carries a "Format compatibility" note for running inside a claude.ai Project (copy body to project instructions, bundle references as project files). They are self-contained — no filesystem-path or repository references leak to the Desktop user, satisfying the distribution-environment rule.

## Naming-convention divergence — repo gap resolved

The naming-convention gap previously flagged here **is resolved at the repository level.** All four production skills have been conformed into `skills/` as `dl-*` four-artifact bundles following the [[skill-naming-convention]] (`dl-<domain>-<action-or-subtype>`): `ol-industry-screener` → `dl-sector-screen`, `overland-posting-memo` → `dl-memo-posting`, `populating-posting-memo-backup` → `dl-memo-posting-backup`, `ol-prompt-generator` → `dl-prompt-generate`. The two new domains the conformance required (`sector`, `prompt`) were registered in `CLAUDE.md` and the methodology page's domain registry in lockstep.

What remains is **production provenance, not an open gap.** The skills still running in Claude Desktop carry their original deployment names (`ol-industry-screener`, `ol-prompt-generator` with an `ol-`/Overland prefix; `overland-posting-memo`, `populating-posting-memo-backup` freeform) until the live fleet is redeployed under the conformant names. Git history shows an `ol-` convention was trialed (commits `154f7ae`, `6164d0d`) then reverted to `dl-` (`ddfd5ce`); the deployment names are kept throughout this category as real institutional knowledge of what is live, paired with each repo-conformant name. Redeploying the Desktop fleet is a maintainer operation tracked outside the wiki. See the resolved-gap note on [[skill-naming-convention]].

## Related Concepts

- [[sector-research-screener]] — the P1 screener skill
- [[posting-memo-automation]] — the P4 narrative + backup pair
- [[prompt-generator-skill]] — the cross-cutting prompt meta-skill
- [[overland-credit-framework]] — the analytical spine three of the skills embed
- [[library-artifact-bundle]] — the construction pattern these realize in production
- [[skill-naming-convention]] — the convention these skills now conform to in `skills/`; deployment names kept as provenance
- [[origination-and-screening]] — the lifecycle stages these skills automate

## Sources

- `ol-industry-screener.zip`, `SKILL.md` + `references/`
- `overland-posting-memo.zip`, `SKILL.md` + `references/` + `scripts/`
- `populating-posting-memo-backup.zip`, `SKILL.md` + `references/`
- `ol-prompt-generator.zip`, `SKILL.md` + `references/`
