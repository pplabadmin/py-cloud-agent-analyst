"""
Dynamic Skill Loader Tool Module.

Implements the 'Progressive Disclosure' architectural pattern. Instead of
front-loading the system prompt with all possible domain rules, schemas, and
geospatial logic, the agent uses this tool to fetch specialized knowledge
on-demand. This approach optimizes context window usage, reduces prompt
distraction, and explicitly manages state transitions in the LangGraph execution.
"""

from typing import Literal

from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command

from strategies.stateful_graph.skills.registry import SKILLS_CATALOG
from strategies.stateful_graph.state import MiBiciState


@tool
def load_skill(
    skill_name: str, runtime: ToolRuntime[None, MiBiciState]
) -> Command[Literal["agent"]]:
    """
    Loads the detailed content of a specialized technical skill into the agent's context.

    This tool should be invoked by the agent when it requires specific domain knowledge
    (e.g., database schemas, geospatial handling, business rules) to fulfill the
    user's request.

    Args:
        skill_name: The exact string identifier of the skill (e.g., 'sql_query_expert').
        runtime: The LangChain tool runtime injected automatically, providing
            access to the graph's state and the active tool call ID.

    Returns:
        A LangGraph `Command` that updates the state by appending the loaded skill
        to 'skills_loaded' and returning a `ToolMessage` with the skill's content.
        Returns an error `ToolMessage` if the requested skill does not exist.
    """
    # 1. Search for the requested skill in the dynamically loaded YAML catalog
    skill_data = next((s for s in SKILLS_CATALOG if s["name"] == skill_name), None)

    if not skill_data:
        available = ", ".join(s["name"] for s in SKILLS_CATALOG)
        return Command(
            update={
                "messages": [
                    ToolMessage(
                        content=f"Error: Skill '{skill_name}' no encontrada. Disponibles: {available}",
                        tool_call_id=runtime.tool_call_id,
                    )
                ]
            }
        )

    # 2. Return a Command to update the persistent state.
    # 'skills_loaded' is appended to via the 'operator.add' reducer in MiBiciState.
    return Command(
        update={
            "skills_loaded": [skill_name],
            "messages": [
                ToolMessage(
                    content=f"Habilidad '{skill_name}' cargada con éxito:\n\n{skill_data['content']}",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )
