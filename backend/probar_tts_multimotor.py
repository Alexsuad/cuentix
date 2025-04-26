# probar_tts_multimotor.py

# Este archivo compara múltiples motores TTS (gTTS, OpenAI, ElevenLabs) para pruebas de calidad y compatibilidad.

import logging
from core.processors.audio_generator import AudioGenerator

# Configurar logging en modo DEBUG para mayor visibilidad
logging.basicConfig(level=logging.DEBUG)

texto = "Hola, este es un cuento corto para probar la generación de audio."
motores = ["gtts", "openai", "elevenlabs"]

for motor in motores:
    print(f"\n🔧 Probando motor: {motor}")
    try:
        generador = AudioGenerator(motor=motor)  # ✅ Usamos el motor dinámicamente
        archivo = f"assets/audio/prueba_{motor}.mp3"
        ruta = generador.generate_audio(texto, archivo)

        if ruta:
            print(f"✅ Audio generado con {motor}: {ruta}")
        else:
            print(f"❌ Falló la generación de audio con {motor}.")
    except Exception as e:
        print(f"❌ Error al probar el motor {motor}: {e}")
