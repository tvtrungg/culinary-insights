import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")

# Load data
df = pd.read_csv('data/cleaned_recipes_v2.csv',index_col=0)

plt.figure(figsize=(15,7))
df["continent"].value_counts().plot(kind='bar',color='red',orientation='vertical')
plt.title('Number of recipes per continent')
plt.ylabel('Number of recipes')
plt.xlabel('Continent')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.savefig("assets/recipes_per_continent.png")


plt.figure(figsize=(20,10))
df["cuisine"].value_counts().plot(kind='bar',color='red',orientation='vertical')
plt.title('Number of recipes per cuisine')
plt.ylabel('Number of recipes')
plt.xlabel('Cuisine')
plt.savefig("assets/recipes_per_cuisine.png")


plt.figure(figsize=(20,10))
df["sub_region"].value_counts().plot(kind='bar',color='red',orientation='vertical')
plt.title('Number of recipes per sub-region')
plt.ylabel('Number of recipes')
plt.xlabel('Continent')
plt.savefig("assets/recipes_per_sub_continent.png")