// File: frontend/assets/js/utils/loadPartials.js

export async function loadPartials() {
    const headerContainer = document.getElementById("header-placeholder");
    const footerContainer = document.getElementById("footer-placeholder");
  
    // Cargar header si existe en el HTML
    if (headerContainer) {
      try {
        const html = await fetch("/frontend/partials/header.html").then(r => r.text());
        headerContainer.innerHTML = html;
      } catch (err) {
        console.error("[loadPartials] No se pudo cargar header.html:", err);
      }
    }
  
    // Cargar footer si existe
    if (footerContainer) {
      try {
        const html = await fetch("/frontend/partials/footer.html").then(r => r.text());
        footerContainer.innerHTML = html;
      } catch (err) {
        console.error("[loadPartials] No se pudo cargar footer.html:", err);
      }
    }
  }
  