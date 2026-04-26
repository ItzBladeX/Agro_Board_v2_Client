import streamlit as st
# Components
from components import render_navbar
from services import get_user_by_id
# Pages

from views import *

# import weather
# import client_app.app.functions as func
import time
from millify import millify
from streamlit_javascript import st_javascript


st.set_page_config(page_title="AGRO-BOARD", layout="wide", )
# st.logo("logo.png", size='large')

if "page" not in st.session_state:
    st.session_state.page = "Home"
if "window_width" not in st.session_state:
    st.session_state.window_width = st_javascript("window.innerWidth", key="main_width") 
if "user" not in st.session_state:
    st.session_state.user = None
PAGES = {
    "Home": home_view,
    "Crop": crop_view,
    "Livestock": livestock_view,
    "Inventory": inventory_view,
    "About": about_view,
    }


def navbar():  
    render_navbar(PAGES)
    PAGES[st.session_state.page]()

def sidebar():
    with st.sidebar:
        user = get_user_by_id(st.session_state.user)
        st.write(f"Name: {user.name}")
        logout = st.button("Log out", type="primary", width="stretch")
        if logout:
            st.session_state.user = None
            st.rerun()

def main():
    if  st.session_state.user == None:
        auth_view()
    # session_states()
    else:
        sidebar()
        navbar()

main()
    


