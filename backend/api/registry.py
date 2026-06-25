"""
Registro de módulos.

Este es el corazón de la escalabilidad que pediste. Cada módulo de "Mi Plan"
(Resultado del plan, Prevención, Información y ayuda, y los que vengan) es una
clase autocontenida que sabe:

  - su identidad (id, título, pregunta central, ícono para el sidebar),
  - cómo construir su propio payload a partir del DataProvider.

Para agregar un módulo nuevo en el futuro:
  1. Creas una clase que herede de `BaseModule` en api/modules/.
  2. La decoras con @register.
  3. Listo. Aparece sola en el sidebar y en la API. No tocas nada más.
"""
from abc import ABC, abstractmethod

from .data_provider import DataProvider


class BaseModule(ABC):
    # Estos atributos los define cada módulo concreto.
    id: str = ""
    title: str = ""
    pregunta_central: str = ""
    icon: str = "ti-layout-dashboard"  # nombre de ícono Tabler para el sidebar

    @abstractmethod
    def build(self, contrato_id: str, provider: DataProvider) -> dict:
        """Arma y devuelve los datos que consumirá el frontend para este módulo."""

    def meta(self) -> dict:
        """Lo mínimo que el sidebar necesita para listar el módulo."""
        return {
            "id": self.id,
            "title": self.title,
            "pregunta_central": self.pregunta_central,
            "icon": self.icon,
        }


# --- El registro en sí ---------------------------------------------------

_REGISTRY: dict[str, BaseModule] = {}


def register(module_cls):
    """Decorador que inscribe un módulo en el registro."""
    instance = module_cls()
    if not instance.id:
        raise ValueError(f"{module_cls.__name__} no definió un 'id'.")
    _REGISTRY[instance.id] = instance
    return module_cls


def all_modules() -> list[BaseModule]:
    return list(_REGISTRY.values())


def get_module(module_id: str) -> BaseModule | None:
    return _REGISTRY.get(module_id)
