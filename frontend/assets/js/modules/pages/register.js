// ────────────────────────────────────────────────────────────────────
// File: frontend/assets/js/modules/pages/register.js
// Descripción: Lógica para el formulario de registro de Cuentix
// - Validación visual y lógica personalizada
// - Envío de datos al backend con Axios (apiClient)
// - Feedback con SweetAlert2
// ────────────────────────────────────────────────────────────────────

import { apiClient } from '../api.js';

export function initPage() {
    // --- Referencias al DOM ---
    const form = document.getElementById('register-form');
    const fullNameInput = document.getElementById('fullName');
    const passwordInput = document.getElementById('registerPassword');
    const confirmPasswordInput = document.getElementById('registerConfirmPassword');
    const passwordStrength = document.querySelector('.password-strength .progress-bar');
    const emailInput = document.getElementById('email');
    const birthDateInput = document.getElementById('birthDate');
    const termsCheckbox = document.getElementById('terms');
    const submitBtn = form.querySelector('button[type="submit"]');

    // 🔐 Barra visual de fortaleza de contraseña
    passwordInput.addEventListener('input', function () {
        const password = this.value;
        let strength = 0;

        if (password.length >= 8) strength += 25;
        if (/[A-Z]/.test(password)) strength += 25;
        if (/[0-9]/.test(password)) strength += 25;
        if (/[^A-Za-z0-9]/.test(password)) strength += 25;

        passwordStrength.style.width = strength + '%';
        passwordStrength.classList.remove('bg-danger', 'bg-warning', 'bg-success');

        if (strength < 50) {
            passwordStrength.classList.add('bg-danger');
        } else if (strength < 75) {
            passwordStrength.classList.add('bg-warning');
        } else {
            passwordStrength.classList.add('bg-success');
        }
    });

    // 📤 Envío del formulario
    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        event.stopPropagation();

        limpiarCamposInvalidos(); // Reinicia errores visuales
        let valid = true;

        const pass = passwordInput.value;
        const confirm = confirmPasswordInput.value;
        const email = emailInput.value;
        const birthDate = birthDateInput.value;

        // Validación 1: Nombre obligatorio
        if (!fullNameInput.value.trim()) {
            fullNameInput.classList.add('is-invalid');
            valid = false;
        }

        // Validación 2: Contraseñas coinciden
        if (pass !== confirm) {
            confirmPasswordInput.classList.add('is-invalid');
            valid = false;
        }

        // Validación 3: Email válido
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            emailInput.classList.add('is-invalid');
            valid = false;
        }

        // Validación 4: Mayoría de edad
        const birth = new Date(birthDate);
        const today = new Date();
        const age = today.getFullYear() - birth.getFullYear() -
            (today.getMonth() < birth.getMonth() ||
                (today.getMonth() === birth.getMonth() && today.getDate() < birth.getDate()) ? 1 : 0);
        if (age < 18 || isNaN(age)) {
            birthDateInput.classList.add('is-invalid');
            valid = false;
        }

        // Validación 5: Acepta términos
        if (!termsCheckbox.checked) {
            termsCheckbox.classList.add('is-invalid');
            valid = false;
        }

        // Validación final
        if (!form.checkValidity() || !valid) {
            form.classList.add('was-validated');
            return;
        }

        // Cargando...
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Registrando...';

        // Preparar datos a enviar
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        delete data.terms; // No enviar

        try {
            const response = await apiClient.post('/auth/register', data);

            if (response.status === 200 || response.status === 201) {
                await Swal.fire({
                    icon: 'success',
                    title: '¡Registro exitoso!',
                    text: 'Tu cuenta ha sido creada. Redirigiendo a inicio de sesión...',
                    timer: 3000,
                    showConfirmButton: false
                });
                window.location.href = 'login.html';
            }

        } catch (error) {
            const msg = error.response?.data?.error || 'Error desconocido al registrar.';
            mostrarError(msg);
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-user-plus me-2"></i> Registrarse';
        }
    });

    // ──────────────── FUNCIONES AUXILIARES ────────────────

    function mostrarError(mensaje) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: mensaje,
            confirmButtonText: 'Aceptar'
        });
    }

    function limpiarCamposInvalidos() {
        [fullNameInput, emailInput, passwordInput, confirmPasswordInput, birthDateInput].forEach(el => {
            el.classList.remove('is-invalid');
        });
        termsCheckbox.classList.remove('is-invalid');
    }
}
