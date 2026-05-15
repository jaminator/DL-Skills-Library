"""GeneratedPromptSpec — Pydantic schema for the dl-prompt-generate bundle.

Schema version:       1
Lifecycle phase:      None — cross-cutting meta-skill (no deal-lifecycle phase).
                      This skill productizes prompt engineering itself for the
                      underwriting team's general Claude Desktop work; it is not
                      bound to any of the 19 lifecycle phases.
Arrakis target app:   Spice prompt library (generate-with-review authoring tool,
                      not a domain application).
Arrakis landing tier: ARRAKIS_RAW.SPICE_LAND.generated_prompt_specs
HITL state at output: PENDING_REVIEW (see wiki/llm-integration/hitl-state-machine.md)

Field naming uses snake_case (Snowflake convention). Types are JSON-serializable
Python primitives. Required-vs-optional is explicit. The schema describes only
the fields the skill's generation pass actually determines; nothing aspirational.

Spec-only note: this skill's PRIMARY output is a free-form generated prompt,
which is intentionally OUT of the structured contract — a generated prompt is an
authoring artifact, not a Snowflake-destined data product. This schema therefore
captures only the GENERATION SPEC: the elicited inputs/tools, the model
selection, and the component set the skill emitted. The generated prompt body is
deliberately not modeled here. When this schema is lifted into Arrakis, it is
registered in the prompt library as the generate-with-review record for the
`prompt_generator_v1` skill and as the data-product schema for the SPICE_LAND
landing table; the prompt text it produced is governed separately as a
versioned prompt-library artifact, not as a structured row.
"""

from typing import Literal

from pydantic import BaseModel, Field


class Elicitation(BaseModel):
    """The three elicited categories the skill gathers before generating.

    Mirrors the skill's Elicitation Framework (Inputs & Tools, Model, Output).
    Each field is a free-text capture of what the analyst supplied or what the
    skill extracted from context and confirmed.
    """

    inputs_tools: str = Field(
        ...,
        description="Reference materials, connectors, and native tools the generated prompt's Claude will use.",
    )
    model: str = Field(
        ...,
        description="Target model elicited or defaulted (e.g. 'Sonnet 4.6' for analytical/credit tasks).",
    )
    output: str = Field(
        ...,
        description="What the generated prompt's Claude should produce, the exact format, and any required structure.",
    )


class GeneratedPromptSpec(BaseModel):
    """Generation spec for one prompt produced by the dl-prompt-generate skill.

    Produced via the prompt-generator prompt. The free-form generated prompt is
    the primary deliverable and is NOT modeled here; this object is the
    Arrakis-side structured record of how that prompt was specified. Always
    emitted in HITL state PENDING_REVIEW with the
    [DRAFT — HUMAN REVIEW REQUIRED] watermark rendered above it in the calling
    skill's response.
    """

    schema_version: int = Field(
        1,
        description="Monotonic schema version; increment on any field addition, removal, or type change.",
    )
    elicitation: Elicitation = Field(
        ...,
        description="The three elicited categories (inputs/tools, model, output) gathered before generation.",
    )
    components_emitted: list[str] = Field(
        ...,
        description="Component names actually emitted into the generated prompt (e.g. 'role', 'input_specification', 'core_instructions').",
    )
    target_model: str = Field(
        ...,
        description="Final target model written into the generated prompt's header line.",
    )
    requires_human_review: bool = Field(
        True,
        description="Always True at output time; set False only after analyst review of the generated prompt downstream.",
    )
    review_state: Literal["PENDING_REVIEW"] = Field(
        "PENDING_REVIEW",
        description="HITL state at output time; subsequent transitions are reviewer-driven.",
    )
