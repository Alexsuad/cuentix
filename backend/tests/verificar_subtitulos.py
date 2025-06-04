# tests/verificar_subtitulos.py
# ──────────────────────────────────────────────────────────────
# File: tests/verificar_subtitulos.py
# Descripción: Script manual de prueba para inspeccionar y validar
# la conversión de un archivo .srt a formato JSON. Permite visualizar
# la estructura resultante para verificar la sincronización de subtítulos.
#
# Requiere que haya al menos un archivo .srt en: assets/subtitles/
#
# ▶️ Uso:
# Ejecutar desde terminal:
#     python tests/verificar_subtitulos.py
#
# El script selecciona automáticamente el archivo .srt más reciente.
# ──────────────────────────────────────────────────────────────


import os
import glob
from core.processors.subtitles_utils import srt_to_json_simple

# Ruta al directorio de subtítulos
SUBTITLES_DIR = "assets/subtitles/"

# Buscar el último archivo .srt creado
archivos_srt = sorted(
    glob.glob(os.path.join(SUBTITLES_DIR, "*.srt")),
    key=os.path.getmtime,
    reverse=True
)

if not archivos_srt:
    print("❌ No se encontró ningún archivo .srt en assets/subtitles/")
    exit(1)

ruta_srt = archivos_srt[0]
print(f"📄 Archivo SRT más reciente: {ruta_srt}")

# Convertir a JSON
subtitulos = srt_to_json_simple(ruta_srt)

print(f"\n🎞️ Subtítulos detectados: {len(subtitulos)}\n")
for i, seg in enumerate(subtitulos, 1):
    print(f"  {i}. [{seg['start']} → {seg['end']}] {seg['text']}")
