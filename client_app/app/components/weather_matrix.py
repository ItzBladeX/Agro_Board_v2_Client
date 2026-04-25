import streamlit as st
from components.ui.text import centered_title


def render_weather_matrix(weather):
    centered_title("Today's weather Report")  
    matric_1, matric_2, matric_3, matric_4 = st.columns(4)
    
    with matric_1:
        st.metric(label="Temperature", value = f"☀️ {weather["temperature"]} °C", border=True)
    with matric_2:
        st.metric("Wind Speed", value = f"💨 {weather["windspeed"]} km/h", border=True)
    with matric_3:
        st.metric("Rainfall", value = f"🌧️ {weather["rainfall"]} mm", border=True)
    with matric_4:
        st.metric("Weather Station", f"🏠 {weather["city"]}", border=True)