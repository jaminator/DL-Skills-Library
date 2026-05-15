---
title: HITL Review State Machine
category: llm-integration
tags: [llm-integration, governance, process]
sources:
  - arrakis_blueprint_v2_3.md
last_updated: 2026-05-15
---

# HITL Review State Machine

Every LLM-generated output in Arrakis flows through a **mandatory human-review gate** before any consequential action. The HITL (Human-In-The-Loop) state machine defines the eight states a draft passes through, the transitions allowed between them, and the audit record persisted at each terminal state. This is the operational mechanism that makes "Claude drafts; humans decide" a property of the platform.

## The eight states

```
AI_DRAFT → VALIDATION_PASSED → PENDING_REVIEW → IN_REVIEW
                                                    │
                ┌───────────────────────────────────┼───────────────────┐
                ▼                                   ▼                   ▼
           APPROVED                            REJECTED          REVISION_REQUESTED → AI_DRAFT
                                                    │                                  (new draft, parent_draft_id link)
                                                    ▼
                                                ESCALATED
```

| State | Meaning |
| --- | --- |
| **AI_DRAFT** | Spice has just returned a response. |
| **VALIDATION_PASSED** | Pydantic validation succeeded. Failure routes to the disposition policy (retry, low-confidence banner, or hard error). |
| **PENDING_REVIEW** | Surfaced in the calling app's UI with the `[DRAFT — HUMAN REVIEW REQUIRED]` (or "AI Draft — Pending Review") banner. **This is the state the library's watermark maps to.** |
| **IN_REVIEW** | A reviewer has opened the draft. `reviewer_id` and `review_started_at` are recorded. |
| **APPROVED** | Terminal. Reviewer accepted the draft (with or without edits). |
| **REJECTED** | Terminal. Reviewer discarded the draft. `rationale` required. |
| **REVISION_REQUESTED** | Reviewer wants a re-draft. Returns to Spice with reviewer annotations attached as additional context; produces a new `AI_DRAFT` with a `parent_draft_id` link. |
| **ESCALATED** | Reviewer routes to a senior reviewer. Terminal at the original level. `rationale` required. |

## Override audit record

When a reviewer **edits** the AI-generated output before approval, the system persists an override audit record:

```python
class HITLOverrideRecord(BaseModel):
    draft_id: str
    reviewer_id: str
    review_state: str                 # Terminal state (APPROVED, REJECTED, ESCALATED)
    sections_modified: list[str]      # Section identifiers the reviewer changed
    edit_magnitude: str               # MINOR | MODERATE | MAJOR
    rationale: str | None             # Required for MAJOR edits and all REJECTED / ESCALATED
    reviewed_at: datetime
```

Override records flow through the standard Bronze → Silver → Gold pipeline as part of the AI output audit trail and are aggregated by the Foldspace Observatory for **drift detection**. If the MAJOR override rate for a given `prompt_id` exceeds 20% over a rolling 30-day window, Spice emits a `data-quality.sla-breach` event and the prompt is flagged for platform review.

## The watermark this library uses

In Claude Desktop (and in any environment where Spice is not orchestrating the flow), the library embeds a literal text watermark `[DRAFT — HUMAN REVIEW REQUIRED]` at the top of every IC-facing, legal, co-lender-facing, or AM-facing artifact. This watermark is the manual analog of the `PENDING_REVIEW` state — when the artifact graduates into Arrakis, the watermark is replaced by the rendered banner on the calling app's UI but the semantics are identical.

The watermark is **not optional**. Conformance rule 5 in the root `CLAUDE.md` specifies it; the pilot validation checks for its presence; reviews discard outputs without it.

## What this means for prompt construction

A prompt destined to flow through this state machine carries three explicit features:

1. **A structured output schema.** Pydantic-validated. The output must parse, or the AI_DRAFT → VALIDATION_PASSED transition fails and the disposition policy fires.
2. **A `[DRAFT — HUMAN REVIEW REQUIRED]` watermark in the output template.** The watermark is removed on `APPROVED` only.
3. **An explicit uncertainty marker.** `[INSUFFICIENT DATA — <what is missing>]` (the only acceptable form). Never silently omit; never fabricate. The Observatory's drift detection treats high uncertainty-marker rates as a signal that the underlying data plumbing or the prompt is failing.

## Output quality criteria recorded at review

Every reviewer's terminal action records four scoring fields alongside the override record:

| Criterion | Type | Used for |
| --- | --- | --- |
| Structural completeness | Pass / fail (Pydantic) | Automated quality monitoring |
| Factual consistency | Consistent / inconsistent | Hallucination detection |
| Edit severity | None / minor / major / rewrite | Drift detection |
| Usefulness | Used / discarded | Pattern abandonment detection |

These feed the Observatory's LLM quality dimension on the data observability dashboard.

## Related Concepts

- [[spice-llm-service]] — produces the drafts that enter the state machine
- [[data-classification-tiers]] — classification governs reviewer routing
- [[restricted-content-discipline]] — the redaction obligation at review
- [[output-validation-failure-taxonomy]] — disposition policy when validation fails

## Sources

- `arrakis_blueprint_v2_3.md`, Section 7 — Output Validation and Human-in-the-Loop
