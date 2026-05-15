# Structuring Rules

## Table of Contents

1. [Standard Deal Sizing](#standard-deal-sizing)
2. [Overland RCF Funding Rule](#overland-rcf-funding-rule)
3. [Default Pricing](#default-pricing)
4. [DDTL Proactive Sizing](#ddtl-proactive-sizing)
5. [Owner Equity Plug](#owner-equity-plug)
6. [Cash from Balance Sheet Mapping](#cash-from-balance-sheet-mapping)
7. [Sources = Uses Balance Check](#sources-uses-balance)
8. [Bespoke Deal Escalation](#bespoke-deal-escalation)
9. [TEV Multiple and Implied Equity](#tev-and-implied-equity)

---

## Standard Deal Sizing

A **standard deal** consists of a senior credit facility only:
RCF + Term Loan + optional DDTL. Uses are limited to: refinance existing debt,
cash to balance sheet, shareholder distribution, transaction expenses.

### RCF Commitment (U32)

**Template auto-calculates:** `=MROUND(I43, 1000)` = floor(LTM CA EBITDA) rounded
to nearest $1MM.

This is a formula — do NOT write to U32. The RCF commitment auto-sizes when
LTM CA EBITDA is populated in FinSum L23.

### Term Loan (F12)

The funded first-lien term loan amount. Derived per the Overland RCF Funding Rule
below — not necessarily the CIM's stated TL amount.

### DDTL (F13)

The funded DDTL amount at close (typically $0 — DDTLs fund post-close for
acquisitions or growth capex). See DDTL Proactive Sizing below for commitment sizing.

---

## Overland RCF Funding Rule

**Rule:** Funded RCF at close = Overland RCF commitment − CIM RCF commitment.

The Overland RCF commitment (≈1× LTM CA EBITDA via U32 formula) typically exceeds
the CIM lender's RCF ask. The increment above the CIM's facility represents
additional undrawn capacity Overland provides. Any funded RCF amount at close
covers the CIM's RCF draw plus this incremental commitment fee exposure.

**Derivation sequence:**
```
CIM RCF commitment (from CIM S&U)           = $A
Overland RCF commitment (from U32 auto-size) = $B
Funded RCF increment                         = $B − $A
CIM TL (from CIM S&U)                       = $C
Overland TL (F12)                            = $C − funded RCF increment
RCF drawn at close (F11)                     = funded RCF increment
```

**Example:**
CIM shows: $25M RCF (unfunded) + $105M TL.
Overland RCF auto-sizes to $31M (from U32 = MROUND($31.0M EBITDA, 1000)).
Funded increment = $31M − $25M = $6M.
Overland TL = $105M − $6M = $99M.
Result: F11 = $6,000, F12 = $99,000.

**Presentation:** Always present the derived amounts in the extraction summary with
the formula chain visible. Wait for user confirmation. If the user overrides, accept
but flag: "Note: User override — F11 set to $X vs. rule-derived $Y."

**When CIM RCF = 0 or no RCF disclosed:** F11 = 0 (undrawn at close). Overland RCF
commitment still auto-sizes via U32. TL = CIM TL as stated.

---

## No-S&U Protocol

### When to Apply

The CIM/CIP contains no Sources & Uses page and no proposed capital structure. This
is common in:
- Early-stage sell-side processes where terms are not yet set
- DCM marketing CIPs / staple financing packages
- Teasers or preliminary information memoranda

### Protocol

1. **Flag the absence explicitly.** Do not attempt to infer a capital structure from
   other CIM pages (e.g., management projections that assume a certain debt level).
   State: "No S&U or proposed capital structure found in the CIP."

2. **Solicit from the analyst in a single message:**
   - Proposed TL size OR target leverage multiple (e.g., "$80M TL" or "4.0× LTM CA EBITDA")
   - RCF funded amount at close (or confirm $0 if fully undrawn)
   - Use-of-proceeds labels and amounts (refi, distribution, cash to BS, etc.)
   - If the analyst provides a leverage multiple instead of a dollar amount, derive
     TL = multiple × LTM CA EBITDA and present the implied dollar amount for confirmation.

3. **Apply standard Overland structuring rules once inputs are received:**
   - Overland RCF Funding Rule: since there is no "CIM RCF commitment" to offset,
     treat as the CIM RCF = 0 case — F11 = 0, TL = analyst-provided TL
   - DDTL Proactive Sizing: derive from the analyst-provided TL per standard formula
   - Present the derived structure in the extraction summary and wait for confirmation

### Example

```
CIP contains no S&U page. Analyst provides: "$79M TL, RCF fully undrawn at close,
uses are Equity Consideration $190M."

Derivation:
  RCF commitment (auto via U32): ~$19M (from LTM CA EBITDA)
  RCF funded at close (F11): $0 (no CIM RCF to offset; analyst confirmed undrawn)
  Term Loan (F12): $79,000 (analyst-provided)
  DDTL commitment (U34): $20,000 (= ROUND($79M ÷ 0.80 × 0.20, $1M))
  DDTL funded at close (F13): $0
  Uses: Equity Consideration (K11) = $190,000
```

---

## Default Pricing

| Tranche | Spread (bps) | Cell | OID | Cell | Notes |
|---------|-------------|------|-----|------|-------|
| RCF | 325 | S32 | 99.00 | T32 | Commitment fee: 50% of spread on unfunded |
| TL | 575 | S33 | 98.00 | T33 | Standard first-lien pricing |
| DDTL | Same as TL | S34 (formula) | Same as TL | T34 (formula) | Auto-copies from TL |

S34 and T34 are formulas (`=S33`, `=T33`). To set different DDTL pricing,
overwrite S34/T34 — but note this destroys the formula link.

**If the CIM discloses specific pricing:** Use the CIM's disclosed spreads and OID
instead of defaults. Write to S32/T32 for RCF, S33/T33 for TL.

**Commitment fees (built into P17 formula):**
- Unfunded RCF: 0.50% (= 50% × spread, hardcoded in P17)
- Unfunded DDTL: 1.00% (hardcoded in P17)

---

## DDTL Proactive Sizing

### Sizing Rule

Regardless of whether the CIM contemplates a DDTL, Overland proactively sizes a
DDTL facility for acquisition/growth capacity.

**Formula:** DDTL commitment = ROUND(TL ÷ (1 − 20%) × 20%, nearest $1M)

This targets 20% of the combined TL + DDTL facility — the bottom of the 20–30%
acceptable range. Do not exceed 30% unless the user directs otherwise.

**Example:**
TL (F12) = $99M.
DDTL = ROUND($99M ÷ 0.80 × 0.20, $1M) = ROUND($24.75M, $1M) = $25M.
Result: U34 = $25,000 (unfunded commitment), F13 = $0 (funds post-close).

### CIM Validation

If the CIM discloses a DDTL, check whether it falls within the 20–30% range:
```
DDTL_commitment ≤ 0.30 × (F12 + DDTL_commitment)
→ DDTL_commitment ≤ 0.30 / 0.70 × F12 ≈ 0.4286 × F12
```
Flag if the CIM's DDTL exceeds 30% of the aggregate.

### DDTL Input Cells

| Cell | What | Notes |
|------|------|-------|
| F13 | DDTL funded at close | Typically $0 |
| U34 | DDTL total unfunded commitment | Used in commitment fee calc and pro forma cap table |

### DDTL Impact on FCCR

P17 includes the unfunded DDTL commitment fee: (U34 − F13) × 1.00%. A $25M unfunded
DDTL adds $250K to the annual FCCR denominator.

---

## Owner Equity Plug

F14 is a formula: `=F21 - SUM(F11:F13)`

This means Owner Equity automatically equals Total Uses minus total funded debt.
Do NOT write to F14.

**The plug works as follows:**
```
F14 (Owner Equity) = F21 (Total Sources) - F11 (RCF) - F12 (TL) - F13 (DDTL)
    where F21 = K21 = SUM(K11:K20) = Total Uses
```

For the equity plug to be correct, all uses of proceeds (K11–K20) must be populated
AND all debt sources (F11–F13) must be populated. The residual is the owner's equity
contribution.

---

## Cash from Balance Sheet Mapping

When the CIM lists "Cash from Balance Sheet" (or similar) as a named source of funds,
this line does **not** map to a separate input cell in the template. It is absorbed
into the Owner Equity plug (F14).

**Rationale:** F14 = Total Uses − Funded Debt. If the owner contributes $38M from the
balance sheet and no other equity, F14 = $38M automatically once uses and debt sources
are populated correctly.

**F14 → I38 dependency:** F14 links directly to SUCAP!I38 (Common Equity in the
Pro Forma Cap table). If F14 were overwritten to explicitly show a cash source, I38
would also need updating. Do NOT overwrite F14 — it is a formula cell.

**Flag in output summary:** "CIM 'Cash from Balance Sheet' ($X) is captured in the
Owner Equity plug (F14 = $Y). F14 is a formula cell — do not overwrite. Downstream:
SUCAP!I38 references F14 directly."

---

## Sources = Uses Balance

The template enforces Sources = Uses structurally:

```
Total Sources (F21) = Total Uses (K21)   [F21 = K21, formula]
```

This means if uses exceed funded debt, the Owner Equity plug (F14) absorbs the
difference. If the resulting equity contribution looks unreasonable (negative or
extremely large relative to TEV), flag this for the analyst.

**Validation check after population:**

```python
ws = wb['SUCAP']
total_uses = sum(ws[f'K{r}'].value or 0 for r in range(11, 21))
total_debt = sum(ws[f'F{r}'].value or 0 for r in range(11, 14))
implied_equity = total_uses - total_debt

# Compute OID fees from write-plan inputs (do NOT read K15 — it's a formula
# cell that returns None via openpyxl without data_only)
oid_fees = 0
if 'T33' in write_plan_values and 'F12' in write_plan_values:
    tl_oid_pct = (100 - write_plan_values['T33']) / 100  # e.g., 98 → 0.02
    oid_fees += write_plan_values['F12'] * tl_oid_pct
if 'T32' in write_plan_values and f11_value:
    rcf_oid_pct = (100 - write_plan_values['T32']) / 100
    oid_fees += f11_value * rcf_oid_pct

total_uses_with_fees = total_uses  # K15 (fees) already in SUM(K11:K20) via formula
implied_equity_check = total_uses - total_debt

if implied_equity < 0:
    print(f"WARNING: Negative implied equity ({implied_equity}). "
          f"Debt exceeds uses — check inputs.")
if total_uses == 0:
    print("WARNING: No uses populated. K11-K20 may be empty.")
```

**Note:** K15 (`=V35`, total financing fees from OID calculations) is a formula cell.
When checking S&U balance outside Excel, compute OID fees manually from the write-plan
inputs (TL × (1 − OID/100) + RCF × (1 − OID/100)) rather than reading K15.

---

## Bespoke Deal Escalation

### Trigger Conditions

HALT and present to the user if the CIM discloses ANY of:

| Non-Standard Component | What to Flag |
|------------------------|--------------|
| HoldCo debt | Structural subordination layer |
| PIK notes | Cash flow priority implications |
| Seller notes | Subordinated tranche below TL |
| Preferred equity | Quasi-debt with priority claims |
| Minority equity raises | Multiple equity tranches |
| Earn-outs | Contingent consideration |
| Multiple equity tranches | Complex waterfall |
| Mezzanine / second lien | Additional debt layers |
| Convertible instruments | Contingent dilution |

### Escalation Protocol

When a bespoke trigger is detected, present to the user:

1. **Full capital stack as read from the CIM** — all tranches, amounts, seniority
2. **Which tranches are non-standard** — with the trigger condition that applies
3. **What SUCAP tab modifications would be required** — e.g., "Seller note requires
   adding a row between TL and Owner Equity; Pro Forma Cap table needs additional
   leverage calc rows"
4. **Recommended approach** — e.g., "Size the senior facility per standard rules;
   model the seller note as a separate input row; adjust TEV multiple to reflect
   full enterprise value including sub-debt"

Wait for user confirmation before proceeding with any writes.

---

## TEV and Implied Equity

### TEV Multiple (J41)

Input cell for the implied TEV / LTM CA EBITDA multiple. If the CIM discloses a
transaction multiple or comps-based valuation, enter it here.

```
TEV (I41) = LTM CA EBITDA (I43) × TEV Multiple (J41)
Total Capitalization (I40) = TEV + Cash
Implied Equity (I39) = Total Cap – Total Debt – Common Equity
```

If the CIM states "12.2x comps-based valuation" or "TEV of $390M on $32M EBITDA,"
derive the multiple and enter in J41.

### Cash at Close (I30)

Pro forma cash & equivalents. Often disclosed in the CIM's pro forma capitalization
or balance sheet. Enter as a positive number in $000s.
