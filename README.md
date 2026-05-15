# Direct Lending Underwriting Library

A Claude-based knowledge and automation library supporting a direct lending firm's non-sponsored US middle-market underwriting team across the 6-stage, 19-phase deal lifecycle.

This repository is the **development environment** for the library. The UW team consumes the library exclusively through **Claude Desktop**, using the assets curated here. Maintainers iterate using Claude Code.

---

## What lives where

| Folder | Purpose | Audience |
| --- | --- | --- |
| `docs/sources/` | Canonical sources (deal lifecycle deck, Arrakis blueprint) | Maintainers + Claude Code |
| `docs/anthropic/` | Anthropic best-practices references (prompting, skills, agent teams) | Maintainers + Claude Code |
| `raw/` | Flat drop zone for unstructured source documents | Maintainers (write); `wiki-editor` agent (read) |
| `wiki/` | LLM-curated, interlinked institutional-knowledge wiki (Obsidian-compatible) | All sessions read; `wiki-editor` agent writes |
| `agents/` | Specialist agent definitions used by Claude Code | Claude Code |
| `skills/` | Skill packages (Claude Skills format) for distribution | Distribution → Claude Desktop |
| `prompts/` | Cache-eligible prompt templates organized by deal stage and phase | Distribution → Claude Desktop |
| `project-instructions/` | Per-stage Claude Desktop project instructions | Distribution → Claude Desktop |
| `system-instructions/` | Per-role system instructions (added in follow-on iteration) | Distribution → Claude Desktop |
| `schemas/` | Pydantic models for structured outputs | Maintainers (Snowflake parity in Arrakis) |
| `scripts/` | Repo maintenance scripts | Maintainers |
| `dist/` | Distribution artifacts (compiled, self-contained) | Future build pipeline |

---

## Two environments

**Development.** This repository. Maintainers and Claude Code see everything. Source of truth.

**Distribution.** Claude Desktop. Users see only what is copy-pasted into their project. Distribution artifacts are fully self-contained — no filesystem paths, no git references, no "check the wiki" instructions.

---

## How to extend the library

1. **Add a source document.** Drop the file into `raw/` using the convention `<topic>-<descriptor>.<ext>` (e.g. `credit-standards-investment-policy.pdf`, `sector-saas-dd-checklist.md`). Run `scripts/wiki-check.sh` to register it as pending. The `wiki-editor` agent ingests it on the next session.
2. **Author a new skill, prompt, or instruction.** Re-read the relevant best-practices file in `docs/anthropic/` first. Place the artifact in the appropriate folder. Conform to the construction rules in `CLAUDE.md`.
3. **Commit per phase.** Use `feat: phase-<n> <deliverable>` for build phases. Standard Conventional Commits otherwise.

---

## Initial build status

The initial build (Phases 0–4) produces:

- The Phase 0 scaffold.
- A wiki seed compiled from the two canonical sources.
- One pilot vertical slice (skill + prompt + project instruction + Pydantic schema) for the user-confirmed pilot phase.
- A pilot self-validation report at `docs/pilot-validation.md`.

Out of scope for the initial build: additional phase coverage, a CI/CD distribution pipeline, role-based system instructions, additional specialist agents.

See `CLAUDE.md` for the full conformance contract.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file
for details.

## Ownership

This repository is developed and maintained by Jamie Anderson in a personal
capacity. It is not produced, sponsored, or maintained on behalf of any
employer, and the views, code, and design decisions represented here are those
of the author alone.

## Company Collaboration

The original author, Jamie Anderson, may from time to time permit Centerbridge
Partners L.P., its affiliates, and other Persons (including without limitation
their partners, employees, advisors, consultants, and any other natural
persons or entities designated by Jamie Anderson) to view, use, edit,
contribute to, or otherwise work with this codebase in separate forks,
branches, cloned repositories, or other derivative or related code bases,
whether internal or external. Any such activity, and any such forks, branches,
clones, or related code bases, do not change, limit, or otherwise affect the
licensing of this repository, which remains licensed under the MIT License.
