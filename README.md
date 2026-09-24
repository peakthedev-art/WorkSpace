# WorkSpace
WorkSpace 2026

Système RFID : gestion des badges, rôles, zones et accès, avec une base MySQL,
une API Python, et une stack d'observabilité (Loki / Promtail / Grafana).

## Configuration Docker

### Première installation

Depuis la racine du projet, vérifier que Docker et Docker Compose sont
installés, puis copier le fichier d'environnement :

```bash
cp .env.example .env
```

Modifier ensuite `.env` et remplacer au minimum les mots de passe de
démonstration (`MYSQL_ROOT_PASSWORD`, `MYSQL_PASSWORD` et
`GRAFANA_ADMIN_PASSWORD`). Les valeurs utilisées par l'API, MySQL et Grafana
doivent rester cohérentes.

Lancer la base, l'API, Loki, Promtail et Grafana :

```bash
docker compose --env-file .env -f docker-compose.yml up -d --build
```

Attendre que MySQL soit sain et vérifier l'état des services :

```bash
docker compose ps
```

Le service `workspace-mysql` doit afficher `healthy`. Les services
`workspace-api`, `workspace-loki`, `workspace-promtail` et
`workspace-grafana` doivent être démarrés.

À cette étape, les scripts SQL sont exécutés automatiquement par MySQL :
`jeux_de_donnees/commandes.sql` crée le schéma et
`jeux_de_donnees/test_donnees.sql` insère les données de démonstration.

Services disponibles :

- API : http://localhost:8000
- Documentation API : http://localhost:8000/docs
- Loki : http://localhost:3100/ready
- Grafana : http://localhost:3000
- Dashboard RFID : http://localhost:3000/d/rfid-access/rfid-controle-des-acces

Identifiants Grafana de développement : `GRAFANA_ADMIN_USER` et
`GRAFANA_ADMIN_PASSWORD` définis dans `.env`.

Les logs de l'API sont écrits en JSON sur sa sortie standard. Promtail les
détecte depuis les conteneurs Docker et les envoie à Loki, en exposant les
labels `service`, `container`, `level` et `event`. Les événements
`http_request` et `access_decision` peuvent ainsi être recherchés directement
dans Loki. Grafana utilise automatiquement Loki comme source de données.

### Dashboard Grafana

Le dashboard `RFID - Controle des acces` est provisionné automatiquement avec
la datasource Loki. Il contient :

- les logs de l'API ;
- les décisions d'accès ;
- le nombre d'accès refusés et autorisés sur la période sélectionnée ;
- l'activité des requêtes HTTP dans le temps.

Ouvrir le lien du dashboard après la connexion Grafana. La période par défaut
est `Last 24 hours` et les panneaux se rafraîchissent toutes les 10 secondes.

### Initialiser les logs de test

Les logs synthétiques ne sont pas chargés par MySQL. Après le démarrage de
Loki, lancer séparément :

```bash
python3 jeux_de_donnees/generate_test_logs.py
```

Le script injecte 20 décisions d'accès réparties sur les dernières 24 heures,
dont 15 refus et 5 autorisations. Il est possible de le relancer pour ajouter
un nouveau jeu de logs.

Les journaux Docker sont envoyés automatiquement à Loki par Promtail.

> Si Loki, Promtail ou Grafana ne sont pas nécessaires temporairement, leurs
> blocs peuvent être commentés dans `docker-compose.yml`.

Pour arrêter les services :

```bash
docker compose --env-file .env down
```

## Base de données

Les identifiants RFID des badges et des rôles sont des entiers positifs de
exactement 12 chiffres (`100000000000` à `999999999999`). Ce format est
contrôlé par la base, l'ORM et les paramètres de l'API. Les identifiants des
utilisateurs et des zones restent des UUID textuels.

Le schéma et le jeu de données de démonstration sont chargés automatiquement
par MySQL au premier démarrage, via deux scripts montés dans
`/docker-entrypoint-initdb.d/` :

Les fichiers sont regroupés dans le dossier `jeux_de_donnees/` :

- `jeux_de_donnees/commandes.sql` : création des tables (`role`, `badge`,
    `user`, `zone`, `location`, `access_zone`) et des contraintes de clés
    étrangères.
- `jeux_de_donnees/test_donnees.sql` : jeu de données de test (rôles, zones,
    badges, utilisateurs et droits d'accès).
- `jeux_de_donnees/generate_test_logs.py` : génération de 20 événements de logs
    synthétiques dans Loki.

⚠️ Ces scripts ne s'exécutent **qu'une seule fois**, lorsque le volume
`mysql_data` est créé. Toute modification des fichiers SQL après un premier
lancement nécessite de réinitialiser la base (voir ci-dessous) pour être prise
en compte.

### Importer un autre jeu de données

Pour tester un jeu de données personnel sans modifier les fichiers fournis par
le projet, créer un fichier SQL dans `jeux_de_donnees/`, par exemple
`jeux_de_donnees/mon_jeu.sql`. Le fichier doit contenir les `INSERT` dans le
bon ordre : `role`, `zone`, `badge`, `user`, `access_zone`, puis `location`.
Les identifiants doivent respecter les contraintes du schéma et ne pas déjà
exister dans la base.

Démarrer MySQL, puis importer le fichier dans la base du conteneur :

```bash
docker compose --env-file .env up -d mysql
docker compose --env-file .env exec -T mysql \
    sh -c 'mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE"' \
    < jeux_de_donnees/mon_jeu.sql
```

Cette commande utilise les identifiants définis dans `.env` et fonctionne quel
que soit le nom de la base choisi par le collègue. Elle n'efface pas les
données déjà présentes : pour un import reproductible, utiliser de nouveaux
identifiants ou réinitialiser la base avant l'import.

Vérifier ensuite l'import avec une requête de comptage :

```bash
docker compose --env-file .env exec -T mysql \
    sh -c 'mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" \
    -e "SELECT COUNT(*) AS roles FROM role; SELECT COUNT(*) AS zones FROM zone; \
    SELECT COUNT(*) AS badges FROM badge; SELECT COUNT(*) AS utilisateurs FROM user;"'
```

Pour remplacer complètement le jeu de données de démonstration, modifier
`jeux_de_donnees/test_donnees.sql`, puis supprimer et recréer le volume MySQL
avant de relancer les services :

```bash
docker compose --env-file .env down -v
docker compose --env-file .env up -d --build
docker compose ps
```

Attendre que `workspace-mysql` soit `healthy` avant d'utiliser l'API. La
commande `down -v` supprime les données locales de MySQL, Loki et Grafana ; ne
pas l'utiliser sur un environnement contenant des données à conserver.

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
SELECT * FROM access_zone;
SELECT * FROM location;
```

Vérifier les droits d'accès par utilisateur (jointure complète) :

```sql
SELECT
    u.name, u.surname, r.name AS role, z.name AS zone_autorisee
FROM user u
JOIN badge b ON u.badge_id = b.id
JOIN role r ON b.role_id = r.id
JOIN access_zone za ON za.role_id = r.id
JOIN zone z ON za.zone_id = z.id
ORDER BY u.surname, z.name;
```

### Réinitialiser la base en développement

Cette procédure supprime les volumes Docker, donc la base MySQL, les logs
Loki et les données Grafana. Elle est adaptée à une nouvelle initialisation ou
à un environnement de développement uniquement.

```bash
docker compose --env-file .env -f docker-compose.yml down -v
docker compose --env-file .env -f docker-compose.yml up -d --build
```

Après cette réinitialisation, attendre que MySQL soit `healthy`, puis relancer
le générateur de logs si nécessaire :

```bash
docker compose ps
python3 jeux_de_donnees/generate_test_logs.py
```

Les scripts SQL d'initialisation sont exécutés uniquement lorsque le volume
MySQL est créé pour la première fois. Un simple `docker compose up -d` conserve
les données existantes et ne rejoue pas les scripts SQL.

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