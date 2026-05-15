# Examples — Populating the Posting Memo Backup

Three annotated examples demonstrating the skill workflow for different deal types.

## Table of Contents

1. [Example 1: Standard Deal — No Explicit LTM, K2-First Rule, DDTL Sizing](#example-1)
2. [Example 2: Bespoke Deal — Seller Note Escalation](#example-2)
3. [Example 3: Non-Calendar FYE Edge Case](#example-3)

---

## Example 1: Standard Deal — No Explicit LTM, K2-First Rule, DDTL Sizing

**Scenario:** CIP for "AquaTech Services" shows FY2022A–FY2024A historical actuals,
FY2025E, and FY2026P. QoE bridge available with Definitional EBITDA disclosed.
December 31 FYE. Senior credit facility only (RCF + TL, CIM has no DDTL). Deal
closing April 2025. No explicit LTM period in the CIM. CIM presents Contribution
Margin rather than Gross Profit. FCF bridge page shows "Pro Forma Adjusted EBITDA —
Closing Stub April '25: $31.0M."

### Step 0: Gather User Inputs (Mandatory Gate)

```
Claude: Before I start reading the CIP, I need to confirm four items:

  1. Expected close date — the CIP targets April 2025. Can you confirm?
  2. Cash at close — the S&U shows $2.1M. Confirm?
  3. Current SOFR rate — for FCCR interest expense?
  4. Cash taxes (annual run-rate, $000s) — for FCCR P13. If you don't have
     a figure, I'll leave P13 blank rather than estimating.
```

```
User: April 2025 confirmed. Cash $2.1M confirmed. SOFR 4.35%. Leave cash taxes
blank — I'll fill in after diligence.
```

### Step 2: Column Map — K2-First Rule, No Explicit LTM

```
Claude: The CIP shows 3 historical FY actuals (FY2022A–FY2024A) plus FY2025E and
FY2026P, with no separate LTM period. Since the deal closes April 2025 — within 6
months of the 12/31/2024 FYE — I'll map FY2024A to column L as the LTM proxy.

Applying the K2-first rule: K2 must = last actual FYE = 12/31/2023. Working backward
4 EOMONTH steps: G2 = 12/31/2019.

COLUMN MAP:
CIM Period       → Col → Date in Row 2      → Write Data?
──────────────────────────────────────────────────────────
(anchor, blank)  → G   → 12/31/2019         → No (CAGR anchor)
FY'20A           → H   → 12/31/2020 (auto)  → No CIM data — blank
FY'21A           → I   → 12/31/2021 (auto)  → No CIM data — blank
FY'22A           → J   → 12/31/2022 (auto)  → Yes
FY'23A           → K   → 12/31/2023 (auto)  → Yes (last actual FYE)
FY'24A (=LTM)   → L   → 12/31/2024 (hard)  → Yes (LTM proxy)
FY'25E           → M   → (see note)         → Yes
Prior-Year LTM   → R   → 12/31/2023 (auto)  → Link to K (=K11, etc.)

FORMULA ADJUSTMENTS REQUIRED:
  • M2: Default =EOMONTH(K2,12) = 12/31/2024, but we need 12/31/2025.
    Will overwrite M2 with =EOMONTH(K2,24).
  • Column O (CAGR): Default references G (empty). Will update O9, O11, O14,
    O23, O27, O28 to reference column J (first populated = FY'22A).
  • Column R: Since LTM = FYE and R2 = 12/31/2023 = K period, will link
    R data cells to K via formula (R11 = =K11, etc.) to avoid duplication.

NOTE: L2 falls on a FYE date — L9 will display "LTM 12/24A" rather than
"FY'24A." Manually update the L9 formula in Excel for consistency.

No separate LTM period in CIM — mapping FY2024A to L2 as LTM proxy given
close-date proximity. Confirm?
```

```
User: Confirmed. Proceed with that column map.
```

### Step 3: Extraction Summary (with GP fallback and close-date EBITDA)

```
Claude: Here's the extraction summary. All amounts in $000s:

INCOME STATEMENT:
| Row | Metric          | Type        | J (FY22) | K (FY23) | L (FY24=LTM) | M (FY25E) |
|-----|-----------------|-------------|----------|----------|---------------|-----------|
| 11  | Revenue         | As-reported | 184,500  | 185,600  | 196,400       | 208,200   |
| 14  | Contrib. Margin | Sub for GP  | 76,300   | 83,900   | 90,800        | 95,200    |
| 18  | EBITDA Reported | As-reported | 25,300   | 10,500   | 28,800        | [blank]   |
| 23  | CA EBITDA       | Adjusted    | 22,800   | 26,800   | 31,000*       | 33,500    |

*L23 (CA EBITDA LTM) = $31,000 sourced from FCF bridge page (CIP p.27):
"Pro Forma Adjusted EBITDA — Closing Stub April '25: $31.0M." This close-date
figure takes precedence over the FY2024A QoE figure of $31.5M.

Notes:
- Row 14: CIP presents no COGS/GP line — discloses Contribution Margin instead.
  Proposing to relabel C14 as "Contribution Margin" and populate. Confirm?
- Row 18 blank for FY2025E: CIP shows only adjusted EBITDA for projections.
- FY2023A Reported EBITDA ($10.5M) vs. CA EBITDA ($26.8M) — large adjustment
  gap due to Turnspire carve-out year. FLAGGED for analyst review.
- R (PY LTM): linked to K (= FY'23A data) since LTM = FYE.

CAPITAL EXPENDITURES:
| Row | Metric      | J (FY22) | K (FY23) | L (FY24=LTM) | M (FY25E) |
|-----|------------|----------|----------|---------------|-----------|
| 27  | Maintenance | 1,800    | 1,800    | 2,000         | 2,800     |
| 28  | Growth      | 900      | 1,000    | 400           | 700       |

PROPOSED OVERLAND STRUCTURE (derived from structuring rules):
  CIM S&U shows: $25M RCF (unfunded) + $105M TL
  RCF commitment (auto via U32): ~$31M (= MROUND($31.0M LTM EBITDA, 1000))
  RCF funded at close (F11): $6,000 (= Overland $31M − CIM $25M)
  Term Loan (F12): $99,000 (= CIM $105M − $6M funded RCF increment)
  DDTL commitment (U34): $25,000 (= ROUND($99M ÷ 0.80 × 0.20, $1M) = 20% target)
  DDTL funded at close (F13): $0 (standard — funds post-close)

  Uses: Refi Existing Debt = $82,000, Shareholder Distribution = $55,000,
        K16 Transaction Expenses = $4,280
  Pricing: CIM doesn't disclose; using defaults (RCF 325/99, TL 575/98)
  SOFR: 0.0435 (per user)
  Cash at close: $2,100
  TEV multiple: 12.2x (from CIP comps-based valuation)
  Cash taxes (P13): left blank per user direction

Does this look correct? Any adjustments before I write to the template?
```

### Step 5: Write, Verify, and Deliver

After user confirms, Claude writes all values, runs pre-write formula validation,
applies intentional formula modifications (M2, column O, column R), saves, and
presents the output summary.

---

## Example 2: Bespoke Deal — Seller Note Escalation

**Scenario:** CIM for "IndustrialCo" discloses a $15M seller note subordinated
to the senior term loan, plus a $5M earn-out tied to FY2026 EBITDA targets.

### Bespoke Detection and Halt

```
Claude: ⚠️ BESPOKE CAPITAL STRUCTURE DETECTED

The CIM discloses non-standard components that require analyst input before
I can populate the SUCAP tab:

FULL CAPITAL STACK (as read from CIM):
  Sources:
    New $20M Revolver (undrawn)          $  —
    New $80M Senior Secured Term Loan      80,000
    $15M Seller Note (subordinated)        15,000
    Cash from Balance Sheet                10,000
    Total Sources                        $105,000

  Uses:
    Refinance Existing Debt              $ 75,000
    Seller Note (rolled from prior)        15,000
    Transaction Fees & Expenses            10,000
    Cash to Balance Sheet                   5,000
    Total Uses                           $105,000

  Earn-Out: Up to $5M contingent on FY2026 EBITDA > $25M

NON-STANDARD TRANCHES:
  1. Seller Note ($15M) — subordinated debt below the TL. Triggers bespoke
     escalation because it adds a leverage layer not in the template's
     standard 3-tranche structure (RCF/TL/DDTL).
  2. Earn-Out ($5M) — contingent consideration. Not debt at close but
     represents a potential future cash obligation.

NOTE: "Cash from Balance Sheet" ($10M) maps to the Owner Equity plug (F14).
F14 is a formula — do not overwrite. Downstream: SUCAP!I38 references F14.

SUCAP MODIFICATIONS REQUIRED:
  • The seller note needs either: (a) a new row between the TL and Owner
    Equity in the Sources section, with corresponding leverage calc rows
    in the Pro Forma Cap table; or (b) modeling as part of the TL with a
    footnote distinguishing the tranches.
  • The earn-out should be footnoted but not modeled as debt at close.
  • The FCCR formula (P17) currently calculates interest only on
    RCF/TL/DDTL — it would need modification to include seller note
    interest if the note is cash-pay.

RECOMMENDED APPROACH:
  Option A: Model the senior facility only (RCF + TL) in SUCAP as-is.
  Add the seller note amount to a Uses line but not to Sources debt.
  Owner Equity plug absorbs it. Footnote the seller note separately.
  FCCR reflects senior-only coverage.

  Option B: Manually add a seller note row to SUCAP. This requires
  template modification beyond the skill's standard workflow.

Which approach do you prefer, or would you like to handle the SUCAP
manually and have me focus on populating FinSum only?
```

```
User: Option A. Model senior only, footnote the seller note. Skip the earn-out.
```

Claude then proceeds with standard FinSum population plus senior-only SUCAP,
applying Overland RCF funding and DDTL sizing rules to the $80M senior TL,
and adding a note in the output summary about the seller note treatment.

---

## Example 3: Non-Calendar FYE Edge Case

**Scenario:** CIM for "FiscalCo" has a June 30 fiscal year-end. CIM shows FY2023A
(ending 6/30/23), FY2024A (ending 6/30/24), LTM 3/31/25A, FY2025E (ending 6/30/25),
FY2026P (ending 6/30/26).

### Column Map — Non-Calendar FYE

```
Claude: This company has a June 30 fiscal year-end, which changes the
EOMONTH cascade dates.

K2-first rule: K2 = last actual FYE = 6/30/2024. Working backward:
G2 = 6/30/2020.

CIM Period           → Col → Date in Row 2    → Write Data?
─────────────────────────────────────────────────────────────
(anchor, blank)      → G   → 6/30/2020        → No (CAGR anchor)
FY'21A               → H   → 6/30/2021 (auto) → No CIM data — blank
FY'22A               → I   → 6/30/2022 (auto) → No CIM data — blank
FY2023A (Jun 30)     → J   → 6/30/2023 (auto) → Yes
FY2024A (Jun 30)     → K   → 6/30/2024 (auto) → Yes (last actual FYE)
LTM 3/31/25A         → L   → 3/31/2025 (hard) → Yes
FY2025E (Jun 30)     → M   → 6/30/2025 (auto) → Yes — verify cascade
FY2026P (Jun 30)     → ?   → N/A              → No column available

NOTES:
  • M2 = EOMONTH(K2,12) = 6/30/2025 ✓ — correct for FY2025E, no adjustment needed.
  • FY2026P has no available column. Column O is CAGR. Options:
    (a) Skip FY2026P entirely — most LTM-focused analyses don't need Y+2.
    (b) If needed, we could discuss template modification.
  • Column O (CAGR): will reference column J (first populated = FY2023A).
  • Column R: R2 = EOMONTH(L2,-12) = 3/31/2024 — this is a valid PY LTM stub.
    Write PY LTM data if CIM discloses it.
  • Template label C9 says "FYE December 31st" — manual update to
    "FYE June 30th" required post-delivery.

Does this work, or would you prefer a different arrangement?
```

```
User: Option A — skip FY2026P. Focus on LTM and actuals.
```

### Key Differences for Non-Calendar FYE

- G2 input: `datetime(2020, 6, 30)` instead of December 31
- L2 input: `datetime(2025, 3, 31)` — the LTM date
- C9 label: flag for manual update to "FYE June 30th"
- The LTM period (3/31/25) is 9 months after FYE (6/30/24), so the LTM column
  represents a full trailing 12-month period ending 3/31/25 — standard treatment.

### Output Summary Note

```
FLAGS FOR ANALYST FOLLOW-UP:
  - Non-calendar FYE (June 30). Template label in C9 says "FYE December 31st"
    — manually update to "FYE June 30th."
  - FY2026P not populated — no column available in standard template layout.
  - Columns H and I are auto-dated but have no CIM data (FY'21A, FY'22A).
  - Detailed FinSum tab has its own date architecture (G2 = 12/31/2019 default)
    that is NOT linked to FinSum G2. If you use Detailed FinSum, update its
    dates independently.
```
