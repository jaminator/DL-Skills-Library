# `raw/` — Source Document Drop Zone

This folder is the unstructured intake layer of the LLM Wiki. It is a **flat folder** — no subfolders. Maintainers drop source documents here; the `wiki-editor` agent reads them and compiles structured pages into `wiki/`.

## Filename convention

Use the pattern `<topic>-<descriptor>.<ext>`. Topic is a short stable category-like prefix; descriptor narrows it. Lowercase, hyphens, no spaces.

Good examples:
- `credit-standards-investment-policy.pdf`
- `template-posting-memo.docx`
- `sector-saas-dd-checklist.md`
- `precedent-clauses-incremental-facility.txt`
- `playbook-non-sponsored-sourcing.pdf`
- `policy-conflicts-cross-strategy-allocation.md`

Avoid:
- Spaces, underscores, mixed case (`Credit Standards Investment Policy.pdf`).
- Live-deal artifacts (e.g., a real CIM, a real model, a real IC memo). The wiki contains institutional knowledge, not deal state.
- Deeply nested topics — keep the prefix one or two words.

## Immutability rule

The `wiki-editor` agent reads `raw/` and **never writes to it**. No agent or process modifies files placed here. If a source needs replacement, drop the new version with a versioned descriptor (`<topic>-<descriptor>-v2.<ext>`) and let the wiki-editor reconcile during the next ingest pass.

## Workflow to add a source

1. Drop the file into `raw/`, using the filename convention.
2. Run `scripts/wiki-check.sh` from the repo root. The script compares modification timestamps in `raw/` against entries in `wiki/log.md` and updates `progress.json.wiki.pending_raw_files`.
3. On the next Claude Code session that triggers the `wiki-editor`, the agent ingests pending files, writes one or more wiki pages per source, updates `wiki/index.md`, and appends to `wiki/log.md`.

## What does not belong here

- Live-deal documents (CIMs, models, IC memos for active deals). These belong in the relevant Claude Desktop deal project, not in the institutional knowledge wiki.
- Fund-level economics and IC deliberation content (RESTRICTED). The wiki may reference policy or process but never embed restricted figures.
- Personal notes intended for a single maintainer. These belong outside the repository.
