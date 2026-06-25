"""
Módulo 1 — Resultado del plan.

Pregunta central: ¿Cuál es el resultado de mi plan en términos simples?

Reúne dos bloques del documento original:
  1.1 Resumen del contrato (datos + desglose de la cotización pactada).
  1.2 Semáforo: balance entre lo que la persona paga y lo que recibe.
"""
from ..data_provider import DataProvider
from ..registry import BaseModule, register

# Etiquetas legibles para el desglose de la cotización pactada.
ETIQUETAS_COTIZACION = {
    "precio_base_plan": "Precio base del plan",
    "factor_grupo_familiar": "Factor grupo familiar",
    "diferencia_fallo_corte_suprema": "Diferencia fallo E. Corte Suprema",
    "valor_uf_edad_2_y_65": "Valor UF edad ≥2 y ≤65",
    "precio_ges": "Precio GES",
    "precio_caec": "Precio CAEC",
    "precio_beneficio_adicional": "Precio beneficio adicional",
    "prima_extraordinaria_ley_21674": "Prima extraordinaria Ley 21.674",
    "ajuste_al_7_ley_21674": "Ajuste al 7% Ley 21.674",
    "total_cotizacion_pactada": "Total cotización pactada",
}

def _clp(monto: int) -> str:
    """Formatea un monto en pesos chilenos: separador de miles con punto."""
    return f"${monto:,.0f}".replace(",", ".")


# Reglas CIRC69: solo cuentan las licencias curativas, de patología del embarazo
# y de medicina preventiva tipos 1, 2 y 4.
PREVENTIVA_TIPOS_VALIDOS = {1, 2, 4}


def _licencia_cuenta(lic: dict) -> bool:
    tipo = lic.get("tipo")
    if tipo in ("curativa", "patologia_embarazo"):
        return True
    if tipo == "medicina_preventiva":
        return lic.get("subtipo") in PREVENTIVA_TIPOS_VALIDOS
    return False


@register
class ResultadoDelPlanModule(BaseModule):
    id = "resultado-del-plan"
    title = "Resultado de mi plan"
    pregunta_central = "¿Cuál es el resultado de mi plan en términos simples?"
    icon = "ti-gauge"

    def build(self, contrato_id: str, provider: DataProvider) -> dict:
        contrato = provider.get_contrato(contrato_id)
        integrantes = provider.get_integrantes(contrato_id)
        prestaciones = provider.get_prestaciones_bonificadas(contrato_id)
        licencias = provider.get_licencias_medicas(contrato_id)

        # --- 1.1 Resumen del contrato ---
        cotizacion = contrato.get("cotizacion_pactada", {})
        desglose = [
            {"label": ETIQUETAS_COTIZACION.get(k, k), "value": v}
            for k, v in cotizacion.items()
            if k != "total_cotizacion_pactada"
        ]
        cotizante = integrantes.get("cotizante", {})
        cargas = integrantes.get("cargas", [])

        resumen = {
            "isapre": contrato.get("isapre"),
            "tipo_plan": contrato.get("tipo_plan"),
            "precio_mensual": cotizacion.get("total_cotizacion_pactada"),
            "desglose_cotizacion": desglose,
            "integrantes": [
                {"nombre": cotizante.get("nombre"), "rol": "cotizante"},
                *[{"nombre": c.get("nombre"), "rol": "carga"} for c in cargas],
            ],
            "numero_integrantes": 1 + len(cargas),
        }

        # --- 1.2 Semáforo ---
        total_pagado = contrato.get("cotizacion_total_a_pagar", 0)
        total_bonificado = sum(p.get("valor_bonificado", 0) for p in prestaciones)
        total_copago = sum(p.get("monto_copago", 0) for p in prestaciones)
        subsidio_licencias = sum(
            lic.get("subsidio_liquido", 0) for lic in licencias if _licencia_cuenta(lic)
        )

        total_recibido = total_bonificado + subsidio_licencias
        estado, mensaje = self._evaluar_semaforo(total_pagado, total_recibido)

        frase = (
            f"Este período pagaste {_clp(total_pagado)} y el seguro te bonificó "
            f"{_clp(total_bonificado)} por tus prestaciones de salud, con un copago "
            f"de {_clp(total_copago)}. Además, generó un pago líquido de licencias "
            f"médicas por {_clp(subsidio_licencias)}."
        )

        semaforo = {
            "estado": estado,            # "a_favor" | "equilibrado" | "en_contra"
            "mensaje": mensaje,
            "frase": frase,
            "total_pagado": total_pagado,
            "total_bonificado": total_bonificado,
            "total_copago": total_copago,
            "subsidio_licencias": subsidio_licencias,
            "total_recibido": total_recibido,
        }

        return {"resumen": resumen, "semaforo": semaforo}

    @staticmethod
    def _evaluar_semaforo(pagado: int, recibido: int) -> tuple[str, str]:
        """Traduce la relación pago/uso a un estado tipo semáforo."""
        if pagado <= 0:
            return "equilibrado", "Sin información suficiente del período"
        ratio = recibido / pagado
        if ratio >= 1.0:
            return "a_favor", "Recibiste más de lo que pagaste este período"
        if ratio >= 0.5:
            return "equilibrado", "Lo que pagas y lo que usas están parejos"
        return "en_contra", "Pagaste más de lo que usaste este período"
