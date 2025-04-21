import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")
from wordcloud import WordCloud

df = pd.read_csv('data/cleaned_recipes_v2.csv',index_col=0)

# clean data
for i in range(len(df)):
    df['ingredients'][i] = df['ingredients'][i].replace('[','').replace(']','').replace("'",'').replace("",'').replace('"','').split(',')

for i in range(len(df)):
    df['ingredients'][i] = [x.strip() for x in df['ingredients'][i]]
    df['ingredients'][i] = [x.replace(' ','_') for x in df['ingredients'][i]]

# Collect all unique ingredients
ingredients_set = set()

for i in range(len(df)):
    for ingredient in df['ingredients'][i]:
        ingredients_set.add(ingredient)


wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='black', 
                stopwords = None, 
                min_font_size = 10).generate(' '.join(ingredients_set))

plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.savefig("assets/wordcloud.png")


countries = np.unique(df['sub_region'])

c_dict = dict()
for i in countries:
    c_dict[i] = dict()
    for j in ingredients_set:
        c_dict[i][j] = 0

for i in range(len(df['sub_region'])):
    ing = df['ingredients'][i]
    print(df['sub_region'][i])
    for j in ingredients_set:
        if j in ing:
            # print(j)
            c_dict[df['sub_region'][i]][j] += 1

c_l = dict()
for i in countries:
    c_l[i] = []

for i in range(len(df)):
    for j in ing:
        c_l[df['sub_region'][i]].append(j)


plt.figure(figsize=(20, 20))
for i in range(len(countries)):
    # wc = WordCloud(width=800, height=800, background_color='black').generate(' '.join(c_l[countries[i]]))
    wc = WordCloud(width = 800, height = 800, 
                background_color ='black', 
                stopwords = None, 
                min_font_size = 10).generate(' '.join(c_l[countries[i]]))
    plt.subplot(5, 5, i+1)
    plt.imshow(wc)
    plt.title(countries[i])
    plt.axis('off')

plt.savefig('assets/wordcloud_general.png')



# PCA
data = pd.read_json('data/json_data/country_ingredients.json', orient='index')
data['country'] = data.index
data = data.reset_index(drop=True)

X = data.drop(['country'], axis=1)
y = data['country']

X = np.array(X)
y = np.array(y)

# A réaliser :

# 1) calcul des vecteurs propres
lam_train, V_train = np.linalg.eig(X.T @ X)
# lam_test, V_test = np.linalg.eig(XTu.T @ XTu)

# Trouver les indices des deux plus grandes valeurs propres
largest_indices = np.argsort(lam_train)[::-1][:2]



# Extraire les deux plus grandes valeurs propres et leurs vecteurs propres correspondants
largest_eigenvalues = lam_train[largest_indices]


max_train = V_train[:, largest_indices]
# max_test = V_test[:, np.argmax(lam_test)]


# 2) affichage (print)
#print("1er valeur rendue:\n", lam_train)
#print("2e valeur rendue :\n", V_train)

# 3) tri et sélection des 2 vecteurs associés aux 2 plus grandes valeurs propres 
#print("Vecteur train :\n", max_train)


plt.figure(figsize=(25,15))
for i in np.unique(y):
    one_train = X[y == i]
    #print(one_train)

    projected_data_train = np.dot(one_train, max_train)

    # Scatter plot for the first point in the class
    plt.scatter(projected_data_train[0, 0], projected_data_train[0, 1], alpha=.8, label=i)
    
    # Add text for each point
    for j in range(projected_data_train.shape[0]):  # Loop through all points in one_train
        plt.text(projected_data_train[j, 0], projected_data_train[j, 1], str(i), fontsize=10, ha='right', va='bottom',rotation=45)

# ####################################
# plt.legend()
plt.title("Ingredients distribution projection")
plt.savefig("assets/proj_usps_all.png",bbox_inches='tight',pad_inches=0)
plt.show()
