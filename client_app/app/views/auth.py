import streamlit as st
from components import centered_title 

if "mode" not in st.session_state:
    st.session_state.mode = "login"

def auth_view():
    
    left, center, right = st.columns(3)
    with center:
        with st.container(border=True):
            mode()

def set_mode(mode):
    st.session_state.mode = mode
    
def mode():
    left, right = st.columns(2)
    login_view_button_type = "secondary" if st.session_state.mode == "login" else "tertiary"
    register_view_button_type = "secondary" if st.session_state.mode == "register" else "tertiary"
    with left: 
        st.button("Login", 
                  type=login_view_button_type , 
                  width="stretch", 
                  on_click=set_mode, 
                  args=("login",)
                  )
    with right: 
        st.button("Register", 
                  type=register_view_button_type, 
                  width="stretch", 
                  on_click=set_mode, 
                  args=("register",)
                  )

    if st.session_state.mode == "login":
        login()
    if st.session_state.mode == "register":
        register()

def register():
    
    st.title("Register",text_alignment="center")
    st.divider()

    st.text_input(label="Full Name", key="register name")
    st.text_input(label="Password", type="password", key="register_password")
    st.text_input(label="Confirm Password", type="password")
    with st.expander("Non-Mandatory"):
        st.number_input(label="Age",step=1)
        st.number_input(label="Land area", step=0.1)
    st.button("Register", key="register_button", width="stretch", type="primary")


def login():
    
    st.title("Login",text_alignment="center")
    st.divider()
    st.text_input(label="Full Name", key="login_name")
    st.text_input("Password", type="password", key="login_password")
    st.button("Login", width="stretch", type="primary", key="login_button")



