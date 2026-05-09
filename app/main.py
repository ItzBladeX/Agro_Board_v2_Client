import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
# Components
from app.components import render_navbar, render_profile, render_settings
from app.services import get_user

# Pages

from app.views import *

# import weather
# import client_app.app.functions as func
import time
from millify import millify
from streamlit_javascript import st_javascript


st.set_page_config(page_title="AGRO-BOARD", layout="wide", initial_sidebar_state="collapsed")

# This markdown is required to disable the "Show password eye" that egde forces on 
# text input of type=password.
st.markdown("""
    <style>
   input::-ms-reveal, input::-ms-clear { display: none !important; }
   </style>
   """, unsafe_allow_html=True)

st.logo("app/assets/logo.png", size='large')

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
    user = get_user(st.session_state.user)
    with st.sidebar:
        with st.container(border=True):
            render_profile(user)

            if st.button("Setting", icon=":material/settings:",width="stretch"):
                render_settings(user)

        if st.button("Log out", type="primary", width="stretch",  icon=":material/logout:"):

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
    


