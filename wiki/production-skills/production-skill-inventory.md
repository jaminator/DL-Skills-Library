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

| Skill | Lifecycle locus | Shape | Page |
| --- | --- | --- | --- |
| `ol-industry-screener` | P1 Deal Sourcing | generate-with-review | [[sector-research-screener]] |
| `overland-posting-memo` | P4 Posting Memo (narrative) | generate-with-review | [[posting-memo-automation]] |
| `populating-posting-memo-backup` | P4 Posting Memo (quantitative) | extract-and-validate | [[posting-memo-automation]] |
| `ol-prompt-generator` | Cross-cutting utility | generate-with-review | [[prompt-generator-skill]] |

## The sourcing-to-posting chain

Three of the four skills form a forward-chained workflow automating the front of [[origination-and-screening]]:

1. **`ol-industry-screener`** decomposes a sector into sub-verticals, scores each against the Overland attractiveness screen, and emits a structured markdown handoff (Pursue / Watch / Screened Out, with cascade anchors, NAICS, trade orgs). It declares a **downstream contract** to an unbuilt `p2_borrower-identification` skill — the schema is frozen so the next phase can parse it.
2. The P4 pair — **`overland-posting-memo`** (the narrative `.docx`) and **`populating-posting-memo-backup`** (the calc `.xlsx`) — together produce the [[screening-templates|posting memo + backup]] deliverable that instantiates [[posting-memo-friction]]. The narrative skill drafts twelve memo sections in-place into the bundled Word template; the backup skill extracts CIM/CIP financials into the `FinSum`/`SUCAP` tabs while protecting all formulas. They share Overland's structuring policy and the [[overland-credit-framework|credit framework]] as a common analytical spine.

`ol-prompt-generator` is orthogonal — a meta-skill that productizes prompt engineering itself, embedding the same credit framework so prompts it generates inherit Overland's analytical conventions.

## Construction characteristics

These skills realize the spirit of [[library-artifact-bundle]] but as **shipped Claude Desktop assets**, not the four-artifact repo bundle: each is a `SKILL.md` plus one-level-deep `references/`, with bundled `assets/` (Word/Excel templates) and `scripts/` (openpyxl / python-docx populators) where the deliverable is an Office file. Each carries a "Format compatibility" note for running inside a claude.ai Project (copy body to project instructions, bundle references as project files). They are self-contained — no filesystem-path or repository references leak to the Desktop user, satisfying the distribution-environment rule.

## Maintainer flag — naming-convention divergence

The production skill names do **not** follow the library's documented [[skill-naming-convention]] (`dl-<domain>-<action-or-subtype>`, binding in `CLAUDE.md` and the methodology page). Two use an `ol-` (Overland) prefix (`ol-industry-screener`, `ol-prompt-generator`); two use freeform descriptive names (`overland-posting-memo`, `populating-posting-memo-backup`). Git history shows an `ol-` convention was trialed (commits `154f7ae`, `6164d0d`) then reverted in `CLAUDE.md`/wiki back to `dl-` (`ddfd5ce`), leaving the deployed fleet on a different scheme from the documented one. Recorded as a governance flag for maintainer resolution, not silently reconciled — renaming production skills and choosing the canonical prefix is a maintainer decision outside the wiki-editor's scope. See the divergence note on [[skill-naming-convention]].

## Related Concepts

- [[sector-research-screener]] — the P1 screener skill
- [[posting-memo-automation]] — the P4 narrative + backup pair
- [[prompt-generator-skill]] — the cross-cutting prompt meta-skill
- [[overland-credit-framework]] — the analytical spine three of the skills embed
- [[library-artifact-bundle]] — the construction pattern these realize in production
- [[skill-naming-convention]] — the documented convention the deployed names diverge from
- [[origination-and-screening]] — the lifecycle stages these skills automate

## Sources

- `ol-industry-screener.zip`, `SKILL.md` + `references/`
- `overland-posting-memo.zip`, `SKILL.md` + `references/` + `scripts/`
- `populating-posting-memo-backup.zip`, `SKILL.md` + `references/`
- `ol-prompt-generator.zip`, `SKILL.md` + `references/`
