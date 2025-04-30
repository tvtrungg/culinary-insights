import streamlit as st
from utils.style import inject_css

inject_css()

# Page configuration
# Title
st.title("🌎 What can culinary cultures reveal to us about the world?")

# Introduction
st.header("Project Overview")
st.markdown("""
This project explores how culinary cultures around the world reflect and relate to broader aspects of society such as economy, environment, healthcare, and cultural identity.

By analyzing a rich dataset of global recipes alongside economic indicators, we aim to uncover patterns and insights that food can reveal about different regions.
""")

# Analysis Summary
st.header("What We Analyzed")
st.markdown("""
We conducted several analyses to answer our central question:

- **PCA (Principal Component Analysis):**  
  To reduce the dimensionality of ingredient data and identify major patterns across regions.
  
- **WordCloud Visualization:**  
  To showcase the most commonly used ingredients globally and within specific regions.
  
- **ANOVA Test:**  
  To statistically verify if ingredient usage significantly differs across sub-regions.

- **Economic Analysis (GDP):**  
  Investigating how economic status relates to culinary diversity and ingredient richness.

- **Environmental Analysis:**  
  Exploring the impact of regional agriculture and environment on cuisine.

- **Health Analysis:**  
  Looking at nutritional aspects like calories and common ingredients across regions.

- **Cultural Analysis:**  
  Studying how traditions and migration patterns influence local and global food habits.
""")

# Key Question
st.header("Why Does It Matter?")
st.markdown("""
By analyzing food, we don't just understand recipes —  we uncover stories about **migration, globalization, tradition, environment, and health**.

This project invites you to look at food from a new, interdisciplinary perspective.
""")

# Call to Action
st.success("👉 Explore the different sections in the sidebar to dive deeper into each analysis!")

if st.button("Go to Data Overview ➡️"):
    st.switch_page("pages/Data_Overview.py")
