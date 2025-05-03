# 🧒 CUENTIX – Plataforma de Video Cuentos Infantiles Personalizados

Cuentix es una plataforma desarrollada en Python que automatiza la creación de video cuentos infantiles utilizando tecnologías de inteligencia artificial. A través de una interfaz sencilla y modular, el sistema genera un cuento a partir de un prompt, crea imágenes ilustrativas, narra el texto con voz artificial y une todos los elementos en un video final accesible para niños y niñas.

---

## 🚀 Características principales

- ✍️ Generación de texto con **DeepSeek Chat API**.
- 🎨 Ilustraciones automáticas con **OpenAI DALL·E**.
- 🎤 Conversión de texto a voz con soporte para tres motores:
  - ElevenLabs (voz expresiva - producción)
  - OpenAI TTS (voz natural - pruebas)
  - gTTS (Google TTS - respaldo rápido)
- 🎬 Creación de clips con MoviePy combinando audio, imagen y texto.
- 🧾 Generación de subtítulos automáticos con **Whisper**.
- 🗂️ Organización estructurada de los recursos generados.

---

## 🗂️ Estructura del Proyecto (actualizada)

```
Cuentix/
├── main.py
├── probar_audio.py
├── probar_tts_multimotor.py
├── verificar_apis.py
├── crear_readme_assets.py
├── README.md
├── requirements.txt
├── .env
├── config/
│   ├── __init__.py
│   ├── prompts.py
│   └── settings.py
├── core/
│   ├── apis/
│   │   ├── __init__.py
│   │   ├── deepseek_api.py
│   │   ├── elevenlabs_api.py
│   │   └── openai_tts_api.py
│   └── processors/
│       ├── __init__.py
│       ├── audio_generator.py
│       ├── audio_generator_openai.py
│       ├── image_generator.py
│       ├── prompt_builder.py
│       ├── subtitles_generator.py
│       ├── text_generator.py
│       └── video_generator.py
├── utils/
│   ├── __init__.py
│   ├── helpers.py
│   ├── logger.py
│   ├── openai_tools.py
│   └── verificar_openai.py
├── assets/
│   ├── audio/
│   ├── images/
│   ├── subtitles/
│   ├── Text/
│   └── video/
└── venv/
```

---

## ⚙️ Tecnologías utilizadas

- **Python 3.10+**
- **DeepSeek API**
- **OpenAI API**
- **ElevenLabs API**
- **gTTS**
- **MoviePy**
- **Whisper**
- **Pydantic + dotenv**

---

## 🔐 Variables de entorno requeridas (.env)

```env
DEEPSEEK_API_KEY=tu_clave_deepseek
OPENAI_API_KEY=tu_clave_openai
ELEVENLABS_API_KEY=tu_clave_elevenlabs
WHISPER_MODEL_SIZE=base
```

---

## 🧪 Estado del desarrollo actual

| Módulo                   | Estado           |
|--------------------------|------------------|
| Generación de texto      | ✅ Completo      |
| Generación de imágenes   | ✅ Completo      |
| Generación de audio      | ✅ Triple motor  |
| Subtítulos (Whisper)     | ✅ Implementado  |
| Video final              | ✅ Funcional     |
| Prompts dinámicos        | 🟡 En desarrollo |
| Control de sesión        | 🔲 Pendiente     |
| Frontend (UI)            | 🔲 Pendiente     |
| Conexión a base de datos | ✅ Implementado  |

---

## 📌 Cómo ejecutar

```bash
source backend/venv/bin/activate
python main.py
```

O pruebas específicas:

```bash
python probar_tts_multimotor.py
python verificar_apis.py
```

---

## 🧪 Pruebas unitarias

```
tests/
├── test_text_generator.py
├── test_audio_generator.py
├── test_image_generator.py
├── test_subtitles_generator.py
```

```bash
pytest tests/ -v
```

---

Desarrollado por Alexander Suárez – Proyecto de Grado 2025
