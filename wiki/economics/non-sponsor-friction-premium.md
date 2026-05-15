---
title: Non-Sponsor Friction Premium
category: economics
tags: [economics, pain-point, process]
sources:
  - deal_lifecycle_automation_051326_vJA.pdf
last_updated: 2026-05-13
---

# Non-Sponsor Friction Premium

Non-sponsor deals embed materially more labor per dollar of AUM at every stage of the lifecycle. This is the empirical grounding for why peer cos / IP ratios from sponsor-backed BSL platforms are not directly portable to the firm's US-MM non-sponsored book — and why the [[efficiency-dividend]] case rests on closing this premium with automation rather than by adding IPs.

## The premium, by stage

| Stage | Friction source | Low | Base | High |
| --- | --- | --- | --- | --- |
| **Sourcing** | WF RMs surface a wider distribution of candidates than sponsor-funneled flow; 60–80% of WF leads die in initial screen vs. 40–60% sponsor. | +30% | +40% | +50% |
| **Underwriting** | Data room reconstruction, GAAP normalization, addback substantiation against unaudited financials, deeper management ODD, legal cleanup. 200–400+ hours vs. 150–250 sponsor. | +30% | +60% | +90% |
| **IC preparation** | No sponsor CIM. Credit narrative built from raw inputs. Structural reformatting and consistency checks consume IC-prep hours. | +30% | +50% | +70% |
| **Syndication** | The firm syndicates a meaningful portion of each deal to existing LPs, prospective LPs, and selected GPs — marketing, allocation, and investor Q&A all run through the underwriting deal team. Larger DL platforms (Antares, Golub, Blue Owl) carry dedicated capital-markets desks. | +40% | +60% | +80% |
| **Portfolio monitoring** | Variable reporting maturity; family / founder management requires hand-holding. 1.6 covenants / deal means relationship-based monitoring, not triggered diligence. ~30–60 extra hours / name / year. | +40% | +70% | +100% |

## The translation

Peer ratios are not portable. The 13-manager peer-average is **1.88× cos / IP**. The friction premiums above — including a syndication workstream that larger DL platforms offload to dedicated capital-markets desks — mean a direct-lending IP carries **~50–70% more work per name** than the average peer IP.

**Absent automation, the firm's natural ratio lands closer to ~1.1–1.3×, materially below the peer mean.**

This is what drives the IP requirement at 225 names without automation: the deck projects 120 IPs ($71.8M / yr fully loaded) under the no-automation, 1.88× peer-regression case. With automation, the production-function shift lifts cos / IP to 5.0× (base) or 6.5× (upside), bringing the IP requirement to 45 or 35 respectively.

## Where the premium goes when automation lands

Each of the five stage-level premiums maps to a specific opportunity in the [[opportunity-register]]:

| Premium source | Library response |
| --- | --- |
| Sourcing screen failure rate | AI teaser auto-parse (P1), DealCloud / SF auto-sync (P1) |
| Data room reconstruction | Standardized data book (P3 → P5), AI initial DD synthesis (P5–P6) |
| IC narrative from raw inputs | AI posting memo draft (P4), pre-screen IC pack auto (P7), IC memo auto-build (P11) — the [[posting-memo-friction]] pilot |
| Syndication workstream on UW team | Syndication CRM auto (P13), AI-assisted co-lender DD responses (P13) |
| Variable borrower reporting | Compliance certificate parser (P17), AI valuation triage (P18), AM distribution list auto-route (P17–P19) |

The pilot phase (P4) sits squarely in the IC-prep premium category — the second-largest premium after underwriting itself. Compressing the IC-prep premium produces a measurable, time-attributable saving per deal that demonstrates the construction pattern works.

## The implication for headcount strategy

The premium framing has a strong implication: **adding IPs at the peer regression rate makes the unit economics worse, not better.** A 225-name book at 120 IPs is not just expensive — it is below the peer mean on cos / IP. Automation is the only path that holds the firm above the peer mean while growing the book.

This is why the [[option-c-recommendation]] frames the [[efficiency-dividend]] as a **production-function shift** rather than a productivity tweak. The shift is structural: the substrate, the apps, and the LLM-mediated workflows together change what an IP can do per unit of time.

## Related Concepts

- [[efficiency-dividend]] — the cost-side ROI lever this premium drives
- [[growth-gap]] — paired revenue-side lever
- [[three-roi-levers]] — full ROI framing
- [[posting-memo-friction]] — the IC-prep premium response
- [[opportunity-register]] — the response per stage premium

## Sources

- `deal_lifecycle_automation_051326_vJA.pdf`, slides 18, 19, 20
