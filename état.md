
# BACK-END

#   Point   U   Fait    Ce qui manque

1) Register + confirmation U3
*60%*
POST /users OK (hash, 409 si doublon). Pas d'étape de confirmation, register ne renvoie pas de token

2) Auth credentials / OIDC U3
*90%*
Login + JWT + get_current_user + check du status OK. Pas de refresh token

3) OAuth 2.0 pour services tiers U3
*45%*
Discord complet. Steam = "not implemented" (auth/steam/steam.py) et router pas branché dans app.py

4) Lier un compte tiers à un user existant U3
*50%*
Discord lié via le state JWT. Steam rien. Pas de route pour délier un service

5) API d'abonnement aux services (+ tokens) U3
*20%*
Juste discord_id / steam_id / weather_id sur user. Le token Discord est jeté après le callback. Pas de route "mes services"

6) Fetchers de données par service U3
*15%*
/discord/me = copie figée au login (jamais rafraîchie). Steam 0. Météo appelée direct par le front (open-meteo), rien au back

7) Catalogue de widgets (params typés) U3
*50%*
WIDGET_CATALOG dans constants.py OK. Mais les 3 widgets steam ont params: [] → widgets NON comptés par le sujet. Pas de route GET /widgets. Pas de refresh_rate dans les params

8) Timer / scheduler (refresh rate par widget) U3
*0%*
Rien côté back (le refresh existe seulement côté front)

9) GET /about.json sur 8080 U3
*80%*
Route OK, port 8080 OK, host + time + services (WIDGET_CATALOG). Reste : params vides pour steam

10) Instances de widgets (grid) U3
*25%*
Module grid/ existe mais :
- create/delete réservés aux admins → un user normal ne peut pas sauver son dashboard
- GET /grid renvoie les widgets de TOUS les users (pas de filtre user_id)
- la table a user_id NOT NULL mais le INSERT ne l'envoie pas → le POST plante
- pas de params, pas de refresh_rate, pas de PATCH (reconfigurer / déplacer)
- le front sauve encore en localStorage

11) Validation des inputs widgets/services U3
*30%*
Pydantic OK pour user. Rien ne vérifie qu'un param respecte le type du catalogue (int / string)

12) Stockage sécurisé credentials/tokens U3
*70%*
PBKDF2 600k + compare_digest, secrets dans .env, state token séparé. Aucun token tiers stocké donc rien de chiffré. Faux email "@discord.local"

13) Admin API U1
*90%*
CRUD users + garde admin OK. Pas de moyen de créer le premier admin sans passer par la DB

14) Docker / docker-compose U3
*60%*
Backend sur 8080 OK. Healthcheck sur /health qui n'existe pas + pas de curl dans l'image alpine → toujours "unhealthy". dashboard.sql pas chargé au démarrage → sur une machine neuve, pas de tables. Pas de variables STEAM_* dans le compose

Moyenne back : ~50%


# DATABASE

1) Table user U3
*80%*
Il manque une colonne de confirmation (ex: is_verified)

2) Identités liées OAuth U3
*40%*
discord OK. steam = juste primary_id (pas de steamid, pseudo, avatar)

3) Table services U2
*0%*
Le catalogue est en dur dans constants.py (acceptable si on l'assume)

4) Table catalogue widgets U2
*0%*
Pareil, en dur dans constants.py

5) Table params des widgets U2
*0%*
Pareil, en dur dans constants.py

6) Abonnements user <-> service U3
*10%*
Juste les FK sur user, aucun token stocké

7) Instances de widgets U3
*30%*
Table grid (id, name, x, y, user_id) OK. Manque : params (json), refresh_rate. database.py n'a pas user_id dans la classe Grid

8) Sessions / tokens U2
*50%*
JWT stateless (acceptable)

9) Table audit admin U1
*0%*
Rien (optionnel)

10) Table weather U3
*0%*
Juste primary_id, sert à rien pour l'instant

Moyenne DB : ~20%


# TRANSVERSE (sujet)

1) Widget sans param = pas compté U3
3 widgets steam à 0 param → il faut leur en donner un (ex: steam_id, nb de jeux...)

2) 2 instances du même widget avec configs différentes U3
OK côté front (localStorage par index). Pas encore en base

3) Nombre de services / widgets U3
3 services (discord, steam, weather), 6 widgets. Règle : (1 + X) services, (3 × X) widgets → pour 3 étudiants il faut 4 services et 9 widgets

4) README U3
À vérifier : liste services/widgets, install, archi


# PRIORITÉS

1. Grid : fix le user_id, ouvrir create/delete aux users, filtrer par user, ajouter params + refresh_rate + PATCH
2. Docker : charger dashboard.sql au démarrage + fix healthcheck
3. Steam : login OpenID + /steam/me + donner des params aux widgets
4. Un 4e service si vous êtes 3
