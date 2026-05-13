"""ComplianceCertificateValidation — Pydantic schema for the P17 pilot.

Schema version:       1
Lifecycle phase:      P17 Portfolio Monitoring (Stage 6 Asset Management)
Arrakis target app:   A12 Corrino
Arrakis landing tier: ARRAKIS_RAW.CORRINO_LAND.compliance_certificate_validations
HITL state at output: PENDING_REVIEW (see wiki/llm-integration/hitl-state-machine.md)

Field naming uses snake_case (Snowflake convention). Types are JSON-serializable
Python primitives. Required-vs-optional is explicit. The schema describes only
the fields the pilot prompt actually produces; nothing aspirational.

When this schema is lifted into Arrakis, it is registered in the prompt library
as the structured-output validator for the `compliance_certificate_parser_v1`
prompt and as the data-product schema for the `CORRINO_LAND` landing table.
The DCA contract for the data product references this module by import path.
"""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class CovenantCalculation(BaseModel):
    """One row of a compliance certificate's covenant table.

    The reviewer reads one of these per covenant tested. The pilot prompt
    produces a list of these inside the parent ComplianceCertificateValidation.
    """

    covenant_name: str = Field(
        ...,
        description=(
            "Canonical covenant name as named on the certificate "
            "(e.g. 'Total Net Leverage Ratio', 'Fixed Charge Coverage Ratio')."
        ),
    )
    covenant_definition_source: str = Field(
        ...,
        description=(
            "Citation of the credit agreement section defining this covenant "
            "(e.g. 'Section 7.10(a)'). Use "
            "'[INSUFFICIENT DATA — covenant_definition_not_located]' if the "
            "agreement excerpts in context do not contain the definition."
        ),
    )
    reported_value: float | None = Field(
        None,
        description=(
            "Value reported by the borrower's CFO on the certificate. None "
            "when the field is absent or illegible."
        ),
    )
    recomputed_value: float | None = Field(
        None,
        description=(
            "Value recomputed from underlying inputs cited on the certificate "
            "applying the credit agreement's specific definitional choices. "
            "None when inputs are missing."
        ),
    )
    threshold: float = Field(
        ...,
        description=(
            "The covenant threshold as written in the credit agreement at the "
            "applicable step (covenants typically step down over the loan life)."
        ),
    )
    threshold_direction: Literal["max", "min"] = Field(
        ...,
        description=(
            "'max' for ceilings (e.g. leverage <= 5.5x); "
            "'min' for floors (e.g. coverage >= 1.10x)."
        ),
    )
    in_compliance: bool | None = Field(
        None,
        description=(
            "Whether the recomputed value satisfies the threshold under "
            "threshold_direction. None when recomputation impossible."
        ),
    )
    headroom_amount: float | None = Field(
        None,
        description=(
            "Absolute distance from threshold (positive = headroom, "
            "negative = breach). None when recomputation impossible."
        ),
    )
    headroom_percent: float | None = Field(
        None,
        description=(
            "Percentage distance from threshold relative to the threshold value. "
            "None when recomputation impossible."
        ),
    )
    arithmetic_error_flag: bool = Field(
        False,
        description=(
            "True when reported and recomputed values differ materially "
            "(default heuristic: > 0.5% of threshold value, or any compliance "
            "sign change)."
        ),
    )
    definition_misapplication_flag: bool = Field(
        False,
        description=(
            "True when the borrower applied the covenant definition incorrectly "
            "(wrong addbacks, wrong cash netting cap, wrong tranche scope, "
            "wrong test period)."
        ),
    )
    reviewer_notes: str | None = Field(
        None,
        description=(
            "Concise free-text observation for the reviewer. Required when any "
            "flag is True or in_compliance is None. Cite which inputs and which "
            "agreement section produced the observation."
        ),
    )


class ComplianceCertificateValidation(BaseModel):
    """Top-level structured output of the P17 compliance certificate parser.

    Produced by the parsing-compliance-certificates skill via the
    compliance_certificate_parser prompt. Always emitted in HITL state
    PENDING_REVIEW with the [DRAFT — HUMAN REVIEW REQUIRED] watermark
    rendered immediately above the JSON in the calling skill's response.
    """

    schema_version: int = Field(
        1,
        description=(
            "Monotonic schema version. Increment on any field addition, "
            "removal, or type change. Carries through into the Arrakis "
            "Avro envelope as schema_version."
        ),
    )
    facility_id: str = Field(
        ...,
        description=(
            "Foldspace MDM facility_id (UUID) when known. When unknown in "
            "the Claude Desktop pilot, populate with the facility name and "
            "include 'facility_id' in insufficient_data_fields."
        ),
    )
    period_end_date: date = Field(
        ...,
        description="Period the certificate covers (e.g. quarter-end ISO date).",
    )
    certificate_received_date: date = Field(
        ...,
        description="Date the borrower delivered the certificate.",
    )
    cfo_signatory: str | None = Field(
        None,
        description=(
            "Name of the CFO or finance officer who signed the certificate. "
            "None when the signatory is illegible or absent."
        ),
    )
    covenants: list[CovenantCalculation] = Field(
        ...,
        description=(
            "One entry per covenant tested by the certificate, including "
            "synthetic entries for required covenants that the certificate "
            "omitted (which are flagged via definition_misapplication_flag)."
        ),
    )
    overall_status: Literal["compliant", "non_compliant", "review_required"] = Field(
        ...,
        description=(
            "'compliant' when every covenant in compliance, no flags set, no "
            "INSUFFICIENT DATA markers. 'non_compliant' when any covenant "
            "fails its threshold under recomputed value. 'review_required' "
            "when any flag set or any field missing data."
        ),
    )
    summary_flags: list[str] = Field(
        default_factory=list,
        description=(
            "Human-readable one-line summary of each significant issue, for "
            "the reviewer's at-a-glance read."
        ),
    )
    insufficient_data_fields: list[str] = Field(
        default_factory=list,
        description=(
            "Field paths where '[INSUFFICIENT DATA — <what>]' was emitted in "
            "place of a value (e.g. 'covenants[2].recomputed_value')."
        ),
    )
    requires_human_review: bool = Field(
        True,
        description=(
            "Always True at output time. Set False only after reviewer "
            "approval downstream (in Arrakis: Corrino's review UI)."
        ),
    )
    review_state: Literal["PENDING_REVIEW"] = Field(
        "PENDING_REVIEW",
        description=(
            "HITL state machine state at output time. The pilot output is "
            "always PENDING_REVIEW; subsequent state transitions are "
            "reviewer-driven and recorded in the override audit record."
        ),
    )
