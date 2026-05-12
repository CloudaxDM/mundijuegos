"""Persistencia de puntuaciones en backend (JSON)."""

import json
import os

SCORES_FILE = os.path.join(os.path.dirname(__file__), "..", "scores.json")

DEFAULT_SCORES = {
    "ahorcado": {
        "puntuacion_total": 0,
        "mejor_racha": 0,
        "partidas_jugadas": 0,
        "partidas_ganadas": 0,
    },
    "colores": {
        "puntuacion_total": 0,
        "mejor_puntuacion": 0,
    },
    "memoria": {
        "mejor_movimientos_facil": 0,
        "mejor_movimientos_medio": 0,
        "mejor_movimientos_dificil": 0,
        "partidas_jugadas": 0,
        "partidas_ganadas": 0,
    },
    "puzzle": {
        "mejor_mov_facil": 0,
        "mejor_mov_dificil": 0,
        "partidas_jugadas": 0,
        "partidas_ganadas": 0,
    },
}


def _ensure_file():
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_SCORES, f, indent=2, ensure_ascii=False)


def load_scores() -> dict:
    """Carga todas las puntuaciones desde disco."""
    _ensure_file()
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        data = DEFAULT_SCORES.copy()
    # Asegurar estructura completa
    for key, defaults in DEFAULT_SCORES.items():
        data.setdefault(key, {}).update(
            {k: data[key].get(k, v) for k, v in defaults.items()}
        )
    return data


def save_scores(data: dict):
    """Guarda todas las puntuaciones en disco."""
    _ensure_file()
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_game_scores(game: str) -> dict:
    """Devuelve las puntuaciones de un juego concreto."""
    all_scores = load_scores()
    return all_scores.get(game, DEFAULT_SCORES.get(game, {}))


def update_game_scores(game: str, updates: dict):
    """Actualiza campos de un juego concreto y guarda en disco."""
    all_scores = load_scores()
    all_scores.setdefault(game, {})
    all_scores[game].update(updates)
    save_scores(all_scores)
