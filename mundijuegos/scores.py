"""Persistencia de puntuaciones en base de datos Reflex/SQLModel."""

import json
from copy import deepcopy
from pathlib import Path

import reflex as rx
import sqlmodel


SCORES_FILE = Path(__file__).resolve().parent.parent / "scores.json"

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


class GameScore(sqlmodel.SQLModel, table=True):
    """Fila de puntuaciones persistentes de un juego."""

    id: int | None = sqlmodel.Field(default=None, primary_key=True)
    game: str
    puntuacion_total: int = 0
    mejor_racha: int = 0
    partidas_jugadas: int = 0
    partidas_ganadas: int = 0
    mejor_puntuacion: int = 0
    mejor_movimientos_facil: int = 0
    mejor_movimientos_medio: int = 0
    mejor_movimientos_dificil: int = 0
    mejor_mov_facil: int = 0
    mejor_mov_dificil: int = 0


def _normalizar_scores(data: dict | None) -> dict:
    """Devuelve todas las claves esperadas sin mutar DEFAULT_SCORES."""
    normalizados = deepcopy(DEFAULT_SCORES)
    if not isinstance(data, dict):
        return normalizados
    for game, defaults in DEFAULT_SCORES.items():
        valores = data.get(game, {})
        if isinstance(valores, dict):
            normalizados[game].update(
                {key: int(valores.get(key, default)) for key, default in defaults.items()}
            )
    return normalizados


def _load_json_scores() -> dict:
    """Importa puntuaciones antiguas desde scores.json si existe."""
    if not SCORES_FILE.exists():
        return deepcopy(DEFAULT_SCORES)
    try:
        with SCORES_FILE.open("r", encoding="utf-8") as file:
            return _normalizar_scores(json.load(file))
    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        return deepcopy(DEFAULT_SCORES)


def _score_to_dict(score: GameScore) -> dict:
    """Convierte una fila de base de datos al dict esperado por cada State."""
    data = {
        "puntuacion_total": score.puntuacion_total,
        "mejor_racha": score.mejor_racha,
        "partidas_jugadas": score.partidas_jugadas,
        "partidas_ganadas": score.partidas_ganadas,
        "mejor_puntuacion": score.mejor_puntuacion,
        "mejor_movimientos_facil": score.mejor_movimientos_facil,
        "mejor_movimientos_medio": score.mejor_movimientos_medio,
        "mejor_movimientos_dificil": score.mejor_movimientos_dificil,
        "mejor_mov_facil": score.mejor_mov_facil,
        "mejor_mov_dificil": score.mejor_mov_dificil,
    }
    return {key: data.get(key, value) for key, value in DEFAULT_SCORES[score.game].items()}


def _get_or_create_score(session, game: str) -> GameScore:
    """Obtiene la fila de un juego o la crea importando datos del JSON antiguo."""
    score = session.exec(sqlmodel.select(GameScore).where(GameScore.game == game)).first()
    if score is not None:
        return score

    json_scores = _load_json_scores()
    defaults = json_scores.get(game, DEFAULT_SCORES.get(game, {}))
    score = GameScore(game=game, **defaults)
    session.add(score)
    session.commit()
    session.refresh(score)
    return score


def load_scores() -> dict:
    """Carga todas las puntuaciones desde la base de datos."""
    with rx.session() as session:
        return {
            game: _score_to_dict(_get_or_create_score(session, game))
            for game in DEFAULT_SCORES
        }


def save_scores(data: dict):
    """Guarda todas las puntuaciones en la base de datos."""
    data = _normalizar_scores(data)
    with rx.session() as session:
        for game, values in data.items():
            score = _get_or_create_score(session, game)
            for key, value in values.items():
                setattr(score, key, value)
            session.add(score)
        session.commit()


def get_game_scores(game: str) -> dict:
    """Devuelve las puntuaciones de un juego concreto."""
    if game not in DEFAULT_SCORES:
        return {}
    with rx.session() as session:
        return _score_to_dict(_get_or_create_score(session, game))


def update_game_scores(game: str, updates: dict):
    """Actualiza campos de un juego concreto y guarda en base de datos."""
    if game not in DEFAULT_SCORES:
        return
    valid_updates = {
        key: int(value)
        for key, value in updates.items()
        if key in DEFAULT_SCORES[game]
    }
    with rx.session() as session:
        score = _get_or_create_score(session, game)
        for key, value in valid_updates.items():
            setattr(score, key, value)
        session.add(score)
        session.commit()
