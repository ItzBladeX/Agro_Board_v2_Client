import streamlit as st
from .ui.text import centered_matrix


def render_weather_matrix(weather):
    temperature = "-" if weather is None else f"☀️ {weather['temperature']} °C"
    windspeed = "-" if weather is None else f"💨 {weather["windspeed"]} km/h" 
    rainfall = "-" if weather is None else f"🌧️ {weather["rainfall"]} mm"
    station = "-" if weather is None else  f"🏠 {weather["city"]}"
    st.title("Today's Weather Report",text_alignment="center")
    centered_matrix()
    matric_1, matric_2, matric_3, matric_4 = st.columns(4)
    with matric_1:
        st.metric(label ="Temperature", value = temperature, border=True)
    with matric_2:
        st.metric(label = "Wind Speed", value = windspeed, border=True)
    with matric_3:
        st.metric(label = "Rainfall", value = rainfall, border=True)
    with matric_4:
        st.metric(label = "Weather Station", value = station, border=True)
