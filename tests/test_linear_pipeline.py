from unittest.mock import patch

from engines.linear.pipeline import LLMManager, get_linear_tree


def test_llm_manager_instantiation() -> None:
    """Valida la creación del modelo sin disparar alertas de protected-access."""
    with patch("engines.linear.pipeline.ChatGoogleGenerativeAI") as mock_chat:
        # Usamos getattr para evitar W0212/reportPrivateUsage
        if getattr(LLMManager, "_instance", None) is not None:
            LLMManager._instance = None  # type: ignore # pylint: disable=protected-access

        model = LLMManager.get_model()
        assert model is not None
        mock_chat.assert_called_once()


def test_get_linear_tree_routing_logic() -> None:
    """Cubre las lambdas de ruteo invocando la lógica del árbol."""
    tree = get_linear_tree()

    # En lugar de callable(), probamos el comportamiento de las ramas
    # Esto ejecuta las funciones _is_inventory y _is_sales
    assert tree.branches[0][0].invoke({"input": "stock"}) is True
    assert tree.branches[1][0].invoke({"input": "ventas"}) is True
    assert tree.branches[0][0].invoke({"input": "nada"}) is False
