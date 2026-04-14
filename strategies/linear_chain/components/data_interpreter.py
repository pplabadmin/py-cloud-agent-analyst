import time
from pathlib import Path
from typing import Any, cast

import yaml
from langchain_core.messages import HumanMessage, SystemMessage

from core.providers import LLMProvider
from schema import TraceStep


class DataInterpreter:
    """
    Final node responsible for synthesizing the data or errors into
    a human-readable response.
    """

    def __init__(self, provider: LLMProvider) -> None:
        self.llm = provider.get_llm(temperature=0.7)

        current_file = Path(__file__).resolve()
        self.prompt_path = current_file.parent.parent / "prompts" / "interpreter.yaml"

        with self.prompt_path.open(encoding="utf-8") as f:
            self.config = cast(dict[str, Any], yaml.safe_load(f))

    async def interpret(
        self,
        query: str,
        data: list[dict[str, Any]] | str,
        is_success: bool,
        context: str = "",
    ) -> tuple[str, TraceStep]:
        start_time = time.perf_counter()

        prompt_key = "success_prompt" if is_success else "failure_prompt"
        system_content = str(self.config.get(prompt_key, ""))

        if is_success:
            # Inyectamos contexto para que el analista entienda qué buscaba hacer el SQL
            system_msg = system_content.format(query=query, explanation=context)
            user_msg = f"Dataset Results: {data}"
        else:
            system_msg = system_content
            user_msg = f"User Request: {query}\nFailure Reason: {data}"

        messages = [SystemMessage(content=system_msg), HumanMessage(content=user_msg)]

        response = await self.llm.ainvoke(messages)
        duration = time.perf_counter() - start_time

        return str(response.content), TraceStep(
            name="Final Interpretation",
            duration=duration,
            details={"mode": "success" if is_success else "failure"},
        )
