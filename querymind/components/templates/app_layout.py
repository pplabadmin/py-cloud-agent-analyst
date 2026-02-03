from typing import Any

import reflex as rx

from querymind.components.organisms.navbar import navbar
from querymind.components.organisms.sidebar import sidebar
from querymind.styles import COLORS, LAYOUT


def app_layout(children: rx.Component, **kwargs: Any) -> rx.Component:
    return rx.box(
        navbar(display=["block", "block", "none", "none"]),
        rx.hstack(
            sidebar(),
            rx.box(
                rx.vstack(
                    navbar(display=["none", "none", "block", "block"]),
                    rx.box(children, width="100%", padding=LAYOUT["padding"]),
                    width="100%",
                    spacing="0",
                ),
                flex="1",
                height="100vh",
                overflow_y="auto",
                background_color=COLORS["bg_dark"],
            ),
            width="100%",
            spacing="0",
            align_items="start",
        ),
        width="100%",
        height="100vh",
        **kwargs,
    )
