# 🎨 Frontend – Cuentix

Este directorio contiene todos los archivos relacionados con la interfaz web de **Cuentix**, diseñada para ser modular, accesible y fácil de mantener. El objetivo es ofrecer una experiencia fluida y visualmente atractiva, permitiendo a los usuarios interactuar con el sistema de generación de cuentos personalizados.

---

## 🧱 Estructura del Frontend

```
frontend/
├── index.html                  # Página de entrada (redirige a landing)
│
├── pages/                      # Páginas HTML principales
│   ├── landing.html
│   ├── login.html
│   ├── register.html
│   ├── generate.html
│   ├── loading.html
│   ├── result.html
│   ├── history.html
│   └── dashboard.html          # Estructura lista, no activa en MVP
│
├── partials/                   # Fragmentos HTML reutilizables
│   ├── header.html
│   └── footer.html
│
├── assets/
│   ├── css/                    # Estilos globales y por página
│   │   ├── base.css
│   │   ├── layout.css
│   │   ├── buttons.css
│   │   ├── components.css
│   │   ├── styles.css          # Archivo principal de importación
│   │   └── pages/
│   │       ├── login.css
│   │       ├── register.css
│   │       ├── generate.css
│   │       ├── landing.css
│   │       ├── result.css
│   │       └── history.css
│   │
│   ├── js/
│   │   ├── main.js             # Carga dinámica de scripts por página
│   │   └── modules/
│   │       ├── api.js          # Cliente Axios con interceptores y loginUsuario()
│   │       ├── utils/
│   │       │   ├── loadPartials.js  # Inserta header/footer en cada página
│   │       │   └── showFeedback.js # Módulo común para SweetAlert2
│   │       └── pages/          # Scripts por vista (cada uno con initPage())
│   │           ├── login.js
│   │           ├── register.js
│   │           ├── generate.js
│   │           ├── loading.js
│   │           ├── result.js
│   │           └── history.js
│   │
│   └── img/                    # Ilustraciones, miniaturas, avatares, etc.
│
└── tests/
    └── e2e/
        └── happy_path.feature  # Flujo principal simulado (estilo Gherkin)
```

---

## 📌 Características clave

- Uso de `partials/` para evitar duplicación de contenido común (header, footer).
- Sistema modular `initPage()` que inicializa solo el JS necesario según la página activa.
- Validaciones HTML5 personalizadas combinadas con feedback visual (SweetAlert2 + Bootstrap).
- Estilos centralizados con CSS modular (`base.css`, `layout.css`, `components.css`).
- Axios configurado con interceptores para añadir el JWT automáticamente a las peticiones.
- SweetAlert2 usado en todos los flujos para feedback visual claro (éxito, error, advertencia).
- Interfaz responsive con Bootstrap 5.3 y ajustes adicionales por CSS personalizado.

---

## 🔄 Flujo de navegación MVP

1. `landing.html` – Bienvenida
2. `register.html` o `login.html` – Registro e inicio de sesión con validación visual y JWT
3. `generate.html` – Ingreso de nombre, edad y selección visual (5 secciones)
4. `loading.html` – Animación de espera mientras se genera el cuento
5. `result.html` – Visualización del video-cuento generado (con opción de descarga)
6. `history.html` – Historial de cuentos generados, con botón de eliminación

---

## 🧪 Pruebas y validaciones

- El archivo `happy_path.feature` define el flujo extremo a extremo ideal del MVP.
- Se validó el correcto uso del token `cuentix_token` y su envío automático vía `apiClient`.
- Todas las páginas HTML fueron revisadas con `F12` y validadores de accesibilidad visual.
- Se está trabajando en pruebas automatizadas con Cypress (post-MVP).

---

## 👨‍💻 Autor

Desarrollado por **Alexander Suárez**  
Proyecto de Grado – Técnico en Desarrollo de Aplicaciones Web  
CESUR · España · 2025
