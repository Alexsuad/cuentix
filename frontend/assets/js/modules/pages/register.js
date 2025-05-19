// frontend/assets/js/modules/pages/register.js

import { apiClient } from '../../api.js';
import Swal from 'sweetalert2';

export function initPage() {
    const form = document.getElementById('register-form');
    const passwordInput = document.getElementById('registerPassword');
    const confirmPasswordInput = document.getElementById('registerConfirmPassword');
    const passwordStrength = document.querySelector('.password-strength .progress-bar');
    const emailInput = document.getElementById('email');
    const birthDateInput = document.getElementById('birthDate');

    // 🔐 Validación de fortaleza de contraseña
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

        let valid = true;

        const pass = passwordInput.value;
        const confirm = confirmPasswordInput.value;
        const email = emailInput.value;
        const birthDate = birthDateInput.value;

        // Validar coincidencia de contraseñas
        if (pass !== confirm) {
            confirmPasswordInput.classList.add('is-invalid');
            valid = false;
        } else {
            confirmPasswordInput.classList.remove('is-invalid');
        }

        // Validar formato básico de email
        if (!/.+@.+\..+/.test(email)) {
            emailInput.classList.add('is-invalid');
            valid = false;
        } else {
            emailInput.classList.remove('is-invalid');
        }

        // Validar mayoría de edad (ej. >= 18 años)
        const today = new Date();
        const birth = new Date(birthDate);
        const age = today.getFullYear() - birth.getFullYear();
        if (age < 18 || isNaN(age)) {
            birthDateInput.classList.add('is-invalid');
            valid = false;
        } else {
            birthDateInput.classList.remove('is-invalid');
        }

        if (!form.checkValidity() || !valid) {
            form.classList.add('was-validated');
            return;
        }

        // Activar estado de carga
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Registrando...';

        // Preparar datos para enviar
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

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
            const msg = error.response?.data?.message || 'Error desconocido al registrar.';
            await Swal.fire({
                icon: 'error',
                title: 'Error',
                text: msg
            });
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-user-plus me-2"></i> Registrarse';
        }
    });
}
