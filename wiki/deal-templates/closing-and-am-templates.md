---
title: Closing and Asset-Management Templates (P16–P19)
category: deal-templates
tags: [template, process, governance, risk]
sources:
  - "[Company] - Overland Closing Memo (MM-DD-YY) vTemplate.docx"
  - "[Company] - Closing Memo Backup (MM-DD-YY) vTemplate.xlsx"
  - "[Company] - Overland Amendment Memo (MM-DD-YY) vTemplate.docx"
  - "[Company] - Compliance Certificate Tracker_vTemplate.xlsx"
  - "[Company] - DDTL Draw Calc (MM-DD-YY) vTemplate.xlsx"
last_updated: 2026-05-15
---

# Closing and Asset-Management Templates (P16–P19)

This cluster spans the underwriting-to-asset-management hand-off and the recurring post-close controls. It is where the [[closing-and-asset-management|most under-instrumented stages]] live and where two of the library's highest-yield extract-and-validate targets sit.

## Closing Memo + Backup (P16)

The **Closing Memo** (.docx) is the definitive post-execution record and the formal hand-off from deal team to Asset Management (distribution spans IC, AM, legal, IR, operations). Sections: executive summary; final sources & uses / pro forma capitalization; an investment summary with pricing/amortization/unused-fee grids and a **covenant summary table** (TNL/FCCR/min-liquidity vs documentation triggers); a **legal documentation overview** that digests the executed credit agreement (maturity, prepayment premium, DDTL governor, ECF sweep & step-downs, EBITDA definition & add-back caps, deemed EBITDA by quarter, reporting cadence, equity-cure mechanics, Required-Lenders voting, intercreditor triggers, events of default); an ESG overview; and a trade-ticket exhibit. The **Closing Memo Backup** (.xlsx, six sheets — `SUCAP`, `Detailed FinSum`, `Pricing Grid - Covenant`, `Bank Group`, `Returns`, `Trade Ticket`) is the calc engine; its sheets mirror the memo's exhibits one-to-one, the same pairing the [[screening-templates|posting-memo backup]] has to the posting memo. Inputs: the executed credit agreement, final funds flow, KYC/board resolutions, allocations. The memo's covenant digest is the authoritative baseline that downstream monitoring tests against.

## Compliance Certificate Tracker (P17, .xlsx)

A single wide sheet, reporting periods as columns (`EOMONTH`-driven), covenant build as rows: a Consolidated EBITDA build (GAAP net income → exclusions → reported EBITDA → add-backs classified **Definitional vs Diligence** → deemed EBITDA), individual & shared add-back caps, the Total Net Leverage test (with cash-netting cap), the FCCR test, and the minimum-liquidity test — each shown **Reported (borrower-stated) vs Covenant (independently recomputed)** side-by-side. This is the manual control that catches CFO arithmetic errors today, and it is exactly the spreadsheet the [[compliance-certificate-parser-pilot]] automates. The Definitional-vs-Diligence add-back typing is the key structured-vocabulary item; the Reported/Covenant column separation is the load-bearing audit control and must be preserved.

## DDTL Draw Calc (P17, .xlsx)

A single-sheet pro forma leverage check for a delayed-draw term loan / RCF draw (typically an add-on acquisition), with LTM → Target → Pro Forma columns: an EBITDA build, sources & uses of the draw, and a pro forma capitalization yielding senior/total/net leverage multiples to test against the DDTL governor. Inputs: current LTM EBITDA from the compliance tracker, target/add-on QoE, the draw's sources & uses, and the governor definition from the credit agreement. This template directly closes the known P17 gap — DDTL draws approved over email with no compliance verification — and should be a required attachment to any draw approval.

## Amendment Memo (P19, .docx)

The IC / Asset-Management approval document for post-close amendments, waivers, and consents (including DDTL-governor waivers tied to add-on draws). Its core is a **Modification Summary table** comparing every term Original vs Proposed (facility size, pricing, fees, maturity, amortization, ECF, call protection, DDTL governor, covenants, EBITDA definition) with "No Change" / "Change Description" flags, plus refreshed projection cases and a second-way-out / distressed-sale-value section. Inputs: the original closing memo and executed agreement (the comparison baseline), the amendment request, and refreshed financials/model. It resets the monitoring baseline — amended levels feed back into the compliance tracker and DDTL calc — and is the governance wrapper that, paired with the DDTL draw calc, supplies the audit trail currently missing.

## Inputs, outputs, downstream

The cluster consumes the executed [[form-credit-agreement]] and the [[dd-analytical-workbooks|model/databook]] baseline. It produces the AM-onboarding record and the recurring covenant and draw controls. A single shared covenant-definition source (the credit agreement's financial-covenant article) must flow through all five so the closing digest, tracker, and draw calc test against identical math.

## Related Concepts

- [[compliance-certificate-parser-pilot]] — the P17 pilot that automates the tracker
- [[closing-and-asset-management]] — the lifecycle stages this cluster serves
- [[ic-and-asset-mgmt-gaps]] — the DDTL-draw and hand-off gaps it closes
- [[form-credit-agreement]] — the covenant source of truth
- [[closing-am-input-schema]] — the per-template input-bucket composition for this cluster
- [[template-library-overview]] — the full template chain

## Sources

- `[Company] - Overland Closing Memo (MM-DD-YY) vTemplate.docx`, section IV covenant digest
- `[Company] - Compliance Certificate Tracker_vTemplate.xlsx`, Reported-vs-Covenant build
- `[Company] - DDTL Draw Calc (MM-DD-YY) vTemplate.xlsx` / `[Company] - Overland Amendment Memo (MM-DD-YY) vTemplate.docx`
