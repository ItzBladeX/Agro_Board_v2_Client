import streamlit as st
from app.services import filter_data, get_livestock_types
from app.components import render_table, render_table_form, render_filter, render_profit_trend, render_amount_trend, render_cost_revenue_trend, render_graph_card
from app.constants import STREAMLIT
from app.models import Livestock

def livestock_view():
    
    mode = load_nav() # return selected nav option
    livestock_types = load_livestock_types() # return dict of livestock types : growth rate

    livestock = load_sidebar(livestock_types, mode) # return filtered livestock from sidebar filter_data [Mode used to disable/enable parts of the filter_data according to content displayed]
  
    if mode == "Table":
        render_table(livestock, table_type="livestock")
        load_form(livestock_types) # responsable for add livestock form and edit livestock form based on session state
        
    elif mode == "Graph":
        load_graph_card(livestock)
    
    elif mode == "Trend":
        load_profit_trend(livestock)
        load_cost_revenue_trend(livestock)
        load_amount_trend(livestock) 

def load_nav():
    return st.segmented_control("Livestock Nav Bar", options=["Table", "Graph", "Trend"], default="Table", width="stretch", selection_mode="single", required=True, label_visibility="hidden")

def load_sidebar(crop_types, mode):
    with st.sidebar:
        filtered_crops = load_filter(crop_types, mode) # Mode to disaple/enable form parts
        st.link_button("Powered by Streamlit :streamlit:", type="tertiary", width="stretch", url=STREAMLIT)
        return filtered_crops
    
def load_livestock_types():
    crop_type_response = get_livestock_types()
    if crop_type_response["status"]: 
        return crop_type_response["data"]
    else:
        st.error("Unable to get livestock types")
        print(crop_type_response["error_code"])

def load_graph_card(livestocks):
    col = st.columns(4)
    curr_col = 0
    if not livestocks:
        st.error("No Livestock To Display")
    for livestock in livestocks:
        with col[curr_col]:
            render_graph_card(livestock, graph_type="livestock")
            if curr_col < 3 : curr_col += 1
            else: curr_col = 0
def load_profit_trend(crops):
    
    with st.container(border=True):
        st.title("Profit Trend", text_alignment="center")
        st.divider()        
        render_profit_trend(crops, show_table=True, trend_type="livestock")

def load_amount_trend(crops):   
    with st.container(border=True):
        st.title("Yield Trend", text_alignment="center")
        st.divider()
        render_amount_trend(crops, show_table = True)
      
def load_cost_revenue_trend(crops):
    with st.container(border=True):
        st.title("Cost vs Revenue", text_alignment="center")
        st.divider()
        render_cost_revenue_trend(crops, show_table = True, trend_type="livestock")

def load_filter(crop_types, mode):
    
    st.title("Livestock Filter", text_alignment="center")
    st.divider()

    # mode used to disable/enable filter_data fields
    # filter_type to identify what data to filter_data livestock/livestock...
    filter_response = render_filter(crop_types, filter_type="livestock", mode=mode) 
    if filter_response["error_code"]:
        print("Filter Error [Component]: ", filter_response["error_code"], filter_response["status"]) 
        return None
    
    elif filter_response["status"]:

        if filter_response["data"]:
            st.success("Filter: ON")
            filtered_crop = filter_data(Livestock, st.session_state.user, *filter_response["data"])

        else:
            st.error("Filter: OFF")
            filtered_crop = filter_data(Livestock, st.session_state.user, sort="Production Year")

        if not filtered_crop["status"]:
            st.error("Filter Unavailable")
            print("Filter Error [Service]", filtered_crop["error_code"])
            return None
    
        return filtered_crop["data"] 
    
def load_form(crop_type_dict):
    if "table_menu" not in st.session_state: 
        st.session_state.table_menu = False
 
    if st.session_state.get("livestock_form", False):
        render_table_form(crop_type_dict, menu = False, form_type="livestock")

    elif st.session_state.get("table_menu", False):
        render_table_form(crop_type_dict, edit_item = st.session_state.edit_item, menu=True, form_type="livestock")
        
def load_table(filtered_crops):
    render_table(filtered_crops, table_type="livestock")
    
