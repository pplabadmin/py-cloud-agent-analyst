from typing import Any

import reflex as rx

from querymind.styles import COLORS


def _merge_classes(base: str, user: Any) -> str:
    """Utilidad interna para combinar clases de Tailwind."""
    if not user or not isinstance(user, str):
        return base
    return f"{base} {user}".strip()


def divider(soft: bool = False, **kwargs: Any) -> rx.Component:
    """
    Componente Base: Divider
    Mapeo profesional de divider.tsx (Catalyst).

    Arquitectura:
    1. Implementa la etiqueta <hr> con rol de presentación para accesibilidad.
    2. Maneja la variante 'soft' mediante opacidad de Tailwind.
    3. Permite extender estilos mediante kwargs sin colisiones.
    """

    opacity_class = "opacity-40" if soft else "opacity-100"

    props = {
        "role": "presentation",
        "border_color": COLORS["border"],
        "class_name": f"w-full border-t {opacity_class}",
    }

    props["class_name"] = _merge_classes(
        props["class_name"], kwargs.pop("class_name", None)
    )
    props.update(kwargs)

    return rx.el.hr(**props)
