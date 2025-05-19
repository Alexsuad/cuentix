// frontend/assets/js/main.js
// Punto de entrada principal del Frontend de Cuentix

import { loadPartials } from './modules/utils/loadPartials.js';  // ⬅️ importamos ahora como módulo

function getCurrentPageName() {
  const path = window.location.pathname;
  const filename = path.substring(path.lastIndexOf("/") + 1);
  return filename.replace(".html", "");
}

async function initPage() {
  const page = getCurrentPageName();
  try {
    const module = await import(`./modules/pages/${page}.js`);
    if (typeof module.initPage === "function") {
      module.initPage();
    } else {
      console.warn(`[main.js] El módulo '${page}.js' no tiene una función initPage().`);
    }
  } catch (error) {
    console.warn(`[main.js] No se pudo cargar el módulo para '${page}.html':`, error);
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  await loadPartials();  // ⬅️ ahora es importado, no declarado aquí
  await initPage();
});
