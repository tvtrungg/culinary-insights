import streamlit as st
import pandas as pd

from utils.data_loader import load_recipes_df, load_who_health
from utils.style import inject_css


inject_css()

st.markdown("## Health Axis")

recipes_df = load_recipes_df()
who_health = load_who_health()


# Preview basic info
st.markdown("### Dataset Overview")
with st.expander("Preview Columns and Data"):
    st.write("Recipe columns:", recipes_df.columns.tolist())
    st.write("WHO Excel sheets:", list(who_health.keys()))
    st.dataframe(recipes_df.head(3))

# WHO Data
who_df = who_health["data"]

# Show sample indicators
st.markdown("### WHO Health Indicators Sample")
with st.expander("Top Indicators"):
    indicators_summary = who_df["IND_NAME"].value_counts().head(30)
    st.dataframe(indicators_summary)

# Selected key indicators
health_indicators = [
    "Life expectancy at birth (years)",
    "Healthy life expectancy at birth (years)",
    "Prevalence of obesity among adults",
    "Prevalence of hypertension among adults",
    "Total alcohol per capita",
    "UHC: Service coverage index"
]

# Filter & reshape
filtered_health_df = who_df[who_df["IND_NAME"].isin(health_indicators)].copy()
filtered_health_df.sort_values("DIM_TIME_YEAR", ascending=False, inplace=True)
filtered_health_df = filtered_health_df.drop_duplicates(subset=["IND_NAME", "DIM_GEO_NAME"])
health_wide = filtered_health_df.pivot(
    index="DIM_GEO_NAME", columns="IND_NAME", values="VALUE_NUMERIC"
).reset_index().rename(columns={"DIM_GEO_NAME": "cuisine"})

st.markdown("### Processed WHO Health Data")
st.dataframe(health_wide.head())

# Evaluate ingredient semantics
recipes_df["ingredient_semantics"] = recipes_df["ingredient_semantics"].apply(eval)

luxury_keywords = ["dairy", "seafood", "nut", "sweetener"]
def count_luxury(sem_list):
    return sum(1 for item in sem_list if item in luxury_keywords)

recipes_df["luxury_score"] = recipes_df["ingredient_semantics"].apply(count_luxury)

# Aggregate features by cuisine
cuisine_health_features = recipes_df.groupby("cuisine").agg({
    "Calories": "mean",
    "Fat": "mean",
    "Carbs": "mean",
    "Protein": "mean",
    "num_ingredients": "mean",
    "luxury_score": "mean",
    "sub_region": "first",
    "continent": "first"
}).reset_index()

# Merge datasets
merged_health_df = cuisine_health_features.merge(health_wide, on="cuisine", how="left")

st.markdown("### Merged Culinary & Health Data")
st.dataframe(merged_health_df.head())
