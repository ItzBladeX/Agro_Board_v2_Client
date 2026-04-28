import streamlit as st
import streamlit_option_menu as om



def render_navbar(pages):
    page_list = list(pages.keys())
    
    om.option_menu(
        menu_title=None,
        options=page_list, 
        icons=["house", "bar-chart", "bar-chart", "bar-chart","bar-chart"],
        default_index=page_list.index(st.session_state.page),
        orientation="horizontal",
        key = "page",
        styles={"nav-link": 
                {"text-align": "center", "margin": "0em", "--hover-color": "#676767"},
            }
        )
