import streamlit as st
from app.services import create_crop, update_crop, get_crop_types, del_crop, filter_crop
from app.models import Crop
from app.utils import formatted, order_years, set_button_size
import time
from app.constants import YEAR_LIST, FILTER_BY_OPTIONS
import pandas as pd
import altair as alt
from collections import defaultdict

def render_crop_filter(crop_types_dict, filter_type, mode=False ):
    if mode == "Trend":
        disable_name = False
        disable_prod_year_range = True
        disable_prod_year_list = True
        disable_year_mode = True
        disable_profit =True
        disable_yield = True
        disable_sort = True
        disable_reset = False
        disable_filter = False
    
    else:
        disable_name = disable_prod_year_range = disable_prod_year_list = disable_year_mode = disable_profit = disable_yield = disable_sort = disable_reset = disable_filter = False

    try:
        with st.form(key=f"{filter_type}_filter_form", border=False):
            name = st.multiselect(f"{filter_type.title()} Name [Type]", options=crop_types_dict.keys(),placeholder="Filter by Name [Type]", disabled=disable_name)
            year_mode = st.segmented_control("Production Year", options=["Select","Range"], selection_mode="single",default="Select",required=True, width="stretch", disabled=disable_year_mode)
            prod_year_range =  prod_year_list = None
            if year_mode == 'Range':
                prod_year_range = st.select_slider(" ", options=YEAR_LIST[::-1], value=(YEAR_LIST[0], YEAR_LIST[-1]),label_visibility="collapsed", disabled=disable_prod_year_range)
            else:
                prod_year_list = st.multiselect("Production Year", options=YEAR_LIST, max_selections=5, placeholder = "Production Years", label_visibility="collapsed", disabled=disable_prod_year_list)
        
            col = st.columns(2)
            with col[0]:
                min_profit =  st.number_input("Min Profit", value=None, step=0.1, placeholder="Min", disabled=disable_profit)
                min_crop_yield = st.number_input("Min Crop Yield ", value=None, step=0.1, min_value=0.0, placeholder="Min", disabled=disable_yield)

            with col[1]:
                max_profit =  st.number_input("Max Profit", value=None, step=0.1, placeholder="Max", disabled=disable_profit)
                max_crop_yield = st.number_input("Max Crop Yield ",value=None, step=0.1, min_value=0.0, placeholder="Max", disabled=disable_yield)

            sort = st.selectbox("Sort by", options=FILTER_BY_OPTIONS, index=0, disabled=disable_sort)
            st.form_submit_button("Reset", width="stretch", icon=":material/filter_alt_off:", disabled=disable_reset)
            filter = st.form_submit_button("Filter", width="stretch", type="primary", icon=":material/filter_alt:", key="filter_button", disabled=disable_filter)
        
        filter_parameters = None
        if filter:
            filter_parameters = [
                name, 
                prod_year_list,
                prod_year_range, 
                (min_crop_yield, max_crop_yield),
                (min_profit, max_profit),
                sort,
            ]

        return {"status": True, "error_code":None, "data": filter_parameters}
    except Exception as e:
        return {"status": False, "error_code":e, "data": None}
 
  
def render_crop_graph_card(crop):
    if not crop:
        st.error("No Crops")
    
    df = pd.DataFrame({
        "Metric": ["Cost", "Revenue", "Yield", "Profit"],
        "Value" : [crop.prod_cost, crop.revenue, crop.crop_yield, crop.profit],
        "colors": ["#e74c3c","#3498db","#f1c40f", "#2ecc71"]
    })
    gf = alt.Chart(df).mark_bar().encode(

    x=alt.X("Metric:N", axis=alt.Axis(title=None, labels=True, ticks=False, grid=True), sort=None),
    y=alt.Y("Value:Q", axis=alt.Axis(title=None, labels=True, ticks=False, grid=True)),
    color = alt.Color("colors:N", scale=None)
    ).properties(
    width=200,
    height=200,
    )
    prod_start_year = crop.prod_start_year
    prod_end_year = crop.prod_end_year
    planted_date = formatted(crop.planted_date) if crop.planted_date else "Unknown"
    harvest_date = formatted(crop.harvest_date) if crop.harvest_date else "Unknown"
    with st.container(border=True):
        col = st.columns(2)
        with col[0]:
            st.button(f"**{crop.name}**", type="secondary", width="stretch", key=f"card {crop.name} {crop.id} ")
        with col[1]:
            if prod_start_year != prod_end_year:
                st.button(f"**{prod_start_year}/{prod_end_year}**", type="secondary", width="stretch", key=f"{crop.id}{crop.prod_start_year}{crop.prod_end_year}")
            else:
                st.button(f"**{prod_start_year}**", type="secondary", width="stretch", key=f"{crop.id}{crop.prod_start_year}{crop.prod_end_year}")
        graph = st.empty()
        space = st.empty()
        space.button(f"**{planted_date} -- {harvest_date}**", type="tertiary",width="stretch", key=f"{crop.id}{crop.planted_date}{crop.harvest_date}")
        
        graph.altair_chart(gf)# height and width not specified for the smooth left to right auto adjestment animation
        time.sleep(0.1) # Animation effect and prevent flicker





