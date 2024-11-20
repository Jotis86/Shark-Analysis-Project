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
    
    ### Sub-objetivos:
    1. **Identificación de Patrones Temporales**: Analizar cómo varían los ataques de tiburones a lo largo del tiempo, incluyendo variaciones estacionales y diurnas.
    2. **Análisis Geográfico**: Determinar las regiones con mayor incidencia de ataques de tiburones y explorar posibles factores geográficos que contribuyan a estos patrones.
    3. **Perfil de las Víctimas**: Examinar las características demográficas de las víctimas, como la edad y el género, para identificar grupos de alto riesgo.
    4. **Actividades de Riesgo**: Identificar las actividades que presentan un mayor riesgo de ataques de tiburones y proporcionar recomendaciones para mitigar estos riesgos.
    5. **Especies de Tiburones**: Analizar las especies de tiburones más comunes en los ataques y explorar sus comportamientos y hábitats.
    6. **Impacto de Factores Ambientales**: Investigar cómo factores ambientales, como la temperatura del agua y la presencia de presas, influyen en la frecuencia y ubicación de los ataques de tiburones.
    7. **Desarrollo de Herramientas de Visualización**: Crear visualizaciones interactivas que permitan a los usuarios explorar los datos y descubrir patrones por sí mismos.
    8. **Generación de Informes y Recomendaciones**: Compilar los hallazgos en informes detallados y proporcionar recomendaciones basadas en los datos para mejorar la seguridad en el agua.

    Estos objetivos nos permitirán comprender mejor los ataques de tiburones y desarrollar estrategias efectivas para reducir su incidencia y mejorar la seguridad de las personas en el agua.
    """)

elif menu == 'Proceso de Desarrollo':
    st.header('Proceso de Desarrollo 🚀')
    st.write("""
    El proceso de desarrollo de este proyecto se llevó a cabo en varias etapas, cada una de las cuales fue crucial para alcanzar los objetivos establecidos. A continuación se describen las etapas principales del proceso:

    ### 1. Recolección de Datos 📥
    - **Fuentes de Datos**: Se recopilaron datos de diversas fuentes, incluyendo bases de datos públicas, informes de incidentes y registros históricos.
    - **Formato de los Datos**: Los datos se obtuvieron en diferentes formatos, como archivos CSV, bases de datos SQL y APIs.
    - **Almacenamiento de Datos**: Los datos recopilados se almacenaron en un repositorio centralizado para facilitar su acceso y análisis.

    ### 2. Limpieza de Datos 🧹
    - **Eliminación de Duplicados**: Se eliminaron registros duplicados para asegurar la integridad de los datos.
    - **Manejo de Valores Faltantes**: Se abordaron los valores faltantes mediante técnicas como la imputación y la eliminación de registros incompletos.
    - **Normalización de Datos**: Se estandarizaron las unidades de medida y los formatos de fecha para asegurar la consistencia de los datos.
    - **Verificación de Calidad**: Se realizaron verificaciones de calidad para identificar y corregir errores en los datos.

    ### 3. Análisis de Datos 🔍
    - **Exploración de Datos**: Se realizó un análisis exploratorio de los datos para identificar patrones y tendencias iniciales.
    - **Análisis Estadístico**: Se aplicaron técnicas estadísticas para cuantificar las relaciones entre diferentes variables.
    - **Modelado Predictivo**: Se desarrollaron modelos predictivos para anticipar la probabilidad de ataques de tiburones en diferentes condiciones.

    ### 4. Visualización de Datos 📊
    - **Gráficos Interactivos**: Se crearon gráficos interactivos utilizando herramientas como Matplotlib y Seaborn para facilitar la exploración de los datos.
    - **Dashboards**: Se desarrollaron dashboards interactivos con Streamlit para permitir a los usuarios visualizar y analizar los datos de manera intuitiva.
    - **Mapas Geoespaciales**: Se utilizaron herramientas de mapeo geoespacial para visualizar la distribución geográfica de los ataques de tiburones.

    ### 5. Reporte 📝
    - **Documentación de Resultados**: Se documentaron los hallazgos del análisis de datos en informes detallados.
    - **Presentaciones**: Se prepararon presentaciones para comunicar los resultados a diferentes audiencias, incluyendo investigadores, autoridades y el público en general.
    - **Recomendaciones**: Se proporcionaron recomendaciones basadas en los datos para mejorar la seguridad en el agua y reducir la incidencia de ataques de tiburones.

    Este proceso de desarrollo estructurado nos permitió abordar de manera efectiva los objetivos del proyecto y generar información valiosa sobre los ataques de tiburones.
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