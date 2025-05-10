// File: frontend/assets/js/modules/pages/login.js
// Módulo encargado de manejar el formulario de inicio de sesión

import { loginUsuario } from '../auth.js';

// Esta función es llamada desde main.js cuando detecta que estás en login.html
export function initPage() {
  const form = document.getElementById('loginForm');         // Referencia al formulario
  const errorDiv = document.getElementById('errorMessage');  // Área para mostrar errores

  if (!form) {
    console.warn('[login.js] No se encontró el formulario de login.');
    return;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = form.email.value.trim();
    const password = form.password.value;

    if (!email || !password) {
      mostrarError('Por favor, rellena todos los campos.');
      return;
    }

    try {
      const respuesta = await loginUsuario(email, password);

      if (respuesta.token) {
        localStorage.setItem('token', respuesta.token);
        window.location.href = 'dashboard.html'; // Redirige al dashboard
      } else {
        mostrarError('Credenciales incorrectas o respuesta inválida del servidor.');
      }
    } catch (err) {
      console.error('[login.js] Error en login:', err);
      mostrarError('Hubo un problema al intentar iniciar sesión. Intenta más tarde.');
    }
  });

  function mostrarError(mensaje) {
    errorDiv.textContent = mensaje;
    errorDiv.style.display = 'block';
  }
}
