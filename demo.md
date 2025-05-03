- Dans le nouveau jeu de données, on trouve des champs comme : steps, rating, cuisine, continent, sub_region,...
- Et après avoir exécuté `df.info()` pour observer, on voit que des champs comme la note et les calories manquent d'informations, on doit donc effectuer un preprocessing pour supprimer les valeurs manquantes (N/A) avant d'analyser.

## Analyse des données

- J'ai sélectionné les champs clés suivants pour l'analyse: **steps, cuisine, continent và sub_region**.

### Selon steps

Au départ, je voulais analyser en fonction des étapes (steps), mais après plusieurs transformations pour essayer d’extraire les mots-clés principaux, j’ai vu que ces mots-clés étaient à peu près les mêmes dans tous les pays. Et en regardant les tops mots-clés liés à la cuisine, je me suis rendu compte qu’ils n’avaient pas vraiment de signification pertinente. Du coup, J'ai ignoré cette analyse avec les étapes

### Selon continent

- J’ai remarqué que les données varient énormément selon les continents. Par exemple, l’Europe a presque 1500 recettes dans l’échantillon, alors que l’Afrique et l’Océanie en ont moins de 200 chacune.
- Sur ce graphique, la différence de volume de données atteint presque 50 % (2 colonnes sur 3), donc je ne suis pas encore décidé à analyser selon cette piste des continents.

### Selon cuisine

- J’ai vu qu’il y a aussi une grosse différence entre les types de cuisine.
- Par exemple, les premières colonnes (types de cuisine) ont beaucoup d’échantillons, tandis que les dernières n’en ont que très peu.
- Cette différence est assez marquée, avec un écart d’environ 30 à 40 %.

### Selon sub_region

- Dans ce champ, la différence dans les données est beaucoup moins importante (environ 10 à 20 %), et du coup, j’ai décidé de partir sur cette piste pour l’analyse.

### WordCloud

- J’ai analysé les ingrédients (ingredients), en supprimant les caractères inutiles et les mots qui ne servent à rien, puis je les ai mis dans un ensemble (set) pour compter combien de fois chaque mot apparaissait.
- Ensuite, j’ai créé un nuage de mots (wordcloud) pour montrer la fréquence de chaque mot dans les ingrédients.
- L’image ci-dessous montre les ingrédients les plus utilisés dans le monde.
- Après ça, j’ai analysé selon les sous-régions pour voir quels ingrédients étaient les plus populaires dans chaque zone.

---

- Tôi đã phân tích các ingredients, loại bỏ các ký tự thừa và các từ không cần thiết, sau đó lưu vào một set để đếm số lần xuất hiện của từng từ.
- Tiếp đến, tôi tạo một wordcloud để thể hiện số lần xuất hiện của từng từ trong ingredients.
- Hình dưới đây thể hiện các ingredients được sử dụng nhiều nhất trên thế giới.
- Sau đó, tôi phân tích dựa vào sub_region để xem các ingredients được sử dụng nhiều nhất ở từng khu vực.

### Cuối cùng

- J’ai analysé les données selon les sous-régions, et j’ai trouvé les ingrédients les plus utilisés dans chaque zone.
- Comme le montre l’illustration, les données se divisent en 4 grands groupes :
  - Le groupe Australie et Nouvelle-Zélande, qui sont proches l’un de l’autre, avec des ingrédients assez similaires.
  - Le groupe Asie. Même s’ils ne sont pas très éloignés géographiquement, les ingrédients utilisés diffèrent vraiment de manière nette.
  - Le groupe Amérique, qui suit le même genre de logique.
  - Le groupe Europe, pareil.

---

- Tôi đã phân tích dữ liệu theo sub_region, và tìm ra các ingredients được sử dụng nhiều nhất ở từng khu vực.
- Như hình minh hoạ, dữ liệu được chia thành 4 cụm chính:
  - Cụm Australia và New Zealand sẽ phân bố gần nhau, các nguyên liệu tương đối giống nhau
  - Cụm Asia. Mặc dù chỉ khác nhau một ít về vị trí (trên thực tế), nhưng các nguyên liệu sử dụng khác nhau một cách rõ rệt.
  - Cụm America cũng tương tự thế
  - Cụm Europe cũng tương tự thế


# Idea 1: Phân tích nguyên liệu giống nhau giữa các nước
# Idea 2: Phân tích nguyên liệu chính của Sub_continent, ăn cái gì nhiều
# Idea 3: Prediction (rating, region)
# Idea 4: Culinary Style Transfer (ML + Creativity)
Generate "Italian-style" versions of Indian recipes, or make low-fat versions of French recipes.
Ideas:
- Use embeddings or similarity to suggest substitutions for ingredients while maintaining cultural characteristics.
- Try GPT-style fine-tuned models (or heuristics) to rewrite steps/ingredients in another cuisine’s "style".