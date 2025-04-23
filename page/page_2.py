import streamlit as st

md_path = "./content/page_2.md"

with open(md_path, "r", encoding="utf-8") as f:
    md_content = f.read()

def page_2():
    """
    Introduction page of the dashboard
    """
    st.markdown(md_content, unsafe_allow_html=True)
