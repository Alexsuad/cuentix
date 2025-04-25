# verificar_apis.py

"""
Script de prueba para verificar que las claves de API de OpenAI y ElevenLabs están funcionando correctamente.
"""

import os
import requests
from config.settings import settings

# Función para verificar conexión con OpenAI TTS
def verificar_openai():
    try:
        print("\n🧪 Verificando OpenAI TTS...")
        headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
        data = {
            "model": "tts-1",
            "input": "Hola, esto es una prueba de voz de OpenAI.",
            "voice": "alloy"
        }
        response = requests.post("https://api.openai.com/v1/audio/speech", headers=headers, json=data)
        response.raise_for_status()
        print("✅ OpenAI TTS responde correctamente.")
    except Exception as e:
        print(f"❌ Error con OpenAI TTS: {e}")

# Función para verificar conexión con ElevenLabs
def verificar_elevenlabs():
    try:
        print("\n🧪 Verificando ElevenLabs...")
        headers = {
            "xi-api-key": settings.ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "text": "Esto es una prueba de voz desde ElevenLabs.",
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.7
            }
        }
        voice_id = "rrErIO88ehxTnspOjKvf"
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print("✅ ElevenLabs responde correctamente.")
    except Exception as e:
        print(f"❌ Error con ElevenLabs: {e}")

if __name__ == "__main__":
    verificar_openai()
    verificar_elevenlabs()
