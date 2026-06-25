"""
Módulo 3 — Información y ayuda.

Pregunta central: ¿Cómo entender mi Plan?

  3.1 Glosario simple.
  3.2 Beneficios y derechos disponibles.

Ambos vienen de contenido de referencia (en el producto real, de la
Superintendencia de Salud). Por eso este módulo no depende del contrato:
entrega el mismo material a cualquier afiliado.
"""
from ..data_provider import DataProvider
from ..registry import BaseModule, register


@register
class InformacionAyudaModule(BaseModule):
    id = "informacion-ayuda"
    title = "Información y ayuda"
    pregunta_central = "¿Cómo entender mi Plan?"
    icon = "ti-help-circle"

    def build(self, contrato_id: str, provider: DataProvider) -> dict:
        return {
            "glosario": provider.get_glosario(),
            "beneficios": provider.get_beneficios(),
        }
