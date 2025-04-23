import streamlit as st
import plotly.express as px
from plotly import figure_factory as ff
import plotly.express as px

import streamlit as st

# Configuration générale pour tous les plots
layout_config = dict(
    width=750,  # Largeur augmentée
    height=500,  # Hauteur augmentée
    font=dict(size=14)  # Taille de police augmentée
)

def data(df):
    """
    Introduction page of the dashboard
    """
    # st.markdown(md_content, unsafe_allow_html=True)
    st.markdown("# Dataset Overview")

    st.write(
        """
        ## Introduction
        In this section, we will describe the data and analyze it to understand the distribution of recipes across different continents and regions.
        - The dataset contains recipes from various countries, with a focus on the number of recipes per continent and region.
        - The data is sourced from the ... and contains information about the ingredients, cuisine, and steps involved in each recipe.
        - After several preprocessing steps, we have a clean dataset ready for analysis.

        """
    )

    st.write(df.head(5))
    string = """
        ## Dataset Description
        **Shape**: 3843 entries x 16 columns  
        **Memory Usage**: ~510.4 KB

        ### Column Summary

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
        """
    st.markdown(string)


    # ---------------------------------------------

    st.markdown("## Data Analysis")
    st.write(
        """
        In this section, we will analyze the dataset to understand the distribution of recipes across different continents and regions.
        We will create visualizations to represent the number of recipes per continent and region.
        """
    )

    # Create a 2-column layout
    col1, col2 = st.columns(2)



    # Plot 1: Number of Recipes per Continent
    # Assuming df is your DataFrame
    with col1:
        st.markdown("### Number of Recipes per Continent")
        st.write(
            """
            This plot shows the number of recipes available in each continent.
            """
        )
        continent_counts = df["continent"].value_counts().reset_index()
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
        st.markdown("### Number of Recipes per Region")
        st.write(
            """
            This plot shows the number of recipes available in each region.
            """
        )
        # Plot 2: Number of Recipes per Region
        subregion_counts = df["sub_region"].value_counts().reset_index()
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
    # Assuming df is your DataFrame
    cuisine_counts = df["cuisine"].value_counts().reset_index()
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