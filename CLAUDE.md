# Mi Plan — Plataforma del afiliado

## Qué es esto

"Mi Plan" es una plataforma **a nivel individual** que le muestra a una persona
afiliada a una Isapre, en lenguaje simple, el resultado de su plan de salud. La
**unidad de análisis es el contrato de salud**.

Estado actual: **prototipo**. Los datos son de juguete (archivos JSON); todavía
no hay conexión a las bases de datos reales ni autenticación real.

## Cómo trabajamos en este repo (importante)

Este proyecto es también un espacio de aprendizaje. Cuando hagas un cambio:

- **Explica el qué y el porqué**, no solo el código. Señala el concepto detrás
  (por qué este patrón, qué problema evita) para que la persona pueda
  reproducirlo por su cuenta y no pierda la práctica de programar.
- Prefiere cambios pequeños y comprensibles sobre soluciones "mágicas".
- Comenta el código en español cuando aclare la intención.

## Stack

- **Backend:** Django 5 + Django REST Framework. Sirve una API JSON.
- **Frontend:** React (pendiente). Consumirá la API. Idioma de la UI: español (Chile).

## Arquitectura: módulos escalables

El producto crece por **módulos**, cada uno anclado a una pregunta del usuario:

- Módulo 1 — Resultado de mi plan: *¿Cuál es el resultado de mi plan en términos simples?* (implementado)
- Módulo 2 — Prevención: *¿Tengo exámenes gratuitos pendientes?* (implementado)
- Módulo 3 — Información y ayuda: *¿Cómo entender mi Plan?* (implementado)

El diseño está pensado para que **agregar un módulo no obligue a tocar el resto**:

- `backend/api/registry.py` — define `BaseModule` y un registro. Cada módulo es
  una clase autocontenida que se inscribe sola con el decorador `@register`.
- `backend/api/modules/` — un archivo por módulo. Para sumar uno nuevo: crear la
  clase, decorarla con `@register`, e importarla en `modules/__init__.py`.
- `backend/api/data_provider.py` — capa de datos abstracta. Hoy lee JSON
  (`JSONDataProvider`); el día que se conecte la BD real se crea un
  `DBDataProvider` y **no cambia nada más** (ni módulos ni API).

### API (data-driven, para que el frontend se arme solo)

- `GET /api/profile/` — datos del afiliado (encabezado del sidebar).
- `GET /api/modules/` — lista de módulos. **El sidebar se construye con esto**:
  cada módulo trae `id`, `title`, `pregunta_central` e `icon`.
- `GET /api/modules/<id>/` — payload completo de un módulo para renderizar su vista.

## Frontend (implementado)

`frontend/` — app React con Vite. Layout con **sidebar** (perfil del afiliado,
navegación entre módulos alimentada por `GET /api/modules/`, y logout simulado).
El área principal muestra el módulo activo.

Espeja la escalabilidad del backend con su propio registro
(`src/modules/registry.js`): mapea cada id de módulo a su componente. Si un
módulo existe en el backend pero aún no tiene componente, la app muestra
"próximamente". Diseño: el veredicto del semáforo en lenguaje humano es el
protagonista (no los números); divulgación progresiva para el desglose pesado.

La conexión al backend usa el proxy de Vite (`/api` → `http://127.0.0.1:8000`),
así que no hay CORS ni URLs del Codespace escritas a mano.

### Cómo correr el frontend

```bash
cd frontend
npm install
npm run dev     # arranca en el puerto 5173
```

Con el backend corriendo en 8000 y el frontend en 5173, abre el puerto 5173 que
te ofrece el Codespace.

## Autenticación

En el prototipo **no hay login real**. Todo cuelga de un contrato demo
(`CONTRATO-001`, constante `CONTRATO_DEMO` en `api/views.py`). Al integrar
autenticación, el contrato saldrá del usuario logueado en lugar de esa constante.

## Cómo correr el backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Luego: `curl http://127.0.0.1:8000/api/modules/`
