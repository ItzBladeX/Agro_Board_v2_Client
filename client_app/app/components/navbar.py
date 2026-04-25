import streamlit as st
import streamlit_option_menu as om

from app.pages.about import about_page
from app.pages.crop import crop_page
from app.pages.inventory import inventory_page
from app.pages.liveStock import livestock_page
from app.pages.home import home_page

def render_navbar(current_page, width, pages):
    
    page_list = list(pages.keys())
    if width >= 1000:
        selected = om.option_menu(
                menu_title=None,
                options=page_list, 
                icons=["house", "bar-chart", "bar-chart", "bar-chart","bar-chart" ],
                default_index=page_list.index(current_page),
                orientation="horizontal",
                styles={"nav-link": {"text-align": "center", "margin": "0em", "--hover-color": "#676767"},
                
            }
         )
    # st.session_state["page"] = selected   
    # if selected != current_page:
    #     st.switch_page(pages[selected])