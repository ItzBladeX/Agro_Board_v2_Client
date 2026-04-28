import streamlit as st
from app.services import get_user_by_id, update_user
import time




def render_profile():

    user = get_user_by_id(st.session_state.user)
    
    with st.container(border=True):

        st.title(f"👤 Profile [{user.id}]", text_alignment="center")
        st.divider()

        view_mode(user)

    if st.button("Log out", type="primary", width="stretch",  icon=":material/logout:"):
        st.session_state.user = None
        st.rerun()

def view_mode(user):
    st.write(f"**Name**: {user.name}")
    st.write(f"**Age:** {"  --  " if not user.age else user.age}")
    st.write(f"**Gender:** { "--" if not user.gender else user.gender}") 
    st.write(f"**Land Area:** {"  --  " if not user.land_area else f"{user.land_area} Ha"}" )
    st.button("Edit", icon=":material/edit:", on_click=edit_mode, args=(user,),width="stretch")

@st.dialog("Edit Profile", width="medium")
def edit_mode(user):
    with st.form("edit_user"):
        st.title(f"👤 Profile [{user.id}]", text_alignment="center")
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Name", value=user.name, icon="👤")
            new_age = st.number_input("Age [Optional]", value = user.age, step=1)
            new_gender = st.radio("Gender",options=[None, "Male", "Female"], index=[None, "Male", "Female"].index(user.gender), horizontal=True) 
        
        with col2:
            new_land_area = st.number_input("Land Area [Optional] [Ha]", value=user.land_area, step=0.1)
            passwd = st.text_input("Current Password", type="password", icon=":material/lock:")
            st.space(10)
            with st.popover("Set New Password", width="stretch", icon=":material/lock:"):
                new_passwd = st.text_input("New Password", type="password",  icon=":material/lock:")
        cancel = st.form_submit_button("Cancel", type="secondary",width="stretch" )
        save = st.form_submit_button("Save", type="primary", width="stretch",  icon=":material/edit:")

    if cancel:
        st.rerun()

    if save:

        if not all([new_name, passwd]):
            st.error("Please Fill in every Box")

        elif passwd != user.passwd:
            st.error("Password Incorrect!")

        else:

            status = update_user(
                id=user.id,
                name=new_name, 
                age=new_age,
                gender = new_gender,
                land_area=new_land_area,
                passwd=new_passwd,
                )
            
            if status:

                st.success("Successfully Saved")
                time.sleep(2)
                st.rerun()

            else:

                st.error("Something Went Wrong")