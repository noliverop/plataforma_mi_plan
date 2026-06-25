import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// El proxy es la clave para el Codespace: el navegador llama a /api en el mismo
// origen del frontend, y Vite reenvía esa llamada al backend Django en el
// puerto 8000 (que vive en el mismo contenedor). Así no hay CORS ni URLs del
// Codespace escritas a mano en el código.
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // necesario para que Vite sea accesible dentro del Codespace
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
});
