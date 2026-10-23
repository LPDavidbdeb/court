# C0-A — Implantation de la correction UC14 R3-CONC

**Agent A, 23 octobre 2026. Candidat corrigé, soumis à une nouvelle revue indépendante B.**
Aucune fusion, aucun déploiement, aucune migration, aucune intervention sur la
base réelle. L'intégration de C0-A reste interdite jusqu'à une décision
explicite.

Ce rapport répond au mandat d'implantation du 23 octobre. La conception
**UC14 R3-CONC** au commit approuvé
`b0adf1136c55c38a830d3a1cd1a4332741bf297d` en est le contrat. Elle n'a pas été
modifiée. Le défaut corrigé est celui de la
[revue B01, §4](REVUE_INDEPENDANTE_B01.md#4-blocage-résiduel-uc14--état-changé-après-la-garde).

## En bref

| Question | Réponse établie sur le banc |
|---|---|
| Fenêtre `pre_delete` → `DELETE` | **Fermée dans le périmètre exercé.** T05 et T06, qui reproduisent les deux variantes tardives de B, échouent contre `f35ec85` par violation du contrat et passent sur le candidat. |
| Réinsertion par une instance périmée | **Fermée pour `save()`.** T07 et T08 recréent l'occurrence contre `f35ec85` ; le candidat refuse sans réinsertion. |
| Les deux ordres sûrs | Ordre A : T2 validée, T1 refuse (T01-T04, T13, T19a, T20). Ordre B : T2 attend réellement le PID de T1, puis refuse sans recréer (T05, T06, T12, T17, T19b). |
| Essais R3-CONC | 28 essais pour T01-T23, trois exécutions successives, **28/28 à chaque fois**. |
| Non-régression | 298 tests applicatifs (270 antérieurs + 28) et 33 d'outillage réussis. Schéma : *No changes detected*. |
| Périmètre | Cinq fichiers autorisés, aucun autre. |
| Divergences | Neuf précisions d'implantation déclarées au §9, dont trois soumises à approbation. Aucune ne change AC01-AC07, un diagramme ou le schéma. |

## 1. Diagnostic et correctif

**Défaut.** Deux risques, que le candidat `f35ec85` laissait ouverts.

**La fenêtre entre la garde et le SQL.** La garde `pre_delete` contrôle
l'instance que le collecteur Django a chargée. Le `DELETE` SQL qui suit retire
des PK, sans condition sur leur état, et aucun verrou ne relie les deux. Une
édition validée dans l'intervalle était donc retirée sous l'archive de l'état
antérieur. T05 et T06 le reproduisent contre `f35ec85` (§4).

**La réinsertion.** Quand l'UPDATE d'une instance à PK n'atteint aucune
ligne, Django tente un INSERT. Une instance chargée avant une suppression
validée, puis sauvegardée, recréait l'occurrence sous son ancien PK. T07 le
démontre contre `f35ec85`.

**Correctif.** C'est le mécanisme de R3-CONC, sans extension.

1. **Plan B0/E0** (`protection.preparer_plan`). Il lit l'ensemble exact du bloc
   par son chemin, l'état de chaque occurrence, le parent hors du bloc dont
   Treebeard décrémentera le compteur, et le texte attendu de chaque Statement.
   Rien n'est écrit, rien n'est verrouillé.
2. **Protection effective** (`proteger_occurrences`). Une requête
   `SELECT … ORDER BY id FOR UPDATE` est évaluée sur le bloc et son parent, dans
   l'`atomic` du service. Elle n'utilise ni `skip_locked`, ni `nowait`.
3. **Relecture et comparaison** (`comparer_plan_et_etat`). Une ligne disparue,
   un état changé, un parent déplacé ou un membre ajouté font refuser tout le
   bloc. Le plan n'est jamais étendu à la volée.
4. **Textes** (`proteger_textes_et_verifier`). Les Statement désignés sont
   verrouillés par PK croissante, après les nœuds, puis leur texte est comparé
   au plan.
5. **Gardes refaites sous protection.** Elles portent sur les lignes relues,
   qui remplacent toute instance antérieure.
6. **Archives** construites depuis l'occurrence et le Statement protégés
   (`archiver_noeud(…, statement=)`). Suivent le repointage, puis le retrait
   du bas vers le haut par l'API Treebeard. Les contrôles d'identité B01 et le
   contrôle du chemin final sont conservés.
7. **Durée.** Aucun verrou n'est relâché explicitement. PostgreSQL les garde
   jusqu'à la fin de la transaction externe, et un `RELEASE SAVEPOINT` ne les
   libère pas (T12).
8. **Voies d'écriture de T2.** `ajax_edit_node` protège et relit sa cible avant
   toute écriture. `LibraryNode.save()`, pour une instance existante, protège la
   ligne, refuse si elle a disparu, écrit par UPDATE seul et refuse
   `force_insert`. Une instance neuve garde l'insertion Treebeard.

## 2. Delta et références Git

| Fichier | Δ | Nature |
|---|---:|---|
| `document_manager/protection.py` | +196 −2 | `EtatControle`, `PlanRetrait`, `preparer_plan`, `proteger_occurrences`, `comparer_plan_et_etat`, `proteger_textes_et_verifier` ; `archiver_noeud(…, statement=None)` |
| `document_manager/concordance.py` | +33 −9 | Orchestration de `supprimer_occurrence` ; docstring de `detacher_pour_edition` |
| `document_manager/models.py` | +32 −1 | `LibraryNode.save()` ; import `router`, `transaction`. Aucun champ ni `Meta` modifié |
| `document_manager/views/produced_views.py` | +20 −10 | Barrière de `ajax_edit_node` ; commentaire dans `ajax_delete_node` |
| `document_manager/test_e01_numerotation.py` | +1140 −18 | Harnais à deux connexions, essais R3-CONC, adaptation de trois anciennes contre-épreuves (§5) |

**Production : +281 −22.** Delta total : 5 fichiers, +1421 −40. Par rapport
au socle : les huit fichiers C0-A, +3138 −147, aucune migration.

| Référence | Valeur |
|---|---|
| Candidat corrigé (commit du banc) | `a7af20913d479d49d4e5a1b6088c70fa71553cdb`, arbre `1e0c504e744f95b2558f0ca320717ca57165ed43` |
| Ancien candidat reconstitué (témoin) | `ef2c219c0a6599e76ed33b1cca19204c39a0c4ec`, soit `515666e` + reprise + delta B01 ; huit empreintes identiques à [`candidat_sha256.json` de B01](preuves_revue_B01/candidat_sha256.json) |
| [`C0A_R3_CONC_DELTA.patch`](C0A_R3_CONC_DELTA.patch) (témoin → candidat) | SHA-256 `ecd20a3afba2bd910455158b97d1917a4b7f705934c1923c0245978d5c9038e7` |
| [`C0A_R3_CONC_DIFF_COMPLET.patch`](C0A_R3_CONC_DIFF_COMPLET.patch) (socle → candidat) | SHA-256 `09259b6a935e011865016de79604002e51cb668c31504c3060d398a59d8c1b1d` |
| [`C0A_R3_CONC_candidat.bundle`](preuves_implantation_R3_CONC/C0A_R3_CONC_candidat.bundle) (deux commits, sur le socle) | SHA-256 `2d093d4e923c1a711bbf0e461120fb16243c62a21077a77ac5c2e97a5ae20692` |

**Reproduction vérifiée dans une copie neuve.** Le socle plus le diff complet
donne l'arbre `1e0c504e`. Le socle plus la reprise, le delta B01 et le delta
R3 donne le même arbre. Le bundle restitue les deux commits. Les commits
n'existent que dans le banc et dans ce bundle : aucune branche applicative n'a
été créée dans le dépôt partagé.

## 3. Résultats T01–T24

Résultats sur le candidat, trois exécutions : 28/28 (31,4 s, 31,6 s,
31,1 s). Les PID sont ceux de la première exécution ; les deux autres sont
dans [`observations_R3.json`](preuves_implantation_R3_CONC/observations_R3.json).
La colonne « Ancienne » renvoie au §4.

| ID | Essai(s) | Entrelacement et observation PostgreSQL | Candidat | Ancienne |
|---|---|---|---|---|
| T01 | `test_T01_b01_remplacement_par_un_statement…` | T2 89633, avant la protection de T1 89632 : retire E1 et ajoute E3. Refus T1 ; seule l'archive de T2 subsiste ; `numchild` = 2 | 3/3 | ok |
| T02 | `test_T02_…par_une_citation…` | Même scénario avec une citation HERITE | 3/3 | ok |
| T03 | `test_T03_edition_http_validee_avant_protection…` | Édition HTTP de T2 validée (200). Refus T1, extrémité restaurée ; Statement et capture de T2 conservés | 3/3 | ok |
| T04 | `test_T04_repointage_orm_vers_citation…` | `save()` de T2 vers une citation. Refus T1, aucune archive | 3/3 | ok |
| T05 | `test_T05_edition_http_entre_garde_et_delete…` | Juste avant le DELETE d'E2 : T2 89643 bloquée par T1 89642 (Lock/transactionid), maintenue 1,2 s. Archive = état retiré ; T2 en 403, sans Statement ni capture | 3/3 | **ÉCART AC03** |
| T06 | `test_T06_repointage_orm_entre_garde_et_delete…` | T2 89701 bloquée par 89700. `ModificationRefusee`, aucune citation persistée, aucune réinsertion | 3/3 | **ÉCART C14-D2** |
| T07 | `test_T07_ancienne_instance…sans_update_fields…` | `save()` ordinaire de trois anciennes instances après le commit du retrait. Refus ; ni PK réinsérée, ni archive changée | 3/3 | **ÉCART G06** |
| T08 | `test_T08_update_fields_et_force_insert…` | Trois variantes : `update_fields`, `force_insert` après retrait, `force_insert` sur ligne vivante. Refus de domaine, état inchangé | 3/3 | **ÉCART G06** sur `force_insert` après retrait ; erreurs techniques sur les deux autres |
| T09 | `test_T09_annulation_de_T1_puis_reprise…http` | T2 89711 bloquée par 89710, puis panne de T1. T1 en 500, sans archive ni repointage ; nœuds et compteurs identiques ; T2 valide (200) | 3/3 | sans attente |
| T10 | `test_T10_…reprise_du_repointage_orm` | Même scénario par l'ORM. Aucune archive de citation ; le repointage de T2 est validé | 3/3 | sans attente |
| T11 | `test_T11_refus_tardif…` et 3 pannes existantes | Refus `pre_delete` au dernier retrait : 403, état identique. Pannes après archive, après repointage et après premier retrait : 500, état identique (`C0ARepriseUC14Suppression`, exécutées dans la suite complète) | 3/3 ; pannes : suite complète | ok |
| T12 | `test_T12_release_du_savepoint…` | `RELEASE SAVEPOINT "s…_x53"` du service, puis T2 89720 bloquée par 89719. T2 termine après le `on_commit` externe ; 403, aucune réinsertion | 3/3 | 500 |
| T13 | `test_T13_plusieurs_descendants…` | T1 par la vue réelle : 403. Aucun des quatre nœuds retiré ou archivé | 3/3 | ok |
| T14 | `test_T14a_branches_soeurs…`, `test_T14b_branche_imbriquee…` | a : T1b 89726 bloquée par T1a 89724 sur le parent commun ; compteur = initial − 2 ; arbre cohérent. b : T1b attend, puis refuse le plan changé | 3/3 | a sans attente ; b ok |
| T15 | `test_T15_ensembles_chevauchants…` | Cibles reçues en ordres inverses, requête `ORDER BY id ASC FOR UPDATE`. T_b attend le tuple de la plus petite PK et n'en tient aucun autre ; refus sans préfixe | 3/3 | non applicable (API nouvelle) |
| T16 | `test_T16_commit_independant…` | T2 hors du bloc valide sans attendre, puis panne de T1. Statement, capture et association de T2 conservés | 3/3 | ok |
| T17 | `test_T17_deux_ecritures_de_T2…` | Deux sauvegardes dans une T2 ; la seconde attend T1, puis est refusée. La première est annulée | 3/3 | **ÉCART AC03** |
| T18 | `test_T18a_…victime_l_ecrivain_etranger`, `test_T18b_…victime_T1` | Interblocage réel : `40P01` pour l'étranger (a) ou pour T1 (b). Victime annulée en entier, un seul appel du service, l'autre conforme | 3/3 | non applicable : aucun interblocage sans protection |
| T19 | `test_T19a_…avant_protection`, `test_T19b_…apres_protection` | a : refus « son texte a changé ». b : l'UPDATE direct de T2 89764 attend T1 89759 ; archive = texte retiré ; aucune purge | 3/3 | a : pas de refus ; **b : ÉCART AC03** |
| T20 | `test_T20_descendant_nouveau_ou_deplace…` | Variantes « nouveau » et « déplacé » (`move()`). Refus à la relecture B1, arbre cohérent. N'éprouve pas l'orphelin tardif | 3/3 | refus, motif différent |
| T21 | `test_T21_chaque_archive_correspond…` | Relevé sous protection, avant la première archive. Cinq archives égales champ par champ, motif compris ; Statement vide distinct d'une structure ; deux correspondances repointées ; `statements_supprimes == []` | 3/3 | ok |
| T22 | `test_T22_refus_inchanges…` et `test_T22_refus_sous_protection…` | REPRODUCED, référent, gardes ORM directes ; refus 403 sous protection et sonde `NOWAIT` réussie avant la fin de T1. Six contenus non admissibles et décisions/ancrages : tests existants, dans la suite complète | 3/3 ; existants : suite complète | ok |
| T23 | `test_T23_creation_treebeard_neuve…`, `test_T23b_…404…` et suites UC13 | `add_child`, `add_sibling`, `add_root` ; UPDATE d'instances existantes ; 404 d'une cible absente dès la requête ; partage, COW et captures UC13 par les suites existantes | 3/3 ; UC13 : suite complète | ok |
| T24 | Suites complètes, outillage, schéma | §5 | réussies | — |

**Effectif réel : 28 méthodes**, dont 4 portent des sous-cas (T08 : 3 ; T20 :
2 ; T21 : 5 ; T22 : 2). Le journal serveur consigne, sur toute la campagne,
166 attentes `still waiting … Process holding the lock` puis leur acquisition,
et 28 interblocages, soit deux par passe R3 du candidat
([extrait](preuves_implantation_R3_CONC/journaux/postgresql_extrait.log)).

## 4. Contre-épreuves sur l'ancien candidat et sur le candidat corrigé

**Méthode.** Le fichier d'essais du candidat est conservé. Les quatre modules
de production sont remplacés par ceux du témoin reconstitué, dans la copie
jetable seulement. Le candidat est restauré dans un `finally`, et ses
empreintes sont vérifiées
([`contre_epreuve_ancienne.py`](preuves_implantation_R3_CONC/harnais/contre_epreuve_ancienne.py),
[`contre_epreuve_ancienne.json`](preuves_implantation_R3_CONC/contre_epreuve_ancienne.json)).
Les points d'intercalation sont des requêtes SQL du témoin comme du candidat.
Aucune garde n'est remplacée.

**Résultat sur le témoin : 28 essais, 13 réussis, 14 en échec, 1 en erreur.**
Le détail des messages est dans le
[dépouillement](preuves_implantation_R3_CONC/ancienne-contre-epreuve-R3.depouillement.json).

| Catégorie | Essais | Ce que le témoin fait |
|---|---|---|
| **A. Violation du contrat de données**, essais discriminants | T05, T06, T07, T08 (`force_insert` après retrait), T17, T19b | **T05** : l'archive porte le Statement 732 « enfant deux », alors que l'occurrence retirée portait le 733 « texte décidé par T2 ». **T06** : une citation est retirée sous une archive de Statement. **T07, T08** : « une occurrence retirée a été recréée sous son ancien PK ». **T17** : l'archive porte l'intitulé « B2 », l'occurrence retirée « B2 réécrit par T2 ». **T19b** : l'archive porte un texte qui n'était plus celui retiré |
| **B. Exigence R3 non remplie, sans perte de données observée** | T09, T10, T14a (aucune attente) ; T12 (500 au lieu de 403) ; T19a (aucune comparaison de texte) ; T08 (`update_fields` : `DatabaseError` ; ligne vivante : `IntegrityError`) ; T20 (refus par la garde d'identité, après archives annulées) | Le témoin n'attend pas, ou refuse par une erreur technique, ou refuse plus tard |
| **C. Sans objet sur le témoin** | T15 (`ImportError` : fonction nouvelle) ; T18a, T18b (sans protection, aucun interblocage ne se forme) | Non comptés comme reproductions |
| **D. Réussis sur le témoin**, attendu | T01, T02, T03, T04, T11, T13, T14b, T16, T21, T22 ×2, T23, T23b | Le B01 initial et l'ordre A restaient corrigés |

**Les trois essais exigés comme discriminants (T05, T06, T07) échouent tous
par une assertion de contrat :** AC03, C14-D2 et G06. Aucun échec n'est dû à un
délai, à un import ou au harnais. T01 et T02 réussissent sur le témoin, comme
le plan le prévoit. Les anciennes contre-épreuves adaptées
(`C0ARepriseConcurrence`) n'échouent sur le témoin que par le libellé du refus
(3 sur 6) ; refus et états finaux y sont identiques. Le candidat réussit
28/28 à chacune des trois exécutions.

## 5. Non-régression (T24)

Les journaux sont dans [`journaux/`](preuves_implantation_R3_CONC/journaux/).
Chaque journal porte le témoin d'isolation.

| Exécution | Découverts / exécutés | Durée | Résultat |
|---|---:|---:|---|
| `ancien-app` (référence, témoin) | 270 / 270 | 17,6 s | OK |
| **`candidat-app-complete`** (16 paquets, base de test neuve) | **298 / 298** | 48,5 s | **OK** |
| `ancien-outillage` / **`candidat-outillage`** | 33 / 33 | 0,04 s | OK |
| **`candidat-schema`** | `makemigrations --check --dry-run`, `check` | — | *No changes detected* ; *0 issues* |

| Module | Témoin | Candidat |
|---|---:|---:|
| `document_manager.test_e01_numerotation` | 96 | 124 (+28) |
| `case_manager.test_e01_cotes_concordance`, dont UC15 (`C0ARepriseUC15Lecture` 7, `C0ARepriseUC15Export` 3, `C0AFraicheurEtPerimetre` 10) | 76 | 76 |
| `core.test_regime_citations` + `…_etape2` (citations P6) | 33 + 22 | 33 + 22 |
| `case_manager` (audit, pièces, registre), `cause_manager`, `argument_manager`, `email_manager` | 43 | 43 |

Côté UC13, `C0ARepriseUC13Isoler` (11) et `C0AEditionEtConservation` (21)
sont inchangés et réussis. Côté UC14, `C0ARepriseUC14Suppression` (7) et
`C0ARepriseConcurrence` (6) réussissent aussi. **Absence de changement de
schéma** : *No changes detected*, et la comparaison AST des déclarations de
champs et des `Meta` est identique au socle pour les deux fichiers de modèles
([`comparaison_schema_ast.json`](preuves_implantation_R3_CONC/comparaison_schema_ast.json)).

**Anciens essais modifiés.** Je les déclare tous ; aucun oracle n'a été
supprimé.

- `_supprimer_avec_intercalage`. Le point d'intercalation passe de l'entrée
  d'`archiver_noeud` à la première requête de protection de T1, ou, à défaut,
  à sa première archive. Sous R3-CONC, l'ancien point se situe après la
  protection : T2 y attendrait T1, qui attendrait T2. Ce cas est désormais
  l'ordre B, éprouvé par les nouveaux essais.
- Deux assertions de libellé suivent les nouveaux messages de refus :
  `test_uc14_occurrence_ajoutee…` et `_remplacer_pendant_la_suppression`.
  La docstring de ce dernier est ajustée.
- `_dans_une_autre_connexion` borne désormais son attente.

## 6. Matrice de conformité code–UML–tests

Elle figure dans [MATRICE_CONFORMITE_R3_CONC.md](MATRICE_CONFORMITE_R3_CONC.md) :
G01 à G10, mécanismes et lignes, essais, résultats et limites, puis la
confrontation message par message aux sept diagrammes. Les dix garanties sont
démontrées dans le périmètre exercé. Les sept vues sont conformes, avec les
précisions D-1, D-3, D-4, D-8 et D-9 du §9.

## 7. Intégrité et isolation

- **Banc indépendant** `/private/tmp/court-r3conc-20261023-ZyKFPa`. La copie Git
  vient du dépôt par `fetch` du socle seul, sans remote ni alternates. Le
  Python 3.11.9 est copié, avec un `pip freeze` identique au `.venv` du projet
  (222 paquets) ; Django 5.2.4, django-treebeard 4.8.0, psycopg2-binary 2.9.11.
- **PostgreSQL 18.1 jetable.** `initdb --locale=C`, rôle `c0a_runner` non
  superutilisateur, socket privé en mode 700, port 55439,
  `listen_addresses=''`, aucune écoute réseau (`lsof` vide).
  `log_connections`, `log_lock_waits` et `deadlock_timeout=1s` sont actifs dès
  le démarrage.
- **Harnais.** Le lanceur et les réglages sont ceux de B, identiques à l'octet
  (`557b256a…`, `303886fa…`). Ils refusent les fichiers `.env`, les réglages
  `mysite.settings.*` et toute connexion hors du socket. La sonde vers la base
  réelle est refusée avant libpq dans chaque journal.
- **1256 connexions, toutes `host=[local]`.** Le cluster a été démarré deux
  fois et arrêté deux fois proprement ; `postmaster.pid` est absent
  ([`isolation.json`](preuves_implantation_R3_CONC/isolation.json)).
- **Journal du serveur.** Le journal complet n'est pas versionné : les erreurs
  attendues de `core.test_regime_citations_etape2` y citent un texte du dossier.
  Seul un extrait filtré est livré : démarrage et arrêt, connexions, attentes,
  interblocages. Aucun des littéraux longs de ce module n'y figure, ni dans
  aucun autre fichier de preuve.
- **Dépôt partagé.** HEAD `f35ec85` est inchangé, et les 671 fichiers suivis hors
  `docs/` et `legal/` sont identiques à `f35ec85`. Les deux modifications
  préexistantes de la copie de travail (`AGENTS.md`,
  `docs/modele_preuve/diagrammes/README.md`) n'ont pas été touchées, pas plus
  que les fichiers non suivis. Le dossier non suivi `lots/C0-A/verification_R3_CONC/`
  a été créé par une autre session pendant ce mandat : il a été lu et n'a pas
  été modifié. La présente livraison est versionnée sur une branche neuve issue
  de `b0adf11`, `docs/uc14-r3-conc-implantation-20261023`, et ne contient que des
  fichiers ajoutés.
- **Reconstitution et empreintes** :
  [`reconstruction.json`](preuves_implantation_R3_CONC/reconstruction.json),
  [`manifest_sha256.json`](preuves_implantation_R3_CONC/manifest_sha256.json).

## 8. Réserves et limites non résolues

1. **Orphelin tardif : inchangé, non corrigé, non testé comme fermé.** Un ajout
   par `ajax_add_node`, ou un `move()` Treebeard, sur un parent que T1 retire
   attend le verrou du parent, puis peut écrire sous un chemin retiré après le
   COMMIT. Cela relève d'un avenant à la voie d'ajout (UC02), hors mandat.
2. **Les verrous portent sur des lignes, pas sur une plage.** Un membre apparu
   est vu à la relecture et fait refuser (T20). Aucune garantie contre toutes
   les insertions n'en est déduite.
3. **Écrivains hors protocole.** SQL brut, `bulk_create`, `save_base` direct ou
   `_state` falsifié ne sont pas couverts. `QuerySet.update()` attend le verrou
   et n'insère jamais, mais contourne les gardes `pre_save` (L1-A, C0-B et L5
   inchangés).
4. **Interblocages.** Un écrivain étranger qui prend les lignes dans l'ordre
   inverse peut en provoquer un. PostgreSQL annule une victime : si c'est T1,
   la vue répond 500 sans effet. Aucune absence universelle d'interblocage
   n'est promise.
5. **Attente supplémentaire.** Pendant une suppression, le Statement du bloc est
   verrouillé `FOR UPDATE` : une capture `VersionTexte` de ce même Statement,
   faite par une autre occurrence, attend la fin de T1. Il en va de même pour
   une édition du parent du bloc.
6. **Coût.** Chaque sauvegarde d'une `LibraryNode` existante ajoute un
   `SELECT … FOR UPDATE`.
7. **`LibraryNode.save()` n'accepte plus que des arguments nommés** (D-7). Les
   arguments positionnels, dépréciés depuis Django 5.1, lèvent `TypeError`.
   Aucun appel positionnel n'existe dans le code applicatif.
8. **Appel direct de `detacher_pour_edition` avec une instance périmée** (D-4).
   La barrière est dans la vue. Un appel direct écrit sa capture et son
   Statement neuf avant le refus de la sauvegarde ; sa transaction les annule.
9. **Repointage des extrémités non verrouillé.** Comme avant, une modification
   concurrente de la colonne `noeud` d'une extrémité, entre sa lecture et son
   repointage, n'est pas protégée. Ce cas est hors du défaut B01.
10. **Banc.** Les points d'intercalation dépendent du SQL de Django 5.2.4. T18
    dépend de `deadlock_timeout = 1 s` ; la victime est identifiée par son
    SQLSTATE à chaque exécution. Il n'y a eu ni essai navigateur, ni essai sur
    données réelles.
11. **Registre de validation.** `registre_validation.md` n'a pas été mis à jour :
    son statut relève de la revue B et de votre décision.
12. **Ceci n'est pas la levée de B01.** La levée exige la revue indépendante du
    candidat par B, qui doit rejouer au moins les essais discriminants.

## 9. Précisions d'implantation et divergences déclarées

Aucune ne modifie AC01-AC07, un diagramme ou le schéma. Trois sont **soumises
à approbation** (★).

| ID | Précision | Justification |
|---|---|---|
| D-1 ★ | Les contrôles du bloc s'exécutent une seule fois, sous protection : il n'y a plus de précontrôle sans verrou | C'est la passe « refaire sous protection » d'ACT14-GARDE. AC01 reste respecté (avant la première archive). Un bloc non admissible est désormais verrouillé un instant avant son refus |
| D-2 | Le plan lit le bloc par `path__startswith`, et non par `get_descendants()` | C'est l'ensemble exact que Treebeard retire, sans dépendre de `numchild` |
| D-3 | `ajax_delete_node` : aucun changement fonctionnel. `terminer_transaction_avant_reponse()` est assurée par l'`atomic` existant de la vue | Le COMMIT a lieu au retour de la vue, avant l'émission de la réponse (T12) |
| D-4 | `detacher_pour_edition` n'a pas de barrière propre : elle reçoit l'occurrence protégée | Cela correspond au `noeud_protege` de class.puml (réserve 8) |
| D-5 ★ | Trois anciennes contre-épreuves sont adaptées (§5) : le point d'intercalation est déplacé, deux libellés et une borne sont modifiés | Sans cela, elles se figeraient sous R3-CONC |
| D-6 | Le parent du bloc est comparé sur (document, chemin) ; `numchild` n'est jamais comparé | Note de la conception sur le compteur structurel |
| D-7 ★ | `LibraryNode.save()` n'accepte que des arguments nommés | Il fallait inspecter `force_insert` sans ambiguïté (réserve 7) |
| D-8 | `archiver_noeud` reçoit un argument optionnel `statement`, compatible avec les appels existants | L'archive est construite depuis le Statement protégé |
| D-9 | Pour une opération à plusieurs cibles, la déclaration des cibles se fait par `proteger_occurrences(ids)` ; chaque `save()` protège une seule ligne | activity_t2 (T15, T17) |

## 10. Reproduire

Il faut un banc neuf, construit selon la procédure C.2 avec les scripts de
`docs/agent_a/banc_c0a/`. On applique ensuite au socle `515666e` le diff
complet, ou on récupère les commits depuis le bundle. Les commandes exécutées
figurent dans
[`preuves_implantation_R3_CONC/README.md`](preuves_implantation_R3_CONC/README.md).
Attendus : 28 essais R3-CONC réussis, 298 et 33 tests réussis, et *No changes
detected*. La contre-épreuve rejoue les mêmes essais contre le témoin :
T05, T06 et T07 en échec de contrat.

**Ce qui n'a pas été fait :** aucune fusion, aucun push, aucun déploiement,
aucune migration réelle, aucun accès à la base ou aux services réels, aucune
modification des diagrammes approuvés ou des archives historiques, aucune
correction de la voie UC02.
