import streamlit as st
from app.services import get_crop_types, filter_crop
from app.components import render_table, render_form, render_crop_filter, render_crop_graph_card, render_profit_trend, render_yield_trend, render_cost_revenue_trend
from app.constants import STREAMLIT

def crop_view():
    mode = load_nav() # return selected nav option
    crop_types = load_crop_types() # return dict of crop types : growth rate

    crops = load_sidebar(crop_types, mode) # return filtered crop from sidebar filter [Mode used to disable/enable parts of the filter according to content displayed]

   
    
    if mode == "Table":
        render_table(crops, table_type="crop")
        load_crop_form(crop_types) # responsable for add crop form and edit crop form based on session state
        
    elif mode == "Graph":
        load_crop_graph_card(crops)
    
    elif mode == "Trend":
        load_crop_profit_trend(crops)
        load_crop_cost_revenue_trend(crops)
        load_crop_yield_trend(crops) 



def load_nav():
    return st.segmented_control(" ", options=["Table", "Graph", "Trend"], default="Table", width="stretch", selection_mode="single", required=True)

def load_sidebar(crop_types, mode):
    with st.sidebar:
        filtered_crops = load_crop_filter(crop_types, mode) # Mode to disaple/enable form parts
        st.link_button("Powered by Streamlit :streamlit:", type="tertiary", width="stretch", url=STREAMLIT)
        return filtered_crops
    
def load_crop_types():
    crop_type_response = get_crop_types()
    if crop_type_response["status"]: 
        return crop_type_response["data"]
    else:
        st.error("Unable to get crop types")
        print(crop_type_response["error_code"])

def load_crop_graph_card(crops):
    col = st.columns(4)
    curr_col = 0
    if not crops:
        st.error("No Crops")
    for crop in crops:
        with col[curr_col]:
            render_crop_graph_card(crop)
            if curr_col < 3 : curr_col += 1
            else: curr_col = 0
def load_crop_profit_trend(crops):
    
    with st.container(border=True):
        st.title("Profit Trend", text_alignment="center")
        st.divider()        
        render_profit_trend(crops, show_table=True, trend_type="crop")

def load_crop_yield_trend(crops):   
    with st.container(border=True):
        st.title("Yield Trend", text_alignment="center")
        st.divider()
        render_yield_trend(crops, show_table = True, trend_type="crop")
      
def load_crop_cost_revenue_trend(crops):
    with st.container(border=True):
        st.title("Cost vs Revenue", text_alignment="center")
        st.divider()
        render_cost_revenue_trend(crops, show_table = True, trend_type="crop")

def load_crop_filter(crop_types, mode):
    
    st.title("Crop Filter", text_alignment="center")
    st.divider()

    # mode used to disable/enable filter fields
    # filter_type to identify what data to filter crop/livestock...
    filter_response = render_crop_filter(crop_types, filter_type="crop", mode=mode) 
    if filter_response["error_code"]:
        print("Filter Error [Component]: ", filter_response["error_code"], filter_response["status"]) 
        return None
    
    elif filter_response["status"]:

        if filter_response["data"]:
            st.success("Filter: ON")
            filtered_crop = filter_crop(st.session_state.user, *filter_response["data"])

        else:
            st.error("Filter: OFF")
            filtered_crop = filter_crop(st.session_state.user, sort="Production Year")

        if not filtered_crop["status"]:
            st.error("Filter Unavailable")
            print("Filter Error [Service]", filtered_crop["error_code"])
            return None
    
        return filtered_crop["data"] 
    
def load_crop_form(crop_type_dict):
    if "table_menu" not in st.session_state: 
        st.session_state.table_menu = False
 
    if st.session_state.get("crop_form", False):
        render_form(crop_type_dict, menu = False, form_type="crop")

    elif st.session_state.get("table_menu", False):
        render_form(crop_type_dict, edit_item = st.session_state.edit_item, menu=True, form_type="crop")
        
def load_crop_table(filtered_crops):
    
    render_table(filtered_crops, table_type="crop")
    
