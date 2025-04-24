def clust():
    import pandas as pd
    import numpy as np
    import streamlit as st
    import plotly.graph_objects as go
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from sklearn.ensemble import RandomForestClassifier
    from collections import defaultdict
    import plotly.express as px

    st.markdown("""# Ingredients clustering
    The ingredients clustering is a technique used to group similar ingredients together based on their characteristics.
    This can help in understanding the relationships between different ingredients and can be useful in recipe generation and recommendation systems.
    The clustering is done using the `RandomForest` algorithm, which is a popular clustering algorithm that groups data points into k clusters based on their features.
    The clustering is done on the `ingredients` column of the dataset, which contains a list of ingredients for each recipe.""")

    ingred = pd.read_csv("data/json_data/country_ingredients.csv", index_col=0).T
    ingred['sub_region'] = ingred.index
    ingred = ingred.melt(id_vars=['sub_region'], var_name='ingredient', value_name='frequency')

    df = ingred

    # Encode
    ingredient_encoder = LabelEncoder()
    df['ingredient_encoded'] = ingredient_encoder.fit_transform(df['ingredient'])

    subregion_encoder = LabelEncoder()
    df['sub_region_encoded'] = subregion_encoder.fit_transform(df['sub_region'])

    X = df[['ingredient_encoded', 'frequency']]
    y = df['sub_region_encoded']

    scaler = StandardScaler()
    X['frequency'] = scaler.fit_transform(X[['frequency']])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    y_pred_labels = subregion_encoder.inverse_transform(y_pred)
    y_test_labels = subregion_encoder.inverse_transform(y_test)

    for i in range(5):
        print(f"Predicted: {y_pred_labels[i]}, Actual: {y_test_labels[i]}")

    def predict_subregion_for_ingredient(ingredient_name, frequency_value=1):
        ingredient_encoded = ingredient_encoder.transform([ingredient_name])[0]
        frequency_scaled = scaler.transform([[frequency_value]])[0][0]
        X_input = [[ingredient_encoded, frequency_scaled]]
        pred_encoded = model.predict(X_input)[0]
        sub_region = subregion_encoder.inverse_transform([pred_encoded])[0]
        return sub_region

    uniq_ingredients = pd.read_json("data/json_data/country_ingredients.json").index.tolist()

    tmp = [predict_subregion_for_ingredient(i, frequency_value=1) for i in uniq_ingredients]

    region_to_ingredients = defaultdict(list)
    for region, ingredient in zip(tmp, uniq_ingredients):
        region_to_ingredients[region].append(ingredient)

    num_regions = len(region_to_ingredients)
    angles = np.linspace(0, 2 * np.pi, num_regions, endpoint=False)
    radius = 5
    region_centers = {region: (radius * np.cos(angle), radius * np.sin(angle))
                      for region, angle in zip(region_to_ingredients.keys(), angles)}

    colors = px.colors.qualitative.Dark24

    st.sidebar.header("Visualization Controls")

    available_regions = list(region_to_ingredients.keys())
    selected_regions = st.sidebar.multiselect(
        "Filter by Sub-Regions",
        options=available_regions,
        default=available_regions
    )

    search_term = st.sidebar.text_input("Search for an ingredient").lower()
    zoom_level = st.sidebar.slider("Zoom Level", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

    fig = go.Figure()
    highlighted_nodes = []

    for idx, (region, ingr_list) in enumerate(region_to_ingredients.items()):
        if region not in selected_regions:
            continue

        cx, cy = region_centers[region]
        color = colors[idx % len(colors)]

        region_x = []
        region_y = []
        region_texts = []
        region_hover = []

        for ingredient in ingr_list:
            x = np.random.normal(cx, 0.5)
            y = np.random.normal(cy, 0.5)

            # is_highlighted = search_term and search_term in ingredient.lower()
            # if is_highlighted:
            #     highlighted_nodes.append((x, y, ingredient))

            region_x.append(x)
            region_y.append(y)
            region_texts.append(ingredient)
            region_hover.append(f"Ingredient: {ingredient}<br>Region: {region}")

        marker_size = [16 if search_term and search_term in ing.lower() else 12 for ing in ingr_list]
        marker_color = ['red' if search_term and search_term in ing.lower() else color for ing in ingr_list]

        fig.add_trace(go.Scatter(
            x=region_x, y=region_y,
            mode='markers+text',
            text=region_texts,
            textposition='bottom center',
            marker=dict(size=marker_size, color=marker_color, line=dict(width=1, color='black')),
            hoverinfo='text',
            hovertext=region_hover,
            name=region,
            showlegend=True
        ))


    fig.update_layout(
        title='Ingredient Clusters by Sub-Region',
        showlegend=True,
        legend=dict(
            title="Sub-Regions",
            orientation="h",  # Horizontal legend
            yanchor="top",
            y=-0.15,  # Position legend below the plot
            xanchor="center",
            x=0.5,
            bgcolor='black',
            bordercolor='black',
            borderwidth=1
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        plot_bgcolor='black',
        height=800,
        hovermode='closest',
        dragmode='zoom',  # ← Makes zoom easier with mouse
        margin=dict(l=0, r=0, t=60, b=0),
    )


    st.title("Ingredient Clustering by Sub-Region")

    st.plotly_chart(fig, use_container_width=True)