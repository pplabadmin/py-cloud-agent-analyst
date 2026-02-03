from unittest.mock import MagicMock, patch

from google.api_core.exceptions import GoogleAPICallError

from core.tools import BigQueryManager, bq_executor


def test_bq_executor_api_error() -> None:
    """Cubre excepciones y soluciona el error de membership test (E1135)."""
    with patch("core.tools.BigQueryManager.get_client") as mock_get:
        mock_client = MagicMock()
        mock_client.query.side_effect = GoogleAPICallError("Quota exceeded")
        mock_get.return_value = mock_client

        result = bq_executor("SELECT 1")

        # Solución E1135: Aseguramos que error no sea None antes del test de membresía
        err_msg = result.error or ""
        assert "GCP Error" in err_msg


def test_bigquery_manager_singleton() -> None:
    """Valida el Singleton sin acceder a miembros protegidos como _client."""
    # En lugar de resetear _client (que da error W0212), validamos el comportamiento
    client1 = BigQueryManager.get_client()
    client2 = BigQueryManager.get_client()

    assert client1 is client2
