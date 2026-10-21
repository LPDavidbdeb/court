# PR #31 et patch C0-A — conflits techniques avant le mandat d'implantation

**Agent A, 20 octobre 2026. Lecture seule.** Aucun code n'a été modifié, aucun patch appliqué, aucun test
exécuté pour cette analyse. Ce document sert à préparer le mandat de l'Agent B. Il ne tranche aucune
question de conception.

> **Suite, même jour.** Analyse antérieure au mandat C0-A (`MANDAT.md`, commit `cb56fa6`), qui a
> enregistré les approbations de UC-C-14 et UC-C-15 et tranché les questions du § 4 :
> - D-a à D-c : adaptation autorisée des tests en conflit ;
> - D-d : erreur globale distincte ;
> - D-f : socle `515666e`.
>
> L'implantation et ses résultats sont dans
> [`RAPPORT_REPRISE_C0A.md`](../architecture_c/lots/C0-A/RAPPORT_REPRISE_C0A.md). Les constats
> ci-dessous restent datés.

## 1. Références lues

| Objet | Référence |
|---|---|
| PR #31 | tête `30724df7ec5c`, branche `docs/approbation-uc13-uml-c0a-20261020`, ouverte, fusionnable |
| UC-C-13 | `C0A-UML-R2-ST`, `APPROUVE_UTILISATEUR` pour `C0A_ISOLER` seulement (`approbation.json`) ; manifeste en tête de PR `1cc630b24cf8c979…` |
| UC-C-14 | `C0A-UML-R2-HIST`, C14-D1/D2 ; registre en tête de PR : `VALIDE_ARCHITECTURE` ; approuvé selon LP, enregistrement en cours ; manifeste `2c5ba44a30d63d65…` |
| UC-C-15 | `C0A-UML-R2-DIAG`, C15-D1 ; mêmes statuts ; manifeste `eb3a3785690191be…` |
| Patch | `C0A_DIFF_COMPLET.patch`, SHA-256 `d10781a1…27a27`, identique dans `main` et dans la PR |
| Code | `515666e`, socle de production, identique à `94f3bc4` pour le code |

Si l'enregistrement final de UC-C-14 ou UC-C-15 change leurs vues, leurs empreintes changent : la
présente analyse est alors à revérifier.

## 2. Conflits entre le patch et les profils approuvés

### 2.1 C0A-ST-01 — UC-C-13 AC02/AC03 : aucune écriture sur l'ancien `Statement`

**Le patch** conserve dans `concordance.detacher_pour_edition` une branche d'écriture en place : il pose
`obj.text = nouveau_texte` puis `obj.save()` quand le `Statement` n'est ni partagé ni protégé.

**Le profil `C0A_ISOLER`** exige autre chose : sur tout changement réel de texte, capter l'ancien
texte, créer un `Statement` neuf, repointer la seule occurrence, puis capter le résultat.

**Correction attendue :** supprimer la branche en place. Les parties conformes du patch se gardent :
- texte identique : retour sans capture ;
- refus du référent ;
- capture avant changement.

**Tests en conflit :**
- *Test du patch* `C0AEditionEtConservation.test_edition_privee_capture_le_texte_avant_modification`.
  Il attend les captures `{"avant", "après"}` sur le **même** `Statement`. Avec une copie neuve, l'ancien
  ne porte que `"avant"`, le nouveau que `"après"`.
- *Tests E01 existants qui appellent `detacher_pour_edition`* :
  - `document_manager` : `T16EditionPartagee` et `T18TraitementEditorial` ;
  - `case_manager` : `T23CycleProbatoire`, `T27ConditionsStrictes` et `T29DemonstrationIntegree`.

  Par lecture, leurs assertions (nouveau `Statement`, `A_REEXAMINER`) restent vraies avec une copie
  systématique. Cela reste **à confirmer par exécution**.

### 2.2 C0A-14-01 — UC-C-14 AC02/AC05 (C14-D1/D2) : ni purge, ni archive d'un contenu non `Statement`

**Le patch, sur deux points :**
- `supprimer_occurrence` supprime les `Statement` devenus orphelins, sauf s'ils portent des
  `appuis_depot` ou des captures utilisées ;
- `archiver_noeud` accepte tout contenu, dont citations et `Event`, avec `statement_pk` nul.

**Le profil, sur deux points :**
- aucune purge : `statements_supprimes` reste toujours vide ;
- refus de **tout le bloc** avant écriture si un membre porte autre chose qu'un `Statement` vérifié ou
  qu'une structure vide. Sont visés : citation, `Event`, objet manquant, clé générique incohérente. La
  nouvelle opération `verifier_archivabilite(noeud)` va dans `protection.py`.

**Tests en conflit :**
- ⚠ **Test E01 existant**, de la référence acceptée des 205 :
  `T22VoiesDeSuppression.test_statement_exclusivement_produced_est_supprimable`
  (`document_manager/test_e01_numerotation.py`, vers la ligne 737). Il attend
  `statements_supprimes == [sid]` et la disparition du `Statement`. **Le profil approuvé inverse cette
  attente.** Le principe de C0-A était de ne jamais réécrire une attente E01 : il faut ici une décision
  explicite (§ 4, D-a).
- *Test du patch* `test_un_identifiant_generique_ne_declenche_pas_la_purge_dun_statement`. Il supprime un
  bloc contenant un `Event` et attend un succès ; C14-D2 exige un refus.

**Conséquence d'usage.** Dans l'éditeur, un nœud portant une citation ne pourra plus être supprimé : la
réponse sera un 403 JSON lisible. Le comportement suit C14-D2, qui est approuvé. Je le signale parce
qu'il s'ajoute au refus d'édition déjà connu.

### 2.3 C0A-REV-01 — UC-C-15 : un résultat qualifié plutôt qu'une `ValueError`

**Le patch** lève `ValueError` pour une anomalie locale (archive non typée, type incompatible). L'export
intercepte alors l'erreur, vide **toutes** les origines de la ligne et recopie le message dans `note`.

**Le profil** fixe quatre règles :
- `appuis_dorigine(noeud, source, cible)` renvoie `LectureAppuis(appuis_valides, anomalies,
  lecture_complete)`. Ce résultat est en mémoire, sans table ;
- une anomalie locale devient un `DiagnosticAppui` (6 codes) et la lecture continue ;
- un contexte invalide produit `ErreurContexteLecture` ;
- l'export collecte les diagnostics **avant** le verdict et les transmet à `_ex04`. Toute incomplétude
  rend `strict_possible` faux.

**Tests en conflit :**
- *Tests E01 existants* : `T23CycleProbatoire.test_les_appuis_d_origine_restent_consultables_et_identifies`
  et `test_une_scission_ne_confirme_pas_automatiquement_ses_cibles`. Ils utilisent le résultat comme une
  liste (`len(...)`, `origines[0]['cote_de_juillet']`). Le changement de type les casse, sauf API
  compatible (§ 4, D-b).
- *Tests du patch* qui attendent une `ValueError` pour une anomalie locale :
  - `C0AFraicheurEtPerimetre.test_identifiant_generique_ne_designe_pas_un_statement_homonyme` ;
  - `test_archive_non_typee_reste_diagnostiquee_sans_deviner`, dont l'assertion `"archiv" in note`
    dépend aussi de la note libre.
- *Test du patch* `test_lecteur_restreint_au_couple_explicitement_demande`, qui utilise le résultat comme
  une liste.
- *Compatible sous condition* : `test_lecteur_sans_couple_refuse_plusieurs_origines_documentaires`
  (`ValueError` pour une erreur globale) passe si `ErreurContexteLecture` dérive de `ValueError` (§ 4, D-d).
- *Point de branchement de l'export* : `_ex04(cible, rapport_lock)`, dans `export_concordance.py`.
  T27 et T29 calculent le strict sur des données sans anomalie : aucun écart n'est attendu, à confirmer
  par exécution.

## 3. Ce que le patch fait déjà conformément

| Profil | Critères satisfaits par le patch (lecture) |
|---|---|
| UC-C-13 | AC01 : refus REPRODUCED et référent, `item` compris. AC04 : texte identique sans capture ; clé générique autre que `Statement` refusée. Les citations restent donc refusées, puisque UC02::RENOMMER_CITATION n'est pas approuvé. AC05/AC06 : fraîcheur par `Statement` et empreinte. AC07 : atomicité. AC08 : aucune migration |
| UC-C-14 | AC01 : précontrôle du bloc ; refus si `ConfirmationAppui` ou `AncrageCitation`. AC03 : `statement_pk` seulement pour un `Statement` vérifié. AC04 : repointage des extrémités. AC06 : 403 JSON et 500 après annulation. AC07 : gardes ORM |
| UC-C-15 | AC01 : couple explicite ; ambiguïté refusée. AC02 : ContentType `Statement` vérifié avant `AppuiDepotJuillet` |

## 4. Décisions à fixer dans le mandat

| # | Question | Options |
|---|---|---|
| D-a | Test E01 `T22…test_statement_exclusivement_produced_est_supprimable` (§ 2.2) | autoriser le changement de son attente (conservation, liste vide), en traçant que C14-D1 la remplace ; ou le marquer comme remplacé et ajouter le test de conservation |
| D-b | Type de retour de `appuis_dorigine` (§ 2.3) | `LectureAppuis` itérable et mesurable sur `appuis_valides`, ce qui laisse intacts les 2 tests E01 ; ou rupture d'API, avec mise à jour autorisée de ces 2 tests |
| D-c | Les 5 tests du patch en conflit (2.1, 2.2, 2.3) | le patch n'a jamais été intégré : les remplacer par les contre-épreuves des profils ; ou les garder ailleurs comme résultats historiques. Ils ne peuvent pas rester tels quels dans la suite |
| D-d | Nature de `ErreurContexteLecture` | sous-classe de `ValueError`, compatible avec l'appel historique, ou exception propre |
| D-e | Forme du refus d'édition (UC-C-13 ne le précise pas) | aujourd'hui une page HTML 403 de Django, que le JavaScript de l'éditeur ne montre pas ; un 403 JSON, comme pour UC-C-14, resterait dans `produced_views.py` |
| D-f | Base de la branche C0-A | voir § 5 |

**Périmètre.** Toutes les corrections tiennent dans les 8 fichiers du patch, à une condition :
`LectureAppuis` et `DiagnosticAppui` doivent être définis dans `concordance.py`. Un module nouveau
serait un neuvième fichier, à autoriser.

## 5. Publication de `94f3bc4` et intégration

**État des branches [git] :**
- `main` ne contient pas `515666e`. Il lui manque **31 commits** : E01, plus les étapes 1 et 2 du régime
  des citations, déjà en production.
- `main` n'a que 3 commits propres, tous documentaires (#29, #30).
- Les deux branches ne modifient **aucun fichier commun**. `git merge-tree` ne prévoit aucun conflit pour
  `epic/E01` vers `main`.
- La PR #31 ne touche que `docs/architecture_c/` : aucun recoupement avec `epic/E01`.

**L'arbre de travail principal ne peut servir à aucune intégration.** 152 fichiers non suivis de
l'Agent B y sont suivis dans `main` : Git refuserait l'extraction ou la fusion. Toute intégration se fait
dans un clone ou un worktree séparé, ou par PR sur GitHub.

**`94f3bc4` ne se publie qu'avec `epic/E01`.** Il corrige `PLAN_REGIME_CITATIONS.md`, qui n'existe pas
dans `main`, et décrit du code absent de `main`.

**Séquence recommandée**, chaque étape sous autorisation distincte :
1. Pousser `epic/E01-numerotation-concordance` : avance rapide de `515666e` à `94f3bc4`.
2. Ouvrir une PR de `epic/E01` vers `main`. Elle apporte le code en production et les documents de
   l'Agent A. C'est un préalable à l'atterrissage de C0-A dans `main` (processus, § 5).
3. Développer C0-A sur une branche dédiée partant du `main` qui en résulte. À défaut, partir de
   `94f3bc4`. Le banc isolé sert à l'exécution, avec des commits distincts du commit documentaire.
