import streamlit as st
import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Liste de stopwords personnalisés (y compris les articles et pronoms)
stop_words = set([
    'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'dans', 'en', 'et', 'à', 
    'au', 'aux', 'ce', 'cet', 'cette', 'cela', 'ça', 'sur', 'pour', 'par', 
    'avec', 'sans', 'sous', 'qui', 'que', 'quoi', 'dont', 'où', 'est', 'sont',
    'être', 'avoir', 'faire', 'comme', 'plus', 'moins', 'très', 'bien', 'mal',
    'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles', 'me', 'te', 'se', 
    'moi', 'toi', 'lui', 'leur', 'eux'
])

# Fonction pour nettoyer le texte
def clean_comment(comment):
    comment = re.sub(r'[^\w\s]', '', comment.lower())  # Mise en minuscule et suppression des caractères spéciaux
    words = comment.split()
    cleaned_words = [word for word in words if word not in stop_words]  # Suppression des stopwords
    return " ".join(cleaned_words)

# Fonction pour analyser les sentiments
def analyze_sentiment(comment):
    positive_words = set([
        'excellent', 'jadore', 'super', 'expérience', 'superbe', 'génial', 
        'incroyable', 'fantastique', 'parfait', 'formidable', 'exceptionnel', 
        'positif', 'agréable', 'satisfait', 'recommandé', 'adore', 'adoré', 'like'
    ])
    negative_words = set([
        'mauvais', 'cher', 'horrible', 'déçu', 'médiocre', 'nul', 'problème', 
        'lent', 'déplorable', 'insatisfait', 'terrible', 'frustrant', 'inacceptable'
    ])
    comment_words = set(comment.split())
    if comment_words & positive_words:
        return 'positif'
    elif comment_words & negative_words:
        return 'négatif'
    else:
        return 'neutre'

# Fonction pour détecter les opportunités d'amélioration
def detect_opportunities(comment):
    opportunity_phrases = [
        'ajouter', 'il manque', 'améliorer', 'optimiser', 'perfectionner', 
        'corriger', 'compléter', 'renforcer', 'adapter', 'modifier', 
        'développer', 'mettre à jour', 'plus rapide', 'plus fluide', 
        'réduire les bugs', 'stabiliser', 'augmenter l\'efficacité', 
        'améliorer la vitesse', 'diminuer la latence', 'rendre plus durable', 
        'meilleure finition', 'plus solide', 'haute qualité', 'résoudre les défauts', 
        'plus fiable', 'inclure', 'intégrer', 'proposer davantage de choix', 
        'ajouter une fonctionnalité', 'enrichir le contenu', 'ajouter des détails', 
        'plus d\'options', 'personnaliser', 'simplifier', 'rendre plus intuitif', 
        'faciliter', 'plus ergonomique', 'améliorer l\'accessibilité', 
        'réduire la complexité', 'clarifier', 'améliorer l\'esthétique', 
        'moderniser', 'mettre en valeur', 'plus attrayant', 'revoir le design', 
        'ajouter des couleurs', 'rendre plus clair', 'réduire le coût', 
        'proposer des promotions', 'améliorer le rapport qualité-prix', 
        'plus compétitif', 'rendre plus abordable', 'rapide', 'lent'
    ]
    for phrase in opportunity_phrases:
        if phrase in comment:
            return True
    return False

# Configuration du mode clair
st.set_page_config(page_title="Analyse des Commentaires Clients", page_icon="🔍", layout="centered", initial_sidebar_state="auto")

# CSS pour personnaliser l'apparence en mode clair
st.markdown("""
    <style>
    body {
        background-color: white;
    }
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .upload-area {
        border: 2px dashed #4CAF50;
        padding: 20px;
        text-align: center;
    }
    .result-area {
        margin-top: 20px;
    }
    .header {
        font-size: 30px;
        font-weight: bold;
        color: #FF5722;
    }
    .success {
        font-size: 20px;
        color: #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# Titre de l'application
st.markdown('<div class="title">Analyse des Commentaires Clients</div>', unsafe_allow_html=True)

# Section d'importation du fichier avec un style personnalisé
st.markdown('<div class="upload-area">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")
st.markdown('</div>', unsafe_allow_html=True)

# Définir les pages
page = st.sidebar.selectbox("Navigation", ["Accueil", "Résultats"])

if page == "Accueil":
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.markdown('<div class="success">Fichier chargé avec succès.</div>', unsafe_allow_html=True)
            # Enregistrer les données dans une session pour les partager entre les pages
            st.session_state['df'] = df
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier : {e}")
            st.stop()

elif page == "Résultats":
    if 'df' in st.session_state:
        df = st.session_state['df']

        st.markdown('<div class="result-area">', unsafe_allow_html=True)
        st.markdown('<div class="header">Données Brutes: les commentaires</div>', unsafe_allow_html=True)
        st.write(df.head())

        df['Mots_Essentiels'] = df['Commentaire'].astype(str).apply(clean_comment)
        df['Sentiment'] = df['Mots_Essentiels'].apply(analyze_sentiment)
        df['Opportunité'] = df['Mots_Essentiels'].apply(detect_opportunities)

        positive_opportunities = df[(df['Opportunité'] == True) & (df['Sentiment'] == 'positif')]
        negative_neutral_opportunities = df[(df['Opportunité'] == True) & ((df['Sentiment'] == 'négatif') | (df['Sentiment'] == 'neutre'))]

        good_comments = df[df['Sentiment'] == 'positif']
        bad_comments = df[df['Sentiment'] == 'négatif']

        good_words = " ".join(good_comments['Mots_Essentiels']).split()
        good_word_counts = Counter(good_words)

        bad_words = " ".join(bad_comments['Mots_Essentiels']).split()
        bad_word_counts = Counter(bad_words)

        st.markdown('<div class="header">Tableau des Commentaires Positifs</div>', unsafe_allow_html=True)
        st.write(good_comments[['Commentaire', 'Sentiment', 'Mots_Essentiels']])

        st.markdown('<div class="header">Nuage de Mots - Commentaires Positifs</div>', unsafe_allow_html=True)
        good_wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies(good_word_counts)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(good_wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

        st.markdown('<div class="header">Tableau des Commentaires Négatifs</div>', unsafe_allow_html=True)
        st.write(bad_comments[['Commentaire', 'Sentiment', 'Mots_Essentiels']])

        st.markdown('<div class="header">Nuage de Mots - Commentaires Négatifs</div>', unsafe_allow_html=True)
        bad_wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies(bad_word_counts)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(bad_wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

        st.markdown('<div class="header">Répartition des Sent
