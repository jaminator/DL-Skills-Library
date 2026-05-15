---
title: Prompt Generator Skill
category: production-skills
tags: [skills, process, system]
sources:
  - ol-prompt-generator.zip
last_updated: 2026-05-15
---

# Prompt Generator Skill

`ol-prompt-generator` is the deployed cross-cutting utility skill. It designs and emits production-ready Claude prompts — system, task, or user prompts — tailored to a specific input set, tool configuration, target model, and output format. It is the only one of the four production skills not bound to a lifecycle phase: it is a **meta-skill** that productizes prompt engineering itself for the underwriting team's general Claude Desktop work, and bakes Overland's analytical conventions into the prompts it generates.

## Elicitation framework

Before generating, the skill gathers three categories in a single consolidated message (extracting from context and confirming rather than re-asking when the invocation already supplies them):

1. **Inputs & tools** — reference materials, connectors (PitchBook Premium, Microsoft 365, Chronograph, S&P Global), native tools (extended thinking, web search, deep research, code execution, file creation, artifacts).
2. **Model** — Haiku 4.5 / Sonnet 4.6 / Opus 4.6, with latency-vs-quality framing; defaults to Sonnet 4.6 for analytical or credit tasks.
3. **Output** — what Claude produces, exact format, required structure.

It then assembles the prompt from a fixed component set (role, problem statement, XML-tagged input spec, numbered core instructions, output spec, constraints, tool configuration), omitting components that genuinely do not apply rather than padding, and presents it as a clean copy-paste-ready markdown block.

## Overland analytical inheritance

The skill's distinguishing feature is **embedded credit-framework awareness**. When generating a prompt for a credit, lending, or Overland workflow it reads its bundled `references/overland-credit-framework.md` and embeds the relevant sections into the generated prompt's core instructions — the [[overland-credit-framework|credit quality screen, FCF decomposition sequence, and first-principles orientation]] (full framework for comprehensive credit prompts, individual sections for narrower scopes). It also carries Overland's model-selection defaults (analytical memos → Sonnet 4.6; deep multi-document synthesis → Opus 4.6; high-volume screening → Haiku 4.5), connector list, and credit-output format conventions (analytical prose not bullets, lead with the insight, flag uncertainty explicitly). Prompts it produces therefore inherit the same analytical lens the [[posting-memo-automation]] and [[sector-research-screener]] skills apply directly.

## Boundaries

The skill explicitly does **not** generate `SKILL.md` files (it defers to skill-creator), keeping a clean line between prompt authoring and skill authoring. This makes it the upstream tool when a maintainer is turning a manual workflow into a reusable Claude instruction set — conceptually adjacent to the development-environment [[prompt-versioning-governance|prompt-versioning discipline]] (versioned system prefix vs. variable inputs), but operating at Claude Desktop authoring time rather than at the Spice runtime. It is a generate-with-review shape: the analyst reviews and adapts the generated prompt before putting it into use.

## Related Concepts

- [[production-skill-inventory]] — the deployed-skill catalog
- [[overland-credit-framework]] — the analytical reference it embeds into credit prompts
- [[prompt-versioning-governance]] — the analogous system-prefix / variable-input discipline in the dev environment
- [[library-artifact-bundle]] — the prompt artifact this skill helps author
- [[opportunity-shapes]] — generate-with-review, its operating shape

## Sources

- `ol-prompt-generator.zip`, `SKILL.md` (elicitation framework, generated structure, Overland guidance) + `references/overland-credit-framework.md`, `references/EXAMPLES.md`
