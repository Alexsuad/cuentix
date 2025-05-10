// frontend/assets/js/modules/pages/landing.js

// ✅ Importamos la función que incluye el header y el footer
import { loadHeaderFooter } from "../utils/include.js";

// ✅ Función principal que se ejecuta al cargar la Landing Page
export function initPage() {
  // Cargar automáticamente el header y footer desde los archivos parciales
  loadHeaderFooter();

  // Si deseas añadir lógica específica para esta página en el futuro (como animaciones o eventos), hazlo aquí.
  console.log("Landing page inicializada correctamente");
}
