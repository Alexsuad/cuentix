# probar_tts_multimotor.py

# Este archivo permite probar múltiples motores de texto a voz (TTS) en paralelo: ElevenLabs, OpenAI y gTTS.

# Compara la calidad y el funcionamiento de cada uno generando archivos de audio a partir de un mismo texto de ejemplo.

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
├── main.py                     # Punto de entrada principal del sistema. Ejecuta todo el flujo: generar texto, imágenes, audio, subtítulos y el video final.
├── probar_audio.py             # Archivo de prueba para validar individualmente la generación de audio con el motor TTS configurado.
├── probar_tts_multimotor.py   # Comparativa entre motores TTS. Este archivo permite evaluar de forma paralela la calidad y desempeño de los motores de audio disponibles (gTTS, OpenAI, ElevenLabs).
├── verificar_apis.py           # Verifica si las APIs funcionan correctamente. Comprueba la conectividad de las claves configuradas para DeepSeek, OpenAI y ElevenLabs.
├── crear_readme_assets.py      # Script auxiliar para generar archivos README.txt en carpetas vacías (audio, images, etc.), útil para mantener la estructura del proyecto.
├── README.md                   # Documentación principal del proyecto
├── requirements.txt            # Librerías necesarias
├── .env                        # Claves API y configuración general
├── config/
│   ├── __init__.py
│   ├── prompts.py              # Contiene los prompts globales y dinámicos para generar los cuentos
│   └── settings.py             # Manejo de claves API usando Pydantic para validación robusta de variables de entorno.
├── core/
│   ├── apis/
│   │   ├── __init__.py
│   │   ├── deepseek_api.py         # Cliente de API para generación de texto con DeepSeek
│   │   ├── elevenlabs_api.py       # Cliente de API para generación de voz con ElevenLabs
│   │   └── openai_tts_api.py       # Cliente de API para generación de voz con OpenAI
│   └── processors/
│       ├── __init__.py
│       ├── audio_generator.py      # Orquestador que selecciona el motor TTS y genera el audio
│       ├── audio_generator_openai.py # Implementación específica para OpenAI TTS
│       ├── image_generator.py      # Genera imágenes a partir de cada párrafo con DALL·E
│       ├── prompt_builder.py       # Construye el prompt final combinando parámetros del niño con el prompt base
│       ├── subtitles_generator.py  # Genera subtítulos .srt a partir del audio (Whisper)
│       ├── text_generator.py       # Envía el prompt al modelo y recibe el texto completo del cuento
│       └── video_generator.py      # Crea los clips de video combinando imagen, audio y texto
├── utils/
│   ├── __init__.py
│   ├── helpers.py                  # Funciones auxiliares como generación de ID únicos o limpieza de texto
│   ├── logger.py                   # Configuración de logs del sistema
│   ├── openai_tools.py             # Utilidades específicas para OpenAI
│   └── verificar_openai.py        # Verifica si la clave API de OpenAI es válida
├── assets/
│   ├── audio/                      # Audios generados por escena
│   ├── images/                     # Ilustraciones generadas
│   ├── subtitles/                  # Archivos de subtítulos .srt
│   ├── Text/                       # Texto plano del cuento generado
│   └── video/                      # Clip final del cuento
└── venv/                           # Entorno virtual local (no subir al repositorio)
```

---

## ⚙️ Tecnologías utilizadas

- **Python 3.10+**
- **DeepSeek API** – Generación de texto creativo
- **OpenAI API** – DALL·E (imágenes) + TTS (voz)
- **ElevenLabs API** – Voz realista y expresiva
- **gTTS** – Motor simple de voz para respaldo
- **MoviePy** – Generación de video a partir de clips
- **Whisper** – Transcripción automática de audio (modelo `base` usado por defecto)
- **Pydantic + dotenv** – Gestión de configuraciones

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

| Módulo                   | Estado           | Comentario                                       |
| ------------------------ | ---------------- | ------------------------------------------------ |
| Generación de texto      | ✅ Completo      | Vía DeepSeek API con prompt global               |
| Generación de imágenes   | ✅ Completo      | DALL·E vía OpenAI                                |
| Generación de audio      | ✅ Triple motor  | ElevenLabs (prod), OpenAI y gTTS (pruebas)       |
| Subtítulos (Whisper)     | ✅ Implementado  | Exporta .srt por escena                          |
| Video final              | ✅ Funcional     | Clips combinados con imagen + audio              |
| Prompts dinámicos        | 🟡 En desarrollo | Se prepara sistema con elección infantil         |
| Control de sesión        | 🔲 Pendiente     | Planeado para fase final                         |
| Frontend (UI)            | 🔲 Pendiente     | Diseño e implementación del sistema web          |
| Conexión a base de datos | 🔲 Pendiente     | Para perfiles, historiales y control de usuarios |

---

## 📌 Cómo ejecutar

1. Activa el entorno virtual:

   ```bash
   .\venv\Scripts\activate  # Windows
   ```

2. Ejecuta el proyecto principal:

   ```bash
   python main.py
   ```

3. Para probar motores de voz individualmente:

   ```bash
   python probar_tts_multimotor.py
   ```

4. Para verificar las claves API:
   ```bash
   python verificar_apis.py
   ```

---

## 📝 Próximos pasos

- Crear exportador a carpeta `/produccion/<nombre_del_cuento>`
- Permitir selección de voz/personaje en frontend
- Implementar control de sesión para adultos y niños
- Agregar exportador resumen para padres/tutores (en PDF)
- 🔧 Diseñar e implementar la interfaz frontend completa (HTML/CSS/JS)
- 🔗 Conectar el sistema a una base de datos para almacenar perfiles de usuario, cuentos y preferencias

---

## 📄 Licencia y uso

Este proyecto se desarrolla como trabajo académico y de investigación. Las tecnologías utilizadas están sujetas a sus respectivas licencias de uso. Asegúrese de revisar las políticas de uso de OpenAI, ElevenLabs, y DeepSeek al implementar en producción.

# 🧪 Pruebas Unitarias – Proyecto Cuentix

Este directorio contiene pruebas automatizadas para los módulos principales del sistema Cuentix.

Las pruebas utilizan `pytest` y están diseñadas para validar:

- ✔️ Correcta generación de texto (DeepSeek)
- ✔️ Creación de audios usando motores TTS (OpenAI, ElevenLabs, gTTS)
- ✔️ Generación de imágenes desde IA (DALL·E u otra)
- ✔️ Transcripción automática con Whisper (.srt)

---

## 📁 Estructura

```
tests/
├── __init__.py
├── test_text_generator.py
├── test_audio_generator.py
├── test_image_generator.py
├── test_subtitles_generator.py
└── README_tests.md
```

---

## ▶️ Cómo ejecutar las pruebas

1. Asegúrate de tener activado el entorno virtual:

```bash
.\venv\Scripts\activate  # Windows
```

2. Ejecuta todas las pruebas:

```bash
pytest tests/ -v
```

3. Ejecuta un archivo específico:

```bash
pytest tests/test_audio_generator.py -v
```

---

## 📦 Requisitos

- Tener las APIs configuradas en `.env`
- Librerías instaladas:

```bash
pip install pytest
```

---

## 🧹 Notas

- Algunas pruebas generan archivos temporales (`.mp3`, `.png`, `.srt`). Puedes descomentar la línea `os.remove()` para eliminarlos tras la prueba.
- Se recomienda mantener las pruebas actualizadas si se modifican los módulos principales.

---

Desarrollado por Alexander Suárez – Proyecto de Grado 2025
