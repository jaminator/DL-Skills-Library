---
title: Spice — Shared LLM Service
category: llm-integration
tags: [llm-integration, architecture, application]
sources:
  - arrakis_blueprint_v2_3.md
last_updated: 2026-05-13
---

# Spice — Shared LLM Service

**Spice** is the FastAPI microservice that wraps the Anthropic API and brokers every Claude API call across the Arrakis suite. **Per-app direct Claude API calls are prohibited.** Centralizing LLM calls is what makes a 14-application platform tractable to operate.

## Why centralize

A single brokering service provides:

- **Centralized cost tracking** and billing attribution by `app_id`, `deal_id`, and `user_id`.
- **Per-app rate budgets** that prevent a single runaway batch job from starving other apps of API capacity.
- **A single point** for model version upgrades — bump the model in Spice, every consumer follows.
- **Uniform input guardrails** (PII detection) and output validation (Pydantic).
- **One audit trail** — every call logged to `ARRAKIS_RAW.APP_EVENTS` with prompt version, token counts, latency, validation result, classification, and edit deltas.

## Resilience profile

| Parameter | Value |
| --- | --- |
| Retry policy | 3 attempts, exponential backoff (1 s / 2 s / 4 s) with jitter, 429 / 5xx only |
| Rate-limit backoff | Respect `Retry-After` header; otherwise 60 s |
| Circuit breaker | Open after 5 consecutive failures within 120 s; half-open after 60 s |
| Per-app rate budget | 60 requests / min default; suite-wide ceiling 200 requests / min |
| Health endpoint | `/health/anthropic` reports breaker state and rate-limit headroom |

When the breaker opens, Spice returns a structured error to the calling app immediately rather than queuing — calling apps must handle this explicitly via their service-layer error policy.

## Token budget framework

Every call is shaped by a token budget enforced per `task_type` in the prompt library:

| Segment | Default Allocation | Notes |
| --- | --- | --- |
| System prompt | ≤ 10% | Role, output format, guardrails. Cache-eligible across tasks of the same type. |
| Retrieved context (RAG) | ≤ 60% | Deal documents, precedent clauses, financial data. Truncated relevance-ranked. |
| Conversation / task input | ≤ 15% | User instructions, prior draft sections. |
| Output reservation | ≥ 15% | Sets `max_tokens`. Long-form drafting may bump to 30% by reducing RAG. |

When the assembled prompt would exceed the total budget, Spice returns a structured error rather than silently truncating. Calling apps must reduce the request or use hierarchical decomposition (section-by-section drafting).

Budgets are logged in the audit trail as `{input_tokens_system, input_tokens_context, input_tokens_user, max_tokens_reserved}` for cost attribution and context-efficiency analysis.

## Output validation

Every Claude response is classified into one of five disposition categories before returning to the caller:

| Mode | Detection | Disposition | Max retries |
| --- | --- | --- | --- |
| Empty response | No content blocks | Auto-retry | 2 |
| Malformatted output | Not parseable as JSON / Pydantic ValidationError | Auto-retry with corrective instruction | 2 |
| Truncated output | `stop_reason = max_tokens` | Continuation request or `max_tokens` bump | 1 |
| Schema-valid but semantically degenerate | Passes Pydantic but fails per-task sanity check | Route to human review with "Low Confidence" banner | 0 |
| API error (non-retryable) | 4xx excluding 429 | Return error to caller | 0 |

Successful outputs flow into the [[hitl-state-machine]].

## PII detection

Before any prompt is transmitted to Anthropic, Spice scans the assembled prompt (system + context + user input) for:

- **Personal identifiers** (SSN, passport numbers, dates of birth)
- Other sensitive classes per the four-tier [[data-classification-tiers]] scheme

Detection uses regex for structured identifiers and a lightweight NER classifier for unstructured personal names in financial context.

## What this means for the library

Every prompt written in this library is built so it works under Spice's budget and validation contract from day one:

- A stable system prefix that Spice can cache.
- Variable inputs in semantic XML tags so Spice knows what to RAG-fill.
- A Pydantic schema for the structured output so Spice's malformatted-output detector can flag drift.
- An explicit `[INSUFFICIENT DATA — <what is missing>]` marker so Spice can route low-confidence outputs to the right reviewer.

When the artifact moves into Arrakis, Spice takes over the brokering — but the prompt does not need to change.

## Related Concepts

- [[hitl-state-machine]] — the review gate Spice outputs flow into
- [[mcp-tool-catalog]] — the read-only tools Spice can invoke
- [[prompt-versioning-governance]] — how prompts are managed
- [[data-classification-tiers]] — what Spice masks and audits

## Sources

- `arrakis_blueprint_v2_3.md`, Section 7 — LLM Integration Layer Architecture
