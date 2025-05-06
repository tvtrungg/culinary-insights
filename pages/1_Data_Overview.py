import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from utils.style import inject_css
from utils.data_loader import load_cleaned_recipes_v2, load_cleaned_recipes3, load_recipes_df

inject_css()

df_v2 = load_cleaned_recipes_v2()
df_v3 = load_cleaned_recipes3()
recipes_df = load_recipes_df()

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

col2, col3= st.columns((1,2))
with col2: 

    st.markdown("""
    ## 2. Dataset Description
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

with col3: 
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






# --------------------------------------------- 
# PCA Analysis
st.markdown("## PCA Projection of Ingredients Distribution by Country")
df = pd.read_json('data/json_data/country_ingredients.json', orient='index')

df['country'] = df.index
df = df.reset_index(drop=True)

X = df.drop(['country'], axis=1)
y = df['country']

X_array = np.array(X)
y_array = np.array(y)

# Use SVD instead of eigendecomposition to avoid complex numbers
# SVD is more numerically stable and guarantees real values
U, S, Vt = np.linalg.svd(X_array, full_matrices=False)

# Take the first two right singular vectors (equivalent to principal components)
max_train = Vt.T[:, :2]

# Create an empty figure
fig = go.Figure()

# Iterate through unique labels in y (your class labels)
for i in np.unique(y_array):
    one_train = X_array[y_array == i]  # Get data points corresponding to class i

    # Project data using the matrix max_train
    projected_data_train = np.dot(one_train, max_train)

    # Scatter plot for each class
    fig.add_trace(go.Scatter(
        x=projected_data_train[:, 0].real,  # x-coordinates, ensure real part only
        y=projected_data_train[:, 1].real,  # y-coordinates, ensure real part only
        mode='markers+text',  # Markers with text annotations
        name=str(i),  # Use class label as the legend name
        text=[str(i)] * projected_data_train.shape[0],  # Add class labels as text
        textposition='bottom right',  # Position of text relative to markers
        marker=dict(size=10, opacity=0.8)  # Customize marker appearance
    ))

# Update layout to add title, axes labels, and legend

col1, col2 = st.columns((1.5,2))
with col1:
    st.markdown("### 2D PCA Projection")

    fig.update_layout(
    #    title="2D PCA Projection of Ingredients Distribution by Country",
        xaxis_title="Projection X",
        yaxis_title="Projection Y",
        legend_title="Classes",
        template="plotly_white",  # Optional: change theme
        font_size=5,
    )

    # Show the interactive plot in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)



with col2: 
    #  ========== 3D PCA ==========
    # Perform SVD for PCA (3 components)
    U, S, Vt = np.linalg.svd(X_array, full_matrices=False)

    # Take the first three right singular vectors
    pca_components = Vt.T[:, :3]

    # Project the data onto the first 3 principal components
    projected_data = np.dot(X_array, pca_components)

    # Create a 3D scatter plot with Plotly
    fig = go.Figure()

    # Add a trace for each country (class)
    for country in np.unique(y_array):
        # Get data points for this country
        country_data = projected_data[y_array == country]
        
        # Add a 3D scatter trace
        fig.add_trace(go.Scatter3d(
            x=country_data[:, 0],
            y=country_data[:, 1],
            z=country_data[:, 2],
            mode='markers',
            name=country,
            text=[country] * country_data.shape[0],
            marker=dict(
                size=6,
                opacity=0.8
            )
        ))

    # Update layout for better visualization
    st.markdown("### 3D PCA Projection")
    fig.update_layout(
        # title="3D PCA Projection of Ingredients Distribution by Country",
        scene=dict(
            xaxis_title="PC1",
            yaxis_title="PC2",
            zaxis_title="PC3",
            # Improve camera angle and perspective
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2)
            )
        ),
        legend_title="Countries",
        template="plotly_white",
        margin=dict(l=0, r=0, b=0, t=40)
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Optionally, print the explained variance for each component
    total_variance = np.sum(S**2)
    explained_variance_ratio = [(s**2)/total_variance for s in S[:3]]

    st.write("\nExplained variance by component:")
    st.write(f"- PC1: {explained_variance_ratio[0]:.2%}")
    st.write(f"- PC2: {explained_variance_ratio[1]:.2%}")
    st.write(f"- PC3: {explained_variance_ratio[2]:.2%}")





df = load_cleaned_recipes_v2()

st.markdown("## Ingredients Word Cloud")
st.markdown("""
This word cloud represents the most common ingredients used in the recipes. The size of each word indicates its frequency in the dataset.
The larger the word, the more frequently it appears in the recipes.
The word cloud is a great way to visualize the most popular ingredients and can help in understanding the culinary trends across different regions.
The word cloud is generated using the `WordCloud` library, which creates a visual representation of the frequency of words in a text.
The word cloud is generated from the `ingredients` column of the dataset, which contains a list of ingredients for each recipe.
""")

col1, col2 = st.columns([1, 1.5])  # col2 will be twice as wide as col1

with col1:
    image = Image.open("assets/wordcloud.png")
    st.image(image, caption="Word Cloud", use_container_width=True)


with col2:

    def wordcloud(sub_region):
        """
        Function to generate a word cloud for a specific sub-region
        """
        ingred = pd.read_json("data/json_data/country_ingredients.json")[sub_region]

        di = dict(ingred)

        # word cloud
        wordcloud = WordCloud(width = 1200, height = 800, 
                background_color ='black', 
                stopwords = None, 
                min_font_size = 10).generate_from_frequencies((dict(di)))
        
        fig = plt.figure(figsize = (8, 8), facecolor = None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad = 0)
        plt.savefig("assets/tmp.png", bbox_inches="tight")

        st.pyplot(fig)

    st.markdown("#### Ingredients word cloud game")
    # Jeu de donnees
    sub_regions = df["sub_region"].unique().tolist()
    sub_region = st.selectbox("Select a sub-region:", sub_regions)
    
    wordcloud(sub_region)
        
