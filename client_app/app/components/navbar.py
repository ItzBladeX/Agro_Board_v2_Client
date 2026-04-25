import streamlit as st
import streamlit_option_menu as om



def render_navbar(current_page, width, pages):
    page_list = list(pages.keys())
    
    selected = om.option_menu(
            menu_title=None,
            options=page_list, 
            icons=["house", "bar-chart", "bar-chart", "bar-chart","bar-chart"],
            default_index=page_list.index(current_page),
            orientation="horizontal",
            styles={"nav-link": 
                    {"text-align": "center", "margin": "0em", "--hover-color": "#676767"},
                }
        )
    # if selected is None:
    #     return current_page
    return selected
    # st.session_state["page"] = selected   
    # if selected != current_page:
    #     st.switch_page(pages[selected])