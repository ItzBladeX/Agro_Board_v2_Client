import streamlit as st
from streamlit_javascript import st_javascript
# import client_app.app.functions as func
import time
def about_view():
    st.set_page_config(page_title="AGRO-BOARD", layout="wide", )



    col1, col2, col3 = st.columns(3)
    with col2:st.image("app/assets/logo.png", width=400)

    st.title("AgroBoard", text_alignment="center")
    st.subheader("***Agricultural Data and Statistics Dashbaord***", text_alignment="center")

    st.title("What is AgroBoard?")
    st.subheader("""
        AgroBoard is an innovative platform designed to simplify agricultural data and statistics management. 
        With its intuitive and user-friendly interface, it caters to everyone—from small-scale farmers to large enterprises. 
        AgroBoard empowers users with powerful data analytics capabilities, making it easier than ever to visualize, track, and optimize agricultural performance and productivity.

    """)
    st.title("Key Features")

    st.header("""
    📊 Comprehensive Data Management
    Store, organize, and access all your agricultural data — from crop yields and expenses to exports and profits — in one centralized platform.
    """)
    st.header("""
    📈 Advanced Analytics & Visualization
    Transform raw data into clear insights through dynamic charts, graphs, and metrics that help you make informed decisions.
    """)
    st.header("""
    💡 Smart Insights
    Identify trends, monitor progress, and detect inefficiencies with automated data analysis designed to improve productivity.""")
    st.header("""
    🖥️ User-Friendly Interface
    An intuitive, clean design that makes it easy for anyone — from small farmers to large enterprises — to navigate and manage data effortlessly.""")
    st.header("""
    ☁️ Local Area Integration
    Securely store and access data anytime with LAN-based synchronization """)


    st.title("Get Started with Agro-Board Today!")
    st.header("""
            
    💬 Inspirational / Call to Action

    Empower your farm with smarter insights — get ready with Agro-Board today on GitHub: https://github.com/itz-BladeX/Agro_Board""")