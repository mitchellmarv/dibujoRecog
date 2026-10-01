import math
import random
from importlib.metadata import version as pkg_version

import numpy as np
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="Detector de Colores Galáctico", page_icon="🌌", layout="centered")

# ---------- Tema espacial / galaxia en morado ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Inter:wght@400;500&display=swap');

    :root {
        --space-900: #0b0221;
        --space-800: #1a0b3d;
        --space-700: #2d1465;
        --purple-500: #7b2ff7;
        --purple-300: #b388ff;
        --purple-100: #e0aaff;
        --nebula-pink: #f107a3;
        --text: #efe6ff;
    }

    .stApp {
        background-color: var(--space-900);
        background-image:
            radial-gradient(1.5px 1.5px at 20px 30px, #fff, transparent),
            radial-gradient(1px 1px at 90px 120px, #e0aaff, transparent),
            radial-gradient(1.5px 1.5px at 160px 70px, #fff, transparent),
            radial-gradient(1px 1px at 230px 180px, #b388ff, transparent),
            radial-gradient(ellipse at 15% 20%, rgba(123, 47, 247, 0.35), transparent 55%),
            radial-gradient(ellipse at 85% 75%, rgba(241, 7, 163, 0.20), transparent 50%),
            radial-gradient(ellipse at 50% 100%, rgba(45, 20, 101, 0.8), transparent 60%);
        background-size: 250px 250px, 250px 250px, 250px 250px, 250px 250px,
                         100% 100%, 100% 100%, 100% 100%;
        background-attachment: fixed;
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stHeader"] { background: transparent; }

    h1 {
        font-family: 'Orbitron', sans-serif !important;
        text-align: center !important;
        letter-spacing: 3px;
        background: linear-gradient(90deg, var(--purple-100), var(--purple-500), var(--nebula-pink));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h2, h3, h4 {
        font-family: 'Orbitron', sans-serif !important;
        color: var(--purple-100) !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--space-800) 0%, var(--space-900) 100%);
        border-right: 1px solid rgba(179, 136, 255, 0.35);
        box-shadow: 4px 0 25px rgba(123, 47, 247, 0.25);
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: var(--text) !important;
    }

    div[data-baseweb="select"] > div {
        background-color: var(--space-700) !important;
        border: 1px solid var(--purple-300) !important;
        color: var(--text) !important;
    }

    div[data-baseweb="slider"] div[role="slider"] {
        background-color: var(--purple-100) !important;
        box-shadow: 0 0 12px var(--purple-500);
    }

    /* ---- Centrar el tablero respecto al título ---- */
    .stElementContainer:has(iframe),
    [class*="st-key-canvas_"],
    [data-testid="stCustomComponentV1"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    iframe {
        display: block;
        margin: 0 auto !important;
        border: 2px solid var(--purple-500) !important;
        border-radius: 12px;
        box-shadow: 0 0 25px rgba(123, 47, 247, 0.6),
                    0 0 60px rgba(241, 7, 163, 0.2);
    }

    .stButton > button {
        background: linear-gradient(90deg, var(--purple-500), var(--nebula-pink));
        color: white;
        border: none;
        border-radius: 8px;
        width: 100%;
    }
    .stButton > button:hover {
        box-shadow: 0 0 15px var(--purple-300);
        color: white;
    }

    /* ---- Tarjetas de color ---- */
    .color-card {
        display: flex;
        align-items: center;
        gap: 18px;
        background: rgba(45, 20, 101, 0.55);
        border: 1px solid rgba(179, 136, 255, 0.4);
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 0 18px rgba(123, 47, 247, 0.25);
    }
    .color-swatch {
        flex: 0 0 72px;
        height: 72px;
        border-radius: 50%;
        border: 3px solid rgba(255, 255, 255, 0.85);
        box-shadow: 0 0 18px rgba(179, 136, 255, 0.6);
    }
    .color-info { flex: 1; min-width: 0; }
    .color-name {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.15rem;
        color: var(--purple-100);
        margin-bottom: 4px;
    }
    .color-codes { font-size: 0.95rem; color: var(--text); line-height: 1.6; }
    .color-codes code {
        background: rgba(11, 2, 33, 0.7);
        color: var(--purple-100);
        padding: 2px 8px;
        border-radius: 6px;
    }
    .share-bar {
        height: 6px;
        border-radius: 3px;
        background: rgba(255, 255, 255, 0.12);
        margin-top: 8px;
        overflow: hidden;
    }
    .share-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--purple-500), var(--nebula-pink));
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌌 Detector de Colores Galáctico")

CANVAS_W = 600
CANVAS_H = 400

# Desde la versión 0.10 el lienzo usa Fabric.js 7: los tipos van capitalizados ("Rect", "Circle"...)
try:
    NEW_CANVAS = tuple(int(x) for x in pkg_version("streamlit-drawable-canvas").split(".")[:2]) >= (0, 10)
except Exception:
    NEW_CANVAS = False


def fabric_type(name):
    return name.capitalize() if NEW_CANVAS else name

# ---------- Estado ----------
if "objects" not in st.session_state:
    st.session_state.objects = []
if "initial_drawing" not in st.session_state:
    st.session_state.initial_drawing = {"version": "4.4.0", "objects": []}
if "canvas_version" not in st.session_state:
    st.session_state.canvas_version = 0


# ---------- Utilidades para figuras geométricas ----------
def hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def polygon_points(n, radius, star=False):
    """Puntos de un polígono regular (o estrella) con la punta hacia arriba."""
    pts = []
    total = n * 2 if star else n
    for i in range(total):
        r = radius if (not star or i % 2 == 0) else radius * 0.45
        ang = -math.pi / 2 + 2 * math.pi * i / total
        pts.append((r * math.cos(ang), r * math.sin(ang)))
    min_x = min(p[0] for p in pts)
    min_y = min(p[1] for p in pts)
    pts = [{"x": x - min_x, "y": y - min_y} for x, y in pts]
    w = max(p["x"] for p in pts)
    h = max(p["y"] for p in pts)
    return pts, w, h


def build_shape(name, size, fill, stroke, stroke_w):
    base = {
        "version": "4.4.0",
        "originX": "left",
        "originY": "top",
        "fill": fill,
        "stroke": stroke,
        "strokeWidth": stroke_w,
    }
    cx = CANVAS_W / 2 + random.randint(-40, 40)
    cy = CANVAS_H / 2 + random.randint(-30, 30)

    if name == "Círculo":
        return {**base, "type": fabric_type("circle"), "radius": size / 2,
                "left": cx - size / 2, "top": cy - size / 2}
    if name == "Elipse":
        return {**base, "type": fabric_type("ellipse"), "rx": size / 2, "ry": size / 3.5,
                "left": cx - size / 2, "top": cy - size / 3.5}
    if name == "Cuadrado":
        return {**base, "type": fabric_type("rect"), "width": size, "height": size,
                "left": cx - size / 2, "top": cy - size / 2}
    if name == "Rectángulo":
        return {**base, "type": fabric_type("rect"), "width": size * 1.6, "height": size,
                "left": cx - size * 0.8, "top": cy - size / 2}
    if name == "Triángulo":
        return {**base, "type": fabric_type("triangle"), "width": size, "height": size,
                "left": cx - size / 2, "top": cy - size / 2}

    sides = {"Rombo": 4, "Pentágono": 5, "Hexágono": 6, "Estrella": 5}[name]
    pts, w, h = polygon_points(sides, size / 2, star=(name == "Estrella"))
    return {**base, "type": fabric_type("polygon"), "points": pts,
            "left": cx - w / 2, "top": cy - h / 2}


# ---------- Detección de colores ----------
# Nombres de colores en español (RGB de referencia)
COLOR_NAMES = {
    "Negro": (0, 0, 0), "Gris oscuro": (64, 64, 64), "Gris": (128, 128, 128),
    "Gris claro": (192, 192, 192), "Plateado": (211, 211, 211), "Blanco": (255, 255, 255),
    "Rojo": (255, 0, 0), "Rojo oscuro": (139, 0, 0), "Carmesí": (220, 20, 60),
    "Granate": (128, 0, 32), "Rosa": (255, 192, 203), "Rosa fuerte": (255, 105, 180),
    "Fucsia": (255, 0, 255), "Salmón": (250, 128, 114), "Coral": (255, 127, 80),
    "Tomate": (255, 99, 71), "Naranja": (255, 165, 0), "Naranja oscuro": (255, 140, 0),
    "Naranja rojizo": (255, 69, 0), "Durazno": (255, 218, 185), "Amarillo": (255, 255, 0),
    "Dorado": (255, 215, 0), "Mostaza": (225, 173, 1), "Caqui": (240, 230, 140),
    "Beige": (245, 245, 220), "Crema": (255, 253, 208), "Marrón": (139, 69, 19),
    "Marrón claro": (205, 133, 63), "Chocolate": (210, 105, 30), "Café": (111, 78, 55),
    "Siena": (160, 82, 45), "Arena": (210, 180, 140), "Verde": (0, 128, 0),
    "Verde lima": (0, 255, 0), "Lima": (50, 205, 50), "Verde claro": (144, 238, 144),
    "Verde oliva": (128, 128, 0), "Verde bosque": (34, 139, 34),
    "Verde esmeralda": (80, 200, 120), "Verde menta": (189, 252, 201),
    "Turquesa": (64, 224, 208), "Aguamarina": (127, 255, 212), "Cian": (0, 255, 255),
    "Verde azulado": (0, 128, 128), "Azul": (0, 0, 255), "Azul marino": (0, 0, 128),
    "Azul real": (65, 105, 225), "Azul cielo": (135, 206, 235), "Azul claro": (173, 216, 230),
    "Azul acero": (70, 130, 180), "Azul cobalto": (0, 71, 171), "Índigo": (75, 0, 130),
    "Violeta": (238, 130, 238), "Morado": (128, 0, 128), "Púrpura": (160, 32, 240),
    "Lavanda": (230, 230, 250), "Lila": (200, 162, 200), "Orquídea": (218, 112, 214),
    "Morado medio": (147, 112, 219), "Azul violeta": (138, 43, 226), "Ciruela": (142, 69, 133),
}


def rgb_to_lab(rgb):
    """Convierte RGB (0-255) a CIE Lab para comparar colores como los percibe el ojo."""
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    x = (c[0] * 0.4124 + c[1] * 0.3576 + c[2] * 0.1805) / 0.95047
    y = (c[0] * 0.2126 + c[1] * 0.7152 + c[2] * 0.0722)
    z = (c[0] * 0.0193 + c[1] * 0.1192 + c[2] * 0.9505) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(x), f(y), f(z)
    return np.array([116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)])


_NAMES = list(COLOR_NAMES.keys())
_NAMES_LAB = np.array([rgb_to_lab(v) for v in COLOR_NAMES.values()])


def color_name(rgb):
    lab = rgb_to_lab(rgb)
    idx = int(np.argmin(np.linalg.norm(_NAMES_LAB - lab, axis=1)))
    return _NAMES[idx]


def analyze_colors(image_data, bg_rgb, max_colors=5, min_share=2.0):
    """Devuelve los colores dominantes del dibujo (sin contar el fondo)."""
    arr = np.asarray(image_data)[:, :, :3].reshape(-1, 3).astype(np.float32)

    # Quitar los píxeles del fondo
    dist = np.linalg.norm(arr - np.array(bg_rgb, dtype=np.float32), axis=1)
    px = arr[dist > 30]
    if len(px) == 0:
        return []

    # Agrupar colores parecidos: primero en cajas de 16 niveles, luego por distancia Lab
    q = (px // 16).astype(np.int32)
    keys = q[:, 0] * 256 + q[:, 1] * 16 + q[:, 2]
    _, inv, counts = np.unique(keys, return_inverse=True, return_counts=True)
    means = np.stack(
        [np.bincount(inv, weights=px[:, c]) / counts for c in range(3)], axis=1
    )

    clusters = []
    for i in np.argsort(-counts):
        lab = rgb_to_lab(means[i])
        for cl in clusters:
            if np.linalg.norm(lab - cl["lab"]) < 14:
                cl["count"] += int(counts[i])
                break
        else:
            clusters.append({"rgb": means[i], "lab": lab, "count": int(counts[i])})

    total = len(px)
    results = []
    for cl in sorted(clusters, key=lambda c: -c["count"]):
        share = cl["count"] / total * 100
        if share < min_share:
            continue
        rgb = tuple(int(round(v)) for v in cl["rgb"])
        results.append({
            "rgb": rgb,
            "hex": "#{:02X}{:02X}{:02X}".format(*rgb),
            "name": color_name(rgb),
            "share": share,
        })
    return results[:max_colors]


# ---------- Barra lateral ----------
with st.sidebar:
    st.subheader("🪐 Propiedades del Tablero")

    drawing_mode = st.selectbox(
        "Herramienta de Dibujo:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )

    stroke_width = st.slider("Selecciona el ancho de línea", 1, 30, 15)
    stroke_color = st.color_picker("Color de trazo", "#E0AAFF")
    fill_color = st.color_picker("Color de relleno", "#7B2FF7")
    bg_color = st.color_picker("Color de fondo", "#0B0221")

    # ----- Figuras geométricas -----
    st.divider()
    st.subheader("✨ Figuras Geométricas")
    shape_name = st.selectbox(
        "Figura:",
        ("Círculo", "Cuadrado", "Rectángulo", "Triángulo",
         "Elipse", "Rombo", "Pentágono", "Hexágono", "Estrella"),
    )
    shape_size = st.slider("Tamaño de la figura", 40, 250, 120, 10)

    if st.button("➕ Añadir figura"):
        new_shape = build_shape(
            shape_name, shape_size, fill_color, stroke_color, min(stroke_width, 8),
        )
        st.session_state.initial_drawing = {
            "version": "4.4.0",
            "objects": list(st.session_state.objects) + [new_shape],
        }
        st.session_state.canvas_version += 1
        st.rerun()

    st.caption(
        "💡 Después de añadir una figura, elige la herramienta "
        "**transform** para moverla, rotarla o cambiar su tamaño."
    )

    if st.button("🧹 Limpiar tablero"):
        st.session_state.objects = []
        st.session_state.initial_drawing = {"version": "4.4.0", "objects": []}
        st.session_state.canvas_version += 1
        st.rerun()

    # ----- Ajustes del análisis -----
    st.divider()
    st.subheader("🔭 Análisis de colores")
    max_colors = st.slider("Máximo de colores a mostrar", 1, 8, 5)
    min_share = st.slider("Ignorar colores menores a (%)", 0.5, 10.0, 2.0, 0.5)

st.subheader("Dibuja en el tablero y presiona el botón para detectar los colores")

# ---------- Lienzo ----------
canvas_kwargs = dict(
    fill_color=fill_color,  # relleno opaco para que el color detectado sea exacto
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    initial_drawing=st.session_state.initial_drawing,
    height=CANVAS_H,
    width=CANVAS_W,
    drawing_mode=drawing_mode,
    key=f"canvas_{CANVAS_W}_{CANVAS_H}_{st.session_state.canvas_version}",
)
try:
    # Versiones nuevas (>= 0.10): hay que pedir explícitamente los píxeles del dibujo
    canvas_result = st_canvas(**canvas_kwargs, return_image_data=True)
except TypeError:
    # Versiones antiguas no conocen ese parámetro
    canvas_result = st_canvas(**canvas_kwargs)

if canvas_result.json_data is not None:
    st.session_state.objects = canvas_result.json_data.get("objects", [])

analyze_button = st.button("🎨 Detectar colores", type="secondary")

if analyze_button:
    try:
        image_data = canvas_result.image_data
    except RuntimeError as e:
        image_data = None
        st.error(
            "No pude leer la imagen del tablero. Instala la dependencia opcional con "
            '`pip install "streamlit-drawable-canvas[image]"`. '
            f"Detalle: {e}"
        )

    if image_data is None:
        st.warning("Dibuja algo en el tablero primero.")
    else:
        with st.spinner("Analizando colores ..."):
            colors = analyze_colors(
                image_data, hex_to_rgb(bg_color), max_colors, min_share
            )

        if not colors:
            st.info("No encontré colores en el tablero. ¡Dibuja algo primero! ✏️")
        else:
            st.subheader(f"Colores encontrados: {len(colors)}")
            for c in colors:
                r, g, b = c["rgb"]
                st.markdown(
                    f"""
                    <div class="color-card">
                        <div class="color-swatch" style="background:{c['hex']};"></div>
                        <div class="color-info">
                            <div class="color-name">{c['name']}</div>
                            <div class="color-codes">
                                HEX: <code>{c['hex']}</code> &nbsp;
                                RGB: <code>rgb({r}, {g}, {b})</code>
                            </div>
                            <div class="color-codes">Presencia en el dibujo: {c['share']:.1f}%</div>
                            <div class="share-bar">
                                <div class="share-fill" style="width:{min(c['share'], 100):.1f}%;"></div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
