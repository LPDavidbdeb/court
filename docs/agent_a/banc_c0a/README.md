# Banc C0-A — scripts conservés

Copies, **à l'octet près**, des deux scripts du banc de l'Agent B, prélevées le 20 octobre 2026 dans
`/private/tmp/court-agent-b-c0a-20261019-bmr16wwh/harness/`. Elles sont conservées ici parce que
`/private/tmp` est purgé par le système. Un déplacement vers `docs/architecture_c/lots/C0-A/` se
coordonne avec l'Agent B.

| Fichier | SHA-256 (identique à l'original) |
|---|---|
| `c0a_settings.py` | `557b256a23268e2993245bc6a95e4b4b025c0d9268ca937e1a25fe958f346bd8` |
| `run_tests.py` | `303886faefde84ead0381f3fd25344802097c024630c60503931dd474d93692d` |

**Ne pas les exécuter depuis ce répertoire.** Ils calculent leur racine par `Path(__file__).parents[1]`.
Exécutés ici, ils prendraient `docs/agent_a/` pour racine du banc.

## Contrôle de contenu (20 octobre)

- Toutes les valeurs de configuration sont synthétiques :
  - `SECRET_KEY = 'synthetic-c0a-only-not-a-production-key'` ;
  - clés d'IA à `'synthetic-disabled'` ;
  - mot de passe de base vide, authentification par socket local.
- Aucun identifiant réel, aucun jeton, aucun chemin vers `~/.env` ou vers les réglages `mysite.settings.*`.
- **Une seule mention de la base réelle**, `run_tests.py`, ligne 50 :
  `psycopg2.connect(host='/tmp', port='5432', user='c0a_runner', dbname='court_project_pg')`.
  - C'est une **contre-épreuve volontaire**. Elle s'exécute après l'installation de l'enveloppe de
    `psycopg2.connect`, et cette enveloppe doit la refuser avant `libpq`.
  - Si le refus n'a pas lieu, le script lève `RuntimeError` et s'arrête.
  - Chaque journal porte la ligne
    `ISOLATION: external PostgreSQL probe rejected before libpq; no .env; no TCP.`

## Fonction

**`c0a_settings.py`** : réglages Django autonomes. Il n'importe aucun module `mysite.settings`.
- `INSTALLED_APPS` et `MIDDLEWARE` ont été recopiés de P6 par lecture AST. `mysite/` est inchangé entre
  `212a7fe` et `515666e`.
- Base : `court_c0a` ; base de test : `test_court_c0a`.
- Rôle `c0a_runner`, socket `<racine>/socket`, port `55439`.
- Cache, courriel et stockage sont locaux.

**`run_tests.py`** : lanceur de tests. Il agit dans cet ordre :
1. Il journalise dans `<racine>/logs/<nom>.log`.
2. Il vide l'environnement du processus, puis le remplace par une liste explicite.
3. Il pose un crochet d'audit qui refuse :
   - l'ouverture de tout fichier `.env*` ;
   - l'import de `mysite.settings`, `.base`, `.local` et `.remote` ;
   - toute connexion réseau Python hors de `<racine>/socket/`.
4. Il enveloppe `psycopg2.connect` pour n'admettre que le socket privé, le port `55439`, le rôle
   `c0a_runner` et les bases `court_c0a`, `test_court_c0a` ou `postgres`.
5. Il exécute la contre-épreuve de la ligne 50.
6. Il lance `test <étiquettes> --keepdb`, en verbosité 2.
7. Avec l'étiquette `C0A_SCHEMA_CHECK`, il lance `makemigrations --check --dry-run` puis `check`.

## Dépendances et paramètres

**Arborescence du banc :**
- `<racine>/repo` : copie Git du code à tester ;
- `<racine>/harness` : les deux scripts ;
- `<racine>/socket`, en mode 700 ;
- `<racine>/logs`, `<racine>/tmp`, `<racine>/static`, `<racine>/media`.

**Logiciels :**
- Python 3.11.9 et les paquets du `.venv` du projet (222 paquets, Django 5.2.4, `psycopg2-binary` 2.9.11,
  `pgvector` 0.4.2). Seul `psycopg2` est installé : l'enveloppe couvre donc toutes les connexions de
  Django.
- PostgreSQL 18 (`/Library/PostgreSQL/18/bin`) avec l'extension `vector` 0.8.0, qui n'est pas
  « trusted ». Elle doit être créée dans `template1` par le superutilisateur du cluster jetable.

**Cluster jetable :**
- rôle `c0a_runner` : `LOGIN CREATEDB NOSUPERUSER` ;
- base `court_c0a` appartenant à ce rôle ;
- aucune écoute TCP.

**Utilisation :** `<racine>/venv/bin/python <racine>/harness/run_tests.py <nom-du-journal> <étiquettes…>`.
- Le nom du journal est alphanumérique, `-` et `_` admis.
- Sans étiquette, le lanceur exécute les 4 suites du rapport C0-A.

## Statut

**Fonctionnement démontré sur le socle `515666e`, sans le patch C0-A, le 20 octobre 2026**, dans un banc
neuf et avec les scripts non modifiés. Les usages démontrés sont :
- contrôle de schéma ;
- suite applicative complète par étiquettes de paquets ;
- suites d'outillage.

Procédure, commandes et résultats : `../PREPARATION_CHANTIER_C_2026-10-20.md`, partie C.

Limites constatées :
- **L'étiquette `.` (découverte depuis la racine) est incompatible avec le crochet d'audit.** La
  découverte importe le paquet `mysite.settings`, que le crochet refuse, ce qui ajoute une erreur
  d'import. Il faut passer les paquets explicitement.
- **`keepdb=True`** conserve la base de test d'une exécution à l'autre. Pour une référence, supprimer
  `test_court_c0a` avant chaque exécution.
- Les noms (`c0a_runner`, `court_c0a`, port `55439`) et les messages sont ceux de C0-A : le banc ne
  porte pas d'autre identité.

Les scripts ne sont pas validés au-delà de ces usages.
