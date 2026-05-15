---
name: dl-sector-screen
description: >
  Decomposes a sector, industry, or sub-industry into discrete sub-verticals, screens each against
  the Overland industry attractiveness framework, and produces a structured markdown handoff with
  cascade anchor companies, NAICS codes, trade orgs, and conference targets for downstream borrower
  identification. Use whenever the user wants to develop sourcing coverage on a sector or industry —
  trigger phrases include "research X sector", "screen the Y industry", "develop sourcing coverage
  on Z", "decompose W into sub-verticals", "what sub-verticals in Q are attractive", or any
  freeform sector-level sourcing question. Use this even when the user describes a sector
  thematically (e.g., "aging infrastructure plays", "outsourced facilities services") rather than
  naming it directly. Do NOT use when the user names a specific company or deal (route to borrower
  identification or posting memo workflows), or for sector-level work unrelated to Overland
  sourcing such as public equity research or general market analysis.
---

# Sector Research & Sub-Vertical Identification

Phase 1 of the Overland sourcing workflow. Decompose a sector, screen sub-verticals against the Overland industry attractiveness framework, and produce a structured markdown handoff for downstream borrower identification.

## Audience and tone

Output is read by senior direct lending professionals. Assume full institutional private credit fluency — do not define EBITDA, leverage, FCF conversion, working capital intensity, or tier structure. Write the output as a credit-side analyst would: lead with the insight, flag uncertainty explicitly, and avoid framework citations in prose.

## Workflow

1. **Disambiguate scope.** If the user names a sector that is too broad to produce a focused output (e.g., "industrials", "healthcare", "business services"), ask one clarifying question to narrow before proceeding. If the input names a single company or specific deal rather than a sector, stop and redirect to borrower identification or the posting memo workflow. Otherwise proceed silently.

2. **Load the attractiveness screen.** Before any scoring, read `reference/overland-industry-attractiveness-screen.md` using the view tool. This file defines the eight Porter-derived FCF signals, the three-tier competitive structure model, and the micro FCF driver checklist. All scoring rationale must map to its named categories. Do not reproduce its contents in output — reference the categories by name only.

3. **Decompose into sub-verticals.** Identify 4–10 discrete sub-verticals within the input sector. Anchor decomposition to NAICS 4-digit groupings where possible; deviate when industry economics cut across NAICS boundaries (common in services). For broad inputs that survived Step 1, cap at 5 sub-verticals and flag partial coverage in the output preamble.

4. **Score each sub-vertical against the screen.** Use web search and PitchBook research to assess each sub-vertical against the eight FCF signals and the tier structure model. Produce one of three verdicts:
   - **Pursue** — clears the screen materially, three-tier structure intact with viable Tier 2 population
   - **Watch** — clears most signals but has one or more flagged risks worth monitoring
   - **Screened Out** — fails the screen materially or lacks Tier 2 addressability

   Verdict rationale must cite specific screen categories by name. Examples: "Entry Barriers: state applicator licensing + EPA registration", "FCF Conversion: asset-light, fleet maintenance capex ~3% of revenue", "Buyer Power: fragmented commercial buyer base, no single account >5% of typical Tier 2 revenue".

5. **Identify cascade anchors for Pursue and Watch sub-verticals.** Name 3–5 large reference companies per sub-vertical that can serve as organizational anchors when searching for smaller comps in the next phase. Mix tiers where possible — at least one public company or BSL borrower, at least one PE-backed Tier 1 platform. Use PitchBook to validate platform sponsorship and recent transaction activity.

   Each anchor entry includes: company name, type (`Public` | `BSL` | `PE-Platform`), and a one-line descriptor naming the operating model. Anchors must be currently operating businesses — do not list companies acquired, merged out of existence, or wound down.

6. **Map NAICS codes.** For each Pursue and Watch sub-vertical, list 1–3 candidate NAICS codes (4- or 6-digit). Prefer 6-digit specificity when the sub-vertical maps cleanly; fall back to 4-digit when the sub-vertical spans multiple 6-digit codes.

7. **Identify trade orgs and conferences.** For each Pursue and Watch sub-vertical, list relevant trade associations, membership directories, and industry conferences. Specificity matters — prefer the industry-specific org over a generic umbrella body (the HVAC contractor association, not the manufacturing umbrella). For conferences, flag any with publicly-available attendee or exhibitor lists; these are high-yield borrower identification sources downstream.

   Each entry includes: name, URL (if known), brief descriptor, and `exhibitor_list: yes | no | unknown`.

8. **Draft the thesis paragraph.** For each Pursue and Watch sub-vertical, write a 1–2 sentence thesis characterizing the Tier 2 addressable opportunity — operating model, scale band of typical Tier 2 incumbents, and the structural feature that makes them Overland-suitable. Analytical prose only. Do not use the words "Porter", "five forces", or "base rate" in any output. Do not recite framework categories in narrative form — the verdict rationale field is where category mapping lives.

9. **Handle edge cases.**
   - Oligopolistic structure (no Tier 2 population, e.g., elevator OEM service): score as Screened Out with rationale "Limited Overland addressability — Tier 2 population thin or non-existent."
   - Geographically or regulatorily concentrated sub-verticals: score normally but populate the `Scope caveat` field naming the constraint.
   - Sub-verticals that fail the screen entirely: place in the `## Screened Out` section with a one-sentence rejection rationale. Do not omit silently.
   - Unresolvable factual gaps (contested HHI, unknown sponsor activity, unclear regulatory regime): list under `## Open Questions` rather than guessing.

10. **Write output.** Produce a single markdown file at `outputs/p1_sector-research_<slug>.md` using the schema below. Section headers, field names, and the Pursue/Watch/Screened Out taxonomy are stable — the downstream borrower identification skill parses against this schema.

## Output schema

ALWAYS produce a single markdown file matching this schema exactly. Use analytical prose in the `Thesis` field; use bullets only inside the structured fields.

```markdown
# Sector Research: [Sector Name]
**Date:** [ISO date]
**Input scope:** [original user input, verbatim]
**Coverage note:** [full | partial — and why, if partial]

## Pursue

### [Sub-Vertical Name]
- **NAICS:** [code(s)]
- **Verdict rationale:** [2–4 sentences mapping to screen categories by name]
- **Scope caveat:** [if applicable; otherwise omit field]
- **Thesis:** [1–2 sentence prose paragraph on Tier 2 addressable opportunity]
- **Cascade anchors:**
  - [Company] — [Public | BSL | PE-Platform] — [one-line descriptor]
  - [3–5 entries total]
- **Trade orgs & conferences:**
  - [Name] — [URL] — [descriptor] — exhibitor_list: [yes | no | unknown]
  - [as many as relevant; prioritize specificity over count]

[Repeat for each Pursue sub-vertical]

## Watch

[Same schema as Pursue. Include a `Watch flags:` field noting the specific screen risks being monitored.]

## Screened Out

### [Sub-Vertical Name]
- **NAICS:** [code(s)]
- **Rejection rationale:** [one sentence]

[Repeat for each Screened Out sub-vertical]

## Open Questions
[Unresolved factual gaps. One bullet per gap.]
```

If any required field cannot be resolved, write `[unresolved: <reason>]` in the field. Do not fabricate.

## Worked example (single sub-vertical block)

The following illustrates the level of specificity expected in a populated Pursue entry:

```markdown
### Commercial fire suppression service & inspection
- **NAICS:** 561621 (Security Systems Services), 238220 (Plumbing/HVAC/Sprinkler)
- **Verdict rationale:** Entry Barriers — NFPA certification plus AHJ approval at the local jurisdiction level create meaningful credentialing lag. Non-Discretionary Demand — code-mandated annual inspection and quarterly testing under NFPA 25; deferral creates direct regulatory and insurance exposure. Substitution Risk — none; sprinkler systems are code-required and not displaceable. Capex Profile — asset-light, primarily van fleet and inspection equipment; maintenance capex ~3% of revenue.
- **Thesis:** Regional Tier 2 inspection-and-service operators in the $5–25M EBITDA band with route-dense commercial customer bases (office, light industrial, multi-family) are highly Overland-suitable — recurring inspection revenue under NFPA 25 produces through-cycle EBITDA stability and the credentialing moat insulates against price-led entry.
- **Cascade anchors:**
  - APi Group — Public — global fire/life safety services platform, multi-brand consolidator
  - Pye-Barker Fire & Safety — PE-Platform — Leonard Green-backed national fire/life safety roll-up
  - Cintas Fire Protection — Public — fire protection division of facility services platform
  - Summit Fire & Security — PE-Platform — SK Capital-backed regional consolidator
- **Trade orgs & conferences:**
  - National Fire Sprinkler Association (NFSA) — nfsa.org — contractor membership directory — exhibitor_list: yes
  - American Fire Sprinkler Association (AFSA) — firesprinkler.org — open-shop contractor body — exhibitor_list: yes
  - NFPA Conference & Expo — nfpa.org/conference — annual industry conference — exhibitor_list: yes
```

The verdict rationale cites screen categories by name (`Entry Barriers`, `Non-Discretionary Demand`, `Substitution Risk`, `Capex Profile`) rather than describing them; the thesis is prose with no framework citations.

## Tools

- **view** — Required at Step 2 to load `reference/overland-industry-attractiveness-screen.md`. Reread sections as needed when scoring rationale needs to map back to a specific category.
- **web_search** — Used at Steps 4, 5, 7 for sub-vertical economics, cascade anchor validation, and trade org / conference identification. Run multiple queries in parallel when calls are independent.
- **PitchBook** (MCP, if connected) — Used at Step 5 to validate PE-backed platform sponsorship, fund identity, and recent transaction activity. Use `pitchbook_search` to resolve company entities, then `pitchbook_get_profile` for ownership detail. If PitchBook is not connected, fall back to web search and flag platform identity confidence in the cascade anchor descriptor.
- **create_file** — Step 10, for writing the output markdown to `outputs/p1_sector-research_<slug>.md`.

## Constraints

- Do not reproduce the Overland industry attractiveness screen, FCF decomposition sequence, or Porter/Mauboussin citations in output. Reference categories by name only.
- Do not score sub-verticals from memory or training data alone. Validate Tier 1 platform identity, recent transaction activity, and trade org existence via web search or PitchBook before naming.
- Cascade anchors must be currently operating businesses.
- Geographic scope defaults to US. If the user specifies otherwise or the sub-vertical is geographically concentrated, populate `Scope caveat`.
- Output is the structured markdown file only. Do not produce a posting memo, deal screen, or borrower-level analysis — those are downstream phases.

## Anti-patterns

These restate the rules above as failure modes to avoid; they introduce no new behavior.

- Do not reproduce the attractiveness screen, the FCF decomposition sequence, or Porter/Mauboussin citations in output. Reference screen categories by name only.
- Do not use the words "Porter", "five forces", or "base rate" anywhere in output, and do not recite framework categories in narrative prose — category mapping belongs only in the verdict rationale field.
- Do not score sub-verticals from memory or training data alone. Validate platform identity, recent transaction activity, and trade org existence via web search or PitchBook before naming.
- Do not list cascade anchors that have been acquired, merged out of existence, or wound down — anchors must be currently operating businesses.
- Do not omit screened-out or concentrated sub-verticals silently. Failed sub-verticals go under `## Screened Out` with a one-sentence rationale; concentrated ones get a `Scope caveat`; unresolvable factual gaps go under `## Open Questions`.
- Do not fabricate a field value. If a required field cannot be resolved, write `[unresolved: <reason>]`.
- Do not modify section headers, field names, or the Pursue/Watch/Screened Out taxonomy without a coordinated downstream update — the schema is the frozen handoff contract.
- Do not produce a posting memo, deal screen, or borrower-level analysis. The only output is the structured markdown file; borrower-level work is a downstream phase.
- Do not proceed on an over-broad input without one clarifying question, and do not run the screen on a single named company or deal — redirect those to borrower identification or the posting memo workflow.

## Downstream contract

The `p2_borrower-identification` skill (not yet built) consumes this output. It expects the schema above intact — sub-vertical names, NAICS codes, cascade anchor names, and trade org / conference names are used directly as query seeds. Do not modify field names or section headers without coordinated update to the downstream skill.

## Format compatibility

Authored as SKILL.md for Claude Desktop. To run inside a claude.ai Project, copy the body (Audience through Downstream contract) into project instructions and bundle `reference/overland-industry-attractiveness-screen.md` as a project file. The view calls in Step 2 resolve against the project filesystem in either environment.

## Portability into Arrakis

This skill maps directly into the P1 Deal Sourcing slice of Stage 1 (Origination) and graduates into the Arrakis sourcing/origination application without a rewrite of the skill body. The lifecycle phase is **Stage 1 / P1 Deal Sourcing** — the binding constraint on the growth path. The structured contract is the **frozen `p2_borrower-identification` markdown handoff**: the section headers, field names, and the Pursue/Watch/Screened-Out taxonomy are stable by design and are formalized field-for-field in `schemas/sector_screen_handoff.py` so the same shape validates in Spice. The handoff is a **generate-with-review** artifact: it is emitted in HITL state `PENDING_REVIEW` with `requires_human_review: true`, and the sourcing analyst validates the screen verdicts and cascade anchors before the handoff feeds downstream borrower identification. When the artifact graduates, the underlying prompt is invoked through Spice, the same schema becomes the data-product contract, and the structured handoff lands in the origination application's landing tier. No rewrite of the skill body is required at graduation.
