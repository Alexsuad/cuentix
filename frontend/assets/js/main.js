// frontend/assets/js/main.js
// Punto de entrada principal del Frontend de Cuentix

/* ----------------------------------------------------------
   1) Detecta el nombre de la página actual (landing, login…)
----------------------------------------------------------- */
function getCurrentPageName() {
  const path = window.location.pathname;
  const filename = path.substring(path.lastIndexOf("/") + 1);
  return filename.replace(".html", "");
}

/* ----------------------------------------------------------
   2) Carga parcial(es) comunes (footer, header…)
----------------------------------------------------------- */
async function loadPartials() {
  const footerContainer = document.getElementById("footer-placeholder");
  if (footerContainer) {
    try {
      const html = await fetch("/partials/footer.html").then(r => r.text());
      footerContainer.innerHTML = html;
    } catch (err) {
      console.error("[main.js] No se pudo cargar footer.html:", err);
    }
  }
}

/* ----------------------------------------------------------
   3) Importa dinámicamente el módulo JS específico de la página
----------------------------------------------------------- */
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

/* ----------------------------------------------------------
   4) Cuando el DOM esté listo
----------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", async () => {
  await loadPartials(); // ① Inserta footer (y header si añades otro fetch)
  initPage();           // ② Luego lógica particular de la página
});
