"""
Al importar este paquete se cargan todos los módulos, y cada uno se inscribe
solo en el registro gracias al decorador @register.

Cuando agregues un módulo nuevo, impórtalo aquí (una línea) y queda activo.
"""
from . import resultado_del_plan  # noqa: F401

# from . import prevencion          # Módulo 2 (futuro)
# from . import informacion_ayuda   # Módulo 3 (futuro)
