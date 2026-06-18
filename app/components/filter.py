import streamlit as st

from app.utils import formatted
from app.constants import YEAR_LIST, FILTER_BY_OPTIONS_1, FILTER_BY_OPTION_2


def render_filter(crop_types_dict, filter_type, mode=False ):
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
                min_crop_yield = max_crop_yield = min_livestock_amount =  max_livestock_amount = None
                min_profit =  st.number_input("Min Profit", value=None, step=0.1, placeholder="Min", disabled=disable_profit)
                if filter_type == 'crop':
                    min_crop_yield = st.number_input("Min Crop Yield ", value=None, step=0.1, min_value=0.0, placeholder="Min", disabled=disable_yield)
                if filter_type == "livestock":
                    min_livestock_amount = st.number_input("Min Crop Yield ", value=None, step=0.1, min_value=0.0, placeholder="Min", disabled=disable_yield)

            with col[1]:
                max_profit =  st.number_input("Max Profit", value=None, step=0.1, placeholder="Max", disabled=disable_profit)
                if filter_type == 'crop':
                    max_crop_yield = st.number_input("Max Crop Yield ",value=None, step=0.1, min_value=0.0, placeholder="Max", disabled=disable_yield)
                if filter_type == "livestock":
                    max_livestock_amount = st.number_input("Max Crop Yield ",value=None, step=0.1, min_value=0.0, placeholder="Max", disabled=disable_yield)

            if filter_type == "crop":
                sort = st.selectbox("Sort by", options=FILTER_BY_OPTIONS_1, index=0, disabled=disable_sort)
            elif filter_type == "livestock":
                    sort = st.selectbox("Sort by", options=FILTER_BY_OPTION_2, index=0, disabled=disable_sort)

            st.form_submit_button("Reset", width="stretch", icon=":material/filter_alt_off:", disabled=disable_reset)
            filter = st.form_submit_button("Filter", width="stretch", type="primary", icon=":material/filter_alt:", key="filter_button", disabled=disable_filter)
        
        filter_parameters = None
        if filter:
            filter_parameters = [
                name, 
                prod_year_list,
                prod_year_range, 
                (min_crop_yield, max_crop_yield),
                (min_livestock_amount, max_livestock_amount),
                (min_profit, max_profit),
                sort,
            ]

        return {"status": True, "error_code":None, "data": filter_parameters}
    except Exception as e:
        return {"status": False, "error_code":e, "data": None}
 