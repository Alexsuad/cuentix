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

# 📝 Notas de Integración Backend - Frontend - Proyecto Cuentix

> Archivo para registrar todos los cambios que afectan a la integración.

---

## 26/04/2025 - Implementación de flujo de generación de video cuentos

- Se creó nuevo endpoint POST `/api/stories/start` para iniciar la generación de historias.
- El JSON enviado debe incluir los campos: nombre, edad, personaje_principal, lugar, objeto_magico, villano y tipo_final.
- Se separó el procesamiento en pasos: generación de texto → escenas → imágenes → audios → subtítulos → video final.
- El backend responde con un `story_id` y gestiona el procesamiento de forma asíncrona.
- Se implementó polling mediante GET `/api/stories/{id}/status` para consultar el estado (`pending`, `generating`, `completed`).
- Se creó endpoint `/api/stories/{id}/download` para obtener el video final generado.

**Impacto en Frontend:**

- En wizard.js, enviar el JSON con las elecciones del wizard a `/api/stories/start`.
- Implementar pantalla de carga (`loading.html`) que haga polling cada 5-10 segundos al endpoint de estado.
- Cuando el estado sea `completed`, redirigir automáticamente a `result.html?id={story_id}`.
- En `result.html`, mostrar el video usando `<video>` y habilitar botón de descarga desde el endpoint de download.
- Gestionar errores de generación mostrando modales informativos si la historia falla.

---

## 26/04/2025 - Autenticación obligatoria para historias

- Todos los endpoints de historias (`start`, `status`, `download`) requieren enviar el token JWT en el header Authorization.

**Impacto en Frontend:**

- Antes de enviar cualquier solicitud relacionada con historias, verificar la existencia del token JWT en localStorage.
- Si el token no existe, redirigir automáticamente al login.html.
- Incluir el header `Authorization: Bearer {token}` en todas las llamadas Axios relacionadas con historias.

---

## 26/04/2025 - Formato de error JSON estandarizado

- Todos los errores ahora responden en el formato:
  ```json
  {
    "error": "Mensaje de error",
    "detail": "Detalle técnico opcional"
  }
  ```

**Impacto en Frontend:**

- Actualizar el interceptor de Axios para capturar errores bajo este nuevo formato.
- Mostrar errores de manera consistente en SweetAlert2 o en mensajes visibles en la UI.
