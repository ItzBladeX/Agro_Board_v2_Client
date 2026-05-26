import streamlit as st

def centered_matrix():
    st.markdown(f"""   
    <style text-align: center>
    [data-testid="stMetricLabel"],
    [data-testid="stTitle"],
    [data-testid="stMetric"] {{
        text-align: center !important;
        display: block !important;
    }}
    </style>          
    """, unsafe_allow_html=True)

  