from typing import Any

import reflex as rx

from querymind.styles import COLORS, FONTS


def _merge_classes(base: str, user: Any) -> str:
    """Utilidad para fusionar clases de Tailwind sin duplicidad."""
    if not user or not isinstance(user, str):
        return base
    return f"{base} {user}".strip()


def textarea(**kwargs: Any) -> rx.Component:
    """
    Componente Base: Textarea
    Mapeo profesional de textarea.tsx (Catalyst).

    Características:
    - Foco con el color de acento de MiBici.
    - Sizing responsivo siguiendo el estándar de Tailwind UI.
    - Estilos de estado (hover, focus, disabled) encapsulados.
    """

    # 1. Propiedades de Identidad Visual (Defaults del Design System)
    props = {
        "font_family": FONTS["sans"],
        "background_color": COLORS["bg_surface"],
        "color": COLORS["text_main"],
        "border": f"1px solid {COLORS['border']}",
        "rows": "4",
        # Clases de Catalyst para padding, tipografía y transiciones
        "class_name": (
            "block w-full appearance-none rounded-lg px-[calc(theme(spacing[3.5])-1px)] "
            "py-[calc(theme(spacing[2.5])-1px)] text-base/6 sm:text-sm/6 "
            "placeholder:text-zinc-500 focus:outline-none transition-all duration-200"
        ),
        # Estados definidos programáticamente para evitar colisiones de Tailwind
        "_focus": {
            "border_color": COLORS["accent"],
            "box_shadow": f"0 0 0 2px {COLORS['accent_dim']}",
        },
        "_hover": {
            "border_color": COLORS["text_secondary"],
        },
        "_disabled": {
            "opacity": "0.5",
            "cursor": "not-allowed",
        },
    }

    # 2. Fusión de Clases y Extensión de Props
    # Extraemos class_name para fusionarlo y permitimos que kwargs sobrescriba defaults
    props["class_name"] = _merge_classes(
        props["class_name"], kwargs.pop("class_name", None)
    )
    props.update(kwargs)

    return rx.text_area(**props)
