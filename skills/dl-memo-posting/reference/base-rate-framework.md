# base-rate-framework.md — Base Rate Evidence Hierarchy

## Contents
- **Tier 1 — Public comps with available data** — direct comparables with observable financial metrics
- **Tier 2 — User-provided base rates** — explicit benchmark metrics provided by the user
- **Tier 3 — Source material reference data** — comp data embedded in CIM, QoE, or attached materials
- **Default — Internal historical benchmarking** — Company's own history when no external reference class exists
- **Prohibition on hallucinated base rates** — never generate industry-level statistics absent Tier 1/2/3 evidence
- **Output framing rules** — when "base rate" / "mean reversion" language is permitted in memo output

---

When analyzing the Company's financial profile across any FCF driver — including
industry structure, revenue decomposition (price, volume, mix), operating leverage
and cost structure, EBITDA quality and normalization, capital intensity (capex, NWC),
financial leverage, and downside/recovery — benchmark against an external reference
class **only** when that reference class is grounded in one of three evidence tiers,
evaluated in priority order:

**Tier 1 — Public comps with available data:** If the Company has a strong universe
of direct public comparables with observable financial metrics, benchmark the
Company's profile against those comps across each relevant FCF driver. Identify
whether the Company is performing above, at, or below the comp set and assess
sustainability accordingly.

**Tier 2 — User-provided base rates:** If the user explicitly provides base rate
metrics for any FCF driver (e.g., industry median EBITDA margin, typical revenue
growth range, standard capex-to-revenue ratios, normal NWC cycle dynamics), use
those as the primary external benchmark and evaluate the Company directly against
them.

**Tier 3 — Source material reference data:** If the CIM, management presentation,
QoE, or other project-attached materials contain public comparable company data,
precedent transaction metrics, or industry benchmarking data relevant to any FCF
driver, extract and use those metrics as the external reference class.

**Default — Internal historical benchmarking (no external reference class):**
If none of the three tiers above are satisfied, default entirely to internal
historical benchmarking across all FCF drivers. In this mode:

- Evaluate the Company's current LTM and forward metrics against the **fullest
  available history** in the source materials — not limited to any fixed lookback
  window. If CIM, QoE, or attached materials contain financial data spanning
  periods beyond 2-3 years (including recessionary periods such as the GFC or
  COVID), incorporate those results into the analysis. Depth of benchmarking
  should be commensurate with depth of available data.
- Flag **material step-changes** in any FCF driver — margins, revenue growth,
  cost structure, capital intensity, NWC behavior, leverage — relative to the
  Company's own prior-period performance and interrogate sustainability. Where
  longer-range financials are available, assess whether current performance
  represents a durable structural shift or a departure from a longer-term baseline.
- If any FCF driver has shifted materially vs. the Company's own history (e.g.,
  EBITDA margins doubled, NWC cycle compressed, capex intensity declined),
  explicitly question whether the current profile is structurally sustainable or
  likely to revert toward prior levels, and identify the operating or competitive
  dynamic that drove the change. Where historical data includes a recessionary
  period, assess how each FCF driver performed through that downturn and what it
  implies for downside resilience.
- **Do not fabricate or imply an external peer benchmark when one does not exist
  in the evidence base.** Frame analysis purely relative to the Company's own
  history across each FCF driver.

**Prohibition on hallucinated base rates:** Never generate or imply industry-level
base rate statistics for any FCF driver (e.g., "typical EBITDA margins for this
sector range from X% to Y%," "industry median revenue growth is Z%") unless those
figures are directly sourced from Tier 1, 2, or 3 evidence. If uncertain whether
a benchmark figure is broadly known public information vs. an assumption, treat it
as an assumption and either omit it or flag it explicitly as unverified.

**Output framing:** References to "base rate distribution," "mean reversion to
cohort," or similar language may appear in memo output **only** when grounded in
Tier 1, 2, or 3 evidence. When defaulting to internal historical benchmarking,
anchor analysis explicitly to the Company's own historical performance — do not
invoke external distribution framing. In no circumstance should generated memo
output reference any specific academic or practitioner author by name.
