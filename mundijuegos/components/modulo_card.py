"""Tarjetas de módulos para el menú principal."""

import reflex as rx
from mundijuegos.config import COLORES


def modulo_card(
    titulo: str,
    descripcion: str,
    emoji: str,
    color_fondo: str,
    href: str,
    activo: bool = True,
) -> rx.Component:
    return rx.link(
        rx.card(
            rx.vstack(
                rx.text(
                    emoji,
                    font_size="3.5rem",
                    line_height="1",
                    style={"filter": "none" if activo else "grayscale(70%)"},
                ),
                rx.heading(
                    titulo,
                    size="6",
                    color=COLORES["texto_principal"] if activo else COLORES["texto_secundario"],
                    text_align="center",
                ),
                rx.text(
                    descripcion,
                    color=COLORES["texto_secundario"],
                    text_align="center",
                    font_size="0.95rem",
                ),
                rx.badge(
                    "¡Jugar!" if activo else "Próximamente",
                    color_scheme="pink" if activo else "gray",
                    size="2",
                    radius="full",
                ),
                spacing="3",
                align="center",
                width="100%",
                padding="1rem",
            ),
            style={
                "background": (
                    f"linear-gradient(145deg, {color_fondo}, {COLORES['blanco_hueso']})"
                    if activo else "rgba(240, 240, 240, 0.7)"
                ),
                "border": f"2px solid {COLORES['rosa_claro'] if activo else '#ddd'}",
                "border_radius": "2rem",
                "box_shadow": "0 8px 32px rgba(255, 105, 180, 0.15)" if activo else "none",
                "transition": "all 0.3s ease",
                "cursor": "pointer" if activo else "default",
                "opacity": "1" if activo else "0.6",
            },
            _hover={
                "transform": "translateY(-8px) scale(1.02)" if activo else "none",
                "box_shadow": "0 16px 48px rgba(255, 105, 180, 0.25)" if activo else "none",
                "border_color": COLORES["rosa_chicle"] if activo else "#ddd",
            },
            width="100%",
            max_width="280px",
        ),
        href=href if activo else "#",
        text_decoration="none",
        width="100%",
        display="flex",
        justify_content="center",
        style={"pointer_events": "auto" if activo else "none"},
    )
