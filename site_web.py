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

# Titre de l'application avec HTML
st.markdown("""
    <style>
    .title {
        font-size: 50px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
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
    <div class="title">Analyse des Commentaires Clients</div>
""", unsafe_allow_html=True)

# Importation du fichier CSV
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.markdown('<div class="success">Fichier chargé avec succès.</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
        st.stop()

    # Afficher les données brutes
    st.markdown('<div class="header">Données Brutes: les commentaires</div>', unsafe_allow_html=True)
    st.write(df.head(10000))

    # Nettoyer les commentaires et extraire les mots essentiels
    df['Mots_Essentiels'] = df['Commentaire'].astype(str).apply(clean_comment)

    # Analyser les sentiments des commentaires
    df['Sentiment'] = df['Mots_Essentiels'].apply(analyze_sentiment)

    # Détecter les opportunités d'amélioration
    df['Opportunité'] = df['Mots_Essentiels'].apply(detect_opportunities)

    # Séparer les opportunités en fonction du sentiment des commentaires
    positive_opportunities = df[(df['Opportunité'] == True) & (df['Sentiment'] == 'positif')]
    negative_neutral_opportunities = df[(df['Opportunité'] == True) & ((df['Sentiment'] == 'négatif') | (df['Sentiment'] == 'neutre'))]

    # Séparer les commentaires en bons et mauvais
    good_comments = df[df['Sentiment'] == 'positif']
    bad_comments = df[df['Sentiment'] == 'négatif']

    # Extraction et comptage des mots-clés pour les bons commentaires
    good_words = " ".join(good_comments['Mots_Essentiels']).split()
    good_word_counts = Counter(good_words)

    # Extraction et comptage des mots-clés pour les mauvais commentaires
    bad_words = " ".join(bad_comments['Mots_Essentiels']).split()
    bad_word_counts = Counter
