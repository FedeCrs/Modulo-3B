# Importamos bibliotecas necesarias para la aplicación
import streamlit as st
import requests  # Para realizar solicitudes HTTP
import os
import base64

# Configuración inicial
st.set_page_config(page_title="Generación de Informes Médicos", layout="wide")

# Verificar si la imagen de fondo existe
image_path = os.path.abspath("imaMedic.webp")
if not os.path.exists(image_path):
    st.error("El archivo 'imaMedic.webp' no se encontró. Asegúrate de colocarlo en el mismo directorio que este script.")
else:
    # Convertir la imagen en base64
    def get_base64_image(file_path):
        try:
            with open(file_path, "rb") as file:
                return base64.b64encode(file.read()).decode()
        except Exception as e:
            st.error(f"Error al convertir la imagen a base64: {e}")
            return None
    
    # Genera la imagen en base64
    image_base64 = get_base64_image(image_path)

    # Verifica si la conversión fue exitosa
    if image_base64:
        st.success("Imagen cargada y convertida exitosamente.")
    else:
        st.error("No se pudo convertir la imagen a base64.")

# Estilo CSS personalizado, inyectar CSS para establecer la imagen de fondo
    st.markdown(
    f"""
    <style>
    @import url('http://fonts.googleapis.com/css2?family=Raleway:wght@100&display=swap');

     /* Fondo general */
    .stApp {{
        background: linear-gradient(rgba(60, 62, 54, 0.3), rgba(20, 62, 54, 0.3)),
                        url("data:image/webp;base64,{image_base64}") no-repeat center center fixed;
            background-size: cover; /* Cambia "cover" a "contain", "auto", o un tamaño específico como "100% 100%" */
            background-position: center; /* Ajusta la posición: center, top, bottom, left, right */
    }}

    /* Contenedor del contenido principal */
    .main-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;              /* Hace que el contenedor ocupe toda la altura de la pantalla */
        text-align: justify;       /* Justifica el texto */
        text-align-last: center;   /* Centra la última línea */
        
    }}

    h1 {{
        text-align: center;                     /* Centra el texto horizontalmente */
        color: white !important;                   
        font-family: 'Raleway', sans-serif;     /* Aplica una fuente moderna */
        font-weight: 900;                      /* Hace que el texto más grueso */
        font-size: 36px;                        /* Ajusta el tamaño de la fuente */
        margin: 0 auto;                         /* Centra el texto dentro del contenedor */
        line-height: 1.5;                       /* Espaciado entre líneas */
    }}

    

    /* Texto general */
    h1, h2, h3, h4, h5, h6, p, label {{
        color: white !important;
        font-family: 'Raleway', sans-serif;
        font-weight: 700;
        align-items: center;
        margin: 0;
        padding: 0;
        
    }}

    /* Estilo de la barra lateral */
    .stSidebar {{
        background-color: rgba(0, 180, 255, 0.8) !important;     # "!important" quiere decir que éste estilo va a prevalecer sobre todos los demás
        border-radius: 10px !important;
    }}

    div.stButton {{
        display: flex;
        justify-content: center; /* Centra horizontalmente */
        align-items: center;     /* Centra verticalmente */
        height: 100%;            /* Asegura que el contenedor ocupe todo el alto disponible */
    }}

     /* Botones */
    div.stButton > button {{
        width: 300px !important;                /* Ancho fijo del botón */
        background-color: black !important;     /* Fondo negro */
        color: white !important;                /* Texto blanco */
        font-family: 'Raleway', sans-serif;      /* Fuente moderna */
        font-weight: 900;                       /* Texto al máximo de grueso */
        font-size: 14px;                        /* Tamaño de fuente de 14px */
        border: 2px solid #5A3E36 !important;    /* Borde marrón oscuro */
        border-radius: 5px;                     /* Esquinas redondeadas */
        padding: 10px 20px;                      /* Relleno interno */
        cursor: pointer;                        /* Cursos tipo mano */
    }}

    .centered-text {{
        text-align: center;                  /* Centra horizontalmente el texto */
        margin: 0 auto;                     /* Centra el contenedor */
        font-family: 'Raleway', sans-serif; /* Fuente moderna */
        font-size: 18px;                    /* Tamaño de fuente ajustable */
        font-weight: bold;                   /* Grosor del texto */
        line-height: 1.5;                   /* Espaciado entre las líneas */
        display: inline-block;              /* Ajusta el ancho del bloque al texto */
        color: white;                       /* Color blanco del texto */
    }}


    div.stButton > button:hover {{
        background-color: #B666D2 !important;       # Aquí se le pone un background color al botón para que cambien de color cuando ponemos el cursor encima del botón
    }}

    /* Inputs de texto */
    textarea, input, select {{
        background-color: rgba(255, 255, 255, 1) !important;
        border: 2px solid #5A3E36 !important;
        border-radius: 5px !important;
        color: black !important;
    }}

    /* Margenes y alineación */
    .stSidebar{{
        padding: 20px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Contenedor principal centrado
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Título principal de la aplicación 
st.title('***Generación de Informes Médicos***')
st.markdown('<div class="centered-text">Esta aplicación permite generar informes médicos estructurados utilizando un modelo IA</div>',
    unsafe_allow_html=True,
)

# -------------------------
# Sección de entrada de datos del paciente
# -------------------------
st.sidebar.header('***Información del paciente***')
patient_name =st.sidebar.text_input("Nombre del paciente:", "")
age = st.sidebar.number_input("Edad:", min_value=0, max_value=120, step=1)
gender = st.sidebar.radio("Género:", ["Masculino", "Femenino", "Otro"])

# -------------------------
# Sección de entrada de datos clínicos
# -------------------------
st.sidebar.header('***Datos Clínicos***')
symptoms = st.sidebar.text_area("Síntomas principales:")
test_results = st.sidebar.text_area("Resultados de pruebas (ej: análisis de sangre):")
diagnosis = st.sidebar.text_area("Diagnóstico preliminar:")
recommendations = st.sidebar.text_area("Recomendaciones iniciales:")

# -------------------------
# Envío de datos al servidor Flask
# -------------------------
if st.button('***Generar Informe***'):
    if patient_name and symptoms and recommendations:
        data = {
            'patient_name': patient_name,
            'age': age,
            'gender': gender,
            'symptoms': symptoms,
            'test_results': test_results,
            'diagnosis': diagnosis,
            'recommendations': recommendations
        }

        response = requests.post('http://127.0.0.1:5000/generate_report', json=data)
        if response.status_code == 200:
            report = response.json()
            st.success("Informe generado exitosamente:")
            st.markdown(report['detailed_report'])
        else:
            st.error("Error al generar el informe. Intente nuevamente")
    else:
        st.warning("Por favor complete el nombre del paciente y los síntomas antes de continuar")

# Cierre del contenedor principal
st.markdown('</div>', unsafe_allow_html=True)