"""
Common Strategies Protocol Module.

Defines the core interfaces and protocols used across all evaluation strategies
(e.g., Stateful Graph, Linear Chain). This ensures a uniform execution and
benchmarking contract regardless of the underlying LLM orchestration framework.
"""

from typing import Protocol

from schema import ExecutionReport


class EvaluationStrategy(Protocol):
    """
    Standard interface for all AI execution strategies.

    By implementing this Protocol, different agent architectures can be executed
    and compared interchangeably by the benchmarking UI, ensuring that all
    strategies provide a uniform output structure (`ExecutionReport`).
    """

    @property
    def name(self) -> str:
        """
        Returns the human-readable identifier of the evaluation strategy.
        """
        ...

    async def run(self, prompt: str) -> ExecutionReport:
        """
        Executes the strategy's core logic with the provided user prompt.

        Args:
            prompt: The natural language query from the user.

        Returns:
            An ExecutionReport containing the result, latency, and telemetry trace.
        """
        ...
