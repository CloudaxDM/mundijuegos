"""Página principal: ¡Hola Valentina! + Menú de módulos."""

import reflex as rx
from mundijuegos.config import NOMBRE_NINA, COLORES
from mundijuegos.components.layout import fondo_animado
from mundijuegos.components.modulo_card import modulo_card



def texto_animado(texto: str) -> rx.Component:
    """Renderiza texto con efecto ola letra por letra."""
    letras = []
    for i, letra in enumerate(texto):
        delay = f"{i * 0.08:.2f}s"
        letras.append(
            rx.el.span(
                letra if letra != " " else "\u00A0",
                class_name="wave-letter",
                style={
                    "animation_delay": delay,
                    "display": "inline-block",
                },
            )
        )
    return rx.el.span(
        *letras,
        style={
            "font_size": "4rem",
            "font_weight": "bold",
            "color": COLORES["rosa_chicle"],
            "text_shadow": "2px 2px 8px rgba(255, 105, 180, 0.3)",
            "line_height": "1.2",
        },
    )


def index() -> rx.Component:
    return fondo_animado(
        rx.vstack(
            # Saludo animado
            rx.box(
                rx.el.div(
                    texto_animado(f"¡Hola {NOMBRE_NINA}!"),
                    style={"text_align": "center"},
                ),
                rx.text(
                    "¿A qué jugamos hoy?",
                    size="5",
                    color=COLORES["texto_secundario"],
                    text_align="center",
                    margin_top="0.5rem",
                    style={
                        "animation": "bounce-in 1s ease-out 0.3s forwards",
                        "opacity": "0",
                    },
                ),
                width="100%",
                margin_bottom="1.5rem",
            ),
            # Grid de módulos
            rx.el.div(
                modulo_card(
                    titulo="La Floripondia",
                    descripcion="Adivina la palabra antes de que la flor pierda todos sus pétalos",
                    emoji="🌸",
                    color_fondo=COLORES["rosa_pastel"],
                    href="/ahorcado",
                ),
                modulo_card(
                    titulo="Memoria",
                    descripcion="Encuentra las parejas de animalitos",
                    emoji="🐾",
                    color_fondo=COLORES["celeste_pastel"],
                    href="/memoria",
                ),
                modulo_card(
                    titulo="Colores",
                    descripcion="Aprende y juega con los colores",
                    emoji="🎨",
                    color_fondo=COLORES["amarillo_pastel"],
                    href="/colores",
                ),
                modulo_card(
                    titulo="Puzzle",
                    descripcion="Ordena las piezas de animalitos deslizándolas",
                    emoji="🧩",
                    color_fondo=COLORES["menta_pastel"],
                    href="/puzzle",
                ),
                style={
                    "display": "grid",
                    "grid_template_columns": "repeat(auto-fit, minmax(260px, 1fr))",
                    "gap": "1.5rem",
                    "width": "100%",
                    "max_width": "700px",
                    "animation": "bounce-in 1s ease-out 0.6s forwards",
                    "opacity": "0",
                },
            ),
            # Pie
            rx.text(
                "Hecho con 💕",
                color=COLORES["texto_secundario"],
                font_size="0.85rem",
                margin_top="2rem",
                opacity="0.7",
            ),
            spacing="0",
            align="center",
            width="100%",
            justify="center",
        ),
    )
