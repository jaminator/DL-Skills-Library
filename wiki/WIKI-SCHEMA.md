# Wiki Schema and Conventions

The wiki is the LLM-curated, interlinked institutional-knowledge layer of the Direct Lending Underwriting Library. The `wiki-editor` agent is the sole writer; every other session reads. This document specifies the page format, the four operations, the lint rules, and the deal-data exclusion rule.

The wiki is Obsidian-compatible — `[[wikilinks]]` and standard markdown render correctly in any Obsidian vault.

---

## 1. Page format

Every wiki page is a single markdown file with YAML frontmatter, a body of 200–800 words, a `## Related Concepts` section, and a `## Sources` section.

```markdown
---
title: <Title Case page title>
category: <category-slug>
tags: [<tag-1>, <tag-2>, ...]
sources:
  - <source-1.pdf>
  - <source-2.md>
last_updated: YYYY-MM-DD
---

# <Title Case page title>

<Body. 200–800 words. Synthesizes; does not transcribe. Uses [[wikilinks]] inline
when referring to other concepts. Avoids deal-specific data.>

## Related Concepts

- [[other-page-slug]] — one-line description of the relationship
- [[another-page-slug]] — one-line description

## Sources

- `<source-1.pdf>`, section/page reference where useful
- `<source-2.md>`, section/page reference where useful
```

### Frontmatter fields

| Field | Type | Notes |
| --- | --- | --- |
| `title` | string | Title Case. Should match the human-readable concept; do not include the category as a prefix. |
| `category` | string (slug) | One of the known categories from `wiki/index.md`, or a new slug recorded by the editor when first used. Lowercase, hyphens. |
| `tags` | list | Lowercase hyphen-slugs from the tag taxonomy below. Add new tags only when no existing tag fits. |
| `sources` | list | Filenames in `docs/sources/` or `raw/`. Filename only — no paths. |
| `last_updated` | ISO date | YYYY-MM-DD. Set on every write. |

### Body conventions

- 200 words minimum, 800 words maximum. If a topic exceeds 800 words, split it.
- Synthesize and compile — do not transcribe. If a page would be a near-verbatim copy of source material, skip it and let downstream agents refer to the source directly.
- Use `[[wikilinks]]` when referring to other concepts. The link target is the slug (filename without extension): `[[stoplight-rating]]` not `[[Stoplight Rating]]`.
- Quote sparingly. Block quotes only when the exact phrasing matters (e.g., a defined term).
- No deal-specific data: no live company names, no real EBITDA figures, no real facility sizes. Use generic placeholders if an example is needed.

### Filename convention

`<slug>.md` where slug is lowercase, hyphenated, derived from the title. Example: a page titled "Stoplight Risk Rating" lives at `wiki/<category>/stoplight-risk-rating.md`.

---

## 2. Tag taxonomy

Tags are flat (no hierarchy). The starting taxonomy:

| Tag | Use for |
| --- | --- |
| `process` | Workflow, sequence, or procedural content |
| `pain-point` | Identified friction or gap |
| `opportunity` | Identified automation or improvement target |
| `system` | Tooling or infrastructure |
| `economics` | Pipeline economics, fees, AUM, headcount |
| `governance` | Conflicts, IC, compliance, audit |
| `architecture` | Arrakis platform structure |
| `application` | One of the 13 Arrakis applications |
| `data-product` | Snowflake landing or curated/consumption product |
| `event` | Redpanda topic or event flow |
| `policy` | Investment policy, credit standards |
| `template` | Reusable form, checklist, or memo template |
| `playbook` | Sequenced response to a scenario |
| `precedent` | Historical clause or term reference |
| `sector` | Industry-specific content |
| `risk` | Risk taxonomy and assessment |

Tags are additive. The wiki-editor records any newly minted tag at the top of `wiki/log.md` for the relevant operation.

---

## 3. Categories

Categories are folder names under `wiki/`. They emerge from ingest — none are pre-created. Likely categories from the canonical sources (the editor decides finalization):

- `deal-lifecycle` — stage and phase content from the deck
- `pain-points` — friction register from the deck
- `economics` — Growth Gap, Efficiency Dividend, ROI levers
- `strategic-options` — Options A / B / C from the deck
- `arrakis-architecture` — Foldspace and substrate
- `data-substrate` — Snowflake medallion, MDM, contracts
- `applications` — per-app pages (Thumper, Gom Jabbar, ...)
- `llm-integration` — Spice, prompts, HITL, MCP catalog
- `governance` — DCA, Observatory, classification, RBAC

The editor creates a category folder the first time it writes a page in that category and records the new category in `wiki/index.md`.

---

## 4. The four wiki operations

| Operation | Trigger | Editor action |
| --- | --- | --- |
| **INGEST** | A new file appears in `raw/` (or in `docs/sources/` for the seed pass) | Read the file, identify topics, write or update one or more pages, update `index.md`, append to `log.md`. |
| **QUERY** | An agent asks an institutional-knowledge question | Search `index.md`, load relevant pages, synthesize an answer with `[[wikilink]]` citations, append a query record to `log.md`. |
| **LINT** | Scheduled or on-demand | Scan for contradictions, stale entries (>180 days), orphan pages (no inbound links), and missing cross-references. Append a lint report to `log.md`. |
| **UPDATE** | A maintainer surfaces an anonymized post-deal insight | Strip deal-specific data, integrate the underlying knowledge into the relevant page, append an update record to `log.md`. |

Append-only `log.md` entry format:

```markdown
## YYYY-MM-DD — <OPERATION> — <one-line summary>

- Files touched: <list>
- New categories: <list, if any>
- New tags: <list, if any>
- Notes: <optional>
```

---

## 5. Lint rules

The wiki-editor scans for and reports:

1. **Contradictions.** Two pages making incompatible factual claims. Marked inline in both pages with a `> ⚠️ CONTRADICTION` callout naming the conflicting page and the conflicting claim. Resolution requires maintainer review.
2. **Stale pages.** `last_updated` more than 180 days old. Reported but not deleted; staleness may be acceptable for stable concepts.
3. **Orphan pages.** No inbound `[[wikilinks]]` from any other page. Reported; the editor proposes parent pages or recommends archival.
4. **Broken wikilinks.** A `[[link]]` whose target page does not exist. The editor either creates the target page (if the concept is real) or removes the link (if the link is stale).
5. **Missing sources.** A page with an empty `sources` list. The editor either backfills sources or flags for maintainer review.
6. **Schema violations.** Frontmatter missing required fields, body length out of bounds, missing `## Related Concepts` or `## Sources` section.

Lint runs do not modify pages without explicit maintainer approval beyond cosmetic fixes (broken-link removal, frontmatter backfill).

---

## 6. Deal-data exclusion rule

The wiki contains institutional knowledge — patterns, processes, policies, precedents, architecture. It does not contain live-deal data.

Excluded from the wiki:
- Real company names, real sponsor names, real management names tied to a specific opportunity.
- Real EBITDA, revenue, leverage, or facility-size figures from a live deal.
- IC deliberation content, individual IC votes, or conditional approval text from a specific deal.
- Fund-level economics above the co-lender tranche.
- firm-internal portfolio context.

If a maintainer's anonymized lesson would be unreadable without specifics, generalize the lesson and use a placeholder example (`Co A, a $50M EBITDA software business, ...`) rather than naming the real deal. The lesson lives in the wiki; the deal lives in its Claude Desktop project.

---

## 7. What the wiki is not

- Not a transcription layer. If a source already says it well, link to the source instead of paraphrasing.
- Not a live operations dashboard. State (deal pipeline, IC queue, portfolio marks) lives in operational systems, not here.
- Not a versioned document store. Versioning belongs in `raw/` filenames or in upstream document management.
- Not a place for personal notes. Maintainer notes go in commits or pull requests, not in wiki pages.
