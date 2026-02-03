import reflex as rx

from querymind.components.atoms.text import code, text
from querymind.styles import COLORS


def terminal(log_messages: list[str]) -> rx.Component:
    """Molécula: Terminal de ingeniería para logs del sistema."""
    return rx.vstack(
        rx.hstack(
            rx.icon("terminal", size=14, color=COLORS["text_secondary"]),
            text(
                "Logs del Sistema",
                class_name="text-[10px] uppercase tracking-[0.2em] font-bold",
            ),
            spacing="2",
            align="center",
            margin_bottom="0.5rem",
        ),
        rx.box(
            rx.vstack(
                *[code(f"> {msg}") for msg in log_messages],
                spacing="1",
                align_items="start",
                padding="0.5rem",
            ),
            bg="rgba(0,0,0,0.3)",
            border=f"1px solid {COLORS['border']}",
            border_radius="0.5rem",
            width="100%",
            height="220px",
            overflow_y="auto",
            class_name="scrollbar-hide",
        ),
        width="100%",
        spacing="1",
    )
