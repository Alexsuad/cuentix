// ──────────────────────────────────────────────────────────────────────────────
// File: frontend/assets/js/modules/pages/loading.js
// Propósito: Espera que la generación del cuento finalice y redirige al usuario
//            a la página de resultados, pasando la URL del video.
// Versión: 1.1.0
// ──────────────────────────────────────────────────────────────────────────────

import { getToken } from '../auth.js'; // Importa la función para obtener el token JWT
import { apiClient } from '../api.js'; // Importa apiClient para manejar las peticiones HTTP con interceptores
import Swal from '../../lib/sweetalert2/sweetalert2.js'; // Importa SweetAlert2 para mensajes de usuario

/**
 * @section InitPage Function
 * @description Inicializa la lógica de la página de carga.
 */
export function initPage() {
    const statusText = document.getElementById('loading-status');
    const token = getToken();

    // 1. Verificación de autenticación y redirección si no hay token
    // Comentario: Se usa 'apiClient' para asegurar que el token sea validado
    //             por el interceptor y redirija correctamente si expiró.
    if (!token) {
        // Redirige sin SweetAlert para una transición rápida si no hay token
        window.location.href = '/pages/login.html';
        return;
    }

    // 2. Extracción del ID del cuento desde los parámetros de la URL
    // Comentario: Asegura que haya un 'storyId' válido para iniciar el polling.
    const params = new URLSearchParams(window.location.search);
    const storyId = params.get('id');

    if (!storyId) {
        Swal.fire({
            icon: 'error',
            title: 'Error de acceso',
            text: 'ID de historia no válido. No se puede verificar el estado del cuento.',
            confirmButtonText: 'Ir a Generar Cuento'
        }).then(() => {
            window.location.href = '/pages/generate.html'; // Redirige a generar si no hay ID
        });
        return;
    }

    const maxIntentos = 30; // Aumentamos los intentos por si la generación es lenta
    let intentos = 0;
    const pollingInterval = 5000; // Intervalo de 5 segundos

    /**
     * @section Verificar Estado Function
     * @description Consulta repetidamente el estado de la generación del cuento
     * al backend.
     */
    async function verificarEstado() {
        try {
            // 3. Consulta al backend usando apiClient (con JWT y manejo de 401 automático)
            // Comentario: apiClient ya maneja el encabezado de autorización y
            //             la redirección a login en caso de 401.
            const response = await apiClient.get(`/stories/${storyId}/status`);
            const data = response.data; // Axios pone la respuesta JSON en .data

            // 4. Procesamiento según el estado devuelto por el backend
            switch (data.status) {
                case 'completed':
                    statusText.textContent = '¡Listo! Redirigiendo a tu video-cuento...';
                    // Almacena la video_url en localStorage para que result.js la recupere
                    if (data.video_url) {
                        localStorage.setItem('currentStoryVideoUrl', data.video_url);
                        // Opcional: si el backend envía el texto del cuento, también almacenarlo
                        if (data.story_text) {
                            localStorage.setItem('currentStoryText', data.story_text);
                        }
                         // Opcional: si el backend envía la URL del thumbnail, también almacenarlo
                        if (data.thumbnail_url) {
                            localStorage.setItem('currentStoryThumbnailUrl', data.thumbnail_url);
                        }
                        // Opcional: si el backend envía la URL de los subtítulos (SRT o JSON), también almacenarlo
                        if (data.subtitles_url) {
                            localStorage.setItem('currentStorySubtitlesUrl', data.subtitles_url);
                        }
                        // Opcional: almacenar el ID de la historia para uso futuro en result.js (aunque ya se puede pasar por URL)
                        localStorage.setItem('currentStoryId', storyId);

                        // Redirige a result.html
                        window.location.href = '/pages/result.html'; // Ya no es necesario pasar el ID por URL si está en localStorage
                    } else {
                        // Manejo si 'completed' pero no hay video_url (debería ser un error backend)
                        Swal.fire({
                            icon: 'warning',
                            title: 'Cuento Completado, pero sin Video',
                            text: 'El cuento se ha generado, pero no se encontró la URL del video. Intenta nuevamente.',
                            confirmButtonText: 'Generar Otro Cuento'
                        }).then(() => {
                            window.location.href = '/pages/generate.html';
                        });
                    }
                    break;

                case 'failed':
                    statusText.textContent = 'La generación del cuento ha fallado. Intenta nuevamente.';
                    Swal.fire({
                        icon: 'error',
                        title: '¡Oh no!',
                        text: 'La creación de tu cuento mágico ha fallado. Por favor, intenta de nuevo.',
                        confirmButtonText: 'Reintentar'
                    }).then(() => {
                        window.location.href = '/pages/generate.html'; // Redirige a generar para reintentar
                    });
                    break;

                case 'pending':
                case 'generating':
                case 'processing_audio': // Asumiendo estados intermedios del backend
                case 'processing_images':
                case 'assembling_video':
                    // Comentario: Mostrar el progreso y el intento actual.
                    statusText.textContent = `Generando tu cuento mágico... Esto puede tardar unos segundos. (Intento ${intentos + 1} de ${maxIntentos})`;
                    if (intentos < maxIntentos) {
                        intentos++;
                        setTimeout(verificarEstado, pollingInterval); // Esperar y volver a intentar
                    } else {
                        // Comentario: Si se supera el límite de intentos, se asume un problema o lentitud excesiva.
                        statusText.textContent = 'El cuento está tardando más de lo esperado. Por favor, revisa tu historial más tarde o intenta nuevamente.';
                        Swal.fire({
                            icon: 'info',
                            title: 'Generación Lenta',
                            text: 'El cuento está tardando demasiado. Puedes revisar tu historial más tarde o intentar nuevamente.',
                            confirmButtonText: 'Ir a Historial'
                        }).then(() => {
                            window.location.href = '/pages/dashboard.html'; // O a history.html si tienes uno directo
                        });
                    }
                    break;

                default:
                    // Comentario: Manejo de estados desconocidos del backend.
                    statusText.textContent = `Estado desconocido del cuento: ${data.status}`;
                    Swal.fire({
                        icon: 'warning',
                        title: 'Estado Desconocido',
                        text: `Se recibió un estado de cuento desconocido: ${data.status}. Por favor, contacta a soporte si persiste.`,
                        confirmButtonText: 'Ok'
                    });
                    break;
            }

        } catch (err) {
            console.error('[loading.js] Error al verificar estado:', err);
            // Comentario: Mejorar el mensaje de error para el usuario y usar SweetAlert.
            let errorMessage = 'Error al contactar con el servidor.';
            if (err.response && err.response.data && err.response.data.error) {
                errorMessage = err.response.data.error; // Errores específicos del backend vía Axios interceptor
            } else if (err.message) {
                errorMessage = err.message; // Otros errores de red o JS
            }

            Swal.fire({
                icon: 'error',
                title: 'Error de Conexión',
                text: errorMessage + '\nPor favor, verifica tu conexión o intenta más tarde.',
                confirmButtonText: 'Cerrar'
            }).then(() => {
                // Opcional: redirigir a una página segura o al dashboard
                // window.location.href = '/pages/dashboard.html';
            });
        }
    }

    // 5. Inicia el ciclo de verificación
    // Comentario: Se inicia el polling inmediatamente al cargar la página.
    verificarEstado();
}