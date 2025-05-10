
import os
from datetime import datetime

# === CONFIGURACIÓN ===
PROYECTO = os.path.basename(os.getcwd())
FECHA = datetime.now().strftime("%d-%m-%Y")
DESTINO_IA = os.path.join(os.path.expanduser("~/Documents/ExportacionesIA"), PROYECTO, FECHA)
EXTENSIONES_VALIDAS = ('.html', '.css', '.js', '.py', '.json', '.md', '.txt')

# === CREAR DESTINO ===
os.makedirs(DESTINO_IA, exist_ok=True)
print(f"📦 Exportación para IA - Proyecto: {PROYECTO}")
print(f"📂 Carpeta destino: {DESTINO_IA}\n")

# === EXPORTAR ARCHIVOS ===
exportados = 0
for root, _, archivos in os.walk("."):
    if "ExportacionesIA" in root or ".git" in root:
        continue  # Evitar recursividad y carpetas no deseadas
    for archivo in archivos:
        if archivo.endswith(EXTENSIONES_VALIDAS):
            ruta_original = os.path.join(root, archivo)
            try:
                with open(ruta_original, 'r', encoding='utf-8', errors='ignore') as f:
                    contenido = f.read()
                rel_path = os.path.relpath(ruta_original, ".")
                nueva_ruta = os.path.splitext(rel_path)[0] + ".txt"
                destino = os.path.join(DESTINO_IA, nueva_ruta)
                os.makedirs(os.path.dirname(destino), exist_ok=True)
                with open(destino, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                exportados += 1
                print(f"✅ Exportado: {rel_path}")
            except Exception as e:
                print(f"❌ Error leyendo {ruta_original}: {e}")

# === RESUMEN FINAL ===
print("\n🎉 Exportación completada.")
print(f"📄 Total de archivos exportados: {exportados}")
print(f"📁 Carpeta para revisar o copiar: {DESTINO_IA}")
print("\n🔗 Puedes abrir esta ruta desde Windows en:")
print(f"\\\\wsl$\\Ubuntu{DESTINO_IA.replace(os.path.expanduser('~'), '')}")
