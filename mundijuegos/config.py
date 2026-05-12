"""Configuración global de la aplicación."""

# ============================================================
# CONFIGURACIÓN PERSONALIZABLE
# Cambia estos valores para adaptar la app a otro niño/a
# ============================================================

NOMBRE_NINA: str = "Zoa"
EDAD_RECOMENDADA: str = "4-8 años"

# ============================================================
# PALETA DE COLORES - Tema Pastel / Rosa Chicle
# ============================================================

COLORES = {
    "rosa_chicle": "#FF69B4",
    "rosa_claro": "#FFB6C1",
    "rosa_pastel": "#FFC0CB",
    "rosa_suave": "#F8C8DC",
    "lila_pastel": "#E6E6FA",
    "celeste_pastel": "#B0E0E6",
    "amarillo_pastel": "#FFFACD",
    "menta_pastel": "#98FF98",
    "melocoton": "#FFDAB9",
    "blanco_hueso": "#FFFAF0",
    "texto_principal": "#5D3A58",
    "texto_secundario": "#8B6F8B",
}

# ============================================================
# CONFIGURACIÓN DE TEMA TAILWIND
# ============================================================

THEME_COLORS = {
    "background": "#FFF0F5",      # Lavanda blush
    "surface": "#FFFFFF",          # Blanco puro para tarjetas
    "primary": "#FF69B4",          # Rosa chicle
    "secondary": "#FFB6C1",        # Rosa claro
    "accent": "#98FF98",           # Menta
    "muted": "#F8C8DC",            # Rosa suave
    "text": "#5D3A58",             # Morado oscuro suave
}

# ============================================================
# CONFIGURACIÓN DE ANIMACIONES
# ============================================================

ANIMACIONES = {
    "float_duration": "3s",
    "bounce_duration": "0.6s",
    "shake_duration": "0.5s",
    "fade_duration": "0.8s",
}
