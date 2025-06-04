# ⚙️ Backend – Cuentix

Este backend forma parte del proyecto **Cuentix**, una plataforma que genera video-cuentos infantiles personalizados mediante inteligencia artificial. Gestiona tanto la autenticación como la lógica completa de generación (texto, imagen, audio, subtítulos, video), y expone una API REST modular, segura y conectada con el frontend.

---

## 🚀 Estado del Backend (junio 2025)

✅ MVP funcional y validado con pruebas reales  
✅ Flujo modular por escena: texto → imagen → audio → subtítulos → video  
✅ Fallback robusto: el proceso continúa si una etapa falla  
✅ Persistencia real con SQLite (modo local)  
📦 Listo para entrega académica final

---

## 🔧 Tecnologías principales

- **Python 3.10+**
- **Flask** – API REST principal
- **SQLAlchemy + SQLite** – ORM y base local (PostgreSQL en producción)
- **JWT** – Autenticación y autorización seguras
- **DeepSeek API** – Narración infantil generada por IA
- **OpenAI API** – Imágenes (DALL·E 3) y voz (TTS)
- **ElevenLabs API** – Voz alternativa de alta calidad
- **gTTS** – Motor de voz de respaldo
- **Whisper (OpenAI)** – Subtitulado automático
- **MoviePy + ffmpeg** – Ensamblaje del video final
- **DiskCache** – Caché local de escenas generadas
- **dotenv + Pydantic** – Configuración centralizada
- **Passlib** – Hasheo seguro de contraseñas
- **Flask-CORS** – Conexión frontend-backend durante desarrollo

---

## 📁 Estructura general

backend/
├── app.py # Punto de entrada principal (Flask + CORS + Blueprints)
├── main.py # Ejecutor del flujo completo (versión MVP)
├── config/ # Configuración (.env, settings.py)
├── core/
│ ├── orchestrator.py # Lanza generación en hilo separado
│ ├── story_pipeline.py # Orquestador principal (flujo completo)
│ ├── prompt_builder.py # Generador de prompts personalizados
│ └── processors/ # Generadores IA: texto, imagen, audio, subtítulos, video
├── models/ # SQLAlchemy: User, Story
├── routes/ # Endpoints: /auth, /stories
├── utils/ # Logger, caché, validaciones, helpers
├── assets/ # Archivos generados por cuento (audio, imágenes, subtítulos, videos)
├── scripts/ # run_dev.py y scripts auxiliares
├── tests/ # Pruebas unitarias y de flujo
├── docs/ # Documentación técnica
├── requirements.txt
└── .env # Variables sensibles

---

## 🔐 Variables de entorno requeridas

```env
DEEPSEEK_API_KEY=...
OPENAI_API_KEY=...
ELEVENLABS_API_KEY=...
OPENAI_PROJECT_ID=...
WHISPER_MODEL_SIZE=base


🗃️ Modelo de datos
User: Usuario autenticado (adulto)

Story: Video-cuento generado con todos los recursos asociados

En el MVP no se usa tabla de perfiles infantiles. Se permite personalización directa por nombre y edad.

📡 API REST
Método	Ruta	Descripción
POST	/auth/register	Registro de nuevo usuario
POST	/auth/login	Login con JWT
POST	/stories/start	Inicia la generación del cuento
GET	/stories/status/<story_id>	Consulta el estado del proceso
GET	/stories/download/<story_id>	Descarga el video generado
GET	/stories/<email>	Lista el historial por usuario
DELETE	/stories/delete/<story_id>	Elimina un cuento

Todos los endpoints sensibles requieren token JWT.
CORS activado para http://localhost:5501 (frontend en modo desarrollo)

🧠 Flujo técnico de generación
Genera el prompt narrativo personalizado (prompt_builder.py)

Genera el texto del cuento con DeepSeek

Divide en escenas y por cada una:

Genera imagen con DALL·E → fallback: imagen de error

Genera audio con OpenAI TTS → fallback: gTTS

Genera subtítulos con Whisper

Ensambla el video con MoviePy

Guarda rutas, estados y errores en la tabla Story

🧪 Pruebas
bash
Copiar
Editar
python backend/tests/video_generator_test.py
Simula la generación de una escena completa (texto + imagen + audio + subtítulos + video)

Usa logging por módulo

Permite probar fallbacks manualmente

📝 Scripts de desarrollo
🔹 Verificar estructura + lanzar backend
bash
Copiar
Editar
python run_dev.py
Verifica existencia de archivos esenciales y claves del .env

Configura PYTHONPATH correctamente

Lanza el servidor Flask (localhost:5000) en modo desarrollo

📎 Documentación técnica
docs/ER_Cuentix.png: Diagrama de entidades y relaciones

docs/cambio_estrategia_mayo2025.md: Versión final del MVP sin perfiles

docs/notas_integracion_frontend_backend.txt: Endpoints, autenticación, flujo de integración

✅ Buenas prácticas implementadas
Código modular y mantenible

Comentarios técnicos en formato estándar Cuentix (# File: ..., # Descripción: ...)

Manejo de errores controlado por etapa

Prompts tratados como plantillas dinámicas

Estrategia de fallback completa para cada etapa del pipeline

Caché y reutilización de escenas para evitar uso innecesario de API

✍️ Autor
Alexander Suárez
Proyecto de Grado – Técnico en Desarrollo de Aplicaciones Web
CESUR · España · 2025


```
