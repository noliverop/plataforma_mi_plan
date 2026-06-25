// Registro de módulos del frontend: mapea el id de cada módulo (el mismo que
// entrega el backend en /api/modules/) a su componente de React.
//
// Espejo del registro del backend. Cuando agregues el Módulo 2:
//   1. Creas su componente en src/modules/.
//   2. Lo registras aquí con su id.
// El sidebar y el ruteo ya funcionan solos a partir de /api/modules/, así que
// no hay que tocar nada más. Si un módulo existe en el backend pero todavía no
// tiene componente aquí, la app muestra un cartel de "próximamente".
import ResultadoDelPlan from "./ResultadoDelPlan.jsx";

export const moduleComponents = {
  "resultado-del-plan": ResultadoDelPlan,
};
