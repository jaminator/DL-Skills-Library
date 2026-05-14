# Overland Underwriting Library — Root Instructions

This repository is the **development environment** for the Overland Underwriting Library: a Claude-based knowledge and automation library that supports Overland's non-sponsored US middle-market direct lending underwriting team across the 6-stage, 19-phase deal lifecycle.

The library is consumed by the broader Overland UW team through Claude Desktop (system instructions, project instructions, prompts, skills) — no repository access. Repo maintainers iterate here using Claude Code; the team consumes through copy-paste of the curated assets.

Every artifact is built so it can graduate directly into Project Arrakis Option C (Foldspace substrate + 13 domain applications). Portability is achieved through construction patterns, not embedded metadata.

---

## Anchor sources — read at every session start, in parallel

Five files are authoritative. Read all five end-to-end before any other action.

**Canonical Overland sources** (`docs/sources/`):
1. `Overland_Deal_Lifecycle_Automation_051326_vJA.pdf` — the deal lifecycle deck. Authoritative for stages, phases, pain points, opportunities, pipeline economics, strategic framing. (A pre-extracted plain-text mirror exists at `Overland_Deal_Lifecycle_Automation_051326_vJA.txt` for tools that cannot parse the PDF.)
2. `arrakis_blueprint_v2_3.md` — Arrakis Option C architecture. Authoritative for Foldspace, the 13 applications, Spice, the Snowflake medallion, Pydantic conventions, the HITL state machine, the build sequencing.

**Anthropic best-practices references** (`docs/anthropic/`):
3. `Prompting_Best_Practices.md` — Opus 4.7 prompt engineering, effort levels, XML structuring, formatting, frontend defaults.
4. `Skills_Best_Practices.md` — SKILL.md structure, naming, progressive disclosure, workflow and validation patterns, the 500-line body limit.
5. `Agent_Teams.md` — when to use agent teams, sizing, task granularity, file-conflict avoidance, hooks.

**Conflict resolution.** When this file and the canonical sources disagree on a fact, the canonical sources win. When this file and the best-practices files disagree on a standard, the best-practices files win.

---

## Session-start protocol

At the start of every working session, in parallel:

1. Read `wiki/index.md` (the master wiki catalog).
2. Read `progress.json` (lightweight build-state tracker).
3. Run `git log --oneline -20` (recent change history).

These three reads orient any maintainer (human or Claude) without requiring a sweep of the full repository.

---

## Two-environment model

| Environment | Audience | Access | Artifacts |
| --- | --- | --- | --- |
| **Development** | Repo maintainers + Claude Code | Full repository | Source of truth |
| **Distribution** | Overland UW team via Claude Desktop | `dist/` contents only | Compiled, self-contained |

Every artifact destined for the distribution environment is fully self-contained: no filesystem paths to `wiki/` or `docs/`, no git commands, no instructions to "check the repository." A Claude Desktop user must be able to run any distributed asset using only the documents uploaded into their project.

A formal `dist/` build pipeline is out of scope for the initial build. Distribution artifacts are produced by copying source files and verifying self-containment manually.

---

## LLM Wiki layer (Karpathy pattern)

- **`raw/`** — flat folder of source documents. No subfolders. Maintainers drop files here. Filename convention encodes the topic: `credit-standards-investment-policy.pdf`, `template-posting-memo.docx`, `sector-saas-dd-checklist.md`. The `wiki-editor` agent reads from `raw/`; nothing modifies it.
- **`wiki/`** — LLM-generated, structured, interlinked Obsidian-readable markdown. Pages are 200–800 words and follow `wiki/WIKI-SCHEMA.md`. The `wiki-editor` agent is the sole writer; all other agents read.
- **`wiki/index.md`** is the master catalog; **`wiki/log.md`** is an append-only chronology of every ingest, query, lint, and update.

Four wiki operations: **INGEST** (raw → wiki page(s)), **QUERY** (knowledge question → synthesized answer), **LINT** (contradiction / staleness scan), **UPDATE** (anonymized post-deal insights merged in).

Wiki categories emerge from ingest. Do not pre-create empty category folders — the wiki-editor creates a category folder the first time it writes a page in that category and records the new category in `wiki/index.md`.

**Deal-data exclusion.** Live-deal data never enters `wiki/`. Deal state lives in Claude Desktop projects.

---

## Portability as a construction principle

Every prompt, skill, and instruction is constructed so it can be lifted into Arrakis Option C without rewriting:

- **Stable system prefix / variable input separation** in every prompt. The system prefix (role, instructions, output format, guardrails) comes first and is cache-eligible. Variable inputs are wrapped in semantic XML tags.
- **Pydantic-validated structured outputs** for any artifact destined for Snowflake persistence. Schemas live in `schemas/` and validate locally during development; in Option C, Spice validates the same schemas.
- **HITL watermark** — every IC-facing, legal, co-lender-facing, or AM-facing artifact carries `[DRAFT — HUMAN REVIEW REQUIRED]` until a human approves. This watermark maps to the Arrakis HITL state machine state `PENDING_REVIEW`.

Portability is achieved through how artifacts are built. Boilerplate frontmatter is not required.

---

## Conformance rules — apply to every artifact

1. **Read best-practices files first.** Re-read `docs/anthropic/Skills_Best_Practices.md` before writing any skill, `docs/anthropic/Prompting_Best_Practices.md` before any prompt, `docs/anthropic/Agent_Teams.md` before spawning any agent or sub-task. Treat them as binding standards.
2. **Source materials are authoritative.** Re-read `docs/sources/` for any factual claim about the deal lifecycle or Arrakis architecture. Do not paraphrase from memory.
3. **Parallel tool calls where independent.** Read multiple reference files at session start in parallel. Write wiki pages in different categories in parallel. Sequential where dependencies exist.
4. **No filesystem-path references in distribution-environment artifacts.** Every skill, prompt, system instruction, and project instruction destined for Claude Desktop is fully self-contained.
5. **HITL watermark.** `[DRAFT — HUMAN REVIEW REQUIRED]` on every IC-facing, legal, co-lender-facing, or AM-facing output.
6. **RESTRICTED-content discipline.** Any artifact intended for co-lender or LP distribution explicitly excludes fund-level economics above the co-lender tranche, IC deliberation content, individual IC votes, and Centerbridge-internal portfolio context. Every external-facing prompt includes a redaction checklist line.
7. **`[INSUFFICIENT DATA — <what is missing>]`** is the only acceptable uncertainty marker. Never silently omit; never fabricate.
8. **Commit after every phase.** Use `feat: phase-<n> <deliverable>` format. Never combine phase commits.
9. **Never modify `raw/`.** The wiki-editor reads only.

---

## Skill naming convention

Every skill in `skills/` follows the pattern **`ol-<domain>-<action-or-subtype>`** from creation. The prefix gives Claude Desktop users a single discovery affordance: typing `/ol-` surfaces every Overland skill, and typing `/ol-<domain>-` surfaces every skill within a domain (e.g., `/ol-ddq-` returns the full DDQ family).

- `ol-` — fixed prefix marking the skill as Overland Underwriting Library.
- `<domain>` — the deliverable cluster or input type the skill operates on. Domain values are shared across related skills so the family surfaces together when typed.
- `<action-or-subtype>` — what the skill does to that domain, or which subtype of the domain it handles.

**Domain registry.** Use these values; add a new domain only when a skill genuinely doesn't fit an existing one. New domains are recorded both here and in `wiki/methodology/skill-naming-convention.md`.

| Domain | Meaning | Example skill names |
| --- | --- | --- |
| `teaser` | Inbound teaser parsing and enrichment | `ol-teaser-parse` |
| `criteria` | Overland investment-criteria screening | `ol-criteria-screen` |
| `nda` | NDA workflow | `ol-nda-extract` |
| `ddq` | Due-diligence question lists across all rounds | `ol-ddq-kickoff`, `ol-ddq-initial`, `ol-ddq-followup`, `ol-ddq-gap` |
| `financials` | GAAP normalization, addbacks, bridges | `ol-financials-normalize` |
| `databook` | Initial and updated DD databook construction | `ol-databook-customers`, `ol-databook-model`, `ol-databook-comps`, `ol-databook-assemble` |
| `expert` | Expert-call synthesis (AlphaSights, GLG) | `ol-expert-synthesize` |
| `mgmt` | Management operational due diligence | `ol-mgmt-synthesize` |
| `stoplight` | Eight-dimension risk rating | `ol-stoplight-rate` |
| `memo` | Posting, pre-screen, commitment, closing, redacted memos | `ol-memo-posting`, `ol-memo-prescreen`, `ol-memo-commitment`, `ol-memo-closing`, `ol-memo-redact` |
| `termsheet` | Term sheet drafting and revision | `ol-termsheet-draft` |
| `ca` | Credit agreement parsing | `ol-ca-extract` |
| `compliance` | Compliance certificate verification | `ol-compliance-verify` |
| `valuation` | ASC 820 valuation narrative drafting | `ol-valuation-draft` |
| `amendment` | Amendment summarization | `ol-amendment-summarize` |
| `wiki` | Wiki-editor operations (development environment only; never compiled into distribution) | `ol-wiki-ingest`, `ol-wiki-query`, `ol-wiki-lint`, `ol-wiki-update` |

**Canonical reference.** `wiki/methodology/skill-naming-convention.md` is the queryable wiki page agents should consult for the convention. This `CLAUDE.md` section is the binding instruction; the wiki page is the synthesized explanation.

**Relationship to skill-authoring best practices.** This naming pattern sits on top of `docs/anthropic/Skills_Best_Practices.md`; it never overrides it. All other rules in the best-practices file — names are lowercase with hyphens only, no reserved words ("anthropic", "claude"), ≤64 characters, description ≤1024 characters in third person, SKILL.md body ≤500 lines, references one level deep, progressive disclosure — remain in force. The pattern is the "action-oriented" alternative form explicitly permitted by the best-practices guidance, adapted with the `ol-` prefix and shared-domain segment.

The `wiki-editor` agent is exempt only in that it lives in `agents/`, not `skills/`. The `ol-wiki-*` domain is reserved for any future Claude Desktop wiki-management skills (none required for the initial build).

---

## Commit convention

Phase commits: `feat: phase-<n> <deliverable>`.

Examples:
- `feat: phase-0 bootstrap scaffold`
- `feat: phase-1 wiki seed from canonical sources`
- `feat: phase-3 pilot vertical slice for P4 Posting Memo`

Subsequent (post-pilot) work uses normal Conventional Commits prefixes (`feat:`, `fix:`, `docs:`, `refactor:`).

---

## Repository layout

```
dl-skills-library/                     # repo root (the "Overland UW Library")
├── CLAUDE.md                          ← this file
├── README.md
├── progress.json                      ← build-state tracker
├── docs/
│   ├── sources/                       ← Overland deck PDF + Arrakis blueprint
│   ├── anthropic/                     ← prompting, skills, agent-teams best-practices
│   └── pilot-validation.md            ← created in Phase 4
├── raw/                               ← flat. No subfolders. Maintainer drop zone.
├── wiki/
│   ├── WIKI-SCHEMA.md                 ← page format, conventions, lint rules
│   ├── index.md                       ← master catalog
│   ├── log.md                         ← append-only operation log
│   └── <category>/                    ← created on first page write
├── agents/
│   └── wiki-editor/CLAUDE.md          ← sole specialist agent for the initial build
├── skills/                            ← pilot skill added in Phase 3
├── prompts/                           ← pilot prompt added in Phase 3
├── system-instructions/               ← empty in initial build
├── project-instructions/              ← pilot stage instruction added in Phase 3
├── schemas/                           ← pilot Pydantic schema added in Phase 3
├── dist/                              ← empty in initial build
└── scripts/
    └── wiki-check.sh                  ← detect unprocessed raw/ files
```
