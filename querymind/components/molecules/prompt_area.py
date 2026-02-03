import reflex as rx

from querymind.components.atoms.button import button
from querymind.components.atoms.text import text
from querymind.components.atoms.textarea import textarea


def prompt_area() -> rx.Component:
    """Molécula: Zona de entrada de comandos y prompts."""
    return rx.vstack(
        text("¿Qué quieres analizar?", class_name="font-semibold text-zinc-200"),
        textarea(
            placeholder="Ej: Compara el uso de MiBici en 2014 vs 2026...",
            id="analysis_prompt",
        ),
        button(
            "Ejecutar Análisis",
            color="green",
            width="100%",
            class_name="shadow-lg shadow-emerald-900/20",
        ),
        width="100%",
        spacing="3",
        align_items="start",
    )
