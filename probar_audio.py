# probar_audio.py

from core.processors.audio_generator import AudioGenerator

# Texto de ejemplo
texto = "Hola, este es un cuento mágico creado por Cuentix para probar el sistema de voz."

# Elegir motor: "openai" o "elevenlabs"
motor = "elevenlabs"  # Cambia a "elevenlabs" si quieres probar con ese

# Generador
generador_audio = AudioGenerator(motor=motor)

# Generar archivo de audio
ruta_audio = generador_audio.generate_audio(texto, "prueba_audio.mp3")

print(f"\n✅ Audio generado: {ruta_audio}")

