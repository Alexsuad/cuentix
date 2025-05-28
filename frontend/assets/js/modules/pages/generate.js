/// archivo: assets/js/modules/pages/generate.js

import { apiClient } from '../api.js';

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('generation-form');
    const submitBtn = document.getElementById('generate-story-btn');

    const optionCards = form.querySelectorAll('.card-option');

    optionCards.forEach(card => {
        card.addEventListener('click', () => {
            const section = card.closest('section');
            section.querySelectorAll('.card-option')
                .forEach(c => c.classList.remove('is-selected'));

            card.classList.add('is-selected');

            const fieldName = section.dataset.selectionName;
            let hidden = form.querySelector(`input[name="${fieldName}"]`);

            if (!hidden) {
                hidden = document.createElement('input');
                hidden.type = 'hidden';
                hidden.name = fieldName;
                form.appendChild(hidden);
            }
            hidden.value = card.dataset.value;
        });
    });

    form.addEventListener('submit', async e => {
        e.preventDefault();

        if (!form.checkValidity()) {
            form.classList.add('was-validated');
            return;
        }

        const requiredSections = ['personaje_principal', 'lugar', 'objeto_magico', 'villano', 'tipo_final'];
        let campoFaltante = null;

        for (const campo of requiredSections) {
            if (!form.querySelector(`input[name="${campo}"]`)) {
                campoFaltante = campo;
                await Swal.fire({
                    icon: 'warning',
                    title: '¡Falta una elección!',
                    text: `Debes elegir una opción en la sección: "${campo.replace('_', ' ')}"`
                });
                return;
            }
        }

        const profileId = localStorage.getItem('profile_id');

        if (!profileId) {
            await Swal.fire({
                icon: 'error',
                title: 'Perfil no seleccionado',
                text: 'Debes seleccionar un perfil infantil antes de generar el video-cuento.'
            });
            return;
        }

        const payload = {
            profile_id: profileId,
            nombre: form.nombre.value.trim(),
            edad: Number(form.edad.value),
            personaje_principal: form.personaje_principal.value,
            lugar: form.lugar.value,
            objeto_magico: form.objeto_magico.value,
            villano: form.villano.value,
            tipo_final: form.tipo_final.value
        };

        try {
            toggleLoading(true);

            const { data } = await apiClient.post('/stories/start', payload);
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
            const backendMsg = err.response?.data?.error;
            await Swal.fire({
                icon: 'error',
                title: 'Error al generar',
                text: backendMsg || campoFaltante
                    ? `Fallo relacionado con: "${campoFaltante.replace('_', ' ')}"`
                    : 'Hubo un error inesperado. Intenta nuevamente más tarde.'
            });


        } finally {
            toggleLoading(false);
        }
    });

    function toggleLoading(isLoading) {
        submitBtn.classList.toggle('loading', isLoading);
        submitBtn.disabled = isLoading;
        submitBtn.innerHTML = isLoading
            ? `<span class="spinner-border spinner-border-sm me-2" role="status"></span> Generando…`
            : `<i class="fas fa-magic me-2"></i> Generar video-cuento`;
    }
});
