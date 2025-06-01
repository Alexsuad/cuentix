# ⚙️ Backend – Cuentix

Este backend forma parte del proyecto **Cuentix**, una plataforma que genera video-cuentos infantiles personalizados utilizando inteligencia artificial. Gestiona tanto la lógica de autenticación como la generación automática del contenido (texto, imágenes, audio, subtítulos y video), y ofrece una API REST modular, segura y conectada con el frontend.

---

## 🚀 Estado del Backend (Junio 2025)

✅ MVP funcional completo validado con pruebas reales.  
✅ Flujo de generación modular: texto, imagen, audio, subtítulos, video.  
✅ Fallback robusto: si falla una parte, se continúa el flujo.  
✅ Base de datos real con usuarios, perfiles y cuentos.  
📦 Preparado para entrega académica final.

---

## 🔧 Tecnologías principales

- **Python 3.10+**
- **Flask** (API REST principal)
- **SQLAlchemy + SQLite** (modo local) / PostgreSQL (modo producción)
- **JWT** para autenticación y autorización
- **DeepSeek API** – generación de texto
- **OpenAI API** – imágenes y voz (TTS)
- **ElevenLabs API** – voz natural alternativa
- **gTTS** – motor de respaldo
- **Whisper (OpenAI)** – subtítulos automáticos
- **MoviePy + ffmpeg** – ensamblaje de video
- **DiskCache** – caché local de imágenes y audios
- **dotenv + Pydantic** – configuración segura
- **Passlib** – hasheo de contraseñas
- **Flask-CORS** – gestión de CORS en desarrollo

---

## 📁 Estructura general

```
backend/
├── main.py                  # Punto de entrada Flask
├── config/                  # Configuración y prompts base
├── core/
│   ├── apis/                # Clientes: OpenAI, ElevenLabs, DeepSeek
│   └── processors/          # Generadores: texto, imagen, audio, subtítulos, video
├── models/                 # SQLAlchemy: User, ChildProfile, Story
├── routes/                 # Endpoints: auth, profiles, stories
├── utils/                  # Helpers, logs, validaciones
├── assets/                 # Archivos generados por historia
│   ├── images/ │ audio/ │ subtitles/ │ text/ │ videos/
├── docs/                   # Documentación técnica
├── requirements.txt
└── .env                    # Variables de entorno (no subir)
```

---

## 🔐 Variables de entorno requeridas

```env
DEEPSEEK_API_KEY=...
OPENAI_API_KEY=...
ELEVENLABS_API_KEY=...
WHISPER_MODEL_SIZE=base
```

---

## 🗃️ Modelo de datos

- `User` → adulto autenticado
- `ChildProfile` → perfiles por niño (solo en versión extendida)
- `Story` → cuento generado: campos incluyen rutas, estado y errores

> En el MVP actual, se usa `User` y `Story`, y se permite personalizar el cuento sin perfil infantil obligatorio.

---

## 📡 API REST

- `/auth/*` → login, registro (sin perfil infantil obligatorio)
- `/stories/start` → inicia generación
- `/stories/status/<id>` → consulta estado
- `/stories/download/<id>` → descarga video
- `/stories/<email>` → historial por usuario
- `/stories/delete/<id>` → elimina cuento

🔐 Todos los endpoints relevantes usan JWT. CORS activo entre frontend (5501) y backend (5000).

---

## 🧠 Flujo técnico completo (por escena)

1. Generar texto con DeepSeek (prompt base + dinámico)
2. Generar imagen con DALL·E (o usar placeholder si falla)
3. Generar audio con OpenAI → fallback a gTTS si hay error
4. Subtítulos con Whisper (opcional)
5. Ensamblaje final con MoviePy (opcional)

> Cada escena es independiente. Se registra cualquier error sin detener el flujo.

---

## 🧪 Pruebas y validaciones

```bash
python tests/video_generator_test.py
```

- Escenario de prueba: genera una escena completa con todos los pasos.
- Logging detallado por módulo.
- Errores simulados y fallback verificado.

---

## 📎 Documentación técnica

- `docs/ER_Cuentix.png` → relaciones lógicas actuales
- `docs/cambio_estrategia_mayo2025.md` → simplificación del MVP
- `docs/notas_integracion_frontend_backend.txt` → endpoints y autenticación

---

## 🧩 Buenas prácticas

- Estructura modular mantenida por carpeta
- Comentarios técnicos explicativos en cada archivo `.py`
- Manejo de errores detallado y logs por componente
- Prompts gestionados como plantilla editable
- Fallback y robustez priorizados

---

## 🧠 Autor

**Alexander Suárez**  
Proyecto de Grado – Técnico en Desarrollo de Aplicaciones Web  
CESUR · España · 2025
