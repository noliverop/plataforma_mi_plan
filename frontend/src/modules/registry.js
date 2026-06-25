// Registro de módulos del frontend: mapea el id de cada módulo (el mismo que
// entrega el backend en /api/modules/) a su componente de React.
//
// Espejo del registro del backend. Para agregar un módulo: creas su componente
// y lo registras aquí con su id. El sidebar y el ruteo ya funcionan solos a
// partir de /api/modules/. Si un módulo existe en el backend pero todavía no
// tiene componente aquí, la app muestra un cartel de "próximamente".
import ResultadoDelPlan from "./ResultadoDelPlan.jsx";
import Prevencion from "./Prevencion.jsx";
import InformacionAyuda from "./InformacionAyuda.jsx";

export const moduleComponents = {
  "resultado-del-plan": ResultadoDelPlan,
  "prevencion": Prevencion,
  "informacion-ayuda": InformacionAyuda,
};
