import streamlit as st


#TODO: Make setting is own component
def render_profile(user): 
    st.title(f"👤 Profile [{user.id}]", text_alignment="center")
    st.divider()

    st.write(f"**Name**: {user.name}")
    st.write(f"**Age:** {"  --  " if not user.age else user.age}")
    st.write(f"**Gender:** { "--" if not user.gender else user.gender}") 
    st.write(f"**Land Area:** {"  --  " if not user.land_area else f"{user.land_area} Ha"}" )
    

