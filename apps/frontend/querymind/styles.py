import reflex as rx

# 1. TOKENS DE COLOR (Urban Night Palette)
# Paleta diseñada para alta legibilidad en entornos técnicos.
COLORS = {
    "bg_dark": "#0F1115",  # Fondo profundo (Base)
    "bg_surface": "#1E2228",  # Superficie de contenedores (Cards/Sidebar)
    "border": "#2D333B",  # Bordes sutiles
    "accent": "#2ECC71",  # Verde MiBici (Éxito / Call to Action)
    "accent_dim": "rgba(46, 204, 113, 0.1)",  # Verde con transparencia para hovers
    "text_main": "#E6EDF3",  # Texto principal (High Contrast)
    "text_secondary": "#8B949E",  # Texto de apoyo / Metadatos
    "status": {
        "error": "#E74C3C",  # Fallo en Linter o Alucinación
        "running": "#3498DB",  # Procesamiento activo
        "success": "#2ECC71",  # Nodo completado
        "idle": "#454C56",  # Estado de espera
    },
}

# 2. TOKENS DE TIPOGRAFÍA
# Mapeo de fuentes para asegurar consistencia entre narrativa y código.
FONTS = {
    "sans": "Inter, system-ui, sans-serif",
    "mono": "JetBrains Mono, Fira Code, monospace",
}

# 3. ESTILOS BASE (Global Scaffolding)
# Estos estilos se inyectan en rx.App para normalizar el comportamiento.
BASE_STYLE = {
    "background_color": COLORS["bg_dark"],
    "color": COLORS["text_main"],
    "font_family": FONTS["sans"],
    # CORRECCIÓN AQUÍ: Usar minúsculas
    rx.heading: {
        "font_family": FONTS["sans"],
        "color": COLORS["text_main"],
    },
    rx.text: {
        "font_family": FONTS["sans"],
        "color": COLORS["text_secondary"],
    },
    rx.code: {
        "font_family": FONTS["mono"],
        "background_color": "transparent",
    },
}

# 4. UTILIDADES DE TAILWIND (Clases reutilizables)
# Definimos strings de clases para el plugin TailwindV4 de Reflex.
TAILWIND_CLASSES = {
    "card": "bg-[#1E2228] border border-[#2D333B] rounded-xl overflow-hidden",
    "transition": "transition-all duration-300 ease-in-out",
    "input_focus": "focus:ring-2 focus:ring-[#2ECC71] focus:border-transparent outline-none",
}

# 5. ATRIBUTOS DE COMPONENTES (Scaffolding Visual)
# Configuraciones de layout para los contenedores principales.
LAYOUT = {
    "sidebar_width": "320px",
    "max_width": "1200px",
    "padding": "2rem",
}
