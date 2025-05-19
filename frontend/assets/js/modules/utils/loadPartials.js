// File: frontend/assets/js/modules/utils/loadPartials.js

/**
 * Carga dinámica de header y footer según la ubicación del HTML.
 * Compatible con páginas en /pages/ o en raíz.
 */
export async function loadPartials() {
  const headerContainer = document.getElementById("header-placeholder");
  const footerContainer = document.getElementById("footer-placeholder");

  // Detecta si estamos en /pages/ para ajustar la ruta relativa
  const isInPagesFolder = window.location.pathname.includes("/pages/");
  const prefix = isInPagesFolder ? "../" : "";

  try {
    if (headerContainer) {
      const res = await fetch(`${prefix}partials/header.html`);
      const html = await res.text();
      headerContainer.innerHTML = html;
    }

    if (footerContainer) {
      const res = await fetch(`${prefix}partials/footer.html`);
      const html = await res.text();
      footerContainer.innerHTML = html;
    }
  } catch (err) {
    console.error("[loadPartials] Error al cargar header o footer:", err);
  }
}
