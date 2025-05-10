# 📁 Estructura del Frontend - Proyecto Cuentix

Este directorio contiene todos los archivos y recursos relacionados con la interfaz web de Cuentix. La estructura ha sido diseñada para favorecer la organización, modularidad y escalabilidad del sistema.

---

## 🗂 Estructura General

frontend/
│
├── index.html # Página de entrada general (opcional redirección a landing)
│
├── pages/ # Páginas principales del sistema (una por vista)
│ ├── landing.html
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ ├── profile-new.html
│ ├── wizard.html
│ ├── loading.html
│ ├── result.html
│ └── history.html
│
├── partials/ # Fragmentos reutilizables
│ ├── header.html
│ └── footer.html
│
├── assets/ # Recursos estáticos
│ ├── css/
│ │ ├── styles.css # Estilos globales
│ │ └── wizard.css # Estilos específicos para el wizard
│ ├── img/ # Imágenes (dividir por avatars, opciones, thumbnails, etc.)
│ └── js/ # Scripts de frontend
│ ├── main.js # Punto de entrada principal
│ └── modules/ # Lógica modular JS
│ ├── api.js # Comunicación con APIs backend
│ ├── auth.js # Manejo de autenticación (JWT, login)
│ ├── router.js # Lógica de navegación si aplica
│ ├── wizard.js # Lógica del generador de cuentos
│ ├── polling.js # Lógica de espera y verificación de estado
│ ├── pages/ # Lógica específica por página
│ │ ├── landing.js
│ │ ├── login.js
│ │ ├── register.js
│ │ ├── dashboard.js
│ │ ├── profile-new.js
│ │ ├── wizard.js
│ │ ├── loading.js
│ │ ├── result.js
│ │ └── history.js
│ └── utils/
│ └── showFeedback.js # Utilidades generales (ej. mostrar mensajes, loaders, etc.)
│
└── tests/e2e/
└── happy_path.feature # Guión de prueba E2E del flujo principal (estilo Gherkin)


---

## 📌 Consideraciones

- Cada archivo `.js` bajo `modules/pages/` exportará una función `initPage()` que será llamada por `main.js`.
- El código está organizado siguiendo el principio de separación de responsabilidades.
- Las páginas usan `partials/header.html` y `footer.html` para evitar duplicación de contenido.
- Las imágenes se dividirán posteriormente en subcarpetas como `avatars/`, `options/` y `thumbnails/`.

---

## 🧪 Pruebas

- El archivo `happy_path.feature` describe el flujo principal del sistema de forma legible, y será la base para implementar pruebas automatizadas con herramientas como Cypress o Playwright.

---

## ✨ Autor y Estructura diseñada por:

- Alexander (Desarrollador Frontend del Proyecto Cuentix)

