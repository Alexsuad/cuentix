# 🧠 CUENTIX – Plataforma de Video-Cuentos Personalizados con IA

Cuentix es una aplicación web que permite generar video-cuentos infantiles personalizados, combinando tecnologías de inteligencia artificial (texto, imagen, audio y video) en un flujo completamente automatizado.

---

## 🚀 Estado del Proyecto

🔧 Actualmente en desarrollo (Mayo 2025)  
✅ Backend funcional con Flask, SQLAlchemy y generación multimedia  
✅ Frontend conectado con backend (registro, login, generación, historial)  
📦 MVP listo para presentación académica (entrega final: 05 junio 2025)

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
- Flask-CORS (para permitir conexión con frontend en otro puerto)
- SQLAlchemy (ORM)
- SQLite (modo local) / PostgreSQL (modo producción)
- OpenAI API (texto, imágenes, voz)
- MoviePy + ffmpeg (ensamblaje de video)
- gTTS (motor de voz alternativo)
- ElevenLabs (voz premium)
- DiskCache (caché inteligente)
- passlib (hasheo de contraseñas)

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

- [x] Registro e inicio de sesión real con base de datos y JWT
- [x] Validación visual de formularios en frontend (login y registro)
- [x] Generación de cuento personalizado con nombre, edad y opciones visuales
- [x] IA genera texto, imágenes, audio y subtítulos automáticamente
- [x] Ensamblado del cuento en video y descarga del archivo
- [x] Página de historial con consulta y eliminación de cuentos
- [x] Interfaz responsive y modular
- [x] Conexión estable frontend-backend (puerto 5501 → 5000 con CORS)
- [ ] Flujo tipo Wizard (en pausa para post-MVP)

---

## 🔒 Seguridad

- Autenticación por JWT en todas las rutas protegidas
- Verificación de email y contraseña en base de datos
- Hasheo seguro con passlib (pbkdf2_sha256)
- Protección CORS entre servidores (`localhost:5501` ↔ `localhost:5000`)
- Validación de datos y sanitización de entradas
- Gestión de errores con registro en base de datos

---

## 📎 Repositorio público

🔗 [https://github.com/Alexsuad/cuentix](https://github.com/Alexsuad/cuentix)

---

## ⚠️ Riesgos técnicos identificados y medidas preventivas

### 🔌 Integración Frontend–Backend

- ✅ Todos los endpoints (`/auth/*`, `/profiles`, `/stories`) probados con Postman y frontend
- ✅ CORS gestionado correctamente con `flask-cors`
- ✅ Peticiones `OPTIONS` eliminadas manualmente y gestionadas automáticamente

### 🧠 Flujo de generación por IA

- Registro de errores por historia (`error_message` en `Story`)
- Flujo tolerante a fallos (por ejemplo, si falla la generación de audio o imagen)

### 🗃️ Persistencia y gestión de archivos

- Ya se registra el `video_path` de cada cuento en la BD
- Se implementará `cleanup_story_files()` para eliminar temporales

### 🎨 Coherencia visual en el frontend

- Variables CSS centralizadas (`base.css`)
- Sistema de grillas de Bootstrap para responsividad
- Cada página se audita para mantener uniformidad visual y accesibilidad

### 🧪 Validaciones y pruebas

- Flujo extremo a extremo validado: `register → login → generate → loading → history`
- Documentación técnica actualizada con estructura de endpoints por módulo
- JWT probado con interceptor automático en Axios

---

## ✍️ Autor

**Alexander Suárez**  
Proyecto de Fin de Grado – Desarrollo de Aplicaciones Web  
Centro de Formación Profesional CESUR · España · Mayo 2025

---

## 📄 Licencia

Este proyecto es de uso educativo. Cualquier reproducción parcial o total debe citar correctamente al autor.
