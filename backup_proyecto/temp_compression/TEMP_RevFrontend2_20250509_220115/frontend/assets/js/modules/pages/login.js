/*frontend\assets\js\modules\pages\login.js
// login.js - Módulo encargado de manejar el formulario de inicio de sesión

// Importamos el módulo de autenticación
import { loginUsuario } from '../auth.js';

// Esperamos que el DOM esté completamente cargado antes de ejecutar nada
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('loginForm'); // Referencia al formulario
  const errorDiv = document.getElementById('errorMessage'); // Área para mostrar errores

  // Escuchamos el envío del formulario
  form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevenimos el comportamiento por defecto (recarga)

    // Obtenemos los valores del formulario
    const email = form.email.value.trim();
    const password = form.password.value;

    // Validamos campos básicos (opcional, ya están en required)
    if (!email || !password) {
      mostrarError('Por favor, rellena todos los campos.');
      return;
    }

    try {
      // Llamamos a la función de login (usa fetch o axios internamente)
      const respuesta = await loginUsuario(email, password);

      // Si se recibe un token, lo almacenamos en localStorage
      if (respuesta.token) {
        localStorage.setItem('token', respuesta.token);

        // Redirigimos al dashboard
        window.location.href = 'dashboard.html';
      } else {
        mostrarError('Credenciales incorrectas o respuesta inválida del servidor.');
      }
    } catch (err) {
      console.error('Error en login:', err);
      mostrarError('Hubo un problema al intentar iniciar sesión. Intenta más tarde.');
    }
  });

  // Función para mostrar mensajes de error
  function mostrarError(mensaje) {
    errorDiv.textContent = mensaje;
    errorDiv.style.display = 'block';
  }
});
