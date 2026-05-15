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

## 2026-05-15 — INGEST — Second-pass template input-schema catalog (canonical bucket library)

- Files touched:
  - **New pages (5):** `wiki/deal-templates/template-input-schema.md` (spine: canonical `$defs` bucket library + JSON-extensible design), `screening-input-schema.md`, `dd-workbook-input-schema.md`, `term-sheet-ic-input-schema.md`, `closing-am-input-schema.md`
  - **Updated pages (8):** the 7 existing `deal-templates` pages each cross-linked to their schema counterpart (`template-library-overview` also gained a body sentence; `form-credit-agreement` and `market-deal-terms-reference` linked to the spine as vocabulary-source / value-calibrator); `wiki/index.md` — 5 new rows, `deal-templates` count 7 → 12
- Sources re-read (the 15 fill-in `raw/` templates; the 2 reference docs have no inputs to populate): extraction parallelized across 4 read-only Explore subagents, one per fill-in cluster, focused on **input-bearing fields/placeholders** rather than the structural sheet/section inventory the first pass captured. Synthesis and all `wiki/` writes by the single sole-writer session (Agent Teams not used — sole-writer rule).
- New categories: none. New tags: `schema` (recorded here per WIKI-SCHEMA §2; applied to all 5 new pages).
- Method / design: the controlling finding is that the term sheet, IC summary, closing memo, compliance tracker, DDTL draw calc, and amendment memo are projections of one shared **deal-terms core**. Modeled as a canonical bucket library (~25 reusable `$defs`: `deal_identity`, `facility_structure`, `pricing`, `grids`, `fees`, `financial_covenants`, `ebitda_build`, `legal_doc_digest`, …) plus two cross-cutting patterns (`modification_delta` for the amendment memo, `trade_ticket` as a flattened view). Each template is catalogued as a `$ref` composition + named template-specific buckets; granular Excels are bucketed, not cell-mapped, per the explicit ask. The form credit agreement supplies the covenant/EBITDA vocabulary; the market deck calibrates value ranges.
- Deal-data exclusion: enforced. Subagents surfaced residual live-deal specifics in the closing/amendment sources (named co-lenders, sponsor, fund-leverage commentary); none preserved — schema pages use bucket/field names and generic placeholders only. The prior maintainer flag (scrub `raw/` before external reuse) stands.
- Graduation path (recommendation, not built): the `$defs` map 1:1 onto Pydantic models in `schemas/` per [[library-artifact-bundle]]; a `deal_terms_core` schema is the natural next artifact when a term-sheet or IC-summary skill is built.
- Page-count discrepancy (pre-existing, not reconciled here — deferred to LINT as the prior entry recommended): `wiki/index.md` now has 44 page rows; `progress.json.wiki.page_count` carried 38 and is set to 43 (38 + 5) to stay consistent with the prior entry's authoritative basis. The unreconciled +1 between the index row count and the tracked count persists and still needs a LINT pass.
- `progress.json` updated: `page_count` 38 → 43; `last_ingest_date` 2026-05-15; `pending_raw_files` left empty.

## 2026-05-15 — INGEST — PortCo Coverage Template (asset-management monitoring workbook)

- Files touched:
  - **New pages (2):** `wiki/deal-templates/portco-coverage-workbook.md` (structural anatomy + upstream/downstream consumer map), `wiki/deal-templates/portco-coverage-input-schema.md` (per-sheet bucket composition against [[template-input-schema]])
  - **Updated pages (5):** `wiki/index.md` (2 new rows, `deal-templates` count 12 → 14); `closing-and-am-templates`, `template-library-overview`, `closing-am-input-schema`, `compliance-certificate-parser-pilot` — each gained one `Related Concepts` backlink so neither new page is an orphan
- Source ingested: `raw/PortCo Coverage Template (02-26-26) vF.xlsx` (added in commit `c591dde`). Python/Excel-COM unavailable in-environment (Store-stub Python; COM stalled on the embedded S&P Capital IQ add-in) — workbook parsed by reading the OOXML zip directly via .NET (`System.IO.Compression` + `XmlReader`/`XmlDocument`), resolving `sharedStrings.xml` (654 entries) against each worksheet. 12 sheets: Dashboard, Charts, Financials Input, Covenant Input, Trade Ticket Input, Add-On Input, Public/Tnx Comps Input, Data Validation, two separators, and a `veryHidden` `_CIQHiddenCacheSheet`.
- New categories: none. New tags: none (reused `template`, `process`, `governance`, `risk`, `data-product`, `schema`).
- Method / design: the workbook is the **standing per-portfolio-company AM monitoring workspace** — not a per-phase deliverable. Modeled as a *referenced* composition that re-keys nothing: it pulls `deal_terms_core`, `pro_forma_cap`, `ebitda_build`, `financial_covenants`, `historical_financials`, `working_capital`, `comparable_set`, `trade_ticket` (view) from the closing artifacts and layers four new monitoring projections — `financial_basis_matrix`, `cap_table_snapshot`, `valuation_mark`, `add_on_summary` — onto them. Upstream: closing memo + backup, form CA §1.6/Art 6, databook/model. Downstream: Chronograph / A12 Corrino seed, recurring covenant control (operational superset of the [[compliance-certificate-parser-pilot]]), quarterly valuation marks (A13 Melange / ASC 820), risk ratings, SEC/LP reporting via the Snowflake consumption layer, and the amendment/upsize databook launch point; at-close trade-ticket + cap = the Facility master-entity payload.
- Deal-data exclusion: enforced. Source is a blank `vTemplate` (placeholders `[Company Name]`, `[X]`, `[Name]`; default comp tickers are a generic Aerospace & Defense set, not deal data; default pricing-grid/call-protection numbers are template examples and were not transcribed). No live-deal data preserved. RESTRICTED-class outputs (fund-level valuation marks) flagged on both pages via [[restricted-content-discipline]].
- Page-count discrepancy (pre-existing, still unreconciled — deferred to LINT as prior entries recommend): `wiki/index.md` now has 46 page rows; `progress.json.wiki.page_count` set 43 → 45 (43 + 2) to stay consistent with the prior entries' authoritative basis. The standing index-vs-tracker offset persists and still needs a LINT pass.
- `progress.json` updated: `page_count` 43 → 45; `last_ingest_date` 2026-05-15; `pending_raw_files` left empty.

## 2026-05-15 — LINT — Post-templates lint pass; stale gerund-form residuals repaired; page-count reconciled

- Files touched:
  - **Updated pages (2):**
    - `wiki/library-design/library-artifact-bundle.md` — §"Skill — the procedural workflow" updated: path placeholder `skills/<gerund-name>/SKILL.md` → `skills/dl-<domain>-<action-or-subtype>/SKILL.md`; "Frontmatter `name` is … gerund form" → "Frontmatter `name` is … follows the [[skill-naming-convention]]"; Related Concepts gains `[[skill-naming-convention]]`; `last_updated` 2026-05-13 → 2026-05-15.
    - `wiki/library-design/compliance-certificate-parser-pilot.md` — Validation Outcome item 2: "Skill — gerund-named `name`" → "Skill — `name` follows the [[skill-naming-convention]] (`dl-compcert-review`)"; Related Concepts gains `[[skill-naming-convention]]`; `last_updated` 2026-05-13 → 2026-05-15.
  - **Non-wiki updates:** `progress.json` — `page_count` 45 → 46 (reconciliation, see below); `last_lint_date` 2026-05-13 → 2026-05-15; new `lint-2` checkpoint appended.
- New categories: none. New tags: none.
- Findings — remediated:
  - **Stale-residual contradictions (2).** `library-artifact-bundle.md` and `compliance-certificate-parser-pilot.md` still described the skill artifact in gerund-form language ("gerund-name", "gerund form", "gerund-named"), contradicting the now-canonical [[skill-naming-convention]] and the `CLAUDE.md` skill-naming section. The pilot skill was renamed `parsing-compliance-certificates` → `dl-compcert-review` in the prior UPDATE (2026-05-13); these two pages were not updated in lockstep. Treated as cosmetic alignment (no factual claim reversed; the canonical convention has been authoritative since the rename), so corrected in place per WIKI-SCHEMA §5 rather than flagged with a `⚠️ CONTRADICTION` callout.
  - **Sole topical orphan: `skill-naming-convention`.** Pre-fix, zero topical inbound `[[wikilinks]]` (the page was only referenced from `wiki/index.md`, which is a catalog, not a topical page). The two contradiction repairs above added two topical inbound links from `library-artifact-bundle` and `compliance-certificate-parser-pilot` — the natural callers, since the bundle pattern and the pilot artifact table are exactly where readers learn how skills get named. Inbound count 0 → 2.
  - **Page-count tracker drift.** `progress.json.wiki.page_count` was 45; `wiki/index.md` row count is 46; on-disk file count is 46. The standing offset originated 2026-05-13 when the skill-naming-convention INGEST added a page but its log entry recorded "Page count unchanged (32)" and `progress.json` was not bumped (true value 31 → 32 at that time). Each subsequent INGEST carried the −1 offset forward (see the recommendations in the last three log entries). Reconciled by setting `page_count = 46` against the on-disk file count, which is authoritative.
- Findings — no action required:
  - **Broken wikilinks:** zero. Full regex sweep of `[[slug]]` references across all 46 topical pages plus `index.md` and `log.md` resolves cleanly to existing page files. (The only literal hit for the pattern is the prose `[[wikilinks]]` example in `WIKI-SCHEMA.md` and `log.md` — not a link.)
  - **Orphans:** none after the two new inbound links above. Lowest topical inbound counts now: `skill-naming-convention`, `portco-coverage-input-schema`, `screening-input-schema` at 2–3 each — appropriate density for definitional / second-pass-schema pages.
  - **Stale pages:** none. The staleness threshold (last_updated < 2025-11-16) is not crossed by any page; all 46 pages are dated 2026-05-13 or 2026-05-15.
  - **Missing sources:** none. All 46 pages declare ≥1 source in frontmatter.
  - **Schema violations:** none. All 46 pages carry the required frontmatter fields, body within ~200–830 words (one page, `application-directory`, sits at 830 including its Related/Sources sections — body proper is within bounds; not flagged), and both `## Related Concepts` and `## Sources` sections present. Folder name matches `category` frontmatter on every page.
  - **CLAUDE.md ↔ wiki domain-registry drift:** none. Both the `CLAUDE.md` skill-naming registry and the [[skill-naming-convention]] page list the same 16 domains in the same order: teaser, criteria, nda, ddq, financials, databook, expert, mgmt, stoplight, memo, termsheet, ca, compcert, valuation, amendment, wiki. The pedagogical note about prior `compliance` → `compcert` rename is on the wiki page only, by design — it is institutional context, not registry content.
  - **Categories table:** consistent with on-disk reality. 12 categories (deal-lifecycle 4, pain-points 3, opportunities 2, economics 4, strategic-options 3, arrakis-architecture 3, data-substrate 3, llm-integration 5, governance 2, library-design 2, methodology 1, deal-templates 14) sum to 46.
- Notes: This entry closes the +1 index-vs-tracker offset that the prior three log entries flagged. The wiki is internally consistent end-to-end as of 2026-05-15. The `raw/`-filename-convention flag (live-deal content in the closing/amendment template sources; spaces and `[Company]` tokens in `raw/` filenames) raised in earlier entries remains an open maintainer item — `raw/` is outside the wiki-editor's write scope.

## 2026-05-15 — INGEST — Production Claude Desktop skills cataloged

- Files touched:
  - **New category:** `production-skills` (first page: `production-skill-inventory`)
  - **New pages (5):** `wiki/production-skills/production-skill-inventory.md` (gateway), `wiki/production-skills/sector-research-screener.md`, `wiki/production-skills/posting-memo-automation.md`, `wiki/production-skills/prompt-generator-skill.md`, `wiki/methodology/overland-credit-framework.md`
  - **Updated pages (6):** `wiki/index.md` (5 new rows, new `production-skills` category, `methodology` count 1→2); `deal-lifecycle/origination-and-screening.md`, `pain-points/posting-memo-friction.md`, `deal-templates/screening-templates.md`, `library-design/library-artifact-bundle.md` — each gained Related-Concepts backlinks so no new page is an orphan; `methodology/skill-naming-convention.md` — added a "Production divergence — maintainer flag" section + backlink
  - **Non-wiki:** `progress.json` (`page_count` 46→51, `last_ingest_date` 2026-05-15); four skill zips committed to `raw/` in a preceding `chore(raw)` commit (precedent: PortCo `c591dde`)
- Sources ingested (4 `raw/` zips, untracked drops): `ol-industry-screener.zip`, `ol-prompt-generator.zip`, `overland-posting-memo.zip`, `populating-posting-memo-backup.zip` — each a `SKILL.md` + one-level-deep `references/` (+ `assets/`/`scripts/` for the Office-output skills). Extracted to a scratch dir and read in full; not transcribed.
- New categories: `production-skills`. New tags: none (reused `skills`, `process`, `template`, `system`, `opportunity`, `sector`, `policy`, `risk`).
- Method / design: these are skills **live in Claude Desktop production**, a new content class distinct from the in-repo pilot and the construction-pattern pages. Modeled as a dedicated `production-skills` category (gateway inventory + one page per skill) with the two P4 posting-memo skills (`overland-posting-memo` narrative .docx + `populating-posting-memo-backup` calc .xlsx) synthesized into a single `posting-memo-automation` page since they are one deliverable split along a narrative/quantitative seam. The shared analytical spine (credit quality screen, FCF 10-step decomposition, base-rate evidence hierarchy, industry attractiveness screen / three-tier structure) was lifted into a single `methodology/overland-credit-framework` page so the three credit skills reference rather than restate it — synthesis over transcription per WIKI-SCHEMA §1.
- Deal-data exclusion: enforced. All four skills are template/meta assets using placeholder names ("Stark Tech", `[Company]`) and generic/public illustrative examples (public-company cascade anchors, illustrative industry tables); no live-deal data preserved.
- **Maintainer flag — naming-convention divergence (open).** The four production skill names do not follow the documented [[skill-naming-convention]] (`dl-<domain>-<action-or-subtype>`): two carry an `ol-` prefix, two are freeform. Git history shows an `ol-` convention was trialed (`154f7ae`, `6164d0d`) then reverted to `dl-` (`ddfd5ce`); the deployed fleet is on a different scheme from the documented one. The page's literal claim (scoped to `skills/`, which holds only the conforming `dl-compcert-review`) is not contradicted, so this is recorded as a governance gap with a `> ⚠️` maintainer-flag callout on `skill-naming-convention.md` and the inventory page — **not** silently reconciled. Renaming production skills or formally adopting `ol-` is a maintainer decision outside the wiki-editor's scope.
- Page count: 46 → 51 (5 additions; no offset introduced — Categories table sums to 51). `progress.json.wiki.page_count` set to 51; `last_ingest_date` 2026-05-15; `pending_raw_files` left empty (zips dropped without a `wiki-check.sh` run).
