from colorsys import rgb_to_hls, hls_to_rgb

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    return "#{:02x}{:02x}{:02x}".format(
        int(rgb_color[0] * 255),
        int(rgb_color[1] * 255),
        int(rgb_color[2] * 255)
    )

def generate_theme(base_color):
    base_rgb = hex_to_rgb(base_color)
    h, l, s = rgb_to_hls(*base_rgb)

    # Generar colores complementarios y contrastantes
    primary = base_color
    secondary = rgb_to_hex(hls_to_rgb((h + 0.5) % 1.0, l, s))  # Complementario
    background = rgb_to_hex(hls_to_rgb(h, min(l + 0.4, 1.0), s))  # Más claro
    text = rgb_to_hex(hls_to_rgb(h, max(l - 0.5, 0.0), s))  # Más oscuro
    error = "#e63946"  # Rojo pastel fijo para errores
    warning = "#ffb703"  # Amarillo pastel fijo para advertencias
    success = "#2a9d8f"  # Verde pastel fijo para éxito

    return {
        "primary": primary,
        "secondary": secondary,
        "background": background,
        "text": text,
        "error": error,
        "warning": warning,
        "success": success,
        "border_radius": "10px"
    }
