"""
Módulo 2 — Prevención.

Pregunta central: ¿Tengo exámenes gratuitos pendientes?

  2.1 Estado preventivo del contrato: para cada integrante adulto, según su edad
      y sexo, qué exámenes del EMP (Examen de Medicina Preventiva) le
      corresponden. Nota del documento: NO se verifica si ya se los hizo; solo se
      informa qué le toca.
  2.2 ¿Dónde realizarlos?: red de prestadores disponibles.
"""
from ..data_provider import DataProvider
from ..registry import BaseModule, register

# Reglas del EMP, como datos. Cada regla dice qué examen corresponde a qué
# población objetivo (rango de edad y sexo). Tenerlas así, declarativas, hace
# trivial ajustarlas o agregar exámenes sin tocar la lógica de abajo.
# sexo = None significa "ambos". (Criterios simplificados para el prototipo.)
EMP_REGLAS = [
    {"examen": "Presión arterial", "desde": 18, "hasta": 120, "sexo": None, "motivo": "Detección de hipertensión"},
    {"examen": "Peso y talla (IMC)", "desde": 18, "hasta": 120, "sexo": None, "motivo": "Evaluación nutricional"},
    {"examen": "Glicemia", "desde": 18, "hasta": 120, "sexo": None, "motivo": "Detección de diabetes"},
    {"examen": "Perfil lipídico (colesterol)", "desde": 40, "hasta": 120, "sexo": None, "motivo": "Riesgo cardiovascular"},
    {"examen": "Papanicolaou (PAP)", "desde": 25, "hasta": 64, "sexo": "F", "motivo": "Detección de cáncer cervicouterino"},
    {"examen": "Mamografía", "desde": 50, "hasta": 69, "sexo": "F", "motivo": "Detección de cáncer de mama"},
    {"examen": "Antígeno prostático", "desde": 50, "hasta": 120, "sexo": "M", "motivo": "Detección de cáncer de próstata"},
]

EDAD_ADULTO = 18


def _examenes_para(edad: int, sexo: str) -> list:
    """Devuelve los exámenes del EMP que le corresponden a una persona."""
    return [
        {"examen": r["examen"], "motivo": r["motivo"]}
        for r in EMP_REGLAS
        if r["desde"] <= edad <= r["hasta"] and (r["sexo"] is None or r["sexo"] == sexo)
    ]


@register
class PrevencionModule(BaseModule):
    id = "prevencion"
    title = "Prevención"
    pregunta_central = "¿Tengo exámenes gratuitos pendientes?"
    icon = "ti-vaccine"

    def build(self, contrato_id: str, provider: DataProvider) -> dict:
        data = provider.get_integrantes(contrato_id)
        cotizante = data.get("cotizante", {})
        cargas = data.get("cargas", [])

        # Unificamos cotizante + cargas en una sola lista de personas.
        personas = [{**cotizante, "rol": "cotizante"}]
        personas += [{**c, "rol": "carga"} for c in cargas]

        integrantes = []
        total_examenes = 0
        for p in personas:
            edad = p.get("edad", 0)
            es_menor = edad < EDAD_ADULTO
            examenes = [] if es_menor else _examenes_para(edad, p.get("sexo"))
            total_examenes += len(examenes)
            integrantes.append(
                {
                    "nombre": p.get("nombre"),
                    "rol": p.get("rol"),
                    "edad": edad,
                    "sexo": p.get("sexo"),
                    "es_menor": es_menor,
                    "examenes": examenes,
                    "nota": (
                        "Menor de edad: aplica el control de niño sano, fuera de este módulo."
                        if es_menor
                        else None
                    ),
                }
            )

        return {
            "resumen": {
                "total_examenes": total_examenes,
                "integrantes_con_examenes": sum(1 for i in integrantes if i["examenes"]),
            },
            "integrantes": integrantes,
            "red_prestadores": provider.get_red_prestadores(),
        }
