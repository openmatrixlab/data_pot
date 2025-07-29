import streamlit as st
import pandas as pd
from pathlib import Path
import base64

# Configuración general de la página de la aplicación
st.set_page_config(page_title="Buscador de Archivos", layout="wide")


# --- FUNCIÓN PARA APLICAR FONDO PERSONALIZADO Y ESTILOS DE INTERFAZ ---
def set_background(jpg_file):
    """
    Aplica una imagen de fondo a la aplicación y configura los estilos de color
    para asegurar el contraste adecuado entre texto e interfaz.
    """
    with open(jpg_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    # Hoja de estilos CSS embebida
    css = f"""
    <style>
    /* Fondo principal de la aplicación */
    .stApp {{
        background-image: url(data:image/jpg;base64,{encoded});
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Texto general en color blanco para mantener contraste sobre el fondo */
    h1, h2, h3, h4, h5, h6, p, label, span, .stMarkdown, .stTextInput label {{
        color: white !important;
    }}

    /* Campo de entrada de texto con fondo semitransparente y texto blanco */
    .stTextInput > div > div > input {{
        background-color: rgba(0,0,0,0.6);
        color: white !important;
    }}

    /* Menú desplegable (extensiones) con estilo claro para mayor legibilidad */
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

    /* Visualización del DataFrame con fondo blanco y texto negro */
    .stDataFrame {{
        background-color: white !important;
        color: black !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# Verifica si la imagen de fondo existe y la aplica
imagen_fondo = "fondo.jpg"
if Path(imagen_fondo).exists():
    set_background(imagen_fondo)

# Título principal de la aplicación
st.title("🔍 Buscador de Archivos - Data POT")

# Ruta y verificación del archivo Excel con el inventario de archivos
excel_path = "Inventario_archivosAnywhere.xlsx"
if not Path(excel_path).exists():
    st.error(f"No se encontró el archivo {excel_path}")
    st.stop()

# Carga del archivo Excel
df = pd.read_excel(excel_path)
df["Extensión"] = df["Extensión"].str.lower()  # Normalización de extensiones

# Selector de campo de búsqueda
modo_busqueda = st.radio(
    "Buscar por:",
    options=["Nombre", "Carpeta", "Todos"],
    horizontal=True,
    index=2
)

# Campo de entrada para búsqueda
busqueda = st.text_input("Buscar por palabra clave:")

# Definir columnas según el modo de búsqueda
if modo_busqueda == "Nombre":
    columnas = ["Nombre"]
elif modo_busqueda == "Carpeta":
    columnas = ["Carpeta"]
else:
    columnas = ["Nombre", "Carpeta"]

# Aplicar filtro si hay búsqueda
if busqueda:
    palabras = busqueda.lower().split()

    def coincide(fila):
        return any(pal in str(fila[col]).lower() for pal in palabras for col in columnas)

    df_filtrado = df[df.apply(coincide, axis=1)]
else:
    df_filtrado = df

# Opciones de filtrado por tipo de extensión de archivo
extensiones = sorted(df_filtrado["Extensión"].dropna().unique())
ext_seleccionadas = st.multiselect("Filtrar por tipo de archivo:",
                                   ["(Mostrar todas)"] + extensiones,
                                   default="(Mostrar todas)")

# Aplica el filtro solo si el usuario selecciona una o varias extensiones específicas
if "(Mostrar todas)" not in ext_seleccionadas:
    df_filtrado = df_filtrado[df_filtrado["Extensión"].isin(ext_seleccionadas)]

# Presentación de resultados filtrados
st.write(f"**{len(df_filtrado)} archivos encontrados**")
st.dataframe(df_filtrado, use_container_width=True, height=200)
