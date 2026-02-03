from typing import Any

import reflex as rx

from querymind.components.atoms.badge import badge
from querymind.components.atoms.heading import heading
from querymind.components.molecules.nav_item import navbar_item
from querymind.styles import COLORS, LAYOUT


def navbar(**kwargs: Any) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.image(
                    src="/logo.png",
                    width="1.75rem",
                    class_name="rounded-md brightness-110",
                ),
                heading("QueryMind", level=3, class_name="text-lg tracking-tight"),
                spacing="3",
                align="center",
            ),
            rx.hstack(
                navbar_item("Dashboard", active=True),
                spacing="2",
                display=["none", "none", "flex", "flex"],
            ),
            rx.hstack(
                badge("MiBici GDL", color="green", class_name="hidden sm:inline-flex"),
                spacing="4",
                align="center",
            ),
            justify="between",
            align="center",
            width="100%",
            max_width=LAYOUT["max_width"],
            margin="0 auto",
            padding_x=LAYOUT["padding"],
            height="4rem",
        ),
        width="100%",
        border_bottom=f"1px solid {COLORS['border']}",
        background_color="rgba(13, 17, 23, 0.8)",
        backdrop_filter="blur(8px)",
        position="sticky",
        top="0",
        z_index="50",
        **kwargs,
    )
