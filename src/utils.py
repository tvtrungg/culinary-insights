# -*- coding: utf-8 -*-
# @Author: T. V. Trung

import numpy as np 
from sklearn.decomposition import PCA
from wordcloud import WordCloud
import random
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme("darkgrid")
random.seed(42)

class Utilities: 
    """
    Utility class for various helper functions.
    """
    def __init__(self):
        pass

    @staticmethod
    def normalize(X: np.ndarray):
        """
        Normalize the input data.
        """
        X_norm = (X - np.mean(X, axis=0)) / np.std(X, axis=0)
        return X_norm

    @staticmethod
    def compute_PCA(
        self,
        X: np.ndarray,
        n_components: int = 2,
    ): 
        X_norm = Utilities.normalize(X)
        pca = PCA(n_components=n_components)
        X_projected_3D = pca.fit_transform(X_norm)

        return X_projected_3D
    
    @staticmethod
    def visualize_wordcloud(
        self,
        size: tuple = (800, 800),
        ingredients_set: set = None,
        stopwords: set = None,
        save_path: str = "../assets/wordcloud.png",
        is_show: bool = False,
    ):
        """
        Visualize a word cloud with the given size.
        """
        wordcloud = WordCloud(
            width=size[0],
            height=size[1],
            background_color="black",
            colormap="viridis",
            max_words=200,
            random_state=42,
            stopwords=stopwords,
        ).generate(" ".join(ingredients_set))
        plt.figure(figsize = (8, 8), facecolor = None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad = 0)
        if save_path:
            plt.savefig(save_path)
        if is_show:
            plt.show()