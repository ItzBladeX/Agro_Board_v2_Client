
import streamlit as st
from app.utils import set_button_size, formatted
import time

def cols(col_type):
    
    column_1 = [1,2,2,2,2,2,2,1,1]
    col = st.columns(column_1)

    with col[0]: st.button("No.", width="stretch")
    with col[1]: st.button("Name", width="stretch")
    if col_type == "crop":
        with col[2]: st.button("Yield", width="stretch")
        with col[3]: st.button("Harvest Date", width="stretch")
    elif col_type == "livestock":
        with col[2]: st.button("Amount", width="stretch")
        with col[3]: st.button("Import Date", width="stretch")

    with col[4]: st.button("Cost", width="stretch")
    with col[5]: st.button("Revenue", width="stretch")
    with col[6]: st.button("Profit", width="stretch")
    with col[7]: st.button("", width="stretch", key=f"{col_type}_form", icon=":material/add:")
    with col[8]: st.button("", width="stretch", icon=":material/download_for_offline:")


def rows(item, no, row_type):
    column_2 = [1,2,2,2,2,2,2,2]
    col = st.columns(column_2)
    with col[0]: st.button(f"{no}.",width="stretch")
    if row_type == "crop":
        
        with col[1]: st.success(item.name, width="stretch")
        with col[2]: st.success(formatted(item.crop_yield, is_yield=True))
        with col[3]: st.success(formatted(item.harvest_date)) 
        with col[4]: st.error(formatted(item.prod_cost, is_currency=True))
        with col[5]: st.info(formatted(item.revenue, is_currency=True))


    elif row_type == "livestock":
    
        with col[1]: st.info(item.name, width="stretch")
        with col[2]: st.info(formatted(item.crop_yield, is_yield=True))
        with col[3]: st.info(formatted(item.harvest_date)) 
        with col[4]: st.error(formatted(item.prod_cost, is_currency=True))
        with col[6]: st.info(formatted(item.revenue, is_currency=True))

    with col[6]: 
        if item.profit and item.profit >=0: st.success(formatted(item.profit, is_currency=True))
        else: st.error(formatted(item.profit, is_currency=True))

    with col[7]: 
        if st.button("", key=f"{item.id}", icon=":material/menu:", width="stretch"):
            st.session_state.table_menu = True
            st.session_state.edit_item = item
            st.rerun() # without this rerun, button takes 2 clicks to work


def render_table(data, table_type):
        if not data:
            st.error("No Data to Display")
            return
        set_button_size("crop_table", 56)
        with st.container(key="crop_table"):
            cols(table_type)
            no = 1
            current_year = None
            for item in data:
                time.sleep(0.1)
                prod_year = (item.prod_start_year, item.prod_end_year)
                if prod_year != current_year: # arrange similar prod years together
                    current_year = prod_year
                    st.button(f"{formatted(current_year, is_year=True)}", key=f"order {item.id}{current_year}",width="stretch")
                rows(item, no, table_type)

                no+=1