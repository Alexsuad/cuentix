// frontend/asset js/modules/auth.js
 
// - Lógica de autenticación

import { apiBaseUrl } from './api.js'; // Base de la API

// Función para iniciar sesión
export async function loginUsuario(email, password) {
  const response = await fetch(`${apiBaseUrl}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    throw new Error('Login fallido');
  }

  return response.json(); // Devolvemos el JSON con el token
}
