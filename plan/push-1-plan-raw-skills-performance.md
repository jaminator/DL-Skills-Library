# Plan — Conform the four production skills in `raw/`, build full four-artifact bundles, relocate to `skills/`

**Status:** APPROVED — decisions D-1..D-3 resolved (see §7); ready to execute
**Author:** Claude Code
**Date:** 2026-05-15
**Scope rule:** conformance + bundle construction with **no behavioral refactoring** of the four skills. They work well in Claude Desktop production; this pass makes them library-conformant, schema-backed, prompt-paired, and stage-pinned — not different.

---

## 1. What we are working with

Four production skills live as immutable archives in `raw/` (per `CLAUDE.md` rule 9, `raw/` is never modified — the zips stay; conformed copies are written to `skills/`):

| `raw/` zip | Current name | Lifecycle locus | Shape | Bundled assets/scripts |
| --- | --- | --- | --- | --- |
| `ol-industry-screener.zip` | `ol-industry-screener` | **Stage 1 / P1** Deal Sourcing | generate-with-review | `references/` (1 file, 187 ln) |
| `overland-posting-memo.zip` | `overland-posting-memo` | **Stage 2 / P4** Posting Memo (narrative) | generate-with-review | `references/` (2), `assets/*.docx`, `scripts/populate_memo.py` |
| `populating-posting-memo-backup.zip` | `populating-posting-memo-backup` | **Stage 2 / P4** Posting Memo (quant) | extract-and-validate | `references/` (5), `assets/*.xlsx` |
| `ol-prompt-generator.zip` | `ol-prompt-generator` | **Cross-cutting** (no lifecycle phase) | generate-with-review | `references/` (2) |

Lifecycle mapping confirmed against `wiki/deal-lifecycle/deal-lifecycle-overview.md` + `origination-and-screening.md`: Stage 1 Origination = P1 Deal Sourcing · P2 NDA; Stage 2 Screening = P3 Kick-Off DDQ · P4 Posting Memo.

The in-repo conformant model is the pilot bundle: `skills/dl-compcert-review/` + `schemas/compliance_certificate_validation.py` + `prompts/stage-6-asset-management/P17-compliance-certificate-parser.md` + `project-instructions/stage-6-asset-management.md`. We mirror its construction exactly.

---

## 2. Conformance gap analysis

Authority: `CLAUDE.md` conformance rules, `wiki/library-design/library-artifact-bundle.md`, `wiki/methodology/skill-naming-convention.md`, `docs/anthropic/Skills_Best_Practices.md`, `wiki/WIKI-SCHEMA.md`, pilot bundle.

| # | Criterion | Current state | Fix | Behavior impact |
| --- | --- | --- | --- | --- |
| C-1 | **Naming** `dl-<domain>-<action/subtype>` | `ol-`/freeform | Rename (§3); register 2 new domains lockstep | None |
| C-2 | **Pydantic schema** per bundle | None | `schemas/*.py` documenting the *existing* emitted contract | None (Arrakis/portability contract, not a runtime instruction) |
| C-3 | **HITL watermark** | Posting memo .docx has none | **D-2 = preserve behavior, document only.** Do NOT inject the watermark into the .docx. Document the obligation in the Portability note + reflect in the prompt's Output Contract + carve it out explicitly in the Stage 2 project instruction (see §4.5) | **None** (per D-2) |
| C-4 | **No path leakage / self-contained** | Backup SKILL hardcodes `/mnt/skills/user/populating-posting-memo-backup/...` | Update embedded path to new skill name; verify others | None (mechanical) |
| C-5 | **SKILL.md ≤500 lines** | `overland-posting-memo` = **540** (over); others 148/425/140 OK | Relocate STEP 13 mechanics + bullet conventions into `reference/population-mechanics.md`; SKILL.md keeps the guide + pointer | None (moves into a ref the skill already reads) |
| C-6 | **Reference >100 ln needs ToC** | 8 refs >100 ln, no ToC | Prepend `## Contents` to each | None (additive) |
| C-7 | **Reference dir name** | `references/` (plural); pilot uses `reference/` | Normalize to `reference/`; update intra-SKILL links (**D-4**) | None (mechanical) |
| C-8 | **Explicit `## Anti-patterns`** | Rules inline | Add a section distilled from existing inline rules | None (surfaces existing rules) |
| C-9 | **Wiki reconciliation** | 7 pages carry the divergence flag + old names | Post-rename LINT/UPDATE (wiki-editor scope) | None (docs only) |
| C-10 | **Description ≤1024 ch, 3rd person** | All 3rd person, within limit | Verify only | None |
| **C-11** | **Prompt artifact** (bundle) | None | `prompts/<stage>/<phase>-<task>.md` per skill, cache-stable system prefix + XML inputs, mirrors existing skill behavior | None (instruction layer mirrors the skill) |
| **C-12** | **Project-instruction artifact** (bundle) | None | Stage-level project instructions (§4.5) — consult wiki, embed institutional knowledge | None (context-pinning layer) |

---

## 3. Approved name mapping (D-1)

| Current | → New | Domain | Domain status |
| --- | --- | --- | --- |
| `ol-industry-screener` | `dl-sector-screen` | `sector` | **NEW** — sector/sub-vertical sourcing screen; no existing domain fits (`criteria` = per-deal investment-criteria screening, not sector decomposition) |
| `overland-posting-memo` | `dl-memo-posting` | `memo` | Existing — registry example |
| `populating-posting-memo-backup` | `dl-memo-posting-backup` | `memo` | Existing — multi-segment subtype keeps the P4 pair under `/dl-memo-` |
| `ol-prompt-generator` | `dl-prompt-generate` | `prompt` | **NEW** — cross-cutting prompt meta-skill; no lifecycle domain fits |

Two new domains (`sector`, `prompt`) require a **lockstep registry edit in the same commit**: (1) `CLAUDE.md` Domain registry, (2) `wiki/methodology/skill-naming-convention.md` Domain registry. Drift between them is a lint finding. **Orchestrator-only** (shared files).

---

## 4. Per-skill work packages (full four-artifact bundle)

Each package = `skills/<new-name>/SKILL.md` + `reference/` (+ `assets/`/`scripts/` verbatim) + `schemas/<name>.py` + `prompts/<stage>/<phase>-<task>.md` + a "Portability into Arrakis" SKILL.md note (mirrors `dl-compcert-review`). Stage-level **project instructions are built once at orchestrator level** (§4.5) because Stage 2 is shared by two skills. Source = extract `raw/*.zip` to a scratch dir (never edit `raw/`).

### WP-A — `dl-sector-screen` (from `ol-industry-screener`) · Stage 1 / P1
- Rename dir + frontmatter `name`. Body unchanged except: `reference/` rename, `## Contents` ToC in `overland-industry-attractiveness-screen.md` (187 ln), `## Anti-patterns` from existing Constraints, Portability note.
- **Schema** `schemas/sector_screen_handoff.py` → `SectorScreenHandoff` (`sub_verticals: list[SubVertical]` with `verdict: Literal["pursue","watch","screened_out"]`, `naics`, `verdict_rationale`, `scope_caveat`, `thesis`, `watch_flags`, `cascade_anchors`, `trade_orgs`; `open_questions`; `schema_version`; `requires_human_review`; `review_state`). Formalizes the already-frozen downstream `p2_borrower-identification` handoff contract — high value.
- **Prompt** `prompts/stage-1-origination/P1-sector-research-screener.md` — system prefix (role: sourcing analyst; 9-step approach; uncertainty = `[unresolved: …]`/Open Questions; classification: internal sourcing; Output Contract = the frozen markdown schema, schema referenced) + XML variable inputs (`<sector_scope>`, optional `<pitchbook_context>`). Mirrors current behavior; emits the same markdown.

### WP-B — `dl-memo-posting` (from `overland-posting-memo`) · Stage 2 / P4
- Rename. **C-5 split**: move STEP 13 (population mechanics, run snippet, bullet-format conventions, out-of-scope list) → `reference/population-mechanics.md`; SKILL.md retains STEP 0 + analytical framework + section map + Sections 1–12 + one-level pointer. Verify ≤500 ln via `wc -l`.
- `reference/` rename; `## Contents` ToC for `memo-sections.md` (296) + `population-mechanics.md`; `base-rate-framework.md` (75) none. `## Anti-patterns` from existing "no follow-ups / no speculation / CA EBITDA label" rules. Copy `assets/posting-memo-template.docx` + `scripts/populate_memo.py` **verbatim**.
- **Schema** `schemas/posting_memo_content.py` → `PostingMemoContent` mirroring the `populate_memo.py` content-dict docstring **field-for-field** (keys: `header`, `situation_overview`, `company_overview{opening,bullets}`, `financial_headline`, `discussion_analysis`, `su_note`, `risk_flags`, `strengths`, `considerations`, `recommendation`, `designated_criteria`, `posting_rating`, `final_rating`). Agent MUST read `scripts/populate_memo.py` first; cross-validate no drift.
- **Prompt** `prompts/stage-2-screening/P4-posting-memo.md` — system prefix mirrors STEP 0 discipline; **D-2 carve-out**: Output Contract states the deliverable is the in-place populated `.docx` (script-produced, unchanged) and the schema is the Arrakis-side structured contract; the watermark is applied at the HITL/PENDING_REVIEW layer and signaled by the `vS` draft filename + "Pending Overland IC Feedback" default — **not** injected into the Word body.

### WP-C — `dl-memo-posting-backup` (from `populating-posting-memo-backup`) · Stage 2 / P4
- Rename. **C-4**: update hardcoded `SKILL_ASSETS = '/mnt/skills/user/populating-posting-memo-backup/assets'` (+ any other embedded old-name path) → `dl-memo-posting-backup`. `reference/` rename. `## Contents` ToC for `cell-map.md` (380), `structuring-rules.md` (323), `EXAMPLES.md` (274), `CHANGELOG.md` (242), `fccr-addback-guide.md` (182). `CHANGELOG.md` historical — keep (satisfies "old patterns" carve-out), note in Portability. `## Anti-patterns` from existing "Key Constraints" + "blank ≠ zero" + "never hallucinate". Copy `assets/*.xlsx` verbatim.
- **Schema** `schemas/posting_memo_backup_extraction.py` → `PostingMemoBackupExtraction` (`company_name`, `column_map`, `finsum_rows` with `type: Literal["as_reported","adjusted"]` and per-column `float|None` blank≠zero, `sucap`, `intentional_formula_mods: list[str]`, `analyst_flags: list[str]`, `schema_version`, `requires_human_review`, `review_state`). Encodes the existing extraction-summary contract.
- **Prompt** `prompts/stage-2-screening/P4-posting-memo-backup.md` — system prefix mirrors the mandatory Step-0 gate, K2-first protocol, formula-protection discipline; Output Contract = the populated `.xlsx` (unchanged) + the extraction-summary schema as the Arrakis contract.

### WP-D — `dl-prompt-generate` (from `ol-prompt-generator`) · Cross-cutting
- Rename. `reference/` rename; `## Contents` ToC for `EXAMPLES.md` (140); `overland-credit-framework.md` (69) none. `## Anti-patterns` from existing "does not generate SKILL.md / omit non-applicable components".
- **Schema** `schemas/generated_prompt_spec.py` → thin `GeneratedPromptSpec` (`elicitation{inputs_tools,model,output}`, `components_emitted: list[str]`, `target_model`, `schema_version`, HITL fields) for bundle-parity symmetry; the Portability note records that this meta-skill's *primary* output (a free-form prompt) is **not** Snowflake-destined, so the schema captures only the generation spec, not the prompt body.
- **Prompt** `prompts/cross-cutting/prompt-generator.md` — system prefix = the elicitation framework + generated-prompt component set + Overland analytical inheritance; XML inputs (`<task_description>`, `<inputs_tools>`, `<model_pref>`, `<output_spec>`).
- **Project instruction = N/A (documented exemption)** — see §4.5.

---

## 4.5 Project-instruction chunking analysis (per maintainer guidance)

Principle (from `deal-lifecycle-overview.md`: "a project instruction exists because one stage's deal context is recurring"; and `library-artifact-bundle.md`: project instruction = stage-level context pinning): **one project instruction per lifecycle stage, covering the whole stage**; fragment into 2+ per stage only when that stage has *many phases × many deliverables × heavy per-deliverable sub-processes* (e.g., a databook deliverable needing extensive ETL/data-cleaning pre-work on non-sponsored primary materials before template population). Established file convention: `project-instructions/stage-<n>-<name>.md` (pilot = `stage-6-asset-management.md` spanning P17–P19 in one file).

Decision for this pass — **no fragmentation needed; build two stage files + one documented exemption:**

| Stage | File | Phases covered | Skills active this pass | Future placeholders (from wiki) | Fragment? |
| --- | --- | --- | --- | --- | --- |
| 1 Origination | `project-instructions/stage-1-origination.md` | P1 Deal Sourcing · P2 NDA | `dl-sector-screen` (P1) | P1 teaser auto-parse, DealCloud/SF sync; P2 auto-NDA (route-and-track) | **No** — 2 phases, one active deliverable, light sub-processes |
| 2 Screening | `project-instructions/stage-2-screening.md` | P3 Kick-Off DDQ · P4 Posting Memo | `dl-memo-posting` + `dl-memo-posting-backup` (P4 narrative+quant pair) | P3 auto-DDQ, standardized databook (flagged as the heavy-pre-work watchpoint) | **No, with watchpoint** — 2 phases; P4 is one deliverable pair within one phase; the two skills are the narrative/quant split of a single deliverable, not separate deliverables |
| — Cross-cutting | *none* | n/a | `dl-prompt-generate` | — | **N/A** — a non-lifecycle utility has no recurring deal context; a stage project instruction would be a hollow artifact. The bundle for `dl-prompt-generate` = skill + prompt + schema; the project-instruction slot is **formally documented as N/A** in its Portability note (honest application of the wiki, not a coverage gap) |

**Documented watchpoint (not actioned now):** if Stage 2 later gains the P3 auto-DDQ skill *and* the standardized-databook skill (the databook deliverable carries heavy non-sponsored primary-materials ETL/data-cleaning pre-work — exactly the user's fragmentation trigger), split into `stage-2a-kickoff-ddq.md` + `stage-2b-posting-memo.md`. Recorded here so the future maintainer has the rationale; not split today because P3 has no skill yet and P4 is a single deliverable pair.

**Each stage project instruction MUST (mirror the pilot `stage-6` file and consult the wiki):**
1. Stage + phase header and purpose (from `deal-lifecycle-overview.md`).
2. Deal-context slot (filled at deal kick-off).
3. **Active deliverables table enumerating every deliverable in the stage** drawn from the wiki (`origination-and-screening.md` phase/deliverable/pain-point/opportunity inventory) — active deliverables mapped to their `dl-` skill + cadence; not-yet-built deliverables listed as explicit future placeholders so the instruction surfaces the *full* stage scope, not only the shipped skills.
4. Artifact-versioning convention `[COMPANY]-[DELIVERABLE]-v[N]-[YYYYMMDD]`.
5. Behavioral rules — incl. the **D-2 watermark carve-out** for the P4 posting-memo `.docx` (watermark obligation stated; the in-place Word artifact is signalled by the `vS` draft filename + "Pending Overland IC Feedback" default and the HITL `PENDING_REVIEW` state, not by injecting the banner into the Word body — keeps the project instruction internally consistent with the preserved skill behavior).
6. **Institutional Knowledge** section: 3–5 wiki pages compiled inline with a compile-date marker (so the project runs without filesystem/wiki access). Recommended embeds — Stage 1: `origination-and-screening`, `growth-gap`, `sector-research-screener`, `overland-credit-framework`. Stage 2: `origination-and-screening`, `posting-memo-friction`, `posting-memo-automation`, `overland-credit-framework`.

---

## 5. Execution strategy — parallel subagents + serialized orchestrator phase

The four bundles are independent with disjoint output paths and need **no inter-agent discussion** → per `docs/anthropic/Agent_Teams.md` this is the **subagent** case ("quick, focused workers that report back … subagents are more effective for … work [without] inter-agent coordination"), not an agent team (teams add token + coordination overhead with no benefit here). Per `CLAUDE.md` rule 10: no worktrees/branches; all work on shared `main`; conflict avoidance by **task partition** only. Each subagent re-reads `docs/anthropic/Skills_Best_Practices.md` first (rule 1).

```
Phase 0 — orchestrator (sequential)
  └─ Extract the 4 raw/*.zip → scratch dir (NOT raw/). git status must show raw/ unchanged.

Phase 1 — 4 subagents IN PARALLEL (disjoint paths, zero collision)
  ├─ Agent A → WP-A : skills/dl-sector-screen/ + schemas/sector_screen_handoff.py
  │                   + prompts/stage-1-origination/P1-sector-research-screener.md
  ├─ Agent B → WP-B : skills/dl-memo-posting/ + schemas/posting_memo_content.py
  │                   + prompts/stage-2-screening/P4-posting-memo.md
  ├─ Agent C → WP-C : skills/dl-memo-posting-backup/ + schemas/posting_memo_backup_extraction.py
  │                   + prompts/stage-2-screening/P4-posting-memo-backup.md
  └─ Agent D → WP-D : skills/dl-prompt-generate/ + schemas/generated_prompt_spec.py
                      + prompts/cross-cutting/prompt-generator.md
     Each runs the §6 checklist + a behavior-diff self-check; reports back.

Phase 2 — orchestrator ONLY (shared / synthesis files, must be serialized)
  ├─ Register `sector` + `prompt` domains: CLAUDE.md + skill-naming-convention.md (one commit)
  ├─ Build project-instructions/stage-1-origination.md and stage-2-screening.md
  │   (shared by ≥1 skill; require wiki consultation + institutional-knowledge embed — §4.5)
  ├─ Wiki LINT/UPDATE (wiki-editor scope): retire divergence flag, repoint old→new names across
  │   the 7 production-skills/methodology pages, refresh index.md, append log.md
  ├─ progress.json: record the four bundles; scratch-dir cleanup
  └─ Commit + push origin main per CLAUDE.md rule 11 (artifact deliverable + wiki LINT both
      trigger commit+push). Conventional Commits. Surface push failure with git output.
```

Project instructions are deliberately Phase-2 orchestrator work (not split to subagents): `stage-2-screening.md` is shared by WP-B and WP-C (collision risk), and all project instructions are cross-cutting wiki-synthesis artifacts better authored with whole-stage context in one place.

---

## 6. Per-bundle conformance checklist (each subagent self-verifies)

```
SKILL
- [ ] dir + frontmatter name = dl-<domain>-<action/subtype>; ≤64 ch; lowercase/hyphen; no claude/anthropic
- [ ] description 3rd person, ≤1024 ch, what + when
- [ ] SKILL.md body ≤500 lines (wc -l)
- [ ] references one level deep; dir = reference/ ; intra-links updated
- [ ] each reference >100 ln has ## Contents ToC
- [ ] ## Anti-patterns present (distilled from existing rules — no new behavior)
- [ ] no path leakage; embedded skill-name paths updated to new name
- [ ] assets/ + scripts/ byte-identical to source — no behavior change
- [ ] Portability-into-Arrakis note added (mirrors dl-compcert-review)
SCHEMA
- [ ] snake_case; JSON-serializable; schema_version; requires_human_review=True;
      review_state Literal["PENDING_REVIEW"]; module docstring (phase/Arrakis app/landing tier/HITL)
- [ ] cross-validated field-for-field against the skill's actual emitted structure (no drift)
PROMPT
- [ ] cache-stable system prefix (role/approach/uncertainty/classification/Output Contract) ABOVE
      the XML variable inputs; Output Contract references the schema; D-2 carve-out honored (B/C)
- [ ] prompt instructions mirror — do not alter — the skill's existing behavior
BEHAVIOR
- [ ] behavior diff = none: workflow steps, output artifact, tool calls all unchanged vs raw/ source
```

---

## 7. Decisions — RESOLVED

- **D-1 Naming & new domains — APPROVED.** Mapping per §3; register `sector` + `prompt` lockstep in CLAUDE.md + skill-naming-convention.md.
- **D-2 Posting-memo watermark — PRESERVE BEHAVIOR, DOCUMENT ONLY.** No watermark injected into the `.docx`. Obligation documented in the Portability note + prompt Output Contract + carved out explicitly in `stage-2-screening.md` behavioral rules (§4.5 item 5). Existing `vS` draft filename + "Pending Overland IC Feedback" default + HITL `PENDING_REVIEW` are the draft signals.
- **D-3 Scope — FULL FOUR-ARTIFACT BUNDLE NOW.** Skill + schema + prompt for all four; stage-level project instructions per §4.5 (Stage 1, Stage 2; `dl-prompt-generate` PI = documented N/A). Project instructions must consult the wiki and surface the full stage deliverable inventory (active + future) with the institutional-knowledge embed.
- **D-4 (minor) `reference/` normalization — YES.** Rename `references/` → `reference/`, update intra-SKILL links (mechanical, behavior-neutral, repo-consistent with the pilot).

---

## 8. Risks & mitigations

| Risk | Mitigation |
| --- | --- |
| Behavior drift while "conforming" | Hard rule: workflow/output/tooling text byte-preserved; only additive (ToC, Anti-patterns, Portability) + mechanical (rename, path, dir) edits. C-5 split moves text into a ref the skill already loads. Per-bundle behavior-diff check vs the `raw/` source. |
| Prompt/PI silently changing skill behavior | Prompt = instruction mirror of the skill, not a re-spec; Output Contract documents (not alters) the artifact. D-2 carve-out keeps the .docx untouched. |
| Schema ↔ skill drift | Subagent reads the actual emitter (e.g., `populate_memo.py` docstring) before writing the schema; field-for-field cross-validate. |
| Registry table lockstep drift | Phase-2 orchestrator-only; both tables in one commit. |
| Project instruction missing stage deliverables | §4.5 mandates enumerating the full wiki deliverable inventory (active + future placeholders), not just shipped skills. |
| Stage-2 PI authored by two agents → conflict | Project instructions are Phase-2 orchestrator-only. |
| Wiki divergence flag left stale | Phase-2 mandatory LINT/UPDATE; index.md/log.md refreshed; commit+push per rule 11. |
| `raw/` accidentally modified | Extraction → scratch dir; `raw/` read-only by rule 9; verify `git status`. |
| Parallel file collision | Disjoint output paths per subagent; all shared/synthesis edits serialized in Phase 2. |
```
