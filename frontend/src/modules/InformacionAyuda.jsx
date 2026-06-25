import { useMemo, useState } from "react";

export default function InformacionAyuda({ data, meta }) {
  const { glosario = [], beneficios = [] } = data || {};
  const [q, setQ] = useState("");

  // Filtro del glosario en el cliente: rápido y sin ir al servidor.
  const glosarioFiltrado = useMemo(() => {
    const t = q.trim().toLowerCase();
    if (!t) return glosario;
    return glosario.filter(
      (g) =>
        g.termino.toLowerCase().includes(t) ||
        g.definicion.toLowerCase().includes(t)
    );
  }, [q, glosario]);

  return (
    <div className="module">
      <header className="module-head">
        <p className="eyebrow">{meta.pregunta_central}</p>
        <h1 className="module-title">{meta.title}</h1>
        <p className="module-sub">
          Conceptos de tu plan en palabras simples, y los beneficios a los que tienes derecho.
        </p>
      </header>

      <section className="card">
        <p className="card-label">Glosario</p>
        <div className="search">
          <i className="ti ti-search" aria-hidden="true" />
          <input
            type="text"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Buscar un término…"
            aria-label="Buscar en el glosario"
          />
        </div>

        {glosarioFiltrado.length === 0 ? (
          <p className="person-note">No encontramos ese término. Prueba con otra palabra.</p>
        ) : (
          <dl className="glosario">
            {glosarioFiltrado.map((g) => (
              <div className="glo-item" key={g.termino}>
                <dt className="glo-term">{g.termino}</dt>
                <dd className="glo-def">{g.definicion}</dd>
              </div>
            ))}
          </dl>
        )}
      </section>

      <section>
        <p className="card-label card-label-loose">Beneficios y derechos disponibles</p>
        <div className="beneficios">
          {beneficios.map((b) => (
            <div className="beneficio" key={b.nombre}>
              <span className="beneficio-icon" aria-hidden="true">
                <i className={`ti ${b.icon || "ti-circle-check"}`} />
              </span>
              <p className="beneficio-name">{b.nombre}</p>
              <p className="beneficio-desc">{b.descripcion}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
