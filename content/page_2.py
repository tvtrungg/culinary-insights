import streamlit as st

def page_2():
    """
    Comment
    """
    st.markdown("## Page 2")
    st.markdown("""
    Au terme de cette exploration, nous retenons :
    - L'angle d'attaque et le nombre de Reynolds sont des facteurs déterminants des performances aérodynamiques.
    - Le modèle XGBoost fournit de bonnes prédictions du ratio L/D, permettant une exploration rapide de l'espace de conception.
    - L'analyse des features importantes éclaire les leviers d'amélioration (profil plus épais, angle optimal, etc.).
    
    *Perspectives* :
    - Intégrer d'autres paramètres géométriques (cambrure, allongement, etc.) pour affiner la prédiction.
    - Coupler cette approche avec des outils d'optimisation évolutive pour trouver des profils encore plus performants.
    - Approfondir l'étude des régimes turbulents et la transition laminaire-turbulent pour une meilleure robustesse.
    
    Merci d'avoir exploré cette application. Nous espérons qu'elle vous aidera à mieux comprendre les facteurs clés influençant les performances aérodynamiques.
    """)

    st.markdown("### Références")
    st.markdown("""
    - Anderson, J.D., Fundamentals of Aerodynamics, McGraw-Hill.  
    - Drela, M. et Giles, M.B., "Viscous-Inviscid Analysis of Transonic and Low Reynolds Number Airfoils", AIAA Journal.
    """)