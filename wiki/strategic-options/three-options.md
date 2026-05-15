---
title: Three Strategic Options (A / B / C)
category: strategic-options
tags: [strategic-options, governance]
sources:
  - deal_lifecycle_automation_051326_vJA.pdf
last_updated: 2026-05-13
---

# Three Strategic Options (A / B / C)

The deal lifecycle deck frames three paths the firm could take to close the [[growth-gap]] and capture the [[efficiency-dividend]]. Two move a number; only one moves the operating model.

## Option A — Extend the Status Quo

**What it is.** Continue building a personal Claude library of prompts and skills used by individual underwriters, without firm-level coordination or platform investment.

**Why it appeals.** Near-zero capex; immediate IP-level productivity from a growing Claude library; useful regardless of whichever broader path is chosen.

**Why it falls short.** Artifacts live in individual users' contexts. Nothing accrues to the firm; nothing compounds across deals; the foundation controls (IC vote tracking, valuation discipline, compliance cert verification, RCF/DDTL enforcement — see [[pain-point-register]]) stay open.

**Verdict.** Useful as a no-regret bridge. Not sufficient on its own.

## Option B — Buy Commercial Point Solutions

**What it is.** Adopt established vendors across the lifecycle: CLM (Ironclad), data rooms (Ansarada), loan accounting (WSO / Allvue), syndication (SyndTrak / Debtdomain), portfolio monitoring (Chronograph / 73 Strings), legal AI (Harvey).

**Why it appeals.** Fastest parity on commodity workflows; established vendors with mature feature sets.

**Why it falls short.**
- These tools were built for **sponsor-backed BSL**, not US-MM **non-sponsored** lending. Workflow assumptions diverge in material ways (no sponsor CIM, deeper management ODD, custom DDQ patterns, [[non-sponsor-friction-premium]]).
- Each vendor maintains its own opinionated data model. The stack does not talk to itself; data fragmentation is intrinsic to the multi-vendor topology.
- No vendor closes the **P1 sourcing gap**, which is the binding constraint on revenue (see [[growth-gap]]).

**Verdict.** Reconsider opportunistically, application by application, once a substrate exists.

## Option C — Build a Custom Application Suite over a Shared Substrate

**What it is.** A semi-autonomous, agentically orchestrated mesh of purpose-built FastAPI applications on top of CBP's existing Snowflake DB. Every node carries its own data model and is a peer on the mesh. This is **Project Arrakis** (see [[arrakis-overview]]).

**Why it wins on every dimension:**

- **Makes One Team real.** Knowledge persists past any individual IP and compounds across Credit, PE, and RE.
- **Closes the Growth Gap.** Solves the P1 lead-enablement layer no vendor can supply: +$285M cumulative fee revenue (2026–30), +$8.6B YE-2030 funded AUM, +115 portfolio companies vs. Status Quo.
- **Captures the Efficiency Dividend.** Tempers IP-headcount growth — ~75 IPs avoided and ~$120M cumulative cost savings vs. running the same book without automation.
- **Preserves optionality.** Institutionalizes the Option A library that is otherwise being built ad-hoc. No vendor lock-in; buy-vs-build stays open at every application; Option C's architecture is the most flexible substrate for whichever way that call lands.

**Verdict.** Recommended primary path.

## The recommended posture

Pursue **Option C as the primary path**. Keep **Option A in parallel as a no-regret bridge** — this library is the Option A bridge, constructed so its artifacts graduate directly into Option C. Re-evaluate **Option B opportunistically**, application by application, once the substrate exists.

Only Option C simultaneously closes the Growth Gap, captures the Efficiency Dividend, and makes One Team a property of the technology rather than a value statement.

## Related Concepts

- [[option-c-recommendation]] — the detailed case for Option C
- [[arrakis-overview]] — what Arrakis is
- [[growth-gap]] — the revenue lever Option C unlocks
- [[efficiency-dividend]] — the cost lever Option C captures
- [[foundation-controls]] — governance investments required regardless of path

## Sources

- `deal_lifecycle_automation_051326_vJA.pdf`, slide 10
