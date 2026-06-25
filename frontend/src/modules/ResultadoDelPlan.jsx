import { useState } from "react";

const clp = new Intl.NumberFormat("es-CL", {
  style: "currency",
  currency: "CLP",
  maximumFractionDigits: 0,
});

// Cada estado del semáforo trae su color, ícono y etiqueta. El color fuerte de
// la app vive solo aquí: es la pieza memorable.
const ESTADOS = {
  a_favor: { tone: "good", icon: "ti-circle-check", label: "A tu favor" },
  equilibrado: { tone: "even", icon: "ti-equal", label: "Equilibrado" },
  en_contra: { tone: "bad", icon: "ti-alert-triangle", label: "En contra" },
};

export default function ResultadoDelPlan({ data, meta }) {
  const [verDesglose, setVerDesglose] = useState(false);
  const { resumen, semaforo } = data;
  const estado = ESTADOS[semaforo.estado] || ESTADOS.equilibrado;

  // Las barras se escalan respecto del mayor de los dos valores.
  const tope = Math.max(semaforo.total_pagado, semaforo.total_recibido, 1);
  const pctPagado = Math.round((semaforo.total_pagado / tope) * 100);
  const pctRecibido = Math.round((semaforo.total_recibido / tope) * 100);

  const metricas = [
    { label: "Total pagado", value: semaforo.total_pagado },
    { label: "Bonificado", value: semaforo.total_bonificado },
    { label: "Copago", value: semaforo.total_copago },
    { label: "Subsidio licencias", value: semaforo.subsidio_licencias },
  ];

  return (
    <div className="module">
      <header className="module-head">
        <p className="eyebrow">{meta.pregunta_central}</p>
        <h1 className="module-title">{meta.title}</h1>
        <p className="module-sub">
          {resumen.isapre} · {resumen.tipo_plan} · {resumen.numero_integrantes} integrantes
        </p>
      </header>

      {/* Veredicto: el titular humano. */}
      <section className={`verdict tone-${estado.tone}`}>
        <div className="verdict-top">
          <span className="verdict-icon" aria-hidden="true">
            <i className={`ti ${estado.icon}`} />
          </span>
          <div>
            <p className="verdict-label">{estado.label}</p>
            <p className="verdict-msg">{semaforo.mensaje}</p>
          </div>
        </div>
        <p className="verdict-frase">{semaforo.frase}</p>
      </section>

      {/* Balance visual pago vs uso. */}
      <section className="card">
        <p className="card-label">Balance del mes: cuánto pagas vs cuánto usas</p>
        <div className="bar-row">
          <span className="bar-name">Pagaste</span>
          <div className="bar-track">
            <div className="bar-fill bar-paid" style={{ width: `${pctPagado}%` }} />
          </div>
          <span className="bar-value">{clp.format(semaforo.total_pagado)}</span>
        </div>
        <div className="bar-row">
          <span className="bar-name">Recibiste</span>
          <div className="bar-track">
            <div className="bar-fill bar-recv" style={{ width: `${pctRecibido}%` }} />
          </div>
          <span className="bar-value bar-value-recv">
            {clp.format(semaforo.total_recibido)}
          </span>
        </div>
      </section>

      {/* Métricas. */}
      <section className="metrics">
        {metricas.map((m) => (
          <div className="metric" key={m.label}>
            <p className="metric-label">{m.label}</p>
            <p className="metric-value">{clp.format(m.value)}</p>
          </div>
        ))}
      </section>

      {/* Integrantes. */}
      <section className="card">
        <p className="card-label">Integrantes del contrato ({resumen.numero_integrantes})</p>
        <div className="chips">
          {resumen.integrantes.map((p, i) => (
            <span className={`chip ${p.rol === "cotizante" ? "chip-main" : ""}`} key={i}>
              <span className="chip-avatar" aria-hidden="true">
                {p.nombre ? p.nombre.split(" ").map((x) => x[0]).slice(0, 2).join("") : "?"}
              </span>
              {p.nombre} · {p.rol}
            </span>
          ))}
        </div>
      </section>

      {/* Desglose: divulgación progresiva. */}
      <section className="card">
        <button
          className="disclosure"
          onClick={() => setVerDesglose((v) => !v)}
          aria-expanded={verDesglose}
        >
          <span>Ver desglose de la cotización pactada</span>
          <span className="disclosure-right">
            {resumen.desglose_cotizacion.length} ítems
            <i className={`ti ti-chevron-${verDesglose ? "up" : "down"}`} aria-hidden="true" />
          </span>
        </button>
        {verDesglose && (
          <ul className="desglose">
            {resumen.desglose_cotizacion.map((item) => (
              <li key={item.label}>
                <span>{item.label}</span>
                <span className="desglose-value">{clp.format(item.value)}</span>
              </li>
            ))}
            <li className="desglose-total">
              <span>Total cotización pactada</span>
              <span className="desglose-value">{clp.format(resumen.precio_mensual)}</span>
            </li>
          </ul>
        )}
      </section>
    </div>
  );
}
