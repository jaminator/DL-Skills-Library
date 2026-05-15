# Cell Map — Posting Memo Backup Template

Derived from direct openpyxl inspection of `Company__Posting_Memo_Backup_MMDDYY_vTemplate.xlsx`.
Last inspected: 2026-03-20. Updated for v3: 2026-03-23.

## Table of Contents

1. [FinSum Tab — Input Cells](#finsum-input-cells)
2. [FinSum Tab — Formula Cells (DO NOT WRITE)](#finsum-formula-cells)
3. [FinSum Tab — Conditionally Modified Formulas](#finsum-conditionally-modified-formulas)
4. [SUCAP Tab — Input Cells](#sucap-input-cells)
5. [SUCAP Tab — Formula Cells (DO NOT WRITE)](#sucap-formula-cells)
6. [Off-Limits Tabs](#off-limits-tabs)
7. [Date Architecture](#date-architecture)
8. [Inspection Notes](#inspection-notes)

---

## FinSum Input Cells

All values in USD thousands unless noted. Columns G–M plus R.

### Header / Metadata

| Cell | Label | Data Type | Notes |
|------|-------|-----------|-------|
| C1 | Company Name | Text | Template default: `[Company Name]` |
| C2 | Subtitle | Text | Template default: `Posting Memo Backup` (leave as-is) |
| G2 | FY Anchor Date | Datetime | Derived from K2-first rule (see Date Architecture) |
| L2 | LTM Reporting Date | Datetime | Hardcoded; breaks the EOMONTH cascade for stub period |

### Income Statement (Columns G–M, R)

| Row | Label | Type Constraint | Columns |
|-----|-------|-----------------|---------|
| 11 | Revenue | **As-reported only** | G–M, R |
| 14 | Gross Profit | **As-reported only** (or Contribution Margin with relabeled C14) | G–M, R |
| 18 | EBITDA (Reported) | **As-reported only** — leave blank if CIM shows only adjusted | G–M, R |
| 23 | CA EBITDA | **Adjusted** — use CIM's highest-level adjusted EBITDA | G–M, R |

**Column G (anchor column): ALWAYS leave data rows empty.** G2 is the only input in column G.

### Capital Expenditures (Columns G–M, R)

| Row | Label | Notes |
|-----|-------|-------|
| 27 | Maintenance | As-reported maintenance capex |
| 28 | Growth | As-reported growth capex |

### Net Working Capital — Current Assets (Columns G–M only, no R)

| Row | Label | Common CIM Labels |
|-----|-------|-------------------|
| 46 | Accounts Receivable | Trade AR, Net AR |
| 47 | Costs in Excess of Billings ("CIE") | Contract Receivables, Unbilled Revenue, WIP |
| 48 | Inventory | Inventory, Raw Materials + Finished Goods |
| 49 | Prepaid & Other | Prepaid Expenses + Other Current Assets |

### Net Working Capital — Current Liabilities (Columns G–M only, no R)

| Row | Label | Common CIM Labels |
|-----|-------|-------------------|
| 52 | Accounts Payable | Trade AP, Tank Owner Payments (service cos.) |
| 53 | Billings in Excess of Costs ("BIE") | Contract Liabilities, Unearned Revenue |
| 54 | Deferred Revenue | Deferred Revenue |
| 55 | Accrued & Other | Accrued Wages + Accrued Insurance + Accrued Expenses + Other |

---

## FinSum Formula Cells

**NEVER write to any cell in this list** (except conditionally modified formulas below).

### Date Row (Row 2)

| Cell | Formula | Purpose |
|------|---------|---------|
| H2 | `=EOMONTH(G2,12)` | Auto-cascade from anchor |
| I2 | `=EOMONTH(H2,12)` | Auto-cascade |
| J2 | `=EOMONTH(I2,12)` | Auto-cascade |
| K2 | `=EOMONTH(J2,12)` | Auto-cascade |
| M2 | `=EOMONTH(K2,12)` | Auto-cascade (skips L2) — **may require modification** |
| R2 | `=EOMONTH(L2,-12)` | Prior-year LTM |

### Period Headers (Row 9)

G9–M9, O9, R9: all formulas generating labels like `FY'22A`, `LTM 9/24A`, `FY'25E`.

### Calculated Metrics

| Rows | Description |
|------|-------------|
| 12 | Revenue % y/y (H12–M12) |
| 15, R15 | Gross Profit % margin |
| 16 | Gross Profit % y/y (H16–M16) |
| 19, R19 | EBITDA Reported % margin |
| 20 | EBITDA Reported % y/y (H20–M20) |
| 22, R22 | Adjustments = CA EBITDA – Reported EBITDA |
| 24, R24 | CA EBITDA % margin |
| 25 | CA EBITDA % y/y (H25–M25) |
| 29, R29 | Total CapEx = Maintenance + Growth |
| 30, R30 | CapEx % revenue |

### CAGR Column (O)

O11, O14, O18, O22, O23, O27, O28: CAGR formulas using YEARFRAC.
**May require modification** — see Conditionally Modified Formulas below.

### Supporting Calculations (Rows 34+)

| Rows | Description |
|------|-------------|
| 37 | Days in Period |
| 39 | TTM Revenue (= row 11) |
| 40 | TTM COGS (= Revenue – GP) |
| 42–44 | Capex % revenue (maintenance, growth, total) |
| 50 | Current Assets = SUM(46:49) |
| 56 | Current Liabilities = SUM(52:55) |
| 58 | NWC = Current Assets – Current Liabilities |
| 59 | NWC % revenue |

### Cash Conversion Cycle (Rows 61–64)

| Row | Label | Formula Type |
|-----|-------|-------------|
| 61 | DSO | **ArrayFormula** — special openpyxl type, must not overwrite |
| 62 | DIH | Standard formula |
| 63 | DPO | Standard formula |
| 64 | CCC | = SUM(DSO + DIH + DPO) |

---

## FinSum Conditionally Modified Formulas

These cells are formulas by default but may require **intentional modification** in
specific column-mapping scenarios. These modifications are exempt from the pre-write
formula-protection block. Document all changes in the output summary.

### M2 — First Projection Year

**Default formula:** `=EOMONTH(K2,12)`

**When to modify:** When the standard 12-month cascade from K2 does not produce the
correct first projection year. This occurs when the LTM column (L) uses the most
recent FYE date and the projection year is >12 months after K2.

**Example:** K2 = 12/31/2023 (last actual FYE), L2 = 12/31/2024 (LTM = FY2024A),
projection is FY2025E = 12/31/2025. Default M2 = EOMONTH(K2,12) = 12/31/2024 (wrong).
Correct: M2 = `=EOMONTH(K2,24)` → 12/31/2025.

### O9, O11, O14, O23, O27, O28 — CAGR Column

**Default formulas:** Reference column G for both the start date (G$2) and start
value (e.g., G11).

**When to modify:** When column G data rows are empty (which is always the case —
G is the anchor column). The CAGR formulas will produce #DIV/0! or errors unless
updated to reference the first column with populated data.

**Modification:** Replace all `G` references in O formulas with the letter of the
first populated data column. Update both the date anchor (G$2 → H$2) and the value
reference (G11 → H11, G14 → H14, etc.). Also update O9 header formula to reference
the correct period label.

### Column R Data Cells — When LTM = FYE

**Default:** R data cells are input cells (write hardcoded values).

**When to modify:** When L2 = last actual FYE date (i.e., LTM column mirrors the
K-period data). In this scenario, the prior-year LTM (R) = K period. Rather than
writing independent hardcoded inputs, link R data cells to K via formula:
`R11 = =K11`, `R14 = =K14`, `R18 = =K18`, `R23 = =K23`, `R27 = =K27`, `R28 = =K28`.

This avoids inconsistency risk if K values are later updated.

---

## SUCAP Input Cells

### Sources of Funds

| Cell | Label | Data Type | Notes |
|------|-------|-----------|-------|
| F11 | RCF Drawn at Close | Number ($000s) | Derived per Overland RCF Funding Rule |
| F12 | 1L Term Loan B | Number ($000s) | CIM TL minus funded RCF increment |
| F13 | DDTL | Number ($000s) | Funded at close (typically $0) |

### Uses of Funds

| Cell Range | Label | Data Type | Notes |
|------------|-------|-----------|-------|
| H11–H14 | Use-of-proceeds labels | Text | e.g., "Refi Existing Debt", "Shareholder Distribution" |
| K11–K14 | Use-of-proceeds amounts | Number ($000s) | One row per distinct use |
| H15 | "Financing Fees" label | Text | Pre-populated |
| K16 | Transaction Expenses | Number ($000s) | Input cell |
| H16 | "Transaction Expenses" label | Text | Pre-populated |

**K15 is a FORMULA** (`=V35`, total financing fees) — do NOT write to K15.

**Uses clean-up:** After writing uses, blank any remaining "[Use]" placeholder rows
between the last populated use and Financing Fees (H15). Write empty strings to
unused labels and 0 to unused amounts.

### Pricing

| Cell | Label | Default | Notes |
|------|-------|---------|-------|
| S32 | RCF Spread (bps) | 325 | Input |
| T32 | RCF OID | 99 | Input (par = 100) |
| S33 | TL Spread (bps) | 575 | Input |
| T33 | TL OID | 98 | Input |

**S34, T34 are FORMULAS** (`=S33`, `=T33`) — DDTL pricing auto-copies from TL.

### Other SUCAP Inputs

| Cell | Label | Data Type | Notes |
|------|-------|-----------|-------|
| U34 | DDTL Unfunded Commitment | Number ($000s) | Derived per DDTL Proactive Sizing Rule |
| S17 | SOFR Rate | Decimal | e.g., 0.0435 |
| I30 | Cash & Equivalents | Number ($000s) | Pro forma cash at close |
| J41 | TEV Multiple | Number | Implied TEV / CA EBITDA multiple |
| P13 | Cash Taxes | Number ($000s) | For FCCR; leave blank if not provided by analyst |
| M32, M33, M34 | Maturity | Text | e.g., "5 Years" |
| P32 | Call Protection (RCF) | Text | e.g., "n/a" |
| P33 | Call Protection (TL) | Text | e.g., "[102 / 101]" |

---

## SUCAP Formula Cells

**NEVER write to any cell in this list.**

### Auto-Calculated Structure

| Cell | Formula | Purpose |
|------|---------|---------|
| U32 | `=MROUND(I43,1000)` | **RCF commitment = floor(LTM CA EBITDA) rounded to nearest $1MM** |
| F14 | `=F21-SUM(F11:F13)` | **Owner Equity plug** (absorbs CIM "Cash from Balance Sheet") |
| F21 | `=K21` | Total Sources = Total Uses |
| K21 | `=SUM(K11:K20)` | Total Uses |
| K15 | `=V35` | Total financing fees (from OID calculations) |

### FCCR Block

| Cell | Formula | Purpose |
|------|---------|---------|
| P11 | `=I43` (= FinSum!L23) | LTM CA EBITDA |
| **P12** | **`=-FinSum!L22`** | **See note below** |
| P14 | `=-FinSum!L29` | Maintenance + Growth Capex |
| P15 | `=SUM(P11:P14)` | FCCR Numerator |
| P17 | Complex formula | Cash interest expense |
| P18 | `=0.01*F12` | Mandatory amortization (1% of TL) |
| P19 | `=SUM(P17:P18)` | FCCR Denominator |
| P21 | `=IFERROR(P15/P19,0)` | FCCR ratio |

**P12 Note:** The template default deducts ALL adjustments (= Reported EBITDA minus
CA EBITDA). This is ultra-conservative — the FCCR numerator effectively starts from
Reported EBITDA. To implement Tier 1/Tier 2 FCCR treatment, the analyst must
deliberately override P12 with an itemized formula. See
[fccr-addback-guide.md](fccr-addback-guide.md) for override instructions.

### Pro Forma Capitalization (Rows 32–43)

All cells in I32–I43, J32–J41, K32–K40 are formulas (leverage multiples, % cap,
TEV calculations). C32–C43 are formula-generated labels. N32–N35, O32–O35 are
formula-generated pricing/OID display strings. S34, T34, S35, T35 are formulas.
V32–V35 are OID dollar calculations.

### Labels and References

C1, C2, C3, C11, C13, C32–C34, C43, I26: all formulas referencing FinSum or
generating dynamic labels.

---

## Off-Limits Tabs

**Detailed FinSum** and **Returns** are entirely formula-driven downstream tabs.
Do not read from or write to any cell in these tabs.

---

## Date Architecture

### K2-First Anchor Rule (v2)

**The governing rule:** K2 must always equal the last actual fiscal year-end period.

**Procedure:**
1. Identify the last actual FYE in the CIM (e.g., FY2024A = 12/31/2024 for calendar FYE)
2. Set K2 = that date. Since K2 = EOMONTH(J2, 12), and J2 = EOMONTH(I2, 12), etc.,
   work backward 4 EOMONTH steps to derive the required G2 input:
   ```
   K2 target = 12/31/2024
   J2 = EOMONTH(K2, -12) = 12/31/2023
   I2 = EOMONTH(J2, -12) = 12/31/2022
   H2 = EOMONTH(I2, -12) = 12/31/2021
   G2 = EOMONTH(H2, -12) = 12/31/2020  ← write this to G2
   ```
3. Verify: the EOMONTH cascade from G2 produces H2 through K2 with K2 landing on the
   last actual FYE.

### Column Layout (FinSum)

```
Col G = Anchor FYE (input, G2 only — data rows empty)
Col H = FY Anchor+1 (EOMONTH cascade)
Col I = FY Anchor+2 (EOMONTH cascade)
Col J = FY Anchor+3 (EOMONTH cascade)
Col K = FY Anchor+4 (EOMONTH cascade) — MUST = last actual FYE
Col L = LTM date (HARDCODED input — breaks cascade)
Col M = FY Anchor+5 (EOMONTH cascade from K, skips L) — may need adjustment
Col R = Prior-Year LTM (EOMONTH(L2,-12) — formula)
```

### Typical Mapping — Calendar FYE, No Explicit LTM

For a CIM showing FY2022A–FY2024A actuals + FY2025E + FY2026P, deal closing April 2025:

| CIM Period | Column | Row 2 Value | Auto or Input? | Notes |
|------------|--------|-------------|----------------|-------|
| (anchor) | G | 12/31/2019 | **Input** (G2) | 4 EOMONTH steps before K2 |
| FY'20A | H | 12/31/2020 | Auto (H2) | No CIM data — leave blank |
| FY'21A | I | 12/31/2021 | Auto (I2) | No CIM data — leave blank |
| FY'22A | J | 12/31/2022 | Auto (J2) | First CIM period → write data |
| FY'23A | K | 12/31/2023 | Auto (K2) | Last actual FYE |
| FY'24A (LTM proxy) | L | 12/31/2024 | **Input** (L2) | LTM = FYE; relabel note |
| FY'25E | M | 12/31/2025 | **Adjusted formula** | =EOMONTH(K2,24) needed |
| PY LTM | R | 12/31/2023 | Auto (R2) | = K period; link R→K |

### Typical Mapping — Calendar FYE, Explicit LTM

For a CIM showing FY2022A–FY2024A actuals + LTM 9/30/25 + FY2025E + FY2026P:

| CIM Period | Column | Row 2 Value | Auto or Input? |
|------------|--------|-------------|----------------|
| (anchor) | G | 12/31/2020 | **Input** (G2) |
| FY2022A | H | 12/31/2021 | Auto (H2) |
| FY2023A | I | 12/31/2022 | Auto (I2) |
| FY2024A | J | 12/31/2023 | Auto (J2) |
| FY2025E | K | 12/31/2024 | Auto (K2) = last actual FYE |
| LTM 9/30/25 | L | 9/30/2025 | **Input** (L2) |
| FY2026P | M | 12/31/2025 | Auto (M2) — verify cascade |
| PY LTM | R | 9/30/2024 | Auto (R2) |

### Non-Calendar FYE

If FYE is not December 31, the EOMONTH cascade still works but produces different
month-end dates. Present the adjusted map and confirm with the user.

---

## Inspection Notes

**Ambiguous cells resolved during inspection:**

1. **SUCAP U32** — Appears in prompt as input; actual template has formula
   `=MROUND(I43,1000)`. Confirmed as FORMULA. RCF commitment auto-sizes from
   LTM CA EBITDA.

2. **SUCAP P12** — Prompt describes as input for itemized Tier 1 formula; actual
   template has formula `=-FinSum!L22`. Confirmed as FORMULA. Override requires
   deliberate analyst decision.

3. **SUCAP F14** — Prompt lists as input for Owner Equity; actual template has
   formula `=F21-SUM(F11:F13)`. Confirmed as FORMULA (plug). Absorbs CIM "Cash
   from Balance Sheet" sources — see structuring-rules.md.

4. **SUCAP S34, T34** — Prompt lists as inputs for DDTL pricing; actual template
   has formulas `=S33`, `=T33`. Confirmed as FORMULAS (copy from TL).

5. **FinSum G61 (DSO)** — Contains ArrayFormula object, not a standard formula
   string. Must be detected separately in pre-write validation (check for
   `hasattr(cell.value, 'text')` in addition to string-starts-with-equals).

6. **SUCAP K15** — Contains formula `=V35` (financing fees from OID). Not an input.
   Do not read via data_only for balance validation — compute OID fees from inputs.

7. **SUCAP P34 (DDTL call protection)** — Formula `=P33` (copies TL). Not an input.
