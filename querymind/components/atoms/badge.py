from typing import Any, Literal

import reflex as rx

from querymind.styles import COLORS, FONTS

BadgeColor = Literal[
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
    "indigo",
    "violet",
    "purple",
    "fuchsia",
    "pink",
    "rose",
    "zinc",
]


def _merge_classes(*classes: Any) -> str:
    """Combina múltiples clases de Tailwind filtrando valores nulos."""
    return " ".join([str(c) for c in classes if c]).strip()


def badge(text: str, color: BadgeColor = "zinc", **kwargs: Any) -> rx.Component:
    """
    Componente Base: Badge (Revisado)
    Mapeo profesional de badge.tsx.

    Solución de colisiones: Se extraen TODAS las propiedades que definimos
    manualmente antes de pasar el resto a rx.el.span.
    """

    # 1. Definición de la paleta Catalyst (Modo Oscuro)
    color_map = {
        "zinc": "bg-zinc-600/10 text-zinc-400 border-zinc-500/20",
        "green": f"bg-[{COLORS['accent_dim']}] text-[{COLORS['accent']}] border-[{COLORS['accent']}]/20",
        "red": "bg-red-500/10 text-red-400 border-red-500/20",
        "blue": "bg-blue-500/10 text-blue-400 border-blue-500/20",
        "amber": "bg-amber-500/10 text-amber-400 border-amber-500/20",
    }

    selected_style = color_map.get(color, color_map["zinc"])

    base_classes = "inline-flex items-center gap-x-1.5 rounded-md px-1.5 py-0.5 text-xs font-medium border"

    user_classes = kwargs.pop("class_name", "")
    full_class_name = _merge_classes(base_classes, selected_style, user_classes)

    font_family = kwargs.pop("font_family", FONTS["sans"])

    return rx.el.span(
        text,
        class_name=full_class_name,
        font_family=font_family,
        **kwargs,
    )
