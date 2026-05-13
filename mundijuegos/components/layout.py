"""Componentes de layout decorativo para toda la app."""

import reflex as rx
from mundijuegos.config import COLORES


def corazon(size: str = "2rem", delay: str = "0s", duration: str = "3s", left: str = "10%", top: str = "10%") -> rx.Component:
    return rx.el.div(
        "💖",
        style={
            "position": "absolute",
            "left": left,
            "top": top,
            "font_size": size,
            "opacity": "0.7",
            "pointer_events": "none",
            "animation": f"float {duration} ease-in-out {delay} infinite",
            "z_index": "0",
        },
    )


def animalito(emoji: str, position: str, size: str = "3rem") -> rx.Component:
    positions = {
        "top-left": {"top": "1rem", "left": "1rem"},
        "top-right": {"top": "1rem", "right": "1rem"},
        "bottom-left": {"bottom": "1rem", "left": "1rem"},
        "bottom-right": {"bottom": "1rem", "right": "1rem"},
    }
    pos = positions.get(position, positions["top-left"])
    return rx.el.div(
        emoji,
        style={
            "position": "absolute",
            **pos,
            "font_size": size,
            "opacity": "0.85",
            "pointer_events": "none",
            "z_index": "0",
            "animation": "float-slow 6s ease-in-out infinite",
        },
    )


def fondo_animado(children: rx.Component) -> rx.Component:
    """Envuelve el contenido con un fondo animado y decorativo."""
    return rx.box(
        # Capa decorativa absoluta
        rx.box(
            corazon("1.5rem", "0s", "3s", "5%", "10%"),
            corazon("2rem", "1s", "4s", "15%", "25%"),
            corazon("1.2rem", "0.5s", "3.5s", "80%", "15%"),
            corazon("1.8rem", "2s", "5s", "90%", "40%"),
            corazon("1.4rem", "1.5s", "3s", "20%", "60%"),
            corazon("2.2rem", "0.8s", "4.5s", "70%", "70%"),
            corazon("1.6rem", "2.5s", "3.8s", "40%", "85%"),
            corazon("1.3rem", "3s", "5.2s", "60%", "5%"),
            corazon("2rem", "1.2s", "4s", "10%", "80%"),
            corazon("1.5rem", "2.2s", "3.2s", "85%", "90%"),
            animalito("🐰", "top-left", "3.5rem"),
            animalito("🦋", "top-right", "3rem"),
            animalito("🐻", "bottom-left", "3.2rem"),
            animalito("🐱", "bottom-right", "3.5rem"),
            rx.el.div(
                "✨",
                style={
                    "position": "absolute",
                    "top": "30%",
                    "left": "50%",
                    "font_size": "1.5rem",
                    "opacity": "0.5",
                    "animation": "sparkle 3s ease-in-out infinite",
                    "pointer_events": "none",
                },
            ),
            rx.el.div(
                "🌸",
                style={
                    "position": "absolute",
                    "top": "75%",
                    "left": "25%",
                    "font_size": "1.8rem",
                    "opacity": "0.6",
                    "animation": "float 4s ease-in-out 1s infinite",
                    "pointer_events": "none",
                },
            ),
            rx.el.div(
                "🍄",
                style={
                    "position": "absolute",
                    "top": "50%",
                    "right": "10%",
                    "font_size": "2rem",
                    "opacity": "0.5",
                    "animation": "float-slow 7s ease-in-out 0.5s infinite",
                    "pointer_events": "none",
                },
            ),
            position="absolute",
            inset="0",
            overflow="hidden",
            z_index="0",
        ),
        # Contenido principal
        rx.box(
            children,
            position="relative",
            z_index="10",
            max_width="1200px",
            width="100%",
            margin="0 auto",
            padding="clamp(1rem, 3vw, 2rem)",
            min_height="100vh",
            display="flex",
            flex_direction="column",
            align_items="center",
            justify_content="center",
        ),
        style={
            "background": f"linear-gradient(135deg, {COLORES['blanco_hueso']} 0%, {COLORES['rosa_suave']} 50%, {COLORES['lila_pastel']} 100%)",
            "min_height": "100vh",
            "position": "relative",
            "overflow_x": "hidden",
            "overflow_y": "auto",
            "display": "flex",
            "flex_direction": "column",
        },
    )
