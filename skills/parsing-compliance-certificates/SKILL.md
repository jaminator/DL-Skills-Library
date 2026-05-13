---
name: parsing-compliance-certificates
description: Extracts covenant metrics from borrower compliance certificate PDFs, recomputes them against the credit agreement's specific definitions, and surfaces CFO arithmetic errors and definitional misapplications for asset management review. Produces a structured ComplianceCertificateValidation output with per-covenant calculations, headroom percentages, error flags, and an overall compliance status. Use when reviewing a quarterly or monthly compliance certificate, validating covenant calculations against the credit agreement, or preparing the AM portfolio monitoring update.
---

# Parsing Compliance Certificates

This skill turns a borrower-delivered compliance certificate into a structured validation report that the asset management team can review and approve. It handles the full extract → recompute → compare → flag pipeline that today is performed manually and consumes meaningful AM time per facility per period.

## When to use this skill

- Quarterly or monthly compliance certificate has arrived from a borrower.
- An ad-hoc compliance verification is needed before approving an RCF or DDTL draw.
- The AM portfolio monitoring update is being prepared and a per-facility validation summary is required.

## What you need before invoking

The skill operates inside a Claude Desktop project that has uploaded:

1. **The compliance certificate.** Typically a PDF from the borrower's CFO, often in non-standard format. The skill expects to see at minimum: the period being certified, the covenant names, the values reported, and the underlying inputs (EBITDA, total debt, interest expense, fixed charges, etc.) used to compute them.
2. **The relevant credit agreement excerpts.** The covenant definitions section (typically Article VII or a "Financial Covenants" section), plus the defined-terms section that anchors the financial inputs (Consolidated EBITDA, Consolidated Total Debt, Fixed Charges, etc.). Full credit agreement is acceptable but the relevant sections must be locatable.
3. **The prior period's compliance certificate** (recommended, not required). Used to cross-check trends and identify period-over-period anomalies.
4. **Facility metadata.** The facility name, facility id (if known), tranche structure, and reporting period.

## Workflow

Copy this checklist into the working response and check items off as they are completed:

```
Compliance Certificate Validation:
- [ ] Step 1: Parse the certificate
- [ ] Step 2: Locate covenant definitions
- [ ] Step 3: Recompute each covenant
- [ ] Step 4: Compare reported vs. recomputed
- [ ] Step 5: Flag and classify each issue
- [ ] Step 6: Assemble the validation output
```

### Step 1: Parse the certificate

Read the certificate end-to-end. Extract:

- The period being certified (e.g., quarter-end date).
- The CFO or finance officer signatory and date signed.
- Each covenant tested, with: covenant name as written, threshold, threshold direction (max ceiling vs. min floor), and reported value.
- The underlying inputs cited on the certificate for each covenant calculation.

If the certificate is illegible in places, mark those fields with `[INSUFFICIENT DATA — <what is missing>]`. Do not silently omit. Do not infer values that the certificate does not report.

### Step 2: Locate covenant definitions

For each covenant identified in Step 1, locate the credit agreement section that defines:

- The exact computation formula (numerator and denominator).
- The relevant addbacks, exclusions, and adjustments to the financial inputs.
- The applicable test period (LTM, NTM, quarterly, etc.).
- The tranche scope (consolidated vs. senior secured vs. specific facility).
- The covenant level and threshold direction.

Cite the section number in the output (e.g., `"Section 7.10(a)"`). See the canonical taxonomy in `reference/covenant-types.md` for the most common covenant types and their definitional patterns.

### Step 3: Recompute each covenant

Using the underlying inputs cited on the certificate plus the credit agreement definitions, compute each covenant from first principles. The recomputation is the heart of the validation — it surfaces CFO arithmetic errors directly.

If the certificate cites inputs that do not match the credit agreement definition (for example, uses Adjusted EBITDA without specifying which addbacks are included, or uses Total Debt that excludes a tranche the agreement requires), do not fabricate the missing detail. Mark `definition_misapplication_flag = true` and explain in `reviewer_notes`.

### Step 4: Compare reported vs. recomputed

For each covenant, compute:

- The absolute and percentage difference between reported and recomputed values.
- Whether the recomputed value satisfies the threshold (`in_compliance`).
- Headroom: absolute distance to threshold and percentage distance.

A material difference (suggested heuristic: > 0.5% of the threshold value, or any sign change) triggers `arithmetic_error_flag = true`.

### Step 5: Flag and classify each issue

For each covenant entry, set:

- `arithmetic_error_flag` — true when reported and recomputed values differ materially.
- `definition_misapplication_flag` — true when the certificate applied the definition incorrectly.
- `reviewer_notes` — concise observation citing which inputs and which agreement section.

For the overall certificate, populate `summary_flags` with one human-readable line per significant issue.

See `reference/cfo-error-patterns.md` for the most commonly observed error patterns and how to classify them.

### Step 6: Assemble the validation output

Produce the output as a single `ComplianceCertificateValidation` JSON object matching the schema. Required at the top of the output:

- `[DRAFT — HUMAN REVIEW REQUIRED]` watermark.
- `requires_human_review: true`, `review_state: "PENDING_REVIEW"`.
- An `overall_status` of `compliant` only when every covenant is in compliance, no flags are set, and no fields are `[INSUFFICIENT DATA]`. Otherwise `non_compliant` (when any covenant fails its threshold) or `review_required` (when any flag is set or any value is missing).

End with a one-line handoff: "AM reviewer to verify flagged items and either approve, request revision, or escalate."

## Output requirements

The output is a single JSON object that conforms to the `ComplianceCertificateValidation` schema. It must:

- Include the `[DRAFT — HUMAN REVIEW REQUIRED]` watermark at the top.
- Carry `review_state: "PENDING_REVIEW"`.
- Use `[INSUFFICIENT DATA — <what is missing>]` for any missing field, never silently omit.
- Cite the credit agreement section for every covenant definition.
- Include a `reviewer_notes` field for any covenant with a flag set.

## Anti-patterns

- Do not fabricate covenant values when the certificate is illegible. Use the `[INSUFFICIENT DATA]` marker.
- Do not infer credit agreement definitions from general knowledge. Cite the section. If the section is not provided, mark `[INSUFFICIENT DATA — credit_agreement_section_not_provided]`.
- Do not collapse multiple covenants into a single entry. Each covenant gets its own row.
- Do not treat a sign-direction inversion (e.g., reported `4.5x` for a max-`5.5x` covenant interpreted as compliant when actually breach due to an inputs typo) as a soft flag — it is an arithmetic error.

## Reference materials

- `reference/covenant-types.md` — canonical covenant types and definitional patterns
- `reference/cfo-error-patterns.md` — common CFO arithmetic error patterns and how to classify them

## Notes on portability into Arrakis

This skill maps directly into the A12 Corrino "Compliance Certificate Parser" feature in the Arrakis blueprint. The same Pydantic output schema applies; the same definitional citation pattern carries through; the same `PENDING_REVIEW` state seeds the Corrino HITL state machine. When the artifact graduates, the underlying prompt is invoked through Spice, and the structured output lands in `CORRINO_LAND` for downstream covenant tracking. No rewrite of the skill body is required at graduation.
