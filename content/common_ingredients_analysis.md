# Common Ingredients Analysis

## Overview

Trong phần nội dung này, tôi sẽ phân tích các nguyên liệu trong các món ăn từ khắp nơi trên thế giới. Tôi sẽ sử dụng một tập dữ liệu chứa thông tin về các món ăn từ nhiều quốc gia khác nhau, bao gồm title,	steps, rating, cuisine, etc. 
Tôi sẽ tập trung vào việc phân tích các nguyên liệu chính được sử dụng trong các món ăn này và cách chúng khác nhau giữa các khu vực địa lý khác nhau.

## Analyse des données

- J'ai sélectionné les champs clés suivants pour l'analyse: **steps, cuisine, continent và sub_region**.

### Selon steps

Au départ, je voulais analyser en fonction des étapes (steps), mais après plusieurs transformations pour essayer d’extraire les mots-clés principaux, j’ai vu que ces mots-clés étaient à peu près les mêmes dans tous les pays. Et en regardant les tops mots-clés liés à la cuisine, je me suis rendu compte qu’ils n’avaient pas vraiment de signification pertinente. Du coup, J'ai ignoré cette analyse avec les étapes

### Selon continent

- J’ai remarqué que les données varient énormément selon les continents. Par exemple, l’Europe a presque 1500 recettes dans l’échantillon, alors que l’Afrique et l’Océanie en ont moins de 200 chacune.
- Sur ce graphique, la différence de volume de données atteint presque 50 % (2 colonnes sur 3), donc je ne suis pas encore décidé à analyser selon cette piste des continents.

![continent](assets/recipes_per_continent.png)

### Selon cuisine

- J’ai vu qu’il y a aussi une grosse différence entre les types de cuisine.
- Par exemple, les premières colonnes (types de cuisine) ont beaucoup d’échantillons, tandis que les dernières n’en ont que très peu.
- Cette différence est assez marquée, avec un écart d’environ 30 à 40 %.

### Selon sub_region

- Dans ce champ, la différence dans les données est beaucoup moins importante (environ 10 à 20 %), et du coup, j’ai décidé de partir sur cette piste pour l’analyse.
