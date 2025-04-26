#verificar_openai.py

import openai

# Usa tu clave directamente o asegúrate de que esté cargada desde settings.py o .env
openai.api_key = "sk-tu-clave-aquí"  # <-- reemplaza por tu clave real si lo haces directo

try:
    modelos = openai.models.list()
    print("✅ Conexión exitosa con la API de OpenAI.")
    print(f"Modelos disponibles: {[m.id for m in modelos.data]}")
except Exception as e:
    print("❌ Error al conectar con la API de OpenAI.")
    print("Detalle:", str(e))

import requests

headers = {
    "Authorization": f"Bearer sk-tu-clave-aquí"
}

res = requests.get("https://api.openai.com/dashboard/billing/credit_grants", headers=headers)
print(res.json())
