import streamlit as st
from app.constants import GENDER_OPTIONS

def render_profile(user): 
    st.title(f"👤 Profile [{user.id}]", text_alignment="center")
    st.divider()

    st.text_input("**Name**", value=user.name, disabled=True)
    st.text_input("**Age:**", value= user.age, disabled=True)
    # st.text_input("**Gender:**", value=user.gender, disabled=True)
    st.segmented_control("Gender [Optional]",options=GENDER_OPTIONS, default=user.gender,selection_mode="single", width="stretch", disabled=True)
    st.text_input("**Land Area:**", value=user.land_area, disabled=True)


    

