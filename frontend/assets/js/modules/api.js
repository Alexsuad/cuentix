// ──────────────────────────────────────────────────────────────────────────────
//  archivo: frontend/assets/js/modules/api.js
//  Módulo central de conexión con el backend (API REST Flask)
//  - Define apiClient con Axios y baseURL común
//  - Maneja token JWT de autenticación (interceptor automático)
//  - Expone funciones reutilizables para login y endpoints futuros
// ──────────────────────────────────────────────────────────────────────────────

import axios from "https://cdn.jsdelivr.net/npm/axios@1.7.2/+esm";

// URL base de la API (ajustable si se hace deploy en otro dominio)
export const apiBaseUrl = 'http://localhost:5000/api';

// Cliente Axios con configuración predefinida
export const apiClient = axios.create({
    baseURL: apiBaseUrl,
    timeout: 10000,
    headers: { "Content-Type": "application/json" }
});

// ──────────────────────────────────────────────────────────────────────────────
//  Interceptor de petición
//  - Agrega automáticamente el token JWT a todas las rutas protegidas
//  - Exceptúa la ruta de login
// ──────────────────────────────────────────────────────────────────────────────
apiClient.interceptors.request.use(cfg => {
    const token = localStorage.getItem('cuentix_token');
    if (token && !cfg.url.includes('/auth/login')) {
        cfg.headers.Authorization = `Bearer ${token}`;
    }
    return cfg;
}, err => Promise.reject(err));

// ──────────────────────────────────────────────────────────────────────────────
//  Interceptor de respuesta
//  - Si la respuesta es 401, el token expiró o no es válido
//  - Elimina el token y redirige al login automáticamente
// ──────────────────────────────────────────────────────────────────────────────
apiClient.interceptors.response.use(
    res => res,
    err => {
        if (err.response?.status === 401) {
            localStorage.removeItem('cuentix_token');

            // MVP: Ruta absoluta fija
            window.location.href = '/frontend/pages/login.html';

            // OPCIONAL para despliegues más flexibles (Netlify, GitHub Pages, etc.):
            // const basePath = window.location.pathname.split('/pages/')[0];
            // window.location.href = `${basePath}/pages/login.html`;
        }
        return Promise.reject(err);
    }
);

// ──────────────────────────────────────────────────────────────────────────────
//  FUNCIONES EXPORTADAS
// ──────────────────────────────────────────────────────────────────────────────

/**
 * Inicia sesión con email y contraseña.
 * Llama al endpoint /api/auth/login y guarda el JWT si es exitoso.
 *
 * @param {string} email - Correo electrónico del adulto.
 * @param {string} password - Contraseña ingresada.
 * @returns {boolean} true si el login fue exitoso; false en cualquier error.
 */
export async function loginUsuario(email, password) {
    try {
        const { data } = await apiClient.post('/auth/login', { email, password });

        // ⚠️ IMPORTANTE: el backend devuelve access_token, no token
        localStorage.setItem('cuentix_token', data.access_token);

        return true;

        // ────────────────────────────────────────────────────────────────
        // OPCIONAL (Post-MVP): Para mostrar errores más específicos
        // return { ok: true, token: data.access_token };
        // ────────────────────────────────────────────────────────────────

    } catch (error) {
        console.error('[loginUsuario] Falló:', error);

        // MVP: simplemente retorna false
        return false;

        // ────────────────────────────────────────────────────────────────
        // OPCIONAL (Post-MVP): Diferenciar tipos de error
        // if (error.response) {
        //   const { status, data } = error.response;
        //   if (status === 401 || status === 400) {
        //     return { ok: false, msg: 'Credenciales incorrectas' };
        //   }
        //   return { ok: false, msg: data?.error || 'Error del servidor' };
        // }
        // return { ok: false, msg: 'Error de red o backend no disponible' };
        // ────────────────────────────────────────────────────────────────
    }
}
