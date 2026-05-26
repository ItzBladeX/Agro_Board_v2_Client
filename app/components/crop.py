import streamlit as st
from app.services import create_crop, update_crop, get_crop_types, del_crop, filter_crop
from app.models import Crop
from app.utils import formatted, order_years, set_button_size
import time
from app.constants import YEAR_LIST, FILTER_BY_OPTIONS
import pandas as pd
import altair as alt

@st.dialog("Crop Form", width = "large")
def render_crop_form(crop_types_dict, edit_crop = None, menu = False, view_mode = False):

    st.session_state.crop_menu
    if menu:
        st.session_state.crop_menu = False
        st.title("Crop Menu", text_alignment="center")
        edit_modes = st.segmented_control("Mode",options=["View Mode", "Edit Mode"], default = "View Mode", selection_mode="single", width = "stretch", label_visibility="hidden", required=True)

        view_mode = False if edit_modes == "Edit Mode" else True

        edit_id = edit_crop.id
        edit_user_id = edit_crop.user_id
        edit_name = list(crop_types_dict.keys()).index(edit_crop.name)
        edit_prod_year = (edit_crop.prod_start_year, edit_crop.prod_end_year) if edit_crop.prod_start_year != edit_crop.prod_end_year else edit_crop.prod_start_year
        edit_planted_date = edit_crop.planted_date
        edit_harvest_date = edit_crop.harvest_date
        edit_crop_yield = edit_crop.crop_yield
        edit_prod_cost = edit_crop.prod_cost
        edit_sell_price = edit_crop.sell_price
        edit_notes = edit_crop.notes

    else:
        st.title("Add Crop", text_alignment="center")
        edit_id = edit_name = edit_prod_year = edit_planted_date = edit_harvest_date = edit_crop_yield = edit_prod_cost = edit_sell_price = edit_notes = None

        edit_user_id = st.session_state.user
    
    left, right = st.columns([1,2])
    with left:
        

        with st.container(border=True):
            st.success("Mandatory Fields")
            with st.container(border=True):
                st.subheader("Crop", text_alignment="center")
                name = st.selectbox("Crop Name [Type] *", options=list(crop_types_dict.keys()), index =edit_name,placeholder="Choose your Crop Option", disabled=view_mode)
                prod_year = st.multiselect("Production Year *", options=YEAR_LIST, default = edit_prod_year,max_selections=2, placeholder = "Production year [Start] - [End]", disabled=view_mode)
                if prod_year and prod_year[0] > prod_year[-1]:
                    prod_start_year = prod_year[-1]
                    prod_end_year = prod_year[0]
                elif prod_year:
                    prod_start_year = prod_year[0]
                    prod_end_year = prod_year[-1]

        with st.container(border=True):
            st.image("app/assets/logo.png")

    with right:
        with st.container(border=True):
            st.info("Non Mandatory Fields")
            dates,eco = st.columns(2)
            with dates:
                with st.container(border=True):
                    st.subheader("Dates", text_alignment="center")
                    planted_date = st.date_input("Planted Date",value=edit_planted_date,help="if helf empty, will fill with current date",disabled=view_mode )
                    harvest_date = st.date_input("Harvest Date", value = edit_harvest_date,disabled=view_mode)

            with eco:
                with st.container(border=True):
                    st.subheader("Economics", text_alignment="center")
                    l,r = st.columns(2)
                    with l:
                        crop_yield = st.number_input("Crop Yield ", value =edit_crop_yield,step=0.1, min_value=0.0, disabled=view_mode)
                        prod_cost = st.number_input("Production Cost", value=edit_prod_cost,step=0.1, min_value=0.0, disabled=view_mode)
                        
                    with r:
                        sell_price =  st.number_input("Sold Price", value=edit_sell_price, step=0.1, min_value=0.0, disabled=view_mode)
                        p = sell_price-prod_cost if sell_price and prod_cost else None
                        profit =  st.number_input("Profit", value=p, step=0.1, disabled=True)

            with st.container(border=True):
                st.space(size="small")
                st.subheader("Notes", text_alignment="center")
                notes = st.text_area("Notes", max_chars=250,value=edit_notes, label_visibility = "hidden", height="stretch", disabled=view_mode)
                
    submit = False     
    if menu and not view_mode:
        left, right = st.columns([1,5])
        with left:
            with st.popover("Delete", width="stretch", icon=":material/delete_forever:"):
                check1 = st.toggle("I WANT TO DELETE THIS DATA PERMENANETLY")
                check2 = st.toggle("I UNDERSTAND THIS IS IRREVERSABLE")
                check3 = st.toggle("DETELE THIS DATA")

                delete_crop = st.button("DELETE", disabled=not all([check1, check2, check3]), width="stretch", icon=":material/delete_forever:")

                if delete_crop:
                    response = del_crop(edit_crop.id, edit_crop.user_id)
                    if response["status"]:
                        st.success("Successfully Deleted")
                        time.sleep(1)
                        st.rerun()

                    else:
                        st.error("Something Unexpected Happened")
                        st.write(response["error_code"])

        with right:
            submit = st.button("Save Crop", type="primary", width="stretch", icon=":material/save:")

    if not menu:
        submit = st.button("Save New Crop", type="primary", width="stretch", icon=":material/save:")
  
    if submit:
        if not all([name, prod_year]):
            st.error("Please Fill Every Mandatory Fields")

        else:
            crop = Crop(
                id = edit_id,
                user_id = edit_user_id,
                name = name,
                crop_type_id = crop_types_dict[name],
                prod_start_year = prod_start_year,
                prod_end_year = prod_end_year,
                planted_date = planted_date,
                harvest_date = harvest_date,
                crop_yield = crop_yield,
                prod_cost = prod_cost,
                sell_price = sell_price,
                profit = profit,
                notes = notes
            )

            if menu:
                response = update_crop(crop)
            else:
                response = create_crop(crop)

            if not response["status"]:
                print(response["error_code"])
                st.error("Unexpected Error")

            else:
                st.success("Crop Successfully Saved")

                time.sleep(1)
                st.rerun()
        

def render_crop_table(crops):

    
    set_button_size("crop_table", 56)
    column_1 = [1,2,2,2,2,2,2,1,1]
    with st.container(key="crop_table"):
        col1, col2,col3, col4, col5, col6, col7, col8,col9 = st.columns(column_1)

        with col1: st.button("No.", width="stretch")
        with col2: st.button("Name", width="stretch")
        with col3: st.button("Yield [KG]", width="stretch")
        with col4: st.button("Harvest Date", width="stretch")
        with col5: st.button("Production Cost", width="stretch")
        with col6: st.button("Sold Price", width="stretch")
        with col7: st.button("Profit", width="stretch")
        with col8: st.button("", width="stretch", key="crop_form", icon=":material/add:")
        with col9: st.button("", width="stretch", icon=":material/download_for_offline:")
        
        no = 1
        column_2 = [1,2,2,2,2,2,2,2]
        current_year = None
        
        for crop in crops:
            time.sleep(0.1)
            prod_year = (crop.prod_start_year, crop.prod_end_year)
            if prod_year != current_year:
                current_year = prod_year
                st.button(f"{formatted(current_year, is_year=True)}", key=f"order {crop.id}{current_year}",width="stretch")


            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(column_2)

            with col1: st.button(f"{no}.",width="stretch")
            with col2: st.success(crop.name, width="stretch")
            with col3: st.success(formatted(crop.crop_yield, is_yield=True))
            with col4: st.success(formatted(crop.harvest_date)) 
            with col5: st.error(formatted(crop.prod_cost, is_currency=True))
            with col6: st.info(formatted(crop.sell_price, is_currency=True))
            with col7: st.success(formatted(crop.profit, is_currency=True)) if crop.profit and crop.profit >=0  else st.error(formatted(crop.profit, is_currency=True))
            with col8: 
                if st.button("", key=f"{crop.id}", icon=":material/menu:", width="stretch"):
                    st.session_state.crop_menu = True
                    st.session_state.edit_crop = crop
                    st.rerun() # without this rerun, button takes 2 clicks to work
            no+=1

def render_crop_filter(crop_types_dict):
    try:
        with st.form(key="crop_filter_form", border=False):
            name = st.multiselect("Crop Name [Type]", options=crop_types_dict.keys(),placeholder="Filter by Name [Type]")
            year_mode = st.segmented_control("Production Year", options=["Select","Range"], selection_mode="single",default=["Select"],required=True, width="stretch")
            prod_year_range =  prod_year_list = None
            if year_mode == 'Range':
                prod_year_range = st.select_slider(" ", options=YEAR_LIST[::-1], value=(YEAR_LIST[0], YEAR_LIST[-1]),label_visibility="collapsed")
            else:
                prod_year_list = st.multiselect("Production Year", options=YEAR_LIST, max_selections=5, placeholder = "Production Years", label_visibility="collapsed")
        
            col = st.columns(2)

            with col[0]:
                min_profit =  st.number_input("Min Profit", value=None, step=0.1, placeholder="Min")
                min_crop_yield = st.number_input("Min Crop Yield ", value=None, step=0.1, min_value=0.0, placeholder="Min")

            with col[1]:
                max_profit =  st.number_input("Max Profit", value=None, step=0.1, placeholder="Max")
                max_crop_yield = st.number_input("Max Crop Yield ",value=None, step=0.1, min_value=0.0, placeholder="Max")

            sort = st.selectbox("Sort by", options=FILTER_BY_OPTIONS, index=0)
            reset = st.form_submit_button("Reset", width="stretch", icon=":material/filter_alt_off:")
            filter = st.form_submit_button("Filter", width="stretch", type="primary", icon=":material/filter_alt:", key="filter_button")
        
        data = None
        if filter:
            data = [
                name, 
                prod_year_list,
                prod_year_range, 
                (min_crop_yield, max_crop_yield),
                (min_profit, max_profit),
                sort,
            ]

       
        return {"status": True, "error_code":None, "data": data}
    except Exception as e:
        return {"status": False, "error_code":e, "data": None}
 
  
def render_crop_graph_card(crop):
    if not crop:
        st.error("No Crops")
    
    df = pd.DataFrame({
        "Metric": ["Prod", "Sold", "Yield", "Profit"],
        "Value" : [crop.prod_cost, crop.sell_price, crop.crop_yield, crop.profit],
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

def render_crop_profit_trend(crops, show_table = False):

    from collections import defaultdict
    if not crops:
        st.error("No Crops")
    profit_dict = defaultdict(float)
    table_dict = defaultdict(float)
    for crop in crops[::-1]:
        
        start_year = crop.prod_start_year
        end_year = crop.prod_end_year
        profit = crop.profit
        if start_year == end_year and profit:
            profit_dict[start_year] += profit
            table_dict[f"{start_year}"] += profit
        elif profit:
            table_dict[f"{start_year} - {end_year}"]
            profit_dict[(start_year + end_year)/2] += profit
    
    label_dates = list(set([crop.prod_start_year for crop in crops]))[::-1]
    graph_df = pd.DataFrame({
        "Date"   : profit_dict.keys(),
        "Profit" :profit_dict.values(),
    })
    table_df = pd.DataFrame({
        "Date"   : table_dict.keys(),
        "Profit" :table_dict.values(),
    })
    area_gf = alt.Chart(graph_df).mark_area(color="#86f3b3ff", opacity=0.4).encode(
            x=alt.X("Date:O", axis=alt.Axis(title=None, labels=True, ticks=False, grid=True, values = label_dates),sort=None),
            y=alt.Y("Profit:Q", axis=alt.Axis(title=None, labels=True, ticks=False, grid=True)),
        )   

    gf_line = alt.Chart(graph_df).mark_line(color="#2fa342ff", point=True).encode(
        x=alt.X("Date:O", axis=alt.Axis(title=None, labels=True, ticks=False, grid=True, values=label_dates),sort=None),
        y=alt.Y("Profit:Q", axis=alt.Axis(title=None, labels=True, ticks=False, grid=True)),
        
    )
    gf = area_gf + gf_line
    
    if show_table:
        col = st.columns(2)
        with col[0]:
            st.altair_chart(gf, height=300, width="stretch")
        with col[1]: 
            st.table(table_df, height=300, width="stretch")
    else:
        st.altair_chart(gf, height=300 )