# crear_readme_assets.py

import os

# Lista de subcarpetas dentro de assets donde queremos agregar README.txt
subcarpetas = ["audio", "images", "subtitles", "Text", "video"]

# Ruta base del proyecto
ruta_assets = os.path.join("assets")

# Contenido que tendrá cada README.txt
contenido_readme = (
    "Esta carpeta contiene los archivos generados automáticamente por el sistema Cuentix.\n"
    "No modificar ni borrar manualmente los contenidos.\n"
)

# Crear el archivo README.txt en cada subcarpeta
for carpeta in subcarpetas:
    ruta_carpeta = os.path.join(ruta_assets, carpeta)
    ruta_readme = os.path.join(ruta_carpeta, "README.txt")

    # Crear el archivo solo si no existe
    if not os.path.exists(ruta_readme):
        with open(ruta_readme, "w", encoding="utf-8") as f:
            f.write(contenido_readme)
        print(f"✅ README.txt creado en: {ruta_carpeta}")
    else:
        print(f"ℹ️ Ya existe README.txt en: {ruta_carpeta}")

