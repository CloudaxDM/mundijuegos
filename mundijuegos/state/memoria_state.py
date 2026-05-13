"""Estado y lógica del módulo Memoria."""

import asyncio
import random
import reflex as rx
from mundijuegos.scores import get_game_scores, update_game_scores


EMOJIS = [
    "🐶", "🐱", "🐻", "🐰", "🦊", "🐸",
    "🦋", "🐘", "🦁", "🐼", "🐧", "🦄",
    "🐬", "🦀", "🦉", "🐙",
]

DIFICULTADES = {
    "facil":  {"parejas": 6,  "cols": 3, "max_width": "340px"},
    "medio":  {"parejas": 8,  "cols": 4, "max_width": "450px"},
    "dificil":{"parejas": 10, "cols": 5, "max_width": "540px"},
}


class MemoriaState(rx.State):
    """Estado del juego Memoria."""

    cartas: list[dict] = []
    primera_carta: int = -1
    bloqueado: bool = False
    movimientos: int = 0
    parejas_encontradas: int = 0
    total_parejas: int = 6
    juego_activo: bool = False
    juego_ganado: bool = False
    config_dificultad: str = "facil"
    mensaje: str = ""

    # Estadísticas persistentes
    mejor_movimientos_facil: int = 0
    mejor_movimientos_medio: int = 0
    mejor_movimientos_dificil: int = 0
    partidas_jugadas: int = 0
    partidas_ganadas: int = 0

    def cargar_estadisticas(self):
        stats = get_game_scores("memoria")
        self.mejor_movimientos_facil = stats.get("mejor_movimientos_facil", 0)
        self.mejor_movimientos_medio = stats.get("mejor_movimientos_medio", 0)
        self.mejor_movimientos_dificil = stats.get("mejor_movimientos_dificil", 0)
        self.partidas_jugadas = stats.get("partidas_jugadas", 0)
        self.partidas_ganadas = stats.get("partidas_ganadas", 0)

    def cambiar_config_dificultad(self, value: str):
        self.config_dificultad = value
        self.cartas = []
        self.juego_activo = False
        self.juego_ganado = False
        self.movimientos = 0
        self.parejas_encontradas = 0
        self.primera_carta = -1
        self.bloqueado = False
        self.mensaje = ""

    def nueva_partida(self):
        config = DIFICULTADES[self.config_dificultad]
        n = config["parejas"]
        self.total_parejas = n
        emojis = random.sample(EMOJIS, n)
        pares = emojis * 2
        random.shuffle(pares)
        self.cartas = [
            {"id": i, "emoji": e, "volteada": False, "encontrada": False}
            for i, e in enumerate(pares)
        ]
        self.primera_carta = -1
        self.bloqueado = False
        self.movimientos = 0
        self.parejas_encontradas = 0
        self.juego_activo = True
        self.juego_ganado = False
        self.mensaje = ""

    async def voltear_carta(self, index: int):
        if self.bloqueado:
            return
        carta = self.cartas[index]
        if carta["encontrada"] or carta["volteada"]:
            return

        # Voltear esta carta
        nuevas = list(self.cartas)
        nuevas[index] = {**carta, "volteada": True}
        self.cartas = nuevas

        if self.primera_carta == -1:
            self.primera_carta = index
            self.mensaje = "Busca su pareja 👀"
            return

        # Segunda carta seleccionada
        i1 = self.primera_carta
        i2 = index
        self.movimientos += 1
        self.bloqueado = True
        yield  # enviar estado (ambas visibles) al frontend

        await asyncio.sleep(0.9)

        nuevas = list(self.cartas)
        if nuevas[i1]["emoji"] == nuevas[i2]["emoji"]:
            nuevas[i1] = {**nuevas[i1], "encontrada": True}
            nuevas[i2] = {**nuevas[i2], "encontrada": True}
            self.cartas = nuevas
            self.parejas_encontradas += 1
            if self.parejas_encontradas >= self.total_parejas:
                self.juego_ganado = True
                self.juego_activo = False
                self.mensaje = "¡Todas las parejas juntas! 🎉"
                self._guardar_estadisticas()
            else:
                self.mensaje = "¡Pareja encontrada! ✨"
        else:
            nuevas[i1] = {**nuevas[i1], "volteada": False}
            nuevas[i2] = {**nuevas[i2], "volteada": False}
            self.cartas = nuevas
            self.mensaje = "Casi, prueba otra pareja 💪"

        self.primera_carta = -1
        self.bloqueado = False

    def _guardar_estadisticas(self):
        self.partidas_jugadas += 1
        self.partidas_ganadas += 1
        key = f"mejor_movimientos_{self.config_dificultad}"
        actual = getattr(self, key)
        if actual == 0 or self.movimientos < actual:
            setattr(self, key, self.movimientos)
        update_game_scores(
            "memoria",
            {
                "mejor_movimientos_facil": self.mejor_movimientos_facil,
                "mejor_movimientos_medio": self.mejor_movimientos_medio,
                "mejor_movimientos_dificil": self.mejor_movimientos_dificil,
                "partidas_jugadas": self.partidas_jugadas,
                "partidas_ganadas": self.partidas_ganadas,
            },
        )

    @rx.var(cache=True)
    def grid_cols(self) -> str:
        cols = DIFICULTADES[self.config_dificultad]["cols"]
        return f"repeat({cols}, minmax(0, 1fr))"

    @rx.var(cache=True)
    def grid_max_width(self) -> str:
        return DIFICULTADES[self.config_dificultad]["max_width"]

    @rx.var(cache=True)
    def mejor_movimientos_actual(self) -> int:
        if self.config_dificultad == "medio":
            return self.mejor_movimientos_medio
        if self.config_dificultad == "dificil":
            return self.mejor_movimientos_dificil
        return self.mejor_movimientos_facil

    @rx.var(cache=True)
    def progreso(self) -> str:
        return f"{self.parejas_encontradas} / {self.total_parejas}"
