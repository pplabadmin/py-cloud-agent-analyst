from typing import Any

import reflex as rx

from querymind.components.atoms.badge import badge
from querymind.components.atoms.divider import divider
from querymind.components.atoms.heading import subheading
from querymind.components.atoms.text import text
from querymind.components.molecules.prompt_area import prompt_area
from querymind.components.molecules.terminal import terminal
from querymind.styles import COLORS, LAYOUT


def sidebar(**kwargs: Any) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.image(src="/logo.png", width="1.25rem", opacity="0.8"),
                subheading(
                    "Controles",
                    level=3,
                    class_name="text-sm font-bold uppercase tracking-wider",
                ),
                align="center",
                spacing="2",
            ),
            divider(soft=True, class_name="mt-4"),
            prompt_area(),
            divider(soft=True, class_name="my-4"),
            terminal(["Engine Ready", "Waiting for input..."]),
            rx.spacer(),
            rx.vstack(
                divider(soft=True, class_name="mb-4"),
                rx.hstack(
                    badge(
                        "Vertex AI Online", color="green", class_name="animate-pulse"
                    ),
                    rx.spacer(),
                    text("v2026.02", size="1", class_name="opacity-30"),
                    width="100%",
                    align="center",
                ),
                width="100%",
            ),
            height="100%",
            padding=LAYOUT["padding"],
        ),
        width=LAYOUT["sidebar_width"],
        height="100vh",
        bg=COLORS["bg_surface"],
        border_right=f"1px solid {COLORS['border']}",
        display=["none", "none", "flex", "flex"],
        **kwargs,
    )
