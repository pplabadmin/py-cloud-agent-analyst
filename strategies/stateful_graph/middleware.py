"""
Skill Orchestration Middleware Module.

Implements the 'Progressive Disclosure' pattern by intercepting requests
to the LLM and dynamically injecting a catalog of available skills into
the system prompt. This ensures the agent is aware of the skills it can
load without bloating the initial context window with their full content,
while resolving LangChain type invariance and incompatible override errors.
"""

from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse

from langchain_core.messages import SystemMessage

from strategies.stateful_graph.skills.registry import SKILLS_CATALOG
from strategies.stateful_graph.state import MiBiciState

# Define the context type variable to respect the base class signature
ContextT = TypeVar("ContextT")


class MiBiciSkillMiddleware(AgentMiddleware[MiBiciState]):
    """
    Middleware that manages progressive disclosure by injecting the skill catalog.

    Uses generic method signatures (`Any`) to comply with the invariance
    requirements of LangChain's `ModelRequest` and avoid typing override errors.
    """

    def _get_addendum(self) -> str:
        """
        Constructs the descriptive skill catalog (Metadata Layer) to be injected.

        Returns:
            A markdown-formatted string listing available skills and explicit
            instructions on how to load them using the 'load_skill' tool.
        """
        skills_list = [
            f"- **{skill['name']}**: {skill['description']}" for skill in SKILLS_CATALOG
        ]
        return (
            "\n\n## Habilidades Disponibles (On-Demand)\n\n"
            + "\n".join(skills_list)
            + "\n\nIMPORTANTE: Tienes acceso a estas habilidades pero su contenido detallado "
            "NO está cargado. Si necesitas realizar un análisis técnico o geográfico, "
            "DEBES usar primero la herramienta 'load_skill' con el nombre de la habilidad."
        )

    def _modify_request(self, request: ModelRequest[Any]) -> ModelRequest[Any]:
        """
        Shared logic to inject the skill catalog addendum into the system message.

        Args:
            request: The incoming model request before it reaches the LLM.

        Returns:
            A new `ModelRequest` with the system message overridden to include
            the dynamically generated skill catalog.
        """
        addendum = self._get_addendum()
        sys_msg = request.system_message

        if sys_msg is None:
            return request.override(system_message=SystemMessage(content=addendum))

        current_content = sys_msg.content
        if isinstance(current_content, str):
            new_content = current_content + addendum
        else:
            new_content = list(current_content) + [{"type": "text", "text": addendum}]

        return request.override(system_message=SystemMessage(content=new_content))

    async def awrap_model_call(
        self,
        request: ModelRequest[Any],  # Use Any to avoid reportIncompatibleMethodOverride
        handler: Callable[[ModelRequest[Any]], Awaitable[ModelResponse]],
    ) -> ModelResponse:
        """
        Asynchronous override compatible with LangChain's middleware API.

        Args:
            request: The original model request containing the prompt and state.
            handler: The next callable in the middleware chain or the model itself.

        Returns:
            The asynchronous response from the model after applying modifications.
        """
        modified_request = self._modify_request(request)
        return await handler(modified_request)

    def wrap_model_call(
        self,
        request: ModelRequest[Any],  # Use Any to avoid reportIncompatibleMethodOverride
        handler: Callable[[ModelRequest[Any]], ModelResponse],
    ) -> ModelResponse:
        """
        Synchronous override compatible with LangChain's middleware API.

        Args:
            request: The original model request containing the prompt and state.
            handler: The next callable in the middleware chain or the model itself.

        Returns:
            The synchronous response from the model after applying modifications.
        """
        modified_request = self._modify_request(request)
        return handler(modified_request)
