import streamlit as st
import pandas as pd

# Titre de l'application
st.title('Importation de Fichier CSV et Affichage des Données')

# Importation du fichier CSV
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file is not None:
    try:
        # Lecture du fichier CSV
        df = pd.read_csv(uploaded_file)
        st.success("Fichier chargé avec succès.")
        
        # Afficher les données brutes
        st.subheader('Données Brutes')
        st.write(df.head())

        # Analyse des données (exemple de description)
        st.subheader('Description des Données')
        st.write(df.describe())
        
        # Option de téléchargement
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger les données en CSV",
            data=csv,
            file_name='données_analyse.csv',
            mime='text/csv',
        )

    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
