"""Utilidades para construir las torres a partir de Pilas de Discos."""
from .disco import Disco
from .pila import Pila

# Rango permitido de discos (compatible con la interfaz).
MIN_DISCOS = 3
MAX_DISCOS = 8


def validar_cantidad_discos(cantidad) -> int:
    """Valida y devuelve la cantidad de discos como entero.

    Lanza ValueError con un mensaje claro si no es válida.
    """
    try:
        cantidad = int(cantidad)
    except (TypeError, ValueError):
        raise ValueError("La cantidad de discos debe ser un número entero.")
    if not (MIN_DISCOS <= cantidad <= MAX_DISCOS):
        raise ValueError(
            f"La cantidad de discos debe estar entre {MIN_DISCOS} y {MAX_DISCOS}."
        )
    return cantidad


def construir_torre_inicial(cantidad_discos: int) -> Pila:
    """Crea una Pila con los discos ordenados de mayor (base) a menor (tope).

    Ejemplo con 3 discos -> base: Disco(3), Disco(2), Disco(1) :tope
    """
    cantidad_discos = validar_cantidad_discos(cantidad_discos)
    torre = Pila()
    for tamanio in range(cantidad_discos, 0, -1):
        torre.push(Disco(tamanio))
    return torre


def torre_a_lista(torre: Pila) -> list:
    """Convierte una torre en lista de tamaños de base a tope. Ej: [3, 2, 1]."""
    return [disco.tamanio for disco in torre.recorrer_base_a_cima()]