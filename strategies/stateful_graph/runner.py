"""
Stateful Graph Runner Module.

This module orchestrates the execution of the stateful LangGraph agent. It acts as
the primary entry point for the 'Progressive Disclosure' strategy, managing the
agent's lifecycle, state initialization, dynamic prompt injection, and telemetry
(trace) extraction for performance benchmarking.
"""

import time
from datetime import datetime
from pathlib import Path
from typing import Any, Final, cast

from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

import yaml
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_core.runnables import RunnableConfig

from core.config import settings
from core.providers import provider as llm_provider
from schema import ExecutionReport, TraceStep
from strategies.common import EvaluationStrategy
from strategies.stateful_graph.middleware import MiBiciSkillMiddleware
from strategies.stateful_graph.state import MiBiciState
from strategies.stateful_graph.tools.bq_tools import execute_query
from strategies.stateful_graph.tools.introspection_tools import (
    get_table_schema,
    list_dataset_tables,
)
from strategies.stateful_graph.tools.skills_tool import load_skill


class StatefulGraphRunner(EvaluationStrategy):
    """
    Executes the stateful AI agent using LangGraph and LangChain.

    This runner sets up the agent with specialized tools, a dynamic system prompt,
    and a stateful checkpointer. It tracks execution latency and intercepts tool
    calls to generate a detailed execution trace for observability.
    """

    def __init__(self, checkpointer: MemorySaver) -> None:
        """
        Initializes the stateful graph runner.

        Args:
            checkpointer: The LangGraph memory saver used to persist state
                across conversational turns and tool invocations.
        """
        self._name: Final[str] = "Stateful Graph (On-Demand Skills)"
        self.llm = llm_provider.get_llm(temperature=0.0)
        self.checkpointer = checkpointer
        self.prompt_path = Path("strategies/stateful_graph/prompts/agent_identity.yaml")

    @property
    def name(self) -> str:
        """Returns the human-readable name of the evaluation strategy."""
        return self._name

    def _get_dynamic_identity(self) -> str:
        """
        Loads and interpolates the dynamic agent identity prompt from YAML.

        Injects real-time context (current date) and infrastructure configurations
        (GCP project and dataset IDs) into the base system prompt to ensure
        temporal and environmental awareness.

        Returns:
            The fully interpolated system prompt string ready for the LLM.
        """
        with open(self.prompt_path, encoding="utf-8") as f:
            config = yaml.safe_load(f)
            raw_prompt = config["base_identity"]

        now = datetime.now()
        date_context = f"Hoy es {now.strftime('%A, %d de %B de %Y')}"  # Kept in Spanish for LLM persona

        return raw_prompt.format(
            current_date_context=date_context,
            project_id=settings.project_id,
            dataset_id=settings.dataset_id,
        )

    async def run(self, prompt: str) -> ExecutionReport:
        """
        Executes the agent graph asynchronously with the given user prompt.

        Initializes the state, invokes the agent, and measures total latency.
        Extracts tool execution paths to construct a detailed trace of the
        agent's reasoning and action sequence.

        Args:
            prompt: The natural language query from the user.

        Returns:
            An ExecutionReport containing the final output, execution latency,
            and a step-by-step trace of the agent's internal tool usage.
        """
        start_time = time.perf_counter()
        config = cast(
            RunnableConfig, {"configurable": {"thread_id": "benchmark_session_01"}}
        )

        system_prompt = self._get_dynamic_identity()

        agent = create_agent(
            model=self.llm,
            tools=[execute_query, load_skill, list_dataset_tables, get_table_schema],
            state_schema=MiBiciState,
            system_prompt=system_prompt,
            checkpointer=self.checkpointer,
            middleware=[MiBiciSkillMiddleware()],
        )

        input_state: MiBiciState = {
            "messages": [HumanMessage(content=prompt)],
            "skills_loaded": [],
            "metadata": {},
            "current_sql": "",
            "query_results": [],
            "retry_count": 0,
            "errors": [],
            "jump_to": None,
            "structured_response": None,
        }

        result = await agent.ainvoke(cast(Any, input_state), config=config)
        total_latency = time.perf_counter() - start_time

        trace: list[TraceStep] = []
        for msg in result["messages"]:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    trace.append(
                        TraceStep(
                            name=f"Agent Decision: {tc['name']}",
                            duration=0.0,
                            details={"args": tc.get("args")},
                        )
                    )
            if isinstance(msg, ToolMessage):
                trace.append(
                    TraceStep(
                        name=f"Tool Execution: {msg.name}",
                        duration=0.0,
                        details={"status": "completed"},
                    )
                )

        last_message: BaseMessage = result["messages"][-1]
        final_output = last_message.content

        # Normalize the output content to prevent returning lists of dictionaries
        if isinstance(final_output, list):
            text_parts = []
            for part in final_output:
                if isinstance(part, dict) and "text" in part:
                    text_parts.append(part["text"])
            final_output = "\n".join(text_parts)

        return ExecutionReport(
            strategy_name=self.name,
            output=str(final_output),
            latency=total_latency,
            trace=trace if trace else [TraceStep("Direct LLM Response", total_latency)],
        )
