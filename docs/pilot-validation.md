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

**Artifact:** `skills/dl-compcert-review/SKILL.md` (plus two reference files)

### Sub-checks

| Sub-check | Verdict | Evidence |
| --- | --- | --- |
| YAML frontmatter `name` is lowercase + hyphens, ≤64 chars | PASS | `dl-compcert-review` (18 chars). Verified by regex against the file. |
| `name` does not contain reserved words ("anthropic", "claude") | PASS | Verified. |
| `name` follows the `dl-<domain>-<action-or-subtype>` convention | PASS | Domain `compcert`, action `review`. See `wiki/methodology/skill-naming-convention.md`. (Superseded the earlier gerund-form sub-check; the file was renamed and re-validated against the current convention.) |
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

# Push-2 Validation — `dl-ddq-kickoff` Kick-Off Data Requests Bundle

**Deliverable:** Stage 2 / P3 Kick-Off Data Requests four-artifact bundle
**Pattern:** generate-with-review over a deterministic period-math core
**Arrakis target app:** Foldspace screening application (same app as the P4 pair)
**Validated:** 2026-05-15
**Validator:** Claude Code session, executing the push-2 plan build sequence
**Execution environment note:** unlike the P17 pilot (markdown-only, no scripts),
this bundle ships two executable scripts, so validation is **execution-based**,
not inspection-only. Python 3.12 + python-docx 1.2.0 + pydantic were installed
locally so the scripts, the schema, and the generated `.docx` could be run and
inspected for real. Evaluation harnesses are retained under the skill's
`_evaltmp/` during the build and removed before commit (they are scratch, not
shipped artifacts).

## Overall verdict

**PASS** — all four artifact checks pass and all three functional evaluations
pass, with the period engine and population mechanic verified by execution.

| # | Check | Verdict |
| --- | --- | --- |
| 1 | Prompt — cache-stable system prefix, semantic XML inputs, outbound redaction line | PASS |
| 2 | Skill — best-practices conformance, scripted/text degrees-of-freedom split | PASS |
| 3 | Project instruction — amended (not duplicated), P3 row + compiled IK embed | PASS |
| 4 | Pydantic schema — parses, instance constructs, projection drives the script with no drift | PASS |
| 5 | `compute_periods.py` — deterministic, FYE-aware, edge-handled (executed) | PASS |
| 6 | `populate_kickoff.py` — in-place, styles/numbering/footnotes preserved (executed) | PASS |
| 7 | Three functional evaluations | PASS |

## Check 1 — Prompt

**Artifact:** `prompts/stage-2-screening/P3-kickoff-data-requests.md`

Cache-eligible system prefix runs `# System` → `# Output Contract`; variable
inputs follow in semantic XML (`<system_date>`, `<sector_classification>`,
`<teaser>`, `<email_color optional>`, `<desktop_research optional>`,
`<pitchbook_excerpt optional>`, `<fiscal_year_end optional>`,
`<existing_lender_status optional>`, `<history_years optional>`,
`<forecast_horizon optional>`). The prompt mirrors — does not re-specify — the
skill. Because the artifact is **outbound to the borrower/debt advisor**, the
*Classification and review* section carries an explicit outbound redaction
checklist line (per [[restricted-content-discipline]]) and the D-2 watermark
carve-out. `[INSUFFICIENT DATA — sector classification not provided]` handling
is explicit. A `<thinking>` allowance is permitted and explicitly excluded from
the `.docx`. **PASS.**

## Check 2 — Skill

**Artifact:** `skills/dl-ddq-kickoff/SKILL.md` (+ 2 reference files, 2 scripts)

`name` = `dl-ddq-kickoff` (14 chars, lowercase+hyphens, no reserved words,
matches the `dl-<domain>-<action>` convention; `ddq` domain pre-exists in the
registry — no CLAUDE.md edit). `description` third-person, 962 chars (≤1024,
both what + when). Body 223 lines (≤500). References one level deep
(`reference/kpi-frameworks.md`, `reference/population-mechanics.md`), both with
a Contents ToC. Forward slashes only (the single backslash is a shell
line-continuation in a bash code block, not a path). No `wiki/`/`docs/` path
leakage. Degrees-of-freedom split is explicit and correct: low (scripted)
period math + population, deterministic standard set, high (text + worked
examples) borrower-KPI block — matching `Skills_Best_Practices.md`. Anti-patterns
section present. **PASS.**

## Check 3 — Project instruction

**Artifact:** `project-instructions/stage-2-screening.md` (amended, not duplicated)

One PI per stage preserved. The P3 active-deliverables row now maps to
`dl-ddq-kickoff`; the post-table narrative and fragmentation watchpoint were
updated (P3 now has one lightweight skill; the databook row stays a future
placeholder). Behavioral rule 1 generalized to the P3+P4 `.docx` D-2 carve-out;
rule 5 gained the **P3 outbound exception** (the kick-off is borrower-facing →
outbound redaction checklist applies, distinct from the internal P4 outputs);
rule 7 adds `schemas/kickoff_data_request.py`. A new compile-dated IK embed
(*kick-off downstream-pre-seeding map*, compiled 2026-05-15) inlines the
request → downstream-field map so the PI runs in Claude Desktop with no
filesystem access. Summary updated. **PASS.**

## Check 4 — Pydantic schema

**Artifact:** `schemas/kickoff_data_request.py`

Parses cleanly; an instance with `KickoffPeriods` + `KpiRequest` children
constructs. snake_case, JSON-serializable primitives, explicit required/optional,
one-line field descriptions, `schema_version: int = 1`, HITL defaults
(`review_state: Literal["PENDING_REVIEW"]`, `requires_human_review = True`).
Module docstring names P3 / Foldspace screening app / `SCREENING_LAND` tier /
`PENDING_REVIEW` and documents the **projection** to the `populate_kickoff.py`
content dict. Cross-validation (`_evaltmp/xval.py`): the documented projection
of a constructed instance was written to JSON and fed to `populate_kickoff.py`,
which exited 0 — every script-consumed key resolves with no drift; provenance
fields (`naics_code`, `gics_*`, per-KPI `rationale`/`downstream_target`) are
Arrakis-side capture the script does not read, and are genuinely emitter-produced
(not aspirational). **PASS.**

## Check 5 — Period engine (executed)

`compute_periods.py` self-tested across the three eval system dates and edges:

| Input | audited | LTM | quarter | budget | forecast |
| --- | --- | --- | --- | --- | --- |
| 2026-05-28, calendar | FY'23-'25 | 3/26 | Q1'26 | FY'26 | FY'26-'30 |
| 2026-05-28, FYE 03-31 | FY'24-'26 | 3/26 | Q4'26 | FY'27 | FY'27-'31 |
| 2026-01-15, hist=1 | FY'24 | 9/25 | Q3'25 | FY'25 | FY'25-'29 |

The 30-day close buffer, non-calendar FYE quarter labeling, `history_years=1`
single-FY form, and invalid-date / invalid-FYE inputs (exit 2 with explicit
messages, no punt) all behave correctly. **PASS.**

## Check 6 — Population mechanic (executed)

`populate_kickoff.py` output inspected at the OOXML level:

- The seven standard lines are rewritten from the period fragments; both
  footnote references (`w:id="1"` on the LTM line, `w:id="2"` on the Mgmt. KPI
  line) survive and stay bound to their paragraphs.
- All inserted stock-cut and borrower-KPI bullets carry `pStyle Bullet2`; the
  three `NumberList1` headers and `numId 9` numbering are untouched.
- `compliance_cert_applicable=false` suffixes ` — N/A (no existing reporting
  facility)`; the line is never deleted.
- Header `Company Name`/`Sponsor` placeholders substituted; `owner=None`
  removes the `(Sponsor)` parenthetical; the cached DATE value is refreshed.
- `MAX_KPI_LINES=14` raises a verbose, overflow-listing error (exit 2) when
  exceeded.
- The output opens cleanly as a valid package via python-docx. **PASS.**

## Check 7 — Functional evaluations

| Eval | Scenario | Expected | Result |
| --- | --- | --- | --- |
| 1 | Residential HVAC roll-up, post-NDA, 5/28/2026, calendar FYE | FY'23-'25 + Q1'26; compliance active; add-on cohort + consideration lines; HVAC KPI block (membership/agreements, technician utilization, 4-wall by branch) | PASS |
| 2 | Vertical SaaS, no existing debt, calendar FY | compliance line N/A; no add-on cohort block; KPI block shifts to ARR/NRR/GRR, CAC payback, logo concentration; `owner=None` drops parenthetical | PASS |
| 3 | Industrials mfr, non-calendar FYE 3/31, existing BSL | FYE-aware labels (audited FY'24-'26, quarter **Q4'26**, budget FY'27); compliance active; backlog/book-to-bill + raw-material pass-through KPI cuts | PASS |

## Portability assessment

The bundle graduates into the Arrakis Foldspace screening application without
rewrite: `KickoffDataRequest` registers as the structured-output validator and
the `SCREENING_LAND` data-product schema; the stable prompt prefix is the
Spice-brokered cache-eligible portion; `<sector_classification>` /
`<system_date>` map to MCP tool calls; the D-2 watermark maps to the rendered
review banner with `review_state: "PENDING_REVIEW"`; `[INSUFFICIENT DATA — …]`
emissions feed the Observatory quality dimension. The two scripts carry through
unchanged. No artifact needs rewriting to graduate.

## Recommendation

`dl-ddq-kickoff` is ready for use in Claude Desktop by the deal team for the P3
post-NDA kick-off data request. It is the upstream feed for the P4 posting-memo
pair: P3 → returned data → `dl-memo-posting` + `dl-memo-posting-backup`.

---

*End of report.*
