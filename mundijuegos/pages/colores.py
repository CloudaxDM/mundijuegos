"""Página del módulo Colores."""

import reflex as rx
from mundijuegos.config import NOMBRE_NINA, COLORES
from mundijuegos.components.layout import fondo_animado
from mundijuegos.components.stats import stat_card, ACENTO_PUNTOS, ACENTO_RACHA, ACENTO_RECORD
from mundijuegos.state.colores_state import ColoresState, MODO_NOMBRE, MODO_TOCA


def panel_configuracion() -> rx.Component:
    """Card horizontal compacta de configuración."""
    return rx.card(
        rx.el.div(
            rx.el.div(
                rx.text("Juego", font_size="0.85rem", color=COLORES["texto_secundario"]),
                rx.hstack(
                    rx.button(
                        "¿Qué color es?",
                        on_click=ColoresState.cambiar_config_modo(MODO_NOMBRE),
                        color_scheme="pink",
                        variant=rx.cond(ColoresState.config_modo == MODO_NOMBRE, "solid", "soft"),
                        size="1",
                        radius="full",
                    ),
                    rx.button(
                        "Toca el color",
                        on_click=ColoresState.cambiar_config_modo(MODO_TOCA),
                        color_scheme="pink",
                        variant=rx.cond(ColoresState.config_modo == MODO_TOCA, "solid", "soft"),
                        size="1",
                        radius="full",
                    ),
                    spacing="2",
                ),
                style={"display": "flex", "flex_direction": "column", "gap": "0.3rem", "min_width": "140px", "flex": "1"},
            ),
            rx.el.div(
                rx.text("Vueltas", font_size="0.85rem", color=COLORES["texto_secundario"]),
                rx.slider(
                    default_value=ColoresState.config_rondas,
                    min=5,
                    max=20,
                    step=1,
                    on_change=ColoresState.cambiar_config_rondas,
                    width="100%",
                    color_scheme="pink",
                ),
                rx.text(
                    ColoresState.config_rondas,
                    color=COLORES["rosa_chicle"],
                    font_weight="bold",
                    font_size="0.8rem",
                    text_align="center",
                ),
                style={"display": "flex", "flex_direction": "column", "gap": "0.2rem", "min_width": "80px", "flex": "1"},
            ),
            rx.button(
                "Empezar",
                on_click=ColoresState.aplicar_configuracion,
                color_scheme="pink",
                size="2",
                radius="full",
                style={
                    "background": COLORES["rosa_chicle"],
                    "color": "white",
                    "box_shadow": "0 4px 12px rgba(255, 105, 180, 0.3)",
                    "align_self": "center",
                    "white_space": "nowrap",
                },
            ),
            style={
                "display": "flex",
                "flex_direction": "row",
                "align_items": "center",
                "gap": "1rem",
                "width": "100%",
                "flex_wrap": "wrap",
            },
        ),
        style={
            "background": "rgba(255, 255, 255, 0.6)",
            "backdrop_filter": "blur(8px)",
            "border": f"1px solid {COLORES['rosa_claro']}",
            "border_radius": "1.5rem",
            "width": "100%",
            "max_width": "600px",
            "padding": "0.75rem 1rem",
        },
    )


def panel_estadisticas() -> rx.Component:
    return rx.hstack(
        stat_card("🎯", ColoresState.puntuacion_partida, "Ahora",        ACENTO_PUNTOS),
        stat_card("🔄", ColoresState.ronda_actual,       "Vuelta",       ACENTO_RACHA),
        stat_card("🏆", ColoresState.mejor_puntuacion,   "Mi mejor",     ACENTO_RECORD),
        spacing="2",
        justify="center",
        wrap="wrap",
    )


def circulo_color(color_hex: str, size: str = "120px") -> rx.Component:
    return rx.el.div(
        style={
            "width": size,
            "height": size,
            "border_radius": "50%",
            "background": color_hex,
            "border": "6px solid white",
            "box_shadow": f"0 0 0 3px rgba(0,0,0,0.12), 0 12px 40px rgba(0,0,0,0.25), 0 4px 12px rgba(0,0,0,0.15)",
            "animation": "float 3s ease-in-out infinite",
        },
    )


def opcion_nombre(color: dict) -> rx.Component:
    es_correcta = color["nombre"] == ColoresState.color_correcto["nombre"]
    es_elegida = color["nombre"] == ColoresState.respuesta_elegida
    return rx.button(
        rx.text(color["nombre"], font_weight="700", font_size="1.1rem"),
        on_click=ColoresState.verificar_respuesta(color["nombre"]),
        disabled=ColoresState.mostrar_respuesta,
        radius="full",
        size="3",
        style={
            "background": rx.cond(
                ColoresState.mostrar_respuesta & es_correcta,
                "linear-gradient(145deg, #D3F9D8, #B2F2BB)",
                rx.cond(
                    ColoresState.mostrar_respuesta & es_elegida & ~es_correcta,
                    "linear-gradient(145deg, #FFE3E3, #FFC9C9)",
                    "white",
                ),
            ),
            "color": COLORES["texto_principal"],
            "border": rx.cond(
                ColoresState.mostrar_respuesta & es_correcta,
                "3px solid #69DB7C",
                rx.cond(
                    ColoresState.mostrar_respuesta & es_elegida & ~es_correcta,
                    "3px solid #FF8787",
                    "2px solid rgba(0,0,0,0.08)",
                ),
            ),
            "box_shadow": "0 3px 12px rgba(0,0,0,0.13)",
            "min_width": "130px",
            "transition": "all 0.2s ease",
            "cursor": "pointer",
            "animation": rx.cond(
                ColoresState.mostrar_respuesta & es_correcta,
                "celebration-pop 0.45s ease-out",
                rx.cond(ColoresState.mostrar_respuesta & es_elegida & ~es_correcta, "shake 0.35s ease-out", "none"),
            ),
        },
        _hover={
            "transform": "translateY(-2px) scale(1.04)",
            "box_shadow": "0 6px 20px rgba(0,0,0,0.16)",
        },
    )


def opcion_circulo(color: dict) -> rx.Component:
    es_correcta = color["nombre"] == ColoresState.color_correcto["nombre"]
    es_elegida = color["nombre"] == ColoresState.respuesta_elegida
    return rx.el.button(
        rx.el.div(
            style={
                "width": "90px",
                "height": "90px",
                "border_radius": "50%",
                "background": color["hex"],
                "border": rx.cond(
                    ColoresState.mostrar_respuesta & es_correcta,
                    "5px solid #69DB7C",
                    rx.cond(ColoresState.mostrar_respuesta & es_elegida & ~es_correcta, "5px solid #FF8787", "5px solid white"),
                ),
                "box_shadow": rx.cond(
                    ColoresState.mostrar_respuesta & es_correcta,
                    "0 0 0 5px rgba(105,219,124,0.25), 0 10px 28px rgba(105,219,124,0.35)",
                    "0 0 0 2px rgba(0,0,0,0.1), 0 8px 24px rgba(0,0,0,0.22), 0 2px 8px rgba(0,0,0,0.15)",
                ),
                "transition": "all 0.2s ease",
                "animation": rx.cond(
                    ColoresState.mostrar_respuesta & es_correcta,
                    "celebration-pop 0.45s ease-out",
                    rx.cond(ColoresState.mostrar_respuesta & es_elegida & ~es_correcta, "shake 0.35s ease-out", "none"),
                ),
            },
        ),
        on_click=ColoresState.verificar_respuesta(color["nombre"]),
        disabled=ColoresState.mostrar_respuesta,
        aria_label="Elegir color",
        style={
            "background": "none",
            "border": "none",
            "cursor": "pointer",
            "padding": "0.4rem",
            "border_radius": "50%",
            "transition": "all 0.2s ease",
        },
        _hover={"transform": "scale(1.15)"},
    )


def area_modo_nombre() -> rx.Component:
    return rx.vstack(
        rx.text(
            "¿Qué color es este?",
            size="5",
            color=COLORES["texto_principal"],
            font_weight="bold",
        ),
        circulo_color(ColoresState.color_correcto["hex"], "180px"),
        rx.hstack(
            rx.foreach(ColoresState.opciones, opcion_nombre),
            spacing="4",
            justify="center",
            wrap="wrap",
        ),
        spacing="4",
        align="center",
        width="100%",
    )


def area_modo_toca() -> rx.Component:
    return rx.vstack(
        rx.text(
            "Toca el color",
            size="4",
            color=COLORES["texto_secundario"],
        ),
        rx.heading(
            ColoresState.color_correcto["nombre"],
            size="8",
            color=COLORES["rosa_chicle"],
            style={"animation": "bounce-in 0.5s ease-out"},
        ),
        rx.el.div(
            rx.foreach(ColoresState.opciones, opcion_circulo),
            style={
                "display": "grid",
                "grid_template_columns": "repeat(3, minmax(0, 1fr))",
                "gap": "1.2rem",
                "max_width": "380px",
            },
        ),
        spacing="4",
        align="center",
        width="100%",
    )


def mensaje_estado() -> rx.Component:
    return rx.cond(
        ColoresState.mensaje != "",
        rx.vstack(
            rx.heading(
                ColoresState.mensaje,
                size="6",
                color=rx.cond(
                    ColoresState.ultima_correcta,
                    COLORES["rosa_chicle"],
                    COLORES["texto_secundario"],
                ),
                text_align="center",
                style={"animation": "bounce-in 0.4s ease-out"},
            ),
            rx.cond(
                ColoresState.ultima_correcta,
                rx.hstack(
                    rx.text("✨", font_size="2rem", animation="sparkle 2s infinite"),
                    rx.text("🎉", font_size="2.5rem", animation="bounce-in 0.6s"),
                    rx.text("🌈", font_size="2.4rem", animation="celebration-pop 0.7s"),
                    rx.text("✨", font_size="2rem", animation="sparkle 2s infinite"),
                    spacing="2",
                    justify="center",
                ),
                rx.box(),
            ),
            rx.cond(
                ~ColoresState.juego_terminado,
                rx.button(
                    "Siguiente →",
                    on_click=ColoresState.siguiente_ronda,
                    radius="full",
                    size="3",
                    style={
                        "background": "white",
                        "color": COLORES["rosa_chicle"],
                        "border": f"2px solid {COLORES['rosa_claro']}",
                        "box_shadow": "0 4px 16px rgba(0,0,0,0.12)",
                        "font_weight": "700",
                        "padding": "0 2rem",
                    },
                    _hover={
                        "background": COLORES["rosa_pastel"],
                        "box_shadow": "0 6px 20px rgba(0,0,0,0.15)",
                        "transform": "translateY(-2px)",
                    },
                ),
                rx.box(),
            ),
            spacing="3",
            align="center",
            padding="1rem",
            width="100%",
        ),
        rx.box(),
    )


def barra_progreso() -> rx.Component:
    return rx.vstack(
        rx.text(
            ColoresState.progreso,
            color=COLORES["texto_secundario"],
            font_size="0.85rem",
        ),
        rx.el.div(
            rx.el.div(
                style={
                    "height": "8px",
                    "background": f"linear-gradient(90deg, {COLORES['rosa_chicle']}, {COLORES['rosa_claro']})",
                    "border_radius": "4px",
                    "transition": "width 0.4s ease",
                    "width": ColoresState.progreso_pct,
                },
            ),
            style={
                "width": "100%",
                "max_width": "400px",
                "background": COLORES["rosa_suave"],
                "border_radius": "4px",
                "overflow": "hidden",
                "height": "8px",
            },
        ),
        spacing="1",
        align="center",
        width="100%",
    )


def area_juego() -> rx.Component:
    return rx.vstack(
        barra_progreso(),
        rx.cond(
            ColoresState.modo == MODO_NOMBRE,
            area_modo_nombre(),
            area_modo_toca(),
        ),
        mensaje_estado(),
        spacing="3",
        align="center",
        width="100%",
    )


def colores() -> rx.Component:
    return fondo_animado(
        rx.vstack(
            rx.hstack(
                rx.link(
                    rx.button(
                        "🏠 Juegos",
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
                rx.heading("Colores 🎨", size="6", color=COLORES["rosa_chicle"]),
                justify="between",
                align="center",
                width="100%",
                max_width="700px",
            ),
            rx.text(
                f"¡Aprende los colores, {NOMBRE_NINA}!",
                color=COLORES["texto_secundario"],
                text_align="center",
                font_size="0.9rem",
            ),
            panel_configuracion(),
            panel_estadisticas(),
            rx.cond(
                ColoresState.juego_activo | ColoresState.juego_terminado,
                area_juego(),
                rx.vstack(
                    rx.text(
                        "Elige cómo jugar y pulsa Empezar",
                        color=COLORES["texto_secundario"],
                        text_align="center",
                    ),
                    spacing="4",
                ),
            ),
            rx.cond(
                ColoresState.juego_terminado,
                rx.button(
                    "Jugar otra vez",
                    on_click=ColoresState.nueva_partida,
                    color_scheme="pink",
                    radius="full",
                    size="3",
                    style={
                        "background": COLORES["rosa_chicle"],
                        "color": "white",
                        "box_shadow": "0 4px 12px rgba(255, 105, 180, 0.3)",
                    },
                ),
                rx.box(),
            ),
            spacing="3",
            align="center",
            width="100%",
            padding_bottom="2rem",
        ),
    )
