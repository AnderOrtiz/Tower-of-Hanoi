# Backend: Torre de Hanói (Django API)

API en Django que maneja **solo la lógica** del juego. La interfaz vive en el frontend y se comunica con este backend por JSON.

## Requisitos

- Python 3.12 o superior
- Git
- (Opcional) Si usas conda, ejecuta `conda deactivate` antes de empezar para evitar mezclar entornos.

## Instalación (primera vez)

Desde la raíz del repositorio:

```bash
cd backend
python3 -m venv venv
```

Activa el entorno virtual:

```bash
# Linux / macOS
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat
```

Instala las dependencias (usa siempre `python -m pip`, así se instala en el venv correcto):

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Levantar el servidor

```bash
python manage.py runserver
```

La API queda disponible en: **http://127.0.0.1:8000/api/**

Para usar otro puerto: `python manage.py runserver 8080`

## Verificar que funciona

```bash
curl http://127.0.0.1:8000/api/health/
curl "http://127.0.0.1:8000/api/torres/?discos=4"
```

Respuesta esperada de `/api/torres/?discos=4`:

```json
{
  "ok": true,
  "cantidad_discos": 4,
  "rango_discos": { "min": 3, "max": 8 },
  "torres": {
    "origen":   [4, 3, 2, 1],
    "auxiliar": [],
    "destino":  []
  }
}
```

Cada torre es una lista **de la base al tope** (el último elemento es el disco de arriba).

## Endpoints disponibles

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/health/` | Comprueba que el backend está activo |
| GET | `/api/torres/?discos=N` | Estado inicial de las torres (N entre 3 y 8) |

Si `discos` es inválido, responde `400` con `{"ok": false, "error": "mensaje"}`.

## Ejecutar las pruebas

```bash
python manage.py test
# Con más detalle (útil para guardar evidencias):
python manage.py test -v 2
```

## Estructura del proyecto

```
backend/
├── manage.py
├── requirements.txt
├── config/            # Configuración de Django (settings, urls)
├── hanoi/
│   ├── estructuras/   # Pila, Disco, torre inicial (Integrante 1)
│   ├── tests/         # Pruebas unitarias
│   ├── urls.py        # Rutas de la API
│   └── views.py       # Endpoints (solo devuelven JSON)
└── docs/              # Documentación técnica
```

## Para el frontend

- CORS está habilitado: puedes consumir la API desde cualquier puerto (`localhost:3000`, `5173`, etc.).
- Ejemplo con `fetch`:

```javascript
const res = await fetch("http://127.0.0.1:8000/api/torres/?discos=4");
const data = await res.json();
console.log(data.torres.origen); // [4, 3, 2, 1]
```

## Problemas comunes

| Error | Solución |
|---|---|
| `No module named 'django'` | Activa el venv y ejecuta `python -m pip install -r requirements.txt` |
| `No module named 'hanoi.estructuras'` | Falta algún archivo o `__init__.py` en `hanoi/estructuras/` |
| `Address already in use` | Usa otro puerto: `python manage.py runserver 8001` |
| Mezcla de conda y venv | Ejecuta `conda deactivate` y vuelve a activar el venv |