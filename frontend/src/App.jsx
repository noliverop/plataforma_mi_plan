import { useEffect, useState } from "react";

import { api } from "./api/client.js";
import Sidebar from "./components/Sidebar.jsx";
import { moduleComponents } from "./modules/registry.js";

export default function App() {
  const [profile, setProfile] = useState(null);
  const [modules, setModules] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [moduleData, setModuleData] = useState(null);
  const [moduleError, setModuleError] = useState(null); // error SOLO del módulo activo
  const [bootError, setBootError] = useState(null); // error de la carga inicial
  const [loading, setLoading] = useState(true);

  // Carga inicial: perfil + lista de módulos. El primer módulo queda activo.
  useEffect(() => {
    Promise.all([api.getProfile(), api.getModules()])
      .then(([prof, mods]) => {
        setProfile(prof);
        setModules(mods);
        if (mods.length > 0) setActiveId(mods[0].id);
      })
      .catch((e) => setBootError(e.message))
      .finally(() => setLoading(false));
  }, []);

  // Cada vez que cambia el módulo activo, traemos sus datos.
  useEffect(() => {
    if (!activeId) return;
    setModuleData(null);
    setModuleError(null);
    api
      .getModule(activeId)
      .then(setModuleData)
      .catch((e) => setModuleError(e.message));
  }, [activeId]);

  function handleLogout() {
    window.alert("El cierre de sesión estará disponible cuando conectemos la autenticación real.");
  }

  if (loading) {
    return <div className="state">Cargando tu plan…</div>;
  }

  if (bootError) {
    return (
      <div className="state state-error">
        <p>No pudimos iniciar la aplicación.</p>
        <p className="state-detail">{bootError}</p>
        <p className="state-detail">¿Está corriendo el backend en el puerto 8000?</p>
      </div>
    );
  }

  const ActiveComponent = activeId ? moduleComponents[activeId] : null;

  // CLAVE: los datos que tenemos en mano corresponden al módulo activo SOLO si
  // su id coincide con activeId. Al cambiar de módulo, durante un instante
  // `activeId` ya es el nuevo pero `moduleData` todavía es el del módulo
  // anterior. Sin esta guarda, le pasaríamos los datos viejos al componente
  // nuevo (p. ej. datos de Prevención a ResultadoDelPlan) y reventaría.
  const datosListos = moduleData && moduleData.id === activeId;

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
        {moduleError && (
          <div className="state state-error">
            <p>No pudimos cargar este módulo.</p>
            <p className="state-detail">{moduleError}</p>
            <p className="state-detail">
              Si ves un error 500, revisa la terminal del backend (Django): ahí
              aparece la causa exacta, normalmente un archivo de datos que falta.
            </p>
          </div>
        )}
        {!moduleError && !datosListos && <div className="state">Cargando módulo…</div>}
        {!moduleError && datosListos && ActiveComponent && (
          <ActiveComponent data={moduleData.data} meta={moduleData} />
        )}
        {!moduleError && datosListos && !ActiveComponent && (
          <div className="state">
            <p>Módulo “{moduleData.title}” próximamente.</p>
            <p className="state-detail">Aún no tiene una vista registrada en el frontend.</p>
          </div>
        )}
      </main>
    </div>
  );
}
