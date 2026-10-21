# C0-A — Rapport de reprise sur `515666e`

**Agent A, 20 octobre 2026.**

| Élément | Référence |
|---|---|
| Mandat | `MANDAT.md` au commit `cb56fa62f3d8aa8a6455a3a06783d734d23ed986`, approuvé par LP |
| Socle de départ | `515666eb8c6e7fdcdd265f9187c9c37b769b0fed` |
| Contrats appliqués | UC-C-13::C0A_ISOLER `C0A-UML-R2-ST` ; UC-C-14 `C0A-UML-R2-HIST` (C14-D1/D2) ; UC-C-15 `C0A-UML-R2-DIAG` (C15-D1) |

**Livré pour revue indépendante par l'Agent B.**
- Aucun commit, push, fusion ni déploiement.
- Aucune ressource réelle utilisée ; aucun fichier de l'Agent A ou de l'Agent B modifié.
- Le rapport et le patch historiques sont intacts : `C0A_DIFF_COMPLET.patch` a toujours le SHA-256
  `d10781a1…27a27`.

## 1. Livrables

| Livrable | Valeur |
|---|---|
| Diff complet par rapport à `515666e` | [`C0A_REPRISE_DIFF_COMPLET.patch`](C0A_REPRISE_DIFF_COMPLET.patch) ; 110 457 octets ; SHA-256 `fd275e7f4951e7c34686918d875eb1a6cd794e699535a23f345383800ae67708` |
| Portée | **8 fichiers, 1 616 insertions, 140 suppressions** : exactement les huit fichiers autorisés |
| Applicabilité | `git apply --check` réussit sur un index propre de `515666e`. Une fois appliqué, chaque fichier est identique, blob pour blob, au fichier testé |
| Copie d'exécution | `/private/tmp/court-agent-a-c0a-20261020-FerNxE/repo`, branche `review/c0a-515666e`, HEAD `515666e`, modifications non commitées, aucun fichier non suivi |

**Écart par rapport au patch historique**, pour orienter la revue (numstat, lignes ajoutées et retirées) :

| Fichier | Ajouts | Retraits |
|---|---:|---:|
| `document_manager/concordance.py` | 184 | 72 |
| `document_manager/protection.py` | 42 | 7 |
| `document_manager/export_concordance.py` | 54 | 10 |
| `document_manager/views/produced_views.py` | 26 | 15 |
| `document_manager/test_e01_numerotation.py` | 540 | 13 |
| `case_manager/test_e01_cotes_concordance.py` | 341 | 11 |
| `case_manager/models.py` | 0 | 0 |
| `document_manager/models.py` | 0 | 0 |

Les méthodes de fraîcheur du patch sont reprises sans changement : elles satisfont déjà UC-C-13 AC05/AC06.

## 2. Isolation

| Point de contrôle | Constat |
|---|---|
| Copie Git | Indépendante : `git init`, puis `fetch` du seul SHA depuis le dépôt principal. Propre `.git`, aucun worktree, aucun `alternates`, aucun remote. Propre et à `515666e` avant toute exécution |
| Python | `venv --copies` en 3.11.9, paquets recopiés du `.venv` du projet. `pip freeze` identique : 222 paquets, Django 5.2.4, psycopg2 2.9.11 seul pilote |
| PostgreSQL | Cluster 18.1 neuf et vide : `initdb --locale=C`, `-A trust`. Socket privé `…/socket`, port 55439, `listen_addresses=''`. Rôle d'exécution `c0a_runner` non superutilisateur, `pgvector` dans `template1`. Bases `court_c0a` et `test_court_c0a`, cette dernière supprimée avant chaque suite |
| Réglages et lanceur | Ceux de [`docs/agent_a/banc_c0a/`](../../../agent_a/banc_c0a/README.md), non modifiés. Ils refusent `.env*`, `mysite.settings*` et toute connexion hors du socket privé. La contre-épreuve vers `court_project_pg` est refusée avant `libpq` dans **chaque** journal |
| Destination effective | `lsof -i` sur le postmaster : aucune écoute réseau. Le journal du cluster compte **321 connexions, toutes `host=[local]`** : `c0a_runner` sur `test_court_c0a` (300), `postgres` (8) et `court_c0a` (2) ; `c0a_owner` sur `postgres` (11) |
| Fin d'exécution | Cluster arrêté, `postmaster.pid` absent |

## 3. Corrections

### 3.1 C0A-ST-01 — UC-C-13::C0A_ISOLER

**Service `concordance.detacher_pour_edition`.**
- La branche d'écriture en place est supprimée. Tout changement réel de texte suit la même suite :
  1. capturer l'ancien texte ;
  2. créer un Statement neuf ;
  3. repointer la seule occurrence ;
  4. capturer le nouveau texte.
- C'est vrai même si l'ancien Statement n'a qu'un usage.
- Texte identique : aucun objet ni capture.
- Le référent et REPRODUCED restent refusés.

**Route `ajax_edit_node`.**
- Une transaction interne englobe contrôles, capture, création, repointage et `item`.
- Un refus métier y est annulé **avant** sa conversion en **403 JSON** `{status: error, message}`. Une
  exception inattendue est annulée de même, puis rendue en **500 JSON**.
- Les autres réponses sont inchangées : GET, 404, 400.
- Les refus restent les mêmes :
  - REPRODUCED et référent, `item` compris ;
  - type autre que Statement, dont les citations HERITE et PHRASE ;
  - objet absent, clé générique incomplète.

### 3.2 C0A-14-01 — UC-C-14, C14-D1/D2

**Nouvelle fonction `protection.verifier_archivabilite`.** N'admet qu'un Statement réel, vérifié par
son ContentType puis par son existence, ou une structure sans type ni objet. Refuse tout le reste :
- citation HERITE ou PHRASE, Event ;
- Statement disparu ;
- clé générique incomplète.

**Service `supprimer_occurrence`.**
- Précontrôle de **tout** le bloc (protections, décisions, ancrages, archivabilité) avant la première
  écriture.
- Archivage, repointage des extrémités, retrait du bas vers le haut.
- **Aucune purge** : `statements_supprimes` est toujours vide.

**`archiver_noeud`.** Ne lit le texte que d'un Statement vérifié. `statement_pk` renseigné distingue un
Statement, même vide, d'une structure.

**Garde de concurrence ajoutée.** Treebeard retire un nœud avec les descendants qu'il a **au moment du
retrait**. Le service vérifie donc deux choses :
- le nombre d'occurrences retirées égale celui du bloc contrôlé ;
- aucune occurrence ne subsiste sous le chemin du bloc.

Sinon, `SuppressionRefusee` et annulation totale. Cela ferme le cas, démontré au § 5, d'un enfant
rattaché depuis une autre connexion après le contrôle : il aurait été retiré sans contrôle ni archive.

**Route `ajax_delete_node`.**
- Une cible absente répondait **500**, parce que `get_object_or_404` se trouvait dans le `try` qui
  attrape `Exception`. Elle répond désormais **404** sans mutation (UC-C-14).
- Le service possède sa transaction : il annule avant interception. Refus en 403 JSON, panne en 500 JSON.

### 3.3 C0A-REV-01 — UC-C-15, C15-D1

`concordance.appuis_dorigine(noeud, *, document_source=None, document_cible=None)` renvoie désormais
`LectureAppuis(appuis_valides, anomalies, lecture_complete)` : une `dataclass` figée, en mémoire, sans
table.

**Anomalies locales.** Chacune devient un `DiagnosticAppui` portant :
- un code, un message ;
- la correspondance, l'extrémité, l'occurrence et l'archive ;
- les documents source et cible.

Les six codes : `ORIGINE_ARCHIVEE_NON_ATTESTEE`, `ORIGINE_ABSENTE`, `DOCUMENT_SOURCE_INCOHERENT`,
`CLE_GENERIQUE_INCOHERENTE`, `TYPE_NON_PRIS_EN_CHARGE`, `OBJET_INTROUVABLE`. La lecture continue après
chacune.

**Lecture d'une origine.**
- Le type est vérifié avant l'objet. Une citation, même PHRASE certifiée, n'est jamais lue comme un
  Statement.
- Une archive n'est jamais relue par son ancien identifiant.
- Une structure ne donne aucun appui et ses descendants ne sont pas explorés.

**Appuis valides.** Ils gardent correspondance, extrémité, antécédent, appui et qualification
VERSION SOURCE, sans dédoublonnage.

**Erreurs globales de contexte.** Choix : `ErreurContexteLecture(ValueError)`, avec `code` et `motif`.
Les codes sont `CIBLE_ETRANGERE`, `DOCUMENT_INEXISTANT` et `SOURCE_AMBIGUE`.
- **Pourquoi `ValueError` :** c'est la convention existante du module pour un contexte invalide. L'appel
  historique, qui attendait `ValueError` pour une source ambiguë, reste valable.
- **Ce qui distingue les deux sortes de défauts :** une erreur globale est **levée**, la lecture n'a pas
  lieu. Une anomalie locale n'est **jamais** levée.
- **Les pannes techniques** ne sont pas attrapées : elles se propagent, et ne deviennent jamais une
  lecture vide.

**Export (`export_concordance`).**
- Chaque ligne porte `appuis_origine`, `diagnostics_appuis` (portée `LOCALE` ou `GLOBALE`) et
  `lecture_appuis_complete`. Seule `ErreurContexteLecture` est interceptée, et elle devient un diagnostic
  `GLOBALE`.
- Les diagnostics de toutes les lignes sont collectés et dédoublonnés **avant** les verdicts, puis
  transmis à `_ex04`. Toute anomalie rend EX04 et le strict impossibles.
- EX01 à EX07 restent cumulatifs ; aucun EX08.
- La `note` n'est plus utilisée pour porter les erreurs.
- Le CSV reçoit une colonne finale `diagnostics_appuis`. Une ligne sans cette clé est tolérée, pour les
  appelants qui composent leurs lignes.

## 4. Tests existants adaptés, sur autorisation

Chaque test porte dans le code un commentaire : ancienne attente, contrat qui la remplace, nouvelle
vérification. Aucune autre méthode de test d'origine n'est modifiée, ce qu'a vérifié une comparaison AST
avec `515666e` et avec le patch.

| Test | Ancienne attente | Contrat | Nouvelle vérification |
|---|---|---|---|
| E01 `T22VoiesDeSuppression.test_statement_exclusivement_produced_est_supprimable`, renommé `…_est_conserve` | Statement purgé, `statements_supprimes == [sid]` | UC-C-14 AC05, C14-D1 | nœud retiré et archivé avec son texte ; Statement conservé, inchangé, non déclaré supprimé |
| E01 `T23CycleProbatoire.test_les_appuis_d_origine_restent_consultables_et_identifies` | une liste d'appuis | UC-C-15 AC04 | mêmes valeurs dans `appuis_valides` ; lecture complète, aucune anomalie |
| E01 `T23CycleProbatoire.test_une_scission_ne_confirme_pas_automatiquement_ses_cibles` | `len(liste) == 1` | UC-C-15 AC04 | un appui valide par cible, lecture complète |
| Patch `test_edition_privee_capture_le_texte_avant_modification`, renommé `test_edition_privee_apparente_cree_un_statement_neuf` | réécriture en place, captures {avant, après} sur un même objet | UC-C-13 AC02/AC03 | objet neuf ; l'ancien garde son texte et sa seule capture « avant » |
| Patch `test_un_identifiant_generique_ne_declenche_pas_la_purge_dun_statement`, renommé `test_bloc_avec_un_contenu_generique_d_un_autre_type_est_refuse` | bloc avec un Event supprimé | UC-C-14 AC02, C14-D2 | refus total ; aucune archive ni aucun retrait ; Event et Statement homonyme intacts |
| Patch `test_lecteur_restreint_au_couple_explicitement_demande` | une liste | UC-C-15 AC01/AC04 | `appuis_valides` du seul couple, lecture complète |
| Patch `test_identifiant_generique_ne_designe_pas_un_statement_homonyme` | `ValueError`, puis note libre « Statement » | UC-C-15 AC03/AC06/AC07 | aucun appui lu par la PK homonyme ; diagnostic `TYPE_NON_PRIS_EN_CHARGE` ; EX04 et strict refusés |
| Patch `test_archive_non_typee_reste_diagnostiquee_sans_deviner` | `ValueError`, puis note libre « archiv » | UC-C-15 AC03/AC06 | diagnostic `ORIGINE_ARCHIVEE_NON_ATTESTEE` désignant l'archive ; EX04 et strict refusés |

Après les seules corrections de code, ce sont **exactement ces 8 tests** qui échouaient, et aucun
autre : journal `dev1-e01.log`.

## 5. Nouvelles contre-épreuves : 31 tests

| Classe | Tests | Essais du mandat couverts |
|---|---:|---|
| `document_manager…C0ARepriseUC13Isoler` | 11 | ST:T01–T08 et AC01–AC08 par POST réel : partagé et privé apparent ; texte égal avec `item` seul ; premier texte ; refus des citations des deux régimes, d'un Event, d'un objet disparu, de deux clés partielles (6 sous-cas) ; refus REPRODUCED et référent lisibles ; anciennes décisions et captures consultables ; **pannes après création, après repointage et après sauvegarde de `item`**, avec état métier identique avant et après |
| `document_manager…C0ARepriseUC14Suppression` | 7 | C14:T01–T07 et T10 : un seul membre non archivable (6 sous-cas, dont HERITE, PHRASE et PK homonyme) ou une décision ou un ancrage → refus total sans archive ; retrait admissible avec comparaison des champs d'archive, des extrémités, des décisions, de tous les contenus et captures, Statement vide distinct d'une structure ; 404 et 405 ; C14:T08–T09, **pannes après la seconde archive, après le repointage et après le premier retrait**, en HTTP 500 sans succès trompeur, avec état identique |
| `document_manager…C0ARepriseConcurrence` (TransactionTestCase, deux connexions PostgreSQL) | 3 | UC-C-13 : rattachement intercalé sur un Statement privé apparent, entre contrôle et édition, sans que son texte change. UC-C-14 : décision insérée pendant la suppression, préservée par la garde ORM `pre_delete` ; occurrence ajoutée au bloc pendant la suppression, tout annulé (garde de comptage) |
| `case_manager…C0ARepriseUC15Lecture` | 7 | C15:T01–T08 et T11–T12 : deux appuis valides et les 8 anomalies (archive, absence, document incohérent, clé partielle, HERITE, PHRASE certifiée, Event homonyme, objet disparu, plus une structure non explorée), dans **8 ordres** (naturel, inverse, 6 permutations à graine fixe) ; deux couples avec un Statement commun ; erreurs globales ; structure pure ; lecture vide distincte d'un SANS_APPUI ; aucune mutation historique ; panne technique propagée |
| `case_manager…C0ARepriseUC15Export` | 3 | C15:T09–T10 : export mixte (appuis et diagnostics gardés, anomalie comptée une fois, EX04 et strict refusés, JSON strict refusé, diagnostics présents en JSON et en CSV) ; lecture complète mais EX01 insatisfait, strict refusé ; ensemble satisfaisant, strict conservé |

**Contre-épreuve sur le code historique.** Les nouveaux tests ont été exécutés contre le code du patch
historique, appliqué tel quel à `515666e`, avec les fichiers de tests de la reprise. **21 des 31
échouent** (`contre-epreuve-patch-historique.log`), sur les écarts attendus :
- réécriture en place ;
- purge, et archivage de contenus non Statement ;
- 404 rendu en 500 ;
- 403 HTML illisible ;
- `ValueError` au lieu de `LectureAppuis` ;
- enfant concurrent retiré sans contrôle.

Les 10 autres vérifient des propriétés que le patch avait déjà : atomicité de la suppression, refus des
décisions, intercalage de rattachement, propagation d'une panne. L'état corrigé a ensuite été restauré et
contrôlé par l'empreinte de son diff.

## 6. Exécutions

Toutes passent par le lanceur isolé, avec une base de test neuve à chaque fois :

```sh
<banc>/venv/bin/python <banc>/harness/run_tests.py <journal> <étiquettes>
```

| Journal | Code | Étiquettes | Découverts | Exécutés | Résultat |
|---|---|---|---:|---:|---|
| `ref-schema-515666e` | `515666e` | `C0A_SCHEMA_CHECK` | — | — | `No changes detected` ; check sans problème |
| `ref-app-515666e-etiquettes` | `515666e` | 16 paquets applicatifs | 205 | 205 | OK |
| `ref-outillage-515666e` | `515666e` | `scripts.regime_citations.test_projection`, `test_verifier_ab` | 33 | 33 | OK |
| `patch-tel-quel-515666e` | patch historique tel quel | 16 paquets | 236 | 236 | OK |
| `dev1-e01` | corrections, tests non adaptés | 2 modules E01 | 138 | 138 | 8 en échec : exactement ceux du § 4 |
| `contre-epreuve-patch-historique` | patch historique avec les nouveaux tests | 5 classes de reprise | 31 | 31 | 21 en échec (attendu, § 5) |
| **`reprise-app-complete`** | **reprise** | **16 paquets** | **267** | **267** | **OK, 16,3 s** |
| **`reprise-outillage`** | **reprise** | **outillage** | **33** | **33** | **OK** |
| **`reprise-schema`** | **reprise** | **`C0A_SCHEMA_CHECK`** | — | — | **`No changes detected` ; `System check identified no issues (0 silenced).`** |

**Composition des 267 tests :**
- 205 du socle, dont les 22 de `core.test_regime_citations_etape2` et les 33 de `core.test_regime_citations` ;
- 31 tests du patch historique ;
- 31 nouveaux.

**Paquets exécutés :** `DAL Utils ai_services argument_manager case_manager cause_manager core
document_manager email_manager events googlechat_manager helpers pdf_manager photos protagonist_manager
video_manager`.

**Exclusion :** `mysite` ne contient aucun test. Une découverte depuis `.` l'importe, ce que le lanceur
refuse.

**Contrôles hors lanceur :**
- `git diff --check` sans défaut ;
- exactement les 8 fichiers autorisés, aucun fichier non suivi ;
- aucune migration ;
- aucun fichier de `core/quote_regime.py`, des fournisseurs Email/PDF ou de `scripts/regime_citations/`
  touché.

**Journaux** dans `<banc>/logs/`, avec le préfixe SHA-256 :

| Journal | Empreinte |
|---|---|
| `reprise-app-complete` | `ab99ed0da234d722` |
| `reprise-outillage` | `f24f42885c29569f` |
| `reprise-schema` | `e35d391b46a176bb` |
| `contre-epreuve-patch-historique` | `482020303dfb6ba4` |
| `patch-tel-quel-515666e` | `3a2eaf69c65df60e` |
| `ref-app-515666e-etiquettes` | `bd3ccee98789037a` |

Ils sont hors dépôt : ce sont des fichiers d'exécution, et le mandat ne prévoit que deux livrables.

## 7. Problèmes découverts et choix à examiner

1. **Réponse des refus d'édition.** C'était une page HTML 403 de Django, que l'éditeur interprétait comme
   du JSON et ne montrait pas. C'est désormais un **JSON 403** dans `produced_views.py`, à périmètre
   constant : le JavaScript existant affiche alors son alerte « Error saving content », sans changement
   frontend.
   *Limite subsistante :* après un refus, l'éditeur en ligne continue d'afficher le texte saisi jusqu'au
   rechargement. Corriger cela demanderait de toucher `produced/_js.html`, hors mandat. **Non résolu.**
2. **404 rendu en 500 sur la suppression** : défaut présent depuis le socle, corrigé (§ 3.2).
3. **Enfant ajouté au bloc pendant une suppression** : démontré, puis fermé par la garde de comptage
   (§ 3.2). Voir la limite 2 ci-dessous.
4. **Restriction acceptée C14-D2.** Un nœud portant une citation ne peut plus être ni modifié (UC-C-13)
   ni supprimé (UC-C-14) depuis l'éditeur. **À signaler si cela entrave la rédaction.** UC02 et UC12,
   qui traiteraient renommage et réexamen, restent EN_REVUE et ne sont pas implantés.

## 8. Limites restantes, affectées aux lots futurs

1. **Garanties locales seulement.** Ni journal immuable, ni manifeste d'examen, ni provenance ou
   propriété persistante, ni contexte sémantique de `item`, ni archive typée. Une citation ne s'archive
   donc pas. **L1-A / C0-B.**
2. **Concurrence.** Une occurrence rattachée au bloc **après** la vérification finale et avant la
   validation de la transaction peut rester orpheline. Aucun verrou général des arbres ni de
   `QuerySet.update`, bulk ou SQL n'est livré. **L5.** De même, le test d'intercalage UC-C-13 ne prouve
   pas la fermeture de tous les rattachements (**L1-A**).
3. **Fraîcheur.** Elle compare des ensembles (Statement, empreinte), pas la composition exacte des
   occurrences. **L1-A / C0-B.**
4. **Reconfirmation écrasante.** `confirmer_traitement` remplace encore les captures. Aucune
   reconfirmation conservant l'historique n'est offerte. **C0-B.**
5. **Données réelles non mesurées.** Le nombre de concordances réelles qui passeraient « à réexaminer »
   ou porteraient des diagnostics n'est pas mesuré, mesure reportée à la revue (décision LP). Aucune
   donnée réelle n'a été lue.
6. **Collation.** La suite tourne en collation `C` dans le banc ; la collation de la base réelle n'est pas
   comparée.

## 9. Reproduire

Le banc se reconstruit par la procédure C.2 de
[`PREPARATION_CHANTIER_C_2026-10-20.md`](../../../agent_a/PREPARATION_CHANTIER_C_2026-10-20.md), avec
`git checkout -b review/c0a-515666e 515666e`.

```sh
git -C <banc>/repo apply <dépôt>/docs/architecture_c/lots/C0-A/C0A_REPRISE_DIFF_COMPLET.patch
/Library/PostgreSQL/18/bin/pg_ctl -D <banc>/pgdata -l <banc>/logs/postgresql.log \
  -o "-k <banc>/socket -p 55439 -h '' -c max_connections=20 -c shared_buffers=32MB -c fsync=off" -w start
/Library/PostgreSQL/18/bin/dropdb -h <banc>/socket -p 55439 -U c0a_owner --if-exists test_court_c0a
<banc>/venv/bin/python <banc>/harness/run_tests.py revue-app DAL Utils ai_services argument_manager case_manager cause_manager core document_manager email_manager events googlechat_manager helpers pdf_manager photos protagonist_manager video_manager
<banc>/venv/bin/python <banc>/harness/run_tests.py revue-outillage scripts.regime_citations.test_projection scripts.regime_citations.test_verifier_ab
<banc>/venv/bin/python <banc>/harness/run_tests.py revue-schema C0A_SCHEMA_CHECK
/Library/PostgreSQL/18/bin/pg_ctl -D <banc>/pgdata -m fast -w stop
```

**Attendus :** 267 OK, 33 OK, `No changes detected`.

## 10. État remis

- Diff et rapport déposés ici, non commités.
- Banc de reprise conservé et arrêté : `/private/tmp/court-agent-a-c0a-20261020-FerNxE`, 2,1 Go.
- Le dépôt principal reste à `94f3bc4` ; les fichiers de l'Agent B sont inchangés.

**Après la revue,** la promotion vers une branche d'intégration puis `main` relève d'une décision
distincte, comme la divergence entre `epic/E01` et `main`. C0-A n'est pas « atterri ».
