# 🧠 CUENTIX – Plataforma de Video-Cuentos Personalizados con IA

**Cuentix** es una aplicación web que permite generar video-cuentos infantiles personalizados, combinando tecnologías de inteligencia artificial (texto, imagen, audio y video) en un flujo completamente automatizado y modular.

---

## 🚀 Estado del Proyecto

✅ MVP funcional completo (junio 2025)  
✅ Backend con Flask + IA multimedia (texto, imagen, audio, subtítulos, video)  
✅ Frontend modular, validado y conectado  
✅ Integración con DeepSeek, DALL·E, OpenAI, ElevenLabs y Whisper  
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
- SQLite (modo local) / PostgreSQL (modo producción)
- DeepSeek (`deepseek-chat-v2`) para generación de texto
- DALL·E 3 (`claymation digital 3D`) para imágenes
- OpenAI Text-to-Speech y ElevenLabs para voz
- gTTS (alternativa de voz)
- Whisper (para subtítulos en `.srt` y `.json`)
- MoviePy + ffmpeg para ensamblaje de video
- DiskCache (caché de escenas)
- dotenv + Pydantic (configuración robusta)

---

## 🧱 Estructura general del repositorio

📁 backend/
│ ├── config/ # Variables de entorno y configuración global
│ ├── core/ # Núcleo del sistema (orquestador, lógica IA)
│ │ ├── processors/ # Módulos de generación IA (texto, audio, imagen, subtítulos)
│ │ └── prompt_builder.py # 🧩 Constructor dinámico del prompt narrativo
│ ├── models/ # ORM SQLAlchemy (Story, User, etc.)
│ ├── routes/ # Blueprints de Flask (auth, stories, perfiles)
│ ├── utils/ # Utilidades compartidas (logger, cache, validaciones)
│ └── app.py # Punto de entrada Flask (registrador de rutas y CORS)
📁 frontend/
│ ├── assets/ # CSS, JS y recursos multimedia
│ ├── pages/ # HTML por página (login, registro, generar, historial)
│ ├── partials/ # Header y footer dinámicos
│ └── index.html # Página principal
📁 scripts/ # Scripts de desarrollo (verificación estructura)
📄 run_dev.py # Lanza verificación + servidor Flask (modo desarrollo)
📄 requirements.txt # Dependencias del backend
📄 README.md # Este archivo

---

## ✅ Funcionalidades actuales

- [x] Registro e inicio de sesión con JWT
- [x] Validación visual de formularios en frontend
- [x] Generación completa de cuentos IA: texto → imagen → audio → subtítulos
- [x] Ensamblaje de video con zoom y sincronización
- [x] Página de historial con listado y eliminación (CRUD)
- [x] Interfaz responsive y modular
- [x] Caché automático de escenas generadas
- [x] Fallbacks inteligentes (imágenes placeholder, gTTS si falla TTS principal)
- [x] Verificación de entorno previa con `run_dev.py`

---

## 🔒 Seguridad

- Autenticación con JWT (Flask-JWT-Extended)
- Contraseñas cifradas con passlib (pbkdf2_sha256)
- Validaciones visuales y por backend
- Protección CORS activada
- Manejo robusto de errores y logs por escena

---

## 🧠 Robustez técnica

### ✔️ Flujo IA Modular y Segmentado

- Prompt dinámico generado desde `prompt_builder.py`
- DeepSeek para narrativa infantil con estructura [Intro, Conflicto, Resolución, Moraleja]
- Imagen: estilo claymation infantil (DALL·E 3)
- Voz: OpenAI TTS / ElevenLabs / gTTS
- Subtítulos: Whisper base
- Video: MoviePy (zoom-in, duración sincronizada, thumbnails)

### ✔️ Sistema de control y recuperación

- Registro de fallos por etapa con logger propio
- Módulo de fallback si falla generación de imagen o audio
- Limpieza automática de archivos temporales por sesión
- Soporte para pruebas por escena (`tests/video_generator_test.py`)

---

## 🛠️ Modo desarrollo

Ejecuta:

```bash
python run_dev.py

Este comando:

Verifica que existan las carpetas, archivos clave y claves API

Carga el entorno .env y lanza Flask en modo desarrollo

Añade automáticamente backend/ al PYTHONPATH para evitar errores de importación

📎 Repositorio público
🔗 https://github.com/Alexsuad/cuentix

📄 Licencia
Este proyecto es de uso académico y educativo.
Para uso comercial o reutilización, contacta al autor y menciona la fuente.

✍️ Autor
Alexander Suárez
Proyecto Final – Desarrollo de Aplicaciones Web
CESUR · España · Junio 2025
```
