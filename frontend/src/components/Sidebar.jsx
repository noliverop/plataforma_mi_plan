// El sidebar de la plataforma individual: marca, perfil del afiliado,
// navegación entre módulos (que viene de la API, no escrita a mano) y logout.
function initials(nombre) {
  if (!nombre) return "?";
  return nombre
    .split(" ")
    .slice(0, 2)
    .map((p) => p[0])
    .join("")
    .toUpperCase();
}

export default function Sidebar({ profile, modules, activeId, onSelect, onLogout }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <span className="brand-mark" aria-hidden="true">
          <i className="ti ti-heartbeat" />
        </span>
        <span className="brand-name">
          Mi<span className="brand-name-soft">Plan</span>
        </span>
      </div>

      {profile && (
        <div className="profile">
          <div className="profile-avatar" aria-hidden="true">
            {initials(profile.nombre)}
          </div>
          <div className="profile-info">
            <p className="profile-name">{profile.nombre}</p>
            <p className="profile-rut">{profile.rut}</p>
          </div>
        </div>
      )}

      <nav className="nav" aria-label="Módulos">
        {modules.map((m) => (
          <button
            key={m.id}
            className={`nav-item ${m.id === activeId ? "is-active" : ""}`}
            onClick={() => onSelect(m.id)}
            aria-current={m.id === activeId ? "page" : undefined}
          >
            <i className={`ti ${m.icon || "ti-layout-dashboard"}`} aria-hidden="true" />
            <span>{m.title}</span>
          </button>
        ))}
      </nav>

      <button className="logout" onClick={onLogout}>
        <i className="ti ti-logout" aria-hidden="true" />
        <span>Cerrar sesión</span>
      </button>
    </aside>
  );
}
