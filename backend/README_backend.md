# ⚙️ Backend – Cuentix

Este backend forma parte del proyecto **Cuentix**, una plataforma que genera video-cuentos infantiles personalizados utilizando inteligencia artificial. Gestiona tanto la lógica de autenticación como la generación automática del contenido (texto, imágenes, audio, subtítulos y video), y ofrece una API REST para interactuar con el frontend.

---

## 🔧 Tecnologías principales

- **Python 3.10+**
- **Flask** (API REST principal)
- **SQLAlchemy + SQLite** (base de datos relacional)
- **JWT** para autenticación y autorización
- **DeepSeek API** – generación de texto
- **OpenAI API** – generación de imágenes y voz (TTS)
- **ElevenLabs API** – voz expresiva para cuentos
- **gTTS** – motor de respaldo de texto a voz
- **Whisper (OpenAI)** – subtítulos automáticos por escena
- **MoviePy + ffmpeg** – ensamblaje de clips de video
- **DiskCache** – almacenamiento temporal eficiente
- **dotenv + Pydantic** – gestión de variables sensibles

---

## 📁 Estructura del Backend

```
backend/
├── main.py                     # Punto de entrada del servidor Flask
├── config/                     # Configuración y rutas internas
│   ├── prompts.py              # Prompts base y dinámicos
│   └── settings.py             # Variables de entorno (usando Pydantic)
├── core/                       # Lógica principal del pipeline de IA
│   ├── apis/                   # Clientes de API externos (OpenAI, DeepSeek, ElevenLabs)
│   └── processors/             # Procesadores de texto, imagen, audio, subtítulos, video
├── models/                     # Modelos SQLAlchemy: User, ChildProfile, Story
├── routes/                     # Endpoints REST: auth, story, status, download
├── utils/                      # Funciones auxiliares: logs, validaciones, helpers
├── tests/                      # Pruebas unitarias y de integración
├── assets/                     # Carpeta donde se guardan los recursos generados
│   ├── audio/
│   ├── images/
│   ├── subtitles/
│   ├── Text/
│   └── video/
├── docs/                       # Documentación técnica e integración frontend-backend
├── requirements.txt
├── .env                        # Variables de entorno (no subir al repo)
```

---

## 🔐 Variables de entorno requeridas

```env
DEEPSEEK_API_KEY=tu_clave
OPENAI_API_KEY=tu_clave
ELEVENLABS_API_KEY=tu_clave
WHISPER_MODEL_SIZE=base
```

---

## 🔁 Endpoints principales

| Método | Ruta                  | Descripción                                 |
|--------|------------------------|---------------------------------------------|
| POST   | /api/auth/register     | Registro de usuario adulto con JWT          |
| POST   | /api/auth/login        | Inicio de sesión, devuelve access_token     |
| POST   | /api/start             | Inicia la generación de cuento              |
| GET    | /api/status/<story_id> | Consulta estado del cuento                  |
| GET    | /api/download/<story_id> | Descarga el video generado                 |
| GET    | /api/stories/<user_id> | Obtiene todas las historias del usuario     |
| DELETE | /api/stories/<story_id>| Elimina la historia y sus archivos          |

Todas las rutas protegidas requieren **JWT** válido en la cabecera:
```
Authorization: Bearer <access_token>
```

---

## ✅ Buenas prácticas de desarrollo

- Seguir estructura modular por carpetas: `core/`, `routes/`, `models/`, `config/`
- Validar tokens con `@jwt_required()`
- Retornar siempre respuestas en JSON con códigos HTTP correctos
- Probar cada endpoint en **Postman** o **Insomnia** antes de hacer `commit`
- Registrar errores en base de datos (campo `error_message` en `Story`)
- Documentar funciones importantes con comentarios claros

---

## 🧪 Pruebas

```bash
pytest tests/ -v
```

Se recomienda probar:
- Generación de texto, imágenes y audios por separado
- Flujo completo con `main.py` desde consola
- Casos de error controlado (clave inválida, fallo de red, etc.)

---

## 📌 Cómo ejecutar localmente

```bash
# Activar entorno virtual
source backend/venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor Flask
python main.py
```

---

## 📝 Checklist antes de hacer commit

- [ ] ¿Probaste todos los endpoints localmente?
- [ ] ¿Validaste el formato de respuesta esperada (JSON)?
- [ ] ¿Incluiste comentarios útiles en funciones nuevas?
- [ ] ¿Notificaste a frontend si el cambio afecta la estructura?
- [ ] ¿No dejaste claves duras ni rutas locales absolutas?

---

## 👨‍💻 Autor

Desarrollado por **Alexander Suárez**  
Proyecto de Grado – Técnico en Desarrollo de Aplicaciones Web  
CESUR · España · 2025
