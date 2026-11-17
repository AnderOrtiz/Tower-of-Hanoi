"""Implementación de una Pila (Stack) con comportamiento LIFO.

¿Por qué una pila para las torres de Hanói?
    En cada torre solo se puede tocar el disco de arriba: el último que entró
    es el primero que sale (LIFO). Eso es exactamente una pila.

Complejidad:
    push, pop, peek, esta_vacia, tamanio -> O(1)  (amortizado en push/pop)
    recorrido                            -> O(n)
"""
from typing import Any, Iterator, List


class PilaVaciaError(Exception):
    """Se lanza al intentar leer o sacar un elemento de una pila vacía."""


class Pila:
    """Pila genérica. El tope es el último elemento apilado."""

    def __init__(self) -> None:
        # Lista interna: la base está en el índice 0 y el tope al final.
        self._elementos: List[Any] = []

    # ---------- Operaciones principales ----------
    def push(self, elemento: Any) -> None:
        """Apila un elemento en el tope. O(1)."""
        self._elementos.append(elemento)

    def pop(self) -> Any:
        """Quita y devuelve el elemento del tope. O(1).

        Lanza PilaVaciaError si la pila está vacía.
        """
        if self.esta_vacia():
            raise PilaVaciaError("La pila está vacía: no hay nada que sacar.")
        return self._elementos.pop()

    def peek(self) -> Any:
        """Devuelve el elemento del tope SIN quitarlo. O(1).

        Lanza PilaVaciaError si la pila está vacía.
        """
        if self.esta_vacia():
            raise PilaVaciaError("La pila está vacía: no hay tope que consultar.")
        return self._elementos[-1]

    def esta_vacia(self) -> bool:
        """True si no tiene elementos. O(1)."""
        return len(self._elementos) == 0

    def tamanio(self) -> int:
        """Cantidad de elementos apilados. O(1)."""
        return len(self._elementos)

    # ---------- Recorrido (para dibujar) ----------
    def recorrer_base_a_cima(self) -> Iterator[Any]:
        """Itera desde la base hasta el tope sin modificar la pila. O(n)."""
        yield from self._elementos

    def recorrer_cima_a_base(self) -> Iterator[Any]:
        """Itera desde el tope hasta la base sin modificar la pila. O(n)."""
        yield from reversed(self._elementos)

    def a_lista(self) -> List[Any]:
        """Copia de los elementos de base a tope (ideal para enviar al frontend)."""
        return list(self._elementos)

    # ---------- Métodos especiales ----------
    def __len__(self) -> int:
        return self.tamanio()

    def __iter__(self) -> Iterator[Any]:
        return self.recorrer_base_a_cima()

    def __repr__(self) -> str:
        return f"Pila({self._elementos!r})"