/*  ---------------------------------------------------------------------------
    frontend/assets/js/modules/pages/login.js
    Controla el formulario de inicio de sesión en login.html
    ---------------------------------------------------------------------------
    ► 1. Importa la función loginUsuario() desde api.js  (capa de comunicación)
    ► 2. Valida el formulario con HTML5  + clases Bootstrap "was-validated"
    ► 3. Si el backend confirma, guarda el JWT en localStorage → cuentix_token
    ► 4. Maneja errores con SweetAlert2 y marca los <input> como inválidos
---------------------------------------------------------------------------- */

import { loginUsuario } from '../../api.js';   // ruta relativa: 2 niveles arriba
import Swal from 'sweetalert2';               // SweetAlert2 ya está cargado vía CDN

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
    evt.stopPropagation();  // Frenamos burbujeo (Bootstrap)

    // 2-A. Validación nativa HTML5
    if (!form.checkValidity()) {
      form.classList.add('was-validated'); // activa estilos de error de Bootstrap
      return;                              // aborta si hay errores
    }

    // 2-B. Limpiamos estados de error previos
    [emailInput, passwordInput].forEach(el => {
      el.classList.remove('is-invalid');
      el.parentElement.querySelector('.invalid-feedback')?.classList.remove('d-block');
    });

    // --- 3. Llamada al backend a través de api.js --------------------------
    const ok = await loginUsuario(emailInput.value.trim(), passwordInput.value);

    if (ok) {
      /* Login correcto ➜ feedback y redirección */
      Swal.fire({
        icon: 'success',
        title: '¡Bienvenido/a!',
        text: 'Redirigiendo a tu panel…',
        timer: 1500,
        showConfirmButton: false
      });

      setTimeout(() => window.location.href = 'dashboard.html', 1600);
      return;
    }

    /* Si la función devolvió false significa credenciales incorrectas */
    marcarInputsInvalidos();
    mostrarError('Correo o contraseña incorrectos.');
  });

  // --- 4. Helpers ----------------------------------------------------------

  /** Muestra alerta de error genérica */
  function mostrarError(mensaje) {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: mensaje,
      confirmButtonText: 'Aceptar'
    });
  }

  /** Añade la clase .is-invalid a email y password */
  function marcarInputsInvalidos() {
    [emailInput, passwordInput].forEach(el => {
      el.classList.add('is-invalid');
      el.parentElement.querySelector('.invalid-feedback')?.classList.add('d-block');
    });
  }
}
