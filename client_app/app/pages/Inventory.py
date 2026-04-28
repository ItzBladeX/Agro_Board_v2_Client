import streamlit as st
import shelve
import pandas as pd
import client_app.app.functions as func
from streamlit_javascript import st_javascript
import time

database = "inventory_database"

st.set_page_config(layout="wide")
st.logo("logo.png", size='large')

Width = st_javascript("window.innerWidth", key="inventory_width")
func.render_nav("Inventory Data", Width)
time.sleep(0.5)


st.markdown("""<style> button { height: 56px !important; padding-bottom:5px !important; } </style>""", unsafe_allow_html=True)

if "big" not in st.session_state:
    st.session_state.big = False


if st.button("Change Table", width="stretch", icon=":material/fullscreen:"):
    st.session_state.big = not st.session_state.big


if st.session_state.big:
    info1, info2 = st.columns(2)
    

    with shelve.open(database) as db:
        col1, col2, col3, col4, col5, col6= st.columns(6)
        with col1: st.button("ID",width="stretch")
        with col2: st.button("Label",width="stretch")
        with col3: st.button("Quantity [Units\Litre\]",width="stretch")
        with col4: st.button("Date", width="stretch")
        with col5: st.button("Add", width="stretch", icon=":material/add:", on_click=func.add_data, args=(database,"inventory"))
        with col6: st.button("Reload ",width="stretch", icon=":material/autorenew:", on_click=st.rerun)

        # st.divider()

        for key in db:  # Loop over the db keys and display results
            col1, col2, col3, col4, col5, col6= st.columns(6)
            inventory = db[key]
            with st.container():
                
                with col1: st.warning(inventory.id)
                with col2: st.warning(inventory.label)
                with col3: st.warning(inventory.quantity)
                with col4: st.warning(inventory.date)
                with col5: st.button("", icon=":material/edit:", type="secondary", key=f"edit{key}",help="Edit Data", on_click=func.edit, args=(database,key), width="stretch")
                with col6: st.button("", icon=":material/delete:", type="primary",key=f"del{key}", help="Delete Data Permanently", on_click=func.delete, args=(database, key), width="stretch")



else:  # DataFrame for small table id toggle not toggled
    with shelve.open(database) as db:
        data = {key: vars(inventory) for key, inventory in db.items()}
        # st.write("Loaded keys:", list(db.keys()))
        data = pd.DataFrame.from_dict(data, orient="index")
        if "id" in data.columns:
            data = data.drop(columns=["id"])
        data.index.name = "ID"
        data = data.rename(columns={
            "id": "ID",
            "label": "Label",
            "quantity": "Quantity [Units\Litre\]",
            "date": "Date"
        })
        st.dataframe(data, width="stretch")




# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
# def toggle():   # Advanced Obtion Toggle
#     st.session_state.adv = not st.session_state.ad