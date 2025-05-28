/* ---------------------------------------------------------------------------
  frontend/assets/js/modules/pages/dashboard.js
  Controla la vista de gestión de perfiles infantiles en dashboard.html
---------------------------------------------------------------------------
  ► 1. Verifica autenticación (cuentix_token)
  ► 2. Obtiene perfiles infantiles desde el backend (/api/profiles)
  ► 3. Renderiza tarjetas dinámicas por perfil con opciones de eliminar/usar
  ► 4. Elimina perfiles con confirmación visual (SweetAlert2)
  ► 5. Guarda perfil activo en localStorage (profile_id)
--------------------------------------------------------------------------- */

import { apiClient } from '../api.js';
import { mostrarFeedback } from '../utils/showFeedback.js';

/** Verifica si hay token. Si no, redirige al login absoluto */
function verificarAutenticacion() {
  const token = localStorage.getItem('cuentix_token');
  if (!token) {
    window.location.href = '/pages/login.html';
  }
}

/** Inicializa la página dashboard.html */
export function initPage() {
  verificarAutenticacion();
  obtenerPerfiles();
}

/** Llama al backend y renderiza los perfiles del adulto */
async function obtenerPerfiles() {
  const contenedor = document.getElementById('perfil-listado');
  contenedor.innerHTML = '<p>Cargando perfiles...</p>';

  try {
    const { data: perfiles } = await apiClient.get('/profiles');

    if (!perfiles.length) {
      contenedor.innerHTML = '<p class="text-muted">Aún no tienes perfiles creados.</p>';
      return;
    }

    contenedor.innerHTML = perfiles.map(perfil => `
      <div class="perfil-card">
        <div class="perfil-avatar">
          <img src="${perfil.avatar_url || '/assets/img/default-avatar.png'}" alt="Avatar" />
        </div>
        <div class="perfil-card-info">
          <h5>${perfil.nombre}</h5>
          <p>Edad: ${perfil.edad}</p>
        </div>
        <div class="perfil-card-actions">
          <button class="btn btn-primary usar-btn" data-id="${perfil.id}">Usar</button>
          <button class="btn btn-danger eliminar-btn" data-id="${perfil.id}">Eliminar</button>
        </div>
      </div>
    `).join('');

  } catch (err) {
    console.error('[dashboard] Error al obtener perfiles:', err);
    mostrarFeedback('error', 'Error de conexión', 'No se pudieron cargar los perfiles.');
  }
}

/** Delegación de eventos para botones dentro del contenedor */
document.addEventListener('click', (e) => {
  const id = e.target.dataset.id;
  if (!id) return;

  if (e.target.classList.contains('usar-btn')) {
    seleccionarPerfil(id);
  } else if (e.target.classList.contains('eliminar-btn')) {
    eliminarPerfil(id);
  }
});

/** Guarda el perfil seleccionado y redirige (flujo post-login) */
function seleccionarPerfil(profileId) {
  localStorage.setItem('cuentix_profile_id', profileId);
  mostrarFeedback('success', 'Perfil seleccionado', 'Redirigiendo...');
  setTimeout(() => {
    window.location.href = 'generate.html';
  }, 1500);
}

/** Elimina un perfil infantil con confirmación visual y error específico */
async function eliminarPerfil(profileId) {
  const confirmacion = await Swal.fire({
    title: '¿Eliminar perfil?',
    text: 'Esta acción no se puede deshacer.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Sí, eliminar',
    cancelButtonText: 'Cancelar'
  });

  if (!confirmacion.isConfirmed) return;

  try {
    await apiClient.delete(`/profiles/${profileId}`);
    mostrarFeedback('success', 'Perfil eliminado', 'Actualizando lista...');
    obtenerPerfiles();
  } catch (err) {
    console.error('[dashboard] Error al eliminar perfil:', err);
    const msg = err.response?.data?.error || 'No se pudo eliminar el perfil';
    mostrarFeedback('error', 'Error', msg);
  }
}
