---
title: Three ROI Levers
category: economics
tags: [economics]
sources:
  - deal_lifecycle_automation_051326_vJA.pdf
last_updated: 2026-05-13
---

# Three ROI Levers

The deal lifecycle deck frames the buildout case on **three independent ROI levers** that stack to a self-funding investment from year one. Each lever is meaningful on its own; together they exceed the cumulative buildout cost in every year of the rollout.

## Lever 01 — Fee Accretion

**$285M cumulative** 5-yr fee delta vs. Status Quo (110 portfolio companies by YE 2030). Automation-Base scales the book to **225 portfolio companies and $245M run-rate fees** vs. $120M.

This lever is the [[growth-gap]] expressed as a revenue line. The mechanism is the P1 lead-enhancement layer — a step-change in qualified-lead volume that, combined with the firm's already-peer-benchmark 4% lead-to-close conversion, makes a 200–250 portfolio target throughput-feasible.

The fee delta is back-loaded: 2026–2027 contribute single-digit millions; 2028 hits +$49M / yr; 2029 hits +$91.5M / yr; 2030 hits +$125M / yr.

## Lever 02 — Headcount Avoidance

**$42.8M / yr** 2030 run-rate savings vs. peer-regression baseline (1.88×). Sensitivity band $25–49M at base $600K / IP loaded cost; up to $54M at $750K / IP.

This lever is the [[efficiency-dividend]] expressed as an avoided-cost line. The mechanism is the **cos / IP lift** from the peer-average regression anchor (1.88×) to the automation base (5.0×) or upside (6.5×), saving ~75 IPs at 225 names and ~$120M cumulatively over 5 years.

The deck is explicit that without automation, the firm regresses toward the peer mean as the book grows from 30 names today to 110+. This is not a hypothetical — it is the natural production-function response to scaling a non-sponsor book without instrumentation. See [[non-sponsor-friction-premium]].

## Lever 03 — CBP Data Unification

**~$46B AUM** strategy-agnostic data substrate amortized across all of CB Credit, PE, and RE. The buildout cost spreads across this combined AUM, and one-team workflows (cross-strategy precedent search, shared MDM, unified reporting) become possible.

This is the qualitative lever that distinguishes Option C from Options A and B (see [[three-options]]). The deck quantifies it as a cost-base advantage — a $10M cumulative buildout cost spread across $46B AUM is **0.3–0.8% as an operating cost percentage** — but the strategic value is the institutional knowledge persistence: when an IP forgets a detail or leaves the platform, their insights stay with the firm rather than walking out the door.

## Buildout cost vs. payback

**Cumulative buildout 2026–2030:** $7.5–12.5M total ($10M base) — $1.5–2.5M / yr at run-rate, 3.5–4.5 incremental FTE on top of the existing 5-person CB dev team.

**Payback:** $10M cumulative spend recovered in **~3 months at 2030 run-rate**. Annual benefit ($8M → $43M ramping) exceeds spend in every year. Self-funds from Year One.

## Combined ROI by scenario (2030 run-rate, $M / yr)

| Scenario | IPs | IP cost | Tech opex | Total cost | Net vs Status Quo | Net vs No Automation |
| --- | --- | --- | --- | --- | --- | --- |
| Status Quo (110 cos) | 29 | $17.6 | — | $17.6 | — | — |
| No Automation (225 cos) | 120 | $71.8 | — | $71.8 | $34.1 cost | — |
| Automation Base (225 cos, 5.0×) | 45 | $27.0 | $2.0 | $29.0 | **+$76.9 benefit** | **+$42.8 benefit** |
| Automation Upside (225 cos, 6.5×) | 35 | $20.8 | $2.0 | $22.8 | +$83.1 | +$49.0 |

## Load-bearing assumption

The deck flags **multi-agent engineering throughput** as the load-bearing assumption underneath the $1.5–2.5M / yr cost frame. If that throughput does not materialize, run-rate reverts toward $3–6M / yr and Lever 03 (firm-wide AUM amortization) carries proportionally more weight.

## What this means for the library

The three-lever framing tells the library what to measure when reporting on its own value:

- **Fee accretion** is captured by phases that touch the funnel (P1, P3, P4) — every minute saved per lead lets the underwriter get to the next lead faster.
- **Headcount avoidance** is captured by phases with the highest per-deal time burden (P4, P10–P11, P14–P16, P17–P18) — every hour saved per deal compounds across 47 closes / yr by 2030.
- **Data unification** is captured by every Pydantic schema that lands in `<APP>_LAND` of the [[snowflake-medallion]] — each schema is a piece of institutional knowledge that persists.

## Related Concepts

- [[growth-gap]] — Lever 01 detail
- [[efficiency-dividend]] — Lever 02 detail
- [[option-c-recommendation]] — the path that captures all three
- [[non-sponsor-friction-premium]] — labor-intensity grounding for Lever 02

## Sources

- `deal_lifecycle_automation_051326_vJA.pdf`, slides 12, 13
