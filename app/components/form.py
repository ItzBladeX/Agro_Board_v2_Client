import streamlit as st
from constants import TABLE_MENU_OPTIONS, YEAR_LIST
import time
from app.services import del_crop, update_crop, create_crop
from app.services import del_livestock, update_livestock, create_livestock
from app.models import Crop, Livestock

# def menu(edit_item,{form_name} data_types_dict):
#     st.session_state.table_menu = False


# def left(data_types_dict, edit_name, view_mode, edit_prod_year, menu_type):
#     with st.container(border=True):
#         st.success("Mandatory Fields")
#         with st.container(border=True):
#             st.subheader("Crop", text_alignment="center")
#             name = st.selectbox("Crop Name [Type] *", options=list(data_types_dict.keys()), index =edit_name,placeholder="Choose your Crop Option", disabled=view_mode)
#             prod_year = st.multiselect("Production Year *", options=YEAR_LIST, default = edit_prod_year,max_selections=2, placeholder = "Production year [Start] - [End]", disabled=view_mode)
#             if prod_year and prod_year[0] > prod_year[-1]:
#                 prod_start_year = prod_year[-1]
#                 prod_end_year = prod_year[0]
#             elif prod_year:
#                 prod_start_year = prod_year[0]
#                 prod_end_year = prod_year[-1]

#         with st.container(border=True):
#             st.image("app/assets/logo.png")

#     return name, prod_year, prod_start_year, prod_end_year



# def right(edit_start_date, edit_end_date,edit_revenue,edit_prod_cost, edit_amount,edit_notes, view_mode,{form_name}:
#     with st.container(border=True):
#             st.info("Non Mandatory Fields")
#             dates,eco = st.columns(2)
#             with dates:
#                 with st.container(border=True):
#                     st.subheader("Dates", text_alignment="center")
#                     if{form_name}== "crop":
#                         start_date = st.date_input("Planted Date",value=edit_start_date,help="if helf empty, will fill with current date",disabled=view_mode )
#                         end_date = st.date_input("Harvest Date", value = edit_end_date,disabled=view_mode)
#                     elif{form_name}== "livestock":
#                         pass

#             with eco:
#                 with st.container(border=True):
#                     st.subheader("Economics", text_alignment="center")
#                     l,r = st.columns(2)
#                     with l:
#                         if{form_name}== "crop":
#                             amount = st.number_input("Crop Yield ", value =edit_amount,step=0.1, min_value=0.0, disabled=view_mode)
#                         prod_cost = st.number_input("Production Cost", value=edit_prod_cost,step=0.1, min_value=0.0, disabled=view_mode)
                        
#                     with r:
#                         revenue =  st.number_input("Revenue", value=edit_revenue, step=0.1, min_value=0.0, disabled=view_mode)
#                         p = revenue-prod_cost if revenue and prod_cost else None
#                         profit =  st.number_input("Profit", value=p, step=0.1, disabled=True)

#             with st.container(border=True):
#                 st.space(size="small")
#                 st.subheader("Notes", text_alignment="center")
#                 notes = st.text_area("Notes", max_chars=250,value=edit_notes, label_visibility = "hidden", height="stretch", disabled=view_mode)

#     return start_date, end_date, amount, prod_cost, revenue, profit, revenue, notes


# @st.dialog("Table Form", width = "large")
# def render_form(data_types_dict{form_name} edit_item = None, menu = False, view_mode = False,):

#     if menu:
#         st.title(f"{form_name}title()} Menu", text_alignment="center")
#         edit_modes = st.segmented_control("Mode",options=TABLE_MENU_OPTIONS, default = "View Mode", selection_mode="single", width = "stretch", label_visibility="hidden", required=True)

#         view_mode = False if edit_modes == "Edit Mode" else True
#         edit_id = edit_item.id
#         edit_user_id = edit_item.user_id
#         edit_name = list(data_types_dict.keys()).index(edit_item.name)
#         edit_prod_year = (edit_item.prod_start_year, edit_item.prod_end_year) if edit_item.prod_start_year != edit_item.prod_end_year else edit_item.prod_start_year
#         if{form_name}== "crop":
#             edit_planted_date = edit_item.planted_date
#             edit_harvest_date = edit_item.harvest_date
#             edit_crop_yield = edit_item.crop_yield
#         elif{form_name}== "livestock":
#             edit_prod_cost = edit_item.prod_cost
#             edit_revenue = edit_item.revenue
#             edit_notes = edit_item.notes

#     else:
#         st.title("Add Crop", text_alignment="center")
#         edit_id = edit_name = edit_prod_year = edit_planted_date = edit_harvest_date = edit_crop_yield = edit_prod_cost = edit_revenue = edit_notes = None

#         edit_user_id = st.session_state.user
    
#     left_side, right_side = st.columns([1,2])
#     with left_side:
#         name, prod_start_year, prod_end_year = left(data_types_dict,edit_name,view_mode,edit_prod_year)

#     with right_side:
#         if{form_name}== "crop":
#             planted_date, harvest_date,prod_year, crop_yield, prod_cost, revenue, profit, revenue,notes = right(edit_planted_date, edit_harvest_date,edit_revenue,edit_prod_cost, edit_notes, view_mode,{form_name}
#         elif{form_name}== "livestock":
#             pass
#             start_date, end_date, amount, prod_cost, revenue, profit, revenue = right(edit_planted_date, edit_harvest_date,edit_revenue,edit_prod_cost, edit_notes, view_mode,{form_name}

                
#     submit = False     
#     if menu and not view_mode:
#         left_side, right_side = st.columns([1,5])
#         with left_side:
#             with st.popover("Delete", width="stretch", icon=":material/delete_forever:"):
#                 check1 = st.toggle("I WANT TO DELETE THIS DATA PERMENANETLY")
#                 check2 = st.toggle("I UNDERSTAND THIS IS IRREVERSABLE")
#                 check3 = st.toggle("DETELE THIS DATA")

#                 delete_crop = st.button("DELETE", disabled=not all([check1, check2, check3]), width="stretch", icon=":material/delete_forever:")

#                 if delete_crop:
#                     response = del_crop(edit_item.id, edit_item.user_id)
#                     if response["status"]:
#                         st.success("Successfully Deleted")
#                         time.sleep(1)
#                         st.rerun()

#                     else:
#                         st.error("Something Unexpected Happened")
#                         st.write(response["error_code"])

#         with right_side:
#             submit = st.button("Save Crop", type="primary", width="stretch", icon=":material/save:")

#     if not menu:
#         submit = st.button("Save New Crop", type="primary", width="stretch", icon=":material/save:")
  
#     if submit:
#         if not all([name, prod_year]):
#             st.error("Please Fill Every Mandatory Fields")

#         else:
#             crop = Crop(
#                 id = edit_id,
#                 user_id = edit_user_id,
#                 name = name,
#                 crop_type_id = data_types_dict[name],
#                 prod_start_year = prod_start_year,
#                 prod_end_year = prod_end_year,
#                 planted_date = planted_date,
#                 harvest_date = harvest_date,
#                 crop_yield = crop_yield,
#                 prod_cost = prod_cost,
#                 revenue = revenue,
#                 profit = profit,
#                 notes = notes
#             )

#             if menu:
#                 response = update_crop(crop)
#             else:
#                 response = create_crop(crop)

#             if not response["status"]:
#                 print(response["error_code"])
#                 st.error("Unexpected Error")

#             else:
#                 st.success("Crop Successfully Saved")

#                 time.sleep(1)
#                 st.rerun()
        



@st.dialog("Crop Form", width = "large")
def render_table_form(data_types_dict, form_type, edit_item = None, menu = False, view_mode = False):
    form_name = form_type.title()
    if menu:
        st.session_state.table_menu = False
        st.title(f"{form_name} Menu", text_alignment="center")
        edit_modes = st.segmented_control("Mode",options=["View Mode", "Edit Mode"], default = "View Mode", selection_mode="single", width = "stretch", label_visibility="hidden", required=True)

        view_mode = False if edit_modes == "Edit Mode" else True

        edit_id = edit_item.id
        edit_user_id = edit_item.user_id
        edit_name = list(data_types_dict.keys()).index(edit_item.name)
        edit_prod_year = (edit_item.prod_start_year, edit_item.prod_end_year) if edit_item.prod_start_year != edit_item.prod_end_year else edit_item.prod_start_year
        if form_type == "crop":
            edit_planted_date = edit_item.planted_date
            edit_harvest_date = edit_item.harvest_date
            edit_crop_yield = edit_item.crop_yield
        elif form_type == "livestock":
            pass
            edit_entry_date = edit_item.entry_date
            edit_exit_date = edit_item.exit_date
            edit_amount = edit_item.amount

        edit_prod_cost = edit_item.prod_cost
        edit_revenue = edit_item.revenue
        edit_notes = edit_item.notes

    else:
        st.title(f"Add {form_name}", text_alignment="center")
        edit_id = edit_name = edit_prod_year = edit_entry_date = edit_exit_date = edit_amount = edit_planted_date = edit_harvest_date = edit_crop_yield = edit_prod_cost = edit_revenue = edit_notes = None

        edit_user_id = st.session_state.user
    
    left, right = st.columns([1,2])
    with left:
        

        with st.container(border=True):
            st.success("Mandatory Fields")
            with st.container(border=True):
                st.subheader(f"{form_name}", text_alignment="center")
                name = st.selectbox(f"{form_name} Name [Type] *", options=list(data_types_dict.keys()), index =edit_name,placeholder=f"Choose your {form_name} Option", disabled=view_mode)
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
                    if form_type == "crop":
                        planted_date = st.date_input("Planted Date",value=edit_planted_date,help="if helf empty, will fill with current date",disabled=view_mode )
                        harvest_date = st.date_input("Harvest Date", value = edit_harvest_date,disabled=view_mode)
                    elif form_type == "livestock":
                        entry_date = st.date_input("Entry [Bought] Date",value=edit_entry_date,help="if helf empty, will fill with current date",disabled=view_mode )
                        exit_date = st.date_input("Exit [Sold] Date", value = edit_exit_date,disabled=view_mode)
                        

            with eco:
                with st.container(border=True):
                    st.subheader("Economics", text_alignment="center")
                    l,r = st.columns(2)
                    with l:
                        if form_type== "crop":
                            crop_yield = st.number_input("Crop Yield ", value =edit_crop_yield,step=0.1, min_value=0.0, disabled=view_mode)
                        elif form_type == "livestock":
                            amount = st.number_input("Livestock Amount", value =edit_amount,step=1, min_value=0, disabled=view_mode)
                        prod_cost = st.number_input("Production Cost", value=edit_prod_cost,step=0.1, min_value=0.0, disabled=view_mode)
                           
                    with r:
                        revenue =  st.number_input("Revenue", value=edit_revenue, step=0.1, min_value=0.0, disabled=view_mode)
                        p = revenue-prod_cost if revenue and prod_cost else None
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
                    if form_type == "crop":
                        response = del_crop(edit_item.id, edit_item.user_id)
                    if form_type == "livestock":
                        response = del_livestock(edit_item.id, edit_item.user_id)
                    if response["status"]:
                        st.success("Successfully Deleted")
                        time.sleep(1)
                        st.rerun()

                    else:
                        st.error("Something Unexpected Happened")
                        st.write(response["error_code"])

        with right:
            submit = st.button(f"Save {form_name}", type="primary", width="stretch", icon=":material/save:")

    if not menu:
        submit = st.button(f"Save New {form_name}", type="primary", width="stretch", icon=":material/save:")
  
    if submit:
        if not all([name, prod_year]):
            st.error("Please Fill Every Mandatory Fields")

        else:
            if form_type== "crop":
                data = Crop(
                    id = edit_id,
                    user_id = edit_user_id,
                    name = name,
                    crop_type_id = data_types_dict[name],
                    prod_start_year = prod_start_year,
                    prod_end_year = prod_end_year,
                    planted_date = planted_date,
                    harvest_date = harvest_date,
                    crop_yield = crop_yield,
                    prod_cost = prod_cost,
                    revenue = revenue,
                    profit = profit,
                    notes = notes
                )
                if menu: response = update_crop(data)
                else: response = create_crop(data)
            if form_type == "livestock":

                data = Livestock(
                    id = edit_id,
                    user_id = edit_user_id,
                    name = name,
                    livestock_type_id= data_types_dict[name],
                    prod_start_year = prod_start_year,
                    prod_end_year = prod_end_year,
                    entry_date =entry_date,
                    exit_date = exit_date,
                    amount = amount,
                    prod_cost = prod_cost,
                    revenue = revenue,
                    profit = profit,
                    notes = notes
                )
                if menu: response = update_livestock(data)
                else: response = create_livestock(data)
                

            if not response["status"]:
                print(response["error_code"])
                st.error("Unexpected Error")
            else:
                st.success(f"{form_name} Successfully Saved")
                time.sleep(1)
                st.rerun()