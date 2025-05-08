// frontend/assets/js/modules/utils/include.js

// Carga dinámica del header y footer si existen
export async function loadHeaderFooter() {
    try {
      // --- Header ---
      const header = document.getElementById("header-placeholder");
      if (header) {
        const response = await fetch("../partials/header.html");
        if (response.ok) {
          const html = await response.text();
          header.innerHTML = html;
        } else {
          console.error("[include.js] Error al cargar header.html:", response.status);
        }
      }
  
      // --- Footer ---
      const footer = document.getElementById("footer-placeholder");
      if (footer) {
        const response = await fetch("../partials/footer.html");
        if (response.ok) {
          const html = await response.text();
          footer.innerHTML = html;
        } else {
          console.error("[include.js] Error al cargar footer.html:", response.status);
        }
      }
    } catch (error) {
      console.error("[include.js] Error general al cargar header/footer:", error);
    }
  }
  