/*  ---------------------------------------------------------------------------
    frontend/assets/js/modules/pages/login.js
    Controla el formulario de inicio de sesión en login.html
    ---------------------------------------------------------------------------
    ► 1. Importa la función loginUsuario() desde api.js (capa de comunicación)
    ► 2. Valida el formulario con HTML5 + clases Bootstrap "was-validated"
    ► 3. Si el backend confirma, guarda el JWT en localStorage → cuentix_token
    ► 4. Muestra feedback visual con SweetAlert2 y marca los <input> inválidos
---------------------------------------------------------------------------- */

import { loginUsuario } from '../api.js';

// ⚠️ No importar SweetAlert2 aquí: ya se carga desde CDN → variable global: Swal

/**  Función que main.js ejecuta automáticamente cuando detecta login.html */
export function initPage() {
  // --- 1. Referencias a elementos del DOM ---------------------------------
  const form = document.getElementById('login-form');
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');

  // Seguridad: si el formulario no existe (html cambiado) salimos
  if (!form) {
    console.warn('[login.js] Formulario no encontrado.');
    return;
  }

  // --- 2. Listener submit --------------------------------------------------
  form.addEventListener('submit', async (evt) => {
    evt.preventDefault();   // Evita recarga de página
    evt.stopPropagation();  // Detiene propagación del evento

    // Validación HTML5
    if (!form.checkValidity()) {
      form.classList.add('was-validated');
      return;
    }

    // Limpiar estados previos
    limpiarInputs();

    // --- 3. Llamada a loginUsuario (con backend) ---------------------------
    const resultado = await loginUsuario(emailInput.value.trim(), passwordInput.value);

    if (resultado === true) {
      // ✔️ Login exitoso ➜ mostrar feedback y redirigir
      Swal.fire({
        icon: 'success',
        title: '¡Bienvenido/a!',
        text: 'Redirigiendo a tu panel…',
        timer: 1500,
        showConfirmButton: false
      });

      setTimeout(() => {
        window.location.href = 'dashboard.html';
      }, 1600);
      return;
    }

    // ❌ Login fallido ➜ mostrar error específico
    marcarInputsInvalidos();
    mostrarError(resultado || 'Credenciales incorrectas.');
  });

  // --- 4. Helpers ----------------------------------------------------------

  function mostrarError(mensaje) {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: mensaje,
      confirmButtonText: 'Aceptar'
    });
  }

  function marcarInputsInvalidos() {
    [emailInput, passwordInput].forEach(el => {
      el.classList.add('is-invalid');
      el.parentElement.querySelector('.invalid-feedback')?.classList.add('d-block');
    });
  }

  function limpiarInputs() {
    [emailInput, passwordInput].forEach(el => {
      el.classList.remove('is-invalid');
      el.parentElement.querySelector('.invalid-feedback')?.classList.remove('d-block');
    });
  }
}
