# 📝 Notas de Integración Backend - Frontend - Proyecto Cuentix

> Archivo para registrar todos los cambios que afectan a la integración.

---

## 25/04/2025 - Ajuste en generación de historias

- Se modificó la ruta de generación: de `/api/stories` a `/api/stories/prepare`.
- El JSON de respuesta ahora incluye el campo adicional: `preview_image_url`.
- El backend ahora genera también una miniatura (`thumbnail.jpg`) en `assets/thumbnails/`.

Impacto en Frontend:

- Actualizar llamada a la API en `wizard.js`.
- Mostrar miniatura en `history.html`.

---

## 24/04/2025 - Actualización en manejo de perfiles

- El endpoint `/api/profiles` ahora requiere token obligatorio (antes era público).
- El campo `avatar_url` en perfiles ahora es obligatorio.

Impacto en Frontend:

- En `profile-new.html`, validar que se seleccione un avatar antes de enviar.

---

## 26/04/2025 - Implementación de flujo de generación de video cuentos

- Se creó nuevo endpoint POST `/api/stories/start` para iniciar la generación de historias.
- El JSON enviado debe incluir los campos: nombre, edad, personaje_principal, lugar, objeto_magico, villano y tipo_final.
- Se separó el procesamiento en pasos: generación de texto → escenas → imágenes → audios → subtítulos → video final.
- El backend responde con un `story_id` y gestiona el procesamiento de forma asíncrona.
- Se implementó polling mediante GET `/api/stories/{id}/status` para consultar el estado (`pending`, `generating`, `completed`).
- Se creó endpoint `/api/stories/{id}/download` para obtener el video final generado.

Impacto en Frontend:

- En wizard.js, enviar el JSON con las elecciones del wizard a `/api/stories/start`.
- Implementar pantalla de carga (`loading.html`) que haga polling cada 5-10 segundos al endpoint de estado.
- Cuando el estado sea `completed`, redirigir automáticamente a `result.html?id={story_id}`.
- En `result.html`, mostrar el video usando `<video>` y habilitar botón de descarga desde el endpoint de download.
- Gestionar errores de generación mostrando modales informativos si la historia falla.

---

## 26/04/2025 - Autenticación obligatoria para historias

- Todos los endpoints de historias (`start`, `status`, `download`) requieren enviar el token JWT en el header Authorization.

Impacto en Frontend:

- Antes de enviar cualquier solicitud relacionada con historias, verificar la existencia del token JWT en localStorage.
- Si el token no existe, redirigir automáticamente al login.html.
- Incluir el header `Authorization: Bearer {token}` en todas las llamadas Axios relacionadas con historias.

---

## 26/04/2025 - Formato de error JSON estandarizado

- Todos los errores ahora responden en el formato:
  {
  "error": "Mensaje de error",
  "detail": "Detalle técnico opcional"
  }

Impacto en Frontend:

- Actualizar el interceptor de Axios para capturar errores bajo este nuevo formato.
- Mostrar errores de manera consistente en SweetAlert2 o en mensajes visibles en la UI.

---

## 02/05/2025 - Gestión de Perfiles Infantiles (CRUD mínimo protegido)

- Se creó el endpoint `POST /api/profiles` para crear un perfil infantil asociado al adulto autenticado por JWT.
- Se creó el endpoint `GET /api/profiles` para listar todos los perfiles del adulto autenticado.
- Cada perfil contiene los campos: `id`, `nombre`, `edad`, `avatar_url`, `adulto_email`, `created_at`.
- El campo `adulto_email` se extrae automáticamente del token JWT (no se debe enviar desde el frontend).
- Validaciones mínimas: `nombre` y `edad` son obligatorios.

Impacto en Frontend:

- En `profile-new.html`, ya no se debe enviar manualmente el campo `adulto_email`.
- En `profile-list.html`, hacer `GET /api/profiles` para mostrar solo los perfiles del adulto autenticado.
- Todas las llamadas deben incluir el token JWT (`Authorization: Bearer {token}`).

---

## 02/05/2025 - Asociación de Historias con Perfiles Infantiles

- El endpoint `POST /api/stories/start` ahora requiere el campo `profile_id` para asociar la historia al niño/a correspondiente.
- Se valida que el `profile_id` pertenezca al adulto autenticado.
- El campo `profile_id` se guarda en la base de datos junto con la historia.

Impacto en Frontend:

- Al iniciar la generación de un cuento, se debe haber creado y seleccionado previamente un perfil infantil.
- El campo `profile_id` debe incluirse en el JSON enviado desde el wizard a `/api/stories/start`.
- Se debe guardar el `profile_id` temporalmente en localStorage o pasarlo por URL según navegación.

---

## 02/05/2025 - Ampliación del endpoint `/api/stories/<id>/status`

- El endpoint `GET /api/stories/<story_id>/status` ahora también devuelve el campo `profile_id` asociado a la historia.

Impacto en Frontend:

- En `result.html`, se puede usar `profile_id` para mostrar el nombre/avatar del niño que pidió el cuento.
- Este campo puede ser útil para mostrar etiquetas o asociar visualmente las historias por perfil.

---

## 02/05/2025 - Endpoint de Login para adultos

- Se habilitó el endpoint `POST /api/auth/login` para simular el login de un adulto.
- Recibe un JSON con el campo `email` y devuelve un token JWT válido por 3 horas.

Ejemplo de JSON de entrada:

```json
{ "email": "adulto@ejemplo.com" }
```

Ejemplo de respuesta:

```json
{
  "access_token": "JWT...",
  "email": "adulto@ejemplo.com",
  "expires_in": 10800
}
```

Impacto en Frontend:

- En `login.html`, hacer POST a `/api/auth/login` con el email del adulto.
- Guardar el `access_token` devuelto en `localStorage` o `sessionStorage`.
- Usar este token en todas las solicitudes protegidas (`Authorization: Bearer {token}`).

---

## 02/05/2025 - Descarga del video generado

- El endpoint `GET /api/stories/<story_id>/download` permite visualizar o descargar el video generado.
- Requiere token JWT.
- El backend verifica que el estado de la historia sea `completed` y que el archivo exista físicamente antes de devolverlo.

Impacto en Frontend:

- En `result.html`, usar este endpoint para cargar el video en un elemento `<video>` o permitir la descarga.
- Mostrar un mensaje adecuado si el archivo aún no está disponible o hay un error.
