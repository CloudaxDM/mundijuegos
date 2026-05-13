"""Estado y lógica del módulo El Ahorcado (Flor)."""

import random
import string
import reflex as rx
from mundijuegos.scores import get_game_scores, update_game_scores


# ============================================================
# BANCO DE PALABRAS - 100 palabras en español para niños
# Todas sin tildes para facilitar la lectura
# ============================================================

PALABRAS = [
    "GATO", "PERRO", "OSO", "CONEJO", "PEZ", "PAJARO", "MARIPOSA", "ABEJA",
    "ELEFANTE", "JIRAFA", "LEON", "TIGRE", "CEBRA", "CABALLO", "VACA",
    "GALLINA", "PATO", "RATON", "LOBO", "RANA",
    "MANZANA", "PLATANO", "UVA", "FRESA", "NARANJA", "PERA", "MELOCOTON",
    "SANDIA", "CEREZA", "LIMON", "PIZZA", "TARTA", "HELADO", "CHOCOLATE",
    "GALLETA", "LECHE", "PAN", "QUESO", "YOGUR", "MIEL",
    "ROJO", "AZUL", "VERDE", "AMARILLO", "ROSA", "MORADO", "NARANJA",
    "BLANCO", "NEGRO", "GRIS",
    "MANO", "PIE", "CABEZA", "BRAZO", "PIERNA", "OJO", "NARIZ", "BOCA",
    "OREJA", "DEDO",
    "CASA", "MESA", "SILLA", "PUERTA", "VENTANA", "CAMA", "LAMPARA",
    "JUGUETE", "PELOTA", "LIBRO", "LAPIZ", "MOCHILA", "RELOJ", "ESPEJO",
    "ALMOHADA",
    "SOL", "LUNA", "ESTRELLA", "NUBE", "FLOR", "ARBOL", "HOJA", "MAR",
    "ARENA", "MONTANA",
    "MAMA", "PAPA", "ABUELA", "ABUELO", "HERMANA", "BEBE", "AMIGA",
    "MAESTRA", "DOCTOR", "BAILARINA",
    "AMOR", "RISA", "JUEGO", "SUENO", "BESO",
]


class AhorcadoState(rx.State):
    """Estado del juego El Ahorcado."""

    # --- Configuración ---
    intentos_maximos: int = 6
    longitud_min: int = 4
    longitud_max: int = 15

    # --- Estado del juego ---
    palabra: str = ""
    letras_adivinadas: list[str] = []
    letras_falladas: list[str] = []
    intentos_restantes: int = 6
    juego_activo: bool = False
    juego_ganado: bool = False
    juego_perdido: bool = False
    puntuacion_partida: int = 0
    racha_actual: int = 0
    mensaje: str = ""

    # --- Estadísticas persistentes (backend) ---
    puntuacion_total: int = 0
    mejor_racha: int = 0
    partidas_jugadas: int = 0
    partidas_ganadas: int = 0

    # --- Config sliders ---
    config_intentos: int = 6
    config_min: int = 4
    config_max: int = 10

    def cambiar_config_intentos(self, value: list[float]):
        self.config_intentos = int(value[0])

    def cambiar_config_min(self, value: list[float]):
        self.config_min = int(value[0])

    def cambiar_config_max(self, value: list[float]):
        self.config_max = int(value[0])

    def cargar_estadisticas(self):
        stats = get_game_scores("ahorcado")
        self.puntuacion_total = stats.get("puntuacion_total", 0)
        self.mejor_racha = stats.get("mejor_racha", 0)
        self.partidas_jugadas = stats.get("partidas_jugadas", 0)
        self.partidas_ganadas = stats.get("partidas_ganadas", 0)

    def aplicar_configuracion(self):
        self.intentos_maximos = self.config_intentos
        self.longitud_min = min(self.config_min, self.config_max)
        self.longitud_max = max(self.config_min, self.config_max)
        self.config_min = self.longitud_min
        self.config_max = self.longitud_max
        self.nueva_partida()

    def _filtrar_palabras(self) -> list[str]:
        palabras = [p for p in PALABRAS if self.longitud_min <= len(p) <= self.longitud_max]
        return palabras if palabras else PALABRAS

    def nueva_partida(self):
        candidatas = self._filtrar_palabras()
        self.palabra = random.choice(candidatas)
        self.letras_adivinadas = []
        self.letras_falladas = []
        self.intentos_restantes = self.intentos_maximos
        self.juego_activo = True
        self.juego_ganado = False
        self.juego_perdido = False
        self.puntuacion_partida = 0
        self.mensaje = ""

    def adivinar_letra(self, letra: str):
        letra = letra.upper()
        if not self.juego_activo or len(letra) != 1 or letra not in string.ascii_uppercase:
            return
        if letra in self.letras_adivinadas or letra in self.letras_falladas:
            return
        if letra in self.palabra:
            self.letras_adivinadas = [*self.letras_adivinadas, letra]
            self._comprobar_victoria()
        else:
            self.letras_falladas = [*self.letras_falladas, letra]
            self.intentos_restantes -= 1
            self._comprobar_derrota()

    def _comprobar_victoria(self):
        if all(l in self.letras_adivinadas for l in self.palabra):
            self.juego_activo = False
            self.juego_ganado = True
            self.racha_actual += 1
            self._calcular_puntuacion(ganada=True)
            self.mensaje = "¡GANASTE! ¡Eres genial!"
            self._guardar_estadisticas(ganada=True)

    def _comprobar_derrota(self):
        if self.intentos_restantes <= 0:
            self.juego_activo = False
            self.juego_perdido = True
            self.racha_actual = 0
            self.puntuacion_partida = 0
            self.mensaje = f"¡Casi! La palabra era: {self.palabra}"
            self._guardar_estadisticas(ganada=False)

    def _calcular_puntuacion(self, ganada: bool):
        if not ganada:
            return
        base = 100
        bonus_intentos = self.intentos_restantes * 20
        bonus_racha = self.racha_actual * 10
        penalizacion = len(self.letras_falladas) * 5
        total = base + bonus_intentos + bonus_racha - penalizacion
        self.puntuacion_partida = max(total, 10)

    def _guardar_estadisticas(self, ganada: bool):
        self.puntuacion_total += self.puntuacion_partida
        self.partidas_jugadas += 1
        if ganada:
            self.partidas_ganadas += 1
        if self.racha_actual > self.mejor_racha:
            self.mejor_racha = self.racha_actual
        update_game_scores(
            "ahorcado",
            {
                "puntuacion_total": self.puntuacion_total,
                "mejor_racha": self.mejor_racha,
                "partidas_jugadas": self.partidas_jugadas,
                "partidas_ganadas": self.partidas_ganadas,
            },
        )

    def rendirse(self):
        if self.juego_activo:
            self.juego_activo = False
            self.juego_perdido = True
            self.racha_actual = 0
            self.puntuacion_partida = 0
            self.mensaje = f"La palabra era: {self.palabra}"
            self._guardar_estadisticas(ganada=False)

    @rx.var(cache=True)
    def palabra_mostrada(self) -> str:
        if not self.palabra:
            return ""
        return " ".join(letra if letra in self.letras_adivinadas else "_" for letra in self.palabra)

    @rx.var(cache=True)
    def total_petalos(self) -> int:
        return self.intentos_maximos

    @rx.var(cache=True)
    def petalos_restantes(self) -> int:
        return self.intentos_restantes

    @rx.var(cache=True)
    def petalos_perdidos(self) -> int:
        return self.intentos_maximos - self.intentos_restantes

    @rx.var(cache=True)
    def petalos_indices(self) -> list[int]:
        return list(range(self.intentos_maximos))

    @rx.var(cache=True)
    def texto_petalos(self) -> str:
        if self.juego_activo:
            return f"Pétalos restantes: {self.intentos_restantes}"
        if self.juego_ganado:
            return "¡La flor está feliz!"
        return "La flor perdió sus pétalos..."
