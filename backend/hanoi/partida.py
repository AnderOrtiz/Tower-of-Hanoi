"""Almacén en memoria de partidas: {partida_id: JuegoHanoi}.

Django no recuerda nada entre peticiones, así que guardamos los juegos
en un diccionario a nivel de módulo. Sirve con `runserver` (un solo proceso);
si se usaran varios workers cada uno tendría su propio diccionario.
"""
import uuid
from threading import Lock

from .juego import JuegoHanoi

_partidas = {}
_lock = Lock()


class PartidaNoEncontrada(Exception):
    """El partida_id no existe."""


def crear_partida(discos):
    """Crea una partida nueva y devuelve (partida_id, juego).

    Lanza ValueError si la cantidad de discos no es válida (3 a 8).
    """
    juego = JuegoHanoi(discos)
    partida_id = uuid.uuid4().hex
    with _lock:
        _partidas[partida_id] = juego
    return partida_id, juego


def obtener_partida(partida_id):
    with _lock:
        try:
            return _partidas[partida_id]
        except KeyError:
            raise PartidaNoEncontrada(f"No existe la partida '{partida_id}'.")


def reiniciar_partida(partida_id):
    juego = obtener_partida(partida_id)
    juego.reiniciar()
    return juego


def eliminar_partida(partida_id):
    with _lock:
        _partidas.pop(partida_id, None)


def limpiar_partidas():
    """Útil en las pruebas."""
    with _lock:
        _partidas.clear()