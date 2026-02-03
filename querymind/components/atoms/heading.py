from typing import Any, Literal

import reflex as rx

from querymind.styles import COLORS, FONTS

HeadingSize = Literal["1", "2", "3", "4", "5", "6", "7", "8", "9"]


def _merge_classes(base: str, user: Any) -> str:
    """Utilidad interna para combinar clases sin duplicados."""
    if not user or not isinstance(user, str):
        return base
    return f"{base} {user}".strip()


def heading(text: str, level: int = 1, **kwargs: Any) -> rx.Component:
    """
    Componente Base: Heading
    Mapeo: text-2xl/8 font-semibold text-zinc-950 sm:text-xl/8
    """
    size_map: dict[int, HeadingSize] = {
        1: "7",  # ~24px
        2: "6",  # ~20px
        3: "5",  # ~18px
        4: "4",  # ~16px
    }

    props = {
        "as_": f"h{level}",
        "size": size_map.get(level, "7"),
        "font_weight": "semibold",
        "font_family": FONTS["sans"],
        "color": COLORS["text_main"],
        "class_name": "tracking-tight sm:tracking-normal leading-8",
    }

    props["class_name"] = _merge_classes(
        props["class_name"], kwargs.pop("class_name", None)
    )
    props.update(kwargs)

    return rx.heading(text, **props)


def subheading(text: str, level: int = 2, **kwargs: Any) -> rx.Component:
    """
    Componente Base: Subheading (Variante con opacidad reducida)
    Mapeo: font-semibold text-zinc-950/75
    """
    props = {
        "as_": f"h{level}",
        "size": "4",
        "font_weight": "semibold",
        "font_family": FONTS["sans"],
        "color": COLORS["text_main"],
        "class_name": "opacity-75 leading-7 sm:leading-6",
    }

    props["class_name"] = _merge_classes(
        props["class_name"], kwargs.pop("class_name", None)
    )
    props.update(kwargs)

    return rx.heading(text, **props)
