"""Configuración de Django para el backend de la Torre de Hanói."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "cambiar-esto-en-produccion-hanoi-dev-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "corsheaders",   # Permite que el frontend (otro puerto) consuma la API
    "hanoi",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Debe ir primero
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# El juego no necesita base de datos; esto solo evita warnings.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# CORS: en desarrollo se permite cualquier origen.
CORS_ALLOW_ALL_ORIGINS = True

LANGUAGE_CODE = "es"
TIME_ZONE = "America/El_Salvador"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"