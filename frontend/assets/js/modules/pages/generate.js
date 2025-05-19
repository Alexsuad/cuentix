/// archivo: assets/js/modules/pages/generate.js
// ────────────────────────────────────────────────────────────────────
//  Módulo de selección interactiva y envío para generate.html
//  - Permite elegir opciones visuales (personaje, lugar, etc.).
//  - Valida el formulario y lanza la petición POST /api/stories/start.
//  - Requiere: apiClient (Axios con baseURL y JWT interceptor) y SweetAlert2.
// ────────────────────────────────────────────────────────────────────

import { apiClient } from '../api.js';           // 1 nivel arriba desde /pages/


document.addEventListener('DOMContentLoaded', () => {
    /* ------------------------- SELECCIÓN DE OPCIONES ------------------------ */

    const form = document.getElementById('generation-form');
    const submitBtn = document.getElementById('generate-story-btn');

    /* 1. localizamos TODAS las tarjetas clicables de esta página */
    const optionCards = form.querySelectorAll('.card-option');

    /* 2. añadimos el listener a cada tarjeta */
    optionCards.forEach(card => {
        card.addEventListener('click', () => {
            /* ── a) quitar selección previa SOLO dentro de la misma sección ── */
            const section = card.closest('section');
            section.querySelectorAll('.card-option')
                .forEach(c => c.classList.remove('is-selected'));

            /* ── b) marcar la tarjeta clicada ── */
            card.classList.add('is-selected');

            /* ── c) guardar el valor para el backend ── */
            const fieldName = section.dataset.selectionName;      // ej. "personaje"
            let hidden = form.querySelector(`input[name="${fieldName}"]`);

            if (!hidden) {                                        // si no existe, lo creamos
                hidden = document.createElement('input');
                hidden.type = 'hidden';
                hidden.name = fieldName;
                form.appendChild(hidden);
            }
            hidden.value = card.dataset.value;                    // ej. "superheroe"
        });
    });
    /* ----------------------------------------------------------------------- */


    /* ------------------------- ENVÍO DEL FORMULARIO ------------------------- */
    form.addEventListener('submit', async e => {
        e.preventDefault();

        // Validación HTML5 (edad 4-8 y nombre requerido)
        if (!form.checkValidity()) {
            form.classList.add('was-validated');
            return;
        }

        // Validar que cada sección tenga una opción seleccionada
        const requiredSections = ['personaje', 'lugar', 'objeto_magico', 'villano', 'tipo_final'];
        for (const campo of requiredSections) {
            if (!form.querySelector(`input[name="${campo}"]`)) {
                await Swal.fire({
                    icon: 'warning',
                    title: '¡Falta una elección!',
                    text: 'Por favor elige una opción en cada sección antes de continuar.'
                });
                return;
            }
        }

        /* ---------- Construir el payload ---------- */
        const payload = {
            nombre: form.nombre.value.trim(),
            edad: Number(form.edad.value),
            tema: form.tema.value.trim() || null,
            personaje: form.personaje.value,
            lugar: form.lugar.value,
            objeto_magico: form.objeto_magico.value,
            villano: form.villano.value,
            tipo_final: form.tipo_final.value
        };

        /* ---------- Enviar al backend ---------- */
        try {
            toggleLoading(true);

            const { data } = await apiClient.post('/api/stories/start', payload); // ← JWT se añade solo
            const storyId = data.story_id;

            await Swal.fire({
                icon: 'success',
                title: '¡Magia en proceso!',
                text: 'Estamos creando tu video-cuento. Te llevaremos a la pantalla de carga.',
                timer: 1800,
                showConfirmButton: false
            });

            window.location.href = `/pages/loading.html?id=${storyId}`;

        } catch (err) {
            console.error('[generate.js] Error:', err);
            await Swal.fire({
                icon: 'error',
                title: 'No se pudo iniciar la historia',
                text: err?.response?.data?.error || err.message || 'Intenta nuevamente más tarde.'
            });

        } finally {
            toggleLoading(false);
        }
    });

    /* --------------------------- HELPER: Loading ---------------------------- */
    function toggleLoading(isLoading) {
        submitBtn.classList.toggle('loading', isLoading);
        submitBtn.disabled = isLoading;
        submitBtn.innerHTML = isLoading
            ? `<span class="spinner-border spinner-border-sm me-2" role="status"></span> Generando…`
            : `<i class="fas fa-magic me-2"></i> Generar video-cuento`;
    }
});
/// EOF generate.js
