# CFO Error Patterns

This reference enumerates the most common error patterns observed on borrower compliance certificates and how to classify them in the validation output. Use this in Step 5 (Flag and classify each issue) of the workflow in `SKILL.md`.

The deck flags this category specifically: *"Compliance certs frequently contain CFO arithmetic errors; OL catches manually."* The goal of this skill is to surface these errors before the certificate reaches a reviewer's desk, so the reviewer's time goes to judgment rather than to arithmetic.

## Contents

- Pure arithmetic errors
- Definitional misapplications
- Period mismatches
- Tranche / scope errors
- Sign and direction errors
- Disclosure omissions

---

## Pure arithmetic errors

**What they look like.** The reported covenant value does not match the value you compute from the inputs the certificate itself cites.

**Examples.**
- Sum of addbacks does not equal the difference between reported EBITDA and the income-statement number.
- Reported leverage of `4.8x` when `Total Debt of 1,200 / EBITDA of 240` clearly equals `5.0x`.
- Reported FCCR of `1.45x` when the cited inputs produce `1.32x`.

**How to classify.** `arithmetic_error_flag = true`. In `reviewer_notes`, write a concise note: "Reported `4.8x`; recomputed `5.0x` from inputs cited on certificate (Total Debt $1,200M, EBITDA $240M). 4.2% discrepancy."

---

## Definitional misapplications

**What they look like.** The borrower computed the covenant using a definition that is not the one in the credit agreement.

**Examples.**
- Borrower nets cash without applying the agreement's `$75M` netting cap.
- Borrower excludes the seller note from Total Debt when the agreement defines Total Debt to include it.
- Borrower applies addbacks that are not on the agreement's list (e.g., adds back "growth investments" when the agreement only permits "transaction expenses, restructuring charges, and stock-based compensation").
- Borrower uses GAAP EBITDA as the base when the agreement defines a "Consolidated EBITDA" with specific adjustments.

**How to classify.** `definition_misapplication_flag = true`. In `reviewer_notes`, cite the agreement section and explain the divergence: "Section 7.10(a) caps cash netting at $75M; certificate netted full $112M cash balance. Recomputed leverage with capped netting yields 5.3x vs. reported 4.7x."

When the misapplication produces a value that crosses a covenant threshold, also set `arithmetic_error_flag = true` and `in_compliance = false` based on the recomputed value.

---

## Period mismatches

**What they look like.** The certificate uses a test period different from what the agreement requires.

**Examples.**
- Agreement requires LTM as of period end; certificate uses LTM as of one month prior.
- Agreement specifies NTM forward look for capex coverage; certificate uses TTM trailing.
- Quarterly certificate uses YTD figures rather than annualizing.

**How to classify.** `definition_misapplication_flag = true`. In `reviewer_notes`, identify the period used and the period required: "Certificate uses LTM as of 11/30; Section 1.01 defines test period as LTM as of fiscal quarter end (12/31). Recompute pending receipt of corrected period inputs."

When the inputs to recompute on the correct period are not on the certificate, mark the recomputed value as `[INSUFFICIENT DATA — period_inputs_unavailable]`.

---

## Tranche / scope errors

**What they look like.** A covenant tested on the wrong scope of debt or the wrong consolidation.

**Examples.**
- Senior Secured Net Leverage computed using Total Debt rather than just senior secured.
- First Lien Leverage including last-out tranche debt.
- Consolidated covenant tested on the operating subsidiary only (excluding holdco debt that should be included).
- Aggregate net leverage computed on a per-fund basis rather than the borrower group basis the agreement requires.

**How to classify.** `definition_misapplication_flag = true`. In `reviewer_notes`, name the scope error: "Senior Secured Net Leverage at Section 7.11 measured against Senior Secured Debt; certificate included $150M unsecured notes in the numerator. Recomputed at 4.1x vs. reported 4.6x."

---

## Sign and direction errors

**What they look like.** A reported value that satisfies the threshold under the wrong direction.

**Examples.**
- Threshold is "min ≥ 1.10x" but the certificate text reads "max 1.10x" and reports `0.95x` as compliant.
- Threshold steps down (5.5x → 5.0x → 4.5x) but the certificate uses the prior-quarter step.

**How to classify.** This is a hybrid flag. Set `arithmetic_error_flag = true` if the misapplied threshold leads to a wrong compliance determination. Set `in_compliance` based on the **correct** threshold direction. In `reviewer_notes`, explain: "Section 7.10(a) tests Total Net Leverage as a maximum (≤ 5.0x for fiscal 2026 onwards). Certificate applied the 5.5x prior-period step; correct threshold is 5.0x. Reported 5.2x is non-compliant under the current step."

---

## Disclosure omissions

**What they look like.** A required covenant or disclosure is missing entirely.

**Examples.**
- The agreement requires reporting all three of Total Net Leverage, Senior Secured Net Leverage, and Fixed Charge Coverage; the certificate reports only two.
- The agreement requires a separate liquidity certification; the certificate omits it.
- The agreement requires a "no Default or Event of Default" representation; the certificate's representation language omits the EoD prong.

**How to classify.** Add a synthetic entry to the `covenants` list with `reported_value = None`, `recomputed_value = None`, `arithmetic_error_flag = false`, `definition_misapplication_flag = true`, and `reviewer_notes = "Required covenant per Section 6.02(a)(iii) not reported on certificate."`. The output's `insufficient_data_fields` list should include the missing covenant name.

---

## Calibrating the materiality threshold

The skill workflow suggests > 0.5% of the threshold value or any sign change as the materiality cutoff for `arithmetic_error_flag`. This is a default. The reviewer may calibrate it for specific facilities (a tighter book may want > 0.1%; a noisier reporting borrower may want > 1%). The default is conservative — set the flag and let the reviewer decide whether to dismiss it. False positives waste a reviewer's seconds; false negatives miss a real error.

---

## When the underlying inputs are not cited

If the certificate reports a covenant value but does not cite the underlying inputs (no breakdown of what went into EBITDA, no debt schedule), recomputation is not possible. Mark `recomputed_value = None` and `reviewer_notes = "Underlying inputs not cited on certificate; cannot recompute. Reviewer should request input detail from borrower."`. Do not assume the reported value is correct — surface the gap.
