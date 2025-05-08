// frontend/assets/js/main.js
// Punto de entrada principal del Frontend de Cuentix

// Esta función detecta el nombre del archivo HTML actual
function getCurrentPageName() {
  const path = window.location.pathname;
  const filename = path.substring(path.lastIndexOf("/") + 1);
  return filename.replace(".html", ""); // Ej: landing, login, etc.
}

// Esta función importa dinámicamente el módulo de la página
async function initPage() {
  const page = getCurrentPageName();

  try {
    // Importación dinámica del archivo JS correspondiente a la página
    const module = await import(`./modules/pages/${page}.js`);

    // Llama a initPage() si existe en el módulo
    if (typeof module.initPage === "function") {
      module.initPage();
    } else {
      console.warn(`[main.js] El módulo '${page}.js' no tiene una función initPage.`);
    }
  } catch (error) {
    console.warn(`[main.js] No se pudo cargar el módulo para '${page}.html':`, error);
  }
}

// Ejecutar cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", initPage);
