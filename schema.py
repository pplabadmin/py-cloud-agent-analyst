"""
Esquemas de datos centrales para observabilidad y reportes.

Este módulo define las estructuras de datos (dataclasses) utilizadas para
estandarizar el registro de métricas, trazas de ejecución y resultados
finales a través de los diferentes motores analíticos (estrategias).
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class TraceStep:
    """
    Representa un paso individual e inmutable dentro de una traza de ejecución.

    Utilizado para medir la latencia y registrar los metadatos de operaciones
    específicas (ej. generación de SQL, auditoría, ejecución en BD) a lo largo
    del ciclo de vida de una consulta.

    Attributes:
        name (str): Nombre identificador del paso o componente ejecutado.
        duration (float): Tiempo total de ejecución del paso en segundos.
        details (dict[str, Any]): Metadatos estructurados arbitrarios (contexto,
            puntajes de confianza, veredictos de seguridad, etc.).
    """

    name: str
    duration: float
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionReport:
    """
    Reporte consolidado de la ejecución de una estrategia de evaluación.

    Agrupa el resultado final que se mostrará al usuario, junto con la
    latencia total acumulada y el desglose detallado de cada paso intermedio
    tomado por el motor (secuencial o agéntico).

    Attributes:
        strategy_name (str): Nombre de la estrategia o motor que generó el reporte.
        output (str): Respuesta final formateada, destinada al usuario final.
        latency (float): Tiempo total transcurrido (end-to-end), en segundos.
        trace (list[TraceStep]): Historial secuencial de los pasos ejecutados.
    """

    strategy_name: str
    output: str
    latency: float
    trace: list[TraceStep] = field(default_factory=list)
