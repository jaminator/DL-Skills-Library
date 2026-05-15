---
name: dl-memo-posting
description: >
  Populates the Overland Advantage Posting Memo Word template (.docx) directly
  from deal materials (CIMs, teasers, CIPs, management presentations, financials,
  term sheets), returning a fully populated copy of the template ready for the
  posting team. Use when the user shares deal materials and asks to draft, post,
  or write up a credit ("post this deal," "draft the memo," "write up this credit,"
  "populate the posting memo"), or references any specific memo section
  (Situation Overview, Company Overview, D&A, Strengths, Considerations, Risk
  Flags, Recommendation, Designated Criteria). Applies the Overland credit quality
  framework as the analytical lens for D&A commentary, Strengths & Considerations,
  and Recommendation — mapped to memo sections, not the full FCF decomposition
  sequence. Output is a populated .docx file (`assets/posting-memo-template.docx`
  edited in-place via `scripts/populate_memo.py`) — not a recreated Word document.
---

# Overland Posting Memo — Population Guide

## STEP 0 — ORIENTATION

When deal materials are provided, draft content for each memo section listed
below, then run `scripts/populate_memo.py` to write the content into the
template at `assets/posting-memo-template.docx` and return the populated file.

**The deliverable is a populated `.docx` file, not text section drafts.** The
script edits the bundled Word template in-place (preserving all formatting,
numbering, and styles) and saves the populated copy under a deal-specific
filename. See `reference/population-mechanics.md` for the exact workflow.

For per-section detail beyond what is in this file, see:
- [`reference/memo-sections.md`](reference/memo-sections.md) — Financial D&A
  per-bullet content standards (6 sub-sections) and Risk Flags definitions /
  assignment logic for all 15 items
- [`reference/base-rate-framework.md`](reference/base-rate-framework.md) —
  Tiered evidence hierarchy for benchmarking the Company against external
  reference classes (consult when drafting D&A bullets that involve margin,
  growth, or capital intensity sustainability assessments)
- [`reference/population-mechanics.md`](reference/population-mechanics.md) —
  STEP 13 population workflow: content-dict schema pointer, the run snippet,
  bullet-format conventions, and the out-of-scope list

**Data availability principle:** Use TBD liberally for items not disclosed in
available materials. Never fabricate financial figures, customer names, or
deal terms not present in the source. Flag TBD items with a brief parenthetical
noting the missing data source — e.g., `TBD (not disclosed in CIP)`.

**Tone:** Terse, institutional. No narrative throat-clearing. Lead every section
with the most important fact. Financial figures in $XMM format. Percentages to
one decimal place.

**No posting team follow-ups anywhere in the memo.** The memo reports facts. It
does not assign tasks, recommend calls, prescribe diligence steps, or direct the
posting team toward investigations. This applies to every section — header fields,
Situation Overview, D&A, Considerations, and Recommendation alike.

**No speculation or conditional hedging.** Report what the data shows. If a metric
deviates from the Company's historical baseline, flag the deviation and its
magnitude. Do not speculate about causes or sustainability unless the source
materials provide explicit evidence.

**CA EBITDA is the standard label.** Use "CA EBITDA" throughout. Do not use
"Adjusted EBITDA" or "Diligence Adjusted EBITDA" in any section of the memo output.

**Concision is a feature.** Every sentence in the memo should earn its place. If a
sentence does not convey a financial fact, a material metric, or a necessary
contextual detail, cut it.

## ANALYTICAL FRAMEWORK — BASE RATE EVIDENCE HIERARCHY (SUMMARY)

When the analysis involves benchmarking the Company against an external reference
class — sustainability of margins, growth, capital intensity, or any other FCF
driver — apply the tiered evidence hierarchy: Tier 1 (public comps), Tier 2
(user-provided base rates), Tier 3 (comp data embedded in source materials), and
default to internal historical benchmarking only when none of those tiers apply.
Never fabricate industry-level base rate statistics. Never name academic or
practitioner authors in memo output.

For the full hierarchy, default-mode rules, and output framing constraints, see
[`reference/base-rate-framework.md`](reference/base-rate-framework.md).

## SECTION MAP — OUTPUT ORDER

Produce all sections below unless the user specifies otherwise. Sections marked
⚙️ require quantitative inputs; produce placeholders in [X] format if unavailable.

| # | Section | Template Location |
|---|---|---|
| 1 | Deal Header Fields | Top metadata table |
| 2 | Situation Overview | Shaded paragraph below header |
| 3 | Company Overview | Left column, first content table |
| 4 | Financial Headline | "LTM Revenue // CA EBITDA" row |
| 5 | Discussion & Analysis | Right column, financial table ⚙️ |
| 6 | Sources & Uses Note | Note below S&U chart ⚙️ |
| 7 | Risk Flags | Y/N/TBD grid table |
| 8 | Preliminary Strengths | Left column, bottom table |
| 9 | Preliminary Considerations & Focus Areas | Right column, bottom table |
| 10 | Posting Team Recommendation | Shaded recommendation box |
| 11 | Overland Designated Criteria | Criteria checkbox table ⚙️ |
| 12 | Posting Committee Final Rating | Final box (pre-IC: leave as TBD) |

## SECTION 1 — DEAL HEADER FIELDS

Populate each field from available materials. Use the exact labels from the template.

**Every field should contain only the populated value or `TBD` with a brief
parenthetical describing the missing data source** — e.g., `TBD (not disclosed
in CIP)`. Do not append investigative notes, caveats, process observations,
follow-up recommendations, or commentary to any header field. If a field's source
materials contain analytically relevant context (ownership dynamics, origination
observations, process notes), relocate that information to the Situation Overview
(Section 2) or another appropriate narrative section.

| Field | Source | Notes |
|---|---|---|
| Company Name | CIM / teaser | Include nickname in quotes: `Stark Tech ("Stark", or the "Company")` |
| Owner(s) | CIM | `Founder-Owned` / `Family-Owned` / `[Sponsor Name]` / `Management-Owned` |
| HQ // Year Founded | CIM | `City, State // YYYY` |
| Sector // Industry | CIM + judgment | Use GICS sector; match template style: `Industrials // Engineering & Construction` |
| Origination Source | Deal context | `Wells-Sourced (Existing Account)` / `Wells-Sourced (Prospective Account)` / `CBP Sourced` |
| Posting Team | Leave for user | `[J. Anderson / P. Lim / J. Barron / R. Gormley]` |
| Received // Posted Date | Deal context | `MM-DD-YY // MM-DD-YY` |
| Process Type // Stage | CIM / context | `Debt Advisor // Pre-Term Sheets` / `Proprietary // Pre-IOI` / etc. |
| Feedback Party | Deal context | `Wells Fargo & Debt Advisor` / `WF / Company` |
| Feedback Deadline | Deal context | `MM-DD-YY` |

**Cover page + running header fields (additional):** The script also populates
the cover page (page 1) and the per-page running header. Provide:
- `cover_company_name` — short name for cover page and running header (e.g.,
  `Stark Tech`); defaults to `company_name` minus any parenthetical if absent
- `cover_date` — long-form date for cover (e.g., `March 15, 2026`); defaults to
  `received_posted_date` if absent

The running header `[Company] ([Owner])` is constructed automatically as
`{cover_company_name} ({owners})`.

## SECTION 2 — SITUATION OVERVIEW

One tight paragraph (~75–125 words). Cover in order:

1. What the Company is doing / why they are in market (refi, acquisition, recap, growth capital)
2. Proposed facility structure: type, amount, leverage through (x TNL / x Net Secured / x Total)
3. Use of proceeds (specific: amounts, names, multiples if M&A-related)
4. Wells Fargo relationship context — **only if explicitly provided** in source materials (e.g., "existing WF banking client," "WF is the agent"). If not provided, omit entirely. Do not insert a TBD placeholder or follow-up recommendation for WF relationship status.

**Default assumption for competitive processes:** All debt-advisor-led and
sponsor-led financing processes should be assumed competitive unless the source
materials explicitly state otherwise or the user instructs otherwise. Do not flag
the competitive vs. proprietary distinction as an open question when a debt advisor
is running the process.

**Do not include** posting team process recommendations, investigative prompts
(e.g., "confirm WF origination context"), or next-step language. The Situation
Overview reports the transaction facts — it does not assign tasks.

Pattern:
> *[Company] is currently working with [Debt Advisor] to raise a [facility description],
> through ~[X]x [leverage metric]. Proceeds will be used to [use of proceeds].
> [WF relationship sentence — only if explicitly sourced.]*

## SECTION 3 — COMPANY OVERVIEW

**Opening paragraph** (~40–60 words): Cover the Company's identity, what it does,
who it serves, its geographic footprint, and key scale metrics (headcount, locations,
units, etc.). The opening paragraph should NOT include revenue mix breakdowns,
demand driver characterization, competitive positioning details, or operating metrics
beyond basic scale indicators.

**The last sentence of the opening paragraph must always follow this structure:**

> *For the LTM period ending M/YY[A/E], the Company [generated / expects to generate]
> revenue and [pro forma adjusted EBITDA] ("CA EBITDA") of $X.XMM and $X.XMM
> (X.X% margin), respectively.*

Use `[A]` suffix for actual periods and `[E]` for estimated/budgeted periods.
Use `generated` for actuals and `expects to generate` for forward periods.

If pro forma CA EBITDA differs materially from reported adjusted EBITDA, add:
> *Pro forma for [X acquisitions / adjustments], [Company] generated ~$[X]MM of
> LTM [M/YY] Financeable EBITDA ("CA EBITDA").*

**Bullet points** — populate each; use TBD where not disclosed:
- **TAM & Market Share:** Total addressable market size, implied market share, key sub-market CAGRs if cited. Also: market share data, competitive scale comparisons (e.g., "~4x the nearest competitor"), and units under management or contracts managed where contextually appropriate.
- **Products / Services:** Revenue mix by segment, product line, or demand driver type (% of revenue). Contractual vs. non-contractual revenue split and subscription characterization. Recurring / reoccurring / break-fix demand driver classification. Key product/service lines and notable metrics (buildings managed, sqft, units, etc.).
- **Customers:** Revenue from existing vs. new customers, customer type breakdown, contract count, order volume metrics, retention metrics, top customer concentration if disclosed.
- **Suppliers:** Key supplier dependencies, sole-source risks, raw material exposure.
- **Labor / Raw Materials:** Headcount (FTEs), subcontractor usage, staffing/retention dynamics, key input cost exposures.
- **Operations / Facilities:** Number and type of locations, owned vs. leased, any notable physical assets.

## SECTION 4 — FINANCIAL HEADLINE ROW

**Use "CA EBITDA" as the standard EBITDA label.** Do not use "Adjusted EBITDA" or
"Diligence Adjusted EBITDA" in this row.

**Anchor to the operative LTM period.** Feature the LTM period that the financing
is being sized against. If the source materials do not explicitly identify an anchor
period, default to the most recent completed actual LTM period. Do not display a
forward budget period as the primary headline unless the debt advisor or source
materials explicitly guide the financing to a forward EBITDA figure.

**Standard format (single EBITDA line):**

> **LTM M/YYA Revenue // CA EBITDA:** $X.XMM // $X.XMM (X.X% margin)

**Financeable EBITDA format (when warranted):** Add a Financeable EBITDA figure on
the same line when extenuating circumstances exist — e.g., the Company has an add-on
acquisition under LOI, there are pro forma synergies beyond the base CA EBITDA, or
the debt advisor is marketing to a forward EBITDA figure that differs from the LTM
anchor. Format:

> **LTM M/YYA Revenue // CA EBITDA // Financeable EBITDA:** $X.XMM // $X.XMM (X.X% margin) // $X.XMM

**Do not display a margin percentage for Financeable EBITDA** unless the Financeable
EBITDA corresponds to the same period as the revenue figure shown. A margin on a
blended or forward EBITDA figure against a trailing revenue number is misleading.

Do not include a second headline row for a forward budget period unless the user
requests it.

## SECTION 5 — DISCUSSION & ANALYSIS

Six bullet points matching the right column of the financial summary table.
See [`reference/memo-sections.md`](reference/memo-sections.md) → *Financial D&A Section* for per-bullet content standards.

**Format: Each sub-section must be a single paragraph of 3–5 sentences.** Lead with
the key metric, provide supporting decomposition, and close with the most important
trend or risk signal. Cut any sentence that does not directly convey a financial
fact, metric, or material trend.

**Strike all diligence follow-ups and recommended next steps.** Do not include
sentences containing language such as "A diligence priority is...,"
"Diligence should confirm...," "The question for diligence is...,"
"Requires validation...," or "[X] requires stress-testing...."

**Do not speculate or editorialize.** Report what the data shows. Do not include
sentences that hedge around plausibility or offer conditional assessments. Avoid
language such as "This is plausible given [X] but requires validation that...,"
"The question is whether this expansion is structural or transient," or "This
suggests management may be acknowledging underinvestment." If a metric is materially
above or below the Company's own historical range, flag the magnitude of the
deviation and the direction — that is the factual signal.

**EBITDA quality and normalization:** When drafting the CA EBITDA & Adjustments
bullet, apply the tiered base rate evidence hierarchy (see
[`reference/base-rate-framework.md`](reference/base-rate-framework.md)) to assess
whether current margin levels are sustainable. If Tier 1/2/3 evidence is available,
benchmark explicitly. If not, assess the Company's current EBITDA margin against
its own historical trajectory using the fullest available data in the source
materials. Flag material margin expansion or compression relative to the Company's
own prior periods. Apply heightened skepticism to addbacks — quantify adjustments
as a % of CA EBITDA and interrogate each material item.

Bullets in order:
- **M&A / Organic Results**
- **Revenue**
- **Gross Profit**
- **CA EBITDA & Adjustments**
- **Capex**
- **NWC**

## SECTION 6 — SOURCES & USES NOTE

One sentence note below the S&U chart. Standard format:
> *Figures reflect mgmt.'s proposal. USD 3mo Term SOFR curve as of [date].*

If no term sheet available:
> *Proposed terms per [Debt Advisor / Company] marketing materials. Figures
> are illustrative; final terms TBD.*

## SECTION 7 — RISK FLAGS TABLE

The script populates Y/N/TBD into the existing template grid. Provide a flag value
for each of the 15 items; default unspecified items to `TBD`.

**Items (in template column order):** Conc., Cyclicality, Seasonality, NWC Needs,
Capex Needs, Project Based, Excessive Revolver, Bonding / Surety, FX Exposures,
Raw Mat Volatility, Unique Accounting, Mgmt. Issues, Regulatory Risks, Technology
Risks. The 15th item — ESG — uses the `RR` / `SA` format (default to `n/a`).

**RR and SA ESG ratings default to `n/a`.** Unless the user explicitly provides RR
(Risk Rating) or SA (Structural Accommodation) ESG ratings, always populate these
fields as `n/a`. Do not mark them as TBD, do not ask the user to provide them, and
do not attempt to derive them from the source materials.

See [`reference/memo-sections.md`](reference/memo-sections.md) → *Risk Flags*
for definitions and assignment logic for all 15 items.

## SECTION 8 — PRELIMINARY STRENGTHS

Five numbered items in the format: **[Bold Header]:** [Supporting detail]

**Bold header text: concise, factual, no marketing language.** Headers should read
like a credit officer's shorthand — not a sell-side pitch book. Guidelines:
- Avoid superlatives and flowery modifiers (e.g., "Genuine," "Massive,"
  "Exceptional," "Robust"). State the attribute directly.
- Use past tense, not present perfect (e.g., "compounded" not "has compounded";
  "grew" not "has grown").
- Truncate conjunctions and prepositions where natural (e.g., "&" for "and",
  "w/" for "with"). Do not overdo this — readability still matters.
- Examples:
  - Bad: "Genuine Secular Tailwinds with Massive Whitespace"
  - Good: "Large TAM w/ Secular Demand Drivers"
  - Bad: "High-Quality Demand Profile with ~84% Contractually Recurring Revenue"
  - Good: "~84% Contractually Recurring Revenue w/ ~97%+ Retention"
  - Bad: "Market-Leading Scale in a Fragmented, Essential Services Industry"
  - Good: "#1 Market Position in Fragmented Industry"

**Order strengths from macro to micro:**
1. Industry-level attributes (TAM, secular tailwinds, acyclicality, fragmentation)
2. Competitive positioning (market share, scale advantages, barriers to entry)
3. Demand driver quality (recurring revenue, retention, contract structure)
4. Financial profile (margins, growth trajectory, FCF conversion, capital intensity)
5. Capital structure / deal-specific attributes (leverage, equity cushion, lender protections)

**Focus on credit considerations over deal structure.** Strengths should emphasize
the business and industry attributes that make this a sound credit — not the terms
of the proposed financing, unless the deal structure is unusually credit-favorable.
A conservative leverage point or strong equity cushion can be a strength, but it
should follow the business-quality strengths, not lead.

Each strength should be specific and evidence-anchored — not generic assertions.
Wrong: *Strong customer relationships*
Right: *~90% Revenue from Existing Customers w/ 17k+ Annual Service Orders:*
*[Supporting detail with specific metrics.]*

Use the Overland quality framework to identify what is genuinely credit-favorable:
- Demand driver quality (contractual recurring > reoccurring > break-fix)
- Competitive positioning within a fragmented industry
- Secular tailwinds that are genuinely structural (not cyclical)
- Track record of revenue/EBITDA growth with supporting data
- Limited capital intensity / strong FCF conversion
- Owner/management alignment and depth

## SECTION 9 — PRELIMINARY CONSIDERATIONS & FOCUS AREAS

Five numbered items in the same format as Strengths.

Frame each as a risk or open question supported by the factual record. The tone is
analytical, not adversarial. The consideration paragraph itself — by clearly framing
the risk and its supporting data — implicitly signals what needs to be investigated.
The reader does not need an explicit instruction.

**Strike all resolution and diligence directives.** Do not include sentences
beginning with or containing:
- "Resolve: ..."
- "Overland should assess..."
- "Diligence should [confirm / validate / stress-test]..."
- "The Posting Team should..."

**Focus on credit considerations; order structural and deal-specific items lower.**
Credit-quality risks (demand driver durability, earnings quality, concentration,
cyclicality, capital intensity, competitive dynamics) should come before structural
or deal-specific risks (leverage, floating rate exposure, sponsor recap mechanics).

**Ignore equity-type considerations.** Frame through the lens of a senior secured
lender, not an equity investor. Revenue growth acceleration assumptions are primarily
an equity concern. If a revenue growth thesis is relevant, reframe around what
happens to coverage and cash flow if that growth does not materialize.

Use the Overland FCF decomposition framework as the lens: price/volume/mix dynamics,
operating leverage and downside EBITDA behavior, GAAP-to-cash earnings quality,
capital intensity, and NWC behavior. "Will revenues hit management's 2026 target?"
is an equity question. "Historical TUMs have not recovered to prior peak; ~34% of
revenue is project-based and lumpy, which may not align with actual cash billings"
is a credit question.

**Anchor earnings quality / EBITDA adjustment risks around GAAP-to-cash and
adjustment magnitude on the anchor LTM period.** When flagging EBITDA adjustment
quality as a consideration:
- Weight the analysis toward the LTM anchor period (the period the financing is
  being sized against), not prior periods.
- Prior-period adjustments that were large but subsequently converted into actual
  run-rate earnings are a *positive* data point (adjustments validated by results),
  not a risk. Flag them as context, not as a concern.
- The risk signal is the magnitude and composition of adjustments *in the anchor
  period* — particularly non-cash items, management fees, one-time costs that may
  recur, and any adjustment that creates a gap between GAAP earnings and cash
  available for debt service.

**De-emphasize management / key-man risk for refinancings and sponsor-backed
transactions.** Management depth and key-man risk are most relevant for non-sponsored
credits where the founder/owner *is* the business. For sponsor-backed transactions —
particularly refinancings or recaps where key C-suite executives are not rolling
significant equity — management risk is a lower-priority consideration. It can still
appear if warranted by the facts (e.g., very thin bench, recent wholesale team
turnover), but it should not occupy a top-3 slot by default.

Apply Overland framework flags:
- Revenue quality / demand driver concerns (project-based, discretionary, cyclical)
- Margin profile vs. history — flag if below target range (12–20% EBITDA) or
  if above upper end (flag sustainability risk; apply tiered evidence hierarchy
  to assess whether above-range margins are structurally supported or likely to
  revert toward the Company's own historical baseline or available comp set)
- Concentration risk (customer, supplier, geography, product)
- Cyclicality and operating leverage in a downside scenario
- EBITDA addback quality — size and composition of adjustments on the anchor period
- Management depth, key-man risk, succession (priority based on ownership context)
- Competitive dynamics (bid-based, commodity pricing, large platform competitors)
- Capital structure concerns (leverage, floating rate exposure, amortization)

## SECTION 10 — POSTING TEAM RECOMMENDATION

**Format:**

> **[Color] ([Initials]):** Recommend a [Color] rating and [passing on the
> opportunity / continuing diligence]. [2–4 sentences citing the key strengths
> and material considerations that drive the rating.]

**Report only facts, strengths, and considerations driving the rating.** The
recommendation rationale should reference the 2–3 strongest credit attributes
supporting the rating and the 1–2 most material open items or risks. Keep language
factual and past-tense. Do not editorialize about the Company's potential or future
trajectory.

**Do not include:**
- A separate "Note:" paragraph with additional commentary
- Language directing the team toward specific diligence priorities
- Qualifications like "the diligence focus should be on..."
- Threshold questions or strategy-level observations
- Supplementary notes or next-step guidance

**Color ratings** (infer from overall credit quality assessment):
- **Green:** High conviction, strong credit quality — recommend aggressive pursuit
- **Yellow:** Good credit, some open items — recommend begin diligence
- **Orange:** Mixed picture, material open questions — recommend high diligence bar / cautious pursuit
- **Red:** Significant structural concerns — recommend pass or alternative structure only

The script also marks the matching Posting Team rating row in the criteria table:
- `posting_rating`: one of `"Very Interesting"`, `"Begin Diligence"`,
  `"High Diligence Bar"`, `"No Diligence Path"`, `"Alternative Strategy"`
  (color synonyms `Green`/`Yellow`/`Orange`/`Red` also accepted). Map color → rating
  using the standard convention above (Green → Very Interesting; Yellow → Begin
  Diligence; Orange → High Diligence Bar; Red → No Diligence Path).

## SECTION 11 — OVERLAND DESIGNATED CRITERIA

Populate Y/N/TBD for each item based on deal terms and size. The script writes
each flag to the correct cell in the criteria table.

**Criteria items:**
- `ebitda` — Y if CA EBITDA ≥ $[Overland minimum — confirm with team]
- `leverage` — Y if proposed leverage is within Overland parameters
- `secured` — Y if first lien / senior secured
- `deal_size` — Y if facility size within Overland deployment range
- `yield` — Y if all-in yield meets Overland return threshold
- `us_domiciled` — Y/N based on borrower domicile
- `other_considerations` — short note on any non-standard factors (prospective
  WF account, unique structure, etc.); use `"n/a"` if none

The Overland IC column is left blank for the IC to fill in later.

## SECTION 12 — POSTING COMMITTEE FINAL RATING & NEXT STEPS

Pre-IC version: Leave the template default in place (do not pass `final_rating`
in the content dict, or pass `null`):
> *[--Prior to Posting IC Meeting in "vS" version of the memo--]*
> *[Pending Overland IC Feedback]*

Post-IC version: Pass populated text in `final_rating` per standard template
language.

## STEP 13 — POPULATE THE TEMPLATE

After drafting all sections, build the content dict and populate the template per [`reference/population-mechanics.md`](reference/population-mechanics.md) — content-dict schema pointer, run snippet, `"Header: detail"` bullet conventions and exact prefix labels, and the out-of-scope list. Follow that file exactly.

## Anti-patterns

These collect the prohibitions already enforced section-by-section above for at-a-glance visibility. No new behavior.

- **No posting team follow-ups, anywhere.** The memo reports facts; it never assigns tasks, recommends calls, or prescribes diligence steps in any section. No "A diligence priority is...," "Diligence should confirm...," "Requires validation...," "Resolve: ...," "Overland should assess...," "The Posting Team should....".
- **No speculation or conditional hedging.** Report what the data shows; do not speculate about causes/sustainability absent explicit source evidence. Flag the magnitude and direction of any deviation from the Company's own history — that is the signal, not the cause.
- **"CA EBITDA" is the only EBITDA label.** Never "Adjusted EBITDA" or "Diligence Adjusted EBITDA" anywhere in the output.
- **Never fabricate.** No invented figures, customer names, or deal terms; use `TBD` with a parenthetical naming the missing source — e.g., `TBD (not disclosed in CIP)`.
- **No fabricated base rates.** Never generate/imply industry-level base-rate statistics absent Tier 1/2/3 evidence; never name an academic or practitioner author in output.
- **No equity-investor framing in Considerations.** Frame through a senior secured lender's lens; reframe revenue-growth-acceleration questions around coverage and cash flow if growth does not materialize.
- **ESG RR/SA default to `n/a`** — never TBD, never derived from source, never solicited unless the user explicitly provides them.
- **Do not regenerate the Word document.** The deliverable is the bundled template edited in-place by `scripts/populate_memo.py`; rebuilding it strips Word auto-numbering and run-level formatting.

## Notes on portability into Arrakis

This skill is the Stage 2 / P4 Posting Memo narrative half of the deal lifecycle, mapping into the Arrakis Foldspace screening application as the posting-memo narrative generator. The section map and Overland analytical discipline carry through unchanged; `scripts/populate_memo.py` produces the in-place populated `.docx`; `schemas/posting_memo_content.py` `PostingMemoContent` is the Arrakis-side structured-output contract for the drafted content the script consumes. At graduation the underlying prompt is invoked through Spice and the structured content lands in the screening application's `_LAND` tier; no rewrite of the skill body is required.

**Watermark obligation (D-2 carve-out).** The P4 posting memo is IC-facing and carries the HITL watermark obligation: at output it sits in HITL state `PENDING_REVIEW` with `requires_human_review = true`. The `[DRAFT — HUMAN REVIEW REQUIRED]` banner is **not** injected into the Word body — that would alter and corrupt the production template. The draft signal is carried by the existing, unchanged mechanisms: the `vS` draft filename suffix, the Section 12 "[Pending Overland IC Feedback]" default left in place pre-IC, and the `PENDING_REVIEW` HITL state recorded around the artifact. The watermark becomes a rendered review banner at the Arrakis HITL layer, outside the .docx, on graduation.
