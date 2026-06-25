export default function Prevencion({ data, meta }) {
  // Destructuring defensivo: si un campo no viene, usamos un valor por defecto
  // en vez de reventar al hacer .map sobre undefined. Un componente no debería
  // caerse porque el backend omitió un dato.
  const {
    resumen = {},
    integrantes = [],
    red_prestadores = [],
  } = data || {};

  return (
    <div className="module">
      <header className="module-head">
        <p className="eyebrow">{meta.pregunta_central}</p>
        <h1 className="module-title">{meta.title}</h1>
        <p className="module-sub">
          Exámenes preventivos gratuitos según la edad y el sexo de cada integrante.
        </p>
      </header>

      <section className="thesis">
        <span className="thesis-icon" aria-hidden="true">
          <i className="ti ti-vaccine" />
        </span>
        <p className="thesis-text">
          A tu grupo familiar le corresponden{" "}
          <strong>{resumen.total_examenes ?? 0} exámenes preventivos</strong> en este
          período, repartidos entre {resumen.integrantes_con_examenes ?? 0}{" "}
          {resumen.integrantes_con_examenes === 1 ? "integrante" : "integrantes"}.
        </p>
      </section>

      {integrantes.length === 0 && (
        <section className="card">
          <p className="person-note">
            El backend no devolvió integrantes para este módulo. Revisa la
            respuesta de <code>/api/modules/prevencion/</code>.
          </p>
        </section>
      )}

      {integrantes.map((p, i) => (
        <section className="card" key={i}>
          <div className="person-head">
            <span className={`chip-avatar ${p.rol === "cotizante" ? "chip-avatar-main" : ""}`} aria-hidden="true">
              {p.nombre ? p.nombre.split(" ").map((x) => x[0]).slice(0, 2).join("") : "?"}
            </span>
            <div>
              <p className="person-name">{p.nombre}</p>
              <p className="person-meta">
                {p.rol} · {p.edad} años · {p.sexo === "F" ? "femenino" : "masculino"}
              </p>
            </div>
          </div>

          {(p.examenes || []).length > 0 ? (
            <ul className="exams">
              {p.examenes.map((e) => (
                <li className="exam-row" key={e.examen}>
                  <i className="ti ti-point-filled exam-dot" aria-hidden="true" />
                  <span className="exam-name">{e.examen}</span>
                  <span className="exam-motivo">{e.motivo}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="person-note">{p.nota}</p>
          )}
        </section>
      ))}

      <section className="card">
        <p className="card-label">¿Dónde realizarlos? Red de prestadores</p>
        {red_prestadores.map((c, i) => (
          <div className="prestador" key={i}>
            <div>
              <p className="prestador-name">{c.nombre}</p>
              <p className="prestador-comuna">
                <i className="ti ti-map-pin" aria-hidden="true" /> {c.comuna}
              </p>
            </div>
            <div className="tags">
              {(c.examenes || []).map((e) => (
                <span className="tag" key={e}>{e}</span>
              ))}
            </div>
          </div>
        ))}
      </section>
    </div>
  );
}
