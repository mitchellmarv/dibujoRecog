import math
import random

import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="Tablero Galáctico", page_icon="🌌", layout="centered")

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
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌌 Tablero Galáctico")

CANVAS_W = 600
CANVAS_H = 400

# ---------- Estado ----------
if "objects" not in st.session_state:
    st.session_state.objects = []          # objetos actuales del lienzo
if "initial_drawing" not in st.session_state:
    st.session_state.initial_drawing = {"version": "4.4.0", "objects": []}
if "canvas_version" not in st.session_state:
    st.session_state.canvas_version = 0


# ---------- Utilidades para figuras geométricas ----------
def hex_to_rgba(hex_color, alpha=0.45):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


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
    # Centro del lienzo con un pequeño desplazamiento para que no se apilen
    cx = CANVAS_W / 2 + random.randint(-40, 40)
    cy = CANVAS_H / 2 + random.randint(-30, 30)

    if name == "Círculo":
        return {**base, "type": "circle", "radius": size / 2,
                "left": cx - size / 2, "top": cy - size / 2}
    if name == "Elipse":
        return {**base, "type": "ellipse", "rx": size / 2, "ry": size / 3.5,
                "left": cx - size / 2, "top": cy - size / 3.5}
    if name == "Cuadrado":
        return {**base, "type": "rect", "width": size, "height": size,
                "left": cx - size / 2, "top": cy - size / 2}
    if name == "Rectángulo":
        return {**base, "type": "rect", "width": size * 1.6, "height": size,
                "left": cx - size * 0.8, "top": cy - size / 2}
    if name == "Triángulo":
        return {**base, "type": "triangle", "width": size, "height": size,
                "left": cx - size / 2, "top": cy - size / 2}

    # Polígonos
    sides = {"Rombo": 4, "Pentágono": 5, "Hexágono": 6, "Estrella": 5}[name]
    pts, w, h = polygon_points(sides, size / 2, star=(name == "Estrella"))
    return {**base, "type": "polygon", "points": pts,
            "left": cx - w / 2, "top": cy - h / 2}


# ---------- Barra lateral ----------
with st.sidebar:
    st.subheader("🪐 Propiedades del Tablero")

    st.subheader("Dimensiones del Tablero")
    st.write("Ancho del tablero:")
    st.write(CANVAS_W)
    st.write("Alto del tablero:")
    st.write(CANVAS_H)

    drawing_mode = st.selectbox(
        "Herramienta de Dibujo:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )

    stroke_width = st.slider("Selecciona el ancho de línea", 1, 30, 15)
    stroke_color = st.color_picker("Color de trazo", "#E0AAFF")
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
    shape_fill = st.color_picker("Color de relleno", "#7B2FF7")

    if st.button("➕ Añadir figura"):
        new_shape = build_shape(
            shape_name, shape_size,
            hex_to_rgba(shape_fill), stroke_color, min(stroke_width, 8),
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

# ---------- Lienzo ----------
canvas_result = st_canvas(
    fill_color="rgba(179, 136, 255, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    initial_drawing=st.session_state.initial_drawing,
    height=CANVAS_H,
    width=CANVAS_W,
    drawing_mode=drawing_mode,
    key=f"canvas_{CANVAS_W}_{CANVAS_H}_{st.session_state.canvas_version}",
)

# Guardar los objetos actuales para conservarlos al añadir nuevas figuras
if canvas_result.json_data is not None:
    st.session_state.objects = canvas_result.json_data.get("objects", [])
