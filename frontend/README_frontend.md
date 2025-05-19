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
│   │       ├── api.js
│   │       ├── utils/
│   │       │   ├── loadPartials.js
│   │       │   └── showFeedback.js
│   │       └── pages/          # Scripts por vista
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
- Sistema modular `initPage()` para inicializar solo el JS necesario por pantalla.
- Estilos centralizados en `base.css` y organizados por página.
- Peticiones al backend realizadas con **Axios**, gestionadas desde `api.js`.
- Retroalimentación visual con **SweetAlert2**.
- Responsive asegurado con **Bootstrap 5.3** y media queries personalizadas.

---

## 🔄 Flujo de navegación MVP

1. `landing.html` – Bienvenida
2. `login.html` o `register.html` – Acceso de usuario
3. `generate.html` – Ingreso de nombre y edad + selección de opciones visuales
4. `loading.html` – Espera mientras se genera el cuento
5. `result.html` – Visualización del cuento generado
6. `history.html` – Listado de cuentos generados y opción de eliminar

---

## 🧪 Pruebas

El archivo `happy_path.feature` define el flujo esperado de uso desde el inicio hasta el resultado. Se ha validado manualmente y se prepara su integración con herramientas de testing como Cypress o Playwright.

---

## 👨‍💻 Autor

Desarrollado por **Alexander Suárez**  
Proyecto de Grado – Técnico en Desarrollo de Aplicaciones Web  
CESUR · España · 2025
