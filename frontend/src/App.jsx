import { useEffect, useState } from "react";

import { api } from "./api/client.js";
import Sidebar from "./components/Sidebar.jsx";
import { moduleComponents } from "./modules/registry.js";

export default function App() {
  const [profile, setProfile] = useState(null);
  const [modules, setModules] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [moduleData, setModuleData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Carga inicial: perfil + lista de módulos. El primer módulo queda activo.
  useEffect(() => {
    Promise.all([api.getProfile(), api.getModules()])
      .then(([prof, mods]) => {
        setProfile(prof);
        setModules(mods);
        if (mods.length > 0) setActiveId(mods[0].id);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  // Cada vez que cambia el módulo activo, traemos sus datos.
  useEffect(() => {
    if (!activeId) return;
    setModuleData(null);
    api.getModule(activeId).then(setModuleData).catch((e) => setError(e.message));
  }, [activeId]);

  function handleLogout() {
    window.alert("El cierre de sesión estará disponible cuando conectemos la autenticación real.");
  }

  if (loading) {
    return <div className="state">Cargando tu plan…</div>;
  }

  if (error) {
    return (
      <div className="state state-error">
        <p>No pudimos cargar los datos.</p>
        <p className="state-detail">{error}</p>
        <p className="state-detail">¿Está corriendo el backend en el puerto 8000?</p>
      </div>
    );
  }

  const ActiveComponent = activeId ? moduleComponents[activeId] : null;

  return (
    <div className="app">
      <Sidebar
        profile={profile}
        modules={modules}
        activeId={activeId}
        onSelect={setActiveId}
        onLogout={handleLogout}
      />
      <main className="content">
        {!moduleData && <div className="state">Cargando módulo…</div>}
        {moduleData && ActiveComponent && (
          <ActiveComponent data={moduleData.data} meta={moduleData} />
        )}
        {moduleData && !ActiveComponent && (
          <div className="state">
            <p>Módulo “{moduleData.title}” próximamente.</p>
            <p className="state-detail">
              Aún no tiene una vista registrada en el frontend.
            </p>
          </div>
        )}
      </main>
    </div>
  );
}
