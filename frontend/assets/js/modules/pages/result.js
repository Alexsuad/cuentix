// ──────────────────────────────────────────────────────────────────────────────
// File: frontend/assets/js/modules/pages/result.js
// Propósito: Muestra el video-cuento generado al usuario y permite su descarga.
//            Recupera la URL del video de localStorage para su visualización.
// Versión: 1.1.0
// ──────────────────────────────────────────────────────────────────────────────

import { getToken } from '../auth.js'; // Importa la función para obtener el token de autenticación del usuario.
import { apiClient } from '../api.js'; // Importa la instancia de Axios configurada para realizar peticiones HTTP, incluyendo interceptores.
import Swal from '../../lib/sweetalert2/sweetalert2.js'; // Importa la librería SweetAlert2 para mostrar alertas y notificaciones al usuario.

/**
 * @section InitPage Function
 * @description Inicializa la lógica principal de la página de resultados.
 * Se encarga de recuperar la información del cuento generado y mostrarla.
 */
export function initPage() {
    // 1. Obtención de referencias a elementos clave del DOM.
    const videoElement = document.getElementById('cuento-video'); // Elemento <video> donde se reproducirá el cuento.
    const downloadBtn = document.getElementById('descargar-btn'); // Botón para descargar el video generado.
    const storyTitleElement = document.getElementById('story-title'); // Elemento para mostrar el título del cuento.
    const storyTextElement = document.getElementById('story-text-display'); // Elemento para mostrar el texto narrativo del cuento.

    const token = getToken(); // Obtiene el token JWT almacenado para la autenticación de la sesión.

    // 2. Verificación de la autenticación del usuario.
    // Si no hay un token presente, se redirige al usuario a la página de inicio de sesión para asegurar el acceso autorizado.
    if (!token) {
        window.location.href = '/pages/login.html';
        return; // Detiene la ejecución de la función si no hay token.
    }

    // 3. Recuperación de datos del cuento desde el almacenamiento local (localStorage).
    // Estos datos fueron guardados previamente por el módulo 'loading.js' una vez que el cuento fue generado.
    const videoUrl = localStorage.getItem('currentStoryVideoUrl');     // URL directa del archivo de video.
    const storyId = localStorage.getItem('currentStoryId');           // Identificador único del cuento.
    const storyText = localStorage.getItem('currentStoryText');       // Contenido textual completo del cuento.
    const thumbnailUrl = localStorage.getItem('currentStoryThumbnailUrl'); // URL de la imagen de miniatura del video.

    // 4. Verificación de la existencia de la URL del video.
    // Es crucial que la URL del video esté disponible para poder mostrar el cuento.
    if (!videoUrl) {
        // Se muestra un mensaje de error al usuario utilizando SweetAlert2, indicando que el video no se pudo encontrar.
        Swal.fire({
            icon: 'error',
            title: 'Video no encontrado',
            text: 'No se pudo cargar la URL del video. Por favor, intente generar un cuento nuevo.',
            confirmButtonText: 'Generar Cuento'
        }).then(() => {
            // Tras la confirmación del usuario, se redirige a la página de generación de cuentos.
            window.location.href = '/pages/generate.html';
        });
        return; // Detiene la ejecución si no hay una URL de video.
    }

    // 5. Asignación de la URL al elemento <video> para su reproducción.
    // El navegador web se encargará de cargar y reproducir el video desde la URL proporcionada.
    if (videoElement) {
        videoElement.src = videoUrl;       // Establece la fuente del video.
        videoElement.controls = true;      // Habilita los controles de reproducción nativos del navegador.
    }

    // 6. Configuración del botón de descarga.
    // Se asigna la misma URL del video al atributo 'href' del botón de descarga,
    // y se define un nombre de archivo predeterminado para la descarga.
    if (downloadBtn) {
        downloadBtn.href = videoUrl;                                   // Establece la URL para la descarga.
        downloadBtn.download = `cuento-magico-${storyId || 'generado'}.mp4`; // Define el nombre de archivo para la descarga.
    }

    // 7. Muestra el título y el texto narrativo del cuento en la página.
    // Estos elementos proporcionan contexto adicional al video-cuento.
    if (storyTitleElement) {
        storyTitleElement.textContent = `Tu Cuento Mágico: ${storyId || 'Sin Título'}`; // Asigna un título al cuento.
    }
    if (storyTextElement && storyText) {
        storyTextElement.textContent = storyText;             // Asigna el texto del cuento.
        storyTextElement.style.whiteSpace = 'pre-wrap';       // Preserva los saltos de línea y el formato del texto.
    }

    // 8. Limpieza de los datos de la historia del almacenamiento local (localStorage).
    // Esta es una buena práctica para asegurar que los datos no persistan innecesariamente
    // y que no se muestre información antigua si el usuario vuelve a la página de resultados sin generar un nuevo cuento.
    localStorage.removeItem('currentStoryVideoUrl');
    localStorage.removeItem('currentStoryId');
    localStorage.removeItem('currentStoryText');
    localStorage.removeItem('currentStoryThumbnailUrl');


    /**
     * @section Mostrar Error Function
     * @description Muestra un mensaje de error visualmente atractivo al usuario
     * y oculta los elementos de video y descarga si están presentes.
     * @param {string} mensaje - El texto del mensaje de error a mostrar al usuario.
     */
    function mostrarError(mensaje) {
        console.error('[result.js] Error al cargar o mostrar video:', mensaje); // Registra el error en la consola para depuración.

        // Oculta los elementos de video y descarga para evitar que se muestren vacíos o incorrectos.
        if (videoElement) videoElement.style.display = 'none';
        if (downloadBtn) downloadBtn.style.display = 'none';

        // Crea un nuevo elemento div para contener el mensaje de error.
        const errorContainer = document.createElement('div');
        // Asigna clases CSS para estilizar el contenedor de error (ej. Bootstrap 'alert' y clases de estilo propias).
        errorContainer.className = 'alert alert-danger text-center p-4 rounded-lg';
        errorContainer.textContent = mensaje; // Establece el texto del mensaje de error.

        // Inserta el contenedor de error en la página, antes del elemento de video si existe,
        // o al principio del cuerpo del documento como fallback.
        if (videoElement && videoElement.parentNode) {
            videoElement.parentNode.insertBefore(errorContainer, videoElement);
        } else {
            document.body.prepend(errorContainer);
        }
    }
}