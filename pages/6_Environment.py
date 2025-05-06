import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import StandardScaler
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from scipy.stats import f_oneway

from utils.data_loader import load_eco_scores_and_luxury_scores, load_recipes_df
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

recipes_df = load_recipes_df()


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

st.markdown("## Correlation Analysis - Eco Score vs Economic and Health Indicators")

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

col1, col2 = st.columns(2)

with col1:
    st.subheader("Eco Score Insights")
    st.markdown("""
    - **Eco Score vs GDP_2022**: `+0.19`  
      A **weak positive correlation** suggests that countries with higher income levels tend to have slightly higher-emission cuisines. This is likely due to the consumption of **resource-intensive foods** (e.g. beef, dairy) that are more affordable in wealthy nations.
    
    - **Eco Score vs GDP Growth**: `+0.06`  
      No meaningful correlation. Economic growth trends don’t significantly impact the sustainability of national cuisines.
    
    - **Eco Score vs Life Expectancy**: `+0.08`  
      Nearly no correlation. This indicates that countries with high-impact cuisines are **not necessarily more or less healthy** in terms of longevity.
    
    - **Eco Score vs Healthy Life Expectancy**: `+0.11`  
      Very weak association. Again, **sustainability and public health longevity do not strongly co-vary** at the country level.
    
    - **Eco Score vs UHC (Service Coverage Index)**: `+0.11`  
      Slight positive trend. Countries with broader healthcare access **may have more industrialized and high-impact food systems**, but the link is weak.
    
    - **Eco Score vs Obesity_Adult_18plus**: `−0.17`  
      Surprisingly, a **moderate negative correlation**. This suggests that higher-obesity countries may **not** be the ones with the highest environmental food footprints — possibly due to **processed, energy-dense but low-CO₂ foods** (e.g., sugar, oil, refined carbs) dominating in less sustainable ways.
    """)

with col2:
    st.subheader("Conclusions")
    st.markdown("""
    - Wealth (GDP) **slightly increases** environmental food impact.
    - **Health outcomes (life expectancy, UHC)** do **not strongly align** with eco score.
    - Obesity and eco score show an **inverse relationship**, indicating that unsustainable eating is not always associated with excess.

    This matrix supports the idea that **sustainable diets can exist in both rich and poor countries**, and **high emissions don't automatically mean unhealthy outcomes** — making this axis especially relevant for holistic policy considerations.
    """)


st.markdown("## Step 4 : Verifying hypotheses related to eco score and recipes ")
# Assuming your dataframes are loaded and preprocessed as in the original code
# Safely convert stringified lists if needed
recipes_df["ingredient_semantics"] = recipes_df["ingredient_semantics"]
luxury_ingredients = {"dairy", "seafood", "nut", "sweetener"}

# Compute luxury score for each recipe
recipes_df["luxury_score"] = recipes_df["ingredient_semantics"].apply(
    lambda sems: sum(1 for item in sems if item in luxury_ingredients)
)

# Re-merge with eco scores
merged_df = recipes_df.merge(
    cuisine_eco_df[["cuisine", "avg_eco_score"]],
    on="cuisine", how="left"
)

# Bin by complexity
bins = [0, 7, 13, np.inf]
labels = ['Low', 'Medium', 'High']
merged_df['ingredient_complexity'] = pd.cut(merged_df['num_ingredients'], bins=bins, labels=labels)

# Prepare groups for ANOVA
groups = [group["avg_eco_score"].dropna() for name, group in merged_df.groupby("ingredient_complexity")]
# Perform ANOVA test
anova_result = f_oneway(*groups)

# Compute correlation
luxury_corr = merged_df[["luxury_score", "avg_eco_score"]].corr().iloc[0, 1]

# Create Streamlit columns
col1, col2 = st.columns(2)

with col1:
    # Boxplot for Eco Score by Ingredient Complexity
    fig1 = px.box(
        merged_df,
        x="ingredient_complexity",
        y="avg_eco_score",
        title="Eco Score by Ingredient Complexity",
        labels={"ingredient_complexity": "Ingredient Complexity", "avg_eco_score": "Average Eco Score (kg CO₂-eq)"},
        color="ingredient_complexity",
        color_discrete_sequence=["#66C2A5", "#FC8D62", "#8DA0CB"]
    )
    fig1.update_layout(
        showlegend=False,
        title_font_size=24,
        margin={"r": 0, "t": 40, "l": 0, "b": 40}
    )
    st.plotly_chart(fig1)

with col2:
    # Scatter plot for Luxury Score vs Average Eco Score
    fig2 = px.scatter(
        merged_df,
        x="luxury_score",
        y="avg_eco_score",
        title="Luxury Score vs Average Eco Score",
        labels={"luxury_score": "Luxury Ingredient Score", "avg_eco_score": "Average Eco Score (kg CO₂-eq)"},
        trendline="ols",  # Add linear regression line
        color="luxury_score",
        color_continuous_scale="Viridis"
    )
    fig2.update_layout(
        showlegend=False,
        title_font_size=24,
        margin={"r": 0, "t": 40, "l": 0, "b": 40}
    )
    st.plotly_chart(fig2)

st.write(anova_result)
st.write(luxury_corr)

col1, col2 = st.columns(2)

with col1:
    st.subheader("H1 - Does Ingredient Complexity Influence Environmental Impact?")
    st.markdown("""
    We tested whether cuisines with **more complex recipes** (more ingredients) have significantly different environmental costs using a **one-way ANOVA**.

    - **Tested Groups**:
      - Low complexity (≤7 ingredients)
      - Medium complexity (8–13 ingredients)
      - High complexity (14+ ingredients)
    
    **ANOVA Result**:
    - **F-statistic** = 81.21
    - **p-value** = 2.86e-35
    
    **Conclusion**:
    The test shows a **highly significant difference** in mean eco scores between complexity groups. This suggests that **ingredient-rich cuisines** tend to have **higher environmental costs**.
    """)

with col2:
    st.subheader("H2 – Does Culinary Luxury Correlate with Environmental Impact?")
    st.markdown("""
    We calculated the **Pearson correlation** between:
    - `luxury_score` = count of luxury ingredients (`dairy`, `seafood`, `nut`, `sweetener`)
    - `avg_eco_score` per recipe
    
    **Correlation Coefficient**:  
    - **r = 0.18** (weak positive correlation)
    
    **Conclusion**:
    There is a **modest but consistent** link between culinary luxury and carbon footprint. While not as strong as ingredient complexity, luxury-rich recipes tend to have **higher eco scores**.
    """)

# Second section, aligned at the bottom
st.subheader("Interpretation")
st.markdown("""
These findings support the idea that:
- **Recipe complexity** is a strong predictor of environmental impact.
- **Luxury ingredients** raise the eco footprint, though less dramatically.
- This aligns with prior expectations and validates the eco_score as a **behavioral proxy** for sustainability.
""")

st.markdown("""## Upcoming Hypothesis Tests

| Hypothesis Code | Question                                         | Type          | Method                      |
|------------------|--------------------------------------------------|---------------|-----------------------------|
| **H3**           | Is Eco Score significantly different across GDP classes? | Group Test    | ANOVA                       |
| **H4**           | Is there a relationship between Healthy Life Expectancy and Eco Score? | Correlation   | Pearson Correlation / Linear Regression |
| **H5**           | Do continents or sub-regions differ in Eco Score? | Group Test    | ANOVA                       |
| **H6**           | Is obesity rate correlated with Eco Score?       | Correlation   | Pearson Correlation         |
| **H7**           | Does Universal Health Coverage predict Eco Score? | Correlation   | Linear Regression           |
| **H8**           | Do Luxury Score and Ingredient Complexity interact to explain Eco Score? | Interaction   | Polynomial Regression       |
""")









st.markdown("## Do Luxury and Complexity Interact to Influence Environmental Impact?")

df = load_eco_scores_and_luxury_scores()

# Drop missing values and create interaction term
df_model = df.dropna(subset=["num_ingredients", "luxury_score", "eco_score"]).copy()
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

col1, col2, col3 = st.columns(3)

# --- Column 1: Method ---
with col1:
    st.markdown("### Method")
    st.markdown("""
We modeled whether **culinary complexity** (number of ingredients) and **luxury** (presence of high-impact ingredients like dairy, seafood, etc.) jointly affect the **eco score** of a recipe.

- Multiple Linear Regression with interaction term:
  - **Predictors**: `num_ingredients`, `luxury_score`, and `num_ingredients × luxury_score`
  - **Target**: `eco_score`
""")

# --- Column 2: Model Performance ---
with col2:
    st.markdown("### Model Performance")
    st.markdown("""
- **R² Score**: **0.28**  
  The model explains ~28% of the variance in eco scores — a reasonable fit given recipe variability.

- **Coefficients**:
  - `num_ingredients`: **+3.87** → More ingredients = higher eco score.
  - `luxury_score`: **−1.51** → Surprisingly, luxury score alone is associated with a lower eco score, likely due to interaction effects.
  - `interaction`: **+0.02** → The impact of luxury **increases with ingredient count**.
""")

# --- Column 3: Interpretation ---
with col3:
    st.markdown("### Interpretation")
    st.markdown("""
This model suggests that:
- **Ingredient complexity** is the strongest standalone predictor of carbon footprint.
- **Luxury alone** isn't environmentally damaging — unless it's **combined with high complexity**.
- The interaction term is crucial: the most **environmentally intense dishes are both luxurious and complex**.

This validates a nuanced view:  
**Not all rich cuisines are unsustainable**, but complex, multi-luxury dishes often are.
""")
    

st.markdown("""## Step 5 : Clustering recipes using K-Means and profiling clusters""")
df_cluster = df.dropna(subset=[
    "eco_score", "Calories", "Fat", "Carbs", "Protein",
    "num_ingredients", "luxury_score"
])

# Select and standardize features
features = ["eco_score", "Calories", "Fat", "Carbs", "Protein", "num_ingredients", "luxury_score"]
X = df_cluster[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply KMeans clustering
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df_cluster["cluster"] = kmeans.fit_predict(X_scaled) + 1

# PCA for 2D visualization
pca = PCA(n_components=2)
pca_coords = pca.fit_transform(X_scaled)
df_cluster["PCA1"] = pca_coords[:, 0]
df_cluster["PCA2"] = pca_coords[:, 1]

# Create interactive scatter plot
fig = px.scatter(
    df_cluster,
    x="PCA1",
    y="PCA2",
    color="cluster",
    hover_data=["cuisine", "eco_score", "luxury_score", "num_ingredients"],
    title="Clustering of Recipes by Environmental & Nutritional Features",
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig.update_layout(
    width=600,
    height=500,
    title_font_size=24,
    legend_title="Cluster",
    margin=dict(l=20, r=20, t=50, b=20)
)

# Display in two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Cluster Distribution")
    cluster_counts = df_cluster["cluster"].value_counts().sort_index().rename_axis("Cluster").reset_index(name="Count")
    st.dataframe(cluster_counts)

st.markdown("""### Cluster profiles""")

# Compute cluster profiles
cluster_profiles = df_cluster.groupby("cluster").agg({
    "eco_score": "mean",
    "Calories": "mean",
    "Fat": "mean",
    "Carbs": "mean",
    "Protein": "mean",
    "num_ingredients": "mean",
    "luxury_score": "mean"
}).round(2).reset_index()

# Display in a nice table
st.markdown("#### Summary Statistics per Cluster")
st.dataframe(cluster_profiles, use_container_width=True)

st.markdown("#### Cluster profiles : Environmental and Nutritional Archetypes")
st.markdown("""
Each recipe was clustered using a combination of:

- **Eco Score** (carbon footprint)
- **Macronutrients**: Calories, Fat, Carbs, Protein
- **Ingredient Complexity**
- **Luxury Ingredient Score**

This revealed 4 distinct culinary profiles across nearly 6000 recipes.
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Cluster 1 - Heavy & Hearty")
    st.markdown("""
- **Highest calories (897.9)** and **protein (43.5)** of all clusters  
- High fat and carb content  
- Moderate ingredient count and luxury score  
- Likely large meat-based or indulgent dishes (e.g. stews, grills, traditional feasts)
    """)

    st.markdown("#### Cluster 2 - Light & Low Impact")
    st.markdown("""
- **Lowest eco score (24.98)** and nutritional values across the board  
- Very low calories, fat, and protein  
- Some luxury (avg. 0.8), likely simple or side dishes  
- Represents sustainable, light recipes — possibly soups, snacks, and plant-based fare
    """)

with col2:
    st.markdown("#### Cluster 3 - Balanced Classics")
    st.markdown("""
- Moderate levels across all dimensions  
- Calories: ~459, Protein: ~20g, Eco Score: ~38  
- Average ingredient count and luxury  
- Possibly represents home-cooked staples or culturally common foods
    """)

    st.markdown("#### Cluster 4 - Luxury Complexity Bomb")
    st.markdown("""
- **Highest Eco Score (125.19)** and **Luxury Score (2.53)**  
- Very high ingredient complexity (24+ ingredients)  
- Moderate calories — intricate but not necessarily heavy  
- Likely gourmet dishes, holiday meals, or rich recipes with seafood, dairy, nuts
    """)

# Overall insights
st.markdown("#### Key Insights")
st.markdown("""
- **Eco Score aligns strongly with complexity and luxury**, more than calories or fat.  
- Sustainable doesn’t always mean low-calorie — and high-calorie doesn’t always mean high-impact.  
- Clusters show that cuisines can be grouped by their **environmental and structural culinary patterns**, not just by geography or health.
""")


st.markdown("""### Mapping cuisines to dominant clusters to profile eco trends by region or cluster """)
# Two columns for logical grouping
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 1. Dominant Cluster per Cuisine")

    # Compute dominant cluster
    dominant_clusters = df_cluster.groupby("cuisine")["cluster"].agg(
        lambda x: x.value_counts().idxmax()
    ).reset_index()
    dominant_clusters.columns = ["cuisine", "dominant_cluster"]

    # Compute eco stats
    eco_stats = df_cluster.groupby("cuisine").agg(
        avg_eco_score=("eco_score", "mean"),
        num_recipes=("eco_score", "count")
    ).reset_index()

    # Merge dominant cluster with eco stats
    cuisine_cluster_map = pd.merge(dominant_clusters, eco_stats, on="cuisine", how="left")

    st.dataframe(cuisine_cluster_map)

with col2:
    st.markdown("#### 2. Cluster Composition by Continent")

    # Merge region and continent info
    cuisine_geo_map = cuisine_cluster_map.merge(
        cuisine_eco_df[["cuisine", "sub_region", "continent"]].drop_duplicates(),
        on="cuisine", how="left"
    )

    # Count number of cuisines per cluster per continent
    region_cluster_counts = cuisine_geo_map.groupby(
        ["continent", "dominant_cluster"]
    ).size().unstack().fillna(0).astype(int)

    st.dataframe(region_cluster_counts)

st.markdown("### Observations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Cluster 1 - *Heavy & Hearty*")
    st.markdown("""
    - Surprisingly **absent in Africa, Americas, and Asia**.  
    - Only **1 instance in Europe**, where perhaps meat-heavy traditions exist in fewer cuisines overall.
    """)

    st.markdown("#### Cluster 2 - *Light & Low-Impact*")
    st.markdown("""
    - The most **globally dominant cluster**, representing **sustainable, lower-calorie, less complex** recipes.  
    - Strongly dominant in **Asia**, **Americas**, and **Europe**.  
    - Likely reflects **daily staples**, **vegetable-forward** dishes, or **cultural minimalism**.
    """)

with col2:
    st.markdown("#### Cluster 3 - *Balanced Classics*")
    st.markdown("""
    - Equally represented in **Asia** and **Europe**.  
    - This is a **moderate-carbon, nutritionally balanced** profile — possibly typical home-style or culturally “complete” meals.  
    - Asia shows **14 cuisines in this group**, suggesting culinary **variety without extremity**.
    """)

    st.markdown("#### Cluster 4 - *Luxury Complexity Bomb*")
    st.markdown("""
    - The **rarest globally**, but appears in **Asia**, **Africa**, **Europe**, and **Oceania** — in small numbers.  
    - Represents **resource-heavy, elaborate dishes**, possibly tied to heritage or ceremonial cuisine.  
    - Asia has the **highest count** (6), showcasing its **culinary richness**.
    """)

st.markdown("### Conclusion")
st.markdown("""
- The **majority of world cuisines lean toward sustainability** (Cluster 2).  
- **Asia is the most balanced and diverse**, with cuisines spread across all clusters.  
- **Luxury and high-impact culinary profiles** exist — but are rare, concentrated, and not the global norm.
""")


# Drop entries without country names
map_df = cuisine_geo_map.dropna(subset=["cuisine"])
map_df["dominant_cluster"] = map_df["dominant_cluster"].astype(str)

color_map = {
    "1": "#66C2A5",  # soft green
    "2": "#FC8D62",  # pastel orange
    "3": "#8DA0CB",  # muted purple
    "4": "#E78AC3"   # pink/red shade
}

# Create spherical choropleth map
fig = px.choropleth(
    data_frame=map_df,
    locations="cuisine",
    locationmode="country names",
    color="dominant_cluster",
    color_discrete_map=color_map,
    category_orders={"dominant_cluster": ["1", "2", "3", "4"]},
    projection="orthographic",  # spherical globe view
)

fig.update_geos(
    showcoastlines=True,
    showland=True,
    landcolor="lightgray",
    oceancolor="lightblue",
    showocean=True,
    projection_rotation=dict(lon=0, lat=0),
    bgcolor='rgba(0,0,0,0)'
)

fig.update_layout(
    title_text="Dominant Recipe Cluster by Cuisine (Environmental Lens)",
    title_font_size=20,
    legend_title_text="Cluster",
    margin=dict(l=0, r=0, t=40, b=0),
    height=600
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)


st.markdown("""## Step 6 : Predictive modeling """)
st.markdown("""For predictive modeling, we'll consider two key environmental targets based on recipe and cuisine-level features.
#### Task 1: Predict `eco_score`  
- **Type**: Regression  
- **Goal**: Assess how well recipe-level features (e.g., ingredient semantics, luxury score, cuisine type) can estimate a recipe’s environmental footprint.""")

# Prepare features and target for eco_score prediction
features = ["Calories", "Fat", "Carbs", "Protein", "num_ingredients", "luxury_score"]
df_model = recipes_df.dropna(subset=features + ["eco_score"])

X = df_model[features]
y = df_model["eco_score"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation
rmse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Feature importance
importances = model.feature_importances_
feature_importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)


st.markdown("""
    We trained a **Random Forest Regressor** to predict the environmental footprint (**eco_score**, in kg CO₂-eq) of recipes using only basic **nutritional and structural features**: 
            
    ##### `Calories`, `Fat`, `Carbs`, `Protein`, `Number of Ingredients`, `Luxury Score` (count of high-impact ingredients)
    """)

# Streamlit Content
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ##### Model Performance:
    
    | Metric | Value |
    |--------|-------|
    | **R² Score**  | 0.55  |
    | **RMSE**      | 35.69 kg CO₂-eq |
    
    - The model explains about **55% of the variance** in eco scores.
    - An RMSE of ~36 suggests moderate prediction error on unseen data.
    """)

with col2:
    st.markdown("""
    ##### Feature Importance:
    
    | Rank | Feature          | Importance |
    |------|------------------|------------|
    | 1    | **Number of Ingredients** | 🟩 Highest |
    | 2    | Protein          | Significant |
    | 3-5   | Carbs, Fat, Calories  | Moderate |
    | 6  |  Luxury Score| Lower impact |
    
    - **Ingredient count** is the most predictive of carbon impact — confirming previous correlation and hypothesis results.
    - **Luxury score** has the least meaningful.
    """)

st.markdown("""
##### Conclusion:
Recipe-level environmental impact is **partially predictable** using nutrition and structure.
            """)