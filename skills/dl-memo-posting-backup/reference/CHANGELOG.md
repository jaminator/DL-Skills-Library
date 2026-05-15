# CHANGELOG: populating-posting-memo-backup

## Contents

- v3 (2026-03-23)
- v2 (2026-03-20)
- v1 (2026-03-20)

## v3 (2026-03-23)
**Status:** Ready for QA retest (cycle 3)
**Author:** Overland Skills Lab

### Changes from v2

**QA report:** `QA_Diagnostic_Report_populating-posting-memo-backup_v2.md` (2026-03-20, Sonnet 4.6, Project LoneStar)

#### MEDIUM findings addressed (3 of 3)

**1. Step 0 consolidated single-message requirement strengthened (Finding D1-F1)**
- Rewrote Step 0 to explicitly require all four items in a **single message**
- Changed "all three items" → "all four items" (v2 text was inconsistent with the four-item list)
- Added bold instruction: "Do not split them across multiple messages or follow-ups"
- Moved the blank-vs-estimate caveat for cash taxes inline with the item description rather than as a separate quoted statement
- Added fast-path: "If the user's invocation message already provides all four items, confirm them and proceed directly to Step 1 without re-asking"
- Example 1 Step 0 updated to show all four items in one message with consistent wording

**2. Test coverage gaps flagged for Aqueduct retest (Finding D2-F1)**
- No SKILL.md changes — this was a QA process gap (LoneStar used instead of Aqueduct)
- A-08 (close-date LTM EBITDA override) and A-10 (GP fallback / Contribution Margin substitution) remain untested against v2 logic
- Recommended retest section below specifies Aqueduct as mandatory primary test material

**3. No-S&U protocol documented (Finding D4-F1)**
- New Step 4c in SKILL.md: explicit branch for CIPs with no Sources & Uses page
- Protocol: halt, flag absence, solicit TL size (or leverage target), funded RCF, and use-of-proceeds from analyst in a single message
- Once inputs received, apply standard Overland RCF Funding Rule and DDTL sizing
- New "No-S&U Protocol" section in structuring-rules.md with trigger conditions, protocol steps, and worked example
- Covers early-stage sell-side processes, DCM marketing CIPs, and staple financing packages

### Components unchanged from v2

- **Formula protection logic** — pre-write `is_formula()` check: PASSED v2 QA, no changes
- **FCCR addback guide** — Tier 1/Tier 2 classification, P12 override: PASSED v2 QA, no changes
- **As-reported / adjusted discipline** — Rows 11, 14, 18, 23 rules: PASSED v2 QA, no changes
- **Bespoke escalation protocol** — trigger conditions, escalation format: PASSED v2 QA, no changes
- **K2-first date architecture** — column mapping, M2/O/R adjustments: PASSED v2 QA, no changes
- **RCF Funding Rule** — derivation, presentation, override flagging: PASSED v2 QA (partial — no S&U case now documented)
- **DDTL Proactive Sizing** — 20% formula, F13 = $0, U34 commitment: PASSED v2 QA, no changes
- **Uses clean-up** — blank unused placeholder rows: PASSED v2 QA, no changes
- **Output summary template** — all required sections present: PASSED v2 QA, no changes

### Files

```
populating-posting-memo-backup/
├── v3/
│   ├── SKILL.md                          (~395 lines)
│   ├── EXAMPLES.md                       (~275 lines, minor Step 0 wording update)
│   ├── references/
│   │   ├── cell-map.md                   (~381 lines, header date update only)
│   │   ├── fccr-addback-guide.md         (183 lines, unchanged)
│   │   └── structuring-rules.md          (~290 lines, +No-S&U Protocol section)
├── CHANGELOG.md                          (this file)
```

### Recommended retest scope for v3

**Primary test material: Project Aqueduct** (mandatory — exercises A-08 and A-10 not covered by LoneStar)

- **Full retest — Confirmation Gates (Dimension 1):** Verify all four Step 0 items solicited in a single message. Also test TC-NEW-02: user provides all four items in invocation message — verify skill confirms and proceeds without re-asking.
- **Full retest — Extraction Quality (Dimension 2):** A-08 (close-date LTM EBITDA override from FCF bridge page) and A-10 (GP fallback / Contribution Margin substitution). These are v2 HIGH-fix test cases that remain unverified.
- **Full retest — Capital Structure (Dimension 4):** A-11 (RCF Funding Rule) on Aqueduct (has S&U page). Also test TC-NEW-01: CIP with no S&U page — verify skill halts, flags absence, and solicits inputs per documented protocol.
- **Spot-check — Column Mapping (Dimension 3):** No changes; confirm no regression.
- **Spot-check — Formula Protection (Dimension 5):** No changes; confirm no regression.
- **Spot-check — As-Reported/Adjusted (Dimension 6):** Confirm GP fallback works correctly on Aqueduct.
- **Spot-check — Output Completeness (Dimension 7):** No changes; confirm no regression.

**New test cases:**
- **TC-NEW-01:** CIP with no S&U page (DCM staple / early-stage sell-side) — verify skill halts, flags absence, and solicits capital structure inputs per the new Step 4c / No-S&U Protocol.
- **TC-NEW-02:** User provides all four Step 0 inputs in the invocation message — verify skill confirms rather than re-asking and proceeds directly to Step 1.

**Secondary (if resources permit):** A CIM with an explicit LTM stub period (e.g., LTM 9/30/25) to verify K2-first rule and column R independent-data path (non-link scenario).

---

## v2 (2026-03-20)
**Status:** QA tested — 0 Critical, 0 High, 3 Medium, 0 Low → triggers v3
**Author:** Overland Skills Lab

### Changes from v1

**QA report:** `QA_Report_populating-posting-memo-backup_v1.md` (2026-03-20, Sonnet 4.6, Project Aqueduct)

#### HIGH findings addressed (6 of 6)

**1. Step 0 gate enforced (Finding: Step 0 Skipped)**
- Rewrote Step 0 as a mandatory pre-extraction gate with explicit halt language
- Added cash taxes as a fourth solicitation item with blank-vs-estimate policy
- Added bold instruction: "This step must complete before any CIM reading begins"
- If user's invocation message omits any item, skill halts and asks before proceeding

**2. FCF bridge / debt model page added to Step 1 targets (Finding: LTM EBITDA Extraction Miss)**
- Added "Projected FCF bridge / debt model page" to the target pages list in Step 1
- Added extraction rule in Step 2 LTM column rules: when close date differs from most recent FYE, check FCF bridge for close-date EBITDA figure
- Added CIM-to-Template mapping entry for "Pro Forma Adjusted EBITDA — Closing Stub" → L23
- Example 1 rewritten to show the $31.0M close-date figure taking precedence over $31.5M FYE QoE figure

**3. No-explicit-LTM-period rule added to Step 2 (Finding: Column Map Incorrect Initial Proposal)**
- Added explicit LTM column rules subsection in Step 2 with three scenarios: explicit LTM, no LTM within 6 months of FYE, and close-date EBITDA override
- When no LTM exists and close date is within 6 months of FYE, skill proposes mapping most recent FYE to column L with confirmation prompt
- Example 1 demonstrates this exact scenario end-to-end

**4. G2 anchor rule replaced with K2-first rule (Finding: G2 Anchor Date Wrong)**
- Replaced "G2 = FYE before first CIM historical year" with "K2 = last actual FYE, derive G2 backward"
- Added sub-steps for M2 formula adjustment when standard cascade produces wrong projection year
- Added sub-steps for column O (CAGR) formula updates when G data rows are empty
- Added sub-steps for column R data cells linked to K when LTM = FYE
- New "Conditionally Modified Formulas" section in cell-map.md documents M2, column O, and column R as intentional formula modifications exempt from pre-write block
- Date Architecture section in cell-map.md rewritten with K2-first derivation procedure and two worked examples (no-explicit-LTM and explicit-LTM)
- Output summary template updated to include "INTENTIONAL FORMULA MODIFICATIONS" section

**5. Overland RCF Funding Rule documented and implemented (Finding: RCF Funded Amount Not Applied)**
- New "Overland RCF Funding Rule" section in structuring-rules.md with derivation sequence, worked example, and presentation template
- Step 4 rewritten as "Apply Overland Structuring Rules" — skill derives RCF funded amount and TL independently before accepting user input
- Extraction summary now presents derived structure with formula chain visible
- User override accepted but flagged: "Note: User override — [cell] set to $X vs. rule-derived $Y"
- Example 1 demonstrates the full RCF derivation ($31M − $25M = $6M funded, TL = $105M − $6M = $99M)

**6. DDTL Proactive Sizing Rule added (Finding: DDTL Not Sized)**
- New "DDTL Proactive Sizing" section in structuring-rules.md replacing the old "DDTL Rules" section
- Two-part rule: (1) proactive sizing at 20–30% of funded TL (preference: bottom of range), (2) CIM validation if CIM discloses a DDTL
- Formula: DDTL = ROUND(TL ÷ (1 − 20%) × 20%, nearest $1M)
- F13 = $0 (funds post-close), U34 = derived commitment
- DDTL impact on FCCR denominator (P17 commitment fee) documented
- Example 1 demonstrates: $99M TL → $25M DDTL commitment

#### MEDIUM findings addressed (5 of 5)

**7. Gross Profit fallback to Contribution Margin (Finding: No Proactive Alternative Offered)**
- Added fallback rule to Step 3: if as-reported GP unavailable but contribution margin disclosed, offer to relabel C14 and populate
- Updated cell-map.md Row 14 note to include "(or Contribution Margin with relabeled C14)"
- Example 1 demonstrates the substitution with explicit confirmation prompt

**8. Cash taxes blank-vs-estimate policy (Finding: P13 Estimated Without Basis)**
- Added cash taxes as Step 0 solicitation item #4 with explicit wording: "If you don't have a cash tax figure, I'll leave P13 blank"
- Added Step 3 extraction rule: "If CIM does not disclose cash taxes, leave P13 blank. Do NOT estimate or infer."
- Output summary template includes "CASH TAXES (P13): [value or 'left blank — analyst to provide']"

**9. Visual cross-reference policy clarified (Finding: Cross-Reference Not Performed)**
- Step 1 sub-step 4 rewritten: S&U page and QoE bridge page ALWAYS cross-referenced regardless of text quality; other financial pages cross-referenced when text quality is uncertain
- Changed from unconditional requirement on all financial pages to tiered approach: mandatory for highest-stakes pages, conditional for others

**10. Cash from Balance Sheet → Owner Equity plug documented (Finding: Mapping Undocumented)**
- New "Cash from Balance Sheet Mapping" section in structuring-rules.md
- Documents that CIM "Cash from Balance Sheet" absorbs into F14 plug
- Documents F14 → I38 dependency chain
- Output summary template includes flag language for this mapping
- Example 2 updated to show the mapping note in bespoke escalation context

**11. L9 label conditional note added (Finding: "LTM 12/24A" Displayed When "FY'24A" Correct)**
- Added L9 label note to Step 2 LTM column rules: when L2 = FYE date, flag that L9 will display as "LTM M/YYA" and instruct analyst to manually update in Excel
- Example 1 demonstrates the flag in the column map presentation

#### LOW findings addressed (3 of 3)

**12. S&U balance check script fixed (Finding: False Negative from K15 formula read)**
- Updated balance check script in structuring-rules.md to compute OID fees from write-plan inputs rather than reading K15 via data_only
- Added note to cell-map.md inspection notes for K15

**13. Uses clean-up step added (Finding: Blank Placeholders Not Cleared)**
- Added Step 5 write sequence item #8: blank unused "[Use]" placeholder rows between last populated use and Financing Fees row
- Added "Uses clean-up" note to cell-map.md SUCAP Uses section

**14. Tank Owner / subscription-service AP mapping note added (Finding: Mapping Judgment)**
- Added note to CIM-to-Template Mapping Notes section in SKILL.md
- Added "Tank Owner Payments (service cos.)" to Row 52 common labels in cell-map.md

### Components unchanged from v1

- **Formula protection logic** — pre-write `is_formula()` check including ArrayFormula detection: PASSED QA, no changes
- **FCCR addback guide** — Tier 1/Tier 2 classification and P12 override syntax: PASSED QA, no changes
- **As-reported / adjusted discipline** — extraction rules for Rows 11, 14, 18, 23: PASSED QA, no changes (enhanced with GP fallback but core rules intact)
- **Bespoke escalation protocol** — trigger conditions and escalation format: PASSED QA, no changes

### Files

```
populating-posting-memo-backup/
├── v2/
│   ├── SKILL.md                          (382 lines)
│   ├── EXAMPLES.md                       (~260 lines)
│   ├── references/
│   │   ├── cell-map.md                   (~310 lines)
│   │   ├── fccr-addback-guide.md         (182 lines, unchanged)
│   │   └── structuring-rules.md          (~240 lines)
├── CHANGELOG.md                          (this file)
```

---

## v1 (2026-03-20)
**Status:** QA tested — Conditional Pass (6 HIGH, 5 MEDIUM, 3 LOW findings)
**Author:** Overland Skills Lab

### Initial Design

**Problem solved:** Manually extracting financial data from CIMs and populating the
posting memo backup template is time-consuming, error-prone (especially column mapping
and as-reported/adjusted conflation), and creates consistency risk across deals.

**Scope:** Populates FinSum and SUCAP tabs from CIM/CIP data. Does not touch Detailed
FinSum or Returns tabs (formula-driven downstream). Does not perform credit analysis
or generate memo prose.

### Key Design Decisions

1. **Cell map derived from direct template inspection, not from prompt memory.**
   Inspection revealed 6 cells described as inputs in the prompt that are actually
   formulas: U32, F14, P12, S34, T34, K15. The cell map is the authoritative
   reference; all workflow steps reference it.

2. **Three mandatory user confirmation gates:**
   - Column map (Step 2) — prevents systemic date/column errors
   - Extraction summary (Step 3) — prevents data quality errors
   - Bespoke escalation (Step 4, conditional) — prevents structural errors

3. **Pre-write formula validation is a hard gate, not a warning.** The `is_formula()`
   check includes ArrayFormula detection (for DSO row G61) and halts on any formula
   cell in the write plan.

4. **FCCR P12 override is an analyst decision, not automatic.** The template default
   (deduct all adjustments) is ultra-conservative. Tier 1/Tier 2 treatment requires
   deliberate override documented in the FCCR addback guide.

5. **Progressive disclosure keeps SKILL.md at 265 lines.** Three reference files
   handle lookup tables and detailed rules. EXAMPLES.md provides three annotated
   scenarios.

6. **Adaptive CIM reading strategy** handles both image-based (ZIP of JPEGs) and
   text-extractable PDFs. Validated against the Aqueduct CIP (63-page image-based
   slide deck).

### Known Constraints

- NWC data often available for only one balance sheet date in the CIM
- CIM label-to-template-row mapping requires judgment (documented in SKILL.md)
- Non-calendar FYE creates column J redundancy (documented in Example 3)
- Detailed FinSum tab has independent date architecture not linked to FinSum G2
- Template C9 label ("FYE December 31st") is static text — not auto-updated
