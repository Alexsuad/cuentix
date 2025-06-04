# ──────────────────────────────────────────────────────────────
# File: backend/tests/test_paths.py
# Descripción: Verifica que utils.paths.new_asset_path genera rutas correctas
# para los distintos tipos de assets (audio, images, subtitles, video).
# ──────────────────────────────────────────────────────────────

# backend/tests/test_paths.py

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.paths import new_asset_path



def test_ruta(tipo, archivo):
    try:
        ruta = new_asset_path(tipo, archivo)
        assert ruta.endswith(archivo), "El nombre del archivo no coincide"
        assert os.path.dirname(ruta).endswith(tipo), "La subcarpeta no es la esperada"
        print(f"✅ {tipo.upper()} → {ruta}")
    except Exception as e:
        print(f"❌ Error en tipo '{tipo}': {e}")


if __name__ == "__main__":
    test_ruta("audio", "test_audio.mp3")
    test_ruta("images", "test_img.png")
    test_ruta("subtitles", "test.srt")
    test_ruta("videos", "test_video.mp4")

    # Caso de error esperado
    test_ruta("documentos", "algo.txt")  # tipo inválido
