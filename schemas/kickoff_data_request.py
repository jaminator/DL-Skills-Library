"""KickoffDataRequest - Pydantic schema for the P3 kick-off data request.

Schema version:       1
Lifecycle phase:      P3 Kick-Off Data Requests (Stage 2 Screening)
Arrakis target app:   Foldspace screening application (kick-off data-request
                      generator; same app as the P4 posting-memo pair)
Arrakis landing tier: ARRAKIS_RAW.SCREENING_LAND.kickoff_data_request
HITL state at output: PENDING_REVIEW (see wiki/llm-integration/hitl-state-machine.md)

This schema is the structured-output contract the dl-ddq-kickoff skill emits.
It is a superset of what `scripts/populate_kickoff.py` consumes: the script
reads a flat projection of these fields (the CONTENT JSON SCHEMA in that
script's docstring), while this schema additionally captures the reasoning
provenance Arrakis lands for lineage and the Foldspace Observatory (the
sector classification that drove the borrower-specific block, and the
per-KPI rationale and downstream target).

PROJECTION TO THE populate_kickoff.py CONTENT DICT (no drift)
------------------------------------------------------------
Every key the script consumes appears here with the same name and type:

    company_name               -> content["company_name"]            (str)
    owner                      -> content["owner"]                   (str|None)
    as_of_date                 -> content["as_of_date"]              (str|None)
    periods                    -> content["periods"]                 (object)
    compliance_cert_applicable -> content["compliance_cert_applicable"] (bool)
    stock_cut_requests         -> content["stock_cut_requests"]      (list[str])
    borrower_kpi_requests      -> content["borrower_kpi_requests"]   via
                                  [k.label for k in borrower_kpi_requests]

`fiscal_year_end`, `naics_code`, the four `gics_*` fields, and the
`rationale` / `downstream_target` on each KpiRequest are reasoning provenance:
the skill produces them while deriving the request, the script does not read
them, and Arrakis lands them alongside the artifact. They are not aspirational
- the emitter genuinely produces them at draft time.

Per the D-2 carve-out the [DRAFT - HUMAN REVIEW REQUIRED] watermark is NOT
written into the outbound Word body; the draft signal is the `vS` filename
suffix plus `review_state` / `requires_human_review` here.

Field naming uses snake_case (Snowflake convention). Types are
JSON-serializable Python primitives. When lifted into Arrakis this module is
registered in the prompt library as the structured-output validator for the
kick-off data-request prompt and as the SCREENING_LAND data-product schema.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class KickoffPeriods(BaseModel):
    """The deterministic period fragments from scripts/compute_periods.py.

    Passed through verbatim as content["periods"]; the script substitutes
    these into the template's bracket placeholders. Mirrors the
    compute_periods.py JSON output field-for-field.
    """

    audited_range: str = Field(
        ..., description="Audited look-back, e.g. \"FY'23-'25\" (or \"FY'25\")."
    )
    ltm_anchor: str = Field(
        ..., description="LTM anchor as M/YY, e.g. \"3/26\"."
    )
    quarter_label: str = Field(
        ..., description="Fiscal quarter of the LTM anchor, e.g. \"Q1'26\"."
    )
    quarterly_range: str = Field(
        ...,
        description="Quarterly internal/compliance range, e.g. \"FY'24 - Q1'26\".",
    )
    budget_fy: str = Field(
        ..., description="Current in-progress FY, e.g. \"FY'26\"."
    )
    forecast_range: str = Field(
        ..., description="Long-range forecast range, e.g. \"FY'26-'30\"."
    )
    last_completed_fy_end: str = Field(
        ..., description="ISO date of the last completed FYE (lineage)."
    )
    ltm_anchor_date: str = Field(
        ..., description="ISO date of the LTM-anchor fiscal quarter end (lineage)."
    )


class KpiRequest(BaseModel):
    """One borrower-specific KPI request line plus its reasoning provenance.

    The script consumes only `label`; `rationale` and `downstream_target` are
    landed by Arrakis for lineage and Observatory quality metrics.
    """

    label: str = Field(
        ...,
        description=(
            "The request line as written into the document - a terse "
            "off-the-shelf noun phrase."
        ),
    )
    rationale: str = Field(
        ...,
        description=(
            "The Overland credit-framework dimension this request tests "
            "(demand-driver quality / growth quality / operating leverage / "
            "concentration / etc.)."
        ),
    )
    downstream_target: str = Field(
        ...,
        description=(
            "The downstream artifact/field this pre-seeds (e.g. 'databook "
            "fin_inputs', 'posting-memo Company Overview')."
        ),
    )


class KickoffDataRequest(BaseModel):
    """Top-level structured output of the P3 kick-off data-request skill.

    Produced by the dl-ddq-kickoff skill. Always emitted in HITL state
    PENDING_REVIEW; the draft signal is the `vS` filename suffix (the outbound
    Word body carries no watermark - D-2 carve-out). The script-consumed
    projection is documented in the module docstring.
    """

    schema_version: int = Field(
        1,
        description=(
            "Monotonic schema version. Increment on any field addition, "
            "removal, or type change. Carries through into the Arrakis Avro "
            "envelope as schema_version."
        ),
    )

    company_name: str = Field(
        ..., description="Borrower legal/common name (header placeholder)."
    )
    owner: str | None = Field(
        None,
        description=(
            "The header '(Sponsor)' parenthetical (sponsor name / "
            "'Founder-Owned' / etc.); None removes the parenthetical."
        ),
    )
    as_of_date: str | None = Field(
        None,
        description=(
            "Long-form preparation date, e.g. 'May 28, 2026'; refreshes the "
            "header DATE field's cached value. None leaves the auto-field."
        ),
    )
    fiscal_year_end: str = Field(
        "12-31",
        description=(
            "Borrower fiscal-year-end as 'MM-DD' (default '12-31'); the "
            "compute_periods.py input that drove the period fragments."
        ),
    )

    periods: KickoffPeriods = Field(
        ..., description="The verbatim compute_periods.py period fragments."
    )

    naics_code: str = Field(
        ...,
        description=(
            "NAICS code from the sector classification handoff; drove the "
            "borrower-specific block. '[INSUFFICIENT DATA - sector "
            "classification not provided]' if absent."
        ),
    )
    gics_sector: str = Field(
        ..., description="GICS sector from the classification handoff."
    )
    gics_industry_group: str = Field(
        ..., description="GICS industry group from the classification handoff."
    )
    gics_industry: str = Field(
        ..., description="GICS industry from the classification handoff."
    )
    gics_sub_industry: str = Field(
        ..., description="GICS sub-industry from the classification handoff."
    )

    compliance_cert_applicable: bool = Field(
        ...,
        description=(
            "True only if the borrower has an existing facility reporting "
            "regularly; False suffixes the compliance-cert line N/A (the "
            "line is never deleted)."
        ),
    )
    stock_cut_requests: list[str] = Field(
        ...,
        description=(
            "The every-borrower standard analytical cuts (concentration, "
            "capex split, NWC, post-close debt-like items, and the add-on "
            "cohort/consideration lines when buy-and-build)."
        ),
    )
    borrower_kpi_requests: list[KpiRequest] = Field(
        ...,
        description=(
            "Sector-specific KPI request lines with reasoning provenance; "
            "the script consumes [k.label for k in borrower_kpi_requests], "
            "capped at the one-page ceiling."
        ),
    )

    requires_human_review: bool = Field(
        True,
        description=(
            "Always True at output time. Set False only after the deal team "
            "approves the list before it is sent (downstream / Arrakis "
            "screening review UI)."
        ),
    )
    review_state: Literal["PENDING_REVIEW"] = Field(
        "PENDING_REVIEW",
        description=(
            "HITL state at output time. The outbound .docx carries no "
            "watermark (D-2 carve-out); the draft signal is the 'vS' "
            "filename. Transitions are reviewer-driven and recorded in the "
            "override audit record."
        ),
    )
