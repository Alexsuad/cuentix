# ──────────────────────────────────────────────────────────────────────────────
# File: backend/tests/test_reparar_batch.py
# Descripción: Script auxiliar para regenerar subtítulos de escenas cuyo audio
# ya existe pero el subtítulo está ausente. Útil cuando falla Whisper en alguna
# escena durante la generación principal.
#
# Uso recomendado:
#   ❯ python backend/tests/test_reparar_batch.py
#
# Puedes ejecutarlo desde cualquier carpeta, el path se corrige automáticamente.
# ──────────────────────────────────────────────────────────────────────────────

import os
import sys
from pathlib import Path

# --- Corrección del sys.path para importar desde backend ---
script_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(script_dir))

from config.settings import settings
from core.processors.subtitles_generator import SubtitlesGenerator

# --- Inicializar generador de subtítulos ---
sub_gen = SubtitlesGenerator()

# --- Directorios de entrada y salida ---
AUDIO_DIR = Path(settings.AUDIO_DIR)
SUBT_DIR = Path(settings.SUBTITLES_DIR)

# --- Procesar todas las escenas con audio pero sin subtítulo ---
def regenerar_subtitulos():
    print("\n♻️ Reparación de subtítulos faltantes\n" + "-" * 40)
    if not AUDIO_DIR.exists():
        print("❌ Carpeta de audio no encontrada.")
        return

    escenas = list(AUDIO_DIR.glob("*.mp3"))
    total = len(escenas)
    faltantes = 0

    for audio_file in sorted(escenas):
        scene_id = audio_file.stem
        subt_path = SUBT_DIR / f"{scene_id}.srt"
        if not subt_path.exists():
            print(f"🔄 Regenerando: {scene_id}")
            sub_gen.generar_subtitulo(str(audio_file), str(subt_path))
            faltantes += 1
        else:
            print(f"✔️ Ya existe: {scene_id}")

    print(f"\n✅ Proceso completado. Subtítulos generados: {faltantes}/{total}")

# --- Punto de entrada ---
if __name__ == "__main__":
    regenerar_subtitulos()
