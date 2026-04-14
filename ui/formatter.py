"""
Módulo de formateo y presentación visual (UI).

Proporciona componentes para renderizar de manera enriquecida (mediante Rich)
las trazas de ejecución, reportes de rendimiento y tablas comparativas en la
terminal. Está diseñado para facilitar la observabilidad del comportamiento
de los motores analíticos.
"""

import logging
from typing import Any

from rich.box import ROUNDED
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from schema import ExecutionReport

logger = logging.getLogger(__name__)


class OutputFormatter:
    """
    Motor de observabilidad y renderizado de alta fidelidad para la terminal.

    Transforma los modelos de datos de ejecución (como `ExecutionReport` y `TraceStep`)
    en representaciones visuales estructuradas, interactivas y fáciles de leer,
    incluyendo árboles de trazas, paneles de Markdown y tablas comparativas.

    Attributes:
        WARNING_THRESHOLD_SEC (float): Umbral en segundos a partir del cual
            un paso de ejecución se marca visualmente como "lento" (advertencia).
        console (Console): Instancia de la consola de Rich compartida para la salida.
    """

    WARNING_THRESHOLD_SEC: float = 2.0

    def __init__(self, console: Console) -> None:
        """
        Inicializa el formateador visual.

        Args:
            console: Instancia de `rich.console.Console` para gestionar la salida estándar.
        """
        self.console = console

    def format_header(self) -> Panel:
        """
        Genera el panel de encabezado principal de la aplicación.

        Returns:
            Panel: Componente visual de Rich con el título y subtítulo del sistema.
        """
        return Panel(
            Text.from_markup(
                "[bold blue]LangChain vs LangGraph Benchmark[/bold blue]\n"
                "[dim]Staff Engineering Observability Engine[/dim]",
                justify="center",
            ),
            box=ROUNDED,
            style="bright_cyan",
        )

    def _add_details_to_tree(self, tree: Tree, details: dict[str, Any]) -> None:
        """
        Agrega metadatos técnicos de forma recursiva a un nodo del árbol de trazas.

        Aplica reglas de resaltado semántico (colores) basándose en las claves
        del diccionario (ej. verde para éxito, rojo para fallos, amarillo para advertencias).

        Args:
            tree: El nodo actual del árbol (`rich.tree.Tree`) al que se añadirán los detalles.
            details: Diccionario con los metadatos a renderizar.
        """
        for key, value in details.items():
            if isinstance(value, dict):
                node = tree.add(f"[bold cyan]{key}[/bold cyan]")
                self._add_details_to_tree(node, value)
            else:
                color = (
                    "green"
                    if key in ["is_safe", "is_semantically_correct", "is_valid"]
                    and value is True
                    else "white"
                )
                if value is False:
                    color = "red"
                if key in ["confidence", "confidence_score"]:
                    color = "yellow"

                tree.add(f"[dim]{key}:[/dim] [{color}]{value}[/{color}]")

    def render_report(self, report: ExecutionReport) -> None:
        """
        Renderiza en consola la traza completa y el resultado de una ejecución.

        Construye un árbol visual que detalla paso a paso la latencia y los metadatos
        de la estrategia ejecutada. Previene errores proporcionando un fallback seguro.

        Args:
            report: El reporte de ejecución estructurado a visualizar.
        """
        # 1. Inicialización de la salida (Safe Fallback)
        formatted_output = (
            Markdown(report.output) if report.output else Text("No data retrieved.")
        )

        # 2. Construcción del Árbol de Observabilidad
        trace_tree = Tree(f"[bold magenta]Trace: {report.strategy_name}[/bold magenta]")

        for step in report.trace:
            status_color = (
                "green" if step.duration < self.WARNING_THRESHOLD_SEC else "yellow"
            )

            step_node = trace_tree.add(
                f"[bold]{step.name}[/bold] "
                f"[dim]in[/dim] [{status_color}]{step.duration:.2f}s[/{status_color}]"
            )

            if step.details:
                self._add_details_to_tree(step_node, step.details)

        # 3. Composición del Grupo de Renderizado
        content = Group(
            trace_tree,
            "\n",
            Panel(
                formatted_output,
                title="[italic white]Final Response[/italic white]",
                title_align="left",
                border_style="bright_blue",
                padding=(1, 1),
            ),
        )

        # 4. Impresión en Consola
        self.console.print(
            Panel(
                content,
                title=f"[bold white]{report.strategy_name}[/bold white]",
                subtitle=f"[bold green]Total Latency: {report.latency:.2f}s[/bold green]",
                border_style="blue",
                padding=(1, 2),
            )
        )

    def render_comparison_table(self, reports: list[ExecutionReport]) -> None:
        """
        Genera y muestra una tabla comparativa de rendimiento entre múltiples estrategias.

        Calcula y resalta la estrategia más rápida ("winner"), así como métricas
        estimadas de rendimiento (TPS) y eficiencia general del flujo.

        Args:
            reports: Lista de reportes de ejecución correspondientes a la iteración actual.
        """
        table = Table(
            title="\n[bold white]Performance Summary Comparison[/bold white]",
            box=ROUNDED,
            header_style="bold cyan",
            expand=True,
        )

        table.add_column("Strategy", style="white", no_wrap=True)
        table.add_column("Latency (s)", justify="right")
        table.add_column("Steps", justify="center")
        table.add_column("Tokens/s (Est.)", justify="right", style="dim")
        table.add_column("Efficiency", justify="center")

        if not reports:
            self.console.print("[yellow]No reports to compare.[/yellow]")
            return

        min_latency = min(r.latency for r in reports)

        for r in reports:
            is_winner = r.latency == min_latency
            latency_style = "bold green" if is_winner else "white"
            tps = len(r.output.split()) / r.latency if r.latency > 0 else 0
            efficiency_score = len(r.trace) / r.latency if r.latency > 0 else 0

            table.add_row(
                f"{'🏆 ' if is_winner else ''}{r.strategy_name}",
                f"[{latency_style}]{r.latency:.2f}s[/{latency_style}]",
                str(len(r.trace)),
                f"{tps:.1f}",
                "⭐" * min(5, int(efficiency_score * 2)),
            )

        self.console.print(table)

    def display_error(self, message: str) -> None:
        """Muestra un error formateado en la terminal."""
        self.console.print(
            Panel(
                Text(message, style="bold white"),
                title="[bold red]Strategy Failure[/bold red]",
                border_style="red",
                padding=(1, 2),
            )
        )
