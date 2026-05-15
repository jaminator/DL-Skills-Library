---
name: dl-memo-posting-backup
description: >-
  Populates the Overland Advantage Posting Memo Backup (.xlsx) from a CIM or CIP
  using Python/openpyxl. Extracts financial data, maps periods to template columns,
  sizes the capital structure per Overland structuring rules, and writes input cells
  while protecting all formulas. The blank template is bundled in assets/ — no
  attachment needed. Activate when a user uploads a CIM/CIP and asks to populate
  the backup — including phrases like "run the backup," "fill in the numbers,"
  "populate the FinSum," "build the SUCAP," or "run the numbers on this deal."
  Do NOT activate for general Excel tasks or financial modeling unrelated to the
  posting memo backup template.
---

# Populating the Posting Memo Backup

## Overview

Extracts data from a CIM/CIP, maps it to the FinSum and SUCAP tabs of the Overland
posting memo backup template, and writes values to input cells only. Detailed FinSum
and Returns tabs are downstream formula-driven — never touch them.

**Template asset (bundled — no upload required):**
```
assets/_Company_-_Posting_Memo_Backup_vTemplate.xlsx
```
The blank template lives at the path above inside the skill folder. Step 5 copies it
to the working directory at runtime before writing. Never write back to the assets/
copy — always work from the copy in /home/claude/.

**References (read before first use):**
- [reference/cell-map.md](reference/cell-map.md) — authoritative cell addresses, input vs. formula status, date architecture
- [reference/fccr-addback-guide.md](reference/fccr-addback-guide.md) — Tier 1/2 classification, P12 override syntax
- [reference/structuring-rules.md](reference/structuring-rules.md) — sizing math, pricing defaults, Overland RCF/DDTL rules, bespoke escalation
- [reference/EXAMPLES.md](reference/EXAMPLES.md) — worked population examples
- [reference/CHANGELOG.md](reference/CHANGELOG.md) — version history and breaking changes

## Dependencies

```bash
pip install openpyxl --break-system-packages
```

pdfplumber may be needed for text-extractable PDFs:
```bash
pip install pdfplumber --break-system-packages
```

## Workflow

### Step 0: Gather User Inputs (MANDATORY GATE)

**This step must complete before any CIM reading begins.** If the user's invocation
message does not provide all four items below, halt and ask in a **single message**.
Check the CIM filename and any accompanying text for clues, but do not begin
extracting CIM data until all four are confirmed.

All four items — including the blank-vs-estimate caveat for cash taxes — **must
appear in one message**. Do not split them across multiple messages or follow-ups.

1. **Expected close date** — confirm if stated in the user's message; ask if not
2. **Target cash at close** ($000s) — confirm if stated; ask if not
3. **Current SOFR rate** — for FCCR interest expense (decimal, e.g. 0.0435)
4. **Cash taxes** ($000s, annual run-rate) — for FCCR P13. Include inline:
   "If you don't have a cash tax figure, I'll leave P13 blank rather than estimating."

If the user's invocation message already provides all four items, confirm them and
proceed directly to Step 1 without re-asking.

Do NOT proceed to Step 1 until the user responds.

### Step 1: Read the CIM (Adaptive Strategy)

CIMs arrive in varied formats. Use an adaptive reading strategy:

1. **Check file type.** If the PDF is actually a ZIP of images (common for slide decks),
   unzip and read pages visually with the `view` tool.
2. **Try text extraction first.** Use pdfplumber on each page. If a page yields
   meaningful text (>50 chars of non-boilerplate), use the extracted text.
3. **Fall back to vision.** For pages where text extraction fails or returns garbled
   output — especially charts, tables, and visual layouts — read the JPEG directly
   with the `view` tool.
4. **Cross-reference critical financial pages.** For the S&U page and QoE bridge page,
   ALWAYS cross-reference text extraction against visual reading regardless of text
   quality. For other financial pages (financial summary, capex, NWC), cross-reference
   when text extraction quality is uncertain (garbled numbers, missing columns,
   formatting artifacts).

**Target pages to locate in every CIM:**
- Transaction overview / S&U (Sources & Uses, capital structure)
- Financial summary (Revenue, Gross Profit, EBITDA, CA EBITDA by period)
- EBITDA adjustment detail / QoE bridge
- Capital expenditures summary (maintenance vs. growth split)
- Net working capital summary (AR, CIE, Inventory, Prepaid, AP, BIE, DR, Accrued)
- **Projected FCF bridge / debt model page** — contains close-date LTM EBITDA, debt
  service projections, and cash flow waterfall. When the deal close date differs from
  the most recent FYE, this page is the primary source for LTM EBITDA at close.

### Step 2: Map CIM Periods to Template Columns

Read [reference/cell-map.md](reference/cell-map.md) for the full date architecture.

**Protocol — K2-first anchor rule:**

1. List all CIM periods (e.g., FY2022A, FY2023A, FY2024A, FY2025E, FY2026P...)
2. Identify which are historical actuals, which is the LTM stub (if any), and which
   are budget/projected
3. **Set K2 = the last actual fiscal year-end period.** This is the anchor for the
   entire column architecture.
4. **Derive G2 by working backward from K2:** G2 = EOMONTH(K2, −48). G2 is the only
   date input; H2–K2 cascade forward automatically via EOMONTH formulas.
5. Hardcode L2 to the LTM reporting date (see LTM rules below)
6. **Check M2:** The template formula is `=EOMONTH(K2,12)`. If this does not produce
   the correct first projection year, M2 must be overwritten with the corrected offset
   formula (e.g., `=EOMONTH(K2,24)` when projections are two years after K2). Document
   this as an intentional formula modification.
7. **Check column O (CAGR):** After setting G2, verify whether G data rows will be
   empty. If so, update O9, O11, O14, O23, O27, O28 formulas to reference the first
   populated data column instead of G. Replace both the date anchor (G$2 → [first]$2)
   and value reference (G11 → [first]11, etc.). These are intentional formula modifications.
8. R2 is formula-driven (`=EOMONTH(L2,-12)`) — do NOT write.
9. Column G data rows stay EMPTY (anchor column, no data).

**LTM column rules:**

- **Explicit LTM in CIM:** Hardcode L2 to the LTM reporting date. Populate L data
  rows with LTM figures.
- **No explicit LTM but close date within 6 months of most recent FYE:** Treat the
  most recent FYE as the LTM column. Set L2 = most recent FYE date. Populate L data
  rows with the same figures as the FYE column (or, when LTM = K2 period, link R data
  cells to K via formula — e.g., `R11 = =K11` — rather than writing independent
  hardcoded inputs). Flag in column map: "No separate LTM period in CIM — mapping
  FY[XXXX]A to L2 as LTM proxy given close-date proximity. Confirm?"
- **Close-date LTM EBITDA override:** If the CIM discloses an EBITDA figure
  specifically tied to the closing date or labeled "pro forma at close" (commonly on
  the FCF bridge / debt model page), use that as the L23 (CA EBITDA LTM) value rather
  than the most recent FYE QoE figure. Flag the source page and value in the
  extraction summary.
- **L9 label note:** When L2 = a FYE date, the template's L9 formula will display
  "LTM M/YYA" instead of "FY'YYA." Flag in the column map and output summary:
  "L2 falls on a FYE date — L9 will display as 'LTM [M/YY]A.' Manually update the
  L9 formula in Excel to display 'FY'[YY]A' for consistency."

**Present the column map to the user and WAIT for confirmation:**

```
CIM Period       → Col → Date in Row 2    → Write Data?
─────────────────────────────────────────────────────────
(anchor, blank)  → G   → [derived from K2] → No (CAGR anchor)
FY20XXA          → H   → (auto from G2)    → Yes
FY20XXA          → I   → (auto)            → Yes
FY20XXA          → J   → (auto)            → Yes (= K2 last actual FYE)
FY20XXA / LTM    → L   → [hard or FYE]     → Yes
FY20XXE          → K   → (auto)            → Yes
FY20XXP          → M   → (auto or adjusted)→ Yes
Prior-Year LTM   → R   → (auto from L2)    → Yes (if data; link to K if LTM=FYE)
```

**Edge cases — halt and ask before proceeding:**
- Non-calendar FYE (EOMONTH cascade math changes)
- LTM date very close to FYE (dedicated column vs. treat as FY?)
- More historical periods than available columns (which to prioritize?)
- M2 or column O formula adjustments needed (present the specific changes)

### Step 3: Extract Data — Structured Summary

Build an extraction summary table with EVERY value found. Enforce the as-reported
vs. adjusted distinction at this step:

| Row | Metric | Type | H (FY22) | I (FY23) | J (FY24) | K (FY25E) | L (LTM) | M (FY26P) | R (PY LTM) |
|-----|--------|------|----------|----------|----------|-----------|---------|-----------|-------------|
| 11 | Revenue | As-reported | ... | ... | ... | ... | ... | ... | ... |
| 14 | Gross Profit | As-reported | ... | ... | ... | ... | ... | ... | ... |
| 18 | EBITDA Reported | As-reported | ... | ... | blank? | blank? | ... | blank? | ... |
| 23 | CA EBITDA | Adjusted | ... | ... | ... | ... | ... | ... | ... |
| 27 | Maintenance Capex | As-reported | ... | ... | ... | ... | ... | ... | ... |
| 28 | Growth Capex | As-reported | ... | ... | ... | ... | ... | ... | ... |

**Non-negotiable rules:**
- Revenue (Row 11): as-reported ONLY. Never use adjusted/pro forma revenue.
- Gross Profit (Row 14): as-reported ONLY. **If as-reported gross profit is
  unavailable but the CIM discloses contribution margin**, offer to relabel C14
  (e.g., "Contribution Margin") and populate with contribution margin figures.
  Flag the substitution in the extraction summary.
- EBITDA Reported (Row 18): populate ONLY where CIM explicitly discloses unadjusted
  EBITDA (e.g., "Definitional EBITDA" from a QoE bridge). Leave blank for periods
  where only adjusted EBITDA is shown.
- CA EBITDA (Row 23): the ONLY adjusted line. Use the CIM's highest-level adjusted
  EBITDA ("PF Adjusted EBITDA," "Company Adjusted EBITDA," final QoE bridge line).
- **Blank = not disclosed.** Never write 0 for missing data — zeros corrupt y/y
  growth and CAGR formulas.
- **Never hallucinate.** If the CIM doesn't disclose a figure, leave the cell empty.
- If the CIM presents only adjusted revenue or adjusted gross profit, FLAG THIS
  explicitly in the summary — it may indicate a data quality issue.
- **Cash taxes (P13):** If the user provided a cash tax figure in Step 0, use it.
  If not provided and CIM does not disclose historical cash taxes, leave P13 blank.
  Do NOT estimate or infer a cash tax figure.

Also extract NWC line items (rows 46–49, 52–55) and SUCAP data (S&U, pricing, terms).

**Present the full extraction summary to the user and WAIT for confirmation.**

### Step 4: Apply Overland Structuring Rules

Read [reference/structuring-rules.md](reference/structuring-rules.md).

**4a. Standard vs. bespoke check:**
Scan the CIM for any of: HoldCo debt, PIK notes, seller notes, preferred equity,
minority equity raises, earn-outs, multiple equity tranches, non-standard structures.

- **If bespoke deal**: HALT and present per the bespoke escalation protocol in
  structuring-rules.md. Wait for confirmation.
- **If standard deal** (senior credit facility only: RCF + TL + optional DDTL):
  proceed to 4b.

**4b. Derive Overland capital structure independently:**
Before accepting any user-provided capital structure figures, apply Overland
structuring rules to derive the proposed structure:

1. **RCF commitment** — auto-sizes via U32 formula (≈1× LTM CA EBITDA)
2. **RCF funded at close** — apply the Overland RCF Funding Rule (see
   structuring-rules.md): Funded RCF = Overland RCF commitment − CIM RCF commitment.
   Deduct the funded increment from CIM TL.
3. **Term Loan** — CIM TL minus any RCF funded increment
4. **DDTL** — apply the Overland Proactive DDTL Sizing Rule (see structuring-rules.md):
   Size at 20–30% of funded TL (preference: bottom of range). F13 = 0 (funds post-close);
   U34 = derived commitment amount.

**4c. No S&U page in CIP:**
If the CIM/CIP contains no Sources & Uses page and no proposed capital structure
(common in early-stage sell-side processes or DCM marketing CIPs where terms are
not yet set), HALT and:

1. Flag the absence: "No S&U or proposed capital structure found in the CIP."
2. Solicit from the analyst in a single message:
   - Proposed TL size or leverage target (e.g., "$80M TL" or "4.0× LTM EBITDA")
   - RCF funded amount at close (or confirm $0 if fully undrawn)
   - Use-of-proceeds labels and amounts (e.g., Refi Existing Debt, Shareholder
     Distribution, etc.)
3. Once received, apply Overland RCF Funding Rule and DDTL Proactive Sizing Rule
   using the analyst-provided TL as the starting point. Present the derived structure
   per the standard extraction summary template and wait for confirmation.

See [reference/structuring-rules.md](reference/structuring-rules.md) for the
full no-S&U protocol.

**Present the derived structure in the extraction summary:**
```
PROPOSED OVERLAND STRUCTURE (derived from structuring rules):
  RCF commitment (auto): ~$XXM (= ≈1× LTM CA EBITDA via U32 formula)
  RCF funded at close (F11): $XM (= Overland RCF $XXM − CIM RCF $XXM)
  Term Loan (F12): $XXM (= CIM TL $XXXM − RCF funded increment $XM)
  DDTL commitment (U34): $XXM (= ~20% of TL, rounded to nearest $1M)
  DDTL funded at close (F13): $0 (standard — funds post-close)
```
Wait for user confirmation. If the user overrides any derived amount, accept but
flag the deviation: "Note: User override — [cell] set to $X vs. rule-derived $Y."

### Step 5: Write to Template

```python
import shutil, os, openpyxl

SKILL_ASSETS = '/mnt/skills/user/dl-memo-posting-backup/assets'
TEMPLATE_FILENAME = '_Company_-_Posting_Memo_Backup_vTemplate.xlsx'

# Copy blank template from skill assets to writable working dir — assets/ is read-only
template_path = f'/home/claude/{TEMPLATE_FILENAME}'
shutil.copy(os.path.join(SKILL_ASSETS, TEMPLATE_FILENAME), template_path)

# NEVER use data_only=True — it destroys formulas permanently
wb = openpyxl.load_workbook(template_path)
```

**Pre-write validation (MANDATORY):**
Before writing any cell, check that the target cell does not contain a formula:

```python
def is_formula(cell):
    """Check if cell contains a formula or ArrayFormula."""
    if isinstance(cell.value, str) and cell.value.startswith('='):
        return True
    if hasattr(cell.value, 'text'):
        return True
    return False

# Build write plan as list of (sheet, cell_addr, value, source_page)
write_plan = [...]

# Validate EVERY cell in the write plan
for sheet_name, addr, value, source in write_plan:
    ws = wb[sheet_name]
    cell = ws[addr]
    if is_formula(cell):
        print(f"BLOCKED: {sheet_name}!{addr} contains formula: {cell.value}")
        print(f"  Attempted value: {value} (from CIM page {source})")
        # HALT and ask user
```

**Intentional formula modifications (exempt from pre-write block):**
Some cells require deliberate formula changes — these are NOT errors. Track them
separately from the write plan and apply after validation:
- M2: when the standard `=EOMONTH(K2,12)` produces the wrong projection year
- O9, O11, O14, O23, O27, O28: CAGR column updates when G data rows are empty
- R data cells: when LTM = FYE and R cells should link to K (e.g., `R11 = =K11`)
- P12: Tier 1/Tier 2 FCCR override (analyst decision)

Log all intentional formula modifications in the output summary.

**Write sequence:**
1. FinSum C1: Company name
2. FinSum G2: FY anchor date (datetime object, derived from K2-first rule)
3. FinSum L2: LTM reporting date (datetime object)
4. Intentional formula modifications: M2, column O, column R (if applicable)
5. FinSum data rows: Revenue, GP (or Contribution Margin with relabeled C14),
   EBITDA Reported, CA EBITDA, Capex, NWC items
6. SUCAP sources: F11 (RCF drawn), F12 (TL), F13 (DDTL funded at close)
7. SUCAP uses: H11–H14 (labels), K11–K14 (amounts)
8. **SUCAP uses clean-up:** Blank any remaining "[Use]" placeholder rows between
   the last populated use and the Financing Fees row (H15/K15) so all uses are
   continuous. Write empty strings to unused H13/H14 labels and 0 to unused K13/K14
   if they still contain "[Use]" placeholders.
9. SUCAP pricing: S32/T32 (RCF), S33/T33 (TL) — S34/T34 auto-copy from TL
10. SUCAP other: S17 (SOFR), I30 (cash), J41 (TEV multiple), U34 (DDTL commitment),
    P13 (cash taxes — only if user provided; leave blank otherwise)
11. If analyst wants Tier 1/Tier 2 FCCR: override P12 per
    [reference/fccr-addback-guide.md](reference/fccr-addback-guide.md)

**Post-write S&U balance validation:**
See [reference/structuring-rules.md](reference/structuring-rules.md) for the
balance check script. Note: K15 is a formula cell — compute OID fees from write-plan
inputs rather than reading K15 via data_only.

**Save and deliver:**
```python
output_path = '/mnt/user-data/outputs/Company_Posting_Memo_Backup_MMDDYY.xlsx'
wb.save(output_path)
```

### Step 6: Output Summary

After saving, present a plain-text summary:

```
POPULATION SUMMARY
==================
Company: [Name]
Template: Posting Memo Backup
Date: [today]

COLUMN MAP (as confirmed):
  G = anchor ([date], no data)
  H = FY'XXA, I = FY'XXA, J = FY'XXA
  K = FY'XXA (last actual FYE)
  L = LTM / FY'XXA ([date], hardcoded)
  M = FY'XXE ([date])

POPULATED CELLS: [count]
  FinSum: C1, G2, L2, [list data cells written]
  SUCAP: F11, F12, F13, K11-K16, S17, S32, T32, S33, T33, U34, ...

INTENTIONAL FORMULA MODIFICATIONS:
  - [list any M2, column O, column R, or P12 formula changes with rationale]

OVERLAND STRUCTURING:
  RCF commitment (auto via U32): ~$XXM
  RCF funded at close (F11): $XM [rule-derived / user override]
  Term Loan (F12): $XXM
  DDTL commitment (U34): $XXM [rule-derived / user override]
  DDTL funded at close (F13): $0

LEFT BLANK (not disclosed in CIM):
  - [list with reason]

FLAGS FOR ANALYST FOLLOW-UP:
  - [data quality issues, unusual items, CIM ambiguities]
  - [L9 label note if L2 = FYE date]
  - [Owner Equity plug note if CIM lists "Cash from Balance Sheet"]

SOFR RATE USED: [rate]
CASH TAXES (P13): [value or "left blank — analyst to provide"]

NOTE: openpyxl does not evaluate formulas. Formula cells will display
stale cached values until opened in Excel. All formulas are intact.
```

Use `present_files` to deliver the .xlsx.

## Key Constraints

- **Columns G data rows are ALWAYS empty** — anchor column only
- **H2–K2, M2, R2 are ALWAYS formulas** — never write dates to these cells
  (exception: M2 may be overwritten with an adjusted formula when needed)
- **Row 22 (Adjustments) is ALWAYS a formula** (= CA EBITDA – Reported EBITDA)
- **Row 29 (Total CapEx) is ALWAYS a formula** (= Maintenance + Growth)
- **All of Detailed FinSum and Returns tabs are off-limits**
- **SUCAP U32, F14, S34, T34, K15 are formulas** — see cell map for complete list
- **FinSum G61 (DSO) contains ArrayFormulas** — never overwrite

## Anti-patterns

These are the existing constraints above, surfaced as explicit do-nots. Nothing
here is new behavior — it restates the formula-protection, blank-≠-zero, and
never-hallucinate rules already in force.

- **Do not write to any formula cell.** Run the mandatory `is_formula()` pre-write
  gate on every cell in the write plan. H2–K2, M2, R2, Row 22, Row 29, SUCAP U32,
  F14, S34, T34, K15, and FinSum G61 (ArrayFormula) are formulas — never overwrite
  them except for the explicitly enumerated intentional formula modifications (M2,
  column O CAGR cells, R-when-LTM=FYE, P12 override).
- **Do not write 0 for missing data.** Blank ≠ zero. A zero corrupts y/y growth and
  CAGR formulas. If the CIM does not disclose a figure, leave the cell empty.
- **Do not hallucinate or infer figures.** If the CIM does not disclose it, leave it
  blank — including cash taxes (P13), which is never estimated or inferred.
- **Do not use adjusted/pro forma revenue or gross profit.** Rows 11 and 14 are
  as-reported only. Row 23 (CA EBITDA) is the only adjusted line.
- **Do not touch the Detailed FinSum or Returns tabs.** They are entirely
  downstream formula-driven — do not read from or write to them.
- **Do not write back to the bundled assets/ template.** Always copy it to the
  working directory and write to the copy.
- **Do not skip the Step 0 gate or the column-map / extraction-summary / bespoke
  confirmation gates.** Proceed only after the user confirms.
- **Do not load the workbook with `data_only=True`** — it destroys formulas
  permanently.

## CIM-to-Template Mapping Notes

Common CIM label → Template row mapping:
- "Total Revenue" / "Net Revenue" → Row 11 (as-reported)
- "Gross Profit" / "Gross Margin $" → Row 14 (as-reported)
- "Contribution Margin" → Row 14 (only if GP unavailable; relabel C14)
- "Definitional EBITDA" / "Reported EBITDA" / "GAAP EBITDA" → Row 18
- "Diligence Adjusted EBITDA" / "PF Adjusted EBITDA" / "Company Adjusted EBITDA" → Row 23
- "Pro Forma Adjusted EBITDA — Closing Stub" / "EBITDA at Close" → Row 23 LTM column (L23)
- "Maintenance CapEx" → Row 27; "Growth CapEx" → Row 28
- "Trade Accounts Receivable" → Row 46 (AR)
- "Contract Receivables" / "Costs in Excess of Billings" → Row 47 (CIE)
- "Inventory" → Row 48
- "Prepaid Expenses" + "Other Current Assets" → Row 49
- "Accounts Payable" → Row 52
- "Deferred Revenue" → Row 54
- "Accrued Wages" + "Accrued Insurance" + "Other Accrued" → Row 55

**Subscription / asset-service companies:** Payment obligations to asset owners or
third-party equipment owners (e.g., "Tank Owner's Payments") should generally map to
Row 52 (Accounts Payable) rather than Row 55 (Accrued & Other) unless clearly
contingent or estimated in nature.

When the CIM's NWC breakdown doesn't map 1:1 to template rows, use best judgment
and flag the mapping in the extraction summary for analyst review.

## Portability into Arrakis

This skill is the **quantitative half** of the P4 Posting Memo bundle (Stage 2 /
P4 — Origination & Screening), paired with the narrative `dl-memo-posting` skill.
Its shape is **extract-and-validate** (deterministic cell mapping under formula
protection), the mirror of the compliance-certificate parser's extract → recompute
→ flag pipeline; it maps into the Arrakis screening application alongside the rest
of the [[library-artifact-bundle]] P4 pair.

The structured-output contract is `schemas/posting_memo_backup_extraction.py`
(`PostingMemoBackupExtraction`). It is always emitted in HITL state
`PENDING_REVIEW` with the `[DRAFT — HUMAN REVIEW REQUIRED]` watermark on the
extraction summary the analyst confirms before any cells are written. When the
artifact graduates, the underlying prompt is invoked through Spice and the
structured extraction summary lands in the screening application's `_LAND` tier;
the populated `.xlsx` remains a script/skill-produced deliverable, so there is
nothing to inject into the workbook beyond what the skill already writes
(D-2: nothing-to-inject — the output is the workbook itself).

`reference/CHANGELOG.md` is retained as **historical context** (the
Skills_Best_Practices "old patterns" carve-out): it records the v1→v2→v3 QA
remediation history and the then-current file trees. Its references to the
pre-rename skill name are historical record, not live runtime paths, and are
intentionally preserved verbatim.
