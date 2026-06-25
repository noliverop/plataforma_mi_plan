// Cliente único de la API. Todo pasa por /api, que Vite reenvía a Django.
// Tener esto en un solo lugar significa que, si mañana cambias cómo se llega al
// backend (otra URL, headers de auth, etc.), lo tocas aquí y nada más.
const BASE = "/api";

async function get(path) {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) {
    throw new Error(`La API respondió ${res.status} en ${path}`);
  }
  return res.json();
}

export const api = {
  getProfile: () => get("/profile/"),
  getModules: () => get("/modules/"),
  getModule: (id) => get(`/modules/${id}/`),
};
