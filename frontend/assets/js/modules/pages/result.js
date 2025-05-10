// File: frontend/assets/js/modules/pages/result.js
// Muestra el video generado y habilita descarga

import { getToken } from '../auth.js';

export function initPage() {
  const videoElement = document.getElementById('cuento-video');
  const downloadBtn = document.getElementById('descargar-btn');
  const token = getToken();

  if (!token) {
    window.location.href = '/pages/login.html';
    return;
  }

  // Obtener story_id desde la URL
  const params = new URLSearchParams(window.location.search);
  const storyId = params.get('id');

  if (!storyId) {
    videoElement.insertAdjacentHTML('beforebegin', '<p>No se encontró el video solicitado.</p>');
    return;
  }

  // Construir la URL del video y establecerla
  const videoUrl = `http://localhost:5000/api/stories/${storyId}/download`;

  // Aplicar URL protegida con token (idealmente usar backend que sirva video por cookie/session, pero aquí lo haremos simple)
  fetch(videoUrl, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('El video aún no está disponible.');
      }
      return response.blob();
    })
    .then(blob => {
      const blobUrl = URL.createObjectURL(blob);
      videoElement.src = blobUrl;
      downloadBtn.href = blobUrl;
      downloadBtn.download = `cuento-${storyId}.mp4`;
    })
    .catch(err => {
      console.error('[result.js] Error al cargar video:', err);
      videoElement.insertAdjacentHTML('beforebegin', `<p>${err.message}</p>`);
    });
}
