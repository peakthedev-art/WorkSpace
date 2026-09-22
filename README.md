# WorkSpace
WorkSpace 2026

Dans le terminal, tapper ceci :
## Configuration Docker

Copier le fichier d'environnement puis remplacer les mots de passe de démonstration :

```
cp .env.example .env
```

Lancer la base, l'API, Loki, Promtail et Grafana :

```bash
docker compose --env-file .env -f db.yml up -d --build
```

Services disponibles :

- API : http://localhost:8000
- Documentation API : http://localhost:8000/docs
- Grafana : http://localhost:3000
- Loki : http://localhost:3100/ready

Les journaux Docker sont envoyés automatiquement à Loki par Promtail. La source
de données Loki est provisionnée dans Grafana au démarrage.

Pour arrêter les services :

```bash
docker compose --env-file .env -f db.yml down
```

## Lancement Python local

Dans le terminal :

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Pour lancer l'API en local, une base MySQL doit être accessible avec les
variables `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` et `DB_NAME` :

```
source .venv/bin/activate
uvicorn app.main:app --reload
```

Le script SQL d'initialisation est exécuté uniquement lorsque le volume MySQL
est créé pour la première fois. Pour réinitialiser la base en développement :

```bash
docker compose --env-file .env -f db.yml down -v
```
```



Pour lancer Python en local :

```
source .venv/bin/activate
uvicorn app.main:app --reload
```