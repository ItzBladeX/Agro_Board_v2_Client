import streamlit as st
from app.services import get_crop, get_crop_types, filter_crop
from app.components import render_crop_table, render_crop_form, render_crop_filter, render_crop_graph_card, render_crop_profit_trend
from app.constants import STREAMLIT

def crop_view():
    mode = load_nav() # return selected nav option
    crop_types = load_crop_types() # return dict of crop types : growth rate

    crops = load_sidebar(crop_types) # return filtered crop from sidebar filter

    load_crop_form(crop_types) # responsable for add crop form and edit crop form based on session state
    if not crops:
        st.error("No Crops")
        return
    
    if mode == "Table":
        render_crop_table(crops)
        
    elif mode == "Graph":
        load_crop_graph_card(crops)
    
    elif mode == "Trend":
        load_crop_profit_trend() # No parameters since trend is unaffected by filter. it gets its own crops from


def load_nav():
    return st.segmented_control(" ", options=["Table", "Graph", "Trend"], default="Table", width="stretch", selection_mode="single", required=True)

def load_sidebar(crop_types):
    with st.sidebar:
        filtered_crops = load_crop_filter(crop_types)
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
    for crop in crops:
        with col[curr_col]:
            render_crop_graph_card(crop)
            if curr_col < 3 : curr_col += 1
            else: curr_col = 0
def load_crop_profit_trend():
    with st.container(border=True):
        st.title("Profit Trend", text_alignment="center")
        st.divider()
        # Retrieve crops independent of Filter. Filter doesnt affect Trends
        crops = filter_crop(st.session_state.user, sort="Production Year")
        render_crop_profit_trend(crops["data"], show_table=True)

def load_crop_filter(crop_types):
    
    st.title("Crop Filter", text_alignment="center")
    st.divider()

    filter_response = render_crop_filter(crop_types)

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
    
    # if filter_response["status"] and filter_response["data"]:

    #     filtered_crop = filter_crop(st.session_state.user, *filter_response["data"])

    #     if filtered_crop["status"]:
    #         st.success("Filter: ON")

    #         return filtered_crop["data"]
        
    #     else:
    #         print("Filter Error [Service]", filtered_crop["error_code"])
    #         st.error("Unable to Load Filter")
    #         return None
        
    # else:  
    #     st.error("Filter: OFF")    
    #     get_crop_response = get_crop(st.session_state.user)
    #     if get_crop_response["status"]:

    #         return get_crop_response["data"]
        
    #     else:
    #         print(" Get Crop Error [Service]",get_crop_response["error_code"])
    #         st.error("Unable To Load Crop Table")
    #         return None
    
def load_crop_form(crop_type_dict):
    if "crop_menu" not in st.session_state: 
        st.session_state.crop_menu = False
 
    if st.session_state.get("crop_form", False):
        render_crop_form(crop_type_dict)

    elif st.session_state.get("crop_menu", False):
        render_crop_form(crop_types_dict=crop_type_dict, edit_crop = st.session_state.edit_crop, menu=True)
        
def load_crop_table(filtered_crops):
    
    render_crop_table(filtered_crops)
    
    






    # st.set_page_config(layout="wide")
    # st.logo("logo.png", size='large')
    # database = "crop_database"

    # width = st_javascript("window.innerWidth", key="crop_width")
    # with st.spinner("Loading..."):
    #     func.render_nav("Crop Data", width)

    # time.sleep(0.5)
    # width = st_javascript("window.innerWidth")

    # # tab1, tab2, tab3 = st.tabs(["View", "Add", "Update"])

    # if "ad" not in st.session_state:
    #     st.session_state.ad = False

    # # ---------------------------------------------------------------------------------------------------
    # # ==================================================================================================
    # # ---------------------------------------------------------------------------------------------------

    # st.markdown("""<style> button { height: 56px !important; padding-bottom:5px !important; } </style>""", unsafe_allow_html=True)



    # if "big" not in st.session_state:
    #     st.session_state.big = False
    # # Toggle for custom made table of built in st.framework()
    # bcol1, bcol2 = st.columns(2)


    # if st.button("Change Table", width="stretch", icon=":material/fullscreen:"):
    #     st.session_state.big = not st.session_state.big


            
        
    # if st.session_state.big:
    #     # info1, info2 = st.columns([1.2,1])
    #     # with info1:
    #     #     st.button("Progress", width="stretch")
    #     # with info2:
    #     #     st.button("Economics [ETB]" ,width='stretch')
        

        
    #     with shelve.open(database) as db:
    #         col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([3,3,3,3,3,2.5,2.5,1,1])
    #         with col1: st.button("Crop Type", width="stretch")
    #         with col2: st.button("Planted Date", width="stretch")
    #         with col3: st.button("Harvested Date", width="stretch")
    #         with col4: st.button("Yield [kg]", width="stretch")
    #         with col5: st.button("Production Cost", width="stretch")
    #         with col6: st.button("Sold Price", width="stretch")
    #         with col7: st.button("Profit", width="stretch")
    #         with col8: st.button("",  icon=":material/add:", on_click=func.add_data, args=(database,"crop"), width="stretch")
    #         with col9: st.button("", icon=":material/autorenew:", on_click=st.rerun,width="stretch")
    #         years = [key for key in db]
    #         year_list = func.sort_years(list(set(years)))
    #         for yr in year_list:
    #             st.button(f"{yr}", width="stretch")
    #             for select_year in db:
    #                 if select_year == yr:
    #                     year_data = db[select_year]
    #                     for crop_type in year_data:
    #                         crop = year_data[crop_type]
                                                        
    #                         col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([3,3,3,3,3,2.5,2.5,1,1])  # Loop over the db keys and display results
                            
    #                         with col1: st.success(crop.type)
    #                         with col2: st.success(crop.date)
    #                         with col3: st.success(str(crop.estimated) + " " + crop.user)
    #                         with col4: st.success(func.format_number(crop.yield_amount))
    #                         with col5: st.success(func.format_number(crop.production_cost))
    #                         with col6: st.success(func.format_number(crop.export_cost))
    #                         with col7: st.success(func.format_number(crop.profit))
    #                         with col8: st.button(icon=":material/edit:", label="", key=f"edit{yr}{crop_type}", on_click=func.edit, args=(database, None, yr, crop_type), type="secondary", width='stretch')
    #                         with col9: st.button(icon=":material/delete:",label="", key=f"del{yr}{crop_type}", on_click=func.delete, args=(database, yr, crop_type), type="primary", width="stretch")
                    
                            


    # else:  # DataFrame for small table id toggle not toggled
    #     with shelve.open(database) as db:
    #         # data_years = [years for years in db]
    #         data = {}
    #         for year, crops_dict in db.items():
    #             for crop_type, crop_data in crops_dict.items():
    #                 data[year, crop_type] = vars(crop_data)
    #         # st.write("Loaded keys:", list(db.keys()))
    #         data = pd.DataFrame.from_dict(data, orient="index")
    #         if "production_year" in data.columns and "type" in data.columns:
    #             data = data.drop(columns=["production_year", "type"])
    #         try:data.index.names = ["Production year", "Type"]
    #         except:data.index.name = "Production year"  
    #         data = data.rename(columns={
    #             "type": "Crop Type",
    #             "date": "Planted Date",
    #             "estimated": "Harvested Date",
    #             "yield_amount": "Yield [kg]",
    #             "export_cost": "Sold Price",
    #             "production_cost" : "Production Cost",
    #             "profit" : "Profit"
    #         })
    #         st.dataframe(data, width="stretch")


        





    # # ---------------------------------------------------------------------------------------------------
    # # ==================================================================================================
    # # ---------------------------------------------------------------------------------------------------
