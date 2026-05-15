# Covenant Types and Definitional Patterns

This reference enumerates the most common covenant types encountered on US-MM non-sponsored direct lending compliance certificates, their typical definitional patterns, and the inputs the recomputation requires. Use this to ground Step 2 (Locate covenant definitions) and Step 3 (Recompute each covenant) of the parsing workflow in `SKILL.md`.

## Contents

- Total Net Leverage Ratio
- Senior Secured Net Leverage Ratio
- First Lien Net Leverage Ratio
- Fixed Charge Coverage Ratio
- Interest Coverage Ratio
- Debt Service Coverage Ratio
- Minimum EBITDA / Minimum Liquidity
- Capex Limit
- Dividend / Restricted Payment Capacity

---

## Total Net Leverage Ratio

**Typical formula.** `(Consolidated Total Debt − Unrestricted Cash up to a cap) / Consolidated EBITDA (LTM)`

**Threshold direction.** Max (ceiling). Often steps down by quarter or year per the agreement.

**Definitional anchors to verify in the agreement.**
- `Consolidated Total Debt` — what is included (e.g., does it include synthetic L/Cs, drawn RCF, undrawn DDTL accruing commitment fees that are convertible to debt, the seller note, finance leases). What is excluded (operating leases under ASC 842 typically excluded; subordinated holdco notes sometimes excluded).
- `Unrestricted Cash` — the netting cap (commonly $75M or 50% of revolver size). Confirm the cap matches the certificate's netting calculation.
- `Consolidated EBITDA` — the addback list. The most common CFO error pattern is over-aggressive addbacks, so list the addbacks explicitly in `reviewer_notes` and confirm each is allowed by the definition.
- Test period — typically LTM as of the period end. Confirm the period ending date matches.

## Senior Secured Net Leverage Ratio

**Typical formula.** `(Senior Secured Debt − Unrestricted Cash up to a cap) / Consolidated EBITDA (LTM)`

**Threshold direction.** Max.

**Definitional anchors to verify.** Same as Total Net Leverage but the numerator is restricted to senior secured tranches. Common error: including subordinated debt or unsecured notes in the numerator.

## First Lien Net Leverage Ratio

**Typical formula.** `(First Lien Debt − Unrestricted Cash up to a cap) / Consolidated EBITDA (LTM)`

**Threshold direction.** Max.

**Definitional anchors.** Numerator restricted to first lien instruments. Often the controlling covenant in unitranche structures where there is a single tranche but the agreement still distinguishes first-out / last-out for waterfall purposes.

## Fixed Charge Coverage Ratio

**Typical formula.** `(Consolidated EBITDA − Capex − Cash Taxes) / (Cash Interest + Scheduled Principal + Cash Taxes — sometimes — + Restricted Payments)`

**Threshold direction.** Min (floor). Often `≥ 1.10x` or `≥ 1.25x`.

**Definitional anchors to verify.**
- Whether the numerator includes a maintenance capex deduction or all capex.
- Whether the denominator includes scheduled principal amortization plus required term-loan repayments.
- Whether restricted payments (dividends, equity buybacks) are in the denominator.
- The test period (often LTM, sometimes prospective NTM).

## Interest Coverage Ratio

**Typical formula.** `Consolidated EBITDA / Consolidated Interest Expense`

**Threshold direction.** Min (floor).

**Definitional anchors.** Confirm whether interest expense is cash interest only or includes accrued PIK interest. Confirm whether commitment fees, agent fees, and ticking fees are included.

## Debt Service Coverage Ratio

**Typical formula.** `(Consolidated EBITDA − Capex − Cash Taxes) / (Cash Interest + Scheduled Principal)`

**Threshold direction.** Min.

**Definitional anchors.** Similar to FCCR but typically narrower denominator (no restricted payments).

## Minimum EBITDA / Minimum Liquidity

**Typical formula.** `Consolidated EBITDA (LTM) ≥ $X` or `Available Liquidity ≥ $Y`.

**Threshold direction.** Min.

**Definitional anchors.** Liquidity = unrestricted cash + revolver availability (net of L/C usage). Confirm the calculation includes the borrowing-base cap if applicable.

## Capex Limit

**Typical formula.** `Capex (TTM or annual) ≤ $X` with a carryforward / build-forward bucket.

**Threshold direction.** Max.

**Definitional anchors.** Confirm the carryforward mechanic (typically 50% of unused capacity rolls one year). Confirm whether maintenance and growth capex are tested separately.

## Dividend / Restricted Payment Capacity

**Typical formula.** Tested via "available amount" basket: starter amount + 50% cumulative net income + qualifying equity contributions − prior restricted payments.

**Threshold direction.** Max (capacity ceiling).

**Definitional anchors.** Verify the starter amount and the cumulative net income definition. Confirm the agreement's specific exclusions (e.g., losses count fully against, gains count at 50%).

---

## How to use this reference

In Step 3 of the workflow, for each covenant identified on the certificate:

1. Locate the matching covenant pattern above.
2. Cross-reference against the credit agreement section provided in the project context.
3. Compute from the inputs cited on the certificate, applying the agreement's specific definitional choices (which addbacks, which cap, which period).
4. Compare to reported. Flag arithmetic errors. Flag definitional misapplications (e.g., the agreement excludes operating leases but the certificate included them).

When a covenant on the certificate does not match any pattern above and no clear definition is in the agreement excerpts provided, mark `[INSUFFICIENT DATA — covenant_definition_not_located]` and surface to the reviewer rather than guessing.
