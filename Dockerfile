# Utilisation d'une image Python légère
FROM python:3.12-slim

# Définition du répertoire de travail dans le conteneur
WORKDIR /workspace

# Copie du fichier de dépendances en premier (optimise le cache Docker)
COPY requirements.txt .

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie du dossier app contenant votre code source
COPY ./app ./app

# Exposition du port (FastAPI utilise souvent 8000 par défaut, Flask 5000)
EXPOSE 8000

# Commande de démarrage (à adapter si vous utilisez Flask au lieu de FastAPI)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]