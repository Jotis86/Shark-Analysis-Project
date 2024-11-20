import streamlit as st
import pandas as pd
import os

# Cargar los datos
@st.cache_data
def load_data():
    # Usar una ruta relativa
    file_path = os.path.join(os.path.dirname(__file__), '..', 'notebooks', 'cleaned_data.csv')
    return pd.read_csv(file_path)

df_cleaned = load_data()

# Título de la aplicación
st.title('Análisis de Datos de Tiburones')

# Descripción
st.write("""
Esta aplicación muestra los gráficos y conclusiones del análisis de datos de tiburones.
""")

# Menú de navegación
st.sidebar.title('Menú de Navegación')
menu = st.sidebar.radio('Selecciona una sección:', ['Objetivos del Proyecto', 'Proceso de Desarrollo', 'Visualizaciones', 'Conclusiones Finales', 'Recomendaciones'])

if menu == 'Objetivos del Proyecto':
    st.header('Objetivos del Proyecto 🎯')
    st.write("""
    El objetivo principal de este proyecto es analizar y visualizar datos de ataques de tiburones para obtener información sobre patrones y tendencias. 📊
    """)

elif menu == 'Proceso de Desarrollo':
    st.header('Proceso de Desarrollo 🚀')
    st.write("""
    1. 📥 **Recolección de Datos**: Reunir datos en bruto.
    2. 🧹 **Limpieza de Datos**: Usar Jupyter Notebooks para limpiar y preprocesar los datos.
    3. 🔍 **Análisis de Datos**: Analizar los datos limpios para extraer información significativa.
    4. 📊 **Visualización de Datos**: Crear visualizaciones para representar los hallazgos.
    5. 📝 **Reporte**: Compilar los resultados en informes y presentaciones.
    """)

elif menu == 'Visualizaciones':
    st.header('Visualizaciones 📊')
    st.write("Selecciona un gráfico del menú de la izquierda para visualizarlo.")
    
    # Menú de selección de gráficos
    options = {
        'Distribución de Rangos de Edad': 'age.png',
        'Distribución por Sexo': 'sex.png',
        'Top 5 Actividades con Más Ataques': 'activities.png',
        'Top 10 Tipos de Tiburones Más Comunes': 'sharks.png',
        'Frecuencia de Océanos y Mares': 'ocean.png',
        'Distribución por Tiempo': 'time.png',
        'Distribución de Ataques por Mes': 'month.png',
        'Número de Ataques en los Últimos 10 Años': 'years.png',
        'Distribución de Ataques por Continente': 'continent.png'
    }

    selected_option = st.sidebar.radio('Selecciona un gráfico', list(options.keys()))

    if selected_option:
        image_path = os.path.join(os.path.dirname(__file__), 'images', options[selected_option])
        if os.path.exists(image_path):
            st.image(image_path, caption=selected_option)
        else:
            st.error(f"No se pudo encontrar la imagen: {image_path}")

elif menu == 'Conclusiones Finales':
    st.header('Conclusiones Finales 📊')
    st.write("""
    - **Edad**: el rango de edad más afectado por los ataques de tiburones es el de 21-30 años. Esto probablemente se deba a que este grupo de edad participa en más actividades acuáticas. 🏄‍♂️
    - **Género**: el 86.5% de los ataques de tiburones son a hombres, lo que los convierte en el grupo con mayor riesgo. 👨
    - **Actividades de Mayor Riesgo**: las actividades con mayor riesgo de ataques de tiburones son el surf 🏄‍♂️, seguido de la natación 🏊‍♂️ y la pesca 🎣.
    - **Frecuencia de Ataques por Océano**: los océanos con más ataques de tiburones son el Océano Pacífico 🌊, el Océano Atlántico 🌊 y el Océano Índico 🌊.
    - **Distribución Temporal de los Ataques**: la mayoría de los ataques de tiburones ocurren en la tarde 🌅, seguidos por la mañana 🌄 y finalmente por la noche 🌃.
    - **Países**: los países con más ataques de tiburones son Estados Unidos 🇺🇸, Australia 🇦🇺 y Sudáfrica 🇿🇦, probablemente debido a la mayor prevalencia de actividades como el surf y la natación en estas regiones.
    """)

elif menu == 'Recomendaciones':
    st.header('Recomendaciones 📋')
    st.write("""
    Basado en el análisis, se proponen las siguientes recomendaciones:

    1. **Aumentar la Conciencia y las Medidas de Seguridad**: 
       - 📢 Dirigir información y pautas de seguridad a grupos de alto riesgo, como surfistas y nadadores.
       - 🦈 Implementar y promover el uso de dispositivos de disuasión de tiburones en áreas de alto riesgo.

    2. **Precauciones Estacionales y Basadas en el Tiempo**: 
       - 📅 Aumentar la vigilancia y las medidas de seguridad durante los meses de mayor incidencia de ataques (julio, enero, agosto y septiembre) y las horas del día (por la tarde).
       - 🚫 Alentar a los bañistas a evitar nadar durante los momentos de alto riesgo.

    3. **Enfoque Geográfico**: 
       - 🌍 Enfocar las campañas de seguridad y los recursos en las regiones con el mayor número de ataques, como América del Norte, Oceanía y África.
       - 🤝 Colaborar con las autoridades locales en estas regiones para mejorar la vigilancia y las estrategias de respuesta ante tiburones.

    4. **Investigación Adicional**: 
       - 🔬 Realizar más estudios para comprender los factores subyacentes que contribuyen al alto número de ataques en regiones y actividades específicas.
       - 🌐 Explorar el impacto de los cambios ambientales en el comportamiento de los tiburones y los patrones de ataque.
    """)