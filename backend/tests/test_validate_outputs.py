# ──────────────────────────────────────────────────────────────────────────────
# File: backend/tests/test_validate_outputs.py
# Descripción: Valida archivos generados por escena (audio, subtítulo, imagen).
# Usa pydub para duración de audio sin depender de MoviePy.
# ──────────────────────────────────────────────────────────────────────────────

import os
from pathlib import Path
from pydub import AudioSegment  # ✅ Más liviano y confiable para validar duración

# Directorios donde se almacenan los outputs del sistema
AUDIO_DIR = Path("assets/audio")
SUBT_DIR = Path("assets/subtitles")
IMG_DIR = Path("assets/images")

# Validar una escena individual (por ID)
def validar_escena(scene_id: str) -> dict:
    resultado = {}

    audio_path = AUDIO_DIR / f"{scene_id}.mp3"
    sub_path = SUBT_DIR / f"{scene_id}.srt"
    img_path = IMG_DIR / f"{scene_id}.png"

    # Audio
    if audio_path.exists():
        try:
            audio = AudioSegment.from_mp3(audio_path)
            dur = len(audio) / 1000  # milisegundos → segundos
            resultado["audio"] = f"✔️ Audio OK     ({dur:.1f}s)"
        except Exception:
            resultado["audio"] = "❌ Error al leer duración"
    else:
        resultado["audio"] = "❌ Audio faltante"

    # Subtítulo
    if sub_path.exists():
        resultado["sub"] = f"✔️ Subtítulo OK"
    else:
        resultado["sub"] = "⚠️ Subtítulo faltante"

    # Imagen
    if img_path.exists():
        resultado["img"] = f"✔️ Imagen OK    ({img_path.name})"
    else:
        resultado["img"] = "❌ Imagen faltante"

    return resultado

# Validar todas las escenas detectadas en la carpeta de audio
def validar_todas_las_escenas():
    print("\n🎯 VALIDACIÓN DE ESCENAS GENERADAS\n" + "─" * 45)

    if not AUDIO_DIR.exists():
        print("❌ No se encontró la carpeta de audio.")
        return

    archivos = list(AUDIO_DIR.glob("*.mp3"))
    if not archivos:
        print("⚠️ No hay escenas generadas aún.")
        return

    for archivo in sorted(archivos):
        scene_id = archivo.stem
        print(f"\n🔍 Escena: {scene_id}")
        resultado = validar_escena(scene_id)
        print(f"  {resultado['audio']}")
        print(f"  {resultado['img']}")
        print(f"  {resultado['sub']}")

# Punto de entrada
if __name__ == "__main__":
    validar_todas_las_escenas()
