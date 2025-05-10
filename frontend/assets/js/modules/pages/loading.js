// File: frontend/assets/js/modules/pages/loading.js
// Se encarga de consultar el estado de la historia y redirigir cuando esté lista

import { getToken } from '../auth.js';

export function initPage() {
  const statusText = document.getElementById('loading-status');
  const token = getToken();

  if (!token) {
    window.location.href = '/pages/login.html';
    return;
  }

  // Obtener el story_id desde la URL
  const params = new URLSearchParams(window.location.search);
  const storyId = params.get('id');

  if (!storyId) {
    statusText.textContent = 'ID de historia no válido.';
    return;
  }

  const endpoint = `http://localhost:5000/api/stories/${storyId}/status`;
  let intentos = 0;
  const maxIntentos = 20;

  async function verificarEstado() {
    try {
      const res = await fetch(endpoint, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const data = await res.json();

      if (res.ok) {
        if (data.status === 'completed') {
          // Redirige al resultado cuando esté lista
          window.location.href = `/pages/result.html?id=${storyId}`;
        } else {
          statusText.textContent = `Estado actual: ${data.status}…`;
          if (intentos < maxIntentos) {
            intentos++;
            setTimeout(verificarEstado, 5000); // Esperar 5s y volver a consultar
          } else {
            statusText.textContent = 'Demasiados intentos. Intenta más tarde.';
          }
        }
      } else {
        throw new Error(data?.error || 'Error inesperado');
      }

    } catch (error) {
      console.error('[loading.js] Error al verificar estado:', error);
      statusText.textContent = 'Error al conectar con el servidor.';
    }
  }

  verificarEstado();
}
