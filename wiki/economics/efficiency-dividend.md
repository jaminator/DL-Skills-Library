---
title: The Efficiency Dividend
category: economics
tags: [economics, opportunity]
sources:
  - deal_lifecycle_automation_051326_vJA.pdf
last_updated: 2026-05-13
---

# The Efficiency Dividend

The Efficiency Dividend is the cost lever paired with the [[growth-gap]]: same growth target (225 portfolio companies by YE 2030), but **automation changes what it costs to get there**. Where the Growth Gap measures the revenue the firm leaves on the table, the Efficiency Dividend measures the IP headcount and operating cost it avoids.

## The numbers (2030 run-rate)

| Metric | No Automation (225 cos) | Automation Base (225 cos) | Delta |
| --- | --- | --- | --- |
| IPs required | 120 | 45 | **−75 IPs** |
| IP cost ($M / yr, fully loaded at $600K) | $71.8 | $27.0 | **−$44.8M / yr** |
| Tech opex / capex ($M / yr) | — | $2.0 | +$2.0M / yr |
| **Total cost (IP + tech)** | **$71.8M** | **$29.0M** | **−$42.8M / yr net** |

Net annual benefit at 2030 run-rate: **$42.8M / yr** at the base case. Sensitivity band $25–49M; up to $54M at $750K / IP loaded cost. **Cumulative ~$120M over five years.**

## The mechanism

Automation lifts cos / IP from the peer-average regression baseline (1.88×) to a target of **5.0× (base case)** or **6.5× (upside case)**. Without automation, the deck argues the firm regresses toward the peer average as the book grows, because non-sponsor labor intensity (see [[non-sponsor-friction-premium]]) means peer cos / IP ratios are not directly portable to a non-sponsor book.

| Scenario | cos / IP | IPs at 225 | IP cost ($M / yr) |
| --- | --- | --- | --- |
| Peer average regression anchor | 1.88× | 120 | $71.8M |
| The firm today (no automation) | 3.75× | 60 | $36.0M |
| Automation-assisted (base) | 5.0× | 45 | $27.0M |
| Automation-assisted (optimistic) | 6.5× | 35 | $20.8M |

## The buildout cost

Cumulative buildout 2026–2030: **$7.5–12.5M total ($10M base)** — $1.5–2.5M / yr at run-rate, 3.5–4.5 incremental FTE on top of the existing 5-person CB dev team.

**Payback:** $10M cumulative spend recovered in ~3 months at 2030 run-rate. Annual benefit ($8M → $43M ramping) exceeds spend in every year. The buildout self-funds from year one of the phased rollout.

The deck flags one **load-bearing assumption**: the $1.5–2.5M / yr cost frame depends on multi-agent engineering throughput. If that throughput does not materialize, run-rate reverts toward $3–6M / yr and firm-wide amortization across ~$46B AUM (Credit + PE + RE — see [[three-roi-levers]]) carries proportionally more weight.

## Where the dividend comes from, phase by phase

Automation does not lift productivity uniformly across phases. The deck implies the highest-yield productivity gains land in:

- **Memo drafting (P4, P10–P11, P16)** — generate-with-review compresses hours per memo materially.
- **DD synthesis (P5–P6, P9–P10)** — extract-and-validate plus structured Q&A retrieval reduces re-asking and re-reading.
- **Closing diligence (P14–P15)** — redline AI and closing memo auto-gen reduce manual document handling.
- **Portfolio monitoring (P17, P18)** — Chronograph auto-feed and AI valuation triage reduce per-name AM hours from ~30–60 / yr toward something materially lower.

These are exactly the phases the library targets for build-out after the [[posting-memo-friction]] pilot.

## What this means for the library

The Efficiency Dividend is the case for breadth: the dividend compounds across the 19 phases, so the library's value scales with how many phases it covers. A pilot that proves the construction pattern (skill + prompt + project instruction + schema, portable into Arrakis) is the unit; replication across phases is what unlocks the dividend.

## Related Concepts

- [[growth-gap]] — paired revenue lever
- [[three-roi-levers]] — full ROI framing
- [[non-sponsor-friction-premium]] — why peer ratios don't port
- [[option-c-recommendation]] — the path that captures both levers

## Sources

- `deal_lifecycle_automation_051326_vJA.pdf`, slides 08, 12, 13, 20
