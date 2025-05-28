// File: frontend/assets/js/modules/pages/loading.js
// Espera que se genere el cuento y redirige cuando esté listo

import { getToken } from '../auth.js';

export function initPage() {
  const statusText = document.getElementById('loading-status');
  const token = getToken();

  // 1. Verifica si el usuario está autenticado
  if (!token) {
    window.location.href = '/pages/login.html';
    return;
  }

  // 2. Extrae el ID del cuento desde la URL
  const params = new URLSearchParams(window.location.search);
  const storyId = params.get('id');

  if (!storyId) {
    statusText.textContent = 'ID de historia no válido.';
    return;
  }

  const endpoint = `http://localhost:5000/api/stories/${storyId}/status`;
  let intentos = 0;
  const maxIntentos = 20;

  // 3. Función que consulta repetidamente el estado del cuento
  async function verificarEstado() {
    try {
      const res = await fetch(endpoint, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data?.error || 'Error inesperado del servidor.');
      }

      // 4. Procesamiento según estado devuelto
      switch (data.status) {
        case 'completed':
          statusText.textContent = '¡Listo! Redirigiendo a tu video-cuento...';
          window.location.href = `/pages/result.html?id=${storyId}`;
          break;

        case 'failed':
          statusText.textContent = 'La generación del cuento ha fallado. Intenta nuevamente.';
          break;

        case 'pending':
        case 'generating':
          statusText.textContent = `Generando cuento mágico... (Intento ${intentos + 1} de ${maxIntentos})`;
          if (intentos < maxIntentos) {
            intentos++;
            setTimeout(verificarEstado, 5000); // esperar 5s y volver a intentar
          } else {
            statusText.textContent = 'El cuento está tardando demasiado. Intenta más tarde.';
          }
          break;

        default:
          statusText.textContent = `Estado desconocido: ${data.status}`;
          break;
      }

    } catch (err) {
      console.error('[loading.js] Error al verificar estado:', err);
      statusText.textContent = 'Error al contactar con el servidor.';
    }
  }

  // 5. Inicia el ciclo de verificación
  verificarEstado();
}
