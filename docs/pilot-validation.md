# Pilot Self-Validation Report

**Pilot phase:** P17 Compliance Certificate Parser (Stage 6 — Asset Management)
**Pattern:** extract-and-validate
**Arrakis target app:** A12 Corrino
**Validated:** 2026-05-13
**Validator:** Claude Code session, applying the Phase 4 protocol from the build prompt

---

## Overall verdict

**PASS** — all four required checks pass with no blocking remediation. Two minor notes are recorded under *Observations* for follow-on iteration.

| # | Check | Verdict |
| --- | --- | --- |
| 1 | Pilot prompt — completeness, cache-stable system prefix, semantic XML inputs | PASS |
| 2 | Pilot skill — best-practices conformance and Claude Desktop runnability | PASS |
| 3 | Pilot project instruction — inline embedded knowledge, no filesystem access | PASS |
| 4 | Pydantic schema — parses cleanly, matches the prompt's structured output | PASS |

---

## Check 1 — Pilot prompt

**Artifact:** `prompts/stage-6-asset-management/P17-compliance-certificate-parser.md`

### Sub-checks

| Sub-check | Verdict | Evidence |
| --- | --- | --- |
| Stable cache-eligible system prefix appears first | PASS | `# System` at line 9, `# Output Contract` at line 42; the cache-eligible portion runs through line 90 (everything before `# Variable Inputs`). |
| Variable inputs separated from system prefix | PASS | `# Variable Inputs` at line 91. Inputs wrapped in semantic XML tags. |
| Semantic XML tags for inputs | PASS | `<facility_metadata>`, `<credit_agreement_excerpts>`, `<compliance_certificate>`, `<prior_period_certificate optional="true">` |
| Brief `<thinking>` allowance, not in output | PASS | "Brief thinking allowance" subsection at end; explicitly states the reasoning block is stripped before submission. |
| `[INSUFFICIENT DATA — <what is missing>]` marker | PASS | 6 mentions in the prompt; explicit handling in the *Uncertainty handling* section for three distinct cases (illegible certificate, missing covenant definition, insufficient inputs to recompute). |
| `[DRAFT — HUMAN REVIEW REQUIRED]` watermark on output | PASS | Output Contract specifies the watermark line outside the JSON, immediately preceding it. |
| Handoff line | PASS | "AM reviewer to verify flagged items and either approve, request revision, or escalate." (specified verbatim in Output Contract). |
| Long-context-first ordering | PASS | The variable inputs (long: full certificate + agreement excerpts) appear after the system prefix per the long-context guidance in `Prompting_Best_Practices.md`. The output contract anchors expectations *before* the inputs are sent, which is the intended cache-stability optimization. |
| Quote-grounded retrieval discipline | PASS | The prompt instructs the model to cite credit-agreement section numbers (`Section 7.10(a)`) for every covenant definition. |
| No prefilled responses (deprecated 4.6+) | PASS | The prompt does not rely on assistant prefilling; structured output is requested via the schema in the contract. |
| Classification handling | PASS | The prompt explicitly identifies the output as internal-AM-facing (CONFIDENTIAL, possibly RESTRICTED context) and notes that the redaction checklist for external-facing artifacts does not apply. |

### Verdict

**PASS** — the prompt is well-formed, cache-stable, semantically tagged, and explicitly handles uncertainty, watermarking, and classification.

---

## Check 2 — Pilot skill

**Artifact:** `skills/ol-compcert-review/SKILL.md` (plus two reference files)

### Sub-checks

| Sub-check | Verdict | Evidence |
| --- | --- | --- |
| YAML frontmatter `name` is lowercase + hyphens, ≤64 chars | PASS | `ol-compcert-review` (18 chars). Verified by regex against the file. |
| `name` does not contain reserved words ("anthropic", "claude") | PASS | Verified. |
| `name` follows the `ol-<domain>-<action-or-subtype>` convention | PASS | Domain `compcert`, action `review`. See `wiki/methodology/skill-naming-convention.md`. (Superseded the earlier gerund-form sub-check; the file was renamed and re-validated against the current convention.) |
| `description` is third-person | PASS | "Extracts...", "Produces...", "Use when..." — no first or second person. |
| `description` ≤1024 chars | PASS | 574 characters (verified by Python script). |
| `description` includes both "what" and "when" | PASS | What: "Extracts covenant metrics from borrower compliance certificate PDFs, recomputes them..." When: "Use when reviewing a quarterly or monthly compliance certificate, validating covenant calculations against the credit agreement, or preparing the AM portfolio monitoring update." |
| Body ≤500 lines | PASS | 121 lines (verified). |
| References one level deep | PASS | `reference/covenant-types.md` and `reference/cfo-error-patterns.md` — both directly under the skill folder, no nested references. |
| Forward slashes in paths | PASS | No backslashes (verified by grep). |
| No filesystem-path leakage to the broader repo | PASS | No `wiki/`, `docs/sources/`, `docs/anthropic/`, `raw/`, or `.git` references in the SKILL body. |
| Self-contained for Claude Desktop | PASS | The "What you need before invoking" section explicitly enumerates the four uploaded inputs. The skill executes entirely from documents in the user's project. |
| Workflow has clear sequential steps with checklist | PASS | 6-step workflow: Parse → Locate definitions → Recompute → Compare → Flag → Assemble. Checklist provided for the model to copy into its working response. |
| Reference files have a Contents/ToC for files >100 lines | PASS | Both reference files include a Contents section near the top. `covenant-types.md` is 99 lines (under threshold but ToC included anyway); `cfo-error-patterns.md` is 122 lines with ToC. |
| Anti-patterns section | PASS | Explicit "Anti-patterns" subsection enumerates what the skill must not do. |
| No time-sensitive content | PASS | No date-dependent guidance; covenant taxonomy is durable. |
| Consistent terminology | PASS | "compliance certificate", "covenant", "credit agreement", "recompute" used consistently throughout. |

### Verdict

**PASS** — the skill conforms to every checklist item in `Skills_Best_Practices.md` § "Checklist for effective Skills" that applies to a markdown-only Skill (the code-and-scripts checklist items are not applicable since this skill carries no executable scripts).

---

## Check 3 — Pilot project instruction

**Artifact:** `project-instructions/stage-6-asset-management.md`

### Sub-checks

| Sub-check | Verdict | Evidence |
| --- | --- | --- |
| Header with stage name, phase range, purpose | PASS | "Stage 6 — Asset Management · P17–P19 · Purpose..." block at the top. |
| Deal-context slot (filled at deal kick-off) | PASS | Eight-field slot covering company, GICS, LTM EBITDA with source, facility structure, current IC status, model version + lock status, QoE status, active document index — all per spec. |
| Active deliverables for the stage | PASS | Table mapping each phase deliverable to its skill, with cadence. The pilot skill is wired in; future-skill placeholders are explicitly marked. |
| Behavioral rules for the stage | PASS | Eight numbered rules covering watermark, INSUFFICIENT DATA, citation discipline, classification, HITL state, schema validation, trend cross-check, and audit readiness. |
| Artifact versioning convention | PASS | `[COMPANY]-[DELIVERABLE]-v[N]-[YYYYMMDD]` with three concrete examples. Date semantics specified ("date is the period being acted on, not the date of action"). |
| Institutional Knowledge section at top with 3–5 wiki pages embedded inline | PASS | Four wiki pages embedded inline with compiled date 2026-05-13: closing-and-asset-management, ic-and-asset-mgmt-gaps, hitl-state-machine, data-classification-tiers. Each compiled section is fully self-contained — the Claude Desktop user does not need to access the wiki. |
| Compile-date marker present | PASS | Each of the four embedded sections carries an explicit `*Compiled from <wiki path> — last updated 2026-05-13.*` line. |
| Runs without filesystem access | PASS — see note | The compiled content is fully inlined; the project instruction is operationally self-contained. The wiki path strings in the provenance markers are metadata for traceability, not navigation paths the user must resolve. See Observations 1. |

### Verdict

**PASS** — the project instruction is operationally self-contained for a Claude Desktop user, embeds four institutional-knowledge pages inline with compile-date markers, and specifies the deal-context slot, deliverables, behavioral rules, and versioning convention.

---

## Check 4 — Pydantic schema

**Artifact:** `schemas/compliance_certificate_validation.py`

### Sub-checks

| Sub-check | Verdict | Evidence |
| --- | --- | --- |
| Schema parses cleanly | PASS | `import` succeeds; example instance constructible with all required fields populated. |
| Field names use snake_case | PASS | All 11 outer fields and 12 inner fields use snake_case. |
| Types are JSON-serializable Python primitives | PASS | `str`, `int`, `float`, `bool`, `date`, `Literal[...]`, `list[CovenantCalculation]`. |
| Required-vs-optional explicit at field level | PASS | Required fields use `Field(..., description=...)`; optional fields use either `Field(None, description=...)` or `Field(default_factory=list, ...)`. |
| One-line description per field | PASS | Every field carries a `description=` argument. |
| Only fields the prompt actually produces | PASS | The schema's outer 11 fields and inner 12 fields all appear in the prompt's Output Contract JSON template. No aspirational fields. |
| Schema version declared | PASS | `schema_version: int = Field(1, ...)` — Arrakis envelope evolution path explicit from day one. |
| HITL state defaults to PENDING_REVIEW | PASS | `review_state: Literal["PENDING_REVIEW"] = Field("PENDING_REVIEW", ...)` and `requires_human_review: bool = Field(True, ...)`. |
| Module docstring documents lifecycle phase, Arrakis target, landing tier | PASS | Module docstring names: schema version 1, lifecycle phase P17, Arrakis app A12 Corrino, landing tier `ARRAKIS_RAW.CORRINO_LAND.compliance_certificate_validations`, HITL state at output. |

### Cross-validation against prompt Output Contract

Every field in the prompt's `# Output Contract` JSON template appears in the schema with the same name and the same type. The reverse is also true: every schema field appears in the prompt's Output Contract. No drift between the two artifacts.

### Verdict

**PASS** — the schema parses, an example instance constructs cleanly, and the schema mirrors the prompt's Output Contract exactly.

---

## Observations (non-blocking notes for follow-on iteration)

### Observation 1 — Provenance markers in the project instruction

The four `*Compiled from wiki/<path>.md*` lines in the embedded sections of `project-instructions/stage-6-asset-management.md` mention internal repo paths. This is acceptable per the spec ("Mark the embedded pages and their compile date") because:

- The compiled content is fully inlined directly below each marker.
- The marker is provenance metadata, not a navigation instruction.
- A Claude Desktop user can operate the project instruction end-to-end without resolving the path.

However, a future iteration may consider replacing the wiki-path metadata with a content-hash or a wiki-version identifier, which would carry the same traceability value without any path-string in the distribution-environment artifact. This is a stylistic refinement, not a conformance gap.

### Observation 2 — Reference file size threshold

`Skills_Best_Practices.md` recommends a Contents section for reference files longer than 100 lines. `covenant-types.md` is 99 lines (just under the threshold) and `cfo-error-patterns.md` is 122 lines. Both files include a Contents section anyway, which is fine. If `covenant-types.md` grows past 100 lines in a follow-on iteration, the Contents section is already in place.

### Observation 3 — Skill / prompt schema reference

The skill mentions "the `ComplianceCertificateValidation` schema" by name. The schema is in `schemas/compliance_certificate_validation.py` in this repo. In Claude Desktop, the user does not have access to the Python file — but they do have the prompt, which fully specifies the schema inline in its `# Output Contract` section. The skill's reference to "the schema" resolves to the prompt's Output Contract. This is intentional and operational, but a follow-on iteration may consider making the skill carry an inline JSON schema specification as well, so a user reading only the skill can fully understand the output structure without also opening the prompt.

---

## Portability assessment (for the eventual graduation into Arrakis)

The pilot artifacts are constructed so they graduate into the A12 Corrino "Compliance Certificate Parser" feature without rewriting. Specifically:

- The **Pydantic schema** is registerable in the prompt library and the DCA as the structured-output validator, with the module docstring naming the landing tier.
- The **prompt's stable system prefix** is the cache-eligible portion that Spice will broker.
- The **prompt's variable XML inputs** map to MCP tool calls in the production binding (`get_facility_terms`, `extract_financial_data`, `get_document` for the certificate, `get_document` for the prior-period cross-check).
- The **HITL `[DRAFT — HUMAN REVIEW REQUIRED]` watermark** maps to the rendered "AI Draft — Pending Review" banner on Corrino's review UI; the schema's `review_state: "PENDING_REVIEW"` is the corresponding state-machine state.
- The **`[INSUFFICIENT DATA — <what>]`** uncertainty markers feed the Foldspace Observatory's LLM quality dimension (rate of insufficient-data emissions per `prompt_id`).

No artifact in the pilot needs rewriting to graduate. The skill body itself stays in Claude Desktop (Arrakis end users use the Corrino UI, not Claude Desktop directly), but the skill's reference materials (`covenant-types.md`, `cfo-error-patterns.md`) lift directly into the Reverend Mother / Corrino prompt library as task-specific reference documents.

---

## Recommendation

The pilot is ready for use in Claude Desktop by the asset management team for P17 compliance certificate validation. The construction pattern (skill + prompt + project instruction + Pydantic schema, HITL-watermarked, [INSUFFICIENT DATA]-aware, Arrakis-portable) is validated and can be replicated for follow-on phases.

**Recommended next builds**, in order of leverage (per [[ic-and-asset-mgmt-gaps]] and [[opportunity-register]] in the wiki):

1. **P17 RCF / DDTL draw verification** — closes the related "DDTL draws approved over email; no compliance verification tracked" pain point. Same extract-and-validate pattern, smaller scope.
2. **P18 mark-to-market triage** — closes the "manual Excel mark-to-market valuations" pain point. Generate-with-review pattern (different shape from the pilot — exercises the second of the three opportunity shapes).
3. **P4 posting memo draft** — the originally-recommended pilot. Generate-with-review pattern with bounded upstream context. High-frequency phase.

Each follow-on uses the same construction pattern proven by this pilot.

---

*End of report.*
