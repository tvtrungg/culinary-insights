import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import linkage
import plotly.figure_factory as ff
sns.set_theme(style="whitegrid")

from utils.data_loader import load_cuisine_with_gdp_growth, load_cleaned_recipes3
from utils.style import inject_css

inject_css()

st.markdown("# Economic Axis")



cuisine_stats = load_cuisine_with_gdp_growth()
recipes_df = load_cleaned_recipes3()


st.write("## Cuisine with GDP growth - Overview")
st.write(cuisine_stats.head())

st.write("## Hypothesis 1: Does GDP growth correlate with an increase in culinary luxury?")
st.markdown("We test whether there is a positive correlation between GDP growth (2010-2022) and the average score of luxury ingredients per recipe (cheese, nuts, seafood, sweeteners).")

# Graph 1: GDP Growth vs. Luxury Score
fig1 = px.scatter(
    cuisine_stats,
    x="GDP_growth",
    y="avg_luxury_score",
    color="GDP_Class",
    title="GDP Growth vs. Luxury Score per Cuisine",
    labels={
        "GDP_growth": "GDP Growth (2010–2022)",
        "avg_luxury_score": "Average Luxury Score",
        "GDP_Class": "GDP Class"
    }
)
fig1.update_layout(
    title_font_size=28,
    title_x=0,
    font=dict(size=18),
    xaxis=dict(title_font=dict(size=20), tickfont=dict(size=16)),
    yaxis=dict(title_font=dict(size=20), tickfont=dict(size=16))
)
st.plotly_chart(fig1, use_container_width=True)


st.write("## Hypothesis 2: Do higher-income countries use more ingredients?")
st.markdown("We compare income classes (Low, Middle, High Income) based on the complexity of the recipes")
# Graph 2: Boxplot - Number of Ingredients by GDP Class
fig2 = px.box(
    cuisine_stats,
    x="GDP_Class",
    y="avg_total_ingredients",
    color="GDP_Class",
    points="all",
    labels={
        "GDP_Class": "GDP Class (2022)",
        "avg_total_ingredients": "Avg. Ingredients per Recipe"
    },
    title="Number of Ingredients per Recipe by GDP Class"
)
fig2.update_layout(
    title_font_size=28,
    title_x=0,
    font=dict(size=18),
    xaxis=dict(title_font=dict(size=20), tickfont=dict(size=16)),
    yaxis=dict(title_font=dict(size=20), tickfont=dict(size=16)),
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig2, use_container_width=True)


st.write("## Hypothesis 3: Is luxury more volatile in unstable economies?")
st.markdown("We explore whether countries with low or negative GDP growth have simpler recipes")
# Graph 3: GDP Growth vs Ingredient Richness
fig3 = px.scatter(
    cuisine_stats,
    x="GDP_growth",
    y="avg_total_ingredients",
    color="GDP_Class",
    hover_name="cuisine",  # Optional: use if you have a 'cuisine' column
    title="Economic Growth vs Ingredient Richness",
    labels={
        "GDP_growth": "GDP Growth (2010–2022)",
        "avg_total_ingredients": "Avg. Number of Ingredients",
        "GDP_Class": "GDP Class"
    }
)
fig3.update_layout(
    title_font_size=28,
    title_x=0,
    font=dict(size=18),
    xaxis=dict(title_font=dict(size=20), tickfont=dict(size=16)),
    yaxis=dict(title_font=dict(size=20), tickfont=dict(size=16)),
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig3, use_container_width=True)


st.title("Exploring the Link Between Economy and Cuisine")
st.markdown("""
## Hypothesis 1:
##### **"An increase in GDP is accompanied by a culinary upgrade."**

**Graph 1: GDP Growth vs. Luxury Score**

### What we see:
- The scatterplot is widely dispersed, with an almost flat slope.
- The average luxury score stays centered around 0.8 to 1, regardless of GDP growth.
- There are a few high outliers (score > 2.5) for countries with moderate growth.

### Interpretation:
There is no significant correlation between GDP growth from 2010 to 2022 and the use of so-called “luxury” ingredients (cheese, nuts, seafood, sweeteners).

This hypothesis appears **unconfirmed** within this timeframe and dataset.

**Possible explanation:** Culinary habits are culturally rooted, relatively insensitive to recent economic changes, or economic growth does not directly affect “popular” cuisine.


## Hypothesis 2:
##### **"Countries with economic stability have more consistent ingredient richness."**

**Graph 2: Boxplot - Number of Ingredients by GDP Class**

### What we see:
- Low-income countries have a higher average number of ingredients, with large variance.
- High-income countries have more homogeneous recipes (tight boxplot), with a lower median.
- Middle-income classes (Lower and Upper) show more diverse distributions but remain close to each other.

### Interpretation:
**Counterintuitive:** Rich countries do not necessarily have more ingredients in their recipes.

However, their culinary standardization seems stronger: more uniform recipes (less variance).

Low-income countries show great heterogeneity, possibly due to diverse regional cuisines.

✅ **Hypothesis partially validated:** Wealthy countries exhibit more **consistent** complexity, but not necessarily **higher**.


## Hypothesis 3:
##### **"During a crisis, culinary luxury decreases."**

**Graph 3: Scatterplot - GDP Growth vs Ingredient Richness**

### What we see:
- Countries with negative or stagnant growth do not systematically have fewer ingredients.
- There's a concentration around 8 to 13 ingredients, regardless of growth level.
- No clear trend by income class either: all colors are mixed.

### Interpretation:
Luxury ingredients don't seem directly impacted by economic crises (at least in the short/medium term).

Cuisine likely remains anchored in traditions, even during hard times.

This could be explored further by analyzing luxury trends over time (year by year), to detect possible drops tied to events (2008 crisis? COVID?).

**Hypothesis not confirmed** by this global data, but worth exploring with finer temporal granularity.

The link between **economy and cuisine** is neither linear nor immediate.

There are powerful **cultural, historical, and social** factors that influence cuisine independently of income.
""")

### Country and region axis
st.write("## Country and Region Axis")
sub_region_map = recipes_df[["cuisine", "sub_region"]].drop_duplicates()
# merge with cuisine_stats
cuisine_stats = cuisine_stats.merge(sub_region_map, on="cuisine", how="left")

st.write(cuisine_stats[["cuisine", "sub_region"]].head())

st.markdown("### Visualisations géographiques et économiques")

# Drop rows with missing sub-region
data = cuisine_stats.dropna(subset=["sub_region"])

# Boxplot: Luxury Score by Sub-Region
fig1 = px.box(
    data,
    x="sub_region",
    y="avg_luxury_score",
    color="sub_region",
    height=650,
    title="Luxury Ingredient Score by Sub-Region",
    labels={"sub_region": "Sub-Region", "avg_luxury_score": "Avg. Luxury Score"},
    points="all"
)
fig1.update_layout(
    title_font_size=28,
    title_x=0,
    font=dict(size=16),
    xaxis=dict(title_font=dict(size=18), tickfont=dict(size=14), tickangle=45),
    yaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
    showlegend=False,
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig1, use_container_width=True)

# Boxplot: Ingredient Richness by Sub-Region
fig2 = px.box(
    data,
    x="sub_region",
    y="avg_total_ingredients",
    color="sub_region",
    width=900,
    height=650,
    title="Recipe Ingredient Richness by Region",
    labels={"sub_region": "Sub-Region", "avg_total_ingredients": "Avg. Ingredients"},
    points="all"
)
fig2.update_layout(
    title_font_size=28,
    title_x=0,
    font=dict(size=16),
    xaxis=dict(title_font=dict(size=18), tickfont=dict(size=14), tickangle=45),
    yaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
    showlegend=False,
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig2, use_container_width=True)

# Countplot equivalent: GDP Class Distribution by Sub-Region
count_data = data.groupby(["sub_region", "GDP_Class"]).size().reset_index(name="count")
fig3 = px.bar(
    count_data,
    x="sub_region",
    y="count",
    color="GDP_Class",
    barmode="group",
    title="GDP Class Distribution by Region",
    labels={"sub_region": "Sub-Region", "count": "Number of Cuisines", "GDP_Class": "GDP Class"}
)
fig3.update_layout(
    title_font_size=28,
    title_x=0,
    font=dict(size=16),
    xaxis=dict(title_font=dict(size=18), tickfont=dict(size=14), tickangle=45),
    yaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig3, use_container_width=True)

# Scatterplot: GDP Growth vs Luxury Score by Sub-Region
fig4 = px.scatter(
    cuisine_stats.dropna(subset=["sub_region", "GDP_growth", "avg_luxury_score"]),
    x="GDP_growth",
    y="avg_luxury_score",
    color="sub_region",
    width=900,
    height=650,
    hover_name="cuisine" if "cuisine" in cuisine_stats.columns else None,
    title="GDP Growth vs Luxury Score by Region",
    labels={"GDP_growth": "GDP Growth (2010-2022)", "avg_luxury_score": "Avg. Luxury Score", "sub_region": "Sub-Region"}
)
fig4.update_layout(
    title_font_size=28,
    title_x=0,
    font=dict(size=16),
    xaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
    yaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig4, use_container_width=True)


# ============================

st.markdown("## Choropleth Maps: Economy & Cuisine")

# Choropleth Map: GDP Class by Country
fig1 = px.choropleth(
    cuisine_stats,
    locations="cuisine",
    locationmode="country names",
    color="GDP_Class",
    title="GDP Class by Country",
    color_discrete_map={
        "Low Income": "#d73027",
        "Lower-Middle Income": "#fc8d59",
        "Upper-Middle Income": "#fee08b",
        "High Income": "#1a9850",
        "Unknown": "lightgray"
    }
)
fig1.update_geos(
    projection_type="orthographic",  # Makes it look like a globe
    showcoastlines=True,
    showland=True,
    landcolor="lightgray",
    oceancolor="LightBlue",
    showocean=True
)

fig1.update_layout(
    title_font_size=28,
    title_x=0,
    height=500,
    margin={"r":0,"t":40,"l":0,"b":40},
    geo=dict(bgcolor='rgba(0,0,0,0)'),
    font=dict(size=16)
)

st.plotly_chart(fig1, use_container_width=True)

# Choropleth Map: Average Luxury Score by Country
st.markdown("## Average Luxury Score by Country")

fig2 = px.choropleth(
    cuisine_stats,
    locations="cuisine",
    locationmode="country names",
    color="avg_luxury_score",
    title="Average Luxury Score by Country (Globe View)",
    color_continuous_scale="Viridis",
    range_color=(0, cuisine_stats["avg_luxury_score"].max()),
    labels={"avg_luxury_score": "Luxury Score"}
)

fig2.update_geos(
    projection_type="orthographic",  # Spherical projection
    showcoastlines=True,
    showland=True,
    landcolor="lightgray",
    oceancolor="LightBlue",
    showocean=True,
    bgcolor='rgba(0,0,0,0)'
)

fig2.update_layout(
    title_font_size=28,
    title_x=0,
    height=500,
    margin={"r":0,"t":40,"l":0,"b":40},
    font=dict(size=16)
)

st.plotly_chart(fig2, use_container_width=True)


# PCA Economic & Culinary Dimensions
features = ["GDP_2022", "GDP_growth", "avg_total_ingredients", "avg_luxury_score"]
scaled = StandardScaler().fit_transform(cuisine_stats[features].fillna(0))
pca = PCA(n_components=2)
pca_coords = pca.fit_transform(scaled)

cuisine_stats["PCA1"] = pca_coords[:, 0]
cuisine_stats["PCA2"] = pca_coords[:, 1]

# Plotly scatter
fig_pca = px.scatter(
    cuisine_stats,
    x="PCA1",
    y="PCA2",
    color="GDP_Class",
    hover_name="cuisine",
    title="PCA of Economic & Culinary Dimensions",
    height=550
)
fig_pca.update_layout(
    title_font_size=28,
    title_x=0,
    margin=dict(l=20, r=20, t=60, b=20),
    legend_title_text="GDP Class",
    xaxis=dict(title_font=dict(size=18), tickfont=dict(size=16)),
    yaxis=dict(title_font=dict(size=18), tickfont=dict(size=16)),
)
st.plotly_chart(fig_pca, use_container_width=True)



# Clustering
features_for_clustering = [
    "GDP_2022", "GDP_growth", "avg_total_ingredients", "avg_luxury_score"
]
X_scaled = StandardScaler().fit_transform(cuisine_stats[features_for_clustering].fillna(0))
linkage_matrix = linkage(X_scaled, method="ward")

# Dendrogram
fig_dendro = ff.create_dendrogram(
    X_scaled,
    orientation='bottom',
    labels=cuisine_stats["cuisine"].values,
    linkagefun=lambda x: linkage_matrix,
    # colorscale=["#FFA500", "#00ff00", "#ff0000", "#0000ff"],
    colorscale=[
       "#0000ff",  # Blue
        "#d73027",  # Red
        "#FFA500",  # Orange
         "#FFA500",  # Orange
         "#91bfdb",  # Light Blue
        "#1a9850",  # Green
    ]
)

fig_dendro.update_layout(
    title="Hierarchical Clustering of Countries (Economic & Culinary)",
    height=700,
    title_font_size=28,
    title_x=0,
    font=dict(size=14),
    margin=dict(t=60, l=40, r=40, b=40)
)

st.plotly_chart(fig_dendro, use_container_width=True)


st.markdown("## What does this graph reveal?")

# 1. Global Structure
st.markdown("""
### 1. Global Structure

We observe **three main clusters** (represented by colored branches: orange, green, and red).

Each cluster groups together countries that are similar **across multiple dimensions**, not just one. These similarities could be economic, culinary, or both.
""")

# 2. Orange Group (Left)
st.markdown("""
---

### 2. Orange Group (Left)

This group includes many countries from **Africa, Central Asia, and Latin America**, such as:

- Zambia, Tanzania, Guatemala, Russia, etc.

These countries often share:

- **Low or medium GDP**
- **Rich and diverse culinary profiles**

**🟠 Interpretation:** Likely represents a group of countries with **"rich cuisine but uneven economic growth."**
""")

# 3. Green Group (Center)
st.markdown("""
---

### 3. Green Group (Center)

This cluster contains:

- Stable European countries: **Austria, Germany, Italy**
- Developed nations: **Canada, United States, Australia**

They tend to have:

- **Strong economies**
- **Consistently moderate culinary richness**

**🟢 Interpretation:** This cluster reflects **"economically developed countries with stable, balanced cuisines."**
""")

# 4. Red Group (Right)
st.markdown("""
---

### 4. Red Group (Right)

This includes countries like:

- **Thailand, Vietnam, Nigeria, Sri Lanka, Bangladesh**

Shared characteristics:

- **High culinary richness** (either in terms of ingredient diversity or luxury score)
- **Economic diversity** (ranging from emerging markets to fragile economies)

**🔴 Interpretation:** This group is notable for its **"culinary diversity despite contrasting economies."**
""")

# Key Interpretations / Hypotheses
st.markdown("""
---

## Key Interpretations / Validated Hypotheses

### Hypothesis 1  
**"Economically wealthy countries tend to share more homogeneous luxury culinary profiles."**  
**✅ Confirmed:** These countries cluster together in the **green group**, indicating strong internal coherence.

---

### Hypothesis 2  
**"Countries with very different economies can still share similar culinary traits."**  
**✅ Example:** Vietnam and Sri Lanka cluster near Thailand, despite economic differences → points to **shared cultural or culinary heritage**.

---

### Hypothesis 3  
**"Some countries exhibit outlier behavior."**  
**✅ Confirmed:** Countries like **Venezuela, Iran, and North Korea** are far from others in the dendrogram, possibly due to:

- **Unstable economic contexts**, or
- **Very distinct culinary profiles**
""")


df = pd.read_csv("data/cuisine_stats_with_sub_region_and_clusters.csv")

# Culinary Luxury Score by Cluster
fig_luxury = px.box(
    df,
    x="cluster",
    y="avg_luxury_score",
    color="cluster",
    title="Culinary Luxury Score by Cluster",
    color_discrete_sequence=px.colors.qualitative.Pastel,
    labels={"avg_luxury_score": "Luxury Score", "cluster": "Cluster"}
)
fig_luxury.update_layout(title_font_size=20, font=dict(size=14))
st.plotly_chart(fig_luxury, use_container_width=True)

# Ingredient Richness by Cluster
fig_ingredients = px.box(
    df,
    x="cluster",
    y="avg_total_ingredients",
    color="cluster",
    title="Ingredient Richness by Cluster",
    color_discrete_sequence=px.colors.qualitative.Set2,
    labels={"avg_total_ingredients": "Number of Ingredients", "cluster": "Cluster"}
)
fig_ingredients.update_layout(title_font_size=20, font=dict(size=14))
st.plotly_chart(fig_ingredients, use_container_width=True)

# GDP Growth by Cluster
fig_gdp_growth = px.box(
    df,
    x="cluster",
    y="GDP_growth",
    color="cluster",
    title="GDP Growth by Cluster",
    color_discrete_sequence=px.colors.qualitative.Pastel,
    labels={"GDP_growth": "GDP Growth (%)", "cluster": "Cluster"}
)
fig_gdp_growth.update_layout(title_font_size=20, font=dict(size=14))
st.plotly_chart(fig_gdp_growth, use_container_width=True)


import streamlit as st

st.markdown("### Cluster Characteristics")

# 1. Culinary Luxury Score
st.markdown("#### 1. Culinary Luxury Score per Cluster")
st.markdown("""
The boxplot for `avg_luxury_score` reveals three distinct culinary profiles:

- **Cluster 1**: Lower luxury scores, suggesting simpler or more modest cuisines. Countries in this group likely use fewer luxury ingredients like seafood, nuts, and dairy.
- **Cluster 2**: Higher luxury averages and broad variability, suggesting a mix of traditional richness and modern economic adaptation.
- **Cluster 3**: Also high in luxury scores, but slightly more concentrated. This could reflect countries where culinary refinement is embedded in cultural identity despite varying economic profiles.
""")

# 2. Ingredient Richness
st.markdown("#### 2. Ingredient Richness per Cluster")
st.markdown("""
The average number of ingredients per recipe reflects culinary complexity:

- **Cluster 3** leads clearly, suggesting cuisines with more elaborate recipes.
- **Clusters 1 and 2** show similar, more modest ingredient counts, possibly due to constraints in availability, tradition, or simplicity in preparation styles.
""")

# 3. GDP Growth
st.markdown("#### 3. GDP Growth per Cluster")
st.markdown("""
The economic growth trend aligns with some of our expectations:

- **Cluster 3** appears as the most economically dynamic, with the highest median GDP growth.
- **Cluster 2** is the most economically stable but less growth-intensive—this might contain developed nations.
- **Cluster 1** includes low-growth and even negative-growth economies, which could explain the simpler culinary expressions observed.
""")
# Grouped Bar Chart: GDP Class Distribution by Cluster
fig = px.histogram(
    df,
    x="cluster",
    color="GDP_Class",
    barmode="group",
    title="Distribution of GDP Classes by Cluster",
    color_discrete_sequence=px.colors.qualitative.Set2,
    category_orders={"cluster": sorted(df["cluster"].unique())}
)

fig.update_layout(
    title_font_size=24,
    xaxis_title="Cluster",
    yaxis_title="Number of Countries",
    font=dict(size=14),
    bargap=0.15,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    legend_title="GDP Class",
    margin=dict(t=60, b=40, l=40, r=40)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("#### 4. GDP Class Distribution")

st.markdown("""
This categorical breakdown confirms the composition of the clusters:

- **Cluster 1**: A mix of **low-income** and **lower-middle-income** countries.
  
- **Cluster 2**: Largely composed of **high-income** nations, which aligns with their economic stability and high culinary luxury scores.

- **Cluster 3**: The most **economically diverse** cluster, yet countries in this group share rich and complex culinary traditions—suggesting that **economic growth**, not just absolute wealth, may be a key driver of culinary development.
""")

# Choropleth Map of Clusters
fig = px.choropleth(
    df,
    locations="cuisine",
    locationmode="country names",
    color="cluster",
    title="Map of Countries by Economic & Culinary Cluster",
    color_continuous_scale=px.colors.qualitative.Set2
)

fig.update_geos(
    projection_type="orthographic",  # Makes the map look like a globe
    showcoastlines=True,
    showland=True,
    showocean=True,
    oceancolor="LightBlue",
    landcolor="whitesmoke",
    showcountries=True,
    showframe=False,
    bgcolor='rgba(0,0,0,0)'
)

fig.update_layout(
    title_font_size=28,
    margin={"r":0,"t":50,"l":0,"b":0},
    height=500
)

st.plotly_chart(fig, use_container_width=True)


# Explanatory Text
st.markdown("### Geographic Distribution of Clusters")

st.markdown("""
The choropleth map clearly visualizes global patterns of culinary and economic clustering:

- **Cluster 1**: Countries often located in **Sub-Saharan Africa** and **parts of South Asia**. These nations generally show modest economic performance and simpler culinary traditions.

- **Cluster 2**: Dominated by **high-income countries** with long-standing culinary richness, such as **Western Europe**, **North America**, and **Japan**.

- **Cluster 3**: A diverse mix of **emerging economies** with vibrant and rich cuisines—especially in **Latin America** and **Southeast Asia**—suggesting a strong connection between **economic ambition** and **culinary complexity**.

---

### Key Takeaways

- **Culinary luxury** and **ingredient richness** are influenced not only by income levels but also by **economic growth and regional traditions**.

- **Cluster 3** demonstrates that **wealth alone doesn’t define cuisine**. These countries may be growing economically but already exhibit complex culinary identities.

- The **geographic visualization** highlights consistent patterns, with **Asia and Latin America** standing out as culturally dynamic regions.

- The **hierarchical clustering approach** offers a powerful lens to categorize and compare world cuisines using a data-driven framework.
""")