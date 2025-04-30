import streamlit as st
import pandas as pd
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from utils.data_loader import load_data
from utils.style import inject_css

inject_css()
data = load_data()
df = data[0]
st.markdown("# Ingredients Word Cloud")
st.markdown("""
This word cloud represents the most common ingredients used in the recipes. The size of each word indicates its frequency in the dataset.
The larger the word, the more frequently it appears in the recipes.
The word cloud is a great way to visualize the most popular ingredients and can help in understanding the culinary trends across different regions.
The word cloud is generated using the `WordCloud` library, which creates a visual representation of the frequency of words in a text.
The word cloud is generated from the `ingredients` column of the dataset, which contains a list of ingredients for each recipe.
""")


image = Image.open("assets/wordcloud.png")
st.image(image, caption="Word Cloud", use_container_width=True)



# Jeu de donnees
sub_regions = df["sub_region"].unique().tolist()
sub_region = st.selectbox("Select a sub-region:", sub_regions)

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

st.markdown(f"## Ingredients word cloud game for {sub_region}")
wordcloud(sub_region)
    
