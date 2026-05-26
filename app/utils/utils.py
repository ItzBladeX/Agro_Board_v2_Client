import streamlit as st
from millify import millify
from datetime import date
def formatted(value, is_currency=False, is_yield=False, is_year = False):
   
    if value is None:
        return "--"
    if is_currency:
        return f"{millify(value, precision=1)} Br"
    if is_yield:
        return f"{millify(value, precision=1)} KG"
        
    if isinstance(value, tuple):
        if value[0] == value[-1]:
            return f"{value[0]}"
        else:
            return f"{value[0]}/{value[1]}"
    if isinstance(value, date):

        return f"{value.strftime('%b %d, %Y')}"

    if isinstance(value, float) and value.is_integer():
        value = int(value)
    

    if isinstance(value, int):
        print(millify(value, precision=3))
        return f"{millify(value, precision=3)}"
    
    return f"{millify(value, precision=3)}"

def order_years(unordered):
    return sorted(unordered, key=lambda x: (x[0], x[-1]), reverse=True)

def sort_crops(unordered_crops):

    sort = sorted(unordered_crops, key=lambda crop: (crop.prod_start_year, crop.prod_end_year), reverse=True)
    return sort

def set_button_size(key,height):
    st.markdown(f"""
        <style>.st-key-{key} button {{
            height: {height}px !important; 
            padding-bottom:5px !important; 
            }} 
        </style>""", 
    unsafe_allow_html=True)
