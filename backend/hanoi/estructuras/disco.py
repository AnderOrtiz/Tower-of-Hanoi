"""Representación de un disco de la Torre de Hanói."""
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Disco:
    """Disco inmutable. Se compara por tamaño (1 = el más pequeño).

    Gracias a order=True se puede escribir: disco_a > disco_b
    """

    tamanio: int

    def __post_init__(self) -> None:
        if not isinstance(self.tamanio, int) or self.tamanio < 1:
            raise ValueError("El tamaño del disco debe ser un entero mayor o igual a 1.")

    def a_dict(self) -> dict:
        """Formato listo para serializar a JSON."""
        return {"tamanio": self.tamanio}

    def __str__(self) -> str:
        return f"Disco({self.tamanio})"