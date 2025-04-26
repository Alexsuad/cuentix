# probar_whisper_directo.py

import whisper
import os

def transcribir_audio():
    # Ruta absoluta del archivo de audio generado
    ruta_audio = os.path.abspath("assets/audio/temp_prueba_subtitulos.mp3")
    
    if not os.path.exists(ruta_audio):
        print(f"❌ El archivo de audio no existe: {ruta_audio}")
        return

    print(f"🔍 Intentando transcribir: {ruta_audio}")
    
    try:
        # Cargar modelo Whisper
        modelo = whisper.load_model("base")
        print("✅ Modelo Whisper cargado correctamente.")
        
        # Transcribir el audio
        resultado = modelo.transcribe(ruta_audio)
        print("\n📝 Transcripción exitosa. Texto obtenido:")
        print(resultado["text"])
        
    except Exception as e:
        print(f"❌ Error durante la transcripción: {str(e)}")

if __name__ == "__main__":
    transcribir_audio()
