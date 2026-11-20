from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("torres/", views.torres_iniciales, name="torres_iniciales"),
    path("partidas/", views.crear_partida, name="crear_partida"),
    path("partidas/<str:partida_id>/", views.estado_partida, name="estado_partida"),
    path("partidas/<str:partida_id>/mover/", views.mover, name="mover"),
    path("partidas/<str:partida_id>/reiniciar/", views.reiniciar, name="reiniciar"),
]