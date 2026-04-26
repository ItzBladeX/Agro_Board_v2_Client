import streamlit as st
from components import render_weather_matrix
from services import get_weather
def home_view():
    with st.container():
        data = get_weather()    
        render_weather_matrix(data)
        st.divider()
    
    

   
    # with shelve.open("config") as db:
    #     try:
    #         SN = db["SN"]
    #         name = db["name"]
    #     except KeyError:
    #         func.configuration()
    # # Widgets

    # st.markdown("""

    # <h2 style="color: #013014ff; text-align: center; font-family: Arial, sans-serif;"> Statistics and Data </h2>


    # """, unsafe_allow_html=True)
    # # Crop
    # with st.expander("Crop Data"):
    #     st.markdown("""<h3 style="color: #013014ff; text-align: center; font-family: Arial, sans-serif;"> Crops </h3>""", unsafe_allow_html=True)
    #     st.divider()
    #     func.display_graph(database=crop_db, filter_on=True) # yr - years user selected
            
        
    #     # Livestock

    # with st.expander("LiveStock Data"):
    #     st.markdown("""<h3 style=" color: #013014ff; text-align: center; font-family: Arial, sans-serif;"> LiveStocks </h3>""", unsafe_allow_html=True)
    #     func.display_graph(livestock_db, filter_on=True)
    # for _ in range(3):
    #     st.write("")


    # with st.container(border=True):
    #     st.markdown("""<h3 style=" color: #013014ff; text-align: center; font-family: Arial, sans-serif;"> Setting </h3>""", unsafe_allow_html=True)
    #     col1, col2 = st.columns(2)
    #     with col1:

    #         with shelve.open('config') as db:
    #             st.button(" ⬆️ Upload Data", on_click=func.package_data, width="stretch", disabled=func.check_sn(), type="secondary")
    #     with col2:

    #         with shelve.open('config') as db:
    #             st.button("⚙️ Edit Personal / Config /  Data", on_click=func.edit_config, width="stretch", disabled=func.check_sn(), type="secondary")


