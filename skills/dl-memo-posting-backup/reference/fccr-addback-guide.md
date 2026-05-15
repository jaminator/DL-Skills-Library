# FCCR Addback Guide

## Table of Contents

1. [Template Default Behavior](#template-default-behavior)
2. [Tier 1 vs. Tier 2 Classification](#tier-1-vs-tier-2-classification)
3. [Overriding P12 for Tier 1/Tier 2 Treatment](#overriding-p12)
4. [Common CIM Addback Language → Tier Classification](#common-addback-language)
5. [FCCR Formula Architecture](#fccr-formula-architecture)

---

## Template Default Behavior

SUCAP P12 contains the formula `=-FinSum!L22`, which equals `-(CA EBITDA – Reported EBITDA)`.

This means the default FCCR numerator is:

```
P11  CA EBITDA (LTM)
P12  minus ALL adjustments (= Reported EBITDA – CA EBITDA)
P13  minus Cash Taxes
P14  minus Total CapEx
────
P15  FCCR Numerator ≈ Reported EBITDA – Taxes – Capex
```

**The default is ultra-conservative** — it strips out every adjustment and starts
the FCCR from reported EBITDA. This is the safest base case for non-sponsored
credits where addback quality is uncertain.

**When to keep the default:** If all adjustments are Tier 1 (pro forma, forward-looking),
the default is already correct.

**When to override:** If the QoE bridge contains Tier 2 diligence adjustments that
represent genuine normalization of operating performance, the analyst should override
P12 to deduct only Tier 1 items — leaving Tier 2 adjustments in the FCCR numerator.

---

## Tier 1 vs. Tier 2 Classification

### Tier 1 — DEDUCT from FCCR Numerator

These inflate CA EBITDA beyond what has actually been earned. They represent future
expectations, unrealized synergies, or pro forma run-rate assertions.

| Category | Common CIM Language | Rationale |
|----------|-------------------|-----------|
| Pro forma adjustments | "Pro forma run-rate," "Annualized impact of," "Full-year effect of" | Hasn't happened yet |
| Revenue normalization | "Normalized revenue," "Revenue add-back," "Adjusted revenue uplift" | Speculative revenue claim |
| Unrealized synergies | "Expected cost savings," "Synergy pipeline," "Identified but not yet realized" | Forward-looking assertion |
| Prospective cost reductions | "Planned headcount reduction," "Anticipated vendor renegotiation" | Not yet implemented |
| Pipeline revenue | "Contracted but not yet recognized," "Signed LOI revenue" | No cash received |
| New contract run-rate | "Full run-rate of contracts won in [year]" | Partially earned at best |

### Tier 2 — LEAVE in FCCR Numerator

These normalize reported EBITDA to a clean operating baseline. They correct for
accounting noise, non-recurring items, and structural carve-out artifacts.

| Category | Common CIM Language | Rationale |
|----------|-------------------|-----------|
| Transaction / carve-out expenses | "Carve-out transaction expenses," "One-time legal fees" | Truly non-recurring |
| Non-cash items | "Equity compensation," "Impairment," "Gain/loss on asset sale" | Non-cash; doesn't reduce FCF |
| Non-recurring restructuring | "One-time severance," "Facility closure costs" | Completed event |
| Audit / accounting adjustments | "POC hindsight analysis," "Revenue restatement," "Accounting policy change" | Corrects past reporting |
| Standalone cost adjustments | "Incremental standalone costs," "TSA elimination" | Normalizes to standalone run-rate |
| Management fee elimination | "Management fees to sponsor," "Advisory fees — no services rendered" | Non-operational expense |
| Bad debt normalization | "Bad debt reserve adjustment," "Write-off normalization" | Normalizes to recurring rate |
| Bonus / compensation normalization | "Bonus true-up," "Officer compensation normalization" | Normalizes to market rate |
| Revolver / facility fees | "Revolver availability fees," "Unused commitment fees" | Eliminated at refi |

### Gray Zone — Analyst Judgment Required

| Item | Lean Tier 1 if... | Lean Tier 2 if... |
|------|--------------------|--------------------|
| "Cost savings from new ERP" | Not yet implemented | Implementation complete, savings verified |
| "Normalized insurance expense" | Based on future quotes | Based on current policy in effect |
| "Exiting line of business" | Still operating, wind-down in progress | Fully exited, P&L impact confirmed |
| "Full-year impact of price increases" | Increase not yet effective | Already in effect, partial-year shown |

---

## Overriding P12

To implement Tier 1/Tier 2 treatment, overwrite P12 with an itemized formula:

```python
ws = wb['SUCAP']

# Example: CIM shows 3 Tier 1 adjustments (values in $000s)
# Pro forma run-rate of new contracts: $2,500
# Annualized cost savings (not yet realized): $1,200
# Revenue normalization: $800
# Total Tier 1: $4,500

# Write as negative (deduction from CA EBITDA)
# Itemize each component so the formula is auditable
ws['P12'] = '=-(2500+1200+800)'

# Or with named components for clarity:
# ws['P12'] = '=-(2500+1200+800)'  # PF new contracts + unrealized savings + rev norm
```

**Formula syntax rules:**
- Always start with `=-(`
- Sum individual Tier 1 amounts inside parentheses
- Each amount is positive; the leading negative sign makes the total a deduction
- Add a Python comment documenting what each number represents

**After override, the FCCR numerator becomes:**

```
P11  CA EBITDA (LTM)
P12  minus Tier 1 adjustments only
P13  minus Cash Taxes
P14  minus Total CapEx
────
P15  FCCR Numerator ≈ (CA EBITDA – Tier 1) – Taxes – Capex
```

This is less conservative than the template default but more analytically precise.

---

## Common Addback Language

Reference table for classifying CIM addback descriptions:

| CIM Addback Description | Likely Tier | Key Signal |
|--------------------------|-------------|------------|
| "Standalone Adjustments" | 2 | Normalizing to independent ops |
| "Carve-Out Transaction Expenses" | 2 | One-time, completed |
| "POC Hindsight Analysis" | 2 | Accounting restatement |
| "Normalization Adjustments (401K, leases)" | 2 | Policy alignment |
| "Non-Cash Items (equity comp, impairment)" | 2 | Non-cash |
| "Non-Recurring Items (rebranding, ERP)" | 2 if completed; 1 if ongoing | Check completion status |
| "Management Fees (to sponsor)" | 2 | Non-operational; eliminated at close |
| "Revolver Fees" | 2 | Eliminated at refi |
| "Exiting Line of Business" | 2 if exited; 1 if in-progress | Check completion status |
| "Full-year impact of price increases" | 1 | Forward-looking annualization |
| "Run-rate of new contracts" | 1 | Prospective revenue |
| "Expected cost savings" | 1 | Unrealized |
| "Pro forma for acquisitions" | 1 | Not yet closed or not full-year |

---

## FCCR Formula Architecture

Complete FCCR calculation chain in the SUCAP tab:

```
NUMERATOR:
  P11 = FinSum!L23                    (LTM CA EBITDA)
  P12 = -FinSum!L22  [or override]    (Adjustments deduction)
  P13 = [input]                       (Cash taxes, negative)
  P14 = -FinSum!L29                   (Total capex, negative)
  P15 = SUM(P11:P14)                  (FCCR Numerator)

DENOMINATOR:
  P17 = (U32-F11)*0.5% + (U34-F13)*1% + F11*(S17+S32/10000)
        + F12*(S17+S33/10000) + F13*(S17+S34/10000)
                                      (Cash interest expense)
  P18 = 0.01 * F12                    (Mandatory amortization: 1% × TL)
  P19 = SUM(P17:P18)                  (FCCR Denominator)

RATIO:
  P21 = IFERROR(P15/P19, 0)           (FCCR)
```

**P17 interest expense components:**
1. Unfunded RCF commitment fee: (U32 – F11) × 0.50%
2. Unfunded DDTL commitment fee: (U34 – F13) × 1.00%
3. RCF drawn interest: F11 × (SOFR + RCF spread)
4. TL interest: F12 × (SOFR + TL spread)
5. DDTL funded interest: F13 × (SOFR + DDTL spread)

**Dual-column FCCR:** When the close date is >3 months after the LTM reporting date,
target both a trailing LTM FCCR and a close-date LTM estimate. The template supports
one FCCR column (the LTM at L2). For a second column, the analyst would need to
manually add calculations or use the close-date LTM in column M.
