import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.style import inject_css


inject_css()

st.markdown("""
# Environmental axis
            
This axis aims to explore the environmental impact of culinary cultures around the world. By estimating the **carbon footprint of ingredients** used in national cuisines, we can assess how sustainable different food traditions are.

This complements our economic and health axes by adding a third dimension: **ecological responsibility**.

Key questions include:
- Which cuisines are the most or least sustainable?
- Does environmental impact correlate with economic status, health outcomes, or culinary complexity?
- Are some regions naturally more eco-conscious in their food culture?
""")

recipes_df = pd.read_csv("data/recipes_df.csv")


region_info = recipes_df[["cuisine", "sub_region", "continent"]].drop_duplicates()

# Re-aggregate eco scores and merge region info
cuisine_eco_df = recipes_df.groupby("cuisine").agg(
    avg_eco_score=("eco_score", "mean"),
    std_eco_score=("eco_score", "std"),
    num_recipes=("eco_score", "count")
).reset_index()

cuisine_eco_df = cuisine_eco_df.merge(region_info, on="cuisine", how="left")

st.markdown("## Aggregating Eco-Score by Cuisine")

st.write(cuisine_eco_df)

st.markdown("## Regional Visualizations")
# Drop missing values once to reuse
filtered_df_continent = cuisine_eco_df.dropna(subset=["continent"])
filtered_df_subregion = cuisine_eco_df.dropna(subset=["sub_region"])

# Boxplot by continent
fig_continent = px.box(
    filtered_df_continent,
    x="continent",
    y="avg_eco_score",
    color="continent",
    title="Eco Score by Continent",
    labels={"avg_eco_score": "Average Recipe Eco Score (kg CO₂-eq)"},
    color_discrete_sequence=px.colors.sequential.Purples  # or adapt to match cubehelix
)
fig_continent.update_layout(xaxis_tickangle=-45, template="plotly_white")

# Boxplot by sub-region
fig_subregion = px.box(
    filtered_df_subregion,
    x="sub_region",
    y="avg_eco_score",
    color="sub_region",
    title="Eco Score by Sub-Region",
    labels={"avg_eco_score": "Average Recipe Eco Score (kg CO₂-eq)"},
    color_discrete_sequence=px.colors.sequential.Purples
)
fig_subregion.update_layout(xaxis_tickangle=-45, xaxis_tickfont=dict(size=10), template="plotly_white")

# To display in Streamlit

st.plotly_chart(fig_continent, use_container_width=True)
st.plotly_chart(fig_subregion, use_container_width=True)

st.markdown("## Correlation Analysis – Eco Score vs Economic and Health Indicators")

gdp_df = pd.read_csv("data/cuisine_with_gdp_growth.csv")
health_df = pd.read_csv("data/df_clustered.csv")

# Standardize column names and merge on 'cuisine'
merged_df = cuisine_eco_df.merge(
    gdp_df[["cuisine", "GDP_2022", "GDP_growth"]],
    on="cuisine", how="left"
).merge(
    health_df[["cuisine", 
               "Life expectancy at birth (years)", 
               "Healthy life expectancy at birth (years)", 
               "UHC: Service coverage index", 
               "Obesity_Adult_18plus", 
               "num_ingredients", 
               "luxury_score"]],
    on="cuisine", how="left"
)

# Rename column
corr_df = merged_df.rename(columns={"avg_eco_score": "Eco Score"})

# Select and compute correlation matrix
corr_cols = ["Eco Score", "GDP_2022", "GDP_growth", 
             "Life expectancy at birth (years)", 
             "Healthy life expectancy at birth (years)", 
             "UHC: Service coverage index", 
             "Obesity_Adult_18plus"]

correlation_matrix = corr_df[corr_cols].corr()

# Create interactive heatmap
fig_corr = px.imshow(
    correlation_matrix,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    title="Correlation between Eco Score, GDP, and Health Indicators",
    labels=dict(color="Correlation"),
    aspect="auto"
)

# Streamlit display
st.plotly_chart(fig_corr, use_container_width=True)

st.markdown("## Do Luxury and Complexity Interact to Influence Environmental Impact?")

recipes_df = pd.read_csv("data/recipes_df_with_eco_scores_and_luxury_scores.csv")

# Drop missing values and create interaction term
df_model = recipes_df.dropna(subset=["num_ingredients", "luxury_score", "eco_score"]).copy()
df_model["interaction"] = df_model["num_ingredients"] * df_model["luxury_score"]

# Interactive scatter plot
fig_scatter = px.scatter(
    df_model,
    x="num_ingredients",
    y="luxury_score",
    color="eco_score",
    color_continuous_scale="RdBu_r",
    labels={
        "num_ingredients": "Number of Ingredients",
        "luxury_score": "Luxury Score",
        "eco_score": "Eco Score"
    },
    title="Luxury × Complexity Interaction Colored by Eco Score",
    opacity=0.7
)

fig_scatter.update_layout(coloraxis_colorbar=dict(title="Eco Score"))

# Streamlit display
st.plotly_chart(fig_scatter, use_container_width=True)