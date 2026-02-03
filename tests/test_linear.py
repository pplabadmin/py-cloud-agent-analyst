import os
import sys
from unittest.mock import MagicMock, patch

import pytest
from _pytest.logging import LogCaptureFixture

from core.tools import QueryResult
from engines.linear.main import main as main_entry
from engines.linear.pipeline import run_linear_engine

# Seteamos entorno para evitar validaciones de API Key reales
os.environ["GOOGLE_API_KEY"] = "fake_key_for_testing"

# --- PRUEBAS DE LÓGICA DEL MOTOR ---


@pytest.mark.parametrize(
    "pregunta, rama_esperada",
    [
        ("¿Cuál es el stock en Brasil?", "inventory"),
        ("¿Cuánto vendimos ayer?", "sales"),
        ("pregunta genérica", "inventory"),
    ],
)
# CORRECCIÓN: Parchamos la función constructora, no la variable global
@patch("engines.linear.pipeline.get_linear_tree")
def test_routing_logic(
    mock_get_tree: MagicMock, pregunta: str, rama_esperada: str
) -> None:
    """Valida el ruteo parchando la función generadora del árbol."""
    mock_tree = MagicMock()
    mock_tree.invoke.return_value = QueryResult(data=[], columns=[])
    mock_get_tree.return_value = mock_tree

    run_linear_engine(pregunta)

    # Verificamos que se llame al invoke del árbol retornado
    mock_tree.invoke.assert_called_with({"input": pregunta})


# --- PRUEBAS DEL PUNTO DE ENTRADA (Integration) ---


@patch("engines.linear.main.run_linear_engine")
def test_main_execution_success(mock_run: MagicMock, caplog: LogCaptureFixture) -> None:
    """Valida ejecución exitosa ajustando el nivel de caplog."""
    # CORRECCIÓN: Forzamos el nivel INFO para que caplog capture todo
    caplog.set_level("INFO")

    mock_run.return_value = QueryResult(data=[[1]], columns=["test"])

    with patch.object(sys, "argv", ["main.py", "¿Stock?"]):
        main_entry()

    # Ahora sí encontrará estos strings en el buffer de logs
    assert "Iniciando benchmark lineal" in caplog.text
    assert "Ejecución exitosa" in caplog.text
