"""
Capa de acceso a datos.

Aquí vive la abstracción que te permite, HOY, leer archivos JSON de juguete y,
MAÑANA, conectar las bases de datos reales (los "archivos maestros") sin tocar
ni la lógica de los módulos ni la API.

La idea:
  - `DataProvider` define QUÉ datos necesita el sistema (la interfaz).
  - `JSONDataProvider` define CÓMO se obtienen hoy (leyendo /data/*.json).
  - El día de mañana creas un `DBDataProvider(DataProvider)` que lea de la BD
    real, y solo cambias una línea en settings (DATA_PROVIDER). Nada más.
"""
from abc import ABC, abstractmethod
import json
from functools import lru_cache
from pathlib import Path

from django.conf import settings


class DataProvider(ABC):
    """Contrato que cualquier fuente de datos debe cumplir.

    Cada método responde por un "archivo maestro" del documento original.
    """

    @abstractmethod
    def get_contrato(self, contrato_id: str) -> dict:
        """VAL_CONTRATOS: datos del contrato y la cotización pactada."""

    @abstractmethod
    def get_integrantes(self, contrato_id: str) -> dict:
        """FA_COTIZANTE / FA_CARGAS: cotizante y cargas del contrato."""

    @abstractmethod
    def get_prestaciones_bonificadas(self, contrato_id: str) -> list:
        """VAL_PRESTACIONES_BONIFICADAS: prestaciones del período."""

    @abstractmethod
    def get_licencias_medicas(self, contrato_id: str) -> list:
        """VAL_LICENCIA_MEDICA_CIRC69: licencias del período."""

    @abstractmethod
    def get_red_prestadores(self) -> list:
        """Red de prestadores donde realizar exámenes (solicitud a la Isapre)."""

    @abstractmethod
    def get_glosario(self) -> list:
        """Glosario simple (fuente: Superintendencia de Salud)."""

    @abstractmethod
    def get_beneficios(self) -> list:
        """Beneficios y derechos disponibles (fuente: Superintendencia)."""


class JSONDataProvider(DataProvider):
    """Implementación de juguete: lee los JSON de la carpeta /data.

    Usa un cache en memoria para no abrir el archivo en cada request. Como los
    JSON no cambian en caliente durante el prototipo, esto es seguro y rápido.
    """

    def __init__(self, data_dir: Path | None = None):
        self.data_dir = Path(data_dir or settings.DATA_DIR)

    @lru_cache(maxsize=None)
    def _load(self, filename: str):
        path = self.data_dir / filename
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)

    def get_contrato(self, contrato_id: str) -> dict:
        return self._load("val_contratos.json").get(contrato_id, {})

    def get_integrantes(self, contrato_id: str) -> dict:
        return self._load("fa_cotizante.json").get(contrato_id, {})

    def get_prestaciones_bonificadas(self, contrato_id: str) -> list:
        return self._load("val_prestaciones_bonificadas.json").get(contrato_id, [])

    def get_licencias_medicas(self, contrato_id: str) -> list:
        return self._load("val_licencia_medica.json").get(contrato_id, [])

    def get_red_prestadores(self) -> list:
        return self._load("red_prestadores.json")

    def get_glosario(self) -> list:
        return self._load("glosario.json")

    def get_beneficios(self) -> list:
        return self._load("beneficios.json")


# Mañana, para conectar la BD real, basta con algo como:
#
#   class DBDataProvider(DataProvider):
#       def get_contrato(self, contrato_id): ...consulta tu modelo/SQL...
#
# y apuntar settings.DATA_PROVIDER a esa clase. La API y los módulos no cambian.


def get_provider() -> DataProvider:
    """Devuelve el proveedor de datos activo según la configuración."""
    return JSONDataProvider()
