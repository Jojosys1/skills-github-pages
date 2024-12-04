# Utiliser une image de base officielle de Python
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt ./

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le contenu du répertoire local dans le répertoire de travail du conteneur
COPY . .

# Exposer le port sur lequel Streamlit fonctionne
EXPOSE 8501

# Définir la commande de démarrage par défaut
CMD ["streamlit", "run", "site_web.py", "--server.port=8501", "--server.address=0.0.0.0"]
