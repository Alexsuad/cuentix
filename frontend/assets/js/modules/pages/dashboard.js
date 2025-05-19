// File: frontend/assets/js/modules/pages/dashboard.js

import { getToken } from '../auth.js';

export function initPage() {
  const perfilContainer = document.getElementById('perfil-listado');
  const token = getToken();

  if (!token) {
    window.location.href = '/pages/login.html';
    return;
  }

  fetch('http://localhost:5000/api/profiles', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
    .then(res => res.json())
    .then(data => {
      if (!Array.isArray(data)) {
        perfilContainer.innerHTML = '<p>No se pudieron cargar los perfiles.</p>';
        return;
      }

      if (data.length === 0) {
        perfilContainer.innerHTML = '<p>No hay perfiles aún. Crea uno para comenzar.</p>';
        return;
      }

      perfilContainer.innerHTML = '';
      data.forEach(perfil => {
        const card = document.createElement('div');
        card.className = 'perfil-card';
        card.innerHTML = `
          <img src="${perfil.avatar_url}" alt="Avatar de ${perfil.nombre}" class="perfil-avatar" />
          <h4>${perfil.nombre}</h4>
          <p>Edad: ${perfil.edad}</p>
          <div class="perfil-card-actions">
            <button class="btn btn-primary" onclick="seleccionarPerfil('${perfil.id}')">Elegir</button>
            <button class="btn btn-danger" onclick="eliminarPerfil('${perfil.id}')">Eliminar</button>
          </div>

        `;
        perfilContainer.appendChild(card);
      });
    })
    .catch(err => {
      console.error('[dashboard.js] Error al obtener perfiles:', err);
      perfilContainer.innerHTML = '<p>Error al cargar perfiles.</p>';
    });
}

// Seleccionar perfil y continuar
window.seleccionarPerfil = function (perfilId) {
  localStorage.setItem('profile_id', perfilId);
  window.location.href = '/pages/wizard.html';
};

// Eliminar perfil con confirmación
window.eliminarPerfil = async function (perfilId) {
  const confirmar = confirm('¿Estás seguro de que deseas eliminar este perfil? Esta acción no se puede deshacer.');
  if (!confirmar) return;

  const token = getToken();
  try {
    const res = await fetch(`http://localhost:5000/api/profiles/${perfilId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (res.ok) {
      alert('Perfil eliminado correctamente.');
      location.reload(); // recarga la vista
    } else {
      const data = await res.json();
      alert(data?.error || 'No se pudo eliminar el perfil.');
    }

  } catch (err) {
    console.error('[dashboard.js] Error al eliminar perfil:', err);
    alert('Hubo un problema al intentar eliminar el perfil.');
  }
};
