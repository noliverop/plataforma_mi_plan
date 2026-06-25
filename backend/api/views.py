"""
Vistas de la API.

Tres endpoints, todos pensados para que el frontend sea data-driven:

  GET /api/profile/        -> datos del afiliado para el sidebar
  GET /api/modules/        -> lista de módulos (alimenta el menú del sidebar)
  GET /api/modules/<id>/   -> payload completo de un módulo

Nota sobre autenticación: en el prototipo NO hay login real. Usamos un
"contrato demo" fijo (CONTRATO_DEMO). Cuando conectes autenticación real, el
contrato saldrá del usuario logueado en vez de esta constante.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .data_provider import get_provider
from .registry import all_modules, get_module

# Mientras no haya login real, todo cuelga de este contrato de demostración.
CONTRATO_DEMO = "CONTRATO-001"


@api_view(["GET"])
def profile(request):
    """Perfil del afiliado para el encabezado del sidebar."""
    provider = get_provider()
    integrantes = provider.get_integrantes(CONTRATO_DEMO)
    cotizante = integrantes.get("cotizante", {})
    return Response(
        {
            "nombre": cotizante.get("nombre"),
            "rut": cotizante.get("rut"),
            "email": cotizante.get("email"),
            "contrato_id": CONTRATO_DEMO,
        }
    )


@api_view(["GET"])
def module_list(request):
    """Lista de módulos disponibles. El sidebar se construye con esto."""
    return Response([m.meta() for m in all_modules()])


@api_view(["GET"])
def module_detail(request, module_id):
    """Datos completos de un módulo para renderizar su vista."""
    module = get_module(module_id)
    if module is None:
        return Response({"detail": "Módulo no encontrado."}, status=404)

    provider = get_provider()
    data = module.build(CONTRATO_DEMO, provider)
    return Response({**module.meta(), "data": data})
