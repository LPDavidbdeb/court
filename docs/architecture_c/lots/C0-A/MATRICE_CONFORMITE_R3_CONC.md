# UC14 R3-CONC — Matrice de conformité code, UML et essais

**23 octobre 2026 — candidat corrigé soumis à revue. Aucune intégration.**
Candidat : commit de banc `a7af20913d479d49d4e5a1b6088c70fa71553cdb`, arbre
`1e0c504e744f95b2558f0ca320717ca57165ed43`. Conception de référence : R3-CONC au
commit approuvé `b0adf1136c55c38a830d3a1cd1a4332741bf297d`, non modifiée.
Rapport principal : [RAPPORT_IMPLANTATION_R3_CONC.md](RAPPORT_IMPLANTATION_R3_CONC.md).

Les lignes citées sont celles du candidat. « 3/3 » désigne les trois exécutions
successives `r3-candidat-1` à `r3-candidat-3`. La colonne « ancienne » rapporte
le même essai exécuté contre les quatre modules de production de `f35ec85`
reconstitué (§4 du rapport). Valeurs de résultat, selon la grille de revue :
DÉMONTRÉ DANS LE PÉRIMÈTRE, ÉCART CONSTATÉ, NON CONCLUANT, NON VÉRIFIÉ. Un
succès vaut pour les variantes exercées, pas au-delà.

## 1. Garanties G01–G10

| G | Mécanisme et localisation | Essais | Résultat obtenu | Limites |
|---|---|---|---|---|
| **G01** ensemble exact, aucune compensation | `PlanRetrait` / `EtatControle` (`protection.py:169-215`) ; `preparer_plan` lit le bloc par son chemin (`:218`) ; `comparer_plan_et_etat` compare l'ensemble sous protection (`:271`) ; contrôle d'identité B01 conservé (`concordance.py:418`, garde `protection.py:441`) | T01, T02, T13, T20 ; anciennes B01 de `C0ARepriseConcurrence` | **DÉMONTRÉ** 3/3. Refus « l'occurrence N, contrôlée, n'existe plus » (T01/T02) et « occurrence(s) [N] non contrôlée(s) » (T20 nouveau et déplacé). Ancienne : T01, T02, T13 réussis (B01 initial déjà corrigé) ; T20 refusé, motif différent | Verrous de lignes seulement ; orphelin tardif hors périmètre |
| **G02** bloc et parents protégés, relecture après acquisition effective, plan modifié refusé en entier | `PlanRetrait.ids` = bloc + parent du compteur (`protection.py:210`) ; `proteger_occurrences` évalue `SELECT … ORDER BY id FOR UPDATE` (`:251`) ; orchestration `concordance.py:383-391` | T03, T04, T13, T14a, T14b, T20 | **DÉMONTRÉ** 3/3. T14a : la seconde suppression attend sur le parent commun (`pg_blocking_pids` = PID de T1a), compteur `numchild` exact, `find_problems()` vide. T14b : attente puis refus du plan changé | `numchild` non comparé (D-6) ; parent comparé sur (document, chemin) |
| **G03** textes Statement stabilisés ; archives depuis les états protégés | `proteger_textes_et_verifier`, Statement par PK après les nœuds (`protection.py:305`) ; `bloc` = lignes relues (`concordance.py:391`) ; `archiver_noeud(…, statement=)` (`protection.py:403`) | T19a, T19b, T21, T05, T06, T17 | **DÉMONTRÉ** 3/3. T19a : refus « son texte a changé ». T19b : l'UPDATE direct de T2 attend T1 ; archive = texte effectivement retiré. T21 : chaque archive égale, champ par champ, au relevé pris sous protection avant la première archive. Ancienne : T19b en **ÉCART** (archive « texte partagé deux », texte retiré « réécrit en SQL ») | Une capture `VersionTexte` du même Statement par une autre occurrence attend la fin de T1 (§8 du rapport) |
| **G04** protections jusqu'au COMMIT externe ; RELEASE SAVEPOINT n'y met pas fin | Verrous de lignes PostgreSQL, gardés jusqu'à la fin de la transaction ; savepoint du service dans l'`atomic` de la vue ; aucune libération explicite | T05, T06, T12, T17, T19b | **DÉMONTRÉ** 3/3. T12 : `RELEASE SAVEPOINT` du service observé avant le départ de T2 ; T2 bloquée par T1 au-delà de 1,2 s, terminée après le `on_commit` de la transaction externe, puis 403. Journal serveur : « still waiting… Process holding the lock: <PID T1> », puis « acquired » | Appel direct du service hors transaction : la sienne est l'externe, verrous rendus à son retour |
| **G05** T2 validée avant la protection → refus T1, commit T2 conservé | Comparaison sous protection (G01/G02) | T01-T04, T13, T19a, T20 | **DÉMONTRÉ** 3/3. Refus T1 sans archive, extrémités restaurées, Statement, captures, citation ou déplacement de T2 conservés ; T13 par la vue réelle : 403 | — |
| **G06** T2 bloquée reprend ; cible retirée → refus sans recréation, même sans `update_fields` | Barrière `ajax_edit_node` (`produced_views.py:246`) ; `LibraryNode.save` d'une instance existante : protection, existence, UPDATE seul, `force_insert` refusé (`models.py:235`) | T05, T06, T07, T08, T12, T17 | **DÉMONTRÉ** 3/3. T05 : 403, aucun Statement ni capture de T2. T06 : `ModificationRefusee`, aucune citation persistée. T07/T08 : aucun ancien PK réinséré, refus de domaine. Ancienne : **ÉCART** T05 (AC03), T06 (C14-D2), T07 et T08 (réinsertion) | `bulk_create`, SQL brut, `save_base` direct, `_state` falsifié ; arguments positionnels de `save()` refusés (D-7) |
| **G07** annulation T1 complète ; T2 reprend sur l'état restauré | `atomic` du service ; `ROLLBACK TO SAVEPOINT` relâche les verrous pris après lui | T09, T10, T11, T16, T22 (concurrence) ; pannes existantes de `C0ARepriseUC14Suppression` | **DÉMONTRÉ** 3/3. T09/T10 : T1 500 sans archive ni repointage, T2 attendait puis valide ; nœuds et compteurs identiques. T11 : refus tardif 403, état identique. T22 : sonde `FOR UPDATE NOWAIT` réussie pendant que la transaction de la vue est encore ouverte | — |
| **G08** ordre commun, refus entier, commits indépendants préservés | `proteger_occurrences` trie les PK ; ordre LibraryNode puis Statement ; refus = exception dans l'`atomic` | T14a, T14b, T15, T16, T17, T18a, T18b | **DÉMONTRÉ** 3/3. T15 : requête `ORDER BY id ASC FOR UPDATE` ; T_b attend le tuple de la plus petite PK (`pg_locks`, `ctid`) et n'en tient aucun autre ; aucun préfixe conservé. T18 : interblocage réel `40P01`, victime annulée en entier, un seul appel du service, l'autre transaction conforme | Un écrivain étranger en ordre inverse peut provoquer un interblocage : résolu par PostgreSQL, 500 si T1 en est la victime |
| **G09** gardes ORM, API Treebeard, refus des citations, contenus conservés, aucun schéma | Gardes inchangées ; retrait par `MP_NodeQuerySet.delete` ; `parent.save()` passe par `LibraryNode.save` | T21, T22, T23, T11 ; suites existantes ; T24 | **DÉMONTRÉ**. `makemigrations --check --dry-run` : *No changes detected* ; AST des champs et `Meta` identique au socle ; `statements_supprimes == []` ; Statement et captures inchangés | — |
| **G10** contrat UC13 ; barrière avant écriture ; 403 distinct du 404 | `ajax_edit_node` : 404 à l'entrée inchangé ; barrière dans l'`atomic` interne ; refus de domaine traduit en 403 | T03, T05, T09, T12, T23, T23b ; `C0ARepriseUC13Isoler` (11), `C0AEditionEtConservation` (21) | **DÉMONTRÉ**. T05/T12 : 403 ; T23b : 404 sans écriture ; suites UC13 réussies. Ancienne : T12 en 500 au lieu de 403 | Appel direct de `detacher_pour_edition` avec une instance périmée : écritures faites avant le refus de la sauvegarde, puis annulées par sa transaction (D-4) |

## 2. Confrontation aux sept diagrammes

Aucun diagramme n'a été modifié. Le contrôle porte sur les identifiants de
messages des sources PlantUML approuvées.

### sequence.puml — conforme

| Message | Implantation | Preuve |
|---|---|---|
| SEQ14-REQ (405 / 404) | `ajax_delete_node` : méthode, puis `get_object_or_404` hors du `try` | `test_cible_absente_404_et_methode_405_sans_mutation` |
| BEGIN T1 externe | `@transaction.atomic` de la vue | T12 |
| SEQ14-SERVICE, SAVEPOINT S1 | `concordance.supprimer_occurrence` sous `@transaction.atomic` | T12 : `SAVEPOINT "s…_x53"` |
| SEQ14-PLAN, aucun verrou garanti | `preparer_plan` : lectures sans verrou | point « avant protection » des T01-T04 |
| Cas A, SEQ14-T2LOCK, puis UC13 ou save | `proteger_occurrences([pk])` dans la vue et dans `LibraryNode.save` | T03, T04 |
| SEQ14-LOCK, SEQ14-COMPARE, ROLLBACK TO S1, 403 | `proteger_occurrences(plan.ids)`, `comparer_plan_et_etat`, `atomic`, `except` de la vue | T03, T13 (403) |
| Cas B, Statement par PK croissante | `proteger_textes_et_verifier` | T19b |
| SEQ14-DUREE | verrous PostgreSQL jusqu'au COMMIT externe | T12 |
| SEQ14-ATTENTE | `FOR UPDATE` de T2 en attente (`wait_event` Lock/transactionid) | T05, T06, T12, T17 |
| SEQ14-ARCH, SEQ14-REL, SEQ14-DELETE | `archiver_noeud` sur états protégés ; repointage ; `retrait_controle`, Treebeard, garde `pre_delete` | T05, T21 |
| Identités et chemin final ; `statements_supprimes = []` | contrôles conservés (`concordance.py:418-434`) | T21 |
| SEQ14-COMMIT, SEQ14-NOINSERT, 403 / 404 | COMMIT de la vue ; `ModificationRefusee` ; 403 de la vue | T05, T06, T07, T12, T23b |

### activity.puml — conforme, une précision (D-1)

ACT14-REQ, TX, PLAN, LOCK, COMPARE, REFUS, ROLLBACK, protection et comparaison
des textes, GARDE, TYPE, groupe DUREE (ARCH, REL, DELETE, chemin final, refus
tardif ou panne, RELEASE, COMMIT), puis SUCCES : `concordance.py:383-434`.
Précision D-1 : les contrôles du bloc sont exécutés **une fois, sous
protection**, avant la première archive. Il n'y a pas de passe préalable sans
verrou (voir le rapport, §9). La note sur `numchild` est respectée.

### activity_t2.puml — conforme, une précision (D-9)

404 initial : `get_object_or_404`. T2-LOCK : barrière de la vue et
`LibraryNode.save`. Disparition → T2-NOINSERT : `ModificationRefusee`,
rollback, 403 ou exception ORM. Ensuite : relecture et vérification des
types, branches UC13 inchangées, sauvegarde existante en UPDATE seul, refus
de `force_insert`, rollback des captures et de l'objet neuf, création neuve
Treebeard conservée (T23). Précision D-9 : « déclarer toutes les cibles
connues » se fait par `proteger_occurrences(ids)` pour une opération à
plusieurs cibles (T15). Chaque `LibraryNode.save` protège une seule ligne ; une
cible disparue plus tard annule tout de même l'opération entière (T17).

### class.puml — conforme, trois précisions (D-3, D-4, D-8)

`produced_views` : `ajax_edit_node` adaptée. `ajax_delete_node` est
inchangée, à un commentaire près ; `terminer_transaction_avant_reponse()` est
assurée par l'`atomic` existant de la vue (D-3, T12). `concordance` :
`supprimer_occurrence` orchestre ; `detacher_pour_edition` reçoit une
occurrence protégée, sans barrière propre (D-4). `protection` : les huit
opérations proposées existent sous leurs noms. `archiver_noeud` reçoit
l'occurrence protégée et, en argument optionnel, son Statement protégé (D-8).
`PlanRetrait` / `EtatControle` sont des valeurs en mémoire, sans table.
`LibraryNode.save` : existence, UPDATE seul, création Treebeard conservée.
Notes respectées : même ordre, parents compris, aucun verrou sur la Cause,
plan modifié non étendu, `40P01` sans reprise cachée (T18).

### erd.puml — conforme

Schéma inchangé : *No changes detected*, AST des champs et `Meta` identique pour
`document_manager/models.py` et `case_manager/models.py`, aucune migration.
ERD14-ARCH, REL, KEEP et GFK : T21, T22 et les suites existantes.

### sequence_rollback.puml — conforme

RB-LOCK, RB-WAIT, RB-WRITE, RB-ROLLBACK et RB-REPRISE : T09 (HTTP) et T10
(ORM), panne après protection, archives, repointage et premier retrait.
Libération par le rollback du savepoint : T22 (concurrence). Cas miroir d'un
commit indépendant : T16. Deux actions dans une même T2 : T17. Erreur
technique sans reprise : T18b.

### sequence_multiple.puml — conforme

MULTI-PLAN, MULTI-LOCK, MULTI-REFUS, MULTI-RB, MULTI-INDEP : T14a, T14b,
T15, T16, T17 et T18 (interblocage étranger, victime annulée).

## 3. Contrat AC01–AC07

Contrat inchangé. AC01 et AC02 : T22, T20, et les tests existants de refus
du bloc et des contenus. AC03 : T05, T06, T17, T19b et T21. AC04 : T21, avec
plusieurs extrémités. AC05 : T21, avec `statements_supprimes == []` et
Statement et captures identiques. AC06 : T09, T10, T11, T18 et les pannes
existantes. AC07 : T22 et les gardes ORM existantes. Aucun texte de critère
n'a été modifié.
