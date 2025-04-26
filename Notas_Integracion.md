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
