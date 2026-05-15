# Project Instruction — Stage 6 Asset Management (P17–P19)

This document is the project-level instruction for any Claude Desktop project that supports a Stage 6 Asset Management workflow on a specific portfolio facility. It carries:

1. A deal-context slot to be filled at portfolio-onboarding time.
2. The active deliverables for the stage and the artifact-versioning convention.
3. Behavioral rules specific to the stage.
4. An **Institutional Knowledge** section embedded inline as compiled wiki content (compile date below). The reader does not need access to the underlying wiki to operate.

---

## Stage and purpose

**Stage:** 6 — Asset Management
**Phases:** P17 Portfolio Monitoring · P18 Valuation & LP Reporting · P19 Amendments / Workout
**Purpose:** Maintain the firm's source-of-truth view of every closed facility — covenant status, mark-to-market valuation, compliance certificate validation, RCF / DDTL draw verification, amendment workflow, and LP reporting inputs.


The stage is the highest-governance phase range in the lifecycle. Several pain points here are flagged as audit and regulatory exposures, not just operational inconveniences. The behavioral rules below reflect that.

---

## Deal-context slot (fill at portfolio onboarding)

Replace each placeholder with the facility-specific value before activating this project for a specific facility.

```
COMPANY:                  {{ legal entity name }}
GICS:                     {{ industry classification }}
LTM EBITDA (with source): {{ value }} as of {{ period }} per {{ source: certificate / model / databook }}
FACILITY STRUCTURE:       {{ commitment ($), tranches, pricing, maturity, MFN flag }}
CURRENT IC STATUS:        {{ approved / amended / on watchlist / workout }}
MODEL VERSION + LOCK:     {{ vN-YYYYMMDD; locked / unlocked }}
QOE STATUS:               {{ original QoE date / accountant / refresh status }}
ACTIVE DOCUMENT INDEX:    {{ list of currently-uploaded documents in this project: credit agreement vN, latest compliance cert, prior compliance cert, latest financials, model, databook, ... }}
```

The deal-context slot is **required** before any artifact is produced inside this project. Skills and prompts read these values from project context.

---

## Active deliverables

| Phase | Deliverable | Cadence | Skill |
| --- | --- | --- | --- |
| P17 | Compliance certificate validation | Per certificate received (typically quarterly) | `dl-compcert-review` |
| P17 | Covenant headroom snapshot | Per period close | (future skill) |
| P17 | RCF / DDTL draw verification | Per draw request | (future skill) |
| P18 | Mark-to-market triage | Per valuation cadence (typically quarterly) | (future skill) |
| P18 | LP reporting commentary | Per LP reporting cycle | (future skill) |
| P19 | Amendment workflow | As triggered | (future skill) |

The pilot for the initial library build is **P17 compliance certificate validation**. Other deliverables are placeholders for follow-on iterations.

---

## Artifact versioning

All artifacts produced inside this project follow the convention:

```
[COMPANY]-[DELIVERABLE]-v[N]-[YYYYMMDD]
```

Examples:
- `Acme-Compliance-Certificate-Validation-v1-20260930`
- `Acme-Mark-to-Market-Triage-v2-20261231`
- `Acme-Amendment-Memo-v1-20261115`

Increment `N` on every revision. Date is the period being acted on, not the date of action (so a Q3 2026 compliance certificate validated in November 2026 is `v1-20260930`).

---

## Behavioral rules

1. **Watermark every output.** Every artifact produced inside this project carries `[DRAFT — HUMAN REVIEW REQUIRED]` at the top. The watermark is removed only when an asset management reviewer approves the artifact (an action that happens outside this project, in the AM workflow tracking system).
2. **Never silently omit.** Use `[INSUFFICIENT DATA — <what is missing>]` for any required field where the inputs in the project do not support a value. Never fabricate.
3. **Cite credit-agreement sections explicitly** for any covenant computation, definitional choice, or amendment reference. If the agreement section is not in the project, mark `[INSUFFICIENT DATA — credit_agreement_section_not_provided]` and surface to the reviewer.
4. **Internal classification only.** Outputs from this project are RESTRICTED-eligible (they may contain firm-internal portfolio context). Do not produce co-lender-facing or LP-facing content from this project — those use a different project with the redaction checklist enforced.
5. **HITL state tagged.** Every artifact's structured output carries `review_state: "PENDING_REVIEW"`. The reviewer is the only party that may transition state.
6. **Schema-validated outputs.** Artifacts that are governed by a Pydantic schema (currently the compliance certificate validation) must produce JSON that parses cleanly. If the prompt cannot fit a value into the schema, use `[INSUFFICIENT DATA]` rather than reshaping the schema.
7. **Trend cross-check whenever a prior-period artifact is present.** When the project contains the prior period's certificate or the prior period's mark, use it as a cross-check input. Note any material variance in the reviewer notes.
8. **Audit ready.** Every flagged finding cites the inputs that produced the finding (which line on the certificate, which section of the agreement, which prior-period value).

---

## Institutional Knowledge

The four wiki pages below are embedded as compiled content from the development environment. **Compile date: 2026-05-13.** A reader operating this project in Claude Desktop does not need access to the wiki — the relevant institutional knowledge for this stage is inlined here.

When the wiki is updated, this section is recompiled by the maintainer (next compile due when any embedded page's `last_updated` is newer than the date above).

### Embedded: closing-and-asset-management

*Compiled from `wiki/deal-lifecycle/closing-and-asset-management.md` — last updated 2026-05-13.*

Stages 5 and 6 cover **P13 Co-Lender / GP Syndication through P19 Amendments / Workout** — everything from term-sheet execution through portfolio monitoring and exit.

**Stage 6 — Asset Management (P17 → P19).** Teams: CBP Asset Management · CBP Finance · CBP Marketing & IR · Underwriting · WF RM / Loan Ops & Admin (plus CBP workout team for distressed cases at P19). Tooling: Chronograph · Excel (mark to market) · SharePoint · DealCloud · Outlook (AM distribution list).

**Pain points (4) at this stage.**

- Chronograph not fully utilized as source of truth; monitoring features not leveraged.
- Manual Excel mark-to-market valuations.
- Compliance certs frequently contain CFO arithmetic errors; underwriting catches manually. *(This is the pain the pilot directly addresses.)*
- DDTL draws approved over email; no compliance verification tracked.

**Opportunities (4).** Chronograph auto-feed · AI valuation triage · amendment doc workflow · AM distribution list auto-route.

**Why these stages are under-instrumented.** The governance load is highest here (compliance certs, mark-to-market, RCF/DDTL draws, amendment tracking are foundation controls and audit and regulatory exposures today). The handoff boundary at P15–P16 is fragile (databook may not reach Chronograph). The vendor fit is poorest (Chronograph is intended portfolio system but is under-utilized).

### Embedded: ic-and-asset-mgmt-gaps

*Compiled from `wiki/pain-points/ic-and-asset-mgmt-gaps.md` — last updated 2026-05-13.*

Two of the deck's three highest-acuity pain-point clusters are the IC process and Asset Management. Both are governance gaps as much as workflow gaps — several are flagged as audit and regulatory exposures today.

**Asset Management gaps.**

- **Chronograph not fully utilized as source of truth.** The upstream-to-Chronograph data pipe is incomplete; monitoring features go unused.
- **Manual Excel mark-to-market valuations.** Flagged against the broader industry direction (Apollo's commitment to daily NAV marks); SEC scrutiny is increasing. Manual marks are less defensible in audit.
- **Compliance certificates frequently contain CFO arithmetic errors; underwriting catches manually.** No automated parser, no schema validation, no comparison against the credit agreement's specific definitions. The most acute extract-and-validate target in Asset Management.
- **DDTL draws approved over email; no compliance verification tracked.** Draws are conditional (no default or EoD, pro forma leverage within covenant, permitted use of proceeds) but those conditions are not enforced at funding.
- **Inconsistent UW to AM handoff at close; databook may not reach Chronograph.** AM may start cold on a deal it inherits.

**Root cause.** The workflow exists, but no system holds the audit trail. The IC meets and decides; AM monitors and reports. But neither the decision nor the monitoring is captured in a queryable form. This is a foundation-control gap that exists independent of the growth gap — required at any portfolio size and more acute as the book scales.

### Embedded: hitl-state-machine

*Compiled from `wiki/llm-integration/hitl-state-machine.md` — last updated 2026-05-13.*

Every LLM-generated output flows through a mandatory human-review gate before any consequential action. The HITL state machine defines the seven states a draft passes through.

**The seven states.**

```
AI_DRAFT → VALIDATION_PASSED → PENDING_REVIEW → IN_REVIEW
                                                    │
                                  ┌─────────────────┼─────────────────┐
                                  ▼                 ▼                 ▼
                              APPROVED         REJECTED         REVISION_REQUESTED → AI_DRAFT
                                                    │
                                                    ▼
                                                ESCALATED
```

| State | Meaning |
| --- | --- |
| **AI_DRAFT** | Just returned from the LLM. |
| **VALIDATION_PASSED** | Pydantic validation succeeded. |
| **PENDING_REVIEW** | Surfaced in the calling app's UI with the `[DRAFT — HUMAN REVIEW REQUIRED]` banner. **This is the state every artifact in this project produces.** |
| **IN_REVIEW** | A reviewer has opened the draft. |
| **APPROVED** | Terminal. Reviewer accepted (with or without edits). |
| **REJECTED** | Terminal. Reviewer discarded. Rationale required. |
| **REVISION_REQUESTED** | Reviewer wants a re-draft. New AI_DRAFT with `parent_draft_id` link. |
| **ESCALATED** | Reviewer routes to a senior reviewer. Rationale required. |

**Override audit record.** When a reviewer edits an output before approval, the system persists `{draft_id, reviewer_id, review_state, sections_modified, edit_magnitude (MINOR/MODERATE/MAJOR), rationale, reviewed_at}`. If the MAJOR override rate for a given prompt exceeds 20% over a rolling 30-day window, the prompt is flagged for platform review.

**What this means here.** Every artifact this project produces lands in PENDING_REVIEW. The reviewer is an asset management team member. The reviewer's decision is the next step — this project does not transition state.

### Embedded: data-classification-tiers

*Compiled from `wiki/governance/data-classification-tiers.md` — last updated 2026-05-13.*

Arrakis uses a four-tier data classification scheme that governs every column, every prompt, every MCP tool's return payload, and every artifact this library produces.

**The four tiers.**

| Tier | What goes here | Examples |
| --- | --- | --- |
| **RESTRICTED** | Most sensitive. Audit-grade access controls. No exposure to co-lenders or LPs. | IC deliberation content, individual IC votes, fund-level economics above the co-lender tranche, firm-internal portfolio context |
| **CONFIDENTIAL** | Deal-specific commercial information. Visible to deal team and approved internal consumers; redacted for external counterparties unless explicitly cleared. | Deal financials, model outputs, DD findings, term-sheet economics, borrower KYC status |
| **INTERNAL** | Non-commercially sensitive operational data. Visible to all internal users with platform access. | Workflow state, task assignments, notification routing, system metadata |
| **PUBLIC** | None in this domain. | — |

**What this means for this project.** Outputs are typically CONFIDENTIAL (deal financials, covenant calculations) and may include RESTRICTED context (firm-internal portfolio comparisons, cross-strategy allocation). Outputs are **internal asset-management facing**. They are not for co-lender or LP distribution; the redaction checklist that applies to external-facing artifacts does not apply here. Outputs may contain RESTRICTED context because the consumer (AM team) is permitted to see it.

---

## Summary

This project supports the Stage 6 Asset Management workflow on a single portfolio facility. Fill the deal-context slot at onboarding. Use the active-deliverable skills as the cadence requires. Every artifact carries the watermark, uses `[INSUFFICIENT DATA]` rather than fabrication, cites credit-agreement sections, and lands in PENDING_REVIEW for an asset management reviewer to act on.
