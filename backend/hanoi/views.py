"""Vistas de la API. Solo exponen datos en JSON; no hay HTML ni UI."""
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .estructuras import (
    MAX_DISCOS,
    MIN_DISCOS,
    Pila,
    construir_torre_inicial,
    validar_cantidad_discos,
)
from .estructuras.torre import torre_a_lista


@require_GET
def health(request):
    """Comprobación rápida de que el backend está vivo."""
    return JsonResponse({"ok": True, "mensaje": "Backend de Torre de Hanói activo"})


@require_GET
def torres_iniciales(request):
    """GET /api/torres/?discos=4

    Devuelve las tres torres en su estado inicial (todo en 'origen').
    Cada torre es una lista de tamaños de BASE a TOPE.
    """
    try:
        cantidad = validar_cantidad_discos(request.GET.get("discos", MIN_DISCOS))
    except ValueError as error:
        return JsonResponse({"ok": False, "error": str(error)}, status=400)

    torres = {
        "origen": construir_torre_inicial(cantidad),
        "auxiliar": Pila(),
        "destino": Pila(),
    }

    return JsonResponse(
        {
            "ok": True,
            "cantidad_discos": cantidad,
            "rango_discos": {"min": MIN_DISCOS, "max": MAX_DISCOS},
            "torres": {nombre: torre_a_lista(t) for nombre, t in torres.items()},
        }
    )