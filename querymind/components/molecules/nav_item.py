import reflex as rx

from querymind.components.atoms.text import text
from querymind.styles import COLORS


def navbar_item(label: str, href: str = "#", active: bool = False) -> rx.Component:
    """
    Molécula: NavbarItem.
    Gestiona el estado visual del enlace y el indicador inferior.
    """
    return rx.link(
        text(
            label,
            size="2",
            font_weight="500",
            color=COLORS["text_main"] if active else COLORS["text_secondary"],
            class_name="transition-colors hover:text-white",
        ),
        href=href,
        class_name=(
            "relative flex items-center px-3 py-2 "
            + (
                f"after:absolute after:bottom-[-1.25rem] after:left-0 after:h-[2px] after:w-full after:bg-[{COLORS['accent']}]"
                if active
                else ""
            )
        ),
    )
