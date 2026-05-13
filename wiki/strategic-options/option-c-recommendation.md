---
title: Option C Recommendation
category: strategic-options
tags: [strategic-options, architecture]
sources:
  - Overland_Deal_Lifecycle_Automation_051326_vJA.pdf
  - arrakis_blueprint_v2_3.md
last_updated: 2026-05-13
---

# Option C Recommendation

The deal lifecycle deck recommends **Option C — build a custom application suite over a shared Snowflake substrate** as the primary path. Options A and B (see [[three-options]]) are kept as a no-regret bridge and an opportunistic fallback respectively, but only Option C delivers all three of the strategic objectives simultaneously.

## The three things only Option C does

### 1. Closes the Growth Gap

Option C solves the **P1 lead-enablement layer** that no commercial vendor supplies. P1 is the binding constraint on revenue: at today's 4% lead-to-close conversion (already at peer benchmark), reaching 200–250 portfolio companies by 2030 requires roughly 3–4× the qualified-lead volume, and only a custom WF-channel-aware sourcing layer can produce that uplift.

The numbers that flow from closing this gap (see [[growth-gap]]):

- **+$285M** cumulative fee revenue (2026–2030)
- **+$8.6B** YE-2030 funded AUM
- **+115** portfolio companies
- **+$125M / yr** run-rate fees by 2030

### 2. Captures the Efficiency Dividend

Option C tempers the IP-headcount growth that scaling from 30 names today to 110 or 225+ would otherwise force. See [[efficiency-dividend]]:

- **~75 IPs avoided** at scale (lifting cos/IP from the peer-average 1.88× to 5.0× base / 6.5× upside)
- **~$120M cumulative cost savings** over five years vs. running the same book without automation
- **$42.8M / yr net benefit** at 2030 run-rate (base case)

### 3. Makes One Team a property of the technology

This is the qualitative argument the deck weights heavily. **One Team** is a Centerbridge core value. Today it is a value statement, not a technological reality — the data across CB strategies does not talk to itself, and when an IP forgets a detail or leaves the platform, their insights leave with them.

Option C builds the foundation controls (IC vote tracking, valuation discipline, compliance cert verification, RCF/DDTL enforcement) on a common architecture so the knowledge base does not just persist — it grows, compounds across Credit, PE, and RE, and accrues to every future deal team. See [[foundation-controls]].

## What Option C is, in one paragraph

A semi-autonomous, agentically orchestrated mesh of purpose-built FastAPI applications on top of CBP's existing Snowflake DB. Every node carries its own data model and is a peer on the mesh. The substrate (Foldspace) owns the integration and master data governance layer; each domain app owns its operational state. This is **Project Arrakis** — see [[arrakis-overview]].

## Why Option B is wrong

Commercial vendors built for sponsor-backed BSL apply the wrong workflow assumptions to a US-MM non-sponsored book. Each vendor maintains its own opinionated data model — the stack does not talk to itself, and no product closes the P1 gap. **Buy-vs-build stays open at every application** under Option C, but the substrate decision is the prerequisite either way.

## Why Option A alone is wrong

Option A's artifacts live in individual users' contexts. Nothing accrues to the firm; nothing compounds across deals; the foundation controls stay open. Option A is the right **bridge** because immediate IP-level productivity is real and useful — but the artifacts must be constructed so they graduate into Option C without rewriting. **This library is exactly that bridge.** Every prompt, skill, and instruction here is built portable: stable system prefix, semantic XML inputs, Pydantic-validated outputs, HITL watermark.

## The recommended posture, restated

> Pursue Option C as the primary path; keep Option A in parallel as a no-regret bridge. Re-evaluate Option B opportunistically, application by application, once the substrate exists.

## Related Concepts

- [[three-options]] — full A/B/C framing
- [[arrakis-overview]] — what Option C builds
- [[growth-gap]] — revenue lever
- [[efficiency-dividend]] — cost lever
- [[foundation-controls]] — governance investments required

## Sources

- `Overland_Deal_Lifecycle_Automation_051326_vJA.pdf`, slide 10
- `arrakis_blueprint_v2_3.md`, Project Arrakis — Overview
