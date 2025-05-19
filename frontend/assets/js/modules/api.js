// frontend/assets/js/api.js
import axios from "https://cdn.jsdelivr.net/npm/axios@1.7.2/+esm";

export const apiBaseUrl = 'http://localhost:5000/api';

export const apiClient = axios.create({
    baseURL: apiBaseUrl,
    timeout: 10000,
    headers: { "Content-Type": "application/json" }
});

apiClient.interceptors.request.use(cfg => {
    const token = localStorage.getItem('cuentix_token');
    if (token && !cfg.url.includes('/auth/login')) {
        cfg.headers.Authorization = `Bearer ${token}`;   // ← back-ticks
    }
    return cfg;
}, err => Promise.reject(err));

apiClient.interceptors.response.use(
    res => res,
    err => {
        if (err.response?.status === 401) {
            localStorage.removeItem('cuentix_token');
            window.location.href = '/frontend/pages/login.html';
        }
        return Promise.reject(err);
    }
);

/**
 * Inicia sesión.
 * @returns {boolean} true si el login fue exitoso; false en cualquier error.
 */
export async function loginUsuario(email, password) {
    try {
        const { data } = await apiClient.post('/auth/login', { email, password });
        localStorage.setItem('cuentix_token', data.token);   // clave única
        return true;
    } catch (error) {
        console.error('[loginUsuario] Falló:', error);
        return false;
    }
}
