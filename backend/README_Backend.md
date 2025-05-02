📚 README – Desarrollo Backend_2
📌 Contexto
Este backend forma parte del proyecto Cuentix, una plataforma que genera video-cuentos personalizados mediante inteligencia artificial para niños y niñas.

El desarrollo actual corresponde a la fase Backend_2, continuando el trabajo inicial.
Debe mantener compatibilidad estricta con el Frontend actual.

📂 Repositorio oficial
🔗 https://github.com/Alexsuad/cuentix

⚙️ Tecnologías principales
Python 3.10+

FastAPI (API REST principal)

SQLAlchemy + SQLite (base de datos)

JWT para autenticación y autorización

DeepSeek API (texto)

DALL·E (imágenes)

ElevenLabs y OpenAI TTS (voz)

Whisper local (subtítulos)

MoviePy (generación de clips de video)

📄 Documentación de Referencia
📄 Actualización Backend 26-04-2025

📄 Actualización Frontend 26-04-2025

Obligatorio leer ambos antes de realizar cambios.

🚦 Buenas prácticas obligatorias

Elemento Reglas
API REST Seguir estructura exacta de endpoints, métodos, request y response.
JWT Validar token en header Authorization: Bearer <token>.
Formatos Respetar estructura JSON definida por Frontend.
Errores Retornar códigos HTTP correctos + mensajes en JSON.
Modularidad Separar funcionalidades en módulos limpios.
Comentarios Código documentado línea a línea.
Pruebas Probar con Postman o Insomnia antes de cada commit.
Comunicación Avisar cualquier cambio que afecte a Frontend.
🧪 Endpoints principales de autenticación
POST /api/auth/register → Registro de usuario adulto.

POST /api/auth/login → Inicio de sesión, devuelve access_token.

Todos los endpoints protegidos requieren JWT en cabecera.

🧱 Organización de carpetas (backend)
bash
Copiar
Editar
backend/
├── main.py # Punto de entrada FastAPI
├── config/ # Configuraciones y prompts
├── core/ # Lógica central (procesadores, API clients)
├── utils/ # Herramientas auxiliares
├── tests/ # Pruebas unitarias
├── assets/ # Audios, imágenes, subtítulos, videos
├── docs/ # Documentación interna
├── .env # Variables sensibles
└── requirements.txt # Dependencias del proyecto
✅ Checklist antes de hacer un commit
¿Probaste localmente todos los endpoints afectados?

¿Validaste que el formato de respuesta es el correcto?

¿Incluiste comentarios claros en el código nuevo o modificado?

¿Notificaste a Frontend si tu cambio impacta la estructura?

¿Corriste alguna prueba rápida de integración?

¿Revisaste que no hay "hardcodeo" de claves, rutas o configuraciones?
