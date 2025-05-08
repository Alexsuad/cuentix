#!/bin/bash


echo "📁 Creando estructura de carpetas del frontend de Cuentix..."

# 1. Crear carpetas primero
mkdir -p frontend/pages
mkdir -p frontend/partials
mkdir -p frontend/assets/css
mkdir -p frontend/assets/img
mkdir -p frontend/assets/js/modules
mkdir -p frontend/assets/js/modules/pages
mkdir -p frontend/assets/js/modules/utils
mkdir -p frontend/tests/e2e

# 2. Crear archivos vacíos
touch frontend/index.html
touch frontend/pages/{landing.html,login.html,register.html,dashboard.html,profile-new.html,wizard.html,loading.html,result.html,history.html}
touch frontend/partials/{header.html,footer.html}
touch frontend/assets/css/{styles.css,wizard.css}
touch frontend/assets/js/main.js
touch frontend/assets/js/modules/{api.js,auth.js,router.js,wizard.js,polling.js}
touch frontend/assets/js/modules/pages/{landing.js,login.js,register.js,dashboard.js,profile-new.js,wizard.js,loading.js,result.js,history.js}
touch frontend/assets/js/modules/utils/showFeedback.js
touch frontend/tests/e2e/happy_path.feature

echo "✅ Estructura del frontend creada correctamente en la carpeta 'frontend/'"

# Archivos HTML
touch frontend/pages/{landing.html,login.html,register.html,dashboard.html,profile-new.html,wizard.html,loading.html,result.html,history.html}
touch frontend/partials/{header.html,footer.html}
touch frontend/index.html

# Archivos CSS
touch frontend/assets/css/{styles.css,wizard.css}

# Archivos JS
touch frontend/assets/js/main.js
touch frontend/assets/js/modules/{api.js,auth.js,router.js,wizard.js,polling.js}
touch frontend/assets/js/modules/pages/{landing.js,login.js,register.js,dashboard.js,profile-new.js,wizard.js,loading.js,result.js,history.js}
touch frontend/assets/js/modules/utils/showFeedback.js

# Tests
touch frontend/tests/e2e/happy_path.feature

echo "✅ Estructura del frontend creada en la carpeta 'frontend/'"
