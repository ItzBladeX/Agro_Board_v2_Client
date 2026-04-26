import streamlit as st
from services import signup_user
from services import login_user
import time

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
    register_view_button_type = "secondary" if st.session_state.mode == "sighup" else "tertiary"
    with left: 
        st.button("Login", type=login_view_button_type , width="stretch", on_click=set_mode, args=("login",))
    with right: 
        st.button("Sign Up", type=register_view_button_type, width="stretch", on_click=set_mode, args=("sighup",))

    if st.session_state.mode == "login":
        login()
    if st.session_state.mode == "sighup":
        sighup()

def sighup():
    
    st.title("Register",text_alignment="center")
    st.divider()

    with st.form("register_form"):
        name = st.text_input(label="Full Name", key="sighup name")
        passwd = st.text_input(label="Password", type="password", key="register_password")
        check_passwd = st.text_input(label="Confirm Password", type="password")
        with st.expander("Non-Mandatory"):
            age = st.number_input(label="Age",step=1)
            land_area = st.number_input(label="Land area", step=0.1)
        submit = st.form_submit_button("Sign Up", key="register_button", width="stretch", type="primary")
    
    if submit:
        if name == None:
            st.error("Please Provide your Full Name")
        if passwd == None or check_passwd == None:
            st.error("Please provide a passwd")
        if passwd != check_passwd:
            st.error("Password Dont Match")
        if all([name, passwd, check_passwd]):
            status = signup_user(name = name, passwd = passwd, age = age, land_area=land_area)
            if status == True:
                st.success("Successfully Signed Up")
                time.sleep(2)
                set_mode("login")
                st.rerun()
            elif status == False:
                st.error("Something Went Wrong")


def login():
    
    st.title("Login",text_alignment="center")
    st.divider()
    with st.form("Login Form"):
        name = st.text_input(label="Full Name", key="login_name")
        passwd = st.text_input("Password", type="password", key="login_password")
        submit = st.form_submit_button("Login", width="stretch", type="primary", key="login_button")
    if submit == True:
        if name == None:
            st.error("Please provide a name")
        if passwd == None:
            st.error("Please provide a password")

        if all([name, passwd]):
            user = login_user(name=name, passwd=passwd)
            if user:
                st.success("Successful")
                time.sleep(2)
                st.session_state.user = user.id
                st.rerun()
            else:
                st.error("Invalud Username or Password")





