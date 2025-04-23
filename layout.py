import streamlit as st
import pandas as pd 
from content.data import data
from content.wordcloud import wordcloud
from content.usps import usps


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

    df = pd.read_csv("data/cleaned_recipes_v2.csv", index_col=0)

    page = st.sidebar.radio("Summary", ["Data Overview", "Word Cloud", "PCA"])

    if page == "Data Overview":
        data(df)
    elif page == "Word Cloud":
        wordcloud(df)
    # elif page == "Optimisation":
    #     optimisation(stratified_df)
    else:
        usps(df)
