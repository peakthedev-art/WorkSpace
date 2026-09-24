# WorkSpace
WorkSpace 2026

Système RFID : gestion des badges, rôles, zones et accès, avec une base MySQL,
une API Python, et une stack d'observabilité (Loki / Promtail / Grafana).

## Configuration Docker

Copier le fichier d'environnement puis remplacer les mots de passe de démonstration :

```bash
cp .env.example .env
```

Lancer la base, l'API, Loki, Promtail et Grafana :

```bash
docker compose --env-file .env -f docker-compose.yml up -d --build
```

Services disponibles :

- API : http://localhost:8000
- Documentation API : http://localhost:8000/docs
- Grafana : http://localhost:3000
- Loki : http://localhost:3100/ready

Les journaux Docker sont envoyés automatiquement à Loki par Promtail. La source
de données Loki est provisionnée dans Grafana au démarrage.

> Si Loki, Promtail ou Grafana ne sont pas encore configurés, leurs blocs
> peuvent être commentés dans `db.yml` : seuls `mysql` et `api_python`
> démarreront alors.

Pour arrêter les services :

```bash
docker compose --env-file .env -f docker-compose.yml
```

## Base de données

Le schéma et le jeu de données de démonstration sont chargés automatiquement
par MySQL au premier démarrage, via deux scripts montés dans
`/docker-entrypoint-initdb.d/` :

- `commandes.sql` : création des tables (`role`, `badge`, `user`, `zone`,
  `habitation`, `zone_access`) et des contraintes de clés étrangères.
- `test_donnees.sql` : jeu de données de test (rôles, zones, badges,
  utilisateurs, droits d'accès).

⚠️ Ces scripts ne s'exécutent **qu'une seule fois**, lorsque le volume
`mysql_data` est créé. Toute modification de `commandes.sql` ou
`test_donnees.sql` après un premier lancement nécessite de réinitialiser la
base (voir ci-dessous) pour être prise en compte.

### Vérifier que les données sont bien chargées

```bash
docker exec -it workspace-mysql mysql -u root -p
```

```sql
SHOW DATABASES;
USE <nom_de_la_base>;   -- valeur de MYSQL_DATABASE dans .env
SHOW TABLES;
SELECT * FROM role;
SELECT * FROM zone;
SELECT * FROM badge;
SELECT * FROM user;
SELECT * FROM zone_access;
SELECT * FROM habitation;
```

Vérifier les droits d'accès par utilisateur (jointure complète) :

```sql
SELECT
    u.name, u.surname, r.name AS role, z.name AS zone_autorisee
FROM user u
JOIN badge b ON u.badge_id = b.id
JOIN role r ON b.role_id = r.id
JOIN zone_access za ON za.role_id = r.id
JOIN zone z ON za.zone_id = z.id
ORDER BY u.surname, z.name;
```

### Réinitialiser la base en développement

```bash
docker compose --env-file .env -f docker-compose.yml down -v
docker compose --env-file .env -f docker-compose.yml up -d --build
```

Le script SQL d'initialisation est exécuté uniquement lorsque le volume MySQL
est créé pour la première fois.

## Lancement Python local

Dans le terminal :

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Pour lancer l'API en local, une base MySQL doit être accessible avec les
variables `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` et `DB_NAME` :

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

Nom d'hôte Raspberry : pi
user : admin
mdp : root

Commandes Rispi :

ping pi.local
ssh admin@pi.local

Dans terminal sur admin :

Se connecter au venv :
source hardware/.venv/bin/activate

Lancer prog :
python hardware/test_rfid.py