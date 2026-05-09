import streamlit as st
import time
from app.services import update_user, link_to_server, reset_password, delete_user


@st.dialog("Settings", width="medium")
def render_settings(user):
    st.title(f"👤 Profile [{user.id}]", text_alignment="center")
    st.divider()
    with st.expander("My Account", icon=":material/account_circle:"):
        user_setting(user)
        
    with st.expander("Security", icon=":material/security:"):
        with st.expander("Reset Password", icon=":material/change_circle:"):
            reset_passwd(user)
        with st.expander("Account Deletion", icon=":material/delete_forever:"):
            del_user(user)

    with st.expander("Server Setting", icon=":material/storage:"):
        server_settings(user)
    
    if st.button("Close", type="secondary",width="stretch" , icon=":material/close:"):
        st.rerun()

def user_setting(user):
    st.subheader("User Information", text_alignment = "center")
    col1, col2 = st.columns(2)
    with col1:
        new_name = st.text_input("Name", value=user.name, icon=":material/account_circle:")
        new_age = st.number_input("Age [Optional]", value = user.age, step=1)
    with col2:
        new_land_area = st.number_input("Land Area [Optional] [Ha]", value=user.land_area, step=0.1)
        new_gender = st.segmented_control("Gender [Optional]",options=["Male", "Female"], default=user.gender,selection_mode="single", width="stretch") 
    if st.button("Save", type="primary", width="stretch", icon=":material/save:"):

        if not new_name:
            st.error("Name can't be empty")

        else:
            status = update_user(
                id=user.id,
                name=new_name, 
                age=new_age,
                gender = new_gender,
                land_area=new_land_area,
                )
            
            if status:
                st.success("Successfully Saved")
                time.sleep(2)

            else:
                st.error("Something Went Wrong")

def reset_passwd(user):
    st.subheader("Reset Password", text_alignment = "center")
    col1, col2 = st.columns(2)
    with col1:
        passwd = st.text_input("Current Password", type="password", icon = ":material/lock:")

    with col2:
        new_passwd = st.text_input("New Password", type="password",  icon =":material/lock:")

    if st.button("Reset", type="primary", width="stretch",  icon=":material/save:"):
        if passwd != user.passwd:
            st.error("Incorrect Password")

        elif not new_passwd:
            st.error("New password cant be empty")

        elif new_passwd == user.passwd:
            st.error("New password cant be the same as previous")

        else:
            status = reset_password(user.id,passwd, new_passwd)
            if status:
                st.success("Password Reset Successful")
            else:
                st.error("Something Went Wrong!")

def del_user(user):
    st.subheader("Delete Account", text_alignment="center")
    col1, col2 = st.columns(2)
    with col1:
        passwd = st.text_input("Please Enter Password", type = "password", icon = ":material/lock:")
    with col2: 
        confirm_passwd = st.text_input("Please Confirm Password", type = "password", icon = ":material/lock:")
    confirm1 = st.toggle("I WANT TO DELETE MY ACCOUNT")
    confirm2 = st.toggle(" I UNDERSTAND THIS ACTION IS IRREVERSABLE")
    confirm3 = st.toggle("DELETE ALL MY DATA AND INFORMATION")

    if all([passwd, confirm_passwd, confirm1, confirm1, confirm3]) and passwd == confirm_passwd:
        if st.button("Delete", width="stretch", icon=":material/delete_forever:"):
            if passwd != user.passwd :
                st.error("Incorrect Password!")
            else:
                status = delete_user(user.id, passwd, confirm_passwd)
                if status:
                    st.success("Account deleted Successfully !")
                    time.sleep(3)
                    st.session_state.user = None
                    st.rerun()

def server_settings(user):
    st.subheader("Server Settings", text_alignment = "center")
    col1, col2 = st.columns(2)
    with col1:
        server_id = st.text_input("Server ID", icon=":material/host:")
    with col2:
        server_passwd = st.text_input("Server Password", type="password", icon=":material/lock:")
    st.text_input("User ID", value=user.user_id, disabled=True, icon=":material/id_card:")

    if st.button("Link To Server", type="primary", width="stretch", icon=":material/cloud:"):
        link_to_server(user, server_id = server_id, server_passwd = server_passwd)
