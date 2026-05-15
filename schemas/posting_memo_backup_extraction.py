"""PostingMemoBackupExtraction — Pydantic schema for the P4 Posting Memo Backup.

Schema version:       1
Lifecycle phase:      P4 Posting Memo (Stage 2 Origination & Screening) — the
                      quantitative half of the P4 bundle, paired with the
                      narrative dl-memo-posting skill.
Arrakis target app:   the screening application that automates the P4
                      Posting Memo deliverable.
Arrakis landing tier: ARRAKIS_RAW.<screening_app>_LAND.posting_memo_backup_extractions
HITL state at output: PENDING_REVIEW (see wiki/llm-integration/hitl-state-machine.md)

This schema encodes the *extraction summary* that the dl-memo-posting-backup
skill already emits and asks the analyst to confirm before any cells are written
to the workbook. It is the structured mirror of that human-confirmed summary; it
does not describe the populated .xlsx (the workbook remains a script/skill
deliverable — D-2 nothing-to-inject).

Field naming uses snake_case (Snowflake convention). Types are JSON-serializable
Python primitives. Per-period values are typed `float | None` so that the
skill's load-bearing **blank != zero** rule is representable: a missing/
not-disclosed figure is None, never 0.0. Required-vs-optional is explicit. The
schema describes only what the skill's extraction summary actually contains;
nothing aspirational.

When this schema is lifted into Arrakis, it is registered in the prompt library
as the structured-output validator for the posting-memo-backup prompt and as the
data-product schema for the screening application's `_LAND` landing table. The
DCA contract for the data product references this module by import path.
"""

from typing import Literal

from pydantic import BaseModel, Field


class ColumnMapEntry(BaseModel):
    """One row of the confirmed column map (CIM period -> template column).

    Mirrors the column-map table the skill presents in Step 2 and echoes in the
    Step 6 output summary under "COLUMN MAP (as confirmed)".
    """

    cim_period: str = Field(
        ...,
        description="CIM period label as written (e.g. 'FY2024A', 'LTM 9/30/25', '(anchor, blank)').",
    )
    template_column: str = Field(
        ...,
        description="Template column letter the period maps to (e.g. 'G', 'K', 'L', 'M', 'R').",
    )
    row2_date: str | None = Field(
        None,
        description="ISO date written to / derived in row 2 for this column; None for the empty anchor when no date is shown.",
    )
    write_data: bool = Field(
        ...,
        description="Whether CIM data rows are written for this column (False for the G anchor column).",
    )
    note: str | None = Field(
        None,
        description="Free-text note for this period mapping (e.g. LTM-proxy flag, link-to-K note); None when no note.",
    )


class FinSumRow(BaseModel):
    """One FinSum data row in the extraction summary with per-period values.

    Covers the income-statement, capex, and NWC rows the skill extracts (rows
    11, 14, 18, 23, 27, 28, 46-49, 52-55). Every per-period value is
    `float | None`: None means not disclosed in the CIM (blank != zero).
    """

    row: int = Field(
        ...,
        description="Template FinSum row number (e.g. 11 Revenue, 23 CA EBITDA, 46 Accounts Receivable).",
    )
    metric: str = Field(
        ...,
        description="Metric label as presented in the extraction summary (e.g. 'Revenue', 'CA EBITDA', 'Maintenance Capex').",
    )
    type: Literal["as_reported", "adjusted"] = Field(
        ...,
        description="'adjusted' only for row 23 CA EBITDA; 'as_reported' for every other row (rows 11/14/18/27/28 and NWC).",
    )
    h: float | None = Field(None, description="Value for template column H; None if not disclosed (blank != zero).")
    i: float | None = Field(None, description="Value for template column I; None if not disclosed (blank != zero).")
    j: float | None = Field(None, description="Value for template column J; None if not disclosed (blank != zero).")
    k: float | None = Field(None, description="Value for template column K (last actual FYE); None if not disclosed.")
    l: float | None = Field(None, description="Value for template column L (LTM); None if not disclosed (blank != zero).")
    m: float | None = Field(None, description="Value for template column M (first projection); None if not disclosed.")
    r: float | None = Field(None, description="Value for template column R (prior-year LTM); None if not disclosed or linked to K.")
    relabel_note: str | None = Field(
        None,
        description="Set when C14 is relabeled (e.g. Gross Profit -> 'Contribution Margin'); None otherwise.",
    )


class SucapData(BaseModel):
    """The SUCAP-tab inputs in the extraction summary (sources, uses, pricing).

    Mirrors the "PROPOSED OVERLAND STRUCTURE" and SUCAP input cells the skill
    derives in Step 4 and writes in Step 5. Formula cells (U32, F14, S34, T34,
    K15) are intentionally absent — the skill never writes them.
    """

    rcf_funded_at_close: float | None = Field(
        None, description="F11 — RCF drawn at close ($000s) per the Overland RCF Funding Rule; None if not yet derived."
    )
    term_loan: float | None = Field(
        None, description="F12 — funded 1L Term Loan ($000s), CIM TL minus the funded RCF increment; None if not derived."
    )
    ddtl_funded_at_close: float | None = Field(
        None, description="F13 — DDTL funded at close ($000s), typically 0; None if not derived."
    )
    ddtl_commitment: float | None = Field(
        None, description="U34 — DDTL total unfunded commitment ($000s) per Proactive Sizing; None if not derived."
    )
    uses: dict[str, float] = Field(
        default_factory=dict,
        description="Use-of-proceeds label -> amount ($000s) for K11-K14 (e.g. {'Refi Existing Debt': 82000}).",
    )
    rcf_spread_bps: float | None = Field(None, description="S32 — RCF spread in bps (default 325); None if not set.")
    rcf_oid: float | None = Field(None, description="T32 — RCF OID (par = 100, default 99); None if not set.")
    tl_spread_bps: float | None = Field(None, description="S33 — TL spread in bps (default 575); None if not set.")
    tl_oid: float | None = Field(None, description="T33 — TL OID (default 98); None if not set.")
    sofr_rate: float | None = Field(None, description="S17 — SOFR rate as a decimal (e.g. 0.0435); None if not provided.")
    cash_at_close: float | None = Field(None, description="I30 — pro forma cash & equivalents at close ($000s); None if absent.")
    tev_multiple: float | None = Field(None, description="J41 — implied TEV / LTM CA EBITDA multiple; None if not disclosed.")
    cash_taxes: float | None = Field(
        None,
        description="P13 — annual run-rate cash taxes ($000s); None when left blank (never estimated or inferred).",
    )


class PostingMemoBackupExtraction(BaseModel):
    """Top-level structured output of the dl-memo-posting-backup extraction.

    Produced by the dl-memo-posting-backup skill via the P4 posting-memo-backup
    prompt. Always emitted in HITL state PENDING_REVIEW with the
    [DRAFT — HUMAN REVIEW REQUIRED] watermark rendered immediately above the
    extraction summary the analyst confirms before any workbook cells are
    written. The populated .xlsx is the skill/script deliverable; this object is
    the Arrakis-side structured contract for the same confirmed summary.
    """

    schema_version: int = Field(
        1,
        description=(
            "Monotonic schema version. Increment on any field addition, removal, "
            "or type change. Carries through into the Arrakis Avro envelope as "
            "schema_version."
        ),
    )
    company_name: str = Field(
        ...,
        description="Company name written to FinSum C1, as shown in the extraction summary header.",
    )
    column_map: list[ColumnMapEntry] = Field(
        ...,
        description="The confirmed CIM-period-to-template-column map (one entry per period, including the blank anchor).",
    )
    finsum_rows: list[FinSumRow] = Field(
        ...,
        description="One entry per extracted FinSum data row, each carrying its as_reported/adjusted type and per-column values.",
    )
    sucap: SucapData = Field(
        ...,
        description="The SUCAP-tab inputs: derived capital structure, uses, pricing, SOFR, cash, TEV multiple, cash taxes.",
    )
    intentional_formula_mods: list[str] = Field(
        default_factory=list,
        description="Human-readable list of intentional formula modifications applied (M2, column O CAGR cells, R-when-LTM=FYE, P12 override).",
    )
    analyst_flags: list[str] = Field(
        default_factory=list,
        description="One line per analyst follow-up flag (data-quality issues, L9 label note, owner-equity plug note, CIM ambiguities).",
    )
    requires_human_review: bool = Field(
        True,
        description="Always True at output time. Set False only after analyst confirmation downstream (in Arrakis: the screening review UI).",
    )
    review_state: Literal["PENDING_REVIEW"] = Field(
        "PENDING_REVIEW",
        description="HITL state machine state at output time; always PENDING_REVIEW. Subsequent transitions are reviewer-driven.",
    )
