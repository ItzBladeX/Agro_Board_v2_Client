import streamlit as st

def centered_title(text):
    st.markdown(f"""   
    <style text-align: center>
    [data-testid="stMetricLabel"],
    [data-testid="stTitle"],
    [data-testid="stMetric"] {{
        text-align: center !important;
        display: block !important;
    }}
    </style>          
    <h2 style="color:#013014ff; text-align: center; font-family: Arial, sans-serif;"> {text} </h2>
    """, unsafe_allow_html=True)  