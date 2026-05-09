import streamlit as st
from app.components import render_signup_form, render_login_form
import time


def auth_view():
    
    if "auth_form_mode" not in st.session_state:
        st.session_state.auth_form_mode = "Log In"


    if st.session_state.auth_form_mode == "Log In":
        user = render_login_form()
        login(user)

    elif st.session_state.auth_form_mode == "Sign Up":
        user = render_signup_form()
        login(user)

    

def login(user):
    if user:
        st.session_state.user = user.id
        time.sleep(2)
        st.rerun()






