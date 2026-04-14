"""
Módulo de la Interfaz de Usuario de Terminal (TUI).

Define y orquesta la experiencia interactiva del usuario en la consola.
Utiliza la librería Rich para crear una interfaz rica y dinámica, gestionando
el ciclo de vida de la aplicación, la captura de prompts, la ejecución de
estrategias de benchmark y la visualización de resultados en tiempo real.
"""

import logging

from rich.console import Console
from rich.live import Live
from rich.prompt import Prompt
from rich.spinner import Spinner

from schema import ExecutionReport
from strategies.common import EvaluationStrategy
from ui.formatter import OutputFormatter

logger = logging.getLogger(__name__)


class TerminalApp:
    """
    Orquestador principal de la interfaz de usuario en la terminal.

    Esta clase encapsula toda la lógica de la TUI. Es responsable de:
    - Gestionar el estado del ciclo de vida de la aplicación (inicio, ejecución, finalización).
    - Renderizar componentes visuales como encabezados, spinners y reportes.
    - Capturar la entrada del usuario de forma segura, manejando señales de salida.
    - Invocar las estrategias de evaluación (benchmarks) y mostrar su progreso.
    - Presentar los resultados finales, incluyendo tablas comparativas de rendimiento.

    Attributes:
        console (Console): Instancia de la consola de Rich para toda la renderización.
        formatter (OutputFormatter): Motor de formato para los reportes de ejecución.
    """

    def __init__(self) -> None:
        """Inicializa la aplicación de terminal y sus componentes de UI."""
        self.console = Console()
        self.formatter = OutputFormatter(self.console)
        self._is_running = True

    def _show_welcome(self) -> None:
        """Limpia la consola y muestra el banner de bienvenida de la aplicación."""
        self.console.clear()
        self.console.print(self.formatter.format_header())

    def ask_user(self) -> str | None:
        """
        Captura la entrada del usuario de forma interactiva y maneja las señales de salida.

        Utiliza Rich Prompt para una experiencia de entrada mejorada. Detecta comandos
        de salida ('exit', 'quit', 'q') o una interrupción de teclado (Ctrl+C) para
        finalizar el bucle principal de la aplicación de forma segura.

        Returns:
            La consulta del usuario como una cadena de texto, o None si se detectó
            una señal de salida.
        """
        try:
            query = Prompt.ask(
                "\n[bold yellow]🔍 Ingrese prompt[/bold yellow] [dim](o 'exit' para salir)[/dim]",
                default="exit",
            )

            if query.lower() in ["exit", "quit", "q"]:
                self._is_running = False
                return None
            else:
                return query
        except KeyboardInterrupt:
            self._is_running = False
            return None

    async def run_benchmark(
        self, strategies: list[EvaluationStrategy], prompt: str
    ) -> list[ExecutionReport]:
        """
        Ejecuta una lista de estrategias de evaluación de forma secuencial para un prompt.

        Para cada estrategia, muestra un spinner de progreso en tiempo real utilizando
        `rich.Live`. Si una estrategia se completa con éxito, su reporte individual
        se renderiza inmediatamente. Si falla, se registra el error y se muestra un
        mensaje en la UI sin detener la ejecución de las estrategias restantes.

        Args:
            strategies: Una lista de objetos que cumplen con la interfaz EvaluationStrategy.
            prompt: La consulta del usuario a ser evaluada.

        Returns:
            Una lista de objetos ExecutionReport, uno por cada estrategia ejecutada.
        """
        reports: list[ExecutionReport] = []

        for strategy in strategies:
            with Live(
                Spinner(
                    "dots",
                    text=f"[bold blue] Ejecutando {strategy.name}...[/bold blue]",
                ),
                console=self.console,
                transient=True,
            ):
                try:
                    report = await strategy.run(prompt)
                    reports.append(report)
                    # Renderizado inmediato del reporte individual
                    self.formatter.render_report(report)
                except Exception as e:
                    logger.exception(f"Falla en estrategia {strategy.name}")
                    self.formatter.display_error(f"Error en {strategy.name}: {str(e)}")

        return reports

    def finalize_iteration(self, reports: list[ExecutionReport]) -> None:
        """
        Renderiza los resultados consolidados al final de una iteración del benchmark.

        Si se generaron reportes, muestra una tabla comparativa de rendimiento.
        También provee al usuario con instrucciones para continuar o salir.

        Args:
            reports: La lista de reportes de ejecución de la iteración.
        """
        if reports:
            self.formatter.render_comparison_table(reports)

        self.console.print("\n[dim]Presione Ctrl+C o escriba 'exit' para salir.[/dim]")

    async def main_loop(self, strategies: list[EvaluationStrategy]) -> None:
        """
        Ejecuta el bucle principal e interactivo de la aplicación.

        Gestiona el ciclo de vida completo: muestra la bienvenida, y luego, en un
        bucle, solicita la entrada del usuario, ejecuta el benchmark con las
        estrategias proporcionadas, y finaliza la iteración mostrando los resultados
        consolidados, hasta que el usuario decide salir.

        Args:
            strategies: La lista de estrategias de evaluación a ejecutar en cada iteración.
        """
        self._show_welcome()

        if not strategies:
            self.formatter.display_error("No se cargaron estrategias de evaluación.")
            return

        while self._is_running:
            prompt = self.ask_user()

            if prompt:
                reports = await self.run_benchmark(strategies, prompt)
                self.finalize_iteration(reports)
            elif self._is_running:
                continue

        self.console.print(
            "\n[bold cyan]👋 Benchmark finalizado. ¡Hasta luego![/bold cyan]"
        )
