import streamlit as st
import pandas as pd
from pathlib import Path
import base64

# Configuración de la página
st.set_page_config(page_title="Buscador de Archivos", layout="wide")

# --- FUNCIÓN PARA FONDO PERSONALIZADO ---
def set_background(jpg_file):
    """Aplica una imagen de fondo y ajusta colores de texto para contraste."""
    with open(jpg_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    css = f"""
    <style>
    /* Fondo general de la app */
    .stApp {{
        background-image: url(data:image/jpg;base64,{encoded});
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Colores blancos para todos los textos visibles */
    h1, h2, h3, h4, h5, h6, p, label, span, .stMarkdown, .stTextInput label {{
        color: white !important;
    }}

    /* Input del buscador */
    .stTextInput > div > div > input {{
        background-color: rgba(0,0,0,0.6);
        color: white !important;
    }}

    /* Filtro desplegable (extensiones) – letras negras para contraste */
    .stMultiSelect div[data-baseweb="select"] > div {{
        background-color: white !important;
        color: black !important;
    }}
    div[data-baseweb="menu"] {{
        background-color: white !important;
        color: black !important;
    }}
    div[data-baseweb="menu"] * {{
        color: black !important;
    }}

    /* DataFrame con fondo blanco y texto negro */
    .stDataFrame {{
        background-color: white !important;
        color: black !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Aplicar fondo si existe
imagen_fondo = "fondo.jpg"
if Path(imagen_fondo).exists():
    set_background(imagen_fondo)

# Título principal
st.title("🔍 Buscador de Archivos - Data POT")

# Cargar archivo Excel
excel_path = "Inventario_archivosAnywhere.xlsx"
if not Path(excel_path).exists():
    st.error(f"No se encontró el archivo {excel_path}")
    st.stop()

df = pd.read_excel(excel_path)
df["Extensión"] = df["Extensión"].str.lower()

# Campo de búsqueda
busqueda = st.text_input("Buscar por palabras clave (en nombre, carpeta o ruta):")

if busqueda:
    palabras = busqueda.lower().split()
    columnas = ["Nombre"]

    def coincide(fila):
        return any(pal in str(fila[col]).lower() for pal in palabras for col in columnas)

    df_filtrado = df[df.apply(coincide, axis=1)]
else:
    df_filtrado = df

# Filtro por extensión (aplicado después de la búsqueda)
extensiones = sorted(df_filtrado["Extensión"].dropna().unique())
ext_seleccionadas = st.multiselect("Filtrar por tipo de archivo:",
                                   ["(Mostrar todas)"] + extensiones,
                                   default="(Mostrar todas)")

if "(Mostrar todas)" not in ext_seleccionadas:
    df_filtrado = df_filtrado[df_filtrado["Extensión"].isin(ext_seleccionadas)]

# Mostrar resultados
st.write(f"**{len(df_filtrado)} archivos encontrados**")
st.dataframe(df_filtrado, use_container_width=True, height=200)


