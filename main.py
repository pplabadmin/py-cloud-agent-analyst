import asyncio
import logging
import sys

from langgraph.checkpoint.memory import MemorySaver  # Requerido para persistencia

from core.logger import setup_logging
from strategies.linear_chain.runner import LinearChainRunner
from strategies.stateful_graph.runner import StatefulGraphRunner
from ui.terminal import TerminalApp


async def main():
    """
    Punto de entrada principal con inyección de dependencias para persistencia.
    """
    setup_logging(level=logging.INFO)

    # Creamos el checkpointer central para que el Runner mantenga habilidades
    shared_checkpointer = MemorySaver()

    terminal = TerminalApp()

    # Inyectamos el checkpointer en el StatefulGraphRunner
    strategies = [
        LinearChainRunner(),
        StatefulGraphRunner(checkpointer=shared_checkpointer),
    ]

    try:
        await terminal.main_loop(strategies)
    except Exception:
        logging.critical("Error fatal no controlado en la aplicación.", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
