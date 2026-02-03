from typing import Any

import reflex as rx

from querymind.styles import COLORS, FONTS


def _merge_classes(base: str, user: Any) -> str:
    """Utilidad interna para combinar clases de Tailwind sin duplicados."""
    if not user or not isinstance(user, str):
        return base
    return f"{base} {user}".strip()


def text(content: str, **kwargs: Any) -> rx.Component:
    """
    Componente Base: Text
    Mapeo: text-base/6 text-zinc-500 sm:text-sm/6
    """
    # 1. Definir la intención del diseño (Catalyst Defaults)
    props = {
        "font_family": FONTS["sans"],
        "size": "3",
        "color": COLORS["text_secondary"],
        "class_name": "leading-6 sm:text-[0.8125rem]",
    }

    # 2. Fusión de clases (Merge)
    props["class_name"] = _merge_classes(
        props["class_name"], kwargs.pop("class_name", None)
    )

    # 3. Sobrescritura de Props (Cualquier kwarg como size="1" gana al default)
    props.update(kwargs)

    return rx.text(content, **props)


def strong(content: str, **kwargs: Any) -> rx.Component:
    """
    Componente Base: Strong
    Mapeo: font-medium text-zinc-950
    """
    props = {
        "font_weight": "medium",
        "color": COLORS["text_main"],
        "font_family": FONTS["sans"],
        "display": "inline",
    }
    props["class_name"] = _merge_classes("", kwargs.pop("class_name", None))
    props.update(kwargs)

    return rx.el.strong(content, **props)


def code(content: str, **kwargs: Any) -> rx.Component:
    """
    Componente Base: Code
    Mapeo: rounded-sm border bg-zinc-950/2.5 text-sm
    """
    props = {
        "font_family": FONTS["mono"],
        "size": "2",
        "color": COLORS["text_main"],
        "bg": "rgba(255, 255, 255, 0.05)",
        "border": f"1px solid {COLORS['border']}",
        "border_radius": "0.25rem",
        "class_name": "px-1 font-medium sm:text-[0.8125rem]",
    }
    props["class_name"] = _merge_classes(
        props["class_name"], kwargs.pop("class_name", None)
    )
    props.update(kwargs)

    return rx.code(content, **props)
