---
title: Sector Research Screener Skill
category: production-skills
tags: [skills, process, opportunity, sector]
sources:
  - ol-industry-screener.zip
last_updated: 2026-05-15
---

# Sector Research Screener Skill

`ol-industry-screener` is the deployed Phase-1 skill for the Overland sourcing workflow. Given a sector, industry, or thematic description ("aging infrastructure plays," "outsourced facilities services"), it decomposes the space into discrete sub-verticals, screens each against the Overland industry attractiveness framework, and emits a structured markdown handoff for downstream borrower identification. It is the first concrete automation of [[origination-and-screening|P1 Deal Sourcing]] — the phase the deck names the binding constraint on the [[growth-gap|growth path]].

## What it does

The workflow is a fixed nine-step sequence:

1. **Disambiguate scope.** Over-broad inputs ("industrials," "healthcare") get one clarifying question; a single named company is redirected to borrower-ID or posting-memo work.
2. **Load the screen.** It reads its bundled `references/overland-industry-attractiveness-screen.md` — the eight Porter-derived FCF signals and the three-tier competitive-structure model (see [[overland-credit-framework]]).
3. **Decompose** into 4–10 sub-verticals, anchored to NAICS 4-digit groupings where industry economics permit.
4. **Score** each against the screen and the tier model, producing one of three verdicts: **Pursue** (clears materially, viable Tier 2 population), **Watch** (clears most signals, flagged risks), or **Screened Out** (fails materially or no Tier 2 addressability). Verdict rationale must cite screen categories by name; web search and PitchBook validate economics rather than scoring from training data.
5–8. For Pursue/Watch: name **cascade anchors** (3–5 currently-operating reference companies, tier-mixed), map **NAICS codes**, identify **trade orgs and conferences** (flagging publicly-available exhibitor lists as high-yield downstream sources), and draft a 1–2 sentence **Tier 2 thesis**.
9. **Handle edge cases** — oligopolistic structures with no Tier 2 population are screened out; concentrated sub-verticals get a scope caveat; unresolvable factual gaps go under Open Questions rather than being guessed.

## The downstream contract

The skill's defining design property is a **frozen output schema**. Section headers and the Pursue/Watch/Screened-Out taxonomy are stable because an unbuilt `p2_borrower-identification` skill is specified to parse them — sub-vertical names, NAICS codes, cascade-anchor names, and trade-org names become query seeds for the next phase. The skill explicitly forbids changing field names without a coordinated downstream update. This is the same forward-contract discipline the [[template-input-schema|input-schema catalog]] applies to deal templates, applied to a skill-to-skill handoff.

## Construction notes

Output is analyst-grade prose for senior credit professionals — no framework definitions, no "Porter"/"five forces"/"base rate" citations in narrative (category mapping lives only in the structured verdict field). The screen reference is consulted but never reproduced in output. It uses `view`, `web_search`, `create_file`, and optionally the PitchBook MCP, degrading gracefully to web search when PitchBook is absent. A "Format compatibility" note covers running it as a claude.ai Project. It is a **generate-with-review** shape: the analyst validates the screen verdicts and anchors before the handoff feeds sourcing.

## Related Concepts

- [[production-skill-inventory]] — the deployed-skill catalog this belongs to
- [[overland-credit-framework]] — the attractiveness screen and three-tier model it applies
- [[origination-and-screening]] — P1, the phase it automates
- [[opportunity-shapes]] — generate-with-review, its operating shape
- [[posting-memo-automation]] — the downstream P4 skills the sourced pipeline eventually reaches

## Sources

- `ol-industry-screener.zip`, `SKILL.md` (workflow, output schema, downstream contract) + `references/overland-industry-attractiveness-screen.md`
