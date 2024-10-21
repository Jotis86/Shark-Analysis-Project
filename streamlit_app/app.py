import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

# Mostrar las primeras 5 filas del dataset
st.subheader('Primeras 5 Filas del Dataset')
st.write(df_cleaned.head())

# Menú de selección de gráficos
st.sidebar.title('Menú de Gráficos')
options = {
    'Distribución de Rangos de Edad': st.sidebar.checkbox('Distribución de Rangos de Edad'),
    'Distribución por Sexo': st.sidebar.checkbox('Distribución por Sexo'),
    'Top 5 Actividades con Más Ataques': st.sidebar.checkbox('Top 5 Actividades con Más Ataques'),
    'Top 10 Tipos de Tiburones Más Comunes': st.sidebar.checkbox('Top 10 Tipos de Tiburones Más Comunes'),
    'Frecuencia de Océanos y Mares': st.sidebar.checkbox('Frecuencia de Océanos y Mares'),
    'Distribución por Tiempo': st.sidebar.checkbox('Distribución por Tiempo'),
    'Distribución de Ataques por Mes': st.sidebar.checkbox('Distribución de Ataques por Mes'),
    'Número de Ataques en los Últimos 10 Años': st.sidebar.checkbox('Número de Ataques en los Últimos 10 Años'),
    'Top 10 Países con Más Ataques': st.sidebar.checkbox('Top 10 Países con Más Ataques'),
    'Continente con Más Ataques': st.sidebar.checkbox('Continente con Más Ataques'),
    'Distribución de Ataques por Continente': st.sidebar.checkbox('Distribución de Ataques por Continente')
}

# Función para mostrar el gráfico seleccionado
def show_plot(option):
    if option == 'Distribución de Rangos de Edad':
        bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
        df_cleaned['AgeRange'] = pd.cut(df_cleaned['Age'], bins=bins, labels=labels, right=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(x='AgeRange', data=df_cleaned, palette='viridis', ax=ax)
        ax.set_title('Distribution of Age Ranges')
        ax.set_xlabel('Age Range')
        ax.set_ylabel('Frequency')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        st.pyplot(fig)
        st.write("Este gráfico muestra la distribución de los rangos de edad de las víctimas de ataques de tiburones.")
    elif option == 'Distribución por Sexo':
        fig, ax = plt.subplots(figsize=(8, 8))
        df_cleaned['Sex'].value_counts().plot.pie(autopct='%1.1f%%', colors=['#ff9999','#66b3ff'], startangle=90, explode=(0.1, 0), ax=ax)
        ax.set_title('Distribution of Sex')
        ax.set_ylabel('')
        st.pyplot(fig)
        st.write("Este gráfico muestra la distribución por sexo de las víctimas de ataques de tiburones.")
    elif option == 'Top 5 Actividades con Más Ataques':
        activity_counts = df_cleaned['Activity'].value_counts()
        top_5_activities = activity_counts.head(5)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=top_5_activities.values, y=top_5_activities.index, palette='viridis', ax=ax)
        ax.set_title('Top 5 Activities with Most Attacks')
        ax.set_xlabel('Number of Attacks')
        ax.set_ylabel('Activity')
        st.pyplot(fig)
        st.write("Este gráfico muestra las 5 actividades con más ataques de tiburones.")
    elif option == 'Top 10 Tipos de Tiburones Más Comunes':
        shark_counts = df_cleaned['Species'].value_counts()
        top_10_sharks = shark_counts.head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=top_10_sharks.values, y=top_10_sharks.index, palette='viridis', ax=ax)
        ax.set_title('Top 10 Most Common Shark Types')
        ax.set_xlabel('Number of Occurrences')
        ax.set_ylabel('Shark Type')
        st.pyplot(fig)
        st.write("Este gráfico muestra los 10 tipos de tiburones más comunes en los ataques.")
    elif option == 'Frecuencia de Océanos y Mares':
        df_cleaned['Ocean_Sea'] = df_cleaned['Ocean_Sea'].astype(str).fillna('')
        df_cleaned['Ocean_Sea'] = df_cleaned['Ocean_Sea'].str.replace(', ', ' and ')
        df_cleaned['Ocean_Sea'] = df_cleaned['Ocean_Sea'].str.split(' and ')
        df_exploded = df_cleaned.explode('Ocean_Sea')
        df_exploded['Ocean_Sea'] = df_exploded['Ocean_Sea'].str.strip()
        df_exploded['Ocean_Sea'] = df_exploded['Ocean_Sea'].str.replace('and', '', regex=False).str.strip()
        ocean_counts = df_exploded['Ocean_Sea'].value_counts()
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(y=ocean_counts.index, x=ocean_counts.values, palette='viridis', orient='h', ax=ax)
        ax.set_title('Frequency of Oceans and Seas')
        ax.set_xlabel('Number of Attacks')
        ax.set_ylabel('Ocean or Sea')
        st.pyplot(fig)
        st.write("Este gráfico muestra la frecuencia de ataques de tiburones por océano o mar.")
    elif option == 'Distribución por Tiempo':
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(x='Time', data=df_cleaned, palette='viridis', ax=ax)
        ax.set_title('Distribution of Time')
        ax.set_xlabel('Time')
        ax.set_ylabel('Frequency')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        st.pyplot(fig)
        st.write("Este gráfico muestra la distribución de los ataques de tiburones por hora del día.")
    elif option == 'Distribución de Ataques por Mes':
        df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'], errors='coerce')
        df_cleaned['Month'] = df_cleaned['Date'].dt.month
        month_counts = df_cleaned['Month'].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(x=month_counts.index, y=month_counts.values, palette='viridis', ax=ax)
        ax.set_title('Distribution of Attacks by Month')
        ax.set_xlabel('Month')
        ax.set_ylabel('Number of Attacks')
        st.pyplot(fig)
        st.write("Este gráfico muestra la distribución de ataques de tiburones por mes.")
    elif option == 'Número de Ataques en los Últimos 10 Años':
        df_cleaned['Year'] = df_cleaned['Date'].dt.year
        filtered_years = df_cleaned[(df_cleaned['Year'] >= 2014) & (df_cleaned['Year'] <= 2023)]
        year_counts = filtered_years['Year'].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(x=year_counts.index, y=year_counts.values, palette='viridis', ax=ax)
        ax.set_title('Number of Attacks from 2014 to 2023')
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Attacks')
        st.pyplot(fig)
        st.write("Este gráfico muestra el número de ataques de tiburones desde 2014 hasta 2023.")
    elif option == 'Top 10 Países con Más Ataques':
        country_counts = df_cleaned['Country'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(x=country_counts.index, y=country_counts.values, palette='viridis', ax=ax)
        ax.set_title('Top 10 Countries with Most Attacks')
        ax.set_xlabel('Country')
        ax.set_ylabel('Number of Attacks')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        st.pyplot(fig)
        st.write("Este gráfico muestra los 10 países con más ataques de tiburones.")
    elif option == 'Continente con Más Ataques':
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(x='Continent', data=df_cleaned, palette='viridis', ax=ax)
        ax.set_title('Continent with Most Attacks')
        ax.set_xlabel('Continent')
        ax.set_ylabel('Number of Attacks')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        st.pyplot(fig)
        st.write("Este gráfico muestra el continente con más ataques de tiburones.")
    elif option == 'Distribución de Ataques por Continente':
        fig, ax = plt.subplots(figsize=(10, 10))
        num_categories = df_cleaned['Continent'].nunique()
        explode = [0.1] + [0] * (num_categories - 1)
        def func(pct):
            return "{:.0f}%".format(pct)
        pie_plot = df_cleaned['Continent'].value_counts().plot.pie(
            autopct=lambda pct: func(pct), 
            colors=['#ff9999','#66b3ff','#99ff99','#ffcc99', '#c2c2f0', '#ffb3e6'],
            startangle=90, 
            explode=explode,
            pctdistance=0.85,  
            textprops={'fontsize': 10},  
            labels=['']*num_categories,  
            ax=ax
        )
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig.gca().add_artist(centre_circle)
        ax.set_title('Distribution of Attacks by Continent', fontsize=16)
        ax.set_ylabel('')
        ax.legend(labels=df_cleaned['Continent'].value_counts().index, loc="best", fontsize=12)
        plt.tight_layout()
        st.pyplot(fig)
        st.write("Este gráfico muestra la distribución de ataques de tiburones por continente.")

# Mostrar los gráficos seleccionados
for option, selected in options.items():
    if selected:
        show_plot(option)

# Conclusiones finales del análisis
st.subheader('Conclusiones finales del análisis')
st.write("""
- **Edad**: el rango de edad más afectado por los ataques de tiburones es el de 21-30 años. Esto probablemente se deba a que este grupo de edad participa en más actividades acuáticas.
- **Género**: el 87.2% de los ataques de tiburones son a hombres, lo que los convierte en el grupo con mayor riesgo.
- **Actividades de Mayor Riesgo**: las actividades con mayor riesgo de ataques de tiburones son el surf, seguido de la natación y la pesca.
- **Frecuencia de Ataques por Océano**: los océanos con más ataques de tiburones son el Océano Pacífico, el Océano Atlántico y el Océano Índico.
- **Distribución Temporal de los Ataques**: la mayoría de los ataques de tiburones ocurren en la tarde, seguidos por la mañana y finalmente por la noche.
- **Países**: los países con más ataques de tiburones son Estados Unidos, Australia y Sudáfrica, probablemente debido a la mayor prevalencia de actividades como el surf y la natación en estas regiones.
""")