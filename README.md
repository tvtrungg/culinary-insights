# culinary-cultural-insights

## Project structure
```txt
culinary-cultural-insights/
│── src/            
│   ├── __init__.py              
│── bin/    
│   ├── eval.py 
│   ├── train.py 
│── config/
│   ├── config.yml
│── demo/
│   ├── preprocessing.ipynb
│── __init__.py
│── .gitattributes
│── .gitignore
│── environment.yml
│── README.md
```

## Users manual
### Setup virtual environment
#### For miniconda3 users:
```bash
conda env create -f environment.yml
<<<<<<< HEAD
conda activate recipes
=======
conda activate culinary
>>>>>>> v_trung
```
### Data source


# Phần giới thiệu dự án
st.markdown("""
## 📖 Introduction

This project explores how culinary cultures around the world reflect and relate to broader aspects of society such as economy, environment, healthcare, and cultural identity.

By analyzing a rich dataset of global recipes alongside economic indicators, we aim to uncover patterns and insights that food can reveal about different regions.
""")

# Các phân tích đã thực hiện
st.markdown("""
## 🔍 Analysis Overview

We conducted several key analyses, including:

- **Data Preprocessing:** Cleaning missing values (e.g., rating, calories) and selecting key fields such as steps, cuisine, continent, and sub-region.
- **Ingredient Analysis:** Using text preprocessing and WordCloud to highlight the most commonly used ingredients worldwide and across sub-regions.
- **PCA (Principal Component Analysis):** Reducing dimensionality to visualize differences and similarities in culinary patterns across regions.
- **ANOVA (Analysis of Variance):** Testing whether the differences in ingredients and recipe features across regions are statistically significant.
- **Economic & Social Analysis:** Investigating how culinary styles relate to broader factors:
  - **GDP**: Linking economic development with culinary diversity.
  - **Environment**: Studying ingredients in relation to environmental sustainability.
  - **Healthcare**: Exploring how health trends may reflect in recipe ingredients.
  - **Cultural Identity**: Highlighting cultural influences through food.
""")

# Highlight chính
st.markdown("""
## 🌟 Key Highlights

- Ingredients reflect regional diversity, even among geographically close areas.
- Economic prosperity often correlates with greater ingredient variety.
- Environmental concerns increasingly shape modern culinary habits.
- Food can serve as a cultural mirror, revealing identity, history, and adaptation.
""")

