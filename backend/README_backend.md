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
- **Passlib** – hasheo de contraseñas
- **Flask-CORS** – gestión de CORS para peticiones entre servidores

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
├── routes/                     # Endpoints REST: auth, story, profiles, status, download
├── utils/                      # Funciones auxiliares: logs, validaciones, helpers
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

## 🗂️ Modelo de datos y relaciones

El sistema gestiona tres entidades principales en la base de datos:

- **User**: Adulto responsable autenticado con correo y contraseña
- **ChildProfile**: Perfiles infantiles asociados a un adulto
- **Story**: Video-cuentos generados para un perfil infantil

Relaciones lógicas actuales:

| Relación             | Tipo           | Vía                                         | Estado |
| -------------------- | -------------- | ------------------------------------------- | ------ |
| User → ChildProfile  | 1 a N (lógica) | `ChildProfile.adulto_email` ↔ `User.correo` | ✅     |
| ChildProfile → Story | 1 a N (lógica) | `Story.profile_id` ↔ `ChildProfile.id`      | ✅     |

📎 Diagrama entidad-relación (ER):

![ER Cuentix](docs/ER_Cuentix.png)

---

## 📡 Endpoints REST (API Pública)

Todos los endpoints se exponen bajo `/api/` y requieren autenticación con JWT para acceder a los recursos protegidos.

### 🔐 Autenticación – `/api/auth/*`

| Endpoint         | Método | Descripción                           | JWT | Campos requeridos                              | Códigos       | Respuesta                             |
| ---------------- | ------ | ------------------------------------- | --- | ---------------------------------------------- | ------------- | ------------------------------------- |
| `/auth/register` | POST   | Registra un nuevo usuario adulto      | ❌  | `full_name`, `email`, `password`, `birth_date` | 201, 400, 409 | `msg`, o `error`                      |
| `/auth/login`    | POST   | Inicia sesión y devuelve un token JWT | ❌  | `email`, `password`                            | 200, 400, 401 | `access_token`, `email`, `expires_in` |

### 👶 Perfiles Infantiles – `/api/profiles/*`

| Endpoint    | Método | Descripción                                      | JWT | Campos requeridos               | Códigos       | Respuesta         |
| ----------- | ------ | ------------------------------------------------ | --- | ------------------------------- | ------------- | ----------------- |
| `/profiles` | GET    | Lista todos los perfiles del usuario autenticado | ✅  | —                               | 200, 500      | Lista de perfiles |
| `/profiles` | POST   | Crea un nuevo perfil infantil                    | ✅  | `nombre`, `edad`, `avatar_url?` | 201, 400, 500 | Perfil creado     |

### 🎬 Video-cuentos – `/api/stories/*`

| Endpoint                 | Método | Descripción                                            | JWT | Campos requeridos                                   | Códigos       | Respuesta        |
| ------------------------ | ------ | ------------------------------------------------------ | --- | --------------------------------------------------- | ------------- | ---------------- |
| `/stories/start`         | POST   | Inicia la generación de un cuento completo             | ✅  | `profile_id`, `nombre`, `edad`, opciones del cuento | 200, 400, 500 | `story_id`       |
| `/stories/status/<id>`   | GET    | Consulta el estado del cuento generado                 | ✅  | —                                                   | 200, 404, 500 | `status`, info   |
| `/stories/download/<id>` | GET    | Descarga el archivo final de video del cuento          | ✅  | —                                                   | 200, 404      | archivo mp4      |
| `/stories/<profile_id>`  | GET    | Lista todos los cuentos asociados a un perfil infantil | ✅  | —                                                   | 200, 404, 500 | Lista de cuentos |
| `/stories/delete/<id>`   | DELETE | Elimina un cuento generado por un perfil del usuario   | ✅  | —                                                   | 200, 403, 404 | confirmación     |

---

## 🧩 Diagrama Entidad–Relación (ER)

El siguiente diagrama representa las relaciones actuales entre los modelos clave del backend:

📎 ![Diagrama ER – Cuentix](ER_Cuentix.png)

| Entidad        | Relación                                |
| -------------- | --------------------------------------- |
| `User`         | 1 → N con `ChildProfile` (por `correo`) |
| `ChildProfile` | 1 → N con `Story` (por `profile_id`)    |

> Nota: Estas relaciones son **lógicas**, no están forzadas con claves foráneas SQL en el MVP, pero están implementadas y controladas desde los controladores usando JWT.

---

## 🌐 Servidores y configuración local

El sistema corre en dos servidores separados durante el desarrollo:

| Componente | Puerto           | Comando de inicio                               | Comentario                                   |
| ---------- | ---------------- | ----------------------------------------------- | -------------------------------------------- |
| Backend    | `localhost:5000` | `python main.py` desde `/backend`               | Ejecuta Flask y expone la API REST           |
| Frontend   | `localhost:5501` | `python3 -m http.server 5501` desde `/frontend` | Sirve los archivos HTML/CSS/JS como estático |

La configuración de CORS se maneja con `flask-cors`, habilitada para `http://localhost:5501`.

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

- [ ] ¿Se probaron todos los endpoints localmente?
- [ ] ¿Se validaron el formato de respuesta esperada (JSON)?
- [ ] ¿Se hicieron comentarios útiles en funciones nuevas?
- [ ] ¿No se dejaron claves duras ni rutas locales absolutas?

---

## 👨‍💻 Autor

Desarrollado por **Alexander Suárez**  
Proyecto de Grado – Técnico en Desarrollo de Aplicaciones Web  
CESUR · España · 2025
