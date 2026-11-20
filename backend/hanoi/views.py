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

# ---------------------------------------------------------------------------
# Partidas (el juego completo: crear, consultar, mover, reiniciar)
# ---------------------------------------------------------------------------
import json

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from . import partida as almacen


def _leer_json(request):
    """Devuelve el cuerpo JSON como dict, o None si no es un JSON válido."""
    try:
        datos = json.loads(request.body or b"{}")
    except (ValueError, UnicodeDecodeError):
        return None
    return datos if isinstance(datos, dict) else None


def _error(mensaje, status):
    return JsonResponse({"ok": False, "mensaje": mensaje}, status=status)


def _respuesta(partida_id, juego, ok=True, mensaje="", status=200):
    """Forma común de respuesta que consume el frontend."""
    datos = juego.resumen()
    return JsonResponse(
        {
            "ok": ok,
            "mensaje": mensaje,
            "id": partida_id,
            "cantidad_discos": datos["discos"],
            "torres": datos["torres"],
            "movimientos": datos["movimientos"],
            "minimo_teorico": datos["minimo_teorico"],
            "victoria": datos["victoria"],
        },
        status=status,
    )


@csrf_exempt
@require_POST
def crear_partida(request):
    """POST /api/partidas/   cuerpo: {"discos": 4}"""
    datos = _leer_json(request)
    if datos is None:
        return _error("El cuerpo debe ser un JSON válido.", 400)
    try:
        partida_id, juego = almacen.crear_partida(datos.get("discos"))
    except (ValueError, TypeError) as error:
        return _error(str(error), 400)
    return _respuesta(partida_id, juego, mensaje="Partida creada.", status=201)


@require_GET
def estado_partida(request, partida_id):
    """GET /api/partidas/<id>/"""
    try:
        juego = almacen.obtener_partida(partida_id)
    except almacen.PartidaNoEncontrada as error:
        return _error(str(error), 404)
    return _respuesta(partida_id, juego)


@csrf_exempt
@require_POST
def mover(request, partida_id):
    """POST /api/partidas/<id>/mover/   cuerpo: {"origen": "origen", "destino": "destino"}"""
    try:
        juego = almacen.obtener_partida(partida_id)
    except almacen.PartidaNoEncontrada as error:
        return _error(str(error), 404)

    datos = _leer_json(request)
    if datos is None:
        return _error("El cuerpo debe ser un JSON válido.", 400)

    # La validación de reglas la hace JuegoHanoi.mover(); aquí no se repite.
    resultado = juego.mover(datos.get("origen"), datos.get("destino"))
    return _respuesta(
        partida_id,
        juego,
        ok=resultado["ok"],
        mensaje=resultado["mensaje"],
        status=200 if resultado["ok"] else 400,
    )


@csrf_exempt
@require_POST
def reiniciar(request, partida_id):
    """POST /api/partidas/<id>/reiniciar/"""
    try:
        juego = almacen.reiniciar_partida(partida_id)
    except almacen.PartidaNoEncontrada as error:
        return _error(str(error), 404)
    return _respuesta(partida_id, juego, mensaje="Partida reiniciada.")