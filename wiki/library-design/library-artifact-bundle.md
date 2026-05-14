---
title: Library Artifact Bundle
category: library-design
tags: [architecture, process, template, governance]
sources:
  - arrakis_blueprint_v2_3.md
  - Overland_Deal_Lifecycle_Automation_051326_vJA.pdf
last_updated: 2026-05-13
---

# Library Artifact Bundle

Every productive unit of work in this library is a **four-artifact bundle**: a skill, a prompt, a project instruction, and a Pydantic schema. Each carries the `[DRAFT — HUMAN REVIEW REQUIRED]` watermark on outputs intended for review, marks gaps with `[INSUFFICIENT DATA — <what is missing>]`, and is constructed so it graduates into [[arrakis-overview]] without rewriting. The bundle is the operational meaning of the **portability principle**.

The pattern was proven by [[compliance-certificate-parser-pilot]] and is the reusable template for every follow-on build.

## The four artifacts

### 1. Skill — the procedural workflow

A markdown file at `skills/<gerund-name>/SKILL.md` that tells Claude **how** to perform the task. Conforms to `docs/anthropic/Skills_Best_Practices.md`:

- Frontmatter `name` is lowercase + hyphens, ≤64 chars, gerund form.
- `description` is third-person, ≤1024 chars, names both **what** and **when**.
- Body ≤500 lines. Anti-patterns section explicit. References one level deep.
- No filesystem-path leakage. Self-contained for a Claude Desktop user.

Reference files (taxonomies, error patterns) live under `skills/<name>/reference/` with a Contents section when ≥100 lines.

### 2. Prompt — the cache-stable instruction

A markdown file at `prompts/<stage>/<phase>-<task>.md` with two zones:

- **System prefix** (cache-eligible). Role, approach, uncertainty handling, classification, output contract. Stable across invocations so [[spice-llm-service]] can cache it.
- **Variable inputs** (per-invocation). Semantic XML tags: `<facility_metadata>`, `<credit_agreement_excerpts>`, `<compliance_certificate>`, etc.

Anything per-invocation lives **below** the system prefix; anything stable lives **above** it. In Claude Desktop the user composes inputs manually; in Arrakis, Spice fills them from MCP tool calls (see [[mcp-tool-catalog]]). The Output Contract sits inside the system prefix **before** the inputs so the model knows what it is producing as it reads.

### 3. Project instruction — the stage-level context pinning

A markdown file at `project-instructions/<stage>.md` that fixes the stage's deal context and behavioral rules:

- Header with stage name, phase range, purpose.
- **Deal-context slot** filled at deal kick-off: company, GICS, LTM EBITDA, facility structure, IC status, model version, QoE status, document index.
- Active deliverables table mapping each phase deliverable to its skill, with cadence.
- Behavioral rules: watermark, `[INSUFFICIENT DATA]`, citation discipline, classification, HITL state, schema validation, audit readiness.
- Artifact versioning: `[COMPANY]-[DELIVERABLE]-v[N]-[YYYYMMDD]`.
- **Institutional Knowledge section** embedding 3–5 wiki pages inline with compile-date markers so the project instruction runs without filesystem access.

### 4. Pydantic schema — the structured-output contract

A Python file at `schemas/<task>.py`:

- Field names **snake_case** (Snowflake convention).
- Types JSON-serializable primitives (`str`, `int`, `float`, `bool`, `date`, `Literal`, `list`).
- Required vs. optional explicit at the field level.
- One-line `description=` per field; no aspirational fields.
- `schema_version: int = Field(1, ...)` for explicit evolution path.
- HITL defaults: `review_state: Literal["PENDING_REVIEW"]`, `requires_human_review: bool = True`.
- Module docstring names lifecycle phase, Arrakis target, landing tier, HITL state at output.

Cross-validate: every JSON template field appears in the schema and vice versa. No drift.

## Watermarks and uncertainty

Every output intended for IC, legal, co-lender, or AM review carries the literal text `[DRAFT — HUMAN REVIEW REQUIRED]` at the top. The watermark maps to the `PENDING_REVIEW` state in [[hitl-state-machine]]; it is removed only on `APPROVED`. Reviews discard outputs missing it.

The only acceptable uncertainty marker is `[INSUFFICIENT DATA — <what is missing>]`. Never silently omit; never fabricate. The Observatory tracks emission rates as a leading indicator of upstream-data degradation or prompt drift.

## Classification and external-facing discipline

Every bundle declares its intended consumer (`<consumer>ic</consumer>`, `<consumer>asset-management</consumer>`, `<consumer>co-lender</consumer>`, `<consumer>lp</consumer>`). External-facing prompts (co-lender, LP) include the inline redaction checklist from [[restricted-content-discipline]]. Internal-facing prompts omit it. The classification is enforced by [[data-classification-tiers]].

## Why this matters — the portability principle

The bundle is constructed once and runs in two environments without rewriting:

- **Claude Desktop today.** A maintainer copies the project instruction into the project, uploads the skill and reference files, and invokes the prompt with manually-pasted inputs. The watermark appears in the output for the human reviewer.
- **Arrakis tomorrow.** The prompt enters the [[prompt-versioning-governance]] library. Spice brokers the call, fills the XML inputs from MCP tools, applies the [[output-validation-failure-taxonomy]], and lands the structured output in `<APP>_LAND` of the [[snowflake-medallion]]. The watermark becomes the rendered review banner; the schema becomes the DCA contract.

Same artifacts, different runtimes. That is the portability principle made operational.

## Related Concepts

- [[compliance-certificate-parser-pilot]] — concrete instance of the bundle
- [[opportunity-shapes]] — the three shapes that determine which artifact dominates
- [[hitl-state-machine]] — review states the watermark maps to
- [[spice-llm-service]] — the broker the bundle graduates to
- [[restricted-content-discipline]] — external-facing redaction obligation

## Sources

- `arrakis_blueprint_v2_3.md`, Section 7 — LLM Integration Layer Architecture
- `Overland_Deal_Lifecycle_Automation_051326_vJA.pdf`, slide 09 (foundation controls), slide 06 (opportunity shapes)
