// Cliente único de la API. Todo pasa por /api, que Vite reenvía a Django.
// Tener esto en un solo lugar significa que, si mañana cambias cómo se llega al
// backend (otra URL, headers de auth, etc.), lo tocas aquí y nada más.
const BASE = "/api";

async function get(path) {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) {
    // Incluimos el código y un trozo del cuerpo para que el error sea útil:
    // un 500 indica que el problema está en el backend (mira su terminal),
    // un 404 que la ruta no existe, etc.
    let detalle = "";
    try {
      detalle = (await res.text()).slice(0, 160);
    } catch {
      /* sin cuerpo legible */
    }
    throw new Error(`HTTP ${res.status} en ${path}${detalle ? ` — ${detalle}` : ""}`);
  }
  return res.json();
}

export const api = {
  getProfile: () => get("/profile/"),
  getModules: () => get("/modules/"),
  getModule: (id) => get(`/modules/${id}/`),
};
