import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

def usps(df):
    st.markdown("# PCA")
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
    fig.update_layout(
       title="2D PCA Projection of Ingredients Distribution by Country",
        xaxis_title="Projection X",
        yaxis_title="Projection Y",
        legend_title="Classes",
        template="plotly_white"  # Optional: change theme
    )

    # Show the interactive plot in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)





    # 3D 
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
    fig.update_layout(
        title="3D PCA Projection of Ingredients Distribution by Country",
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
    
    st.write("Explained variance by component:")
    st.write(f"PC1: {explained_variance_ratio[0]:.2%}")
    st.write(f"PC2: {explained_variance_ratio[1]:.2%}")
    st.write(f"PC3: {explained_variance_ratio[2]:.2%}")