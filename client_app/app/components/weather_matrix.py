import streamlit as st
from components.ui.text import centered_title


def render_weather_matrix(weather):
    temperature = "-" if weather is None else f"☀️ {weather['temperature']} °C"
    windspeed = "-" if weather is None else f"💨 {weather["windspeed"]} km/h" 
    rainfall = "-" if weather is None else f"🌧️ {weather["rainfall"]} mm"
    station = "-" if weather is None else  f"🏠 {weather["city"]}"
    centered_title("Today's Weather Report")
    matric_1, matric_2, matric_3, matric_4 = st.columns(4)
    with matric_1:
        st.metric(label ="Temperature", value = temperature, border=True)
    with matric_2:
        st.metric(label = "Wind Speed", value = windspeed, border=True)
    with matric_3:
        st.metric(label = "Rainfall", value = rainfall, border=True)
    with matric_4:
        st.metric(label = "Weather Station", value = station, border=True)
