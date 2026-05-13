"""Página del módulo El Ahorcado."""

import reflex as rx
from mundijuegos.config import NOMBRE_NINA, COLORES
from mundijuegos.components.layout import fondo_animado
from mundijuegos.components.stats import stat_card, ratio_pill, ACENTO_PUNTOS, ACENTO_RACHA, ACENTO_RECORD, ACENTO_TOTAL
from mundijuegos.state.ahorcado_state import AhorcadoState


def petalo(index: int) -> rx.Component:
    """Dibuja un pétalo individual."""
    return rx.cond(
        index < AhorcadoState.petalos_perdidos,
        rx.el.div(
            "🥀",
            style={
                "font_size": "2.5rem",
                "opacity": "0.3",
                "animation": "petal-fall 1s ease-in forwards",
                "filter": "grayscale(80%)",
            },
        ),
        rx.el.div(
            "🌸",
            style={
                "font_size": "2.5rem",
                "opacity": "1",
                "animation": "float 3s ease-in-out infinite",
                "filter": "drop-shadow(0 2px 4px rgba(255,105,180,0.3))",
            },
        ),
    )


def dibujo_flor() -> rx.Component:
    """Visualiza la flor con sus pétalos."""
    return rx.vstack(
        rx.hstack(
            rx.foreach(AhorcadoState.petalos_indices, petalo),
            spacing="4",
            wrap="wrap",
            justify="center",
            width="100%",
        ),
        rx.box(
            rx.cond(
                AhorcadoState.juego_perdido,
                rx.text("😢", font_size="3rem", animation="shake 0.5s"),
                rx.text("🌼", font_size="3rem"),
            ),
            margin_top="-0.5rem",
        ),
        rx.text(
            AhorcadoState.texto_petalos,
            color=COLORES["texto_secundario"],
            font_size="0.9rem",
            margin_top="0.5rem",
        ),
        align="center",
        spacing="2",
        width="100%",
        padding="1rem",
        style={
            "background": "rgba(255, 255, 255, 0.5)",
            "border_radius": "2rem",
            "backdrop_filter": "blur(8px)",
            "border": f"2px dashed {COLORES['rosa_claro']}",
        },
    )


def palabra_display() -> rx.Component:
    """Muestra la palabra con letras adivinadas."""
    return rx.box(
        rx.heading(
            AhorcadoState.palabra_mostrada,
            size="8",
            color=COLORES["texto_principal"],
            style={
                "letter_spacing": "0.3rem",
                "font_family": "'Courier New', monospace",
            },
            text_align="center",
        ),
        padding="1.5rem",
        style={
            "background": "rgba(255, 255, 255, 0.7)",
            "border_radius": "1.5rem",
            "border": f"2px solid {COLORES['rosa_claro']}",
            "box_shadow": "0 4px 16px rgba(255, 105, 180, 0.1)",
        },
        width="100%",
        max_width="600px",
    )


def teclado_letra(letra: str) -> rx.Component:
    """Botón individual del teclado virtual."""
    usada = AhorcadoState.letras_adivinadas.contains(letra) | AhorcadoState.letras_falladas.contains(letra)
    acertada = AhorcadoState.letras_adivinadas.contains(letra)

    return rx.el.button(
        letra,
        on_click=AhorcadoState.adivinar_letra(letra),
        disabled=usada,
        style={
            "width": "2.8rem",
            "height": "2.8rem",
            "border_radius": "0.8rem",
            "border": f"2px solid {COLORES['rosa_claro']}",
            "background": rx.cond(
                acertada,
                COLORES["menta_pastel"],
                rx.cond(
                    usada,
                    COLORES["rosa_suave"],
                    "white",
                ),
            ),
            "color": rx.cond(
                usada,
                COLORES["texto_secundario"],
                COLORES["texto_principal"],
            ),
            "font_size": "1.2rem",
            "font_weight": "bold",
            "cursor": rx.cond(usada, "default", "pointer"),
            "transition": "all 0.2s ease",
            "opacity": rx.cond(usada, "0.6", "1"),
        },
        _hover={
            "transform": rx.cond(usada, "none", "scale(1.1)"),
            "background": rx.cond(usada, "", COLORES["rosa_pastel"]),
        },
    )


def teclado_fila_grid(letras: list[str], cols: int) -> rx.Component:
    """Fila de teclado con CSS Grid para que nunca se rompa."""
    return rx.el.div(
        rx.foreach(letras, teclado_letra),
        style={
            "display": "grid",
            "grid_template_columns": f"repeat({cols}, minmax(0, 1fr))",
            "gap": "0.35rem",
            "width": "100%",
            "max_width": f"{cols * 2.6 + (cols - 1) * 0.35}rem",
        },
    )


def teclado() -> rx.Component:
    """Teclado virtual QWERTY con grid perfecto."""
    fila1 = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"]
    fila2 = ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Ñ"]
    fila3 = ["Z", "X", "C", "V", "B", "N", "M"]

    return rx.vstack(
        teclado_fila_grid(fila1, 10),
        teclado_fila_grid(fila2, 10),
        teclado_fila_grid(fila3, 7),
        spacing="1",
        align="center",
        width="100%",
        max_width="520px",
    )


def panel_configuracion() -> rx.Component:
    """Card horizontal compacta de configuración."""
    return rx.card(
        rx.el.div(
            rx.el.div(
                rx.text("Pétalos", font_size="0.85rem", color=COLORES["texto_secundario"]),
                rx.slider(
                    default_value=AhorcadoState.config_intentos,
                    min=3,
                    max=10,
                    step=1,
                    on_change=AhorcadoState.cambiar_config_intentos,
                    width="100%",
                    color_scheme="pink",
                ),
                rx.text(
                    AhorcadoState.config_intentos,
                    color=COLORES["rosa_chicle"],
                    font_weight="bold",
                    font_size="0.8rem",
                    text_align="center",
                ),
                style={"display": "flex", "flex_direction": "column", "gap": "0.2rem", "min_width": "80px", "flex": "1"},
            ),
            rx.el.div(
                rx.text("Palabra corta", font_size="0.85rem", color=COLORES["texto_secundario"]),
                rx.slider(
                    default_value=AhorcadoState.config_min,
                    min=3,
                    max=8,
                    step=1,
                    on_change=AhorcadoState.cambiar_config_min,
                    width="100%",
                    color_scheme="pink",
                ),
                rx.text(
                    AhorcadoState.config_min,
                    color=COLORES["rosa_chicle"],
                    font_weight="bold",
                    font_size="0.8rem",
                    text_align="center",
                ),
                style={"display": "flex", "flex_direction": "column", "gap": "0.2rem", "min_width": "80px", "flex": "1"},
            ),
            rx.el.div(
                rx.text("Palabra larga", font_size="0.85rem", color=COLORES["texto_secundario"]),
                rx.slider(
                    default_value=AhorcadoState.config_max,
                    min=6,
                    max=15,
                    step=1,
                    on_change=AhorcadoState.cambiar_config_max,
                    width="100%",
                    color_scheme="pink",
                ),
                rx.text(
                    AhorcadoState.config_max,
                    color=COLORES["rosa_chicle"],
                    font_weight="bold",
                    font_size="0.8rem",
                    text_align="center",
                ),
                style={"display": "flex", "flex_direction": "column", "gap": "0.2rem", "min_width": "80px", "flex": "1"},
            ),
            rx.button(
                "Empezar",
                on_click=AhorcadoState.aplicar_configuracion,
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
    return rx.vstack(
        rx.hstack(
            stat_card("🎯", AhorcadoState.puntuacion_partida, "Ahora",        ACENTO_PUNTOS),
            stat_card("🔥", AhorcadoState.racha_actual,       "Seguidas",     ACENTO_RACHA),
            stat_card("🏆", AhorcadoState.mejor_racha,        "Mi mejor",     ACENTO_RECORD),
            stat_card("⭐", AhorcadoState.puntuacion_total,   "Total",        ACENTO_TOTAL),
            spacing="2",
            justify="center",
            wrap="wrap",
        ),
        ratio_pill(AhorcadoState.partidas_ganadas, AhorcadoState.partidas_jugadas),
        spacing="2",
        align="center",
    )


def mensaje_estado() -> rx.Component:
    return rx.cond(
        AhorcadoState.mensaje != "",
        rx.box(
            rx.heading(
                AhorcadoState.mensaje,
                size="6",
                color=rx.cond(
                    AhorcadoState.juego_ganado,
                    COLORES["rosa_chicle"],
                    COLORES["texto_secundario"],
                ),
                text_align="center",
                style={"animation": "bounce-in 0.6s ease-out"},
            ),
            rx.cond(
                AhorcadoState.juego_ganado,
                rx.hstack(
                    rx.text("✨", font_size="2rem", animation="sparkle 2s infinite"),
                    rx.text("🎉", font_size="2.5rem", animation="bounce-in 0.8s"),
                    rx.text("🌸", font_size="2.6rem", animation="celebration-pop 0.7s"),
                    rx.text("✨", font_size="2rem", animation="sparkle 2s infinite"),
                    spacing="2",
                    justify="center",
                ),
                rx.box(),
            ),
            padding="1rem",
            width="100%",
        ),
        rx.box(),
    )


def ahorcado() -> rx.Component:
    return fondo_animado(
        rx.vstack(
            # Header compacto
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
                rx.heading("La Floripondia 🌸", size="6", color=COLORES["rosa_chicle"]),
                justify="between",
                align="center",
                width="100%",
                max_width="700px",
            ),
            rx.text(
                f"¡Adivina la palabra, {NOMBRE_NINA}!",
                color=COLORES["texto_secundario"],
                text_align="center",
                font_size="0.9rem",
            ),
            # Configuración compacta
            panel_configuracion(),
            # Estadísticas
            panel_estadisticas(),
            # Área de juego
            rx.cond(
                AhorcadoState.palabra != "",
                rx.vstack(
                    dibujo_flor(),
                    palabra_display(),
                    mensaje_estado(),
                    teclado(),
                    rx.hstack(
                        rx.button(
                            "Nueva partida",
                            on_click=AhorcadoState.nueva_partida,
                            color_scheme="pink",
                            radius="full",
                            size="3",
                        ),
                        rx.button(
                            "Me rindo",
                            on_click=AhorcadoState.rendirse,
                            color_scheme="red",
                            variant="soft",
                            radius="full",
                            size="3",
                        ),
                        spacing="4",
                        margin_top="1rem",
                    ),
                    spacing="4",
                    width="100%",
                    align="center",
                    style={
                        "animation": "bounce-in 0.8s ease-out",
                    },
                ),
                rx.vstack(
                    rx.text(
                        "Configura arriba y pulsa Aplicar para empezar",
                        color=COLORES["texto_secundario"],
                        text_align="center",
                    ),
                    spacing="4",
                ),
            ),
            spacing="3",
            align="center",
            width="100%",
            padding_bottom="2rem",
        ),
    )
