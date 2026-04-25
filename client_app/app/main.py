import streamlit as st
# Components
from components.navbar import render_navbar
# Pages

from app.pages.about import about_page
from app.pages.crop import crop_page
from app.pages.inventory import inventory_page
from app.pages.liveStock import livestock_page
from app.pages.home import home_page

# import weather
# import client_app.app.functions as func
import time
from millify import millify
from streamlit_javascript import st_javascript


st.set_page_config(page_title="AGRO-BOARD", layout="wide", )
# st.logo("logo.png", size='large')

PAGES = {
    "Home": home_page,
    "Crop": crop_page,
    "Livestock": livestock_page,
    "Inventory": inventory_page,
    "About": about_page,
    }

if "page" not in st.session_state:
    st.session_state.page = "Home"
if "window_width" not in st.session_state:
    st.session_state.window_width = st_javascript("window.innerWidth", key="main_width") 

def navbar():  
    width = st.session_state.window_width
    current_page = st.session_state.page
    selected = render_navbar(current_page, width, PAGES)
    if selected != current_page:
        st.session_state.page = selected
        st.rerun()
    PAGES[st.session_state.page]()


def login():
    pass
def main():
    # session_states()
    navbar()
main()
    


