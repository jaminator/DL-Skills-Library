"""SectorScreenHandoff — Pydantic schema for the P1 sector research screener.

Schema version:       1
Lifecycle phase:      P1 Deal Sourcing (Stage 1 Origination)
Arrakis target app:   Sourcing / origination application (deal-sourcing slice)
Arrakis landing tier: ARRAKIS_RAW sourcing landing tier (sector_screen_handoffs)
HITL state at output: PENDING_REVIEW (see wiki/llm-integration/hitl-state-machine.md)

This schema formalizes the already-frozen downstream `p2_borrower-identification`
markdown handoff contract emitted by the dl-sector-screen skill. The skill's
output is a single markdown file whose section headers, field names, and the
Pursue/Watch/Screened-Out verdict taxonomy are stable by design because an
unbuilt p2_borrower-identification skill is specified to parse them. This module
is the structured mirror of that markdown contract — field-for-field, with zero
drift from what the skill actually emits.

Field naming uses snake_case (Snowflake convention). Types are JSON-serializable
Python primitives. Required-vs-optional is explicit. The schema describes only
the fields the skill actually produces; nothing aspirational.

When this schema is lifted into Arrakis, it is registered in the prompt library
as the structured-output validator for the sector research screener prompt and
as the data-product schema for the sourcing landing table. The DCA contract for
the data product references this module by import path.
"""

from typing import Literal

from pydantic import BaseModel, Field


class CascadeAnchor(BaseModel):
    """One reference company used as an organizational anchor downstream.

    The skill names 3–5 of these per Pursue/Watch sub-vertical; the anchor
    names are used directly as query seeds by p2_borrower-identification.
    """

    company_name: str = Field(
        ...,
        description="Name of the currently-operating reference company.",
    )
    anchor_type: Literal["Public", "BSL", "PE-Platform"] = Field(
        ...,
        description="Anchor classification: 'Public', 'BSL', or 'PE-Platform'.",
    )
    descriptor: str = Field(
        ...,
        description="One-line descriptor naming the company's operating model.",
    )


class TradeOrg(BaseModel):
    """One trade association, membership directory, or industry conference.

    The skill lists these per Pursue/Watch sub-vertical; names are used as
    query seeds and exhibitor lists are flagged as high-yield downstream.
    """

    name: str = Field(
        ...,
        description="Trade association, membership directory, or conference name.",
    )
    url: str | None = Field(
        None,
        description="URL when known; None when not resolvable.",
    )
    descriptor: str = Field(
        ...,
        description="Brief descriptor of what the org or conference is.",
    )
    exhibitor_list: Literal["yes", "no", "unknown"] = Field(
        ...,
        description="Whether a public attendee/exhibitor list exists: yes|no|unknown.",
    )


class SubVertical(BaseModel):
    """One screened sub-vertical with its verdict and structured fields.

    Mirrors a single sub-vertical block under the Pursue, Watch, or
    Screened Out section of the frozen markdown handoff.
    """

    name: str = Field(
        ...,
        description="Sub-vertical name as written under its section header.",
    )
    verdict: Literal["pursue", "watch", "screened_out"] = Field(
        ...,
        description="Screen verdict: 'pursue', 'watch', or 'screened_out'.",
    )
    naics: list[str] = Field(
        ...,
        description="Candidate NAICS codes (4- or 6-digit), 1–3 entries.",
    )
    verdict_rationale: str = Field(
        ...,
        description=(
            "2–4 sentences mapping to screen categories by name; for a "
            "screened_out sub-vertical this is the one-sentence rejection "
            "rationale. Use '[unresolved: <reason>]' if not resolvable."
        ),
    )
    scope_caveat: str | None = Field(
        None,
        description=(
            "Geographic/regulatory concentration constraint; None when the "
            "sub-vertical has no caveat (field omitted in the markdown)."
        ),
    )
    thesis: str | None = Field(
        None,
        description=(
            "1–2 sentence prose thesis on the Tier 2 addressable opportunity. "
            "Present for pursue/watch; None for screened_out."
        ),
    )
    watch_flags: list[str] = Field(
        default_factory=list,
        description=(
            "Specific screen risks being monitored; populated only for the "
            "'watch' verdict, empty otherwise."
        ),
    )
    cascade_anchors: list[CascadeAnchor] = Field(
        default_factory=list,
        description=(
            "3–5 reference companies for pursue/watch; empty for screened_out."
        ),
    )
    trade_orgs: list[TradeOrg] = Field(
        default_factory=list,
        description=(
            "Trade orgs and conferences for pursue/watch; empty for "
            "screened_out."
        ),
    )


class SectorScreenHandoff(BaseModel):
    """Top-level structured output of the P1 sector research screener.

    Produced by the dl-sector-screen skill via the sector research screener
    prompt. Always emitted in HITL state PENDING_REVIEW with the
    [DRAFT — HUMAN REVIEW REQUIRED] watermark rendered immediately above the
    handoff in the calling skill's response. This is the structured mirror of
    the frozen `p2_borrower-identification` markdown handoff contract.
    """

    schema_version: int = Field(
        1,
        description=(
            "Monotonic schema version. Increment on any field addition, "
            "removal, or type change. Carries through into the Arrakis "
            "Avro envelope as schema_version."
        ),
    )
    sector_name: str = Field(
        ...,
        description="The screened sector name as titled in the handoff.",
    )
    input_scope: str = Field(
        ...,
        description="Original user input, verbatim.",
    )
    coverage_note: str = Field(
        ...,
        description="'full', or 'partial' with the reason coverage was capped.",
    )
    sub_verticals: list[SubVertical] = Field(
        ...,
        description=(
            "One entry per screened sub-vertical across the Pursue, Watch, "
            "and Screened Out sections; 4–10 typical (capped at 5 for broad "
            "inputs)."
        ),
    )
    open_questions: list[str] = Field(
        default_factory=list,
        description=(
            "Unresolved factual gaps, one per entry; from the handoff's "
            "## Open Questions section."
        ),
    )
    requires_human_review: bool = Field(
        True,
        description=(
            "Always True at output time. Set False only after the sourcing "
            "analyst approves the handoff downstream."
        ),
    )
    review_state: Literal["PENDING_REVIEW"] = Field(
        "PENDING_REVIEW",
        description=(
            "HITL state machine state at output time. The handoff is always "
            "PENDING_REVIEW; subsequent transitions are reviewer-driven and "
            "recorded in the override audit record."
        ),
    )
