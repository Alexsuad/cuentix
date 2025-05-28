// archivo: frontend/assets/js/modules/pages/history.js
// -----------------------------------------------------------------------------
// Módulo para la página history.html
// Muestra los cuentos generados por el usuario autenticado y permite eliminarlos
// Requiere: apiClient (con JWT), SweetAlert2, estructura HTML en history.html
// -----------------------------------------------------------------------------

import { apiClient } from '../api.js';

// Función principal de inicialización
function initPage() {
    const listContainer = document.getElementById('history-list');
    const loading = document.getElementById('history-loading');
    const empty = document.getElementById('no-history');
    const error = document.getElementById('history-error');

    // Oculta todos los estados al inicio
    function resetStates() {
        loading.hidden = true;
        empty.hidden = true;
        error.hidden = true;
    }

    // Obtener el historial desde la API
    async function fetchHistorial() {
        try {
            resetStates();
            loading.hidden = false;

            const { data } = await apiClient.get('/stories/history');

            loading.hidden = true;

            if (!data || data.length === 0) {
                empty.hidden = false;
                return;
            }

            data.forEach(story => {
                const col = document.createElement('div');
                col.className = 'col';
                col.innerHTML = renderCard(story);
                listContainer.appendChild(col);
            });
        } catch (err) {
            console.error('[history.js] Error al cargar historial:', err);
            resetStates();
            error.hidden = false;
        }
    }

    // Plantilla HTML de una tarjeta de cuento
    function renderCard(story) {
        const fecha = new Date(story.created_at).toLocaleDateString('es-ES', {
            year: 'numeric', month: 'short', day: 'numeric'
        });

        return `
      <div class="history-card">
        <img src="${story.thumbnail_url}" alt="Miniatura del cuento" class="history-card__img">
        <div class="history-card__body">
          <h5 class="history-card__title">${story.nombre}</h5>
          <p class="history-card__meta">${fecha}</p>
          <div class="history-card__actions">
            <a href="result.html?id=${story.id}" class="btn btn-info btn-sm btn-rounded">Ver</a>
            <a href="${story.video_url}" download class="btn btn-warning btn-sm btn-rounded">Descargar</a>
            <button class="btn btn-danger btn-sm btn-rounded" data-id="${story.id}">Eliminar</button>
          </div>
        </div>
      </div>
    `;
    }

    // Delegación de eventos para botones de eliminar
    listContainer.addEventListener('click', async e => {
        if (e.target.matches('button[data-id]')) {
            const id = e.target.dataset.id;
            const card = e.target.closest('.col');

            const confirm = await Swal.fire({
                icon: 'warning',
                title: '¿Eliminar este cuento?',
                text: 'Esta acción no se puede deshacer.',
                showCancelButton: true,
                confirmButtonText: 'Sí, eliminar',
                cancelButtonText: 'Cancelar'
            });

            if (confirm.isConfirmed) {
                try {
                    await apiClient.delete(`/api/stories/${id}`);
                    card.remove();
                } catch (err) {
                    console.error('[history.js] Error al eliminar:', err);
                    Swal.fire('Error', 'No se pudo eliminar. Intenta de nuevo.', 'error');
                }
            }
        }
    });

    // Ejecutar al cargar
    fetchHistorial();
}

// Ejecutar initPage() cuando el DOM esté listo
if (document.readyState !== 'loading') {
    initPage();
} else {
    document.addEventListener('DOMContentLoaded', initPage);
}
