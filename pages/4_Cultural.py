import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from utils.style import inject_css


import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid")

inject_css()

st.markdown("# Ingredients Analysis on Cultural Diversity")

recipes_df_with_hofstede = pd.read_csv("data/recipes_df_with_hofstede.csv", index_col=0)

st.write("## Hofstede Cultural Dimensions - Overview")
st.write(recipes_df_with_hofstede.head())

st.write(
    "The **Hofstede cultural framework** quantifies national cultures using six dimensions. "
    "These metrics can offer valuable context when analyzing how culture influences food systems, "
    "cooking styles, and dietary choices."
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Key Cultural Dimensions")
    st.markdown("- **PDI (Power Distance Index)**  \n"
                "Measures the acceptance of unequal power distribution in society. High PDI countries may have more "
                "hierarchical food traditions or social norms around who cooks and eats what.")
    
    st.markdown("- **IDV (Individualism)**  \n"
                "Reflects the degree to which individuals are integrated into groups. In highly individualistic cultures, "
                "food choices may be more personalized and diverse, while collectivist cultures may emphasize shared, "
                "family-style meals.")
    
    st.markdown("- **MAS (Masculinity)**  \n"
                "Indicates whether a society values competitiveness and achievement (masculine) versus care and quality "
                "of life (feminine). This could influence preferences for hearty, protein-rich foods vs. balanced, "
                "health-conscious diets.")

with col2:
    st.markdown("### ")
    st.markdown("- **UAI (Uncertainty Avoidance Index)**  \n"
                "Captures a society’s tolerance for ambiguity. High UAI may relate to more structured food traditions, "
                "recipes, and aversion to trying unfamiliar ingredients.")
    
    st.markdown("- **LTO (Long-Term Orientation)**  \n"
                "Assesses a society’s focus on future rewards vs. tradition. Cultures with long-term orientation may "
                "adopt sustainable, evolving food practices.")
    
    st.markdown("- **IVR (Indulgence vs. Restraint)**  \n"
                "Describes the degree of freedom in fulfilling human desires. Indulgent cultures may show more openness "
                "to rich, luxurious, or experimental cuisines.")

# List of Hofstede dimensions
hofstede_dimensions = ["pdi", "idv", "mas", "uai", "ltowvs", "ivr"]

# distributions of each Hofstede dimension
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 10))
axes = axes.flatten()

for i, dim in enumerate(hofstede_dimensions):
    sns.histplot(recipes_df_with_hofstede[dim].dropna(), kde=True, ax=axes[i], color="teal")
    axes[i].set_title(f"{dim.upper()} Distribution")
    axes[i].set_xlabel(dim.upper())
    axes[i].set_ylabel("Frequency")

plt.suptitle("Distribution of Hofstede Cultural Dimensions", fontsize=16, y=1.03)
plt.tight_layout()
st.pyplot(fig)


st.markdown(
    "## Cultural Analysis : Grouping By Quantiles"
)

quartile_df = recipes_df_with_hofstede.dropna(subset=["idv", "eco_score", "num_ingredients", "luxury_score"])

# Bin countries into 4 cultural quartiles based on IDV
quartile_df["idv_quartile"] = pd.qcut(quartile_df["idv"], 4, labels=["Q1 (Low)", "Q2", "Q3", "Q4 (High)"])

# Group by quartile and calculate average culinary traits
quartile_means = quartile_df.groupby("idv_quartile").agg({
    "eco_score": "mean",
    "num_ingredients": "mean",
    "luxury_score": "mean"
}).round(2).reset_index()

st.write(quartile_means)

st.markdown("### Key Observations Across IDV Quartiles")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### 🟩 Q3 Cultures  
    *Moderate to High Individualism*
    
    - 🥩 **Highest luxury scores**  
    - 🍲 **Highest ingredient complexity**  
    - 🌱 **Highest Eco Scores**  
    - ➕ Balanced richness with environmental awareness
    """)

with col2:
    st.markdown("""
    #### 🟦 Q4 Cultures  
    *Most Individualist*
    
    - 🧂 **Fewest ingredients**  
    - 🍽️ **High luxury scores**  
    - 🍷 Preference for **gourmet minimalism**
    """)

with col3:
    st.markdown("""
    #### 🟨 Q2 Cultures  
    *Moderate Individualism*
    
    - 🥕 **Modest ingredient use**  
    - ♻️ **Lower environmental impact**  
    - ⚖️ Balanced, **less indulgent culinary style**
    """)

# Plotting boxplots of culinary traits across IDV quartiles
# Boxplot 1: Eco Score by IDV Quartile
fig_eco = px.box(
    quartile_df,
    x="idv_quartile",
    y="eco_score",
    color="idv_quartile",
    title="Eco Score by IDV Quartile",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_eco.update_layout(
    xaxis_title="IDV Quartile",
    yaxis_title="Eco Score",
    showlegend=False
)

# Boxplot 2: Number of Ingredients by IDV Quartile
fig_ingredients = px.box(
    quartile_df,
    x="idv_quartile",
    y="num_ingredients",
    color="idv_quartile",
    title="Ingredient Complexity by IDV Quartile",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_ingredients.update_layout(
    xaxis_title="IDV Quartile",
    yaxis_title="Number of Ingredients",
    showlegend=False
)

# Boxplot 3: Luxury Score by IDV Quartile
fig_luxury = px.box(
    quartile_df,
    x="idv_quartile",
    y="luxury_score",
    color="idv_quartile",
    title="Luxury Score by IDV Quartile",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_luxury.update_layout(
    xaxis_title="IDV Quartile",
    yaxis_title="Luxury Ingredient Score",
    showlegend=False
)

col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(fig_eco, use_container_width=True)

with col2:
    st.plotly_chart(fig_ingredients, use_container_width=True)

with col3:
    st.plotly_chart(fig_luxury, use_container_width=True)

st.markdown("""## Indulgence vs. Restraint
""")
# Filter rows with valid IVR and culinary data
ivr_df = recipes_df_with_hofstede.dropna(subset=["ivr", "eco_score", "num_ingredients", "luxury_score"])

# Create IVR quartile labels
ivr_df["ivr_quartile"] = pd.qcut(ivr_df["ivr"], 4, labels=["Q1 (Low)", "Q2", "Q3", "Q4 (High)"])

# Group and average by IVR quartile
ivr_means = ivr_df.groupby("ivr_quartile").agg({
    "eco_score": "mean",
    "num_ingredients": "mean",
    "luxury_score": "mean"
}).round(2).reset_index()

st.write(ivr_means)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""##### Q4 – More Indulgent Cultures
Contrary to expectations, the **most indulgent cultures** (Q4) exhibit:
- **Lower ingredient complexity**
- **Lower luxury ingredient usage**
- **Lower environmental impact (eco footprint)**""")

with col2: 
    st.markdown("""
##### Q1 – More Restrained Cultures
More **restrained societies** (Q1) tend to show:
- **Higher culinary complexity**
- **Greater use of luxury ingredients**
- **Higher eco scores**, indicating more resource-intensive food practices
""")
    
# Boxplot 1: Eco Score by IVR Quartile
fig_eco = px.box(
    ivr_df,
    x="ivr_quartile",
    y="eco_score",
    color="ivr_quartile",
    title="Eco Score by IVR Quartile",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_eco.update_layout(
    xaxis_title="IVR Quartile",
    yaxis_title="Eco Score",
    showlegend=False
)

# Boxplot 2: Number of Ingredients by IVR Quartile
fig_ingredients = px.box(
    ivr_df,
    x="ivr_quartile",
    y="num_ingredients",
    color="ivr_quartile",
    title="Ingredient Complexity by IVR Quartile",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_ingredients.update_layout(
    xaxis_title="IVR Quartile",
    yaxis_title="Number of Ingredients",
    showlegend=False
)

# Boxplot 3: Luxury Score by IVR Quartile
fig_luxury = px.box(
    ivr_df,
    x="ivr_quartile",
    y="luxury_score",
    color="ivr_quartile",
    title="Luxury Score by IVR Quartile",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_luxury.update_layout(
    xaxis_title="IVR Quartile",
    yaxis_title="Luxury Ingredient Score",
    showlegend=False
)

# Display in three Streamlit columns
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(fig_eco, use_container_width=True)

with col2:
    st.plotly_chart(fig_ingredients, use_container_width=True)

with col3:
    st.plotly_chart(fig_luxury, use_container_width=True)

st.markdown("""## Power Distance Index (PDI)
""")
# Filter for valid PDI and culinary metrics
pdi_df = recipes_df_with_hofstede.dropna(subset=["pdi", "eco_score", "num_ingredients", "luxury_score"])

# Create quartile groups for PDI
pdi_df["pdi_quartile"] = pd.qcut(pdi_df["pdi"], 4, labels=["Q1 (Low)", "Q2", "Q3", "Q4 (High)"])

# Group and compute mean values
pdi_means = pdi_df.groupby("pdi_quartile").agg({
    "eco_score": "mean",
    "num_ingredients": "mean",
    "luxury_score": "mean"
}).round(2).reset_index()

st.write(pdi_means)

st.markdown("""
- **Q4 (High PDI) cultures** — where hierarchy is emphasized — prepare the **most complex and eco-intensive recipes**.

- **Q1 (Low PDI) cultures** are **simpler and lighter** in ingredient count.

- **Luxury score** does **not follow a clear linear trend**, but **peaks in Q3**.
            """)

# Eco Score by PDI Quartile
fig_eco = px.box(
    pdi_df,
    x="pdi_quartile",
    y="eco_score",
    color="pdi_quartile",
    title="Eco Score by PDI Quartile",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_eco.update_layout(xaxis_title="PDI Quartile", yaxis_title="Eco Score", showlegend=False)

# Ingredient Count by PDI Quartile
fig_ingredients = px.box(
    pdi_df,
    x="pdi_quartile",
    y="num_ingredients",
    color="pdi_quartile",
    title="Ingredient Complexity by PDI Quartile",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_ingredients.update_layout(xaxis_title="PDI Quartile", yaxis_title="Number of Ingredients", showlegend=False)

# Luxury Score by PDI Quartile
fig_luxury = px.box(
    pdi_df,
    x="pdi_quartile",
    y="luxury_score",
    color="pdi_quartile",
    title="Luxury Score by PDI Quartile",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_luxury.update_layout(xaxis_title="PDI Quartile", yaxis_title="Luxury Ingredient Score", showlegend=False)

# Display in Streamlit columns
col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(fig_eco, use_container_width=True)
with col2:
    st.plotly_chart(fig_ingredients, use_container_width=True)
with col3:
    st.plotly_chart(fig_luxury, use_container_width=True)


st.markdown("""## Uncertainty Avoidance Index (UAI)
""")
uai_df = recipes_df_with_hofstede.dropna(subset=["uai", "eco_score", "num_ingredients", "luxury_score"]).copy()

uai_df["uai_quartile"] = pd.qcut(uai_df["uai"], 4, labels=["Q1 (Low)", "Q2", "Q3", "Q4 (High)"])

uai_means = uai_df.groupby("uai_quartile").agg({
    "eco_score": "mean",
    "num_ingredients": "mean",
    "luxury_score": "mean"
}).round(2).reset_index()
st.write(uai_means)
# Eco Score
fig_eco = px.box(
    uai_df,
    x="uai_quartile",
    y="eco_score",
    color="uai_quartile",
    title="Eco Score by UAI Quartile",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_eco.update_layout(xaxis_title="UAI Quartile", yaxis_title="Eco Score", showlegend=False)

# Ingredient Complexity
fig_ingredients = px.box(
    uai_df,
    x="uai_quartile",
    y="num_ingredients",
    color="uai_quartile",
    title="Ingredient Complexity by UAI Quartile",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_ingredients.update_layout(xaxis_title="UAI Quartile", yaxis_title="Number of Ingredients", showlegend=False)

# Luxury Score
fig_luxury = px.box(
    uai_df,
    x="uai_quartile",
    y="luxury_score",
    color="uai_quartile",
    title="Luxury Score by UAI Quartile",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_luxury.update_layout(xaxis_title="UAI Quartile", yaxis_title="Luxury Ingredient Score", showlegend=False)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### ♻️ Eco Score  
    - **Q1 (Low UAI)**: Highest environmental impact  
    - **Q4 (High UAI)**: Drop in eco score  
    - 🌍 Suggests environmentally modest cuisines in risk-averse cultures
    """)

with col2:
    st.markdown("""
    ### 🍲 Ingredient Complexity  
    - Gradual **decline** as UAI increases  
    - **Q1**: Most complex recipes  
    - ✨ May reflect openness to experimentation
    """)

with col3:
    st.markdown("""
    ### 🧂 Luxury Score  
    - Sharp **drop in Q4**  
    - High UAI cultures likely **avoid extravagant or unfamiliar ingredients**  
    - ➖ Simpler, safer culinary choices
    """)

# Display in Streamlit columns
col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(fig_eco, use_container_width=True)
with col2:
    st.plotly_chart(fig_ingredients, use_container_width=True)
with col3:
    st.plotly_chart(fig_luxury, use_container_width=True)

# Filter and prepare for correlation analysis
corr_culture_df = recipes_df_with_hofstede[
    ["eco_score", "num_ingredients", "luxury_score", "Calories", "Fat", "Carbs", "Protein",
     "pdi", "idv", "mas", "uai", "ltowvs", "ivr"]
].dropna()

# Compute correlation matrix
correlation_matrix = corr_culture_df.corr().round(2)

# Convert matrix to long-form for Plotly
corr_long = correlation_matrix.reset_index().melt(id_vars="index")
corr_long.columns = ["Feature1", "Feature2", "Correlation"]

# Plotly heatmap
fig = px.imshow(
    correlation_matrix,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    zmin=-1, zmax=1,
    labels=dict(x="Feature", y="Feature", color="Correlation")
)
fig.update_layout(
    title="Correlation Between Cultural and Culinary Features",
    xaxis_side="bottom",
    width=800,
    height=700
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Cultural Traits and Culinary Correlations

| Cultural Trait              | Positive Correlation     | Negative Correlation     | Interpretation                                         |
|----------------------------|--------------------------|--------------------------|--------------------------------------------------------|
| **IDV (Individualism)**     | Fat, Calories             | Number of Ingredients     | More indulgent but simpler dishes                     |
| **IVR (Indulgence)**        | Fat, Luxury               | Complexity                | Indulgence relates to richer but simpler meals        |
| **UAI (Uncertainty Avoidance)** | None strong             | Eco Score, Fat            | Avoidant cultures are more restrained                 |
| **LTO (Long-Term Orientation)** | Complexity             | None major                | Long-term cultures may favor tradition and rich dishes|
| **PDI (Power Distance)**    | Ingredient Count          | None strong               | Hierarchical cultures may favor formal complexity     |
""")

st.markdown("""## Cultural-culinary clustering """)

# Features for clustering at the recipe level
features = [
    "eco_score", "Calories", "Fat", "Carbs", "Protein",
    "num_ingredients", "luxury_score",
    "pdi", "idv", "mas", "uai", "ltowvs", "ivr"
]

# Keep all rows with complete feature data, but preserve metadata
df_valid = recipes_df_with_hofstede.dropna(subset=features).copy()

# Scale only the selected features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_valid[features])

# Elbow Method to determine optimal k
inertia = []
K_range = range(1, 10)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

col1, col2 = st.columns(2)
with col1:
    # Plot Elbow
    elbow_fig = go.Figure()
    elbow_fig.add_trace(go.Scatter(
        x=list(K_range),
        y=inertia,
        mode='lines+markers',
        marker=dict(color='mediumslateblue'),
        line=dict(width=2),
    ))
    elbow_fig.update_layout(
        title="Elbow Method to Determine Optimal k",
        title_font_size=24,
        xaxis_title="Number of Clusters (k)",
        yaxis_title="Inertia",
        height=600
    )
    st.plotly_chart(elbow_fig, use_container_width=True)

# PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

optimal_k = 4
kmeans_final = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
clusters = kmeans_final.fit_predict(X_scaled)

df_clust_result = df_valid.copy()
df_clust_result["PCA1"] = X_pca[:, 0]
df_clust_result["PCA2"] = X_pca[:, 1]
df_clust_result["cluster"] = clusters + 1

with col2:
    # PCA scatter plot
    fig = px.scatter(
        df_clust_result,
        x="PCA1",
        y="PCA2",
        color="cluster",
        title="PCA of Recipes (Culinary + Cultural Features)",
        color_discrete_sequence=px.colors.qualitative.Set2,
        hover_data=["cuisine"],  # Optional: show country name or any metadata
        template="plotly_white"
    )

    fig.update_traces(marker=dict(size=10, line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(
        title_font_size=24,
        legend_title_text="Cluster",
        height=600,
        margin=dict(l=20, r=20, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)


# Profile each cluster by averaging values
cluster_profile = df_clust_result.groupby("cluster")[features].mean().round(2)
cluster_profile["count"] = df_clust_result["cluster"].value_counts().sort_index()

st.write(cluster_profile)

# Compute the dominant cluster per cuisine
country_clusters = (
    df_clust_result.groupby("cuisine")["cluster"]
    .agg(lambda x: x.value_counts().index[0])
    .reset_index()
    .rename(columns={"cluster": "dominant_cluster"})
)

# Merge back metadata for geographic mapping
country_clusters = country_clusters.merge(
    df_clust_result[["cuisine", "code_3", "continent", "sub_region"]].drop_duplicates(),
    on="cuisine",
    how="left"
)


st.write(country_clusters)

country_clusters["dominant_cluster"] = country_clusters["dominant_cluster"].astype(str)
color_map = {
    "1": "#66C2A5",  # green
    "2": "#FC8D62",  # orange
    "3": "#8DA0CB",  # blue/purple
    "4": "#E78AC3"   # pink
}

fig = px.choropleth(
    data_frame=country_clusters,
    locations="code_3",               # ISO 3-letter country codes
    locationmode="ISO-3",
    color="dominant_cluster",
    hover_name="cuisine",
    color_discrete_map=color_map,
    projection="orthographic",       # <- Change this to orthographic for globe effect
    title="Dominant Cultural-Culinary Cluster by Country"
)

fig.update_geos(
    showcoastlines=True,
    showland=True,
    landcolor="lightgray",
    oceancolor="lightblue",
    showocean=True,
    showframe=False,
    projection_rotation=dict(lon=0, lat=0),  # Optional: Adjust rotation to center globe
    bgcolor='rgba(0,0,0,0)',

)

fig.update_layout(
    title_font_size=28,
    legend_title_text="Cluster",
    margin={"r": 0, "t": 52, "l": 0, "b": 20},
    height=700,
)

st.plotly_chart(fig, use_container_width=True)


# Make sure "continent" and "dominant_cluster" are categorical
country_clusters["continent"] = country_clusters["continent"].astype(str)
country_clusters["dominant_cluster"] = country_clusters["dominant_cluster"].astype(str)

# Plotly bar chart
fig = px.histogram(
    country_clusters,
    x="continent",
    color="dominant_cluster",
    barmode="group",
    title="Cultural-Culinary Clusters by Continent",
    labels={"continent": "Continent", "dominant_cluster": "Cluster"},
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig.update_layout(
    xaxis_title="Continent",
    yaxis_title="Number of Cuisines",
    legend_title="Cluster",
    bargap=0.2
)

# Show in Streamlit
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Cluster 1 (Green)")
    st.markdown("""
    - Primarily found in **Europe** and parts of the **Americas**  
    - Represents cuisines with **moderate eco and nutritional traits**  
    - Reflects **balanced cultural dimensions**
    """)

    st.markdown("### Cluster 2 (Orange)")
    st.markdown("""
    - Mostly concentrated in **Asia**  
    - Likely includes **complex, eco-aware cuisines**  
    - Associated with **collectivist or hierarchical** cultures
    """)

with col2:
    st.markdown("### Cluster 3 (Blue)")
    st.markdown("""
    - Scattered across **Africa**, **Asia**, and **Europe** in low numbers  
    - Possibly denotes **rich, indulgent cuisines**  
    - High in **calories and protein**
    """)

    st.markdown("### Cluster 4 (Pink)")
    st.markdown("""
    - The most **globally represented** cluster  
    - Dominant in the **Americas** and **Asia**  
    - Suggests **minimalist or adaptable cuisines**  
    - Characterized by **lower luxury scores** and **moderate eco impact**
    """)


st.markdown("""## Cluster profile classification """)
import streamlit as st
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Define features and target
features = [
    "Calories", "Fat", "Carbs", "Protein",
    "num_ingredients", "luxury_score",
    "pdi", "idv", "mas", "uai", "ltowvs", "ivr"
]
X = df_clust_result[features]
y = df_clust_result["cluster"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.25, random_state=42)

# Train Random Forest
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Classification Report
report = classification_report(y_test, y_pred, output_dict=True)
report_df = pd.DataFrame(report).transpose().round(2)

# Display Classification Report
st.markdown("### Classification Report")
st.dataframe(report_df)

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
labels = [str(cls) for cls in sorted(y.unique())]

fig_cm = ff.create_annotated_heatmap(
    z=cm,
    x=labels,
    y=labels,
    colorscale='Blues',
    showscale=True,
    annotation_text=cm.astype(str),
    hoverinfo="z"
)
fig_cm.update_layout(
    title="Confusion Matrix: Cluster Prediction",
    xaxis_title="Predicted",
    yaxis_title="Actual"
)

st.markdown("### Confusion Matrix")
st.plotly_chart(fig_cm, use_container_width=True)

# Get and prepare feature importances
importances = model.feature_importances_
feature_importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

# Plot feature importance using Plotly
fig_feature_importance = px.bar(
    feature_importance_df,
    x="Importance",
    y="Feature",
    orientation="h",
    title="Feature Importance for Cluster Prediction",
    color="Importance",
    color_continuous_scale="Cividis",
    labels={"Importance": "Feature Importance", "Feature": "Features"}
)

# Display in Streamlit
st.markdown("### Feature Importances")
st.plotly_chart(fig_feature_importance, use_container_width=True)

# Show feature importance table
st.markdown("### Feature Importance Table")
st.dataframe(feature_importance_df.reset_index(drop=True))

st.markdown("""##### Top Features Driving Cluster Assignment

| Rank | Feature             | Importance | Interpretation                                                                 |
|------|---------------------|------------|---------------------------------------------------------------------------------|
| 1️⃣   | Calories            | 17.2%      | Caloric density is a key driver — helps distinguish heavy vs. light cuisines.   |
| 2️⃣   | PDI (Power Distance)| 17.0%      | Cultural hierarchy influences how cuisines cluster — possibly tied to food norms. |
| 3️⃣   | IDV (Individualism) | 13.2%      | Openness and independence shape culinary complexity and expression.             |
| 4️⃣   | Num Ingredients     | 10.2%      | Ingredient richness is a strong cluster discriminator.                          |
| 5️⃣   | UAI (Uncertainty Avoidance) | 9.3% | Risk tolerance in culture may affect improvisation and recipe diversity.        |


##### Notably Lower Impact

- **MAS (Masculinity)**: 1.8%  
  Suggests assertiveness or competition values have **minimal influence** on culinary clustering.

- **Luxury Score**: 3.5%  
  Despite being intuitively important, it contributes less — likely **overlapping with calories or complexity**.


The model shows that **both cultural values and culinary metrics** (like calories and complexity) play a significant role in determining cultural-culinary cluster membership.

- Strongest predictors: **Calories, Power Distance (PDI), and Individualism (IDV)**
- This supports the idea that culinary clusters reflect **nutritional patterns and sociocultural structure** together.
""")

st.markdown("""## Eco score prediction """)

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Define features and target
features = [
    "Calories", "Fat", "Carbs", "Protein",
    "num_ingredients", "luxury_score",
    "pdi", "idv", "mas", "uai", "ltowvs", "ivr"
]
target = "eco_score"

# Assume df is your dataframe that has the relevant data
X = df_clust_result[features]
y = df_clust_result[target]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Train the RandomForestRegressor
regressor = RandomForestRegressor(random_state=42)
regressor.fit(X_train, y_train)

# Predictions and evaluation
y_pred = regressor.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Display model evaluation metrics in Streamlit
st.markdown("### Model Evaluation: Random Forest Regressor")
st.write(f"**Mean Squared Error (MSE)**: {mse:.2f}")
st.write(f"**R-squared (R²)**: {r2:.2f}")

# Feature importance for Eco Score Prediction
eco_importances = regressor.feature_importances_
eco_feature_importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": eco_importances
}).sort_values(by="Importance", ascending=False)

# Plot feature importance using Plotly
fig_eco_importance = px.bar(
    eco_feature_importance_df,
    x="Importance",
    y="Feature",
    orientation="h",
    title="Feature Importance for Eco Score Prediction",
    color="Importance",
    color_continuous_scale="Blues",
    labels={"Importance": "Feature Importance", "Feature": "Features"}
)

# Display the feature importance plot
st.plotly_chart(fig_eco_importance, use_container_width=True)

# Display feature importance table
st.markdown("### Feature Importance Table")
st.dataframe(eco_feature_importance_df.reset_index(drop=True))


# Luxury score prediction
st.markdown("""## Luxury score prediction""")
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load your DataFrame (ensure it's already loaded as 'df' with correct features)
# features_corrected = [
#     "Calories", "Fat", "Carbs", "Protein", "num_ingredients", 
#     "pdi", "idv", "mas", "uai", "ltowvs", "ivr"
# ]
features_corrected = [
    "Calories", "Fat", "Carbs", "Protein", "num_ingredients",
    "pdi", "idv", "mas", "uai", "ltowvs", "ivr"
]
X = df_clust_result[features_corrected]
y = df_clust_result["luxury_score"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Train model
lux_model_corrected = RandomForestRegressor(random_state=42)
lux_model_corrected.fit(X_train, y_train)

# Evaluate
y_pred = lux_model_corrected.predict(X_test)
mse_lux_fixed = mean_squared_error(y_test, y_pred)
r2_lux_fixed = r2_score(y_test, y_pred)

# Feature importance
lux_importances_fixed = lux_model_corrected.feature_importances_
lux_feature_importance_df_fixed = pd.DataFrame({
    "Feature": features_corrected,
    "Importance": lux_importances_fixed
}).sort_values(by="Importance", ascending=False)

# Plotly Bar Plot for Feature Importance
fig = px.bar(lux_feature_importance_df_fixed, 
             x="Importance", y="Feature", 
             orientation="h", 
             color="Importance", 
             color_continuous_scale="bluered",
             labels={"Importance": "Feature Importance", "Feature": "Features"},
             title="Feature Importance for Luxury Score Prediction (Corrected)")

# Streamlit Display
st.write("### Random Forest Regressor - Luxury Score Prediction")
st.write(f"**Mean Squared Error (MSE):** {mse_lux_fixed:.4f}")
st.write(f"**R-squared (R²):** {r2_lux_fixed:.4f}")
st.plotly_chart(fig)


# 4. Cultural Value Prediction (Country-Level Regression)

st.markdown("""## Cultural Value Prediction""")
st.markdown("""
| Target | R² Score | Top Predictive Features | Conclusion |
|--------|----------|--------------------------|------------|
| **UAI** (Uncertainty Avoidance) | -0.35 | luxury_score, num_ingredients | ❌ Not predictable from food |
| **IDV** (Individualism)         | 0.03  | luxury_score, protein         | ❌ Weak link to culinary profile |
| **PDI** (Power Distance)        | -0.11 | luxury_score, protein, eco_score | ❌ Very weak — cultural values transcend food data |
""")

st.write("### Final Thoughts")

st.markdown("""
- **Clusters and eco metrics** are the most predictable, food clearly reflects regional practices and environmental impact.
- **Cultural values** like PDI, UAI, and IDV are harder to model — they involve psychology, history, and societal systems beyond cuisine.
- Nonetheless, we uncovered subtle signals: luxurious, high-protein, and complex recipes **correlate loosely** with individualism and power dynamics.

This modeling validated some clustering logic and revealed the **limits** of inferring deep cultural traits from food alone.
""")
            
