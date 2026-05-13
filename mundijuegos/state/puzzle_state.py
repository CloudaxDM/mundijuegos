"""Estado y lógica del módulo Puzzle deslizante."""

import random
import reflex as rx
from mundijuegos.scores import get_game_scores, update_game_scores

EMOJIS_3x3 = ["🦁", "🐯", "🐻", "🦊", "🐼", "🐨", "🐸", "🐧"]
EMOJIS_4x4 = ["🦁", "🐯", "🐻", "🦊", "🐼", "🐨", "🐸", "🐧",
               "🐶", "🐱", "🐰", "🐮", "🐷", "🐑", "🦆"]


class PuzzleState(rx.State):
    """Estado del puzzle deslizante."""

    tiles: list[dict] = []     # [{"pos": i, "emoji": "🦁"}, ...]  "" = hueco
    solucion: list[str] = []   # orden objetivo de emojis
    blank_pos: int = -1        # posición actual del hueco en el grid
    size: int = 3
    movimientos: int = 0
    juego_activo: bool = False
    juego_ganado: bool = False
    config_size: int = 3
    mensaje: str = ""

    # Estadísticas
    mejor_mov_facil: int = 0
    mejor_mov_dificil: int = 0
    partidas_jugadas: int = 0
    partidas_ganadas: int = 0

    def cargar_estadisticas(self):
        stats = get_game_scores("puzzle")
        self.mejor_mov_facil = stats.get("mejor_mov_facil", 0)
        self.mejor_mov_dificil = stats.get("mejor_mov_dificil", 0)
        self.partidas_jugadas = stats.get("partidas_jugadas", 0)
        self.partidas_ganadas = stats.get("partidas_ganadas", 0)

    def cambiar_config_size(self, value: int):
        self.config_size = value
        self.tiles = []
        self.juego_activo = False
        self.juego_ganado = False
        self.movimientos = 0
        self.blank_pos = -1
        self.mensaje = ""

    def nueva_partida(self):
        n = self.config_size
        self.size = n
        emojis = EMOJIS_3x3 if n == 3 else EMOJIS_4x4
        solucion = list(emojis) + [""]
        self.solucion = solucion

        # Revolver desde estado resuelto → siempre resoluble
        tiles_emojis = list(solucion)
        blank = n * n - 1
        n_moves = 60 if n == 3 else 120
        prev = -1
        for _ in range(n_moves):
            vecinos = [v for v in self._vecinos(blank, n) if v != prev]
            swap = random.choice(vecinos)
            tiles_emojis[blank], tiles_emojis[swap] = tiles_emojis[swap], tiles_emojis[blank]
            prev = blank
            blank = swap

        self.tiles = [{"pos": i, "emoji": e} for i, e in enumerate(tiles_emojis)]
        self.blank_pos = blank
        self.movimientos = 0
        self.juego_activo = True
        self.juego_ganado = False
        self.mensaje = ""

    def _vecinos(self, pos: int, n: int) -> list[int]:
        row, col = divmod(pos, n)
        result = []
        if row > 0:     result.append(pos - n)
        if row < n - 1: result.append(pos + n)
        if col > 0:     result.append(pos - 1)
        if col < n - 1: result.append(pos + 1)
        return result

    def click_tile(self, pos: int):
        if not self.juego_activo or pos == self.blank_pos:
            return
        if pos not in self._vecinos(self.blank_pos, self.size):
            self.mensaje = "Busca una pieza pegadita al hueco 🕳️"
            return

        self.mensaje = ""
        tiles = list(self.tiles)
        emoji_movido = tiles[pos]["emoji"]
        tiles[self.blank_pos] = {"pos": self.blank_pos, "emoji": emoji_movido}
        tiles[pos] = {"pos": pos, "emoji": ""}
        self.tiles = tiles
        self.blank_pos = pos
        self.movimientos += 1

        if [t["emoji"] for t in tiles] == self.solucion:
            self.juego_ganado = True
            self.juego_activo = False
            self.mensaje = "¡Lo has conseguido! 🎉"
            self._guardar_estadisticas()

    def _guardar_estadisticas(self):
        self.partidas_jugadas += 1
        self.partidas_ganadas += 1
        key = "mejor_mov_facil" if self.config_size == 3 else "mejor_mov_dificil"
        actual = getattr(self, key)
        if actual == 0 or self.movimientos < actual:
            setattr(self, key, self.movimientos)
        update_game_scores("puzzle", {
            "mejor_mov_facil": self.mejor_mov_facil,
            "mejor_mov_dificil": self.mejor_mov_dificil,
            "partidas_jugadas": self.partidas_jugadas,
            "partidas_ganadas": self.partidas_ganadas,
        })

    @rx.var(cache=True)
    def grid_cols(self) -> str:
        return f"repeat({self.size}, minmax(0, 1fr))"

    @rx.var(cache=True)
    def grid_max_width(self) -> str:
        return "360px" if self.size == 3 else "460px"

    @rx.var(cache=True)
    def mejor_movimientos_actual(self) -> int:
        return self.mejor_mov_facil if self.config_size == 3 else self.mejor_mov_dificil

    @rx.var(cache=True)
    def solucion_tiles(self) -> list[dict]:
        return [{"pos": i, "emoji": e} for i, e in enumerate(self.solucion)]
