# ──────────────────────────────────────────────────────────────────────────────
# File: core/validators/campos_requeridos.py
# Descripción: Define la lista oficial de campos que deben enviarse desde el
# frontend para generar un video-cuento válido en Cuentix. Esta constante se
# importa en todos los módulos que requieren validar la estructura de entrada.
# ──────────────────────────────────────────────────────────────────────────────

# Lista centralizada de campos requeridos para validar los datos de usuario
CAMPOS_REQUERIDOS = [
    "nombre",
    "edad",
    "personaje_principal",
    "lugar",
    "villano",
    "objeto_magico",
    "tipo_final"
]
