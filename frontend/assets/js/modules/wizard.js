// File: frontend/assets/js/modules/pages/wizard.js
// Controla el flujo de pasos para crear un videocuento personalizado

import { getToken } from '../auth.js';

export function initPage() {
  const pasos = document.querySelectorAll('.wizard-step');
  const btnSiguiente = document.getElementById('wizard-next');
  const barraProgreso = document.getElementById('wizard-progress');

  let pasoActual = 0;
  const elecciones = [];

  // Validar autenticación
  const token = getToken();
  if (!token) {
    console.warn('[wizard.js] No hay token. Redirigiendo al login...');
    window.location.href = '/pages/login.html';
    return;
  }

  // Verificar que haya un profile_id seleccionado
  const profileId = localStorage.getItem('profile_id');
  if (!profileId) {
    alert('Debes seleccionar un perfil infantil antes de crear el cuento.');
    window.location.href = '/pages/dashboard.html';
    return;
  }

  mostrarPaso(pasoActual);

  // Manejo del clic en opciones (botones de cada paso)
  pasos.forEach((paso, index) => {
    const opciones = paso.querySelectorAll('.btn');
    opciones.forEach(boton => {
      boton.addEventListener('click', () => {
        // Guardar elección
        elecciones[index] = boton.textContent.trim();

        // Resaltar botón seleccionado
        opciones.forEach(btn => btn.classList.remove('btn-primary'));
        boton.classList.add('btn-primary');
      });
    });
  });

  // Botón siguiente
  btnSiguiente.addEventListener('click', () => {
    // Validar que se haya hecho una elección
    if (!elecciones[pasoActual]) {
      alert('Por favor selecciona una opción antes de continuar.');
      return;
    }

    // Avanzar paso o finalizar
    if (pasoActual < pasos.length - 1) {
      pasoActual++;
      mostrarPaso(pasoActual);
    } else {
      enviarHistoria();
    }
  });

  function mostrarPaso(index) {
    pasos.forEach((paso, i) => {
      paso.style.display = i === index ? 'block' : 'none';
    });

    // Actualizar progreso visual (ej. 20%, 40%, etc.)
    const porcentaje = ((index + 1) / pasos.length) * 100;
    barraProgreso.style.width = `${porcentaje}%`;
  }

  async function enviarHistoria() {
    const payload = {
      profile_id: profileId,
      nombre: elecciones[0],
      lugar: elecciones[1],
      objeto_magico: elecciones[2],
      villano: elecciones[3],
      tipo_final: elecciones[4]
    };

    try {
      const response = await fetch('http://localhost:5000/api/stories/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (!response.ok) {
        const error = data?.error || 'No se pudo iniciar la historia.';
        alert(error);
        return;
      }

      // Redirigir a pantalla de carga con story_id
      const storyId = data.story_id;
      localStorage.removeItem('profile_id'); // limpiar
      window.location.href = `/pages/loading.html?id=${storyId}`;

    } catch (error) {
      console.error('[wizard.js] Error al enviar historia:', error);
      alert('Hubo un error al generar el cuento.');
    }
  }
}
