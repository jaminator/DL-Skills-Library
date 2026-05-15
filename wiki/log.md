# Wiki Operations Log

Append-only chronology of every INGEST, QUERY, LINT, and UPDATE operation performed by the `wiki-editor` agent. Entries follow the format defined in `WIKI-SCHEMA.md` § 4.

## 2026-05-13 — INGEST — Seed pass from canonical sources

- Files touched: `docs/sources/deal_lifecycle_automation_051326_vJA.pdf` (read via pre-extracted `.txt` mirror), `docs/sources/arrakis_blueprint_v2_3.md`
- Pages written: 26 across 9 categories
  - **deal-lifecycle (4):** deal-lifecycle-overview, origination-and-screening, term-sheet-and-commitment, closing-and-asset-management
  - **pain-points (3):** pain-point-register, posting-memo-friction, ic-and-asset-mgmt-gaps
  - **opportunities (1):** opportunity-register
  - **economics (4):** growth-gap, efficiency-dividend, three-roi-levers, non-sponsor-friction-premium
  - **strategic-options (3):** three-options, option-c-recommendation, foundation-controls
  - **arrakis-architecture (3):** arrakis-overview, foldspace-substrate, application-directory
  - **data-substrate (3):** snowflake-medallion, master-data-entities, redpanda-event-bus
  - **llm-integration (3):** spice-llm-service, hitl-state-machine, mcp-tool-catalog
  - **governance (2):** data-classification-tiers, restricted-content-discipline
- New categories: deal-lifecycle, pain-points, opportunities, economics, strategic-options, arrakis-architecture, data-substrate, llm-integration, governance (all 9 minted in this pass)
- New tags: process, deal-lifecycle, pain-point, opportunity, economics, governance, architecture, application, data-product, event, policy
- Notes: Seed bootstrap. Pages compile and synthesize from the two canonical sources rather than transcribing. Category folders created on first page write per the schema. No raw/ files present yet — the seed runs against `docs/sources/` only. `progress.json.wiki.seed_complete` set to `true` upon completion of this entry.

## 2026-05-13 — LINT — Post-pilot lint pass; broken links repaired; pilot and pattern pages added

- Files touched:
  - **New pages (5):**
    - `wiki/llm-integration/prompt-versioning-governance.md`
    - `wiki/llm-integration/output-validation-failure-taxonomy.md`
    - `wiki/opportunities/opportunity-shapes.md`
    - `wiki/library-design/compliance-certificate-parser-pilot.md`
    - `wiki/library-design/library-artifact-bundle.md`
  - **Updated pages (5):**
    - `wiki/opportunities/opportunity-register.md` — cross-links to `opportunity-shapes` and `compliance-certificate-parser-pilot`
    - `wiki/pain-points/posting-memo-friction.md` — cross-links to `opportunity-shapes`, `compliance-certificate-parser-pilot`, `library-artifact-bundle`
    - `wiki/deal-lifecycle/closing-and-asset-management.md` — updated to reflect that P17 was chosen as the actual first pilot (not P4); cross-link to `compliance-certificate-parser-pilot`
    - `wiki/strategic-options/option-c-recommendation.md` — cross-links to `library-artifact-bundle` and `compliance-certificate-parser-pilot`
    - `wiki/index.md` — five new rows; new `library-design` category recorded; `opportunities` and `llm-integration` page counts bumped
- New categories: `library-design` (first page: `compliance-certificate-parser-pilot`)
- New tags: `pilot` (used on `compliance-certificate-parser-pilot`)
- Lint findings remediated:
  - **Broken wikilinks (2):** `[[prompt-versioning-governance]]` from `spice-llm-service.md` and `[[output-validation-failure-taxonomy]]` from `hitl-state-machine.md` — both concepts authoritatively defined in `arrakis_blueprint_v2_3.md` Section 7. Pages created with content sourced from the blueprint.
  - **Content gaps:** Phase-2 / Phase-3 / Phase-4 build (pilot vertical slice for P17 Compliance Certificate Parser) had no wiki representation despite being 60% of committed phases. Created `compliance-certificate-parser-pilot.md`. Promoted the "Three recurring shapes" sub-section of `opportunity-register.md` into its own `opportunity-shapes.md` page since the taxonomy is the spine of the library's expansion logic. Created `library-artifact-bundle.md` to document the reusable skill + prompt + project instruction + Pydantic schema construction pattern proved by the pilot.
- Lint findings — no action required:
  - **Orphans:** zero. Every existing page has ≥3 inbound `[[wikilinks]]`. Lowest inbound counts: `closing-and-asset-management`, `origination-and-screening`, `redpanda-event-bus`, `term-sheet-and-commitment` at 3 each. These are stage-level / infrastructure-level pages where 3 inbound is appropriate density.
  - **Stale pages:** none. All pages dated 2026-05-13, well within the 180-day threshold.
  - **Contradictions:** none detected on full read of all 26 existing pages plus the two canonical sources.
  - **Missing sources:** none. All pages declare at least one source in frontmatter.
  - **Schema violations:** none. All pages carry required frontmatter, body within 200–800 words, `## Related Concepts` and `## Sources` sections present.
- Page count: 26 → 31 (five additions). `progress.json.wiki.page_count` updated. `progress.json.wiki.last_lint_date` set to 2026-05-13.

## 2026-05-13 — INGEST — Skill naming convention documented

- Files touched:
  - **New pages (1):** `wiki/methodology/skill-naming-convention.md`
  - **Updated pages (1):** `wiki/index.md` — new row for `skill-naming-convention`; new `methodology` category recorded
- New categories: `methodology` (first page: `skill-naming-convention`)
- New tags: `skills`, `conventions`, `naming`
- Notes: Codifies the `dl-<domain>-<action-or-subtype>` skill naming convention adopted in `CLAUDE.md` in the same commit cluster. The wiki page is the queryable synthesis; `CLAUDE.md` is the binding instruction. The 16-domain registry is mirrored on both — drift between the two is a future lint finding. The convention sits on top of `docs/anthropic/Skills_Best_Practices.md` and never overrides it. The pilot skill (`parsing-compliance-certificates`) does not yet conform and will be migrated in a follow-on commit; the wiki page already names `dl-compliance-verify` as the target so the cross-link from `compliance-certificate-parser-pilot` lands correctly once the rename happens.

## 2026-05-13 — UPDATE — Pilot skill renamed; compcert domain registered

- Files touched:
  - **Renamed:** `skills/parsing-compliance-certificates/` → `skills/dl-compcert-review/` (directory + 3 files: `SKILL.md`, `reference/covenant-types.md`, `reference/cfo-error-patterns.md` — only `SKILL.md` content modified).
  - **Updated pages (3):**
    - `wiki/library-design/compliance-certificate-parser-pilot.md` — artifact table rows updated to new skill path; "Gerund-named" descriptor replaced with `dl-<domain>-<action-or-subtype>` convention reference.
    - `wiki/methodology/skill-naming-convention.md` — registry row `compliance` → `compcert`; "Adding a new domain" inline example updated; Related Concepts cross-link updated to `dl-compcert-review`.
    - `wiki/log.md` — this entry.
  - **Non-wiki updates** (recorded here for cross-environment traceability since this UPDATE has wiki-side consequences): `CLAUDE.md` registry (compliance → compcert), `progress.json` (skill_path), `project-instructions/stage-6-asset-management.md` (P17 row), `schemas/compliance_certificate_validation.py` (docstring), `docs/pilot-validation.md` (artifact path, char count, name-convention sub-check superseded from "gerund form" to "dl-<domain>-<action-or-subtype>" check).
- New categories: none.
- New tags: none.
- Registry change: `compliance` (canonical example `dl-compliance-verify`) → `compcert` (canonical example `dl-compcert-review`). The semantic scope ("compliance certificate review") is unchanged; the domain slug is tightened to a compound-noun form so a future `compliance` slug remains available for non-certificate regulatory work if needed. Updated in lockstep in `CLAUDE.md` and `wiki/methodology/skill-naming-convention.md` in the same commit.
- Notes: Supersedes the forward-looking note in the prior log entry that named `dl-compliance-verify` as the rename target. The actual rename target was `dl-compcert-review`, chosen because `compliance` is too broad for a domain (could later collide with KYC/regulatory compliance work) and `compcert` is the precise compound noun for the input class. Final grep confirms zero remaining references to `parsing-compliance-certificates` outside of pedagogical "legacy gerund-form names" examples in the methodology page, and zero references to `dl-compliance-verify` outside of the historical context of the prior log entry. Page count unchanged (32). `last_ingest_date` unchanged.

## 2026-05-15 — INGEST — Direct-lending deal template set cataloged

- Files touched:
  - **New category:** `deal-templates` (first page: `template-library-overview`)
  - **New pages (7):** `wiki/deal-templates/template-library-overview.md`, `screening-templates.md`, `dd-analytical-workbooks.md`, `term-sheet-and-ic-templates.md`, `closing-and-am-templates.md`, `form-credit-agreement.md`, `market-deal-terms-reference.md`
  - **Updated pages (1):** `wiki/index.md` — 7 new rows; new `deal-templates` category recorded (page count 7)
- Sources ingested (19 `raw/` files): 17 blank "vTemplate" deal documents (kick-off data requests; posting memo + backup; screening memo + sponsor addendum; databook; Overland model; comps; refi-payback analysis; Wells & Overland DD list; IC summary; Wells & Overland term sheet; closing memo + backup; compliance certificate tracker; DDTL draw calc; amendment memo) plus 2 institutional reference documents (`Overland Form Credit and Guaranty Agreement.docx`; `Overland - Middle Market Deal Terms Presentation (May 2025).pdf`).
- New categories: `deal-templates`
- New tags: none (used existing `template`, `process`, `precedent`, `governance`, `policy`, `risk`, `sector`, `deal-lifecycle`)
- Method: extraction parallelized across 5 read-only subagents (Office files are ZIP+XML — no Python/pandoc/libreoffice available; `unzip` + tag-strip used; PDF read directly). Synthesis and all `wiki/` writes performed by the single sole-writer session. Agent Teams deliberately not used (sole-writer rule forbids parallel `wiki/` writers; same-category pages written sequentially for cross-link coherence).
- Deal-data exclusion enforced: subagents flagged residual live-deal content in three sources — the closing memo and amendment memo (real borrower / sponsor / project names, fund-leverage commentary in threaded comments, named co-lenders/affiliates) and the closing-memo backup (fund-leverage comments). These specifics were **not** preserved in the wiki; pages describe the underlying template structure and process with generic placeholders only. Maintainer note: the `raw/` source files still contain this live content and should be scrubbed to placeholders before any external reuse (the wiki-editor does not modify `raw/`).
- Notes:
  - The 19 files form one dependency chain (intake → analysis → decision → closing → monitoring); the controlling cross-file pattern is a single covenant-definition source (`Overland Form Credit and Guaranty Agreement.docx` §6 / §1.6) cascading through the closing digest, compliance tracker, DDTL draw calc, and amendment memo — reinforces [[compliance-certificate-parser-pilot]].
  - `raw/` filenames violate the `raw/README.md` lowercase-hyphen convention (spaces, brackets, `[Company]` token). Ingested as-found per the immutability rule; `sources:` frontmatter quotes the verbatim filenames. Flag for maintainer: future drops should follow the convention or the README should note the template-naming exception.
  - Pre-existing discrepancy observed (not modified): the prior UPDATE log note states "Page count unchanged (32)" while `progress.json.wiki.page_count` and `wiki/index.md` both reflected 31 before this ingest. Treated 31 as authoritative; new count 31 → 38. Recommend a LINT pass to reconcile the stray 32 reference.
  - `progress.json` updated: `page_count` 31 → 38; `last_ingest_date` 2026-05-15. `pending_raw_files` was empty (these files were dropped without a `wiki-check.sh` run); left empty.
