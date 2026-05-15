---
title: Form Credit and Guaranty Agreement
category: deal-templates
tags: [precedent, governance, policy, template]
sources:
  - "Overland Form Credit and Guaranty Agreement.docx"
last_updated: 2026-05-15
---

# Form Credit and Guaranty Agreement

The firm's standard precedent senior secured credit and guaranty agreement. It is **not** a per-deal fill-in template — its bracketed placeholders (`[___]:1.00` covenant grids, `[Reserved]`, sponsor-fee carve-outs) mark deal-negotiated variables. It plays two structural roles: the precedent the P14 Credit Agreement is negotiated from, and the **covenant source of truth** that post-close monitoring tests against. Every downstream covenant calculation in the library traces back here.

## Article map

Twelve articles: (1) Definitions and Rules of Interpretation — including §1.6 Financial Covenant Calculations, §1.8 Limited Condition Transactions; (2) Loans and Letters of Credit — including §2.11 Uncommitted Incremental Facility; (3) Representations and Warranties (§§3.1–3.27); (4) Affirmative Covenants — §4.1 Financial Statements and Other Reports is the compliance-certificate delivery hook; (5) Negative Covenants (debt, liens, dispositions, restricted distributions, investments, affiliate transactions, sponsor fees, AML/anti-corruption); (6) **Financial Covenants**; (7) Conditions — §7.3 Conditions to Each Delayed Draw Term Loan; (8) Events of Default; (9) Expenses and Indemnity; (10) Guaranty; (11) Administrative Agent; (12) Miscellaneous — §12.5 Amendments and Waivers, §12.6 Assignments.

## Financial-covenant architecture

This is the high-value core the [[compliance-certificate-parser-pilot]] must replicate exactly:

- **§6.1 Fixed Charge Coverage Ratio** = (Consolidated EBITDA less cash capex funded from internally generated cash, trailing four quarters) ÷ Fixed Charges, tested quarter-end against a per-quarter minimum grid.
- **§6.2 Total Debt to Consolidated EBITDA Ratio** ≤ a per-quarter maximum grid, tested quarterly.
- **§6.4 Equity Cure Right** — a "Specified Equity Contribution" curing within 10 business days of financial-statement delivery, constrained to no two consecutive cured quarters in any four, max four cures post-closing, capped at the amount needed to cure, and disregarded for all other EBITDA-based basket/pricing math.
- **Consolidated EBITDA build** = Consolidated Net Income plus (without duplication, to the extent deducted) interest expense, tax expense, depreciation & amortization, specified non-cash charges, and capped transaction fees/costs — a standard sponsor-style adjusted-EBITDA stack.

The agreement defines roughly 232 terms; the covenant-relevant chain (`Consolidated EBITDA`, `Consolidated Net Income`, `Fixed Charges`, `Fixed Charge Coverage Ratio`, `Total Debt to Consolidated EBITDA Ratio`, `Test Period`, `Internally Generated Cash`, `Delayed Draw Term Loan`, `Specified Transaction`) also gates Article 5 baskets and the §2.11 incremental facility.

## Why it is the system backbone

The same covenant definitions cascade through the [[closing-and-am-templates|closing memo digest, compliance tracker, DDTL draw calc, and amendment memo]]. If those four artifacts each re-encode the math independently they will drift; the design intent is a single shared covenant-definition source derived from this document. The §1.6 calculation conventions (pro forma adjustments, Specified Transactions, Limited Condition Transactions) are as load-bearing as the ratio grids themselves — a parser that ignores §1.6 will mis-compute even with correct ratio formulas. §12.5 defines what can be amended and at which voting threshold, which is the precedent the [[term-sheet-and-ic-templates|amendment workflow]] operates within.

This is firm-proprietary legal precedent — RESTRICTED, never externally distributed. It is institutional reference material, so the wiki captures its structure and covenant architecture rather than transcribing clauses; downstream agents needing exact language refer to the source.

## Related Concepts

- [[compliance-certificate-parser-pilot]] — encodes this article 6 / §1.6 logic
- [[closing-and-am-templates]] — the monitoring artifacts that test against it
- [[market-deal-terms-reference]] — market context for negotiating its bracketed variables
- [[term-sheet-and-ic-templates]] — the term sheet negotiated toward this precedent
- [[template-input-schema]] — supplies the covenant/EBITDA vocabulary for the bucket library
- [[restricted-content-discipline]] — handling of firm-proprietary legal precedent

## Sources

- `Overland Form Credit and Guaranty Agreement.docx`, Article 1 (§1.6), Article 5, Article 6, §2.11, §7.3, §12.5–12.6
