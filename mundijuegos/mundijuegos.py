"""Mundijuegos - Punto de entrada principal."""

import reflex as rx
from mundijuegos.config import NOMBRE_NINA
from mundijuegos.pages.index import index
from mundijuegos.pages.ahorcado import ahorcado
from mundijuegos.pages.colores import colores
from mundijuegos.pages.memoria import memoria
from mundijuegos.pages.puzzle import puzzle
from mundijuegos.state.ahorcado_state import AhorcadoState
from mundijuegos.state.colores_state import ColoresState
from mundijuegos.state.memoria_state import MemoriaState
from mundijuegos.state.puzzle_state import PuzzleState


app = rx.App(
    stylesheets=["/custom_animations.css"],
)

app.add_page(index, route="/", title=f"Mundo de {NOMBRE_NINA} 🌸")
app.add_page(ahorcado, route="/ahorcado", title="La Floripondia 🌸", on_load=AhorcadoState.cargar_estadisticas)
app.add_page(colores, route="/colores", title="Colores 🎨", on_load=ColoresState.cargar_estadisticas)
app.add_page(memoria, route="/memoria", title="Memoria 🐾", on_load=MemoriaState.cargar_estadisticas)
app.add_page(puzzle, route="/puzzle", title="Puzzle 🧩", on_load=PuzzleState.cargar_estadisticas)
