import streamlit as st

md_path = "./content/common_ingredients_analysis.md"

with open(md_path, "r", encoding="utf-8") as f:
    md_content = f.read()

def common_ingredients_analysis():
    """
    Introduction page of the dashboard
    """
    st.markdown(md_content, unsafe_allow_html=True)
    st.image('assets/recipes_per_continent.png', caption="Recipes per continent", use_container_width =True)



