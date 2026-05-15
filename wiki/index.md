# Wiki Index

Master catalog of every page in the wiki. Maintained by the `wiki-editor` agent.

| Page | Category | Summary | Status |
| --- | --- | --- | --- |
| [[deal-lifecycle-overview]] | deal-lifecycle | Six stages, 19 phases, lifecycle economics, gateway to stage detail | seed |
| [[origination-and-screening]] | deal-lifecycle | Stages 1–2 (P1 Sourcing → P4 Posting Memo) detail | seed |
| [[term-sheet-and-commitment]] | deal-lifecycle | Stages 3–4 (P5 Initial DDQ → P12 EL / Commit) detail | seed |
| [[closing-and-asset-management]] | deal-lifecycle | Stages 5–6 (P13 Syndication → P19 Amendments) detail | seed |
| [[pain-point-register]] | pain-points | All 23 pain points across the lifecycle, organized by stage | seed |
| [[posting-memo-friction]] | pain-points | P4 posting-memo friction (the highest-yield single pain point and recommended pilot) | seed |
| [[ic-and-asset-mgmt-gaps]] | pain-points | IC vote / minutes / approval-tracking and asset-management gaps | seed |
| [[opportunity-register]] | opportunities | All ~19 automation opportunities organized by stage and shape (extract / generate / route) | seed |
| [[opportunity-shapes]] | opportunities | The three repeating shapes (extract-and-validate / generate-with-review / route-and-track) and how to pick one | lint |
| [[growth-gap]] | economics | Status quo vs growth target portfolio trajectory; +$285M cumulative fee delta | seed |
| [[efficiency-dividend]] | economics | Headcount-avoidance economics; ~75 IPs avoided, ~$120M cumulative cost savings | seed |
| [[three-roi-levers]] | economics | Fee accretion, headcount avoidance, CBP data unification — self-funding from year one | seed |
| [[non-sponsor-friction-premium]] | economics | Per-stage labor-intensity premium; why peer cos/IP ratios don't port directly | seed |
| [[three-options]] | strategic-options | A (extend status quo), B (commercial point solutions), C (custom suite over substrate) | seed |
| [[option-c-recommendation]] | strategic-options | Why Option C is recommended primary path (Arrakis) | seed |
| [[foundation-controls]] | strategic-options | Eight governance investments required at any portfolio scale | seed |
| [[arrakis-overview]] | arrakis-architecture | One platform substrate plus 13 domain applications | seed |
| [[foldspace-substrate]] | arrakis-architecture | Foldspace platform layer: Kong, MDM API, DCA, Observatory, Spice, foldspace-mcp | seed |
| [[application-directory]] | arrakis-architecture | The 13 domain apps mapped to deal lifecycle phases | seed |
| [[snowflake-medallion]] | data-substrate | RAW / CURATED / CONSUMPTION layout; one landing schema per app | seed |
| [[master-data-entities]] | data-substrate | Seven golden-record entities with SCD Type 2 and ownership transfer | seed |
| [[redpanda-event-bus]] | data-substrate | Topic taxonomy, standard envelope, outbox pattern, idempotent consumer contract | seed |
| [[spice-llm-service]] | llm-integration | Centralized LLM brokering; resilience, token budgets, output validation | seed |
| [[hitl-state-machine]] | llm-integration | Eight review states, override audit record, drift detection | lint |
| [[mcp-tool-catalog]] | llm-integration | foldspace-mcp tool surface, error contract, governance metadata | seed |
| [[prompt-versioning-governance]] | llm-integration | Versioned prompts in Postgres + Git, four-tier classification, cross-app prompts as data contracts | lint |
| [[output-validation-failure-taxonomy]] | llm-integration | Five disposition categories Spice applies before returning a Claude response | lint |
| [[data-classification-tiers]] | governance | Four-tier scheme (RESTRICTED / CONFIDENTIAL / INTERNAL / PUBLIC) and how it travels | seed |
| [[restricted-content-discipline]] | governance | Redaction obligation for external-facing artifacts; canonical checklist text | seed |
| [[compliance-certificate-parser-pilot]] | library-design | The P17 pilot — first end-to-end vertical slice, extract-and-validate shape, A12 Corrino target | lint |
| [[library-artifact-bundle]] | library-design | The four-artifact construction pattern (skill + prompt + project instruction + Pydantic schema) | lint |
| [[skill-naming-convention]] | methodology | The `dl-<domain>-<action-or-subtype>` skill naming pattern and the 18-domain registry; production-skill conformance into `skills/` (deployment names kept as provenance) | lint |
| [[template-library-overview]] | deal-templates | Gateway: the 17-template + 2-reference deal-document chain, dependency map, recurring construction patterns | ingest |
| [[screening-templates]] | deal-templates | P3–P4 cluster: kick-off data requests, posting memo + backup, screening memo + sponsor addendum | ingest |
| [[dd-analytical-workbooks]] | deal-templates | P6 analytical core: databook, Overland model, comps, refi-payback analysis | ingest |
| [[term-sheet-and-ic-templates]] | deal-templates | P6–P11 instruments: DD list, IC summary scorecard, Wells & Overland term sheet | ingest |
| [[closing-and-am-templates]] | deal-templates | P16–P19 cluster: closing memo + backup, compliance tracker, DDTL draw calc, amendment memo | ingest |
| [[form-credit-agreement]] | deal-templates | Precedent + covenant source of truth; Article 6 / §1.6 architecture the P17 parser mirrors | ingest |
| [[market-deal-terms-reference]] | deal-templates | Counsel market-benchmarking deck across four MM segments; calibrates term-sheet variables | ingest |
| [[template-input-schema]] | deal-templates | Canonical input-bucket library (`$defs`/`$ref`); the single deal-terms object every template composes | ingest |
| [[screening-input-schema]] | deal-templates | P3–P4 per-template input-bucket composition (kick-off, posting backup/memo, screening deck/addendum) | ingest |
| [[dd-workbook-input-schema]] | deal-templates | P6 per-workbook input-bucket composition (databook, model, comps, refi) | ingest |
| [[term-sheet-ic-input-schema]] | deal-templates | P6–P11 per-template input-bucket composition and the `deal_terms_core` thesis | ingest |
| [[closing-am-input-schema]] | deal-templates | P16–P19 per-template input-bucket composition (closing memo/backup, tracker, draw calc, amendment) | ingest |
| [[portco-coverage-workbook]] | deal-templates | Standing per-PortCo AM monitoring workbook; closing→Chronograph/Corrino seed, valuation/risk/LP-reporting & amendment launch point | ingest |
| [[portco-coverage-input-schema]] | deal-templates | Per-sheet bucket composition of the coverage workbook; introduces financial-basis-matrix, cap-table-snapshot, valuation-mark, add-on-summary | ingest |
| [[production-skill-inventory]] | production-skills | Gateway: the four production skills, now conformed into `skills/` as `dl-*` bundles (deployment names kept as provenance), lifecycle mapping, sourcing→posting chain | ingest |
| [[sector-research-screener]] | production-skills | `dl-sector-screen` (production: `ol-industry-screener`) — P1 sub-vertical decomposition + attractiveness screen + frozen downstream handoff contract | ingest |
| [[posting-memo-automation]] | production-skills | `dl-memo-posting` + `dl-memo-posting-backup` (production: `overland-posting-memo` / `populating-posting-memo-backup`) — the P4 narrative .docx / calc .xlsx skill pair and Overland structuring policy | ingest |
| [[prompt-generator-skill]] | production-skills | `dl-prompt-generate` (production: `ol-prompt-generator`) — cross-cutting prompt meta-skill embedding the Overland credit framework | ingest |
| [[overland-credit-framework]] | methodology | The shared analytical spine: credit quality screen, FCF decomposition, base-rate evidence hierarchy, industry attractiveness screen | ingest |

## Categories

The wiki-editor records each category here the first time it writes a page in that category.

| Category | First page written | Page count |
| --- | --- | --- |
| deal-lifecycle | deal-lifecycle-overview (2026-05-13) | 4 |
| pain-points | pain-point-register (2026-05-13) | 3 |
| opportunities | opportunity-register (2026-05-13) | 2 |
| economics | growth-gap (2026-05-13) | 4 |
| strategic-options | three-options (2026-05-13) | 3 |
| arrakis-architecture | arrakis-overview (2026-05-13) | 3 |
| data-substrate | snowflake-medallion (2026-05-13) | 3 |
| llm-integration | spice-llm-service (2026-05-13) | 5 |
| governance | data-classification-tiers (2026-05-13) | 2 |
| library-design | compliance-certificate-parser-pilot (2026-05-13) | 2 |
| methodology | skill-naming-convention (2026-05-13) | 2 |
| deal-templates | template-library-overview (2026-05-15) | 14 |
| production-skills | production-skill-inventory (2026-05-15) | 4 |
