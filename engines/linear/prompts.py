from langchain_core.prompts import ChatPromptTemplate

# Clasificador de Intenciones (Routing)
ROUTER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Eres un clasificador de consultas experto. Tu única función es etiquetar la entrada del usuario "
            "en una de estas dos categorías: 'INVENTORY' o 'SALES'.\n"
            "Responde solo con la etiqueta en mayúsculas.",
        ),
        ("user", "{input}"),
    ]
)

# Rama de Inventario: Corrección de columna product_distribution_center_id
INVENTORY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Eres un experto en BigQuery para `bigquery-public-data.thelook_ecommerce`. "
            "Genera SQL siguiendo estas reglas:\n"
            "1. Usa `COUNT(*)` como `total_inventory`.\n"
            "2. JOIN CORRECTO: `inventory_items` (t1) con `distribution_centers` (t2) usando `t1.product_distribution_center_id = t2.id`.\n"
            "3. NORMALIZACIÓN: Usa nombres en inglés para los centros (ej. 'Brazil' en lugar de 'Brasil'). "
            "Usa UPPER(t2.name) = UPPER('nombre_traducido').",
        ),
        ("user", "{input}"),
    ]
)

# Rama de Ventas
SALES_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Eres un analista de ventas para `bigquery-public-data.thelook_ecommerce`. "
            "Calcula el Net Revenue sumando `sale_price` de `order_items` donde el estado no sea 'Cancelled'.\n"
            "Solo devuelve el código SQL puro.",
        ),
        ("user", "{input}"),
    ]
)
