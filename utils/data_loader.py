import pandas as pd
import streamlit as st

@st.cache_data
def load_cleaned_recipes_v2():
    return pd.read_csv("data/cleaned_recipes_v2.csv", index_col=0)

@st.cache_data
def load_cleaned_recipes3():
    return pd.read_csv("data/cleaned_recipes3.csv", index_col=0)

@st.cache_data
def load_recipes_df():
    return pd.read_csv("data/recipes_df.csv", index_col=0)

@st.cache_data
def load_cuisine_stats():
    return pd.read_csv("data/cuisine_stats_with_sub_region_and_clusters.csv", index_col=0)

@st.cache_data
def load_df_clustered():
    return pd.read_csv("data/df_clustered.csv", index_col=0)

@st.cache_data
def load_eco_scores_and_luxury_scores():
    return pd.read_csv("data/recipes_df_with_eco_scores_and_luxury_scores.csv", index_col=0)

@st.cache_data
def load_recipes_df_with_hofstede():
    return pd.read_csv("data/recipes_df_with_hofstede.csv", index_col=0)

@st.cache_data
def load_who_health():
    return pd.read_excel("data/world_health_statistics_2024.xlsx", sheet_name=None)

@st.cache_data
def load_cuisine_with_gdp_growth():
    return pd.read_csv("data/cuisine_with_gdp_growth.csv")

