import streamlit as st
import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Configuration du mode clair - doit être la première commande Streamlit
st.set_page_config(page_title="Analyse des Commentaires Clients", page_icon="🔍", layout="centered", initial_sidebar_state="auto")

# Importer Font Awesome pour les icônes
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">', unsafe_allow_html=True)

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
        font-family: 'Arial', sans-serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .upload-area {
        border: 2px dashed #4CAF50;
        padding: 20px;
        text-align: center;
        background-color: #F9F9F9;
        border-radius: 10px;
        margin-bottom: 20px;
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
    .description {
        font-size: 18px;
        color: #000;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .icon-home {
        font-size: 30px;
        color: #FF5722;
    }
    .icon-results {
        font-size: 30px;
        color: #4CAF50;
    }
        </style>
""", unsafe_allow_html=True)

# Titre de l'application
st.markdown('<div class="title"><i class="fas fa-chart-line"></i> Analyse des Commentaires Clients</div>', unsafe_allow_html=True)
st.markdown('<div class="description"><i class="fas fa-info-circle"></i> Téléchargez un fichier CSV contenant les commentaires des clients pour une analyse approfondie.</div>', unsafe_allow_html=True)

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

# Section d'importation du fichier avec un style personnalisé
st.markdown('<div class="upload-area"><i class="fas fa-upload"></i>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")
st.markdown('</div>', unsafe_allow_html=True)



# Définir les pages principales et sous-pages
page = st.sidebar.selectbox("Navigation", ["Accueil", "Résultats"])

if page == "Accueil":
    st.sidebar.markdown('<i class="fas fa-home icon-home"></i>', unsafe_allow_html=True)
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.markdown('<div class="success"><i class="fas fa-check-circle"></i> Fichier chargé avec succès.</div>', unsafe_allow_html=True)
            # Enregistrer les données dans une session pour les partager entre les pages
            st.session_state['df'] = df
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier : {e}")
            st.stop()

elif page == "Résultats":
    df = st.session_state['df']
    st.sidebar.markdown('<i class="fas fa-chart-bar icon-results"></i>', unsafe_allow_html=True)
    # Nettoyer les commentaires et extraire les mots essentiels
    df['Mots_Essentiels'] = df['Commentaire'].astype(str).apply(clean_comment)
    df['Sentiment'] = df['Mots_Essentiels'].apply(analyze_sentiment)
    # Séparer les commentaires en bons et mauvais
    good_comments = df[df['Sentiment'] == 'positif']
    bad_comments = df[df['Sentiment'] == 'négatif']
    # Extraction et comptage des mots-clés pour les bons commentaires
    good_words = " ".join(good_comments['Mots_Essentiels']).split()
    good_word_counts = Counter(good_words)
    # Extraction et comptage des mots-clés pour les mauvais commentaires
    bad_words = " ".join(bad_comments['Mots_Essentiels']).split()
    bad_word_counts = Counter(bad_words)
    # Sous-pages pour "Résultats"
    subpage = st.sidebar.selectbox("infos traitées",["Données Brutes", "Analyse des Sentiments", "Opportunités d'Amélioration"])

    if 'df' in st.session_state:
        df = st.session_state['df']
        
        
        if subpage == "Données Brutes":
            st.markdown('<div class="result-area">', unsafe_allow_html=True)
            st.markdown('<div class="header"><i class="fas fa-database"></i> Données Brutes: les commentaires</div>', unsafe_allow_html=True)
            st.write(df.head())
        
        elif subpage == "Analyse des Sentiments":
            st.sidebar.markdown('<i class="fas fa-smile icon-sentiment"></i>', unsafe_allow_html=True) 
            st.markdown(
                """
                <div style="display: flex; align-items: center;">
                <img src="https://cdn-icons-png.flaticon.com/512/742/742751.png" alt="Sentiment Analysis Icon" style="width:40px; height:40px; margin-right:10px;">
                <h3 style="margin: 0;">Analyse de Sentiments</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            subpage = st.sidebar.selectbox("options",["Diagramme des sentiments", "Commentaires"])
            if 'df' in st.session_state:
                df = st.session_state['df']
                
                if subpage=="Diagramme des sentiments":
                    # Répartition des sentiments avec des couleurs plus nuancées et des légendes
                    st.subheader('Répartition des Sentiments')
                    sentiment_counts = df['Sentiment'].value_counts()
                    fig, ax = plt.subplots(figsize=(10, 7))
                    colors = ['#4CAF50', '#FF5722', '#9E9E9E']  # Couleurs nuancées : Vert pour positif, Rouge pour négatif, Gris pour neutre
                    sentiment_counts.plot(kind='pie', ax=ax, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops=dict(edgecolor='w'))
                    ax.set_ylabel('')
                    ax.set_title('Répartition des Sentiments')
                    plt.legend(labels=sentiment_counts.index, loc='upper left', bbox_to_anchor=(1, 0.5), title="Sentiments")
                    st.pyplot(fig)
                    #     
                elif subpage=="Commentaires": 
                    
                    
                    
                    subpage = st.sidebar.selectbox("Classification des commentaires et occurences",["Bon commentaires", "Mauvais commentaires","Occurrences des Mots"])
                    if 'df' in st.session_state:
                        df = st.session_state['df']
                        
                        if subpage=="Bon commentaires":
                            # Afficher les bons  commentaires 
                            st.subheader('Tableau des Commentaires Positifs')
                            st.write(good_comments[['Commentaire', 'Sentiment', 'Mots_Essentiels']])

                            # Visualisation du nuage de mots pour les bons commentaires
                            st.subheader('Nuage de Mots - Commentaires Positifs')
                            good_wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies(good_word_counts)
                            fig, ax = plt.subplots(figsize=(10, 5))
                            ax.imshow(good_wordcloud, interpolation='bilinear')
                            ax.axis('off')
                            st.pyplot(fig)
                            
                        elif subpage=="Mauvais commentaires":
                                

                            # Afficher les mauvais commentaires
                            st.subheader('Tableau des Commentaires Négatifs')
                            st.write(bad_comments[['Commentaire', 'Sentiment', 'Mots_Essentiels']])

                            # Visualisation du nuage de mots pour les mauvais commentaires
                            st.subheader('Nuage de Mots - Commentaires Négatifs')
                            bad_wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies(bad_word_counts)
                            fig, ax = plt.subplots(figsize=(10, 5))
                            ax.imshow(bad_wordcloud, interpolation='bilinear')
                            ax.axis('off')
                            st.pyplot(fig)
                            
                        elif subpage == "Occurrences des Mots":
                            st.markdown('<h2><i class="fas fa-word icon"></i> Occurrences des Mots</h2>', unsafe_allow_html=True)
                            all_words = " ".join(df['Mots_Essentiels'])
                            word_counts = Counter(all_words.split())
                            st.write(pd.DataFrame(word_counts.most_common(10), columns=['Mot', 'Occurrences']))
                            fig, ax = plt.subplots()
                            plt.bar(*zip(*word_counts.most_common(10)))
                            st.pyplot(fig)    
            
        elif subpage == "Opportunités d'Amélioration": 
            st.sidebar.markdown('<i class="fas fa-lightbulb icon-opportunities"></i>', unsafe_allow_html=True) 
            st.markdown('<h2><i class="fas fa-lightbulb icon"></i> Opportunités d\'Amélioration</h2>', unsafe_allow_html=True) 
            st.write(df[df['Opportunité'] == True])
            positive_opportunities = df[(df['Opportunité'] == True) & (df['Sentiment'] == 'positif')]
            negative_neutral_opportunities = df[(df['Opportunité'] == True) & ((df['Sentiment'] == 'négatif') 
            (df['Sentiment'] == 'neutre'))]
            st.markdown('<div class="header">Suggestions ou améliorations</div>', unsafe_allow_html=True) 
            st.write(negative_neutral_opportunities[['Commentaire', 'Sentiment', 'Mots_Essentiels']])   
            
