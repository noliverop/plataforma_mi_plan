# Backend — Mi Plan

API en Django + DRF que sirve los datos del prototipo.

## Correr

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Endpoints

| Método | Ruta | Qué entrega |
| --- | --- | --- |
| GET | `/api/profile/` | Perfil del afiliado (sidebar) |
| GET | `/api/modules/` | Lista de módulos (menú del sidebar) |
| GET | `/api/modules/<id>/` | Datos completos de un módulo |

## Estructura

```
backend/
  config/            Proyecto Django (settings, urls, wsgi/asgi)
  api/
    registry.py      BaseModule + registro de módulos
    data_provider.py Capa de datos (JSON hoy, BD mañana)
    views.py         Los 3 endpoints
    urls.py          Rutas de la API
    modules/         Un archivo por módulo (cada uno se registra solo)
      resultado_del_plan.py   Módulo 1
  data/              Archivos maestros de juguete (JSON)
```

## Agregar un módulo nuevo

1. Crea `api/modules/mi_modulo.py` con una clase que herede de `BaseModule`,
   define `id`/`title`/`pregunta_central`/`icon` y el método `build()`.
2. Decórala con `@register`.
3. Impórtala en `api/modules/__init__.py`.

Aparece sola en `/api/modules/` (y por lo tanto en el sidebar). No tocas nada más.
