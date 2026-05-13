---
title: foldspace-mcp Tool Catalog
category: llm-integration
tags: [llm-integration, architecture]
sources:
  - arrakis_blueprint_v2_3.md
last_updated: 2026-05-13
---

# foldspace-mcp Tool Catalog

The **foldspace-mcp** server exposes the read-only structured tools Claude can invoke during agentic flows in Arrakis. It runs as a sidecar process during Claude Code agentic tasks and is the production interface used by Reverend Mother, CHOAM, Mentat, and other apps that invoke Claude through Spice. **All tools are read-only**; write operations go exclusively through the Foldspace REST API.

## The catalog

### Deal and entity context

```python
get_deal_context(deal_id: str) -> DealContextSchema
get_company_profile(company_id: str) -> CompanyProfileSchema
get_sponsor_profile(sponsor_id: str) -> SponsorProfileSchema
get_facility_terms(facility_id: str) -> FacilityTermsSchema
```

### Financial and modeling data

```python
get_financial_metrics(company_id: str, period: str) -> FinancialMetricsSchema
get_model_outputs(deal_id: str, model_version: str = "latest") -> ModelOutputSchema
get_data_book(deal_id: str, version: str = "latest") -> DataBookSchema
```

### Diligence

```python
get_dd_findings(deal_id: str, status: str = "all") -> DDFindingsSchema
get_dd_queue(deal_id: str) -> DDQueueSchema
```

### Portfolio and loan

```python
get_portfolio_position(facility_id: str) -> PortfolioPositionSchema
get_covenant_status(facility_id: str) -> CovenantStatusSchema
```

### Document search

```python
search_deal_documents(deal_id: str, query: str, k: int = 10) -> list[DocumentChunkSchema]
get_document(document_id: str) -> DocumentMetadataSchema
```

### IC and terms history

```python
get_ic_decisions(deal_id: str) -> list[ICDecisionSchema]
get_negotiation_history(deal_id: str) -> NegotiationHistorySchema
```

### Co-lender DD support

```python
get_colender_dd_context(deal_id: str, question_id: str) -> ColenderDDContextSchema
```

### Precedent library

```python
search_precedent_library(clause_type: str, query: str, k: int = 5) -> list[PrecedentSchema]
```

### Specialized extraction

```python
get_covenant_narrative_context(facility_id: str, period: str) -> CovenantNarrativeContextSchema
extract_financial_data(document_id: str, extraction_template: str) -> FinancialExtractionSchema
extract_nda_metadata(document_id: str) -> NDAMetadataSchema
extract_agent_notice(document_id: str) -> AgentNoticeSchema
```

## Tool error contract

All tools return a standardized error schema on failure so Claude can reason about disposition during agentic workflows:

```python
class MCPToolError(BaseModel):
    error_code: Literal[
        "NOT_FOUND",          # Entity does not exist
        "ACCESS_DENIED",      # RBAC denial
        "INVALID_PARAMS",     # Parameter validation failed
        "UPSTREAM_TIMEOUT",   # Snowflake or PostgreSQL query timeout
        "UPSTREAM_ERROR",     # Non-timeout upstream failure
        "RATE_LIMITED",       # Tool-level rate limit
    ]
    detail: str
    retryable: bool
    tool_name: str
    params: dict
```

The expected Claude behavior per error class is documented per tool. `NOT_FOUND` and `ACCESS_DENIED` never retry; `UPSTREAM_TIMEOUT` retries once after 5s; `RATE_LIMITED` waits per `detail`.

## Tool governance metadata

Each tool carries governance metadata in addition to its typed signature:

| Field | Purpose |
| --- | --- |
| `tool_version` | SemVer; incremented on signature, return schema, or data source change |
| `allowed_callers` | Exhaustive list of `app_ids` permitted to invoke; Spice rejects unlisted callers with HTTP 403 |
| `return_data_classification` | Highest tier in return payload (RESTRICTED / CONFIDENTIAL / INTERNAL / PUBLIC) — see [[data-classification-tiers]] |
| `certification_status` | CERTIFIED / PROVISIONAL / DEPRECATED (deprecated tools auto-removed after 90 days) |
| `certified_by` | Engineer / reviewer name |
| `certified_at` | UTC timestamp |
| `depends_on_prompt_ids` | Prompt library IDs that typically use this tool — enables cascade validation |

## Step-level tool invocation lineage

Every tool invocation emits a `ToolInvocationRecord` appended to an ordered list within the session's audit trail:

```python
class ToolInvocationRecord(BaseModel):
    sequence_number: int
    tool_name: str
    tool_version: str
    parameters: dict                  # Sanitized, PII-redacted
    return_data_classification: str
    latency_ms: int
    result_status: str                # SUCCESS | ERROR | TIMEOUT
    result_row_count: int | None
    otel_span_id: str
```

The audit trail in `ARRAKIS_RAW.APP_EVENTS` carries a `tool_invocations` VARIANT column with the ordered array. This enables queries like: "For audit record X, which MCP tools were called, in what order, accessing what classification tiers?" — required for regulatory audit reconstruction.

## What this means for the library

Skills and prompts in this library are **not** invoking foldspace-mcp tools today (Claude Desktop has no access to the platform). But they are constructed so that **when** the artifact graduates into Arrakis, the same prompt can be re-bound to use the appropriate MCP tools without rewriting.

Practically:

- A prompt that needs deal context names that need explicitly: e.g. `<deal_context>{{ from get_deal_context(deal_id) }}</deal_context>`. In Claude Desktop, the user pastes the deal context into the tagged slot. In Arrakis, Spice fills it from `get_deal_context`.
- A skill that performs financial extraction documents that the production binding is `extract_financial_data(document_id, "<template>")`. In Claude Desktop, the skill processes a manually-uploaded PDF.
- A pilot prompt for the [[posting-memo-friction]] phase explicitly notes the future Arrakis bindings (`get_dd_findings`, `search_deal_documents`, `get_company_profile`).

This gives the artifact its portability path without making the Claude Desktop user wait for any backend.

## Related Concepts

- [[spice-llm-service]] — the LLM brokering layer that calls these tools
- [[hitl-state-machine]] — the gate that processes tool outputs
- [[data-classification-tiers]] — what the `return_data_classification` enforces
- [[foldspace-substrate]] — host of foldspace-mcp

## Sources

- `arrakis_blueprint_v2_3.md`, Section 7 — MCP Server Design (foldspace-mcp Expanded), MCP Tool Error Contract, MCP Tool Governance Metadata
