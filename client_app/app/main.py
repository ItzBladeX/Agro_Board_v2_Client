import streamlit as st
# import weather
import client_app.app.functions as func
import shelve
import streamlit_option_menu as om
import time
from millify import millify
from streamlit_javascript import st_javascript
st.set_page_config(page_title="AGRO-BOARD", layout="wide", )
st.logo("logo.png", size='large')


width = st_javascript("window.innerWidth", key="main_width")
func.render_nav("main", width)
time.sleep(0.5)

st.markdown("""
<style>
    /* Target the default nav section in sidebar */
    [data-testid="stSidebar"] > div > div > div > section > div:first-child {
        display: none !important;
    }
    /* Alternative selector if above doesn't catch it (more broad) */
    /* section[data-testid="stSidebar"] nav { display: none !important; } */
</style>
""", unsafe_allow_html=True)

crop_db = "crop_database"
livestock_db = "livestock_database"
inventory_db = "inventory_database"

with st.container():  # Weather Section
    st.markdown("""   
    <style text-align: center>
    [data-testid="stMetricLabel"],
    [data-testid="stTitle"],
    [data-testid="stMetric"] {
        text-align: center !important;
        display: block !important;
    }
    </style>          
    <h2 style="color:#013014ff; text-align: center; font-family: Arial, sans-serif;"> Today's Weather Report </h2>
    """, unsafe_allow_html=True)  # CSS Styling for the st.metric and Title

    st.divider()
    matric_col1, matric_col2, matric_col3, matric_col4 = st.columns(4)
    st.set_page_config(page_title="AGRO-BOARD", layout="wide")
    #Todo: change the following matric to a "display_matric" function for simplicity 
    with st.spinner("Fetching Weather Data..."):
        with matric_col1:
            st.metric(label="Temperature", value=func.get_weather('temp'), border=True)
        with matric_col2:
            st.metric("Wind Speed", func.get_weather('wind'), border=True)
        with matric_col3:
            st.metric("Precipitation", func.get_weather('rainfall'), border=True)
        with matric_col4:
            st.metric("Weather Station", func.get_weather('station'), border=True)

    st.divider()

with shelve.open("config") as db:
    try:
        SN = db["SN"]
        name = db["name"]
    except KeyError:
        func.configuration()
# Widgets

st.markdown("""

<h2 style="color: #013014ff; text-align: center; font-family: Arial, sans-serif;"> Statistics and Data </h2>


""", unsafe_allow_html=True)
# Crop
with st.expander("Crop Data"):
    st.markdown("""<h3 style="color: #013014ff; text-align: center; font-family: Arial, sans-serif;"> Crops </h3>""", unsafe_allow_html=True)
    st.divider()
    func.display_graph(database=crop_db, filter_on=True) # yr - years user selected
        
    
    # Livestock

with st.expander("LiveStock Data"):
    st.markdown("""<h3 style=" color: #013014ff; text-align: center; font-family: Arial, sans-serif;"> LiveStocks </h3>""", unsafe_allow_html=True)
    func.display_graph(livestock_db, filter_on=True)
for _ in range(3):
    st.write("")


with st.container(border=True):
    st.markdown("""<h3 style=" color: #013014ff; text-align: center; font-family: Arial, sans-serif;"> Setting </h3>""", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:

        with shelve.open('config') as db:
            st.button(" ⬆️ Upload Data", on_click=func.package_data, width="stretch", disabled=func.check_sn(), type="secondary")
    with col2:

        with shelve.open('config') as db:
            st.button("⚙️ Edit Personal / Config /  Data", on_click=func.edit_config, width="stretch", disabled=func.check_sn(), type="secondary")


