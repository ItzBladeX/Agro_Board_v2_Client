import streamlit as st
# Components
from components import render_navbar
# Pages

from views import *

# import weather
# import client_app.app.functions as func
import time
from millify import millify
from streamlit_javascript import st_javascript


st.set_page_config(page_title="AGRO-BOARD", layout="wide", )
# st.logo("logo.png", size='large')

PAGES = {
    "Home": home_view,
    "Crop": crop_view,
    "Livestock": livestock_view,
    "Inventory": inventory_view,
    "About": about_view,
    }

if "page" not in st.session_state:
    st.session_state.page = "Home"
if "window_width" not in st.session_state:
    st.session_state.window_width = st_javascript("window.innerWidth", key="main_width") 

def navbar():  
    render_navbar(PAGES)
    PAGES[st.session_state.page]()


def login():
    pass
def main():
    # session_states()
    navbar()

main()
    


