"""Estado y lógica del módulo Colores."""

import random
import reflex as rx
from mundijuegos.scores import get_game_scores, update_game_scores


COLORES_JUEGO = [
    {"nombre": "Rojo", "hex": "#FF6B6B", "emoji": "🔴"},
    {"nombre": "Azul", "hex": "#4DABF7", "emoji": "🔵"},
    {"nombre": "Verde", "hex": "#69DB7C", "emoji": "🟢"},
    {"nombre": "Amarillo", "hex": "#FFD43B", "emoji": "🟡"},
    {"nombre": "Rosa", "hex": "#F783AC", "emoji": "🩷"},
    {"nombre": "Naranja", "hex": "#FFA94D", "emoji": "🟠"},
    {"nombre": "Morado", "hex": "#DA77F2", "emoji": "🟣"},
    {"nombre": "Celeste", "hex": "#66D9E8", "emoji": "🩵"},
    {"nombre": "Marrón", "hex": "#C07756", "emoji": "🟤"},
    {"nombre": "Negro", "hex": "#495057", "emoji": "⚫"},
    {"nombre": "Blanco", "hex": "#F8F9FA", "emoji": "⚪"},
    {"nombre": "Gris", "hex": "#ADB5BD", "emoji": "🔘"},
]

MODO_NOMBRE = "nombre"
MODO_TOCA = "toca"


class ColoresState(rx.State):
    """Estado del juego Colores."""

    modo: str = MODO_NOMBRE
    max_rondas: int = 10

    ronda_actual: int = 0
    color_correcto: dict = {}
    opciones: list[dict] = []
    puntuacion_partida: int = 0
    aciertos_seguidos: int = 0
    juego_activo: bool = False
    juego_terminado: bool = False
    mensaje: str = ""
    mostrar_respuesta: bool = False
    ultima_correcta: bool = False

    # --- Estadísticas persistentes (backend) ---
    puntuacion_total: int = 0
    mejor_puntuacion: int = 0

    # --- Config temporales ---
    config_modo: str = MODO_NOMBRE
    config_rondas: int = 10

    def cargar_estadisticas(self):
        stats = get_game_scores("colores")
        self.puntuacion_total = stats.get("puntuacion_total", 0)
        self.mejor_puntuacion = stats.get("mejor_puntuacion", 0)

    def set_config_modo(self, value: str):
        self.config_modo = value

    def set_config_rondas(self, value: list[float]):
        self.config_rondas = int(value[0])

    def aplicar_configuracion(self):
        self.modo = self.config_modo
        self.max_rondas = self.config_rondas
        self.nueva_partida()

    def _generar_ronda(self):
        self.color_correcto = random.choice(COLORES_JUEGO)
        if self.modo == MODO_NOMBRE:
            otros = [c for c in COLORES_JUEGO if c["nombre"] != self.color_correcto["nombre"]]
            distractores = random.sample(otros, min(2, len(otros)))
            self.opciones = random.sample([self.color_correcto] + distractores, 3)
        else:
            otros = [c for c in COLORES_JUEGO if c["nombre"] != self.color_correcto["nombre"]]
            distractores = random.sample(otros, min(5, len(otros)))
            self.opciones = random.sample([self.color_correcto] + distractores, 6)
        self.mostrar_respuesta = False
        self.ultima_correcta = False
        self.mensaje = ""

    def nueva_partida(self):
        self.ronda_actual = 1
        self.puntuacion_partida = 0
        self.aciertos_seguidos = 0
        self.juego_activo = True
        self.juego_terminado = False
        self.mensaje = ""
        self._generar_ronda()

    def verificar_respuesta(self, nombre_color: str):
        if not self.juego_activo or self.mostrar_respuesta:
            return
        correcto = nombre_color == self.color_correcto["nombre"]
        self.mostrar_respuesta = True
        self.ultima_correcta = correcto
        if correcto:
            self.aciertos_seguidos += 1
            bonus_racha = self.aciertos_seguidos * 5
            puntos = 10 + bonus_racha
            self.puntuacion_partida += puntos
            self.mensaje = "¡Correcto!"
            self._acumular_puntuacion(puntos)
        else:
            self.aciertos_seguidos = 0
            self.mensaje = f"Era {self.color_correcto['nombre']}"

    def siguiente_ronda(self):
        if self.ronda_actual >= self.max_rondas:
            self.juego_activo = False
            self.juego_terminado = True
            self.mensaje = f"¡Partida terminada! Puntuación: {self.puntuacion_partida}"
            self._actualizar_mejor_puntuacion()
            return
        self.ronda_actual += 1
        self._generar_ronda()

    def _acumular_puntuacion(self, delta: int):
        """Acumula solo el delta de puntos de esta respuesta."""
        self.puntuacion_total += delta
        update_game_scores(
            "colores",
            {
                "puntuacion_total": self.puntuacion_total,
                "mejor_puntuacion": self.mejor_puntuacion,
            },
        )

    def _actualizar_mejor_puntuacion(self):
        if self.puntuacion_partida > self.mejor_puntuacion:
            self.mejor_puntuacion = self.puntuacion_partida
        update_game_scores(
            "colores",
            {
                "puntuacion_total": self.puntuacion_total,
                "mejor_puntuacion": self.mejor_puntuacion,
            },
        )

    @rx.var(cache=True)
    def progreso(self) -> str:
        return f"Ronda {self.ronda_actual} de {self.max_rondas}"

    @rx.var(cache=True)
    def progreso_pct(self) -> str:
        if self.max_rondas == 0:
            return "0%"
        pct = int(self.ronda_actual / self.max_rondas * 100)
        return f"{pct}%"
