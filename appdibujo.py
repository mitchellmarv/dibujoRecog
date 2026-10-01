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

    /* Fondo de galaxia con estrellas y nebulosas */
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

    /* Encabezado transparente */
    [data-testid="stHeader"] { background: transparent; }

    /* Título */
    h1 {
        font-family: 'Orbitron', sans-serif !important;
        text-align: center;
        letter-spacing: 3px;
        background: linear-gradient(90deg, var(--purple-100), var(--purple-500), var(--nebula-pink));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(179, 136, 255, 0.4);
    }

    h2, h3, h4 {
        font-family: 'Orbitron', sans-serif !important;
        color: var(--purple-100) !important;
    }

    /* Barra lateral */
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

    /* Selectbox */
    div[data-baseweb="select"] > div {
        background-color: var(--space-700) !important;
        border: 1px solid var(--purple-300) !important;
        color: var(--text) !important;
    }

    /* Slider */
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: var(--purple-100) !important;
        box-shadow: 0 0 12px var(--purple-500);
    }

    /* Canvas con resplandor */
    iframe {
        border: 2px solid var(--purple-500) !important;
        border-radius: 12px;
        box-shadow: 0 0 25px rgba(123, 47, 247, 0.6),
                    0 0 60px rgba(241, 7, 163, 0.2);
    }

    /* Botones (incluye los del canvas si aplica) */
    .stButton > button {
        background: linear-gradient(90deg, var(--purple-500), var(--nebula-pink));
        color: white;
        border: none;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌌 Tablero Galáctico")

with st.sidebar:
    st.subheader("🪐 Propiedades del Tablero")

    # Dimensiones del lienzo
    st.subheader("Dimensiones del Tablero")
    st.write("Ancho del tablero:")
    canvas_width = 600  # st.slider("Ancho del tablero", 300, 700, 500, 50)

    canvas_height = 400  # st.slider("Alto del tablero", 200, 600, 300, 50)
    st.write(canvas_width)
    st.write("Alto del tablero:")
    st.write(canvas_height)

    # Selector de herramienta
    drawing_mode = st.selectbox(
        "Herramienta de Dibujo:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )

    # Ancho de línea
    stroke_width = st.slider("Selecciona el ancho de línea", 1, 30, 15)

    # Color de trazo (lavanda estelar por defecto)
    stroke_color = st.color_picker("Color de trazo", "#E0AAFF")

    # Color de fondo (espacio profundo por defecto)
    bg_color = st.color_picker("Color de fondo", "#0B0221")

# Lienzo de dibujo
canvas_result = st_canvas(
    fill_color="rgba(179, 136, 255, 0.3)",  # relleno morado translúcido
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    key=f"canvas_{canvas_width}_{canvas_height}",
)
