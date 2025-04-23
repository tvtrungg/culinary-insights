import streamlit as st
import pandas as pd 
from content.common_ingredients_analysis import common_ingredients_analysis
from content.page_2 import page_2
from content.page_3 import page_3


st.set_page_config(
    page_title="SDA 2025 - Thieu",
    page_icon=":Airplane:",
    layout='wide',
    initial_sidebar_state="auto",
    menu_items={
        'About': "#Github Repository :\n\nhttps://github.com/Meriadoc-gitgit/DeepLearWing-viz"
    }
)


def app_layout():
    print("Chargement avec succès")

    page = st.sidebar.radio("Summary", ["Common Ingredients Analysis", "Page 2", "Conclusion"])

    if page == "Common Ingredients Analysis":
        common_ingredients_analysis()
    elif page == "Page 2":
        page_2()
    # elif page == "Optimisation":
    #     optimisation(stratified_df)
    else:
        page_3()
