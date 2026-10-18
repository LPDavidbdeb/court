# Bascule de l'étape 1 du régime des citations sur la base réelle — plan exécutable

**Version 2 (2026-10-18).** Corrige la version 1 après la revue indépendante : corrections I1 à I9,
réglages Django explicites du contrôle de fumée, identité de la cible, intégrité du schéma, sûreté du
contrôle de fumée, incident après réouverture. **Statut : non exécuté sur la base réelle.** Toutes les
procédures ont été éprouvées sur des bases jetables (§ 11). Prochaine étape soumise à autorisation :
la répétition générale P6 (§ 12). Validation qui précède : `PLAN_REGIME_CITATIONS.md`, § 10.4.

---

## 0. Ce qui bascule

**Code.** `epic/E01-numerotation-concordance` avance, **par avance rapide**, de `14f7533` à la pointe de
`integration/quote-regime-step1`. Cette pointe contient :
- `4b53e83` — **la référence validée** : le merge de `5fa62ed` (ordre des affidavits), `b45808c`
  (régime) et `11214d1` (instrument), éprouvé sur le clone (empreinte `64def7f9…`) ;
- au-delà de `4b53e83`, **uniquement** des fichiers de `docs/` et de `scripts/regime_citations/` :
  ce plan et son outillage. Aucun code de l'application.

`bascule.sh ouvrir` refuse toute cible qui ne contient pas `4b53e83`, qui n'a pas `14f7533` pour
ancêtre, ou qui modifie, depuis `4b53e83`, un fichier hors de ces deux dossiers.

**Base.** Exactement deux migrations, `email_manager.0009_quote_regime` et
`pdf_manager.0009_quote_regime`. Sur chacune des deux tables de citations, elles ajoutent :
- la colonne `regime`, `varchar(6)`, NOT NULL, sans défaut en base ;
- sa contrainte NOT NULL (PostgreSQL 18 l'inscrit dans `pg_constraint`, sous le nom `<table>_regime_not_null`) ;
- deux index Django (btree, et `varchar_pattern_ops`).

Les citations existantes sont classées `HERITE`.

**Effets visibles attendus.** L'administration des citations (O1.6). Dans les affidavits, l'ordre des
citations PDF d'une même pièce devient l'ordre de lecture (23 trames, § 10.1 du plan du régime).

---

## 1. L'outillage

Tout est dans `scripts/regime_citations/` (versionné) :

| Fichier | Rôle |
|---|---|
| `bascule.sh` | le **pilote** : une étape par commande, préconditions, verdict, code de sortie |
| `bascule_fonctions.sh` | ses contrôles : identité de la cible, connexions, processus, instantanés, comparaisons |
| `bascule_fumee.py` | le contrôle de fumée, et l'identité de la cible vue par Django |
| `settings_bascule.py` | les réglages Django de la bascule : base explicite, base réelle sur confirmation seulement |
| `essai_bascule.sh` | le banc d'essai : chemin nominal et scénarios d'échec sur des bases jetables |

**Principes :**
1. **bash exigé (I1).** Le pilote et la bibliothèque refusent de tourner sous un autre shell :
   message `ÉCHEC`, code 1. Ils sont compatibles avec bash 3.2, celui de macOS.
2. **Verdicts automatiques (I2).** Chaque contrôle affiche `OK` ou `ÉCHEC`. Chaque étape rend 0 si
   tout est conforme, 1 sinon. Aucune décision ne repose sur la lecture d'un `diff`. Les requêtes
   tournent avec `ON_ERROR_STOP`, les pipelines avec `pipefail` ; le contrôle de contenu des tables
   tient en une seule requête, et toute erreur la fait échouer.
3. **État et journal (I3).** `ouvrir` crée un dossier privé (mode 700). Il contient :
   - `etat.env` : horodatage, nature, base, hôte, port, identifiant du serveur, arbre, branche,
     SHA avant / après, sauvegarde, base de référence, étape atteinte, réouverture ;
   - `journal.log` : toute la sortie, horodatée.

   **Aucun secret** : le mot de passe passe par `PGPASSWORD`, lu dans `~/.court-backup.env` sans
   sourcer le fichier (qui porte aussi `DB_NAME`, et ne doit jamais décider de la cible) ; il n'est
   jamais écrit. Vérifié sur les fichiers produits par le banc (§ 11).
4. **Cible explicite (I9, 4.1).** La cible est fixée une fois par `ouvrir`, puis revérifiée avant
   chaque opération critique, par psql **et** par Django : base (`current_database`), port
   (`inet_server_port`) et identifiant système du serveur (`pg_control_system`).
   - Pour la base réelle, chaque commande exige `BASCULE_REELLE_CONFIRMEE=oui`. La nature `essai`
     refuse le nom, l'arbre et la branche réels.
   - `pg_dump` et `pg_restore` prennent hôte, port et utilisateur des mêmes variables, et le nom de
     base inscrit dans la sauvegarde est vérifié.
5. **Django en environnement propre (point 3 de la revue).** Chaque appel Python passe par `env -i`,
   avec uniquement :
   - `HOME`, `PATH`, `LANG=en_CA.UTF-8` (celui du serveur 8000) ;
   - `DJANGO_SETTINGS_MODULE=settings_bascule`, `PYTHONPATH=<dossier de l'outil>` ;
   - `BASCULE_BASE`, `BASCULE_PORT`, `BASCULE_SYSID`, `BASCULE_REELLE_CONFIRMEE` ;
   - `PGOPTIONS=-c lock_timeout=10s`.

   Aucune variable du terminal n'entre. Le banc d'essai lui-même est lancé par
   `env -i … bash --noprofile --norc`. Sans ces variables, `bascule_fumee.py` refuse de tourner
   (code 2) : il ne devine rien.
6. **Verrous et connexions (I4).** Avant la sauvegarde, avant les migrations, avant R2 et R3 :
   aucune autre connexion ne doit être ouverte sur la base, sinon `ÉCHEC`. Le pilote liste alors les
   connexions (pid, application, adresse, depuis) et les processus clients (`lsof`), et n'en termine
   aucune. Toute attente de verrou par une migration est bornée à 10 s (`lock_timeout`) ; au-delà,
   la migration échoue proprement, sans rien appliquer.

---

## 2. Faits relevés (2026-10-18, lecture seule)

| Fait | Valeur |
|---|---|
| Serveur | `runserver 0.0.0.0:8000`, terminal `ttys000`, parent 45849 (16 août), enfant 28428, dossier `court/`, `LANG=en_CA.UTF-8` |
| Autres processus Python dans un arbre `court*` | **le serveur isort de l'extension VS Code** (pid 6993, interpréteur `court/.venv`) ; B1 le refusera : **fermer VS Code** pendant la fenêtre |
| Autres applications | `finance_agent` (serveur 8001, workers Celery, Redis) : base `finance` seulement |
| Connexions à `court_project_pg` | aucune au relevé |
| Rôles, droits | un seul rôle de connexion, `postgres` (superutilisateur), propriétaire de tout ; aucun droit explicite ; aucun réglage propre à la base |
| Schéma | `public` seul ; 88 tables, 86 séquences ; aucune vue ni déclencheur utilisateur ; 118 fonctions, toutes de l'extension `vector` 0.8.0 |
| Encodage, collation | `UTF8` / `C` pour la base réelle, `template1` et les copies |
| Colonne `id` des citations | identité `GENERATED BY DEFAULT` |
| Migrations manquantes en base réelle | exactement les deux `0009_quote_regime` |
| Sauvegarde automatique | `com.court.backup-db` à 01 h 00 ; elle écrase `court_project_pg.dump` |

**Contrainte du retour arrière (vérifiée).** Sur une base migrée, l'ancien code ne peut plus créer de
citation : `regime` est NOT NULL sans défaut en base. D'où la règle : **la base d'abord, le code
ensuite**. `bascule.sh r1` refuse de ramener l'ancien code tant que la base porte une migration
`0009` ou une colonne `regime`.

---

## 3. Préalables (GO / NO-GO)

Tous vrais, sinon pas de bascule :

1. **P6 réussie**, sur une copie fraîche de la base réelle (§ 12).
2. `epic/E01-numerotation-concordance` est encore à `14f7533`, et l'arbre principal est propre.
   Sinon, l'avance rapide est impossible : refaire le merge dans la branche d'intégration et la
   revérifier.
3. `integration/quote-regime-step1` est poussée, et sa pointe ne modifie, depuis `4b53e83`, que
   `docs/` et `scripts/regime_citations/` (`ouvrir` le vérifie).
4. La fenêtre est à plus d'une heure de 01 h 00, avec plus de 1 Gio libre.
5. Les sessions Claude et tout script sont en pause, et VS Code est fermé.
6. Personne n'utilise l'application pendant la fenêtre (environ 20 minutes).

---

## 4. La fenêtre de bascule

Dans un terminal **bash**, depuis l'arbre de l'outil (branche d'intégration, propre) :

```bash
cd /Users/Louis-Philippe/Documents/GitHub/court-quote-regime
export BASCULE_REELLE_CONFIRMEE=oui
B="bash scripts/regime_citations/bascule.sh"

$B ouvrir --nature reelle --base court_project_pg --arbre /Users/Louis-Philippe/Documents/GitHub/court \
          --branche epic/E01-numerotation-concordance --vers integration/quote-regime-step1
ETAT=<dossier affiché>/etat.env       # ~/Backups/court/regime_etape1/bascule_reelle_<horodatage>/etat.env
```

Puis, **dans l'ordre, une commande à la fois** ; on ne passe à la suivante que sur `=== … : OK` :

| Étape | Commande | Ce qu'elle vérifie ou fait | En cas d'échec |
|---|---|---|---|
| — | arrêter le serveur 8000 : **Ctrl-C dans `ttys000`** (ou `kill -INT 45849`) ; fermer VS Code | — | — |
| B1 | `$B b1 --etat "$ETAT" --sessions-en-pause` | cible ; port 8000 fermé ; aucun processus Python dans un arbre `court*` ; aucune connexion | corriger la cause, relancer B1 ; rien n'a changé |
| B2 | `$B b2 --etat "$ETAT"` | sauvegarde fraîche et distincte (`avant_bascule.dump`, somme SHA-256 notée), nom de base vérifié dans l'archive ; restauration complète dans `court_project_pg_ref_<horodatage>` ; **référence identique à la base** (structure, contenu des 88 tables, séquences, migrations) ; nombres de citations notés | abandon : rien n'a changé ; redémarrer le serveur |
| B3 | `$B b3 --etat "$ETAT"` | branche et HEAD inchangés depuis `ouvrir`, arbre propre ; avance rapide vers la pointe notée ; HEAD et propreté vérifiés | `etat` ; `reparer-git` si l'arbre est sale ; sinon R1 |
| B4 | `$B b4 --etat "$ETAT"` | cible vue par Django ; `check` ; plan de migration **exactement** les deux `0009` ; `makemigrations --check` | R1 |
| B5 | `$B b5 --etat "$ETAT"` | aucune connexion ; cible ; `migrate email_manager 0009`, puis `pdf_manager 0009`, chacune atomique, attente de verrou bornée à 10 s | le pilote diagnostique : aucune `0009` → R1 ; sinon R2 |
| B6 | `$B b6 --etat "$ETAT"` | voir ci-dessous | R2 |
| — | redémarrer : `cd /Users/Louis-Philippe/Documents/GitHub/court && .venv/bin/python manage.py runserver 0.0.0.0:8000` | — | — |
| B7 | `$B b7 --etat "$ETAT"` | port à l'écoute ; page de connexion en HTTP 200 ; **réouverture notée** | voir § 6 |

**B6, sans intervention humaine :**
1. Cible, connexions, `migrate --check`.
2. Comparaison avec la référence B2, sur la liste explicite des changements permis par les deux `0009` :

   | Objet | Changement permis | Tout autre écart |
   |---|---|---|
   | structure | +2 colonnes `regime` `varchar(6)` NOT NULL sans défaut, +2 contraintes `<table>_regime_not_null`, +4 index `<table>_regime_<hash>` et `…_like` sur `(regime)` | ÉCHEC |
   | migrations | +2 lignes : `email_manager.0009_quote_regime`, `pdf_manager.0009_quote_regime` | ÉCHEC |
   | contenu des 88 tables (colonnes d'origine) | seule `django_migrations` change, de +2 lignes | ÉCHEC |
   | séquences | seule `django_migrations_id_seq` avance (≥ 2) | ÉCHEC |

3. Comptes par régime : tout `HERITE`, mêmes nombres qu'en B2.
4. Contrôle de fumée (§ 9).
5. Nouvel instantané : **identique** à celui d'avant la fumée (contenu, structure, séquences,
   migrations). La fumée n'a laissé aucune trace durable.

Il n'y a plus d'écriture réelle en B7 (I6) : l'écriture de l'ancien régime est éprouvée par le
contrôle de fumée, dans une transaction annulée, sans consommer de séquence. Les chemins de création
sont aussi couverts par les tests de l'application (T1.7).

---

## 5. Retour arrière pendant la fenêtre (écritures immobilisées)

**Ordre impératif : la base d'abord (R2 ou R3), le code ensuite (R1).** `r1` le garantit. Pour
choisir : `$B etat --etat "$ETAT"` affiche HEAD (avant / après), la propreté de l'arbre, les bases
présentes, les `0009` appliquées, les colonnes `regime` et les connexions.

| Situation (diagnostic `etat`) | Procédure | Préconditions vérifiées par le pilote | Réussite |
|---|---|---|---|
| Base intacte, code avancé (échec en B3, B4, ou B5 sans aucune `0009`) | **R1** `$B r1 --etat "$ETAT"` | base : 0 `0009`, 0 colonne `regime` ; arbre propre ; HEAD = après (ou déjà avant) | HEAD = `14f7533`, arbre propre |
| Une `0009` appliquée sur deux (migration partielle) | **R2**, puis **R1** | HEAD = nouveau code ; cible ; aucune connexion ; Django vise la bonne base | structure, migrations et contenu identiques à la référence B2 ; seule la séquence de `django_migrations` reste avancée |
| Les deux appliquées, contrôle B6 en échec | **R2**, puis **R1** ; si R2 échoue, **R3** | idem | idem |
| Le nouveau code ne peut plus lancer Django (import impossible) | **R3**, puis **R1** (R2 exige Django) | aucune connexion sur la base **et** sur la référence ; référence encore identique à B2 (instantané comparé) | la base porte le nom réel et est identique à B2 en tout, séquences comprises ; l'ancienne base est gardée sous `court_project_pg_echec_<horodatage>` |
| Doute sur les données (écart de contenu inexpliqué) | **R3**, puis **R1** | idem | idem |
| Avance rapide interrompue (HEAD à avant ou après, arbre sale) | **reparer-git**, puis reprise | toute modification doit appartenir à l'avance rapide (`git diff avant..après`) ; sinon refus, examen à la main | arbre propre, HEAD inchangé |
| R3 interrompu entre ses deux renommages | **relancer r3** : il reprend au second | référence présente ; base renommée en `…_echec_…` | idem R3 |
| Connexion résiduelle pendant un retour arrière | arrêter le processus à sa source (le pilote l'identifie), relancer | — | le contrôle de connexion passe |

**Après R1**, redémarrer le serveur (commande affichée par `r1`). La sauvegarde B2, la base de référence
(ou la base en échec) et le journal sont gardés.

**Interruption de la procédure** (terminal fermé, panne) : rouvrir un terminal bash, `cd` vers l'arbre de
l'outil, `export BASCULE_REELLE_CONFIRMEE=oui`, `B=…`, retrouver `etat.env` dans
`~/Backups/court/regime_etape1/bascule_reelle_<horodatage>/`, puis `$B etat --etat "$ETAT"`.

- **Chaque étape est rejouable** ou refuse explicitement : B2 refuse si la sauvegarde ou la référence
  existe déjà, et ces deux objets se suppriment à la main après examen.
- **Chaque migration est atomique** : une `0009` est appliquée en entier ou pas du tout.
- **L'étape atteinte** est dans `etat.env`.

---

## 6. Incident découvert après la réouverture (4.4)

Après B7, des écritures **légitimes** ont pu avoir lieu. La référence B2 ne décrit plus les données : la
restaurer ferait perdre ces écritures.

1. **Diagnostiquer d'abord.** Établir le défaut et sa portée, puis `etat`. Arrêter le serveur si le
   défaut risque d'abîmer des données.
2. **Retour de structure, sans perte : R2.** `r2` le fait automatiquement quand l'état indique la
   réouverture. Il défait les deux `0009` et garde toutes les données écrites depuis. Ses critères
   portent alors sur la **structure** (schéma, colonnes, migrations identiques à la référence), pas
   sur le contenu ni les séquences. Puis R1.
3. **Restauration avec perte : R3, seulement sur décision explicite.** `r3` refuse après la réouverture,
   sauf avec `--perte-acceptee`. Il sauvegarde alors d'abord l'état rouvert
   (`apres_reouverture_<horodatage>.dump`), pour que les écritures perdues restent récupérables.
   Cette décision revient à LP, après le diagnostic.

**Éprouvé** (scénario S-E, § 11) : une écriture faite après la réouverture survit à R2 ; R3 refuse sans
décision explicite.

---

## 7. L'immobilisation des écritures (I7)

| Source | Détection | Prévention, maintien |
|---|---|---|
| Serveur 8000 (rechargement automatique) | B1 : port fermé (`lsof`) | arrêté **avant** l'avance rapide ; redémarré seulement après B6, ou après R1 |
| Tout processus Python lancé dans un arbre `court*` : serveur, `manage.py shell`, scripts, extension VS Code, arbre `court-quote-regime-avant` (ancien code) | B1 : `processus_projet` (dossier de travail de chaque processus) | B1 refuse tant qu'il en reste ; l'arbre `-avant` reste sur disque, et le risque — son exécution contre la base migrée — est couvert par ce contrôle |
| Sessions Claude Code (3 processus au relevé) | comptées en B1 | mises en pause par LP ; `--sessions-en-pause` est exigé |
| Connexions PostgreSQL | `pg_stat_activity` avant B2, B5, B6, R2 et R3 | refus ; jamais de fin de connexion forcée par le pilote |
| Sauvegarde automatique (01 h 00) | heure | fenêtre loin de 01 h (préalable 4) |
| `finance_agent`, Redis | base `finance` | sans objet |
| Écriture concurrente non détectée en amont | **B6** : toute modification d'une colonne d'origine, dans n'importe laquelle des 88 tables, entre B2 et B6 | ÉCHEC, puis R3 (la base en échec garde l'écriture pour analyse) |

**Limite déclarée** : le seul rôle de connexion est le superutilisateur `postgres`, que l'application
utilise aussi. PostgreSQL ne peut donc pas refuser les autres connexions sans refuser celles de la
bascule. L'immobilisation est procédurale, contrôlée à chaque étape sensible, et vérifiée après coup
par B6.

---

## 8. Les contrôles d'intégrité (4.2)

**Instantané d'une base** (`instantane`), écrit en fichiers dans le dossier d'état :

| Fichier | Contenu | Compare |
|---|---|---|
| `.colonnes` | colonnes de chaque table, dans l'ordre de déclaration | ajout, retrait, renommage, déplacement |
| `.md5` | par table : nombre de lignes, et md5 de la concaténation des lignes `row(colonnes)::text`, triées (collation `C`), sur les colonnes **de la référence** | toute valeur, ligne ajoutée ou retirée ; NULL / vide |
| `.schema` | colonnes (type, NOT NULL, défaut, identité), contraintes (définition), index (définition), séquences (type, pas, bornes, cycle), extensions (version) | toute différence de structure |
| `.seqv` | dernière valeur de chaque séquence | avance ou recul |
| `.mig` | `django_migrations` (application, nom) | migrations ajoutées ou retirées |

**Ce qui n'est pas comparé** : les droits et propriétaires (un seul rôle, aucun droit explicite), les
commentaires, les statistiques, l'ordre physique des lignes.

**Les séquences** :
- **B2** : identiques (la restauration rejoue `setval`).
- **B6** : seule celle de `django_migrations` avance. Le contrôle exige une avance minimale, non
  exacte : une séquence ne recule jamais, et une migration échouée puis rejouée peut consommer une
  valeur. Les lignes de `django_migrations`, elles, sont contrôlées exactement.
- **R2** : seule celle de `django_migrations` reste avancée.
- **R3** : identiques à B2.

**La référence** est une restauration complète de la sauvegarde B2. Son identité avec la base réelle
au moment de B2 prouve la sauvegarde. Elle sert ensuite de référence à B6 et R2, et de base de secours
à R3.

---

## 9. Le contrôle de fumée (4.3)

`bascule_fumee.py fumee`, lancé par B6 :

1. **Cible** : réglage Django et connexion — base, port, identifiant du serveur.
2. **Garde-fous éprouvés au départ**, chacun par un essai qui doit échouer :
   - réseau sortant bloqué, à la résolution de nom puis à la connexion (PostgreSQL passe par libpq,
     en C, et n'est pas concerné) ;
   - toute écriture de fichier par un stockage Django refusée.
3. **Comptes** :
   - citations au total égales aux nombres de B2 ;
   - toutes visibles par l'ancien système (`objects`) ;
   - aucune `PHRASE` ;
   - aucune ligne dont le régime n'est pas `HERITE`.
4. **Dans une transaction annulée** :
   - connexion d'un superutilisateur ; GET de 14 pages (accueil, liste des citations, courriel, fil,
     fiche de citation, PDF, citation PDF, trame, affidavit, liste TinyMCE, deux listes
     d'administration) : toutes en HTTP 200 ;
   - filtre `PHRASE` de l'administration : 0 citation ;
   - **écriture de l'ancien régime** : une citation de courriel et une citation PDF créées par l'ORM
     avec une PK explicite, hors de la plage existante. Elles doivent être `HERITE` et visibles par
     l'ancien système. La PK explicite ne consomme pas la séquence d'identité.
5. **Après l'annulation** : les deux citations d'essai n'existent plus.

**Résultat** : 0 si tout est conforme, 1 si un contrôle échoue, 2 si le contrôle n'a pas pu s'exécuter.
**Aucune trace durable** : B6 compare la base avant et après la fumée — contenu, structure,
séquences, migrations. Éprouvé (§ 11).

---

## 10. Git

- **Référence validée** : `4b53e83`, merge de `feat/quote-regime-step1` dans la branche d'intégration.
- **Pointe de la branche d'intégration** : `4b53e83` plus les commits de l'outillage de la bascule
  (ce plan, les scripts). Poussée vers `origin/integration/quote-regime-step1`.
- **Avance rapide** : possible tant que `epic/E01-numerotation-concordance` reste à `14f7533`, ancêtre de
  la pointe. `ouvrir` et B3 le vérifient.
- **Rien n'est commité sur `epic/E01`** d'ici la bascule.

---

## 11. Ce qui a été éprouvé (2026-10-18)

**Banc d'essai** `essai_bascule.sh` :
- lancé depuis un environnement vide (`env -i … bash --noprofile --norc` : ni `DJANGO_SETTINGS_MODULE`,
  ni `PYTHONPATH`, ni `LANG`) ;
- sur des bases jetables restaurées de la sauvegarde nocturne du 18 oct. (01 h 01) ;
- avec un arbre de travail et une branche temporaires, partant de `14f7533` et avançant vers la
  branche d'intégration.

**Résultat : 52 contrôles réussis, 0 raté.**

| Scénario | Contrôles |
|---|---|
| **S-A** chemin nominal | B1 à B6 réussis. Dans B6 : structure conforme à la liste permise ; +2 lignes de migrations ; 268 + 126 citations HERITE ; garde-fous réseau et fichiers éprouvés ; écritures d'essai HERITE et visibles, puis annulées ; **aucune trace durable**. La fumée avec de faux comptes échoue (code 1) ; sans environnement explicite, elle refuse de tourner (code 2). **R1 refusé** tant que la base porte le régime ; R2, puis R1, ramènent la base et le code à l'état d'avant |
| **S-F** avance rapide interrompue | B3 refuse un arbre sale ; `reparer-git` refuse une modification étrangère à l'avance, puis remet l'arbre propre (y compris un fichier ajouté à l'index) |
| **S-B** R3 | R3 refusé avec une connexion ouverte sur la référence ; **interruption simulée** après le premier renommage : `r3` reprend et la base est identique à B2 en tout ; puis R1 |
| **S-C** migration partielle | `email_manager` seule : B6 refusé ; R2, puis R1 |
| **S-D** connexion et verrou | B5 refusé (connexion ouverte) ; sans ce contrôle, la migration est arrêtée par `lock_timeout` (« canceling statement due to lock timeout », 17 s en tout), aucune `0009` appliquée, diagnostic « R1 » ; verrou levé, B5 réussit ; puis R2 et R1 |
| **S-E** incident après réouverture | B7 simulé ; une écriture légitime ; R3 refusé sans décision ; R2 réussit et **l'écriture est conservée** ; R1 |
| **S-G** contrôles isolés | `md5_tables` échoue sur une table inexistante ; `verifier_cible` détecte un serveur différent ; `settings_bascule` refuse la base réelle sans confirmation, avant toute connexion ; `ouvrir --nature reelle` refusé sans confirmation ; `processus_projet` détecte les processus des arbres (serveur 8000 et extension VS Code) |
| Nettoyage | aucune base d'essai restante ; arbre et branche d'essai supprimés ; base réelle intacte (aucune `0009`, aucune colonne `regime`, en lecture seule) |

Également vérifié : aucun fichier d'état, de journal ni d'instantané ne contient le mot de passe
(recherche sur la valeur elle-même).

**Non éprouvé, et pourquoi :**
- **Les branches propres à la nature `reelle`** : contrôle du port 8000, refus des processus,
  redémarrage et B7 réel. Les éprouver exige d'arrêter le serveur. Les fonctions sous-jacentes sont
  éprouvées : détection des processus, refus de la nature réelle sans confirmation.
- **B2 sur une sauvegarde fraîche de la base réelle** : c'est l'objet de P6.

---

## 12. P6 — répétition générale (protocole prêt, à autoriser séparément)

**Préconditions** : autorisation distincte ; ce plan poussé ; branche d'intégration propre dans
`../court-quote-regime` ; serveur 8000 laissé en marche ; plus de 2 Gio libres.

**Effets** :
- une lecture de la base réelle : `pg_dump`, verrous de lecture brefs, aucune écriture ;
- `court_quote_regime_clone` écrasé ;
- des bases `bascule_essai_*`, un arbre `../court-p6-mesure`, et l'arbre et la branche temporaires du
  banc : tous créés puis supprimés ;
- **aucun effet** sur `court/`, `epic/E01`, le serveur ou la base réelle.

**Durée** : 60 à 75 minutes.

```bash
I=/Users/Louis-Philippe/Documents/GitHub/court-quote-regime          # outil (branche d'intégration)
C=/Users/Louis-Philippe/Documents/GitHub/court                       # dépôt (arbre principal, non modifié)
PY=$C/.venv/bin/python
P6=~/Backups/court/regime_etape1/p6_$(date +%Y%m%d-%H%M%S); mkdir -p "$P6"; chmod 700 "$P6"
. $I/scripts/regime_citations/bascule_fonctions.sh && charger_identifiants      # dans un terminal bash

# 1. Sauvegarde fraîche de la base réelle (lecture seule)
"$PG_BIN/pg_dump" -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" -Fc -f "$P6/source.dump" court_project_pg

# 2. Banc d'essai complet sur cette copie, environnement vide
env -i HOME="$HOME" PATH=/usr/bin:/bin:/usr/sbin:/sbin bash --noprofile --norc \
  "$I/scripts/regime_citations/essai_bascule.sh" --dossier "$P6/banc" --source "$P6/source.dump" > "$P6/banc.log" 2>&1
tail -1 "$P6/banc.log"                                                   # → « bilan : N réussi(s), 0 raté(s) »

# 3. Empreintes A et B sur cette copie : même arbre pour A et B, outil figé de la branche d'intégration
"$PG_BIN/dropdb" -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" --if-exists court_quote_regime_clone
"$PG_BIN/createdb" -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" court_quote_regime_clone
"$PG_BIN/pg_restore" -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" -d court_quote_regime_clone --no-owner --exit-on-error "$P6/source.dump"
git -C "$C" worktree add --detach "$C/../court-p6-mesure" 5fa62ed                  # état A : historique + ordre
sed 's/^DB_NAME=.*/DB_NAME=court_quote_regime_clone/' "$C/.env" > "$C/../court-p6-mesure/.env"
chmod 600 "$C/../court-p6-mesure/.env"
cd "$C/../court-p6-mesure"
export PYTHONHASHSEED=0 PYTHONPATH="$I/scripts/regime_citations" DJANGO_SETTINGS_MODULE=settings_clone_regime
"$PY" "$I/scripts/regime_citations/empreinte.py" --base court_quote_regime_clone --sortie "$P6/A.json"
git checkout -q --detach integration/quote-regime-step1                             # état B : la pointe
"$PY" "$I/scripts/regime_citations/instantane_t11.py" --base court_quote_regime_clone instantane "$P6/t11.json"
"$PY" manage.py migrate
"$PY" "$I/scripts/regime_citations/instantane_t11.py" --base court_quote_regime_clone comparer "$P6/t11.json"
"$PY" "$I/scripts/regime_citations/empreinte.py" --base court_quote_regime_clone --sortie "$P6/B.json"
"$PY" "$I/scripts/regime_citations/comparer.py" "$P6/A.json" "$P6/B.json" > "$P6/comparaison.txt"
cd "$I"; git -C "$C" worktree remove --force "$C/../court-p6-mesure"
unset PYTHONHASHSEED PYTHONPATH DJANGO_SETTINGS_MODULE
```

**Critères de réussite de P6 :**
1. Banc d'essai : 0 raté, sur la copie fraîche.
2. T1.1 : seule la colonne `regime` est nouvelle ; tables identiques sur les colonnes d'origine ;
   toutes les citations sont `HERITE`.
3. A → B : **surfaces et services identiques** ; HTML secondaire différent seulement sur
   `/admin/argument_manager/tramenarrative/<pk>/change/` ; mêmes erreurs 500.
4. Aucune base `bascule_essai_*` restante, `../court-p6-mesure` supprimé, base réelle intacte
   (aucune `0009`, aucune colonne `regime`).

Si un critère échoue : arrêt et rapport, sans bascule.

---

## 13. Hors du périmètre

Aucune citation `PHRASE` ; pas d'étape 2 ; aucune correction des 24 erreurs 500 préexistantes ; aucune
modification de la sauvegarde automatique ni du serveur en dehors de la fenêtre.
