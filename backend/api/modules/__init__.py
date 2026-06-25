"""
Al importar este paquete se cargan todos los módulos, y cada uno se inscribe
solo en el registro gracias al decorador @register.

El ORDEN de estos imports define el orden en que aparecen en el sidebar.
"""
from . import resultado_del_plan  # noqa: F401  (Módulo 1)
from . import prevencion          # noqa: F401  (Módulo 2)
from . import informacion_ayuda   # noqa: F401  (Módulo 3)
