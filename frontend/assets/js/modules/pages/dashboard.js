// File: frontend/assets/js/modules/pages/dashboard.js
// Muestra perfiles infantiles del adulto autenticado

import { getToken } from '../auth.js';

export function initPage() {
  const perfilContainer = document.getElementById('perfil-listado'); // Contenedor donde mostrar perfiles

  // Validar si el usuario está autenticado
  const token = getToken();
  if (!token) {
    console.warn('[dashboard.js] No hay token, redirigiendo al login.');
    window.location.href = '/pages/login.html';
    return;
  }

  // Obtener los perfiles del backend
  fetch('http://localhost:5000/api/profiles', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
    .then(res => res.json())
    .then(data => {
      // Manejo de error si el backend devuelve estructura inesperada
      if (!Array.isArray(data)) {
        console.error('[dashboard.js] Respuesta inesperada:', data);
        perfilContainer.innerHTML = '<p>No se pudieron cargar los perfiles.</p>';
        return;
      }

      if (data.length === 0) {
        perfilContainer.innerHTML = '<p>No hay perfiles aún. Crea uno para comenzar.</p>';
        return;
      }

      // Renderizar cada perfil en la interfaz
      perfilContainer.innerHTML = ''; // Limpiar contenido anterior
      data.forEach(perfil => {
        const card = document.createElement('div');
        card.className = 'perfil-card';
        card.innerHTML = `
          <img src="${perfil.avatar_url}" alt="Avatar de ${perfil.nombre}" class="perfil-avatar" />
          <h4>${perfil.nombre}</h4>
          <p>Edad: ${perfil.edad}</p>
          <button onclick="seleccionarPerfil('${perfil.id}')">Elegir</button>
        `;
        perfilContainer.appendChild(card);
      });
    })
    .catch(err => {
      console.error('[dashboard.js] Error al obtener perfiles:', err);
      perfilContainer.innerHTML = '<p>Error al cargar perfiles.</p>';
    });
}

// Esta función guarda el perfil seleccionado y redirige al wizard
window.seleccionarPerfil = function (perfilId) {
  localStorage.setItem('profile_id', perfilId);
  window.location.href = '/pages/wizard.html';
}
