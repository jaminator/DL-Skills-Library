---
title: Push Workflow
category: methodology
tags: [process, playbook, governance]
sources:
  - arrakis_blueprint_v2_3.md
  - deal_lifecycle_automation_051326_vJA.pdf
last_updated: 2026-05-15
---

# Push Workflow

All post-pilot build work in the library proceeds in **pushes**. A push is one full iteration of a fixed four-step loop. This page is the synthesized explanation; the binding instruction is the **Push workflow** section of `CLAUDE.md`. The two stay in lockstep — drift between them is a lint finding (the same discipline [[skill-naming-convention]] uses for its CLAUDE.md/registry pair).

## The four steps

1. **Plan.** Write `plan/push-<n>-plan-*.md` before any execution, after re-reading the binding best-practices files (conformance rule 1). The plan is a design contract: objective, artifacts, naming/lifecycle/shape, build sequence, evaluations authored before extensive docs, out-of-scope, and a mandatory execution-model section (below). Forward-looking.
2. **Execute.** Build strictly against the approved plan on the shared local `main` working tree (CLAUDE.md rule 10 — no worktrees/branches by default). Commit per the convention; commit and push on the rule-11 triggers.
3. **Log.** Write `push-logs/push-<n>-log.md` — the retrospective record: what was built, executional issues and lessons, the execution model actually used and whether it was right, and the recommended next build for push `<n+1>`. Retrospective, and deliberately distinct from the plan: `plan/` is forward-looking, `push-logs/` is the post-hoc record. This split directly addresses the lifecycle's recurring "summary built post hoc from memory" failure mode (see [[posting-memo-friction]]) by making the build's own audit trail a first-class artifact.
4. **Wiki UPDATE + LINT.** Record the push (UPDATE: add/extend the page, reconcile [[skill-naming-convention|index/log]] and `progress.json`), then run a full LINT pass per the wiki schema. LINT completion is a rule-11 push trigger.

`<n>` is closed only after step 4. The plan number and push number are the **same `<n>`**, incrementing by exactly 1 only after a full iteration completes — never reused, never advanced mid-iteration.

## Execution-model selection (mandatory in every plan)

Every plan must state which execution model the push uses, with rationale grounded in `docs/anthropic/Agent_Teams.md`:

- **Single agent, sequential — the default.** Correct for dependency-chained builds where almost no two steps are independent, which the [[library-artifact-bundle]] four-artifact bundle almost always is (inspect → scripts → references → SKILL.md → schema → prompt → project-instruction → evaluations → wiki). Parallel fan-out adds coordination and token cost with near-zero benefit; progress is tracked with a task list, not agent coordination.
- **Sub-agents (report-back).** For bounded, independent, parallelizable units that only need to return a result — a broad read-only validation sweep, or several genuinely independent skills with no shared script. The plan specifies each sub-agent's role and bounded deliverable.
- **Agent team (3–5 teammates, task-partitioned).** Only for genuinely parallel independent workstreams or competing-hypothesis investigation. Per Agent_Teams.md: 3–5 teammates, 5–6 tasks each, partitioned **by file** to avoid write conflicts (not by branch/worktree — rule 10 keeps the single shared `main` tree), monitored and steered, started on research/review-shaped work. The plan recommends concrete roles (one per independent skill, or reviewer lenses: schema/no-drift, best-practices conformance, evaluation).

Default to single-agent sequential and say why when in doubt.

## Worked precedent

Push-1 conformed the four production skills into `dl-*` bundles. Push-2 built the [[kickoff-data-request-bundle]] (`dl-ddq-kickoff`) and was the first push to also produce a `push-logs/` retrospective. Push-2 ran **single-agent sequential** — the textbook case: a fully dependency-chained four-artifact bundle where fan-out would have added cost with no parallel benefit. Its log records the executional lessons (no system Python, in-place `.docx` populator discipline, scratch-dir hygiene) that future script-bearing pushes inherit.

## Related Concepts

- [[library-artifact-bundle]] — the four-artifact unit each push builds
- [[skill-naming-convention]] — the sibling CLAUDE.md-binding / wiki-synthesized convention pair
- [[kickoff-data-request-bundle]] — push-2, the first full iteration to also produce a log
- [[compliance-certificate-parser-pilot]] — the pilot the post-pilot push workflow follows
- [[posting-memo-friction]] — the "summary built post hoc from memory" failure mode the log step counters

## Sources

- `arrakis_blueprint_v2_3.md`, build sequencing and HITL discipline
- `deal_lifecycle_automation_051326_vJA.pdf`, slide 06 (opportunity shapes informing execution-model choice)
