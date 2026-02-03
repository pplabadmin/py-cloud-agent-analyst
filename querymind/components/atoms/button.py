from typing import Any, Literal

import reflex as rx

from querymind.styles import COLORS

ButtonColor = Literal[
    "dark/zinc",
    "light",
    "dark/white",
    "dark",
    "white",
    "zinc",
    "indigo",
    "cyan",
    "red",
    "orange",
    "amber",
    "yellow",
    "lime",
    "green",
    "emerald",
    "teal",
    "sky",
    "blue",
    "violet",
    "purple",
    "fuchsia",
    "pink",
    "rose",
]


def _merge_classes(base: str, user: Any) -> str:
    """Fusión limpia de clases de Tailwind."""
    if not user or not isinstance(user, str):
        return base
    return f"{base} {user}".strip()


def button(
    text: str,
    color: ButtonColor | None = "dark/zinc",
    outline: bool = False,
    plain: bool = False,
    href: str | None = None,
    **kwargs: Any,
) -> rx.Component:
    """
    Componente Base: Button
    Mapeo profesional de button.tsx (Catalyst).

    Arquitectura:
    1. Define estilos base y variantes (Tailwind).
    2. Maneja polimorfismo (rx.link vs rx.button).
    3. Implementa TouchTarget (Accesibilidad).
    """

    base_classes = (
        "relative isolate inline-flex items-baseline justify-center gap-x-2 rounded-lg border "
        "text-base/6 font-semibold px-[calc(theme(spacing[3.5])-1px)] py-[calc(theme(spacing[2.5])-1px)] "
        "sm:px-[calc(theme(spacing[3])-1px)] sm:py-[calc(theme(spacing[1.5])-1px)] sm:text-sm/6 "
        "focus:outline-none data-[focus]:outline-2 data-[focus]:outline-offset-2 data-[focus]:outline-blue-500 "
        "disabled:opacity-50 transition-all duration-200"
    )

    if outline:
        variant_classes = (
            f"border-[{COLORS['border']}] text-[{COLORS['text_main']}] "
            "hover:bg-white/5 active:bg-white/5 shadow-sm"
        )
    elif plain:
        variant_classes = (
            f"border-transparent text-[{COLORS['text_main']}] "
            "hover:bg-white/10 active:bg-white/10"
        )
    else:
        bg_color = (
            COLORS["accent"]
            if color in ["green", "dark/zinc", "emerald"]
            else COLORS["bg_surface"]
        )
        text_color = (
            COLORS["bg_dark"]
            if color in ["green", "dark/zinc", "emerald"]
            else COLORS["text_main"]
        )
        variant_classes = (
            f"border-transparent bg-[{bg_color}] text-[{text_color}] "
            "shadow-sm hover:brightness-110 active:brightness-95"
        )

    user_classes = kwargs.pop("class_name", "")
    props = {
        "class_name": _merge_classes(f"{base_classes} {variant_classes}", user_classes),
        **kwargs,
    }

    content = rx.box(
        rx.el.span(
            class_name="absolute top-1/2 left-1/2 size-[max(100%,2.75rem)] -translate-x-1/2 -translate-y-1/2 pointer-events-none"
        ),
        text,
        position="relative",
    )

    if href:
        return rx.link(content, href=href, **props)

    return rx.button(content, **props)
