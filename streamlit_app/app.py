import streamlit as st
import pandas as pd
import os

# Load data
@st.cache_data
def load_data():
    # Use a relative path
    file_path = os.path.join(os.path.dirname(__file__), '..', 'notebooks', 'cleaned_data.csv')
    return pd.read_csv(file_path)

df_cleaned = load_data()

# Application title
st.title('Shark Data Analysis')

# Description
st.write("""
This application displays the charts and conclusions of the shark data analysis.
""")

# Add image to the main page
main_image_path = os.path.join(os.path.dirname(__file__), 'images', 'nemo.jpg')
if os.path.exists(main_image_path):
    st.image(main_image_path, caption='Shark Data Analysis')

# Navigation menu
st.sidebar.title('Navigation Menu')

# Add image to the sidebar
sidebar_image_path = os.path.join(os.path.dirname(__file__), 'images', 'nemo.png')
if os.path.exists(sidebar_image_path):
    st.sidebar.image(sidebar_image_path, caption='Navigation Menu')

# Button to go to the GitHub repository
st.sidebar.markdown("[Go to GitHub Repository](https://github.com/Jotis86/Shark-Analysis-Project)")

menu = st.sidebar.radio('Select a section:', ['Project Objectives', 'Development Process', 'Visualizations', 'Power BI', 'Final Conclusions', 'Recommendations'])

if menu == 'Project Objectives':
    st.header('Project Objectives 🎯')
    st.write("""
    The main objective of this project is to analyze and visualize shark attack data to gain insights into patterns and trends. 📊
    
    
    1. **Identification of Temporal Patterns**: Analyze how shark attacks vary over time, including seasonal and diurnal variations.
    2. **Geographic Analysis**: Determine the regions with the highest incidence of shark attacks and explore possible geographic factors contributing to these patterns.
    3. **Victim Profile**: Examine the demographic characteristics of the victims, such as age and gender, to identify high-risk groups.
    4. **Risk Activities**: Identify activities that present a higher risk of shark attacks and provide recommendations to mitigate these risks.
    5. **Shark Species**: Analyze the most common shark species in attacks and explore their behaviors and habitats.
    6. **Impact of Environmental Factors**: Investigate how environmental factors, such as water temperature and prey presence, influence the frequency and location of shark attacks.
    7. **Development of Visualization Tools**: Create interactive visualizations that allow users to explore the data and discover patterns themselves.
    8. **Generation of Reports and Recommendations**: Compile the findings into detailed reports and provide data-driven recommendations to improve water safety.

    These objectives will allow us to better understand shark attacks and develop effective strategies to reduce their incidence and improve people's safety in the water.
    """)

elif menu == 'Development Process':
    st.header('Development Process 🚀')
    st.write("""
    The development process of this project was carried out in several stages, each of which was crucial to achieving the established objectives. The main stages of the process are described below:

    ### 1. Data Collection 📥
    - **Data Sources**: Data was collected from various sources, including public databases, incident reports, and historical records.
    - **Data Formats**: Data was obtained in different formats, such as CSV files, SQL databases, and APIs.
    - **Data Storage**: Collected data was stored in a centralized repository to facilitate access and analysis.

    ### 2. Data Cleaning 🧹
    - **Duplicate Removal**: Duplicate records were removed to ensure data integrity.
    - **Handling Missing Values**: Missing values were addressed using techniques such as imputation and removal of incomplete records.
    - **Data Normalization**: Units of measurement and date formats were standardized to ensure data consistency.
    - **Quality Verification**: Quality checks were performed to identify and correct errors in the data.

    ### 3. Data Analysis 🔍
    - **Data Exploration**: An exploratory data analysis was conducted to identify initial patterns and trends.
    - **Statistical Analysis**: Statistical techniques were applied to quantify relationships between different variables.
    - **Predictive Modeling**: Predictive models were developed to anticipate the likelihood of shark attacks under different conditions.

    ### 4. Data Visualization 📊
    - **Interactive Charts**: Interactive charts were created using tools like Matplotlib and Seaborn to facilitate data exploration.
    - **Dashboards**: Interactive dashboards were developed with Streamlit to allow users to visualize and analyze data intuitively.
    - **Geospatial Maps**: Geospatial mapping tools were used to visualize the geographic distribution of shark attacks.

    ### 5. Reporting 📝
    - **Documentation of Results**: The findings of the data analysis were documented in detailed reports.
    - **Presentations**: Presentations were prepared to communicate the results to different audiences, including researchers, authorities, and the general public.
    - **Recommendations**: Recommendations based on the data were provided to improve water safety and reduce the incidence of shark attacks.

    This structured development process allowed us to effectively address the project's objectives and generate valuable insights into shark attacks.
    """)

elif menu == 'Visualizations':
    st.header('Visualizations 📊')
    st.write("Select a chart from the menu on the left to view it.")
    
    # Chart selection menu
    options = {
        'Age Range Distribution': 'age.png',
        'Gender Distribution': 'sex.png',
        'Top 5 Activities with Most Attacks': 'activities.png',
        'Top 10 Most Common Shark Types': 'sharks.png',
        'Frequency of Oceans and Seas': 'ocean.png',
        'Time Distribution': 'time.png',
        'Monthly Attack Distribution': 'month.png',
        'Number of Attacks in the Last 10 Years': 'years.png',
        'Continent Attack Distribution': 'continent.png'
    }

    selected_option = st.sidebar.radio('Select a chart', list(options.keys()))

    if selected_option:
        image_path = os.path.join(os.path.dirname(__file__), 'images', options[selected_option])
        if os.path.exists(image_path):
            st.image(image_path, caption=selected_option)
        else:
            st.error(f"Could not find the image: {image_path}")

elif menu == 'Power BI':
    st.header('Power BI 📊')
    st.write("Below are some Power BI visualizations related to the shark data analysis.")
    
    # Add Power BI images
    power_bi_image1_path = os.path.join(os.path.dirname(__file__), 'images', 'picture_1.png')
    power_bi_image2_path = os.path.join(os.path.dirname(__file__), 'images', 'picture_2.png')
    
    if os.path.exists(power_bi_image1_path):
        st.image(power_bi_image1_path, caption='Power BI Visualization 1')
    else:
        st.error(f"Could not find the image: {power_bi_image1_path}")
    
    if os.path.exists(power_bi_image2_path):
        st.image(power_bi_image2_path, caption='Power BI Visualization 2')
    else:
        st.error(f"Could not find the image: {power_bi_image2_path}")
    
    # Add Power BI video
    power_bi_video_path = os.path.join(os.path.dirname(__file__), 'images', 'clip.mp4') 
    if os.path.exists(power_bi_video_path): 
        st.video(power_bi_video_path) 
    else: st.error(f"Could not find the video: {power_bi_video_path}")


elif menu == 'Final Conclusions':
    st.header('Final Conclusions 📊')
    st.write("""
    - **Age**: The age range most affected by shark attacks is 21-30 years. This is likely because this age group participates in more water activities. 🏄‍♂️
    - **Gender**: 86.5% of shark attacks are on men, making them the highest-risk group. 👨
    - **High-Risk Activities**: The activities with the highest risk of shark attacks are surfing 🏄‍♂️, followed by swimming 🏊‍♂️ and fishing 🎣.
    - **Frequency of Attacks by Ocean**: The oceans with the most shark attacks are the Pacific Ocean 🌊, the Atlantic Ocean 🌊, and the Indian Ocean 🌊.
    - **Temporal Distribution of Attacks**: Most shark attacks occur in the afternoon 🌅, followed by the morning 🌄 and finally at night 🌃.
    - **Countries**: The countries with the most shark attacks are the United States 🇺🇸, Australia 🇦🇺, and South Africa 🇿🇦, likely due to the higher prevalence of activities such as surfing and swimming in these regions.
    """)

elif menu == 'Recommendations':
    st.header('Recommendations 📋')
    st.write("""
    Based on the analysis, the following recommendations are proposed:

    1. **Increase Awareness and Safety Measures**: 
       - 📢 Direct information and safety guidelines to high-risk groups, such as surfers and swimmers.
       - 🦈 Implement and promote the use of shark deterrent devices in high-risk areas.

    2. **Seasonal and Time-Based Precautions**: 
       - 📅 Increase surveillance and safety measures during months with higher incidence of attacks (July, January, August, and September) and times of the day (afternoon).
       - 🚫 Encourage swimmers to avoid swimming during high-risk times.

    3. **Geographic Focus**: 
       - 🌍 Focus safety campaigns and resources on regions with the highest number of attacks, such as North America, Oceania, and Africa.
       - 🤝 Collaborate with local authorities in these regions to improve shark surveillance and response strategies.

    4. **Additional Research**: 
       - 🔬 Conduct further studies to understand the underlying factors contributing to the high number of attacks in specific regions and activities.
       - 🌐 Explore the impact of environmental changes on shark behavior and attack patterns.
    """)