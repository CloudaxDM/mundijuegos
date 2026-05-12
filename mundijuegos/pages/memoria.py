"""Página del módulo Memoria."""

import reflex as rx
from mundijuegos.config import NOMBRE_NINA, COLORES
from mundijuegos.components.layout import fondo_animado
from mundijuegos.components.stats import stat_card, ratio_pill, ACENTO_PUNTOS, ACENTO_RACHA, ACENTO_RECORD
from mundijuegos.state.memoria_state import MemoriaState

CARTA_SIZE = "88px"

ESTILO_CARTA_BASE = {
    "width": CARTA_SIZE,
    "height": CARTA_SIZE,
    "border_radius": "1rem",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "user_select": "none",
}


def carta_dorso(c: dict) -> rx.Component:
    return rx.el.div(
        "🌸",
        on_click=MemoriaState.voltear_carta(c["id"]),
        style={
            **ESTILO_CARTA_BASE,
            "background": f"linear-gradient(145deg, {COLORES['rosa_pastel']}, {COLORES['rosa_chicle']})",
            "border": "3px solid white",
            "box_shadow": "0 5px 16px rgba(0,0,0,0.18)",
            "cursor": "pointer",
            "font_size": "2rem",
            "transition": "transform 0.15s ease, box-shadow 0.15s ease",
        },
        _hover={
            "transform": "scale(1.08)",
            "box_shadow": "0 8px 22px rgba(0,0,0,0.22)",
        },
    )


def carta_cara(c: dict) -> rx.Component:
    return rx.el.div(
        rx.text(c["emoji"], font_size="2.5rem", line_height="1"),
        style={
            **ESTILO_CARTA_BASE,
            "background": "white",
            "border": f"3px solid {COLORES['rosa_claro']}",
            "box_shadow": "0 4px 14px rgba(0,0,0,0.12)",
            "animation": "card-flip 0.25s ease-out",
        },
    )


def carta_encontrada(c: dict) -> rx.Component:
    return rx.el.div(
        rx.text(c["emoji"], font_size="2.5rem", line_height="1"),
        style={
            **ESTILO_CARTA_BASE,
            "background": f"linear-gradient(145deg, {COLORES['menta_pastel']}, #b8ffb8)",
            "border": "3px solid #69DB7C",
            "box_shadow": "0 2px 8px rgba(105,219,124,0.35)",
            "opacity": "0.85",
        },
    )


def carta(c: dict) -> rx.Component:
    return rx.cond(
        c["encontrada"],
        carta_encontrada(c),
        rx.cond(
            c["volteada"],
            carta_cara(c),
            carta_dorso(c),
        ),
    )


def grid_cartas() -> rx.Component:
    return rx.el.div(
        rx.foreach(MemoriaState.cartas, carta),
        style={
            "display": "grid",
            "grid_template_columns": MemoriaState.grid_cols,
            "gap": "0.65rem",
            "width": "100%",
            "max_width": MemoriaState.grid_max_width,
        },
    )


def panel_configuracion() -> rx.Component:
    def btn_dif(label: str, value: str) -> rx.Component:
        return rx.button(
            label,
            on_click=MemoriaState.set_config_dificultad(value),
            size="1",
            radius="full",
            color_scheme="pink",
            variant=rx.cond(MemoriaState.config_dificultad == value, "solid", "soft"),
        )

    return rx.card(
        rx.el.div(
            rx.el.div(
                rx.text("Dificultad", font_size="0.7rem", color=COLORES["texto_secundario"]),
                rx.hstack(
                    btn_dif("Fácil", "facil"),
                    btn_dif("Medio", "medio"),
                    btn_dif("Difícil", "dificil"),
                    spacing="2",
                ),
                style={
                    "display": "flex",
                    "flex_direction": "column",
                    "gap": "0.3rem",
                    "flex": "1",
                },
            ),
            rx.button(
                "¡Jugar!",
                on_click=MemoriaState.nueva_partida,
                size="2",
                radius="full",
                style={
                    "background": COLORES["rosa_chicle"],
                    "color": "white",
                    "box_shadow": "0 4px 12px rgba(255,105,180,0.3)",
                    "font_weight": "700",
                    "align_self": "center",
                    "white_space": "nowrap",
                },
            ),
            style={
                "display": "flex",
                "flex_direction": "row",
                "align_items": "center",
                "gap": "1.5rem",
                "width": "100%",
                "flex_wrap": "wrap",
            },
        ),
        style={
            "background": "rgba(255,255,255,0.6)",
            "backdrop_filter": "blur(8px)",
            "border": f"1px solid {COLORES['rosa_claro']}",
            "border_radius": "1.5rem",
            "width": "100%",
            "max_width": "600px",
            "padding": "0.75rem 1rem",
        },
    )


def panel_estadisticas() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            stat_card("👆", MemoriaState.movimientos,             "Movimientos",  ACENTO_PUNTOS),
            stat_card("🃏", MemoriaState.progreso,                "Parejas",      ACENTO_RACHA),
            stat_card(
                "🏆",
                rx.cond(MemoriaState.mejor_movimientos_actual == 0, "—", MemoriaState.mejor_movimientos_actual),
                "Récord",
                ACENTO_RECORD,
            ),
            spacing="2",
            justify="center",
            wrap="wrap",
        ),
        ratio_pill(MemoriaState.partidas_ganadas, MemoriaState.partidas_jugadas),
        spacing="2",
        align="center",
    )


def pantalla_victoria() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "¡Lo encontraste todo! 🎉",
            size="6",
            color=COLORES["rosa_chicle"],
            text_align="center",
            style={"animation": "bounce-in 0.6s ease-out"},
        ),
        rx.hstack(
            rx.text("✨", font_size="2.5rem", animation="sparkle 2s infinite"),
            rx.text("🎊", font_size="3rem", animation="bounce-in 0.8s"),
            rx.text("✨", font_size="2.5rem", animation="sparkle 2s infinite"),
            spacing="2",
            justify="center",
        ),
        rx.text(
            "¡Lo hiciste en ",
            MemoriaState.movimientos,
            " movimientos!",
            color=COLORES["texto_secundario"],
            font_size="1.1rem",
            text_align="center",
        ),
        rx.button(
            "¡Jugar otra vez!",
            on_click=MemoriaState.nueva_partida,
            size="3",
            radius="full",
            style={
                "background": COLORES["rosa_chicle"],
                "color": "white",
                "box_shadow": "0 4px 16px rgba(255,105,180,0.35)",
                "font_weight": "700",
            },
            _hover={
                "transform": "scale(1.05)",
                "box_shadow": "0 6px 22px rgba(255,105,180,0.45)",
            },
        ),
        spacing="4",
        align="center",
        padding="1.5rem",
        style={"animation": "bounce-in 0.7s ease-out"},
    )


def memoria() -> rx.Component:
    return fondo_animado(
        rx.vstack(
            # Header
            rx.hstack(
                rx.link(
                    rx.button(
                        "← Volver",
                        radius="full",
                        size="2",
                        style={
                            "background": "white",
                            "color": COLORES["rosa_chicle"],
                            "border": f"2px solid {COLORES['rosa_claro']}",
                            "box_shadow": "0 2px 8px rgba(0,0,0,0.12)",
                            "font_weight": "600",
                        },
                        _hover={
                            "background": COLORES["rosa_pastel"],
                            "box_shadow": "0 4px 16px rgba(0,0,0,0.15)",
                        },
                    ),
                    href="/",
                    text_decoration="none",
                ),
                rx.heading("Memoria 🐾", size="6", color=COLORES["rosa_chicle"]),
                justify="between",
                align="center",
                width="100%",
                max_width="700px",
            ),
            rx.text(
                f"¡Encuentra las parejas, {NOMBRE_NINA}!",
                color=COLORES["texto_secundario"],
                text_align="center",
                font_size="0.9rem",
            ),
            panel_configuracion(),
            rx.cond(
                MemoriaState.juego_activo | MemoriaState.juego_ganado,
                rx.vstack(
                    panel_estadisticas(),
                    rx.cond(
                        MemoriaState.juego_ganado,
                        pantalla_victoria(),
                        grid_cartas(),
                    ),
                    spacing="3",
                    align="center",
                    width="100%",
                ),
                rx.text(
                    "Elige la dificultad y pulsa ¡Jugar!",
                    color=COLORES["texto_secundario"],
                    text_align="center",
                ),
            ),
            spacing="3",
            align="center",
            width="100%",
            padding_bottom="2rem",
        ),
    )
