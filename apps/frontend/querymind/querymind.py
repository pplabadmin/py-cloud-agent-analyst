import reflex as rx

from querymind.components.atoms.heading import heading
from querymind.components.atoms.text import text
from querymind.components.templates.app_layout import app_layout


def index() -> rx.Component:
    """
    Página Principal (Dashboard) de QueryMind.
    Envuelta en el App Shell para mantener consistencia global.
    """
    return app_layout(
        rx.vstack(
            rx.vstack(
                heading("Analista de Red MiBici GDL", level=1),
                text(
                    "Bienvenido al Sistema Experto. Utiliza los controles laterales para iniciar una consulta sobre la red de transporte.",
                    class_name="max-w-2xl",
                ),
                align_items="start",
                spacing="2",
            ),
            # Aquí irá el Canvas del Grafo / Resultados
            rx.box(
                rx.center(
                    rx.vstack(
                        rx.icon("box_select", size=48, opacity=0.2),
                        text(
                            "El lienzo del análisis aparecerá aquí",
                            class_name="opacity-50",
                        ),
                        spacing="4",
                    ),
                    height="60vh",
                ),
                width="100%",
                border="1px dashed rgba(255,255,255,0.1)",
                border_radius="1rem",
                margin_top="2rem",
            ),
            width="100%",
            spacing="6",
        )
    )


# Configuración de la App
app = rx.App()
app.add_page(index, title="QueryMind")
