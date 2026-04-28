import streamlit as st
from services import create_user, auth_user


def mode_buttons(login = "secondary", signup = "secondary"):
    leftb, rightb = st.columns(2)
        
    with leftb: 
        st.button("Log-in", type=login, on_click=set_mode, args=("login",), width="stretch")
    
    with rightb: 
        st.button("Sign-up", type=signup,on_click=set_mode, args=("signup",),width="stretch")

def set_mode(mode):
    st.session_state.auth_form_mode = mode

def render_signup_form():
   
        
    left, center, right = st.columns([1,2,1])

    with center:
        with st.container(border=True):
            mode_buttons(signup="primary")

            st.title("Sign-up",text_alignment="center")
            st.divider()

            with st.form("signup_form"):
                mandatory, non_mandatory = st.columns(2)
                with mandatory:
                    st.success("Mandatory Fields")
                    name = st.text_input(label="Full Name", key="sighup name",  icon="👤")
                    passwd = st.text_input(label="Password", type="password", key="signup_password",  icon=":material/lock:")
                    check_passwd = st.text_input(label="Confirm Password", type="password",  icon=":material/lock:")
                with non_mandatory:
                    st.info("Non-Mandatory Fields")
                    age = st.number_input(label="Age",value=None, step=1)
                    gender = st.radio(label="Gender", options=[None,"Male", "Female"], horizontal=True, width="stretch")
                    land_area = st.number_input(label="Land area [Ha]", step=0.1)

                submit = st.form_submit_button("Sign-up", key="signup_button", width="stretch", type="primary",  icon=":material/upload:")
            
            if submit:
                if not name:
                    st.error("Please Provide your Full Name")

                if not passwd:
                    st.error("Please provide a password")

                if passwd != check_passwd:
                    st.error("Password Don't Match")

                elif all([name, passwd, check_passwd]):
                    user = create_user(
                        name = name,
                        passwd = passwd,
                        age = age,
                        gender = gender,
                        land_area = land_area if land_area > 0 else None)
                    
                    if user:
                        st.success("Successfully Signed Up")
                        return user

                    else:
                        st.error("Something Went Wrong")
                        return False


def render_login_form():

    left, center, right = st.columns(3)
    with center:
        with st.container(border=True):
            mode_buttons(login="primary")

            st.title("Login",text_alignment="center")
            st.divider()

            with st.form("Login Form"):
                name = st.text_input(label="Full Name", key="login_name", icon="👤")
                passwd = st.text_input("Password", type="password", key="login_password",  icon=":material/lock:")
                login = st.form_submit_button("Login", width="stretch", type="primary", key="login_button",  icon=":material/login:")
        
            if login:
                if not name:
                    st.error("Please provide a name")

                if not passwd:
                    st.error("Please provide a password")

                if all([name, passwd]):
                    user = auth_user(name=name, passwd=passwd)

                    if user:
                        st.success("Successful")
                        return user
                    
                    else:
                        st.error("Invalud Username or Password")
                        return False

