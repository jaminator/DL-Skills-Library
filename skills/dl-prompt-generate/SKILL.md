---
name: dl-prompt-generate
description: Designs and generates production-ready Claude prompts — system prompts, task prompts, or user prompts — tailored to specific inputs, tools, models, and output formats. Use this skill whenever a user asks to write, design, draft, create, or improve a prompt for Claude, including for analytical workflows, credit analysis, document generation, or any structured task. Also activate when the user wants to configure Claude for a specific role or workflow, asks how to best prompt Claude for a task, or wants to turn a manual workflow into a reusable Claude instruction set. Does not generate SKILL.md files — use skill-creator for that.
---

# Prompt Generator

Generate production-ready Claude prompts through structured elicitation and Anthropic best practices.

## Elicitation Framework

Before generating, gather three categories of information. If the user's invocation already contains this information, extract it from context and confirm — don't re-ask. Otherwise, ask in a single consolidated message (not piecemeal across multiple exchanges).

**Category 1: Inputs & Tools**
- Reference files or materials Claude will work with (e.g., CIM PDF, inline text, uploaded Excel, existing project files)
- Connectors needed — available: PitchBook Premium, Microsoft 365, Chronograph, S&P Global
- Native tools: extended thinking, web search, deep research, code execution, file creation, artifacts

**Category 2: Model**
- Target model: Haiku 4.5 (speed/cost), Sonnet 4.6 (balanced), Opus 4.6 (max reasoning)
- Latency-sensitive or quality-critical?
- If unspecified and the task is analytical or credit-focused, default to Sonnet 4.6

**Category 3: Output**
- What Claude should produce (analysis, document, extraction, recommendation, etc.)
- Format: inline markdown, .md, .docx, .pptx, .xlsx, .json, HTML, etc.
- Any required structure, template, or section organization?

## Generated Prompt Structure

Every prompt should include these components as applicable. Omit sections that genuinely don't apply — don't pad.

### 1. Role / System Prompt (2–3 sentences)
Set the analytical lens and domain. Assume the user is expert-level. For Overland/credit tasks: assume institutional private credit knowledge — no need to define EBITDA, leverage, or direct lending mechanics.

### 2. Problem Statement (1–2 sentences)
What does the prompt solve? Lead with the insight, not the process.

### 3. Input Specification (XML-tagged)

```xml
<inputs>
  <required>
    - [Input 1]: format and description
  </required>
  <optional>
    - [Input 2]: what it enables
  </optional>
</inputs>
```

### 4. Core Instructions

- Number complex tasks as sequential steps
- Provide input/output example pairs when output quality depends on seeing examples — wrap in `<example>` tags
- For analytical tasks: specify the analytical framework explicitly (see Overland-Specific Guidance below)
- For quantitative tasks: specify calculation method or formula explicitly
- Match degree of freedom to task fragility:
  - **High freedom**: judgment-heavy analysis where context drives the approach
  - **Low freedom**: formula-driven, template-bound, or sequencing-critical tasks where consistency matters

### 5. Output Specification
- Exact format: markdown, JSON, docx, etc.
- Required sections or template structure — use `ALWAYS` language when structure is non-negotiable
- Formatting preference: prose paragraphs vs. bullets (default to analytical prose for credit outputs)

### 6. Constraints (when needed)
- Scope limitations, data boundaries, known edge cases
- Analytical assumptions the prompt makes

### 7. Tool Configuration (when applicable)
- Which tools Claude should use and when (e.g., "Use extended thinking before modeling covenant scenarios")
- MCP server references with fully qualified tool names: `PitchBook Premium:pitchbook_search`, `S&P Global:kfinance_get_company`, etc.
- Code execution or file creation instructions

## Overland-Specific Guidance

Apply when generating prompts for credit, lending, or Overland internal workflows.

**Model defaults:**
- Analytical memos, deal summaries, posting memo sections → Sonnet 4.6
- Multi-step agentic tasks (populating templates, running calculations) → Sonnet 4.6 at high effort
- Deep multi-document synthesis or extended reasoning → Opus 4.6
- High-volume screening or latency-sensitive tasks → Haiku 4.5

**Available connectors:**
- `PitchBook Premium` — company profiles, deal comps, investor/sponsor data
- `S&P Global` — market data, credit ratings, financial data
- `Microsoft 365` — Word, Excel, Outlook integration
- `Chronograph` — portfolio monitoring, fund analytics

**Credit analytical frameworks:**
When generating a prompt that requires Overland's credit quality screen, FCF decomposition sequence, or first principles orientation, read [reference/overland-credit-framework.md](reference/overland-credit-framework.md) and embed the relevant framework sections into the prompt's Core Instructions. The reference file contains:
- Credit quality screen — industry-level criteria (secular tailwinds, cyclicality, competitive structure)
- Credit quality screen — company-level criteria (demand driver quality, concentration, margin profile, capital intensity, DDTL use case)
- FCF analytical framework — 10-step decomposition sequence (Porter through origination context)
- First principles orientation (Porter + Mauboussin anchors, base rate discipline)

Use the full framework for comprehensive credit analysis prompts. Use individual sections selectively when the prompt covers a narrower analytical scope (e.g., only EBITDA quality, only covenant stress, only industry screen).

**Format defaults for credit outputs:**
- Analytical prose paragraphs — not bullet points
- No unnecessary preamble — lead with the most important insight
- Flag uncertainty explicitly rather than filling gaps with assumption

## Output Format

Present the generated prompt as a clean markdown block:

```markdown
# [Prompt Title]

**Target Model:** [model] | **Key Tools:** [tools, or omit if none]

## Your Role
[Role statement]

## Input
<inputs>...</inputs>

## Task
[Instructions — numbered steps if multi-step]

## Output Format
[Exact format and structure]

## Constraints (if applicable)
[Scope limits, assumptions]
```

Include a brief note (1–2 sentences max) on key design choices only if non-obvious. Make the prompt immediately copy-paste ready.

## Anti-patterns

These constraints are already enforced by the rules above; they are surfaced here explicitly so they are not overlooked.

- **Do not generate `SKILL.md` files.** This skill authors prompts, not skills. Defer skill authoring to skill-creator. The line between prompt authoring and skill authoring is intentional and not crossed.
- **Do not pad the generated prompt with non-applicable components.** Every prompt should include the components in "Generated Prompt Structure" *as applicable* — omit sections that genuinely don't apply rather than including an empty or filler section.
- **Do not re-ask for information already supplied.** When the invocation already contains inputs/tools, model, or output details, extract from context and confirm; do not run the elicitation as a fresh multi-exchange interview.
- **Do not fill analytical gaps with assumption in credit outputs.** Generated credit prompts must instruct Claude to flag uncertainty explicitly rather than papering over missing data.

## Reference Files

- [reference/overland-credit-framework.md](reference/overland-credit-framework.md) — Full Overland credit quality screen, FCF analytical framework, and first principles orientation. Read when generating prompts for credit or lending workflows.

## Examples

See [reference/EXAMPLES.md](reference/EXAMPLES.md) for worked end-to-end examples showing elicitation → generated prompt.

## Portability into Arrakis

This is a **cross-cutting meta-skill with no lifecycle phase** — it productizes prompt engineering itself for the underwriting team's general Claude Desktop work rather than mapping to a single deal-lifecycle stage. It carries the Overland analytical inheritance (credit quality screen, FCF decomposition, first-principles orientation) into the prompts it generates, the same lens the lifecycle skills apply directly.

Its **primary output — a free-form generated prompt — is not Snowflake-destined**. The paired schema (`schemas/generated_prompt_spec.py`) therefore captures only the *generation spec* (the elicited inputs/tools, model selection, and the component set emitted), not the generated prompt body, which is intentionally left outside the structured contract. The `[DRAFT — HUMAN REVIEW REQUIRED]` watermark and the `PENDING_REVIEW` HITL state still apply to the spec artifact: a generated prompt is a generate-with-review deliverable that the analyst reviews and adapts before use.

The **project-instruction slot is formally N/A — a documented exemption, not a coverage gap.** A non-lifecycle utility has no recurring per-deal context, so a stage project instruction would be a hollow artifact (per the approved plan §4.5). The bundle for this skill is therefore skill + prompt + schema only. When the skill graduates, the generation spec lands in the Arrakis prompt library as a generate-with-review record seeded in the `PENDING_REVIEW` HITL state; the generated prompt itself remains a free-form authoring artifact, not a structured data product. No rewrite of the skill body is required at graduation.
