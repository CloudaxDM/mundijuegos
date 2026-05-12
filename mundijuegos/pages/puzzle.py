"""Página del módulo Puzzle deslizante."""

import reflex as rx
from mundijuegos.config import NOMBRE_NINA, COLORES
from mundijuegos.components.layout import fondo_animado
from mundijuegos.components.stats import stat_card, ratio_pill, ACENTO_PUNTOS, ACENTO_RECORD
from mundijuegos.state.puzzle_state import PuzzleState

TILE_SIZE   = "88px"
TILE_REF    = "58px"


def tile_pieza(t: dict) -> rx.Component:
    """Pieza del puzzle principal."""
    es_hueco = t["emoji"] == ""
    return rx.cond(
        es_hueco,
        rx.el.div(
            style={
                "width": TILE_SIZE,
                "height": TILE_SIZE,
                "border_radius": "0.75rem",
                "background": "rgba(255,182,193,0.15)",
                "border": f"2px dashed {COLORES['rosa_claro']}",
            },
        ),
        rx.el.div(
            rx.text(t["emoji"], font_size="2.4rem", line_height="1"),
            on_click=PuzzleState.click_tile(t["pos"]),
            style={
                "width": TILE_SIZE,
                "height": TILE_SIZE,
                "border_radius": "0.75rem",
                "background": "white",
                "border": f"2px solid {COLORES['rosa_claro']}",
                "box_shadow": "0 4px 12px rgba(0,0,0,0.11)",
                "display": "flex",
                "align_items": "center",
                "justify_content": "center",
                "cursor": "pointer",
                "transition": "all 0.12s ease",
                "user_select": "none",
            },
            _hover={
                "transform": "scale(1.07)",
                "box_shadow": "0 6px 18px rgba(0,0,0,0.17)",
                "border_color": COLORES["rosa_chicle"],
            },
        ),
    )


def tile_ref(t: dict) -> rx.Component:
    """Pieza pequeña de la imagen de referencia."""
    es_hueco = t["emoji"] == ""
    return rx.cond(
        es_hueco,
        rx.el.div(
            style={
                "width": TILE_REF,
                "height": TILE_REF,
                "border_radius": "0.3rem",
                "background": "rgba(255,182,193,0.1)",
                "border": f"1px dashed {COLORES['rosa_claro']}",
            },
        ),
        rx.el.div(
            rx.text(t["emoji"], font_size="2rem", line_height="1"),
            style={
                "width": TILE_REF,
                "height": TILE_REF,
                "border_radius": "0.3rem",
                "background": "white",
                "border": f"1px solid {COLORES['rosa_claro']}",
                "box_shadow": "0 1px 4px rgba(0,0,0,0.07)",
                "display": "flex",
                "align_items": "center",
                "justify_content": "center",
                "user_select": "none",
            },
        ),
    )


def imagen_referencia() -> rx.Component:
    return rx.vstack(
        rx.text(
            "Objetivo",
            font_size="0.65rem",
            color=COLORES["texto_secundario"],
            font_weight="700",
            text_transform="uppercase",
            letter_spacing="0.06em",
        ),
        rx.el.div(
            rx.foreach(PuzzleState.solucion_tiles, tile_ref),
            style={
                "display": "grid",
                "grid_template_columns": PuzzleState.grid_cols,
                "gap": "0.18rem",
            },
        ),
        align="center",
        spacing="1",
        style={
            "background": "rgba(255,255,255,0.75)",
            "border_radius": "1rem",
            "border": f"1.5px solid {COLORES['rosa_claro']}",
            "padding": "0.65rem 0.75rem",
            "box_shadow": "0 2px 8px rgba(0,0,0,0.07)",
        },
    )


def grid_puzzle() -> rx.Component:
    return rx.el.div(
        rx.foreach(PuzzleState.tiles, tile_pieza),
        style={
            "display": "grid",
            "grid_template_columns": PuzzleState.grid_cols,
            "gap": "0.5rem",
            "width": "100%",
            "max_width": PuzzleState.grid_max_width,
        },
    )


def panel_configuracion() -> rx.Component:
    return rx.card(
        rx.el.div(
            rx.el.div(
                rx.text("Tamaño", font_size="0.7rem", color=COLORES["texto_secundario"]),
                rx.hstack(
                    rx.button(
                        "3×3 Fácil",
                        on_click=PuzzleState.set_config_size(3),
                        size="1",
                        radius="full",
                        color_scheme="pink",
                        variant=rx.cond(PuzzleState.config_size == 3, "solid", "soft"),
                    ),
                    rx.button(
                        "4×4 Difícil",
                        on_click=PuzzleState.set_config_size(4),
                        size="1",
                        radius="full",
                        color_scheme="pink",
                        variant=rx.cond(PuzzleState.config_size == 4, "solid", "soft"),
                    ),
                    spacing="2",
                ),
                style={"display": "flex", "flex_direction": "column", "gap": "0.3rem", "flex": "1"},
            ),
            rx.button(
                "¡Jugar!",
                on_click=PuzzleState.nueva_partida,
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
            stat_card("👆", PuzzleState.movimientos, "Movimientos", ACENTO_PUNTOS),
            stat_card(
                "🏆",
                rx.cond(PuzzleState.mejor_movimientos_actual == 0, "—", PuzzleState.mejor_movimientos_actual),
                "Récord",
                ACENTO_RECORD,
            ),
            spacing="2",
            justify="center",
        ),
        ratio_pill(PuzzleState.partidas_ganadas, PuzzleState.partidas_jugadas),
        spacing="2",
        align="center",
    )


def pantalla_victoria() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "¡Puzzle resuelto! 🧩",
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
            "¡Lo resolviste en ",
            PuzzleState.movimientos,
            " movimientos!",
            color=COLORES["texto_secundario"],
            font_size="1.1rem",
            text_align="center",
        ),
        rx.button(
            "¡Otra vez!",
            on_click=PuzzleState.nueva_partida,
            size="3",
            radius="full",
            style={
                "background": COLORES["rosa_chicle"],
                "color": "white",
                "box_shadow": "0 4px 16px rgba(255,105,180,0.35)",
                "font_weight": "700",
            },
        ),
        spacing="4",
        align="center",
        style={"animation": "bounce-in 0.7s ease-out"},
    )


def puzzle() -> rx.Component:
    return fondo_animado(
        rx.vstack(
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
                rx.heading("Puzzle 🧩", size="6", color=COLORES["rosa_chicle"]),
                justify="between",
                align="center",
                width="100%",
                max_width="700px",
            ),
            rx.text(
                f"¡Ordena las piezas, {NOMBRE_NINA}!",
                color=COLORES["texto_secundario"],
                text_align="center",
                font_size="0.9rem",
            ),
            panel_configuracion(),
            rx.cond(
                PuzzleState.juego_activo | PuzzleState.juego_ganado,
                rx.vstack(
                    panel_estadisticas(),
                    rx.cond(
                        PuzzleState.juego_ganado,
                        pantalla_victoria(),
                        rx.flex(
                            grid_puzzle(),
                            imagen_referencia(),
                            gap="1.5rem",
                            align="start",
                            justify="center",
                            wrap="wrap",
                            width="100%",
                        ),
                    ),
                    spacing="3",
                    align="center",
                    width="100%",
                ),
                rx.text(
                    "Elige el tamaño y pulsa ¡Jugar!",
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
