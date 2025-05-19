# 🧠 CUENTIX – Plataforma de Video-Cuentos Personalizados con IA

Cuentix es una aplicación web que permite generar video-cuentos infantiles personalizados, combinando tecnologías de inteligencia artificial (texto, imagen, audio y video) en un flujo completamente automatizado.

---

## 🚀 Estado del Proyecto

🔧 Actualmente en desarrollo (Mayo 2025)  
✔️ Backend funcional con Flask, SQLAlchemy y generación multimedia  
⚙️ Frontend en fase de integración y ajustes finales  
🗃️ MVP listo para presentación académica (entrega final: 05 junio 2025)

---

## 📦 Tecnologías utilizadas

### 🔹 Frontend
- HTML5 + CSS3 modular
- JavaScript ES Modules
- Bootstrap 5.3
- Axios (cliente HTTP)
- SweetAlert2 (alertas visuales)
- AOS.js (animaciones al hacer scroll)
- FontAwesome + Bootstrap Icons

### 🔹 Backend
- Python 3.10
- Flask + Flask-JWT-Extended
- SQLAlchemy (ORM)
- SQLite (modo local) / PostgreSQL (modo producción)
- OpenAI API (texto, imágenes, voz)
- MoviePy + ffmpeg (ensamblaje de video)
- gTTS (motor de voz alternativo)
- ElevenLabs (voz premium)
- DiskCache (caché inteligente)

---

## 🧱 Estructura general del repositorio

```
📁 backend/
│   ├── config/
│   ├── core/
│   ├── models/
│   ├── routes/
│   ├── utils/
│   └── main.py
📁 frontend/
│   ├── assets/
│   ├── pages/
│   ├── partials/
│   └── index.html
📁 tests/
│   └── e2e/
📄 requirements.txt
📄 README.md
```

---

## ✅ Funcionalidades actuales

- [x] Registro e inicio de sesión con JWT
- [x] Generación de cuento personalizado con nombre y edad
- [x] IA genera texto, imágenes, audio y subtítulos automáticamente
- [x] Ensamblado del cuento en video y descarga del archivo
- [x] Página de historial con consulta y eliminación de cuentos
- [x] Interfaz responsive y modular
- [ ] Conexión total frontend-backend (en progreso)
- [ ] Flujo tipo Wizard (en pausa para post-MVP)

---

## 🔒 Seguridad

- Autenticación por JWT en todas las rutas protegidas
- Validación de datos y sanitización de entradas
- Gestión de errores con registro en base de datos

---

## 📎 Repositorio público

🔗 [https://github.com/Alexsuad/cuentix](https://github.com/Alexsuad/cuentix)

---

## ⚠️ Riesgos técnicos identificados y medidas preventivas

A lo largo del desarrollo del sistema se han identificado puntos críticos que podrían afectar la estabilidad o funcionalidad del proyecto. A continuación se describen estos posibles inconvenientes, junto con las medidas adoptadas para prevenirlos.

### 🔌 Integración Frontend–Backend

- ✅ Todos los endpoints (`/start`, `/status`, `/download`, `/auth/*`) fueron probados exitosamente con Postman antes de conectarlos al frontend.
- Se validó el envío correcto de datos desde `generate.html` y su recepción estructurada en el backend.
- Se verificaron las respuestas esperadas (`status`, `story_id`, `video_path`) y el manejo de errores.

### 🧠 Flujo de generación por IA

- Se implementó registro de errores por historia mediante el campo `error_message` en la base de datos.
- Se están probando flujos con historias incompletas para asegurar tolerancia a fallos (por ejemplo, si falla la generación de audio o imagen).

### 🗃️ Persistencia y gestión de archivos

- Se programará la función `cleanup_story_files()` para eliminar archivos temporales tras completar o eliminar una historia.
- Ya se registra el `video_path` de cada cuento para asegurar su disponibilidad desde el historial.

### 🎨 Coherencia visual en el frontend

- Se utilizan variables CSS centralizadas (`base.css`) para mantener estilos consistentes.
- Se aplica el sistema de grillas de Bootstrap para garantizar responsividad en todas las pantallas.
- Se está auditando cada página para asegurar uniformidad visual.

### 🧪 Validaciones y pruebas

- El flujo extremo a extremo ha sido validado con datos reales desde frontend simulado.
- Se ha comenzado la documentación del flujo tipo `happy_path.feature` como base para pruebas futuras.

---

## ✍️ Autor

**Alexander Suárez**  
Proyecto de Fin de Grado – Desarrollo de Aplicaciones Web  
Centro de Formación Profesional CESUR · España · Mayo 2025

---

## 📄 Licencia

Este proyecto es de uso educativo. Cualquier reproducción parcial o total debe citar correctamente al autor.
