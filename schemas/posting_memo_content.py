"""PostingMemoContent — Pydantic schema for the P4 posting-memo content dict.

Schema version:       1
Lifecycle phase:      P4 Posting Memo (Stage 2 Screening) — narrative half
Arrakis target app:   Foldspace screening application (posting-memo generator)
Arrakis landing tier: ARRAKIS_RAW.SCREENING_LAND.posting_memo_content
HITL state at output: PENDING_REVIEW (see wiki/llm-integration/hitl-state-machine.md)

This schema mirrors, field-for-field, the CONTENT JSON SCHEMA documented in the
docstring of `skills/dl-memo-posting/scripts/populate_memo.py`. It is the
structured-output contract for the content dict the skill drafts and the script
consumes to populate the bundled Word template in-place. It does not describe
the populated `.docx` itself (that artifact is produced unchanged by the
script); it describes the JSON the skill emits before invoking the script.

Field naming uses snake_case (Snowflake convention). Types are JSON-serializable
Python primitives. All content fields are optional exactly as the script
documents them ("All fields optional; omitted fields leave the template
placeholder in place"); the schema does not add required content fields the
emitter does not require, and does not invent fields the emitter does not read.

Per the D-2 carve-out, the `[DRAFT — HUMAN REVIEW REQUIRED]` watermark is NOT
written into the Word body. The HITL obligation is carried by `review_state`
and `requires_human_review` here plus the existing draft signals (the `vS`
draft filename suffix and the Section 12 "[Pending Overland IC Feedback]"
template default left in place pre-IC).

When this schema is lifted into Arrakis, it is registered in the prompt library
as the structured-output validator for the posting-memo prompt and as the
data-product schema for the SCREENING_LAND landing table.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class PostingMemoHeader(BaseModel):
    """Section 1 deal-header fields plus cover-page / running-header fields.

    Maps to the `header` object in the populate_memo.py content dict. Each
    field is the populated value or a `TBD (<missing source>)` string.
    """

    company_name: str | None = Field(
        None, description="Company name; include the nickname in quotes."
    )
    owners: str | None = Field(
        None, description="Owner(s): Founder-Owned / Family-Owned / sponsor / Management-Owned."
    )
    hq_year: str | None = Field(
        None, description="HQ city, state and year founded, formatted 'City, State // YYYY'."
    )
    sector_industry: str | None = Field(
        None, description="GICS sector // industry, matching template style."
    )
    origination_source: str | None = Field(
        None, description="Origination source (Wells-Sourced / CBP Sourced variants)."
    )
    posting_team: str | None = Field(
        None, description="Posting team members; left for the user to fill."
    )
    received_posted_date: str | None = Field(
        None, description="Received // posted date, formatted 'MM-DD-YY // MM-DD-YY'."
    )
    process_stage: str | None = Field(
        None, description="Process type // stage (e.g. 'Debt Advisor // Pre-Term Sheets')."
    )
    feedback_party: str | None = Field(
        None, description="Feedback party (e.g. 'Wells Fargo & Debt Advisor')."
    )
    feedback_deadline: str | None = Field(
        None, description="Feedback deadline, formatted 'MM-DD-YY'."
    )
    cover_company_name: str | None = Field(
        None,
        description=(
            "Short name for cover page + running header; defaults to "
            "company_name minus any parenthetical when absent."
        ),
    )
    cover_date: str | None = Field(
        None,
        description=(
            "Cover-page date, e.g. 'March 15, 2026'; defaults to "
            "received_posted_date when absent."
        ),
    )


class CompanyOverview(BaseModel):
    """Section 3 company overview: an opening paragraph plus the bullet list.

    Maps to the `company_overview` object: {opening, bullets}. Each bullet is a
    'Header: detail' string the script splits at the first ': '.
    """

    opening: str | None = Field(
        None, description="Opening paragraph (~40-60 words) with the required LTM closing sentence."
    )
    bullets: list[str] | None = Field(
        None,
        description=(
            "Company-overview bullets as 'Header: detail' strings (TAM & Market "
            "Share, Products / Services, Customers, Suppliers, Labor / Raw "
            "Materials, Operations / Facilities)."
        ),
    )


class RiskFlags(BaseModel):
    """Section 7 Y/N/TBD risk-flag grid plus the ESG RR/SA pair.

    Maps to the `risk_flags` object. Each of the 14 named flags is 'Y' | 'N' |
    'TBD' (omitted flags default to TBD in the script). esg_rr / esg_sa default
    to 'n/a'.
    """

    conc: Literal["Y", "N", "TBD"] | None = Field(None, description="Concentration risk flag.")
    cyclicality: Literal["Y", "N", "TBD"] | None = Field(None, description="Cyclicality risk flag.")
    seasonality: Literal["Y", "N", "TBD"] | None = Field(None, description="Seasonality risk flag.")
    nwc_needs: Literal["Y", "N", "TBD"] | None = Field(None, description="NWC-needs risk flag.")
    capex_needs: Literal["Y", "N", "TBD"] | None = Field(None, description="Capex-needs risk flag.")
    project_based: Literal["Y", "N", "TBD"] | None = Field(None, description="Project-based revenue risk flag.")
    excessive_revolver: Literal["Y", "N", "TBD"] | None = Field(None, description="Excessive-revolver risk flag.")
    bonding_surety: Literal["Y", "N", "TBD"] | None = Field(None, description="Bonding / surety risk flag.")
    fx_exposures: Literal["Y", "N", "TBD"] | None = Field(None, description="FX-exposure risk flag.")
    raw_mat_volatility: Literal["Y", "N", "TBD"] | None = Field(None, description="Raw-material-volatility risk flag.")
    unique_accounting: Literal["Y", "N", "TBD"] | None = Field(None, description="Unique-accounting risk flag.")
    mgmt_issues: Literal["Y", "N", "TBD"] | None = Field(None, description="Management-issues risk flag.")
    regulatory_risks: Literal["Y", "N", "TBD"] | None = Field(None, description="Regulatory-risk flag.")
    technology_risks: Literal["Y", "N", "TBD"] | None = Field(None, description="Technology-risk flag.")
    esg_rr: str | None = Field(None, description="ESG Risk Rating; defaults to 'n/a'.")
    esg_sa: str | None = Field(None, description="ESG Structural Accommodation; defaults to 'n/a'.")


class DesignatedCriteria(BaseModel):
    """Section 11 Overland designated-criteria Y/N/TBD grid plus the note.

    Maps to the `designated_criteria` object. The Overland IC column is left
    blank for the IC and is not part of this contract.
    """

    ebitda: Literal["Y", "N", "TBD"] | None = Field(None, description="CA EBITDA meets the Overland minimum.")
    leverage: Literal["Y", "N", "TBD"] | None = Field(None, description="Proposed leverage within Overland parameters.")
    secured: Literal["Y", "N", "TBD"] | None = Field(None, description="First lien / senior secured.")
    deal_size: Literal["Y", "N", "TBD"] | None = Field(None, description="Facility size within Overland deployment range.")
    yield_: Literal["Y", "N", "TBD"] | None = Field(
        None,
        alias="yield",
        description="All-in yield meets the Overland return threshold ('yield' in the content dict).",
    )
    us_domiciled: Literal["Y", "N", "TBD"] | None = Field(None, description="Borrower is US-domiciled.")
    other_considerations: str | None = Field(
        None, description="Short note on non-standard factors; 'n/a' if none."
    )


class PostingMemoContent(BaseModel):
    """Top-level content dict the dl-memo-posting skill emits for the script.

    Mirrors the populate_memo.py CONTENT JSON SCHEMA field-for-field. All
    content fields are optional (omitted fields leave the template placeholder
    in place, exactly as the script documents). The HITL fields below are not
    consumed by the script; they carry the PENDING_REVIEW obligation for the
    Arrakis-side contract per the D-2 carve-out (no watermark in the .docx).
    """

    model_config = {"populate_by_name": True}

    header: PostingMemoHeader | None = Field(
        None, description="Section 1 deal-header + cover/running-header fields."
    )
    situation_overview: str | None = Field(
        None, description="Section 2 single-paragraph situation overview (~75-125 words)."
    )
    company_overview: CompanyOverview | None = Field(
        None, description="Section 3 company overview: opening paragraph + bullets."
    )
    financial_headline: str | None = Field(
        None, description="Section 4 LTM revenue // CA EBITDA headline row string."
    )
    discussion_analysis: list[str] | None = Field(
        None,
        description=(
            "Section 5 six D&A bullets as 'Header: detail' strings (M&A / Organic "
            "Results, Revenue, Gross Profit, CA EBITDA & Adjustments, Capex, NWC)."
        ),
    )
    su_note: str | None = Field(
        None, description="Section 6 single-sentence Sources & Uses note (first 'Note: [X]')."
    )
    risk_flags: RiskFlags | None = Field(
        None, description="Section 7 Y/N/TBD risk-flag grid + ESG RR/SA pair."
    )
    strengths: list[str] | None = Field(
        None, description="Section 8 preliminary strengths as 'Header: detail' strings."
    )
    considerations: list[str] | None = Field(
        None, description="Section 9 preliminary considerations as 'Header: detail' strings."
    )
    recommendation: str | None = Field(
        None, description="Section 10 posting-team recommendation paragraph."
    )
    designated_criteria: DesignatedCriteria | None = Field(
        None, description="Section 11 Overland designated-criteria grid + note."
    )
    posting_rating: str | None = Field(
        None,
        description=(
            "Section 10/11 posting rating: 'Very Interesting' | 'Begin Diligence' "
            "| 'High Diligence Bar' | 'No Diligence Path' | 'Alternative Strategy' "
            "(Green/Yellow/Orange/Red synonyms accepted)."
        ),
    )
    final_rating: str | None = Field(
        None,
        description=(
            "Section 12 posting-committee final rating; null/omitted pre-IC "
            "leaves the '[Pending Overland IC Feedback]' template default."
        ),
    )

    schema_version: int = Field(
        1,
        description=(
            "Monotonic schema version. Increment on any field addition, removal, "
            "or type change. Carries through into the Arrakis Avro envelope."
        ),
    )
    requires_human_review: bool = Field(
        True,
        description=(
            "Always True at output time. Set False only after posting-IC review "
            "downstream (in Arrakis: the screening review UI)."
        ),
    )
    review_state: Literal["PENDING_REVIEW"] = Field(
        "PENDING_REVIEW",
        description=(
            "HITL state at output time. Per the D-2 carve-out the draft signal is "
            "the 'vS' filename + the Section 12 IC-feedback default, not a "
            "watermark injected into the .docx; state transitions are "
            "reviewer-driven and recorded in the override audit record."
        ),
    )
