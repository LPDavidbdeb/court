# Rapport d'exécution — Epic E01

Numérotation fidèle et concordance de la demande modifiée.

---

## 4.1 Résultat et identification

    Epic                     : E01
    Date d'exécution         : 14 octobre 2026, 03 h 40 – 04 h 30 (UTC−4)
    Dépôt                    : https://github.com/LPDavidbdeb/court
    Branche                  : epic/E01-numerotation-concordance
    Commit de départ         : dae8da2d8713d9851ae34161dfb82cbaff924bca
    Commit livré             : (celui de cette branche — voir git log)
    État global              : PARTIEL

    Référent source contrôlé : source archivée identifiée
                               legal/demande_DEPOT_2026-07-21.md
                               sha256 0f141193300fed121bf9e3d2a69a3cc66018f2fe29b164274763ce8c19db078d
                               — identique à l'empreinte déclarée par la table
                               de concordance publiée.
                               Table : concordance_md_imprime.json
                               sha256 b916599815e7f40264caae52340cd5bf6dbcbabe1f380e298ecdeabd139963d1
                               Candidat imprimé déclaré par la table :
                               demande_DEPOT_2026-07-21.docx
                               sha256 6f1818262835e9c0adbcbec3a282adc624431bdd93902c48b506832842971d3b
                               — vérifié identique sur disque.

    Origine de la copie      : copie PostgreSQL par template de la base du
                               dossier (`createdb -T court_project_pg
                               court_e01_copie`), prise le 14 octobre 2026
                               vers 03 h 55. Copie fidèle, bit pour bit.
    Document utilisé         : document 9 — « DEMANDE INTRODUCTIVE D'INSTANCE
                               — dépôt du 24 juillet 2026 », PRODUCED,
                               371 nœuds, schéma « Demande introductive
                               normalisée ». Sélectionné par `--document 9`,
                               jamais codé en dur.

    Contrôle préalable (T01) : RÉUSSI — 198 lignes, 198 appariées,
                               198 occurrences distinctes, 0 manquante,
                               0 ambiguë, 0 doublon, 0 oubli, 0 contenu
                               incompatible, 0 occurrence étrangère,
                               0 conflit, 0 écriture.
    Contrôle des 198 (T03)   : RÉUSSI — 198 valeurs contrôlées, 198 conformes,
                               0 écart, 19 suffixes conservés, 47 divergences
                               d'avec le Markdown. 43→41, 72→67, 142→139
                               vérifiés nommément.
    Protection du référent   : RÉUSSIE, et indépendante de DocumentSource — le
                               référent du dossier est PRODUCED et bénéficie
                               des mêmes refus qu'un REPRODUCED.
    Lock historique          : IDENTIFIÉ — legal/depots/2026-07-24_initial/
                               cotes.lock.json,
                               sha256 d1193dcb4ef2a38d2b7adbb12bb463604805e4b03f772ae917d3b072a50fd56a
                               Réconciliation : NON CONFORME — 102 des
                               106 cotes concordent, 4 divergences non
                               résolues (voir § 4.5).
    État du registre         : 334 entrées, 268 cotées en juillet (106 cotes
                               racines), 66 sans cote de juillet.
                               Empreinte de l'état de cotation du 14 octobre :
                               dda2ee0d2270bf16…
    Suppressions protégées   : RÉUSSIES — refus REPRODUCED par instance, lot,
                               vue et cascade ; suppressions PRODUCED tracées.
    Cycle probatoire         : RÉUSSI — confirmer → modifier → réexaminer →
                               reconfirmer, sur fixtures.
    Cycle éditorial          : RÉUSSI — conservé V1 → texte V2 → réexamen →
                               nouvelle décision, sur fixtures ; indépendance
                               des deux confirmations démontrée.
    Citations P-12 → P-13    : RÉUSSI sur fixture ; non exercé sur le dossier,
                               faute d'ancrages de citation saisis.
    EX01–EX07                : chacune exercée en refus puis en réussite sur
                               fixture. Sur le dossier : EX01, EX03, EX06,
                               EX07 satisfaites ; EX02, EX04, EX05 bloquées
                               par du travail éditorial non encore fait.
    Python / Django          : 3.11.9 / 5.2.4
    Système                  : macOS (Darwin 21.6.0)
    Backend de test          : PostgreSQL 18.1 + pgvector, accès VÉRIFIÉ —
                               base de test créée, 100 % des migrations
                               appliquées, tests exécutés, base détruite.
    Paramètres d'exécution   : DJANGO_SETTINGS_MODULE pointant un module qui
                               surcharge DATABASES['default']['NAME'].
                               Gabarit : scripts/e01/settings_copie_e01.py.exemple

**Ce qui est livré.** Les deux numérotations coexistent et chaque version
affiche la sienne : la demande déposée porte les 198 numéros de son papier, la
version modifiée les numéros que sa structure calcule. Une seule implémentation
les résout, et les onze sorties actives en ont été vérifiées. Le référent est
protégé contre l'écriture, pas seulement surveillé. Les correspondances entre
versions se décrivent, y compris les scissions et les fusions, avec des
confirmations éditoriales et probatoires distinctes qui se périment quand le
texte change. Les cotes se traduisent par le service chronologique existant et
se contrôlent contre le lock du dépôt. La concordance s'exporte en mode
diagnostique toujours, en mode strict seulement si EX01–EX07 passent.

**Ce qui n'est pas livré.** Les quatre divergences du lock restent non
résolues : c'est une décision à prendre, pas un défaut de code (§ 4.5). Le
travail éditorial proprement dit — relier les paragraphes de la version 2 à
ceux de l'acte déposé, confirmer les appuis, ancrer les citations — n'a pas été
fait : ce n'est pas une tâche de développement, et l'outil le rapporte
exactement comme tel.

---

## 4.0 Diagnostic et estimation

Établi le 14 octobre 2026 sur le commit dae8da2, avant écriture de code.

### Accès vérifiés

| Ressource | État | Preuve |
|---|---|---|
| Base du dossier | **ACCÈS VÉRIFIÉ** | PostgreSQL 18.1, 10 documents, document 9 à 371 nœuds |
| Copie fidèle | **CRÉÉE** | `createdb -T`, 371 nœuds pour le document 9 |
| Markdown archivé | **VÉRIFIÉ** | sha256 identique à celui déclaré par la table |
| Candidat imprimé (.docx) | **VÉRIFIÉ** | sha256 identique à celui déclaré par la table |
| Table de concordance | **VÉRIFIÉE** | 198 lignes, 179 simples + 19 suffixées, 47 divergentes |
| `cotes.lock.json` | **ACCÈS VÉRIFIÉ** | présent localement, 106 cotes, non publié sur GitHub |
| Backend de test | **ACCÈS VÉRIFIÉ** | base de test créée et détruite, migrations appliquées |

Le cahier prévoyait que le lock puisse être indisponible. Il ne l'est pas : il
est présent sur le disque local, et `*.json` au `.gitignore` explique seulement
son absence de GitHub. Le contrôle historique a donc pu être exécuté.

### Choix de conception arrêtés avant les modifications

| Question | Choix | Pourquoi |
|---|---|---|
| Version du texte | `VersionTexte`, une ligne par empreinte de texte | Une confirmation doit pouvoir dire SUR QUOI elle portait ; un booléen reste vrai après la réécriture |
| Référence textuelle | `AncrageCitation` : position + identité de la pièce | Un remplacement global de « P-12 » toucherait dates, sommes, numéros de paragraphes adverses et citations historiques |
| Rattachement `Fait.statement` | **conservé sur la source**, résolution par contexte documentaire | Le fait est plaidé dans un acte ; `numero_plaide(document=…)` le résout là, et refuse de deviner quand l'énoncé est repris ailleurs |
| Modèle de correspondance | groupe `Correspondance` + extrémités typées | Un FK unique perd une origine dans une fusion |
| Gardes de suppression | signaux `pre_delete` | Seuls eux voient `QuerySet.delete()`, l'admin et les cascades — et les enregistrer désactive le « fast delete » |
| Mode sans schéma | grammaire héritée des vues, explicite | Trois écrans la portaient déjà ; ne pas la reprendre les aurait vidés |

### Charge réellement constatée

Le cahier demandait une estimation ; le travail ayant été exécuté dans la
foulée, voici les charges **constatées**, plus utiles qu'une prévision.

| Tâche | Charge constatée |
|---|---|
| US02 — modèles et migrations | ~0 h 5 |
| US02 — résolveur et adaptation des 9 consommateurs | ~1 h 0 |
| US02 — préparation T01, reprise, T03 | ~0 h 7 |
| US01 — référent, instantanés, gardes | ~0 h 5 |
| US03 — correspondances, suppressions, archives | ~0 h 5 |
| US04 — confirmations probatoires | ~0 h 3 |
| US05 — lock, table chronologique, départage | ~0 h 6 |
| US06 — export et EX01–EX07 | ~0 h 5 |
| Tests (101 méthodes) | ~1 h 0 |
| Vérification des sorties réelles | ~0 h 5 |

### Charge éditoriale — distincte, et non estimée

Le parcours de rédaction n'est pas du développement et n'a pas été fait. Son
**volume** est connu, pas sa durée :

- **198 occurrences source** et **2 paragraphes cible** actuellement, à relier
  au fur et à mesure que la version 2 s'écrit ;
- **70 énoncés contestés** répartis sur 7 documents ;
- **515 appuis de juillet** consultables par remontée des correspondances, à
  réexaminer paragraphe par paragraphe pour la version modifiée ;
- **4 divergences du lock** à trancher.

Ces quantités ne se convertissent pas en heures sans une décision sur la forme
de la version 2, laquelle n'est pas arrêtée (`AGENTS.md`). Poste **NON ESTIMÉ**,
et l'outillage ne le raccourcit pas : il le rend contrôlable.

---

## 4.2 Matrice de satisfaction des critères

| Critère | Story | Statut | Code livré | Tests | Preuve | Limite |
|---|---|---|---|---|---|---|
| C01 | US01 | **VALIDÉ** | `reprise_numeros.verifier` | T01, T12, T15 | `preuves_E01/manifeste_rattachement_198.json` | — |
| C02 | US01 | **VALIDÉ** | `referent.py`, `protection.py` | T02, T03, T11, T12, T14 | log de reprise, 7 tests de garde | — |
| C03 | US01 | **VALIDÉ** | `verifier`, `appliquer`, `numeros_manquants` | T04 (6 refus), T13, T15 | tests de refus | — |
| C04 | US02 | **VALIDÉ** | `NumberingMode`, `paragraph_number` | T05, T10, T11, T16 | migration 0016 | — |
| C05 | US02 | **VALIDÉ** | `appliquer`, `controler_apres_reprise` | T03, T13, T14 | 198/198, 19 suffixes, 47 écarts | — |
| C06 | US02 | **VALIDÉ** | `numerotation.resoudre` + 9 consommateurs | T06–T09, T17 | `preuves_E01/T17_sorties.log` | contestation n'affiche aucun numéro (gabarit) |
| C07 | US03 | **VALIDÉ** | `Correspondance`, `ExtremiteCorrespondance` | T10, T18, T19, T20 | tests scission/fusion | — |
| C08 | US03 | **VALIDÉ** | `protection.py`, `NoeudArchive` | T21, T22 | 6 tests de suppression | — |
| C09 | US03 | **VALIDÉ** | `detacher_pour_edition`, `supprimer_occurrence` | T16, T18, T22 | tests d'édition partagée | — |
| C10 | US04 | **VALIDÉ** | `concordance.appuis_dorigine` | T19, T20, T23 | tests de remontée | — |
| C11 | US04 | **VALIDÉ** | `ConfirmationAppui.etat_courant` | T23 (8 sous-tests) | cycle V1→V2→reconfirmation | — |
| C12 | US04 | **VALIDÉ** | `Fait.numero_plaide(document=…)` | T10, T23 | test d'ambiguïté | — |
| C13 | US05 | **PARTIEL** | `cotes_concordance.reconcilier` | T24 (7 sous-tests) | 102/106 concordantes | **4 divergences non résolues** |
| C14 | US05 | **VALIDÉ** | `dispersion_des_liasses` | T25, T26 | 30 liasses, dispersion montrée | — |
| C15 | US05 | **PARTIEL** | `table_des_cotes` | T24, T25, T26, T28 | `preuves_E01/demo_table_cotes.json` | fidélité **NON QUALIFIÉE** tant que C13 n'est pas résolu |
| C16 | US06 | **VALIDÉ** | `export_concordance.construire` | T27, T28, T29 | `demo_concordance.json/.csv` | — |
| C17 | US06 | **VALIDÉ** | verdicts EX01–EX07 | T27 (7 refus + résolutions), T29 | export strict refusé puis accepté | — |
| C18 | US06 | **VALIDÉ** | le présent rapport | — | ce document | — |

**16 critères VALIDÉS sur 18. 2 PARTIELS** (C13, C15), pour la même cause : les
quatre divergences du lock, qui appellent une décision et non du code.

### Verdict par story

| Story | Verdict | Motif |
|---|---|---|
| US01 | **VALIDÉE** | T01 et T03 réussis sur la copie fidèle ; gardes actives |
| US02 | **VALIDÉE** | 198 numéros repris et contrôlés ; 11 sorties vérifiées |
| US03 | **VALIDÉE** | moteur complet et testé ; les liens du dossier restent à saisir (éditorial) |
| US04 | **VALIDÉE** | moteur complet et testé ; les confirmations du dossier restent à prendre (éditorial) |
| US05 | **PARTIELLE** | table produite et contrôlée ; 4 divergences du lock non tranchées |
| US06 | **VALIDÉE** | export diagnostique et strict ; EX01–EX07 exercées dans les deux sens |

---

## 4.3 Résultats de tests et contrôles

**101 méthodes de test exécutées par le runner** pour les 29 scénarios — un
scénario en regroupe souvent plusieurs. 51 dans `document_manager`, 50 dans
`case_manager`. Le nombre de scénarios prescrits (29) et le nombre de méthodes
réellement exécutées (101) sont deux comptes distincts, et ce dernier est celui
que le runner rapporte.

`T29DemonstrationIntegree` hérite de `T27ConditionsStrictes` : le runner
réexécute donc les sept méthodes de T27 dans T29, d'où huit méthodes comptées
pour T29. `T01`, `T03` (application réelle), `T17`, le contrôle du lock sur le
dossier et `demonstration_e01` sont des contrôles en ligne de commande, hors
runner — ils sont exécutés à part, sur la copie des données réelles ou sur une
base de démonstration vide.

| Scénario | Commande | Exécuté | Résultat | Sortie |
|---|---|---|---|---|
| T01 | `manage.py reprendre_numeros_imprimes --document 9 --concordance … --markdown …` sur la copie (hors runner) | Oui | **PASS** — données réelles | 0 |
| T02 | `test document_manager.test_e01_numerotation.T02ProtectionDuReferent` (7 méthodes) | Oui | **PASS** | 0 |
| T03 | la même commande avec `--appliquer --passer-en-stored`, sur la copie | Oui | **PASS** — 198/198 | 0 |
| T04 | `T04Refus` (5 méthodes : manque, ambiguïté, texte, oubli, état changé) | Oui | **PASS** (refus vérifiés) | 0 |
| T05 | `T05ModesEtChamp` (4) | Oui | **PASS** | 0 |
| T06 | `T06AutoSuitLaStructure` (3) | Oui | **PASS** | 0 |
| T07 | `T07GenresConserventLeurTraitement` (2) | Oui | **PASS** | 0 |
| T08 | `T08FiltrerNeChangePasLeNumero` (1) | Oui | **PASS** | 0 |
| T09 | `T09DocumentSansSchema` (2) | Oui | **PASS** | 0 |
| T10 | `T10IndexParStatement` (2) | Oui | **PASS** | 0 |
| T11 | `T11Migration` (1) + `migrate` sur la copie à données réelles | Oui | **PASS** | 0 |
| T12 | `T12ModeRapport` (2) | Oui | **PASS** | 0 |
| T13 | `T13DivergenceLegitime` (3) | Oui | **PASS** | 0 |
| T14 | `T14Idempotence` (2) + seconde application réelle | Oui | **PASS** — 0 écriture | 0 |
| T15 | `T15NouvelleImportation` (1) | Oui | **PASS** | 0 |
| T16 | `T16EditionPartagee` (1) | Oui | **PASS** | 0 |
| T17 | `scripts/e01/verifier_sorties_E01.py` sur la copie (hors runner) | Oui | **PASS** — 12 sorties contrôlées | 0 |
| T18 | `T18TraitementEditorial` (4) | Oui | **PASS** | 0 |
| T19 | `T19Scission` (1) | Oui | **PASS** | 0 |
| T20 | `T20Fusion` (1) | Oui | **PASS** | 0 |
| T21 | `T21AjoutRetraitEtAbsenceDeDecision` (2) | Oui | **PASS** | 0 |
| T22 | `T22VoiesDeSuppression` (6) | Oui | **PASS** | 0 |
| T23 | `T23CycleProbatoire` (9) | Oui | **PASS** | 0 |
| T24 | `T24ControleDuLock` (7) + `T24TableChronologique` (5) + `manage.py table_des_cotes` réel | Oui | **PASS** (mécanisme) / **NON CONFORME** (dossier : 4 divergences) | 1 |
| T25 | `T25LiassesDatesEtDepartage` (3) | Oui | **PASS** | 0 |
| T26 | `T26GroupesEtDatation` (2) | Oui | **PASS** | 0 |
| T27 | `T27ConditionsStrictes` (7) | Oui | **PASS** | 0 |
| T28 | `T28CitationsRendues` (9) | Oui | **PASS** | 0 |
| T29 | `T29DemonstrationIntegree` (8 — la classe hérite de T27) + `manage.py demonstration_e01` | Oui | **PASS** | 0 |
| `check` | `manage.py check` | Oui | **PASS** — 0 problème | 0 |
| migrations manquantes | `manage.py makemigrations --check --dry-run` | Oui | **PASS** — « No changes detected » | 0 |
| suite complète | `manage.py test` | Oui | **PASS** — 127 tests | 0 |

**Aucune régression.** Les 26 tests préexistants passent comme avant.

### Sous-tests des scénarios composés

- **T18** (4) : reformulation déplacée descriptible ; réécriture → réexamen avec
  décision historique conservée ; reconfirmer les seuls appuis ne confirme pas
  le traitement, puis une décision éditoriale explicite le résout ; une
  renumérotation d'affichage conserve la confirmation.
- **T22** (6) : refus REPRODUCED par instance / lot / cascade ; refus d'un
  Statement utilisé par REPRODUCED par instance et par lot ; suppression d'une
  occurrence PRODUCED partageant un Statement protégé, qui le conserve ;
  suppression d'un Statement exclusivement PRODUCED ; refus d'un bloc entier
  sans suppression partielle ; trace consultable après suppression.
- **T23** (9) : confirmer V1 → réécrire → réexamen ; reconfirmer sur V2 ;
  changement de portée ; sauvegarde sans changement ; renumérotation
  d'affichage ; absence d'appui documentée ; appréciations copiées sans valeur ;
  appuis d'origine consultables sans confirmation automatique ; scission sans
  confirmation automatique.
- **T28** (9) : rendu avant / après reclassement ; source préservée ; citation
  historique littérale intacte ; aucun nombre hors citation touché ; référence
  non ancrée bloquante ; référence ambiguë bloquante puis résolue ; positions
  périmées après réécriture ; accents, guillemets et sauts de ligne en CSV.
- **T27** (7) : chaque condition EX01–EX07 refusée séparément puis résolue ;
  « sans appui documenté » accepté avec motif, refusé sans ; export strict
  refusé puis accepté ; reproductibilité ; absence d'associations fabriquées.

---

## 4.4 Inventaire des consommateurs

### Numérotation

| Consommateur | Route | Rôle | Résolveur après modification | Test | État |
|---|---|---|---|---|---|
| `new_views._format_nodes_for_new_display` | `/documents/clean/9/`, `/interactive/`, `/cinematic/` | affichage | `index_par_noeud` sur le document **complet**, puis filtrage | T08, T17 | **couvert** |
| `DocumentRenderer._numbered_nodes` | rendu PDF | export | même fonction, document passé explicitement | T17 (indirect) | **couvert** |
| `produced_views._get_and_process_tree` | `/produced/editor/`, `/contestation/` | éditeur | `index_par_noeud` ; la numérotation hiérarchique locale est supprimée | T17 | **couvert** |
| `produced_views.statement_backbone_view` | `/backbone/` | analyse | `index_par_noeud` | T17 | **couvert** |
| `NewPerjuryElementListView._get_paragraph_numbering_map` | `/perjury-elements/` | liste | `index_par_noeud`, par occurrence | T17 | **couvert** — 70/70 identifiants justes |
| `schema_views.schema_detail_view` | `/documents/schema/` | contrôle | **`resoudre`** — appelait `numeroter`, qui ignore le mode | T17 | **corrigé et couvert** |
| `core.views.document_public_view` | `/document/<pk>/` | publique | **`resoudre`** — même défaut | T17 | **corrigé et couvert** |
| `argument_manager.views` (désignations « § n ») | axes | rapport | **`resoudre`** — même défaut | — | **corrigé** |
| `Fait.numero_plaide()` | `differentiel_axes` | rapport | résolution dans un document nommé ; refuse de deviner | T10 | **couvert** |
| `index_numeros` | `verifier_appuis_depot`, `persister_appuis_depot` | commandes | **supprimé**, remplacé par `index_par_noeud` clé nœud | — | **couvert** |

**Le libellé « numéro (dépôt item) » est supprimé**, ainsi que la règle et les
commentaires qui le présentaient comme obligatoire. Vérifié absent des onze
sorties (`preuves_E01/T17_sorties.log`). Les seules occurrences restantes du mot
« dépôt » sont du contenu (« dépôt direct, type N » dans une pièce citée) et une
infobulle du gabarit de schéma.

**Trois vues ignoraient `numbering_mode`** — c'est le défaut le plus matériel
trouvé : `schema_detail_view`, `document_public_view` et `argument_manager`
appelaient `numeroter()`, qui calcule toujours. Sur l'acte passé en STORED,
elles affichaient donc le numéro recalculé là où le papier en porte un autre.
Corrigées ; `numeroter()` n'est plus appelée que par le résolveur.

**Limite déclarée.** `/documents/contestation/<pk>/` utilise la résolution
commune mais son gabarit n'affiche aucun numéro de paragraphe — il n'en a jamais
affiché (vérifié sur le commit de départ). Ce n'est pas une régression ; la page
reste muette sur ce point.

`ProducedDocumentCleanDetailView` est définie dans `produced_views.py` et n'est
atteinte par aucune route ni par aucun autre appelant (vérifié par recherche
sur tout le dépôt). Elle passe néanmoins par `_get_and_process_tree`, donc par
le résolveur.

### Cotation

| Consommateur | Rôle | État |
|---|---|---|
| `cotation_service.cotation_chronologique` | moteur unique | **corrigé** : départage déterministe jusqu'à `pk` ; date d'un passage héritée de sa pièce |
| `traduire_cotes` | commande existante | inchangée, bénéficie de la correction |
| `cotes_concordance.table_des_cotes` | table autonome | nouveau |
| `citations.rendre` | rendu des cotes citées | nouveau |
| `export_concordance` | concordance | nouveau, même état de cotation |

### Suppression et édition

| Chemin | Garde | Test |
|---|---|---|
| `LibraryNode.delete()` | `pre_delete` | T02, T22 |
| `LibraryNode.objects.filter().delete()` | `pre_delete` (désactive le fast-delete) | T22 |
| `Statement.delete()` / `.filter().delete()` | `pre_delete` | T22 |
| `Document.delete()` et sa cascade | `pre_delete` sur Document et LibraryNode | T02, T22 |
| administration Django | mêmes signaux | couvert par construction |
| `ajax_edit_node` (Statement partagé) | `pre_save` sur Statement | T02 |
| nœud du référent (`item`, arbre) | `pre_save` sur LibraryNode | T02 |
| `paragraph_number` du référent | `pre_save` + `metadonnees_autorisees` | T02 |

---

## 4.5 Reprise et intégrité des données

### Le référent

Document 9, sélectionné par argument. **PRODUCED** — ce qui est précisément le
cas que le cahier signalait : sa protection ne peut pas se déduire de
`DocumentSource`. Elle vient d'une table dédiée, `ReferentHistorique`, que les
gardes consultent avant toute écriture.

Instantané pris avant la reprise : **371 nœuds**, **515 appuis de juillet**,
empreinte globale
`02d9c468c95b2c4294103c162b6ce4f253b7cef2ad27a5c8c57650b1d23fbf14`.

### T01 — l'appariement

    manage.py reprendre_numeros_imprimes \
        --document 9 \
        --concordance legal/amendements/01_avant_notification/concordance_md_imprime.json \
        --markdown   legal/demande_DEPOT_2026-07-21.md \
        --manifeste  …/manifeste_rattachement_198.json

| Assertion | Attendu | Obtenu |
|---|---|---|
| Lignes de référence | 198 (179 simples + 19 suffixées) | **198** |
| Lignes appariées | 198 | **198** |
| Occurrences distinctes | 198, toutes dans le document 9 | **198** |
| Ligne sans occurrence / ambiguë | 0 | **0 / 0** |
| Occurrence visée plusieurs fois | 0 | **0** |
| Paragraphe admissible oublié | 0 | **0** |
| Contenu incompatible | 0 | **0** |
| Occurrence d'un autre document | 0 | **0** |
| Écriture en base | 0 | **0** |

Manifeste : `legal/amendements/01_avant_notification/preuves_E01/manifeste_rattachement_198.json`
— 198 associations, chacune portant ligne, numéro Markdown, numéro imprimé
attendu, `LibraryNode.pk`, `Statement.pk`, résultat du contrôle de contenu et
les deux empreintes comparées.

**Le périmètre admissible est lu sur la structure**, non sur un total à
atteindre : sont admissibles les occurrences que le résolveur classe
« paragraphe » — ni titre, ni conclusion `C-n`, ni mention de clôture, ni nœud
transparent, ni énumération portant déjà sa puce. Il s'est trouvé en contenir
exactement 198, ce qui est une **concordance constatée** et non une contrainte
posée.

**Le contenu est comparé au texte complet du Markdown archivé**, pas à
l'incipit de 120 caractères de la table — lequel ne démontrerait pas
l'intégrité. Règles de normalisation appliquées, toutes de représentation :

1. normalisation Unicode NFC ;
2. apostrophes et guillemets typographiques ramenés à l'ASCII ;
3. marqueurs Markdown d'emphase (`*`, `_`, `` ` ``) retirés ;
4. liens Markdown réduits à leur libellé ;
5. espaces, insécables et retours à la ligne réduits à une espace ;
6. espaces de tête et de fin retirés.

Aucune ne supprime un mot, un chiffre ou une ponctuation de sens.

**Un défaut d'analyse a été trouvé et corrigé en cours de route.** Le premier
lecteur de Markdown accumulait, dans le texte d'un paragraphe, les blocs qui le
suivaient — la citation en bloc qu'il annonce, la formule « tel qu'il appert de
la pièce P-20 » qui la referme, le chapeau en gras d'une section. Trois
paragraphes (¶ 1, ¶ 123, ¶ 127) ressortaient alors comme « contenu
incompatible ». Vérification faite dans la base, un paragraphe y est **une
ligne** du Markdown, et les blocs suivants sont des nœuds distincts : c'était le
lecteur qui avait tort, non les données. Corrigé, les 198 contenus concordent.

### T03 — après la reprise

| Contrôle | Attendu | Obtenu |
|---|---|---|
| Valeurs contrôlées | 198 | **198** |
| Conformes | 198 | **198** |
| Écarts | 0 | **0** |
| Suffixes conservés | 19 | **19** |
| Divergents du Markdown | 47 | **47** |
| `item` 43 → `paragraph_number` | 41 | **41** |
| `item` 72 → `paragraph_number` | 67 | **67** |
| `item` 142 → `paragraph_number` | 139 | **139** |
| `item` 22-A → `paragraph_number` | 22-A | **22-A** |

Les 198 valeurs sont contrôlées une à une, pas seulement les trois exemples.

**Intégrité après écriture** — comparaison à l'instantané :

| Catégorie | Écarts |
|---|---|
| Textes | **0** |
| Arborescence (chemins, profondeurs) | **0** |
| `item` | **0** |
| Appuis de juillet | **0** |
| Nœuds disparus / apparus | **0 / 0** |
| `paragraph_number` | **198** — la métadonnée autorisée |

**Idempotence** : seconde application, **0 écriture**, 198/198 toujours
conformes.

**Refus** (T04) : ligne sans nœud, correspondance ambiguë, contenu modifié,
paragraphe admissible oublié, et modification des données entre contrôle et
application. Chaque cas bloque, diagnostique, et laisse **tous** les
`paragraph_number` vides — aucune écriture partielle. Un numéro déjà posé et
divergent est signalé comme conflit et n'est **pas** écrasé. Aucune option de
forçage n'existe.

### Le lock et les cotes

Lock : `legal/depots/2026-07-24_initial/cotes.lock.json`,
sha256 `d1193dcb4ef2a38d2b7adbb12bb463604805e4b03f772ae917d3b072a50fd56a`,
schéma `cotes.lock/1`, généré le 27 juillet 2026, **106 cotes**.

Normalisation des identités : **(modèle en minuscules, pk)**, lue depuis le
champ `identites_attendues`, qui liste les identités séparées par `|`. La
comparaison n'est **pas** ligne à ligne : le lock porte des cotes principales,
le registre leur détail (334 entrées, dont 192 sous-cotes). Une liasse du lock
répond donc à N lignes de registre partageant sa `cote_racine`.

| Mesure | Valeur |
|---|---|
| Cotes contrôlées | 106 |
| Concordantes | **102** |
| Absentes du registre | 0 |
| Identités illisibles | 0 |
| **Divergentes** | **4** |
| Ajouts sans cote de juillet | 66 — **ne sont pas des manques** |

**🔴 Les quatre divergences.** P-1, P-8, P-15 et P-101. Dans chacune, le lock
nomme une **Photo** et le registre nomme le **PhotoDocument** qui la contient :

| Cote | Lock | Registre | Vérification |
|---|---|---|---|
| P-1 | `photo:4558` | `photodocument:14` | PhotoDocument 14 ne contient que la photo 4558 |
| P-8 | `photo:4526` | `photodocument:3` | ne contient que la photo 4526 |
| P-15 | `photo:4551` | `photodocument:9` | ne contient que la photo 4551 |
| P-101 | `photo:4554` | `photodocument:12` | ne contient que la photo 4554 |

C'est la même matière, désignée à deux niveaux : l'image, et la pièce d'un seul
feuillet qui la présente. **Elles ne sont pas comptées comme concordantes pour
autant.** Les tenir d'emblée pour égales reviendrait à trancher, dans un
rapport, une question d'identité documentaire — la correction silencieuse que le
cahier interdit. Elles sont donc rapportées sous un verdict propre,
`EQUIVALENCE_CONTENANT`, avec la preuve du contenant, et l'option
`--accepter-equivalences-contenant` permet de les retenir **par décision
explicite**, auquel cas la sortie porte la trace de cette décision.

**Par défaut, la réconciliation est NON CONFORME et la table des cotes ne se
dit pas fidèle au dépôt.** Rien n'a été corrigé, ni dans le lock, ni en base.

**Le départage chronologique est corrigé.** Le tri s'arrêtait à
`(horodatage, type, pk de la source)` : deux lignes visant la même source — une
liasse et l'un de ses composants, une pièce et un passage qu'on en extrait — y
sont strictement égales, et leur ordre ne tenait qu'à celui que la base rendait.
Le tri descend désormais jusqu'à `pk`. **Vérifié sans effet sur la cotation
actuelle** : le dossier ne comporte aujourd'hui aucune collision (0 source visée
par plusieurs entrées), de sorte que la correction protège l'avenir sans
déplacer le présent. T25 l'exerce sur une fixture qui en crée une.

**La date d'un passage est corrigée aussi.** Une ligne de précision héritait de
`horodatage` la date de création de son objet, laquelle peut n'avoir aucun
rapport avec la pièce. Elle hérite désormais de la date de sa pièce mère.

**Dispersion des liasses** : 30 liasses de juillet, dont la plupart se
dispersent — P-43, ses 19 composants, s'étale de P-34 à P-241. Chaque composant
et sa destination sont montrés ; la composition de juillet est préservée.

### Ce qui n'a pas été fait sur le dossier

- **Les ancrages de citation** ne sont pas saisis : le cas P-12 → P-13 est
  démontré sur fixture, non sur le dossier. L'export réel signale une cote
  écrite sans ancrage (nœud 1243, « P-2 »).
- **Les correspondances** entre le document 9 et le document 10 ne sont pas
  établies : 200 occurrences « à établir ».
- **Les confirmations d'appui** de la version 2 ne sont pas prises.

Ce sont des actes de rédaction. L'outil les rapporte précisément et refuse
l'export strict tant qu'ils manquent — c'est son office.

---

## 4.6 Démonstration de concordance

`manage.py demonstration_e01` construit la fixture du cahier, exporte, puis
**annule sa transaction** : la base reste inchangée, les fichiers restent.

Source STORED portant 1, 2, 4, 4-A, 9, 10, 11 ; cible AUTO de sept paragraphes.

| Source | Cible | Situation | Obtenu |
|---|---|---|---|
| 1 | 3 | même Statement, déplacé | `CONSERVE`, `deplace=True` |
| 2 | 1 | reformulé et déplacé | `REFORMULE`, `deplace=True`, nouveau Statement |
| 4 | 4 et 5 | scindé | `SCINDE`, deux lignes, un antécédent chacune |
| 4-A et 9 | 2 | fusionnés | `FUSIONNE`, deux antécédents conservés |
| — | 6 | ajout confirmé | `AJOUT` avec motif |
| 10 | — | retrait confirmé | `RETRAIT` avec motif |
| 11 | — | aucune décision source | « à établir », puis décidé |
| — | 7 | aucune décision cible | « à établir », puis décidé |

**Ces artefacts ne sont pas versionnés, et c'est voulu.** `.gitignore` exclut
`*.json` et `*.log`, ce dépôt est public, et le manifeste des 198 associations
porte le texte et les identifiants de l'acte déposé. Ils vivent donc sur le
disque, à l'emplacement indiqué, comme `cotes.lock.json` lui-même — que l'Epic
notait déjà comme non publié pour la même raison. Chacun se régénère par la
commande qui l'a produit.

Artefacts, dans `legal/amendements/01_avant_notification/preuves_E01/` :

| Fichier | Contenu |
|---|---|
| `demo_concordance_diagnostique.json` / `.csv` | la restitution **avant** décisions, EX02 et EX05 bloquantes |
| `demo_concordance.json` / `.csv` | la restitution **après** décisions, export **strict** accepté |
| `demo_table_cotes.json` | la table autonome, 15 lignes, fidèle au lock de fixture |
| `demo_cotes.lock.json` | le lock de fixture, pour que le contrôle soit reproductible |
| `demo_reclassement_P12_P13.json` | le cas textuel, avant / après |
| `manifeste_rattachement_198.json` | **le dossier réel** : les 198 associations |
| `T17_sorties.log` | **le dossier réel** : les onze sorties vérifiées |

### Le cas P-12 → P-13

| | Valeur |
|---|---|
| Texte **stocké** | « …citant la pièce **P-12** » — inchangé de bout en bout |
| Rendu **avant** | « …citant la pièce **P-12** » |
| Rendu **après** ajout d'une pièce antérieure | « …citant la pièce **P-13** » |
| Source citée | la **même** entrée dans les deux cas |
| Qui occupe P-12 après | une **autre** entrée — et elle n'est pas citée |
| Confirmation d'appui | **CONFIRME** — seul le libellé affiché a changé |
| État de cotation avant / après | deux empreintes distinctes |
| Export antérieur | conservé, portant toujours P-12 |

Également démontré : une citation historique littérale n'est pas réécrite ; un
texte contenant « 12 000 $ » et « le paragraphe 12 » n'est pas touché ; une
référence non ancrée ou ambiguë bloque EX04 jusqu'à résolution explicite.

### Le parcours des confirmations (T29)

1. état diagnostique : EX02 et EX05 bloquent ;
2. décisions prises : export strict **possible** ;
3. le texte cible est réécrit : EX02 **et** EX05 retombent, séparément ;
4. **les seuls appuis** sont reconfirmés : EX05 passe, **EX02 reste bloquée** ;
5. décision éditoriale explicite : EX02 passe, export strict de nouveau possible.

C'est l'indépendance des deux confirmations, exercée dans les deux sens.

---

## 4.7 Couverture technique

    Outil                    : NON MESURÉ — coverage n'est pas installé
                               (absent de requirements-dev.txt)
    Modules concernés        : document_manager.{numerotation, protection,
                               referent, reprise_numeros, concordance,
                               export_concordance}
                               case_manager.{cotation_service,
                               cotes_concordance, citations}
    Couverture des lignes    : NON MESURÉE
    Couverture des branches  : NON MESURÉE
    Tests de migration       : exécutés — migration appliquée à la copie à
                               données réelles (371 nœuds), puis base de test
                               construite depuis zéro à chaque exécution
    Limites de l'environnement : aucune rencontrée ; PostgreSQL 18.1 +
                               pgvector pleinement disponible

Aucun pourcentage n'est avancé. La grille fonctionnelle est la matrice C01–C18
du § 4.2 : **16 validés sur 18**.

---

## 4.8 Changements et utilisation

### Fichiers

**Nouveaux**

| Fichier | Rôle |
|---|---|
| `document_manager/protection.py` | gardes de suppression et d'écriture |
| `document_manager/referent.py` | désignation du référent, instantanés, comparaison |
| `document_manager/reprise_numeros.py` | T01, application, T03, normalisation |
| `document_manager/concordance.py` | correspondances, édition, suppression tracée |
| `document_manager/export_concordance.py` | restitution et verdicts EX01–EX07 |
| `case_manager/cotes_concordance.py` | réconciliation du lock, table des cotes |
| `case_manager/citations.py` | ancrage et rendu des cotes citées |
| 5 commandes de gestion | voir ci-dessous |
| 2 modules de tests | 101 méthodes |
| `scripts/e01/verifier_sorties_E01.py` | contrôle des sorties rendues |
| 2 migrations | `document_manager.0016`, `case_manager.0015` |

**Modifiés** : `document_manager/models.py` (2 champs, 7 modèles),
`case_manager/models.py` (2 modèles), `document_manager/numerotation.py`
(résolveur), `document_manager/apps.py` (signaux), les 3 vues qui ignoraient le
mode, les 2 formateurs de vues, le rendu PDF, les 2 commandes d'appuis,
`Fait.numero_plaide`, `cotation_service` (départage et dates), et
`argument_manager/forms_axes.py`.

**Aucune dépendance ajoutée.**

### Un correctif de passage

`argument_manager/forms_axes.py` construisait son index de libellés **à l'import
du module** — un champ de formulaire évalué dans le corps de sa classe. Toute
commande chargeant les URL avant d'avoir migré échouait donc, `makemigrations`
la première. L'index est désormais construit à la première étiquette demandée.
Défaut préexistant, rencontré parce que l'Epic ajoute des champs.

### Comment s'en servir

**1. Choisir le mode d'un document** — `Document.numbering_mode`, `AUTO` ou
`STORED`. `AUTO` par défaut, y compris après la migration.

**2. Prévisualiser puis appliquer une reprise**

    # constat, sans écriture
    manage.py reprendre_numeros_imprimes --document 9 \
        --concordance legal/amendements/01_avant_notification/concordance_md_imprime.json \
        --markdown    legal/demande_DEPOT_2026-07-21.md \
        --manifeste   manifeste.json

    # protéger d'abord
    manage.py designer_referent --document 9 \
        --libelle "Demande introductive — dépôt du 24 juillet 2026" \
        --depose-le 2026-07-24 \
        --source      legal/demande_DEPOT_2026-07-21.md \
        --concordance legal/amendements/01_avant_notification/concordance_md_imprime.json

    # puis écrire
    manage.py reprendre_numeros_imprimes --document 9 … --appliquer --passer-en-stored

**3. Créer et confirmer des correspondances** — `document_manager.concordance` :
`relier(source, cible, sources=[…], cibles=[…], traitement=…)` puis
`confirmer_traitement(corr, traitement, motif=…)`. Scission : une source, N
cibles. Fusion : N sources, une cible. Ajout : `sources=[]`. Retrait :
`cibles=[]`.

**4. Générer la concordance**

    manage.py exporter_concordance --source 9 --cible 10 \
        --json concordance.json --csv concordance.csv        # diagnostique
    manage.py exporter_concordance --source 9 --cible 10 --strict …

**5. Reproduire les tests**

    manage.py test document_manager.test_e01_numerotation
    manage.py test case_manager.test_e01_cotes_concordance
    manage.py demonstration_e01

**6. Supprimer une occurrence PRODUCED et consulter sa trace** —
`concordance.supprimer_occurrence(noeud, motif=…)` ; la trace se relit par
`concordance.historique_de(document)`. Un élément REPRODUCED est refusé par
toutes les voies.

**7. Retrouver une confirmation historique** — `ConfirmationAppui.etat` donne la
décision prise, `etat_courant()` dit si elle vaut encore, et
`version_examinee.texte` rend le texte sur lequel elle a été donnée.

**8. Calculer les cotes chronologiques**

    manage.py table_des_cotes --liasses --json cotes.json --csv cotes.csv

L'état commun est l'`empreinte_etat` que portent la table et l'export.

**9. Rattacher une citation** — `citations.proposer_ancrages(noeud)` propose,
`AncrageCitation` enregistre, `citations.rendre(noeud)` rend. Une référence non
ancrée est listée par `citations.citations_non_resolues(document)`.

**10. Réexaminer le traitement éditorial** — `Correspondance.etat_courant()`
le dit ; `confirmer_traitement` le tranche. Indépendant des appuis.

### Changements d'API

| Avant | Après | Appelants adaptés |
|---|---|---|
| `index_numeros(document)` → `{statement_pk: "44 (dépôt 28)"}` | **supprimée**. `index_par_noeud(document)` → `{noeud_pk: "41"}` | `verifier_appuis_depot`, `persister_appuis_depot` |
| — | `index_par_statement(document, strict=True)` — adaptateur qui **lève** sur ambiguïté | — |
| `numeroter(document)` | reste le calculateur pur ; les consommateurs passent par `resoudre(document)` | 3 vues |
| `Fait.numero_plaide()` | `numero_plaide(document=None, noeud=None)` ; rend `None` plutôt que de deviner | `differentiel_axes` |
| `_format_nodes_for_new_display(nodes)` | `(nodes, document=None)` | 3 vues + rendu PDF |

### Retour de migration

`migrate document_manager 0015` et `migrate case_manager 0014` retirent les deux
champs et les neuf modèles. **Les données qu'ils portaient sont perdues** : les
198 `paragraph_number`, le mode, les référents, les instantanés, les
correspondances, les versions, les confirmations et les ancrages. Les champs et
associations antérieurs sont intacts. La reprise se rejoue à l'identique, étant
idempotente et fondée sur des sources archivées.

### Problèmes connexes découverts, non traités

1. **`/documents/contestation/<pk>/` n'affiche aucun numéro** — gabarit, jamais
   corrigé ici (hors périmètre : la vue utilise bien la résolution commune).
2. **`ProducedDocumentCleanDetailView` est sans route** — laissée en place.
3. **Un paragraphe cible sans `item` n'est pas numéroté** : par la convention de
   l'importateur, un `item` vide à la profondeur des paragraphes désigne une
   mention de clôture, qui ne se numérote pas. Conservé tel quel, mais c'est un
   piège pour qui crée un paragraphe à l'éditeur sans lui donner d'`item`.
4. **`.env` contient des identifiants en clair**, dont le mot de passe de la
   base et deux clés d'API. Hors périmètre, signalé.

---

## 4.9 Verdict

**Les six stories sont-elles livrées et validées ?** Cinq le sont. US05 est
**partielle** : la table des cotes est produite et son contrôle exécuté, mais
quatre divergences du lock restent non tranchées, et la table ne se qualifie
donc pas de fidèle au dépôt.

**T01 a-t-il réussi sur une copie fidèle, et T03 démontre-t-il les 198 valeurs ?**
**Oui aux deux.** T01 : 198 lignes, 198 occurrences distinctes, aucune anomalie,
aucune écriture, manifeste joint. T03 : 198 valeurs contrôlées une à une sur la
même copie, 198 conformes, 19 suffixes, 47 divergences d'avec le Markdown.

**Le référent est-il protégé, indépendamment de PRODUCED ou REPRODUCED ?**
**Oui.** Il est PRODUCED, et la protection ne s'en déduit pas : elle vient d'une
table dédiée que les gardes consultent. Modification de texte, d'`item`,
d'arborescence et suppression sont refusées par toutes les voies éprouvées.
Seul `paragraph_number` s'écrit, dans un bloc explicite.

**Les associations historiques ont-elles été contrôlées contre le lock ?**
**Oui, et la réconciliation n'est pas conforme** : 102 des 106 cotes concordent,
4 divergent. Aucune correction silencieuse n'a été faite.

**Quels critères empêchent une validation complète ?** C13 et C15, pour la même
cause : les quatre divergences. Leur résolution est une décision sur l'identité
documentaire des pièces P-1, P-8, P-15 et P-101 — photo ou document-photo —, pas
un correctif.

**Les sorties permettent-elles de retrouver les numéros d'origine et la
concordance après réécriture ?** Oui. `item` conserve le numéro du Markdown,
`paragraph_number` celui du papier, les instantanés conservent l'état complet, et
les correspondances portent sur des identifiants d'occurrences que la réécriture
ne déplace pas.

**Le texte source, les associations probatoires et les cotes ont-ils été
préservés ?** Oui. Après la reprise réelle : 0 écart de texte, d'arborescence,
d'`item` et d'appuis ; seules les 198 métadonnées de numérotation diffèrent.

**Les registres et tables de cotes sont-ils disponibles et concordants ?** Oui,
sur un état identifié par empreinte, partagé par la demande, le bordereau et la
concordance. Restent à établir : les correspondances du dossier, les
confirmations d'appui de la version 2, et les ancrages de citation.

**Toutes les voies de suppression respectent-elles REPRODUCED ?** Oui — instance,
lot, vue, administration et cascade depuis Document. Les suppressions PRODUCED
restent permises et laissent une trace exploitable.

**Une modification de texte rend-elle les confirmations précédentes
historiques ?** Oui, pour les deux espèces, et séparément.

**Le traitement éditorial est-il réexaminé indépendamment des appuis ?** Oui —
T18 et T29 démontrent que reconfirmer les seuls appuis ne lève pas EX02.

**Le classement chronologique réutilise-t-il le service existant ?** Oui,
`cotation_service.cotation_chronologique()`, avec son départage corrigé. Il
inclut les 66 pièces sans cote de juillet et n'impose pas P-107. Les exports
antérieurs sont préservés par leur empreinte d'état.

**Le texte rendu cite-t-il les nouvelles cotes pour les mêmes sources ?** Oui,
démontré sur fixture ; non exercé sur le dossier, faute d'ancrages saisis.

**EX01–EX07 ont-elles été exercées en refus puis en réussite ?** Oui, chacune.

### En un mot

**E01 n'est pas entièrement validée.** Deux critères sur dix-huit restent
partiels, pour une cause unique et nommée. Tout le reste est livré, exécuté et
prouvé : les contrôles obligatoires T01 et T03 ont réussi sur une copie fidèle
des données réelles, le référent est protégé, les onze sorties actives sont
vérifiées, et les vingt-neuf scénarios ont été exécutés par 101 méthodes de
test sans aucune régression sur les 26 tests préexistants.

La branche n'est **pas fusionnée** et rien n'est déployé.

---

## 4.10 Résultats structurés

Voir `rapport_execution_epic_E01.json`, qui développe les 18 critères, les
29 scénarios avec leur nombre réel de méthodes, les contrôles du référent, du
lock et des citations, et les verdicts EX01–EX07 sur fixture comme sur le
dossier.

Comme les artefacts du § 4.6, **ce fichier n'est pas versionné** : `.gitignore`
exclut `*.json`, le dépôt est public, et le détail y nomme les pièces du
dossier. Il est produit à la racine du dépôt de travail.
