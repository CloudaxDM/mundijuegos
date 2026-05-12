"""Componente reutilizable de tarjeta de estadística."""

import reflex as rx
from mundijuegos.config import COLORES

# Paleta de acento por tipo de estadística
ACENTO_PUNTOS  = "#FF69B4"   # rosa_chicle
ACENTO_RACHA   = "#69DB7C"   # verde menta
ACENTO_RECORD  = "#FFD43B"   # dorado
ACENTO_TOTAL   = "#4DABF7"   # azul
ACENTO_NEUTRO  = "#C084FC"   # lila


def stat_card(emoji: str, valor, label: str, acento: str) -> rx.Component:
    """Tarjeta de estadística con icono, valor grande y etiqueta."""
    return rx.box(
        rx.vstack(
            rx.el.span(emoji, style={"font_size": "1.5rem", "line_height": "1"}),
            rx.text(
                valor,
                style={
                    "font_size": "1.75rem",
                    "font_weight": "900",
                    "color": acento,
                    "line_height": "1",
                },
            ),
            rx.text(
                label,
                style={
                    "font_size": "0.6rem",
                    "color": COLORES["texto_secundario"],
                    "text_align": "center",
                    "text_transform": "uppercase",
                    "letter_spacing": "0.06em",
                    "font_weight": "700",
                    "line_height": "1.3",
                },
            ),
            spacing="1",
            align="center",
            gap="0.25rem",
        ),
        style={
            "background": "rgba(255,255,255,0.92)",
            "backdrop_filter": "blur(8px)",
            "border_radius": "1.2rem",
            "border": f"1.5px solid {acento}25",
            "border_top": f"3.5px solid {acento}",
            "box_shadow": f"0 4px 14px rgba(0,0,0,0.07), 0 1px 3px {acento}18",
            "padding": "0.7rem 0.85rem",
            "min_width": "80px",
            "text_align": "center",
            "transition": "transform 0.2s ease",
        },
        _hover={"transform": "translateY(-2px)"},
    )


def ratio_pill(ganadas, jugadas) -> rx.Component:
    """Pastilla con ratio partidas ganadas/jugadas."""
    return rx.cond(
        jugadas > 0,
        rx.box(
            rx.hstack(
                rx.text("🏅", font_size="0.85rem"),
                rx.text(
                    ganadas,
                    " ganadas de ",
                    jugadas,
                    " partidas",
                    font_size="0.75rem",
                    color=COLORES["texto_secundario"],
                    font_weight="600",
                ),
                spacing="1",
                align="center",
            ),
            style={
                "background": "rgba(255,255,255,0.75)",
                "border_radius": "2rem",
                "border": f"1px solid {COLORES['rosa_claro']}",
                "padding": "0.3rem 0.9rem",
                "box_shadow": "0 2px 8px rgba(0,0,0,0.06)",
            },
        ),
        rx.box(),
    )
