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

  const params = new URLSearchParams(window.location.search);
  const storyId = params.get('id');

  if (!storyId) {
    mostrarError('No se encontró el video solicitado.');
    return;
  }

  const videoUrl = `http://localhost:5000/api/stories/${storyId}/download`;

  fetch(videoUrl, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
    .then(res => {
      if (!res.ok) throw new Error('El video aún no está disponible o ocurrió un error.');
      return res.blob();
    })
    .then(blob => {
      if (!blob || blob.size === 0) throw new Error('El video está vacío o dañado.');
      const blobUrl = URL.createObjectURL(blob);
      videoElement.src = blobUrl;
      downloadBtn.href = blobUrl;
      downloadBtn.download = `cuento-${storyId}.mp4`;
    })
    .catch(err => {
      console.error('[result.js] Error al cargar video:', err);
      mostrarError(err.message || 'No se pudo cargar el video.');
    });

  function mostrarError(mensaje) {
    videoElement.style.display = 'none';
    downloadBtn.style.display = 'none';
    videoElement.insertAdjacentHTML('beforebegin', `<p style="color:var(--clr-error);">${mensaje}</p>`);
  }
}
