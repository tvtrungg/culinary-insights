import streamlit as st
import plotly.express as px
from plotly import figure_factory as ff
import plotly.express as px
from utils.data_loader import load_data
from utils.style import inject_css

data = load_data()
inject_css()

df_v2, df_v3, recipes_df = data[0], data[1], data[6]

st.markdown("# Dataset Overview")
st.write(
    """
    ## 1. Introduction
    In this section, we will describe the data and analyze it to understand the distribution of recipes across different continents and regions.
    - This dataset contains information about recipes from AllRecipes, including details such as recipe name, rating, dish type, ingredients, and nutritional information. 
    - The data is categorized by criteria such as geographic region and preparation time, offering an overview of popular recipes worldwide.
    - The dataset consists of 4,551 rows and 32 columns, reflecting the diversity of culinary recipes.
    - After several preprocessing steps, we have a clean dataset ready for analysis.
    """
)

st.write(df_v3.head(5))

st.markdown("""
## 2. Data Overview
### Dataset Description
**Shape**: 4551 entries x 32 columns  
**Memory Usage**: ~1.1+ MB

### Column Summary
<div style="max-height: 268px; overflow-y: auto; width: 100%;">
<pre>

| #   | Column                | Non-Null Count | Data Type |
|-----|-----------------------|----------------|-----------|
| 0   | `url`                 | 4551           | object    |
| 1   | `title`               | 4551           | object    |
| 2   | `steps`               | 4551           | object    |
| 3   | `rating`              | 4432           | float64   |
| 4   | `comments`            | 4551           | object    |
| 5   | `dish_type`           | 1317           | object    |
| 6   | `cuisine`             | 3843           | object    |
| 7   | `continent`           | 4551           | object    |
| 8   | `sub_region`          | 4551           | object    |
| 9   | `Calories`            | 4514           | float64   |
| 10  | `Fat`                 | 4551           | float64   |
| 11  | `Carbs`               | 4551           | float64   |
| 12  | `Protein`             | 4551           | float64   |
| 13  | `prep_time`           | 4551           | int64     |
| 14  | `cook_time`           | 4551           | int64     |
| 15  | `additional_time`     | 4551           | int64     |
| 16  | `total_time`          | 4551           | int64     |
| 17  | `servings`            | 4551           | float64   |
| 18  | `ingredients`         | 4551           | object    |
| 19  | `num_ingredients`     | 4551           | int64     |
| 20  | `num_steps`           | 4551           | int64     |
| 21  | `log_prep_time`       | 4551           | float64   |
| 22  | `log_cook_time`       | 4551           | float64   |
| 23  | `log_additional_time` | 4551           | float64   |
| 24  | `log_total_time`      | 4551           | float64   |
| 25  | `log_Calories`        | 4514           | float64   |
| 26  | `log_Fat`             | 4551           | float64   |
| 27  | `log_Carbs`           | 4551           | float64   |
| 28  | `log_Protein`         | 4551           | float64   |
| 29  | `ingredients_str`     | 4551           | object    |
| 30  | `ingredients_cleaned` | 4551           | object    |
| 31  | `ingredient_semantics`| 4551           | object    |

</pre>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------
st.markdown("## 3. Preprocessed ANOVA Data")

st.write(df_v2.head(5))

st.markdown("""
    ### Dataset Description
    **Shape**: 3843 entries x 16 columns  
    **Memory Usage**: ~510.4 KB

    ### Column Summary
    <div style="max-height: 268px; overflow-y: auto; width: 100%;">
    <pre>
            
    | #  | Column           | Non-Null Count | Data Type |
    |----|------------------|----------------|-----------|
    | 0  | `title`          | 3843           | object    |
    | 1  | `steps`          | 3843           | object    |
    | 2  | `rating`         | 3744           | float64   |
    | 3  | `cuisine`        | 3843           | object    |
    | 4  | `continent`      | 3843           | object    |
    | 5  | `sub_region`     | 3843           | object    |
    | 6  | `Calories`       | 3811           | float64   |
    | 7  | `Fat`            | 3843           | float64   |
    | 8  | `Carbs`          | 3843           | float64   |
    | 9  | `Protein`        | 3843           | float64   |
    | 10 | `prep_time`      | 3843           | int64     |
    | 11 | `cook_time`      | 3843           | int64     |
    | 12 | `additional_time`| 3843           | int64     |
    | 13 | `total_time`     | 3843           | int64     |
    | 14 | `servings`       | 3843           | float64   |
    | 15 | `ingredients`    | 3843           | object    |
            
    </pre>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------

st.markdown("### Data Analysis")
st.write(
    """
    In this section, we will analyze the dataset to understand the distribution of recipes across different continents and regions.
    We will create visualizations to represent the number of recipes per continent and region.
    """
)

# Create a 2-column layout
col1, col2 = st.columns(2)



# Plot 1: Number of Recipes per Continent
# Assuming df_v2 is your DataFrame
with col1:
    st.markdown("#### Number of Recipes per Continent")
    st.write(
        """
        This plot shows the number of recipes available in each continent.
        """
    )
    continent_counts = df_v2["continent"].value_counts().reset_index()
    continent_counts.columns = ["Continent", "Number of Recipes"]

    fig = px.bar(
        continent_counts,
        x="Continent",
        y="Number of Recipes",
        title="Number of Recipes per Continent",
        color_discrete_sequence=["red"]
    )

    fig.update_layout(
        xaxis_title="Continent",
        yaxis_title="Number of Recipes",
        height=500,
        width=1000,
        xaxis_tickangle=45
    )
    st.plotly_chart(fig)

with col2:
    st.markdown("#### Number of Recipes per Region")
    st.write(
        """
        This plot shows the number of recipes available in each region.
        """
    )
    # Plot 2: Number of Recipes per Region
    subregion_counts = df_v2["sub_region"].value_counts().reset_index()
    subregion_counts.columns = ["Sub Region", "Number of Recipes"]

    fig = px.bar(
        subregion_counts,
        x="Sub Region",
        y="Number of Recipes",
        title="Number of Recipes per Sub-Region",
        color_discrete_sequence=["red"]
    )

    fig.update_layout(
        xaxis_title="Sub Region",
        yaxis_title="Number of Recipes",
        height=500,
        width=1000,
        xaxis_tickangle=45
    )
    st.plotly_chart(fig)

# Plot 3: Number of Recipes per Cuisine
# Assuming df_v2 is your DataFrame
cuisine_counts = df_v2["cuisine"].value_counts().reset_index()
cuisine_counts.columns = ["Cuisine", "Number of Recipes"]

fig = px.bar(
    cuisine_counts,
    x="Cuisine",
    y="Number of Recipes",
    title="Number of Recipes per Cuisine",
    color_discrete_sequence=["red"]
)

fig.update_layout(
    xaxis_title="Cuisine",
    yaxis_title="Number of Recipes",
    height=500,
    width=1200,
    xaxis_tickangle=45
)
st.plotly_chart(fig)