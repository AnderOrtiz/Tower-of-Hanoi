# Tower of Hanoi

## 1. Clonar el repositorio

```bash
git clone https://github.com/AnderOrtiz/Tower-of-Hanoi.git
cd Tower-of-Hanoi
```

## 2. Crear y activar el entorno (Miniconda)

Crea el entorno incluyendo `pip` y Python desde el inicio para evitar errores de comandos no encontrados:

```bash
conda create -n Django python pip -y
conda activate Django
```

## 3. Instalar dependencias

Con el entorno `(Django)` activo, instala los paquetes ubicados dentro de `backend`:

```bash
pip install -r backend/requirements.txt
```

## 4. Ejecutar el servidor

Inicia el servidor de desarrollo:

```bash
python backend/manage.py runserver
# python manage.py runserver
```

## 5. Verificar funcionamiento

Abre tu navegador o realiza una petición a la siguiente ruta para confirmar que la API responde correctamente:

```bash
http://127.0.0.1:8000/api/health/
```