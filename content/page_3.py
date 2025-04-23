import streamlit as st

def page_3():
    """
    Page 3 of the dashboard
    """
    st.markdown("## Page 3")
    st.markdown("""
    Au terme de cette exploration, nous retenons :
    - L'angle d'attaque et le nombre de Reynolds sont des facteurs déterminants des performances aérodynamiques.
    - Le modèle XGBoost fournit de bonnes prédictions du ratio L/D, permettant une exploration rapide de l'espace de conception.
    - L'analyse des features importantes éclaire les leviers d'amélioration (profil
    plus épais, angle optimal, etc.).
                
            """)
    st.markdown("### Références")