# 🧠 CUENTIX – Plataforma de Video-Cuentos Personalizados con IA

Cuentix es una aplicación web que permite generar video-cuentos infantiles personalizados, combinando tecnologías de inteligencia artificial (texto, imagen, audio y video) en un flujo completamente automatizado.

---

## 🚀 Estado del Proyecto

✅ MVP funcional completo (junio 2025)  
✅ Backend con Flask + IA multimedia  
✅ Frontend modular y conectado  
📦 Flujo validado: texto → imagen → audio → subtítulos → video final

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
- Flask-CORS (conexión frontend-backend)
- SQLAlchemy ORM
- SQLite (local) / PostgreSQL (producción)
- DeepSeek (texto IA)
- DALL·E (imágenes IA)
- OpenAI TTS y ElevenLabs (voz IA)
- Whisper (subtítulos IA)
- MoviePy + ffmpeg (video)
- gTTS (voz alternativa)
- DiskCache (caché de escenas)
- dotenv + Pydantic (configuración)

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

- [x] Registro e inicio de sesión con JWT y base de datos
- [x] Validación visual de formularios en frontend
- [x] Generación completa del cuento (texto → imagen → audio → subtítulos)
- [x] Ensamblaje en video con MoviePy
- [x] Página de historial con CRUD de cuentos
- [x] Interfaz responsive y modular
- [x] Conexión estable entre frontend y backend
- [x] Fallbacks inteligentes (placeholder, gTTS)

---

## 🔒 Seguridad

- Autenticación JWT
- Contraseñas con passlib (pbkdf2_sha256)
- Protección CORS
- Validaciones backend y frontend
- Manejo robusto de errores

---

## 📎 Repositorio público

🔗 [https://github.com/Alexsuad/cuentix](https://github.com/Alexsuad/cuentix)

---

## 🧠 Robustez técnica (MVP)

### ✔️ Flujo IA Modular

- IA de texto: DeepSeek con prompt personalizado
- Imagen: DALL·E con estilo claymation infantil
- Audio: OpenAI TTS + fallback con gTTS o ElevenLabs
- Subtítulos: Whisper base + conversión a SRT/JSON
- Video: Ensamblaje sincronizado con MoviePy

### ✔️ Control de errores

- Errores por etapa registrados en base de datos
- Fallback si falla una escena (imagen o audio)
- Archivos temporales organizados en `assets/`

---

## 📄 Licencia

Este proyecto es de uso académico y educativo. Si deseas reutilizarlo, por favor contacta al autor y cita correctamente.

---

## ✍️ Autor

**Alexander Suárez**  
Proyecto de Fin de Grado – Desarrollo de Aplicaciones Web  
CESUR · España · Junio 2025
