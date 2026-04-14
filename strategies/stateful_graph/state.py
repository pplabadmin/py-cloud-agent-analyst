"""
Stateful Graph State Module.

Defines the centralized state schema for the MiBici LangGraph agent.
This state is passed continuously between the LLM and the tools, accumulating
messages, active skills, database queries, and execution metadata.
"""

import operator
from typing import Annotated, Any

from langchain.agents import AgentState  # Required for create_agent compatibility


def merge_metadata(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    """
    Explicit reducer for merging metadata dictionaries.

    Uses dictionary unpacking to merge the new metadata into the existing one.
    Defined explicitly as a function rather than a lambda to prevent
    'reportUnknownLambdaType' errors in strict type checkers like Pylance.

    Args:
        old: The current metadata dictionary in the state.
        new: The new metadata dictionary to update with.

    Returns:
        A new dictionary containing the combined key-value pairs.
    """
    return {**old, **new}


class MiBiciState(AgentState):
    """
    Core state definition for the MiBici agent execution graph.

    Inherits from LangChain's `AgentState` to natively include standard keys
    like 'messages', 'jump_to', and 'structured_response', while adding
    custom domain-specific fields for the Progressive Disclosure architecture.
    """

    # Metadata uses the explicit reducer to resolve Pylance typing errors
    metadata: Annotated[dict[str, Any], merge_metadata]

    # Accumulators: Use operator.add to append items to lists during state updates
    skills_loaded: Annotated[list[str], operator.add]
    query_results: Annotated[list[dict[str, Any]], operator.add]
    errors: Annotated[list[str], operator.add]

    # Standard scalar values for business logic and control flow (overwritten on update)
    current_sql: str
    retry_count: int
