# Régime des citations — l'instrument de non-régression

Ces scripts mesurent ce que l'ancien système fait des citations, avant et après
l'introduction du régime `HERITE` / `PHRASE`. Plan :
`docs/modele_preuve/PLAN_REGIME_CITATIONS.md` (§§ 1-3, 9, 10).

| Fichier | Rôle |
|---|---|
| `settings_clone_regime.py` | réglages du **clone** (base `court_quote_regime_clone`, ou `REGIME_CLONE_DB`) ; refuse la base réelle |
| `surfaces.py` | l'inventaire des surfaces, fixé ; haché dans chaque mesure |
| `projection.py` | la projection : ensembles, séquences, normalisations (module pur) |
| `empreinte.py` | la mesure : surfaces + services → `mesure.json` |
| `comparer.py` | le diff lisible entre deux mesures |
| `instantane_t11.py` | T1.1 : la migration ne touche aucune donnée existante |
| `test_projection.py` | les règles de la projection, éprouvées seules (T-C4, T-C5) |
| `bascule.sh` | **la bascule** : pilote, une étape par commande (`ouvrir`, `b1`…`b7`, `r1`…`r3`, `reparer-git`, `etat`) |
| `bascule_fonctions.sh` | ses contrôles : identité de la cible, connexions, instantanés (contenu, schéma, séquences, migrations), comparaisons à verdict |
| `bascule_fumee.py` | contrôle de fumée et vérification de la cible vue par Django |
| `settings_bascule.py` | réglages Django de la bascule : base explicite (`BASCULE_BASE`), base réelle sur confirmation seulement |
| `essai_bascule.sh` | banc d'essai de la bascule, sur des bases jetables `bascule_essai_*` |

Procédure de la bascule : `docs/modele_preuve/BASCULE_REGIME_ETAPE1.md`.

**Les sorties restent hors du dépôt** (`*.json` des mesures, dossiers d'état et
sauvegardes de la bascule) : ce sont des fichiers temporaires d'exécution.

## Reproduire une mesure

1. Restaurer la sauvegarde dans le clone (jamais la base réelle) :

   ```sh
   createdb court_quote_regime_clone
   pg_restore --no-owner -d court_quote_regime_clone ~/Backups/court/court_project_pg.dump
   ```

2. Depuis la racine de l'arbre de travail **à mesurer** :

   ```sh
   export PYTHONHASHSEED=0 PYTHONPATH=scripts/regime_citations DJANGO_SETTINGS_MODULE=settings_clone_regime
   python scripts/regime_citations/empreinte.py --base court_quote_regime_clone --sortie a.json
   python scripts/regime_citations/comparer.py a.json b.json
   ```

   Deux mesures ne se comparent que **depuis le même chemin d'arbre** : l'export
   docx écrit le chemin des photos absentes dans son texte. Et que si leur
   `liste_des_surfaces` concorde.

3. Autour de la migration (T1.1) :

   ```sh
   python scripts/regime_citations/instantane_t11.py --base court_quote_regime_clone instantane t11.json
   python manage.py migrate
   python scripts/regime_citations/instantane_t11.py --base court_quote_regime_clone comparer t11.json
   ```

Sûretés de `empreinte.py` : base vérifiée, transaction annulée (point de
sauvegarde par surface), réseau sortant bloqué, `PYTHONHASHSEED=0` exigé (l'ordre
des ensembles de chaînes en dépend : liste des participants d'un fil).

## La projection

Trois sortes de collections, et une règle générale pour les distinguer :

- **séquence sémantique** — l'ordre influence le rendu, une numérotation, une
  cote, une structure sérialisée ou un résultat métier : gardé tel quel, comparé
  rang par rang ;
- **collection non ordonnée** — seule la composition compte : triée,
  dédoublonnée ;
- **collection non consommée** par la surface — présente dans le contexte, mais
  ni la vue ni le gabarit ne l'a évaluée (un `QuerySet` dont le cache est vide
  après le rendu) : sa présence et son contenu sont contrôlés, son ordre non.
  L'instrument l'évalue lui-même ; l'ordre que la base lui donne alors est
  accidentel et n'est pas un comportement de la surface.

Rien n'est trié par défaut.

| Champ | Sorte | Ce qu'il retient |
|---|---|---|
| `statut`, `type`, `location` | valeur | la réponse |
| `ens_instanciees` | ensemble | citations et trames instanciées pendant la requête (signal `post_init`) — l'oracle de présence |
| `nb_instanciations` | valeur | combien d'instanciations, par modèle |
| `ens_contexte` | ensemble | citations et trames présentes dans le contexte de rendu, collections non consommées comprises |
| `seq_contexte` | **séquence** | les citations des collections **consommées**, dans l'ordre où la vue les remet au gabarit, à leur première rencontre (parcours en profondeur ; un `set` Python y est parcouru trié, il n'a pas d'ordre). L'ordre d'affichage est porté d'abord par `seq_marqueurs` et le HTML secondaire |
| `seq_marqueurs` | **séquence** | les citations désignées par le rendu, dans l'ordre du document : liens de fiche, `data-quote-id`, boutons `data-evidence-id` |
| `json` | **séquence** | empreinte du JSON ; les listes gardent leur ordre, les clés d'objet non |
| `texte` | **séquence** | empreinte d'une réponse texte non HTML |
| `docx_texte` | **séquence** | empreinte du texte de `word/document.xml` (métadonnées du fichier hors projection) |
| `longueur` | valeur | autres binaires |
| services `ens_registre`, `ens_rattrapage…`, `table_*`, `liaison_*`, `ens_instanciees` | ensemble | ce qui est inscrit, sélectionné, stocké |
| services `seq_pieces_produites`, `seq_chronologie` | **séquence** | pièces dans l'ordre de leur numérotation ; chronologie de preuve d'une trame |
| secondaire `html` | **séquence** | empreinte du HTML normalisé entier (hors pages 5xx) — la sonde la plus stricte |

**Historique de la règle.** La première version de l'instrument mettait dans
`seq_contexte` l'ordre de **tout** queryset du contexte, qu'il l'évalue lui-même ou
non. Elle a signalé quatre fiches de protagoniste divergentes entre les états A et
B : la vue y place `email_quotes`, trié par date du courriel, que ni le gabarit ni
ses inclusions ne lisent. Les citations d'un même courriel y sont à égalité de
date, et l'ordre de ces égalités suit le plan d'exécution. La règle des
collections non consommées a été précisée avant la mesure finale ; la vue n'a pas
été modifiée.

Hors projection, et contrôlé ailleurs : la colonne `regime` des tables de
citations (elle n'existe pas avant la migration ; `instantane_t11.py` en compte
les valeurs).

## Les normalisations autorisées

Trois, et aucune autre sans justification écrite ici **avant** usage :

1. **Jetons CSRF** — 64 caractères alphanumériques, tirés à chaque rendu.
2. **Anti-cache du visionneur PDF** — `?v=<time.time()>` (`ajax_get_pdf_viewer`).
3. **PK d'un objet temporaire désigné par une redirection** — `manage-perjury`
   crée un `PerjuryArgument` puis y redirige ; la transaction est annulée mais la
   séquence PostgreSQL avance. Seule une PK qui **n'existe plus après
   l'annulation** est remplacée ; une PK existante est gardée telle quelle.

Les pages d'erreur 5xx ne contribuent pas au HTML secondaire (trace de débogage,
adresses mémoire) ; leur statut et leurs champs canoniques restent mesurés.
