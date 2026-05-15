---
title: Three Opportunity Shapes
category: opportunities
tags: [opportunity, process, architecture]
sources:
  - deal_lifecycle_automation_051326_vJA.pdf
last_updated: 2026-05-13
---

# Three Opportunity Shapes

Every automation opportunity in the [[opportunity-register]] resolves to one of **three repeating shapes**. The shape determines what gets built (which artifacts in the [[library-artifact-bundle]] dominate), how the output is reviewed (which [[hitl-state-machine]] variant fires), and where the artifact lands in [[arrakis-overview]]. The taxonomy is the spine that organizes the library's expansion: new builds are categorized by shape first, by phase second.

## Shape 1 — Extract-and-validate

**What it does.** Parse a document (PDF, Word, Excel, or a structured intake form), extract structured facts, validate against a Pydantic schema, flag gaps and inconsistencies. The output is data, not narrative.

**Typical phases.** P1 (teaser parse), P2 (NDA metadata), P3 (kick-off DDQ), P5 (initial DDQ), P9 (follow-up DDQ), P14 (credit agreement final terms), **P17 (compliance certificate parser — the [[compliance-certificate-parser-pilot]]).**

**Artifact emphasis.** Pydantic schema dominates. The prompt is short and focused on extraction discipline. Reference files (taxonomies, error patterns) carry significant weight in the [[library-artifact-bundle]].

**Review profile.** The reviewer is checking field-level accuracy. Edits are usually surgical — a single value corrected, not a section rewritten. `min_quality_spec` sanity checks tend to be tight (e.g., "extracted NDA metadata must contain at least N non-null fields").

**Common failure modes.** Definitional misapplication (the extractor used the wrong definition), period mismatch (compared LTM to QTD), scope error (consolidated vs. senior secured), illegible source content. Each becomes a structured flag in the output.

## Shape 2 — Generate-with-review

**What it does.** Generate a draft (memo section, narrative response, executive summary) from upstream structured inputs. Surface to a reviewer with the `[DRAFT — HUMAN REVIEW REQUIRED]` watermark. The output is prose, anchored in cited facts.

**Typical phases.** P4 ([[posting-memo-friction]]), P7 (pre-screen IC pack), P10 (follow-up DD synthesis), P11 (commitment IC memo), P12 (EL / commit papers narrative), P16 (closing memo), P18 (LP commentary).

**Artifact emphasis.** Prompt dominates — cache-eligible system prefix carrying the role, format, guardrails, and structural template. Variable inputs in semantic XML tags. Pydantic schema describes the prose-with-structure output (section-level, not field-level).

**Review profile.** The reviewer is checking factual consistency, edit severity, and usefulness. The override audit record (see [[hitl-state-machine]]) is rich — `sections_modified` is informative, not just `edit_magnitude`. Drift detection on `MAJOR` override rate is the operative signal.

**Common failure modes.** Factual drift (statement not supported by retrieved context), structural omission (section blank because of upstream data gap), tone mismatch (memo register doesn't match consumer audience). The first becomes a hallucination flag; the second a `[INSUFFICIENT DATA]` marker; the third surfaces through edit severity.

## Shape 3 — Route-and-track

**What it does.** Maintain a workflow state machine across multiple deal-lifecycle steps. Track artifact provenance, deadlines, owners, and handoffs. Surface "what's next" and "what's blocked" to the right team at the right time.

**Typical phases.** P2 (NDA workflow), P3–P9 (DDQ item lifecycle tracker), P13 (syndication commitment book), P15 (closing checklist), P17–P19 (AM cadence routing).

**Artifact emphasis.** Project instruction dominates. The instruction pins state, defines transitions, names owners, and gates on conditions. The prompt is light; the schema captures the state record (status, owner, deadline, completion criteria).

**Review profile.** Review is event-driven — at each state transition, not on each draft. The "human review" is approval of a transition, often a single click. The audit trail captures who approved each transition rather than what content was edited.

**Common failure modes.** Stale state (workflow advanced in another system but not here), missing owner, ambiguous transition criteria, dropped handoff. The fixes are usually instruction tightening or new events on the [[redpanda-event-bus]], not prompt rewrites.

## Why three shapes, not more

The deck's 19 automation opportunities all reduce to these three because the underlying activities reduce to them: **read documents** (extract), **write documents** (generate), **manage transitions** (route). A given phase often touches more than one shape — P4 has both an extract component (parse the CIM) and a generate component (draft the memo) — but each component is one of the three. Hybrid phases are decomposed into multiple skills, each cleanly one shape.

## How to pick the shape for a new build

The deciding question is **what does the output look like?**

- If the output is a JSON of structured fields — extract-and-validate.
- If the output is prose (memo, narrative, narrative within a structured frame) — generate-with-review.
- If the output is a state record (status, next action, owner) — route-and-track.

Once the shape is fixed, the [[library-artifact-bundle]] structure is determined: which artifact dominates, what the review profile looks like, where the artifact lands in Arrakis.

## Related Concepts

- [[opportunity-register]] — the full opportunity list this taxonomy organizes
- [[library-artifact-bundle]] — the construction pattern shaped by the shape
- [[compliance-certificate-parser-pilot]] — concrete instance of extract-and-validate
- [[posting-memo-friction]] — flagship generate-with-review target
- [[hitl-state-machine]] — the review-gate variant per shape

## Sources

- `deal_lifecycle_automation_051326_vJA.pdf`, slide 06
