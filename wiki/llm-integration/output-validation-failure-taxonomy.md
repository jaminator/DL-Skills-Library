---
title: Output Validation Failure Taxonomy
category: llm-integration
tags: [llm-integration, governance, process]
sources:
  - arrakis_blueprint_v2_3.md
last_updated: 2026-05-13
---

# Output Validation Failure Taxonomy

Spice classifies every Claude response into one of **five disposition categories** before returning it to the calling app. Each category has a detection method, a disposition policy, and a maximum retry count. The taxonomy is the operational rulebook that decides whether a response is retried, surfaced to a reviewer with a special banner, or returned to the calling app as an error. See [[spice-llm-service]] for how the taxonomy fits into the broader brokering contract.

## The five modes

| Mode | Detection | Disposition | Max retries |
| --- | --- | --- | --- |
| **Empty response** | Response body has no content blocks, or all blocks empty. | Automatic retry with the same prompt. | 2 |
| **Malformatted output** | Not parseable as JSON when structured output was requested, **or** Pydantic raises `ValidationError` on a non-nullable required field. | Automatic retry with an appended instruction: "Your previous response was malformatted. Return valid JSON matching the schema." | 2 |
| **Truncated output** | `stop_reason = max_tokens` rather than `end_turn`. | If the task supports chunked generation (e.g., section-by-section memo drafting), issue a continuation request. Otherwise, automatic retry with `max_tokens` increased by 50% up to the model's context limit. | 1 |
| **Schema-valid but semantically degenerate** | Pydantic passes but a task-specific sanity check (registered per `task_type` as a `min_quality_spec` JSON column in the `prompt_library` table) fails. Example: extracted NDA metadata returns zero non-null fields; covenant narrative is < 50 characters. | Route to human review with a distinct **"AI Draft — Low Confidence"** banner (different from the standard "AI Draft — Pending Review" banner). | 0 |
| **API error (non-retryable)** | 4xx errors excluding 429. | Return a structured error to the calling app. Log to the audit trail with `validation_result = 'api_error'`. | 0 |

The success path — well-formed structured output that passes both Pydantic validation and the `min_quality_spec` sanity check — flows into [[hitl-state-machine]] as `AI_DRAFT → VALIDATION_PASSED → PENDING_REVIEW`.

## The two distinct review banners

The taxonomy produces two reviewer-facing states that look superficially similar but carry different semantics:

- **`PENDING_REVIEW`** — "AI Draft — Pending Review." Standard success path. The output validated, the schema parsed, the sanity check passed. The reviewer's job is to verify content correctness and approve / revise / reject.
- **`LOW_CONFIDENCE`** — "AI Draft — Low Confidence." Sub-state of `PENDING_REVIEW` driven by the schema-valid-but-degenerate mode. The output passed Pydantic but the per-task sanity check failed. The reviewer is being asked: "Should this output exist at all, or is this a sign the underlying inputs were too thin?"

Both states share the `PENDING_REVIEW` row in the state machine but render differently in the calling app's UI. The library's `[DRAFT — HUMAN REVIEW REQUIRED]` watermark maps to the standard banner; the low-confidence variant is platform-rendered only.

## Audit trail records

Every retry attempt logs to the AI Output Audit Trail with `validation_result` reflecting the failure mode and the retry sequence number. The final disposition — success after retry, escalation to human, or hard failure — is recorded in the same field on the terminal record. Retry token costs are attributed to the originating `app_id` and `deal_id` so the cost of a "noisy" prompt is visible without re-aggregation.

The disposition-category distribution is one of the Observatory's standing LLM-quality views: a sudden spike in `malformatted_output` for a given `prompt_id` is a leading indicator that an upstream context source has changed shape, or that the prompt's output schema and instruction text have drifted apart.

## What this means for the library

A prompt drafted in this development environment is built so the taxonomy works for it without modification:

- A clear, single JSON output specification so **Empty response** and **Malformatted output** are crisp signals, not ambiguous edge cases.
- Pydantic-validated structured output so **Malformatted output** detection runs the same validator locally and in Spice.
- An explicit `min_quality_spec` (described in the prompt body and in the schema docstring) so the **Schema-valid but degenerate** check has criteria to apply when the prompt graduates into the platform.
- An explicit `[INSUFFICIENT DATA — <what is missing>]` marker so partial information is preferred over silent omission — keeping the response valid under the structural check while still flagging the gap.

The taxonomy is what makes "fail loudly, never silently" a property of the platform.

## Related Concepts

- [[spice-llm-service]] — the broker that applies the taxonomy
- [[hitl-state-machine]] — the review states the success path enters
- [[prompt-versioning-governance]] — how `min_quality_spec` is registered per task
- [[library-artifact-bundle]] — how this library packages outputs to clear the taxonomy

## Sources

- `arrakis_blueprint_v2_3.md`, Section 7 — LLM Output Failure Taxonomy and Output Validation
