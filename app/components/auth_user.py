import streamlit as st
from services import create_user, auth_user


def mode_buttons():

    st.segmented_control("Mode", key="auth_form_mode",options=["Log In", "Sign Up"], default="Log In", selection_mode="single", width="stretch", label_visibility="hidden", required=True)

def render_signup_form():  
    left, center, right = st.columns([1,2,1])

    with center:
        with st.container(border=True):
            mode_buttons()

            st.title("Sign Up",text_alignment="center")
            st.divider()

            with st.form("signup_form"):
                mandatory, non_mandatory = st.columns(2)
                with mandatory:
                    st.success("Mandatory Fields")
                    name = st.text_input(label="Full Name", key="sighup name",  icon=":material/account_circle:")
                    passwd = st.text_input(label="Password", type="password", key="signup_password",  icon=":material/lock:")
                    check_passwd = st.text_input(label="Confirm Password", type="password",  icon=":material/lock:")
                with non_mandatory:
                    st.info("Non-Mandatory Fields")
                    age = st.number_input(label="Age",value=None, step=1)
                    gender = st.segmented_control(label="Gender", options=["Male ", "Female"], width="stretch")
                    land_area = st.number_input(label="Land area [Ha]", step=0.1, value=None)

                submit = st.form_submit_button("Sign-up", key="signup_button", width="stretch", type="primary",  icon=":material/upload:")
            
            if submit:
                if not name:
                    st.error("Please Provide your Full Name")

                elif not passwd or len(passwd) < 4:
                    st.error("Please provide a password greater than 4 characters")

                elif passwd != check_passwd:
                    st.error("Password Don't Match")

                elif all([name, passwd, check_passwd]):
                    user = create_user(
                        name = name,
                        passwd = passwd,
                        age = age,
                        gender = gender,
                        land_area = land_area)
                    
                    if user:
                        st.success("Sign Up Successful")
                        return user

                    else:
                        st.error("Something Went Wrong!")


def render_login_form():

    left, center, right = st.columns(3)
    with center:
        with st.container(border=True):
            mode_buttons()

            st.title("Log In",text_alignment="center")
            st.divider()

            with st.form("Login Form"):
                name = st.text_input(label="Full Name", key="login_name", icon=":material/account_circle:")
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
                        st.success("Login Successful")

                        return user
                    else:
                        st.error("Invalid Username or Password")


