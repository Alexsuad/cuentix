# ──────────────────────────────────────────────────────────────────────────────
# File: backend/main_mvp_audio_unico.py
# Descripción: Script principal del MVP Cuentix que genera un videocuento
# utilizando un solo audio completo, subtítulos y sincronización con imágenes.
# Diseñado para probar el pipeline de generación de forma lineal y controlada.
# ──────────────────────────────────────────────────────────────────────────────

import sys
import os
import uuid
from pathlib import Path

# ────────────────────────────────────────────────────────────────────
# Ajustar sys.path para importar módulos del backend
# Esto es necesario cuando se ejecuta el script directamente desde la terminal
# ────────────────────────────────────────────────────────────────────
# Obtener la ruta absoluta del directorio actual (donde está este script)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Subir un nivel para llegar a backend/
backend_dir = os.path.join(current_dir, '..')
# Insertar la ruta de backend al inicio del sys.path
sys.path.insert(0, backend_dir)
# ────────────────────────────────────────────────────────────────────


# ────────────────────────────────────────────────────────────────────
# Importar módulos del backend
# ────────────────────────────────────────────────────────────────────
from config.settings import settings # Configuración centralizada (rutas, claves)
from utils.logger import get_logger # Logger del proyecto
from core.processors.text_generator import TextGenerator # Genera texto del cuento
from core.processors.audio_generator import AudioGenerator # Genera audio por escena
from core.processors.subtitles_generator import SubtitlesGenerator # Genera subtítulos
from core.processors.subtitles_utils import srt_to_json_simple # Convierte SRT a JSON
from core.processors.image_generator import ImageGenerator # Genera imagen
from core.processors.video_generator_sync import crear_video_sincronizado # Ensambla video
# ────────────────────────────────────────────────────────────────────


# ────────────────────────────────────────────────────────────────────
# Inicialización
# ────────────────────────────────────────────────────────────────────
logger = get_logger(__name__) # Inicializar logger

# Asegurar que los directorios de assets existen (usando rutas de settings)
# Esto es crucial antes de intentar guardar archivos
try:
    os.makedirs(settings.AUDIO_DIR, exist_ok=True)
    os.makedirs(settings.SUBTITLES_DIR, exist_ok=True)
    os.makedirs(settings.IMAGES_DIR, exist_ok=True)
    os.makedirs(settings.VIDEOS_DIR, exist_ok=True)
    logger.info("✅ Directorios de assets verificados/creados.")
except Exception as e:
    logger.error(f"❌ Error al crear directorios de assets: {e}")
    sys.exit(1) # Salir si no se pueden crear los directorios


# Instanciar los generadores (una vez)
generador_texto = TextGenerator()
# Usar el motor de audio configurado en settings (ej: "openai", "elevenlabs", "gtts")
audio_generator = AudioGenerator(motor=settings.TTS_ENGINE)
# SubtitlesGenerator necesita ser instanciado
subtitle_generator = SubtitlesGenerator()
generador_imagen = ImageGenerator()


# ────────────────────────────────────────────────────────────────────
# Bloque de ejecución principal para pruebas desde consola
# ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logger.info("🚀 Iniciando pipeline de generación de video-cuento (MVP - Audio Único)...")

    # --- Datos simulados del usuario para pruebas ---
    # Estos datos simulan la entrada que vendría del frontend (página generate.html)
    datos_usuario = {
        "nombre": "Leo",
        "edad": 5,
        "personaje_principal": "un valiente caballero",
        "lugar": "un castillo en las nubes",
        "objeto_magico": "una espada brillante",
        "villano": "un dragón dormilón",
        "tipo_final": "un final feliz con amigos"
    }
    logger.info(f"👤 Datos de usuario de prueba: {datos_usuario}")


    # --- 1. Generar texto del cuento ---
    logger.info("1. Generando texto del cuento...")
    # generate_text usa construir_prompt_personalizado internamente con datos_usuario
    texto_cuento = generador_texto.generate_text(datos_usuario)
    if not texto_cuento or len(texto_cuento.strip()) < 50: # Validación básica de texto generado
        logger.error("❌ Fallo crítico: La generación de texto falló o el cuento es demasiado corto.")
        sys.exit(1) # Salir si la generación de texto falla
    logger.info("✅ Texto generado correctamente.")
    # Opcional: Guardar el texto generado para referencia
    # try:
    #     texto_output_path = Path(settings.TEXT_DIR) / f"cuento_{uuid.uuid4().hex[:6]}.txt"
    #     texto_output_path.write_text(texto_cuento, encoding="utf-8")
    #     logger.info(f"💾 Texto del cuento guardado en: {texto_output_path}")
    # except Exception as e:
    #     logger.warning(f"⚠️ No se pudo guardar el texto del cuento: {e}")


    # --- 2. Generar audio completo del cuento ---
    logger.info("2. Generando audio completo del cuento...")
    audio_filename = f"cuento_{uuid.uuid4().hex[:6]}.mp3"
    audio_path = Path(settings.AUDIO_DIR) / audio_filename # Construir ruta completa
    # generate_audio espera la ruta completa como string
    generated_audio_path = audio_generator.generate_audio(texto_cuento, str(audio_path))
    if not generated_audio_path:
        logger.error("❌ Fallo crítico: No se pudo generar el audio.")
        sys.exit(1) # Salir si la generación de audio falla
    logger.info(f"✅ Audio generado correctamente: {generated_audio_path}")


    # --- 3. Generar subtítulos .srt desde audio ---
    logger.info("3. Generando subtítulos desde audio...")
    srt_filename = f"subtitulos_{uuid.uuid4().hex[:6]}.srt"
    srt_path = Path(settings.SUBTITLES_DIR) / srt_filename # Construir ruta completa
    # generar_subtitulo espera la ruta del audio y la ruta de salida srt como string
    generated_srt_path = subtitle_generator.generar_subtitulo(generated_audio_path, str(srt_path))
    # Decidir si la falta de subtítulos es crítica para tu MVP.
    # Si el video DEBE tener subtítulos, salir. Si puede no tenerlos, loguear warning y continuar.
    if not generated_srt_path:
        logger.error("❌ Fallo crítico: No se pudo generar el archivo SRT.")
        sys.exit(1) # Salir si la generación de subtítulos falla
    logger.info(f"✅ Subtítulos generados correctamente: {generated_srt_path}")


    # --- 4. Convertir subtítulos a JSON para trabajar con MoviePy ---
    logger.info("4. Convirtiendo subtítulos a JSON...")
    # srt_to_json_simple espera la ruta del archivo srt como string
    subtitulos_json = srt_to_json_simple(generated_srt_path)
    # Si no hay subtítulos válidos después de parsear, no hay segmentos
    if not subtitulos_json:
        logger.error("❌ Fallo crítico: No se generaron subtítulos JSON válidos.")
        sys.exit(1) # Salir si no hay subtítulos JSON
    logger.info(f"✅ Subtítulos convertidos a JSON. Encontrados {len(subtitulos_json)} segmentos.")


    # --- 5. Generar una imagen por segmento de subtítulo ---
    logger.info("5. Generando imágenes por segmento de subtítulo...")
    image_paths = []
    # Usar ThreadPoolExecutor para paralelizar la generación de imágenes
    # Ajusta max_workers según tus recursos y límites de API concurrentes
    # Por ejemplo, 4 workers si DALL-E permite 4 peticiones concurrentes
    max_workers = 4 # Configurable si es necesario
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Crear una lista de tareas (futures) para la generación de imágenes
        # Cada tarea llama a generate_image para un segmento de subtítulo
        futures = []
        for i, segmento in enumerate(subtitulos_json):
            prompt = f"Ilustración estilo cuento infantil: {segmento['text']}" # Prompt básico por ahora
            # En versión futura: Usar prompt_image_designer(prompt) si implementas ese módulo
            image_filename = f"img_{i+1:02}_{uuid.uuid4().hex[:4]}.png" # Nombre de archivo único
            image_path = Path(settings.IMAGES_DIR) / image_filename # Construir ruta completa
            logger.info(f"🖼️ Programando generación de imagen para segmento {i+1}, ruta esperada: {image_path}")

            # Submit la tarea al executor, pasando el prompt y la ruta de salida
            future = executor.submit(generador_imagen.generate_image, prompt, str(image_path))
            futures.append(future)

        # Recopilar los resultados de las tareas (rutas de imágenes generadas)
        # Mantener el orden original de los segmentos
        generated_image_results = [f.result() for f in futures]

    # Filtrar las rutas de imágenes generadas con éxito
    image_paths = [path for path in generated_image_results if path]

    # Validar si se generó al menos una imagen
    if not image_paths:
        logger.error("❌ Fallo crítico: No se generó ninguna imagen.")
        sys.exit(1) # Salir si no se generó ninguna imagen
    logger.info(f"✅ Se generaron {len(image_paths)} imágenes correctamente.")

    # Opcional: Verificar si el número de imágenes coincide con los subtítulos
    if len(image_paths) != len(subtitulos_json):
        logger.warning(f"⚠️ El número de imágenes generadas ({len(image_paths)}) no coincide con los segmentos de subtítulo ({len(subtitulos_json)}). El video se ensamblará con las imágenes disponibles.")
        # Si decides que esto es un fallo crítico, puedes poner sys.exit(1) aquí


    # --- 6. Ensamblar video final sincronizado ---
    logger.info("6. Ensamblando video final...")
    video_filename = f"videocuento_{uuid.uuid4().hex[:6]}.mp4"
    video_path = Path(settings.VIDEOS_DIR) / video_filename # Construir ruta completa
    # crear_video_sincronizado espera lista de rutas de imágenes, ruta audio, subtítulos JSON, ruta salida video
    final_video_path = crear_video_sincronizado(image_paths, generated_audio_path, subtitulos_json, str(video_path))
    if not final_video_path:
        logger.error("❌ Fallo crítico: No se pudo ensamblar o exportar el video final.")
        sys.exit(1) # Salir si el ensamblaje/exportación falla
    logger.info("✅ Video ensamblado correctamente.")


    # --- Resultado final ---
    logger.info("\n🎉 ¡Pipeline de generación completado con éxito!")
    logger.info(f"📼 Video final disponible en: {final_video_path}")