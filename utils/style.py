import streamlit as st

def inject_css():
    st.markdown("""
    <style>
        table {
            width: 100% !important;
            table-layout: auto;
        }
        .st-emotion-cache-mtjnbi {
            max-width: 90% !important;
        }
    </style>
    """, unsafe_allow_html=True)
