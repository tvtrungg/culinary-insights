import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    
    cleaned_recipes_v2 = pd.read_csv("data/cleaned_recipes_v2.csv", index_col=0) # Data overview
    cleaned_recipes3 = pd.read_csv("data/cleaned_recipes3.csv", index_col=0) # Data overview
    recipes_df = pd.read_csv("data/recipes_df.csv", index_col=0) # Data overview, giống với recipes3
    cuisine_stats = pd.read_csv("data/cuisine_stats_with_sub_region_and_clusters.csv", index_col=0)
    df_clustered = pd.read_csv("data/df_clustered.csv", index_col=0)
    eco_scores_and_luxury_scores = pd.read_csv("data/recipes_df_with_eco_scores_and_luxury_scores.csv", index_col=0)
    recipes_df_with_hofstede = pd.read_csv("data/recipes_df_with_hofstede.csv", index_col=0)
    
    return cleaned_recipes_v2, cleaned_recipes3, cuisine_stats, df_clustered, eco_scores_and_luxury_scores, recipes_df_with_hofstede, recipes_df