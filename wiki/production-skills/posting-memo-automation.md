---
title: Posting Memo Automation Skills
category: production-skills
tags: [skills, process, template]
sources:
  - overland-posting-memo.zip
  - populating-posting-memo-backup.zip
last_updated: 2026-05-15
---

# Posting Memo Automation Skills

The P4 posting-memo deliverable is automated by a **coupled pair** of skills that split it along the narrative/quantitative seam: `dl-memo-posting` (production deployment name: `overland-posting-memo`) produces the Word memo; `dl-memo-posting-backup` (production deployment name: `populating-posting-memo-backup`) produces the Excel backup that feeds its financial exhibits. Together they attack [[posting-memo-friction]] — the highest-yield single pain point in the lifecycle — by collapsing first-draft time on the most-frequently-drafted memo in [[origination-and-screening|Stage 2]]. They map onto the [[screening-templates]] artifacts (the Posting Memo `.docx` and Posting Memo Backup `.xlsx`).

## `dl-memo-posting` (production: `overland-posting-memo`) — the narrative

Populates the bundled Overland Posting Memo Word template **in place** via `scripts/populate_memo.py`, preserving Word auto-numbering and run-level bold/italic formatting — it returns a populated `.docx`, not a regenerated document. It drafts twelve mapped sections (deal header, situation/company overview, financial headline, six-bullet Discussion & Analysis, sources-&-uses note, the 15-item risk-flags grid, five strengths, five considerations, recommendation with color rating, designated criteria). Its discipline is heavily prescriptive and worth capturing as institutional knowledge:

- **"CA EBITDA" is the only EBITDA label** — never "Adjusted" or "Diligence Adjusted."
- **No posting-team follow-ups anywhere** — the memo reports facts; it never assigns tasks, recommends calls, or prescribes diligence steps, in any section.
- **No speculation or conditional hedging** — report what the data shows; flag deviation magnitude and direction, not causes.
- **Anchor to the operative LTM period** the financing is sized against; `TBD (source)` liberally rather than fabricate.
- Strengths ordered macro→micro (industry → competitive → demand → financial → structure); credit considerations framed for a senior secured lender, not an equity investor.

## `dl-memo-posting-backup` (production: `populating-posting-memo-backup`) — the calc engine

Extracts CIM/CIP financials with openpyxl into the `FinSum` and `SUCAP` tabs of the bundled backup template, **writing input cells only and protecting every formula** (a mandatory pre-write `is_formula` gate; detailed FinSum and Returns tabs are off-limits). Its load-bearing conventions:

- **K2-first date anchor.** K2 = last actual FYE; G2 derived backward (`EOMONTH(K2,−48)`); H–K cascade by formula. M2 and CAGR-column formulas are deliberately modified only when projections or empty anchor columns require it, and logged as intentional.
- **Blank ≠ zero.** Missing data stays empty — zeros corrupt growth/CAGR formulas; never hallucinate a figure.
- **Mandatory user gate** before reading any CIM: close date, target cash, SOFR, cash taxes, asked in one message.
- **Bespoke-deal escalation:** HoldCo/PIK/seller notes/preferred/earn-outs halt for analyst confirmation.

## Shared Overland structuring policy

The backup encodes firm structuring rules that are reusable institutional knowledge beyond this skill: the **Overland RCF Funding Rule** (funded RCF at close = Overland RCF commitment − CIM RCF commitment, with the increment deducted from CIM TL); **DDTL Proactive Sizing** (size to 20% of TL+DDTL even if the CIM omits a DDTL); the **owner-equity plug** (F14 = total uses − funded debt, absorbing "cash from balance sheet"); default tranche pricing; and the **FCCR Tier 1 / Tier 2 addback** discipline (default strips all addbacks to reported EBITDA; override P12 to retain only genuine Tier 2 normalizations). The analytical lens for D&A, strengths, and considerations is the [[overland-credit-framework]] base-rate evidence hierarchy — never fabricate industry base rates; never name academic authors in output.

## Why a pair, not one skill

The deliverable has two irreducibly different shapes: the memo is **generate-with-review** (prose judgment, watermarked for the reviewer); the backup is **extract-and-validate** (deterministic cell mapping under formula protection). Splitting them lets each carry the discipline its shape needs, and matches the template chain where the `.xlsx` outputs flow one-to-one into the `.docx` financial exhibits. Together they instantiate the [[library-artifact-bundle]] pattern for P4 in production.

## Related Concepts

- [[production-skill-inventory]] — the deployed-skill catalog
- [[posting-memo-friction]] — the P4 pain point this pair attacks
- [[screening-templates]] — the .docx/.xlsx templates these skills populate
- [[screening-input-schema]] — the input buckets these skills fill
- [[overland-credit-framework]] — the analytical spine (credit screen + base-rate hierarchy)
- [[library-artifact-bundle]] — the bundle pattern realized here in production
- [[opportunity-shapes]] — the two shapes the pair splits along

## Sources

- `overland-posting-memo.zip`, `SKILL.md` (section map, discipline rules) + `references/base-rate-framework.md`, `references/memo-sections.md`
- `populating-posting-memo-backup.zip`, `SKILL.md` (K2-first protocol, write gate) + `references/structuring-rules.md`, `references/fccr-addback-guide.md`, `references/cell-map.md`
