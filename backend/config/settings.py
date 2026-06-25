"""
Configuración de Django para el prototipo "Mi Plan".

Pensada para desarrollo en un Codespace. NO usar tal cual en producción
(DEBUG=True, SECRET_KEY de ejemplo, CORS abierto).
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Carpeta con los archivos maestros de juguete (los JSON).
DATA_DIR = BASE_DIR / "data"

# --- Seguridad (solo para prototipo) ---
SECRET_KEY = "django-insecure-cambia-esto-en-produccion"
DEBUG = True
# Abierto para que funcione dentro del Codespace y su URL pública.
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Terceros
    "rest_framework",
    "corsheaders",
    # Propias
    "api",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Django REST Framework ---
REST_FRAMEWORK = {
    # Prototipo: sin autenticación todavía.
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
}

# --- CORS ---
# En desarrollo permitimos todo para que el frontend React se conecte sin fricción.
# Más adelante, restríngelo a la URL de tu frontend con CORS_ALLOWED_ORIGINS.
CORS_ALLOW_ALL_ORIGINS = True
