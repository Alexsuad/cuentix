# backend/tests/video_generator_test.py

import os
import numpy as np
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx import resize, margin  # ✅ Importación correcta en MoviePy 2.x

# Ruta del archivo de audio (ya debe existir)
RUTA_AUDIO = "assets/audio/test.mp3"

# Verificar existencia del audio
if not os.path.exists(RUTA_AUDIO):
    print(f"❌ Audio no encontrado: {RUTA_AUDIO}")
    exit(1)

# Crear imagen blanca de fondo (numpy array)
imagen_array = np.ones((720, 1280, 3), dtype=np.uint8) * 255
imagen_clip = ImageClip(imagen_array).set_duration(3)  # Clip de 3 segundos

# Cargar audio
audio_clip = AudioFileClip(RUTA_AUDIO)

# Asignar audio y redimensionar imagen a 720p
imagen_clip = resize.resize(
    imagen_clip.with_duration(audio_clip.duration)
               .with_audio(audio_clip),
    height=720
)

# Crear subtítulo
subtitulo = TextClip(
    text="Esto es una prueba",
    font="DejaVuSans-Bold",      # Asegúrate de que esté instalada o cámbiala
    font_size=30,
    color="white",
    method="caption",
    size=(1080, None)
).with_duration(audio_clip.duration) \
 .with_position(("center", "bottom"))

# Añadir margen inferior
subtitulo = margin.margin(subtitulo, bottom=30)

# Componer el video final
video = CompositeVideoClip([imagen_clip, subtitulo])

# Definir ruta de salida
ruta_salida = "assets/videos/test_clip.mp4"
os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

# Guardar el archivo de video
video.write_videofile(ruta_salida, fps=24)

# Cerrar audio para liberar recursos
audio_clip.close()

print("✅ Video de prueba generado:", ruta_salida)
