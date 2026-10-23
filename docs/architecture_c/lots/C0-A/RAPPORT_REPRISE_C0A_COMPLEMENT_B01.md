# C0-A — Complément au rapport de reprise : correction de B01

**Agent A, 21 octobre 2026.** Ce complément répond au défaut bloquant B01 de la
[revue indépendante de B](REVUE_INDEPENDANTE_REPRISE_C0A.md) (verdict C), sur autorisation ciblée de LP.

Il ne remplace rien :

| Version | Statut | Fichiers et empreintes (SHA-256) |
|---|---|---|
| Livrée le 20 octobre | **rejetée sur B01** | [`C0A_REPRISE_DIFF_COMPLET.patch`](C0A_REPRISE_DIFF_COMPLET.patch) `fd275e7f…ae67708` ; [`RAPPORT_REPRISE_C0A.md`](RAPPORT_REPRISE_C0A.md) inchangés |
| Corrigée | soumise à la revue ciblée | [`C0A_REPRISE_B01_DELTA.patch`](C0A_REPRISE_B01_DELTA.patch), **à appliquer par-dessus la version livrée** : 11 979 octets, SHA-256 `edb421e899fab4bcce4f25cf4a63c13f3691e8586e1d6fa11d40783dac35e4ef` |

**Ce qui n'a pas été fait :**
- aucun schéma, aucune migration, aucune fonctionnalité ni voie nouvelle ;
- aucun diagramme rouvert ;
- aucun commit applicatif, aucune fusion, aucun déploiement.

## 1. Le delta

**3 fichiers, 148 insertions, 14 suppressions**, tous dans le périmètre autorisé pour B01 :

| Fichier | Changement |
|---|---|
| `document_manager/protection.py` | Nouveau contexte `retrait_controle`, propre à chaque fil (`threading.local`), et extension de la garde `pre_delete` existante de `LibraryNode` |
| `document_manager/concordance.py` | Dans `supprimer_occurrence`, la comparaison d'effectifs est **remplacée** par une vérification d'identité à chaque retrait |
| `document_manager/test_e01_numerotation.py` | 3 contre-épreuves nouvelles. L'assistant `_supprimer_avec_intercalage` rend désormais le motif du refus ; le test déjà livré `…occurrence_ajoutee_au_bloc…` vérifie ce motif |

**Reconstruction vérifiée.** `515666e`, puis le patch livré, puis ce delta, donnent des fichiers
identiques, blob pour blob, aux fichiers testés. Les cinq autres fichiers de C0-A sont inchangés et
gardent les empreintes relevées par B.

Empreintes SHA-256 des fichiers modifiés :

| Fichier | Empreinte |
|---|---|
| `concordance.py` | `9599281c27bccaa51fb7a2d4611603690ac6a7732d5e17ccef654032f47a8d6f` |
| `protection.py` | `3d798295b7126a4fe3a0501141e065499a8da718598b38329741c2dcabba1b26` |
| `test_e01_numerotation.py` | `98d3d4fbd1d9e8890cbb23bf93d98e4d647cd2f71af5be1e6c7b7dffb40f0f0f` |

## 2. La correction

**Défaut.** La version livrée additionnait les occurrences retirées et comparait cette somme à
l'effectif contrôlé. Un retrait nul (E1, retirée par T2) compensait un retrait multiple : Treebeard
retirait P **et** E3, ajoutée par T2. E3 disparaissait sans contrôle ni archive.

**Correction.** Chaque retrait, du bas vers le haut, s'exécute dans `retrait_controle(n)` :

1. **Au passage du collecteur ORM, avant qu'aucune ligne ne soit retirée**, la garde `pre_delete` de
   `LibraryNode` refuse :
   - toute occurrence autre que `n`, par exemple E3 emportée avec P ;
   - `n` elle-même si son état diffère de celui qui a été contrôlé et archivé.
2. **Après le retrait**, le service exige que les identités retirées soient **exactement** `[n.pk]`. Une
   occurrence déjà absente donne un relevé vide, donc un refus. Rien ne compense rien.
3. **Tout refus** lève `SuppressionRefusee` dans la transaction du service. Archives, repointages et
   retraits déjà faits par T1 sont annulés ensemble.

L'**état comparé** à l'étape 1 est : document, chemin, intitulé, numéro, et clé générique du contenu.

**Ce qui est conservé :**
- les gardes ORM existantes (protections, décisions, ancrages, captures, archives, Document) ;
- les compteurs Treebeard : aucune écriture hors de son API ;
- le contrôle final « aucune occurrence sous le chemin du bloc », déjà livré et inchangé.

**À examiner par B : la comparaison de l'état archivé.** Elle étend la vérification d'identité demandée
dans un cas de même nature, que la version livrée laissait passer. T2 repointe E2 vers une citation après
le contrôle :
- la PK de E2 est inchangée ;
- T1 l'aurait donc retirée en l'archivant comme le Statement contrôlé ;
- c'est contraire à C14-D2.

La contre-épreuve du § 3 le démontre. C'est la même garde, au même endroit, sans nouveau mécanisme.

## 3. Contre-épreuves à deux connexions PostgreSQL

Classe `C0ARepriseConcurrence`, qui est une `TransactionTestCase`. T2 s'exécute dans un autre fil, donc
sur une autre connexion, et valide aussitôt. Il intervient juste après le précontrôle complet de T1,
avant sa première archive.

| Test | Scénario | Attendu et vérifié |
|---|---|---|
| `test_uc14_b01_remplacement_concurrent_par_un_autre_statement_refuse` | B01, variante Statement : T2 retire E1 par le service, puis ajoute E3 (Statement) sous P | refus de T1 sur l'identité (« l'occurrence E1, contrôlée et archivée, n'existait plus ») ; P, E2, E3 présents ; **aucune archive de T1** ; conservés : retrait et archive de E1 par T2, E3, son contenu, son rattachement à P, `numchild` de P à 2 |
| `test_uc14_b01_remplacement_concurrent_par_une_citation_refuse` | B01, variante citation (HERITE) | identique |
| `test_uc14_b01_occurrence_repointee_vers_une_citation_apres_controle_refuse` | T2 repointe E2 vers une citation (§ 2) | refus (« modifié depuis son contrôle ») ; E1, E2 et P présents ; aucune archive ; repointage de T2 conservé |
| `test_uc14_occurrence_ajoutee_au_bloc_pendant_la_suppression_annule_tout`, déjà livré | T2 ajoute un enfant sous P | assertion ajoutée : le refus vient désormais de la **garde d'identité du collecteur** (« Nœud E3 : il serait retiré avec l'occurrence P »), et non d'un comptage |

**Exécutions de l'ordre de preuve :**
1. **Avant correction** : les deux tests B01, ajoutés à la version livrée, échouent par
   `SuppressionRefusee not raised` (`b01-avant-correction`).
2. **Après correction** : succès.
3. **Contre-épreuve** : `concordance.py` et `protection.py` de la version livrée, remis avec les tests
   corrigés, font échouer 4 tests (`b01-contre-epreuve-version-rejetee`) :
   - les deux variantes B01 et le repointage, par absence de refus ;
   - l'ajout d'enfant, par le motif : la version livrée refusait par comptage.

   Les fichiers corrigés ont ensuite été restaurés et vérifiés par empreinte.

## 4. Résultats

Même banc isolé que la reprise : `/private/tmp/court-agent-a-c0a-20261020-FerNxE`, copie Git
indépendante à `515666e`, PostgreSQL 18 jetable, socket privé, aucune écoute TCP, lanceur synthétique
inchangé. Le journal du cluster compte **151 connexions le 21 octobre, toutes `host=[local]`**. Le
cluster est arrêté.

| Journal | Étiquettes | Découverts | Exécutés | Résultat |
|---|---|---:|---:|---|
| `b01-avant-correction` | `C0ARepriseConcurrence`, version livrée avec les 2 tests B01 | 5 | 5 | **2 échecs attendus** (B01) |
| `b01-correction-ciblee` | `C0ARepriseConcurrence` et `C0ARepriseUC14Suppression` | 13 | 13 | OK |
| `b01-contre-epreuve-version-rejetee` | `C0ARepriseConcurrence`, code livré, tests corrigés | 6 | 6 | **4 échecs attendus** |
| **`b01-app-complete`** | **suite applicative complète, 16 paquets** | **270** | **270** | **OK, 18,3 s** |
| **`b01-outillage`** | **`scripts.regime_citations.test_projection`, `test_verifier_ab`** | **33** | **33** | **OK** |
| **`b01-schema`** | **`C0A_SCHEMA_CHECK`** | — | — | **`No changes detected` ; `System check identified no issues (0 silenced).`** |

**Contrôles :**
- 270 = 267 + 3 contre-épreuves nouvelles ;
- `git diff --check` sans défaut ;
- toujours exactement les 8 fichiers C0-A par rapport à `515666e`, aucun fichier non suivi, aucune
  migration.

**Empreintes des journaux** (préfixe SHA-256), dans `<banc>/logs/`, hors dépôt :

| Journal | Empreinte |
|---|---|
| `b01-avant-correction` | `1c4123cbd3d08fe1` |
| `b01-correction-ciblee` | `a5d665b5294dde9b` |
| `b01-contre-epreuve-version-rejetee` | `087e89ffe32921a5` |
| `b01-app-complete` | `6e377639b8f3b3a8` |
| `b01-outillage` | `7e5da12c3c8049f5` |
| `b01-schema` | `e35d391b46a176bb` |

## 5. Correction d'un chiffre du rapport de reprise

Le rapport du 20 octobre (§ 5) annonçait « 21 des 31 » nouvelles contre-épreuves en échec contre le code
historique. Après recomptage du journal `contre-epreuve-patch-historique`, le bon chiffre est **20
méthodes distinctes**, pour 31 incidents de sous-cas : 11 échecs et 20 erreurs. B l'avait relevé. Le
diagnostic fonctionnel est inchangé. Le rapport lui-même n'est pas réécrit : ce complément fait foi sur
ce point.

## 6. Ce que cette correction ne traite pas

**L'orphelin tardif** (revue B, § 3) reste distinct et n'est pas intégré. Il s'agit d'un ajout validé
après le contrôle final et le commit de la suppression, par `ajax_add_node` sur un parent périmé. Le
contrôle final déjà livré n'est ni renforcé ni étendu. Son traitement (verrou du parent dans l'ajout)
relève d'un avenant ciblé, s'il est autorisé.

**Autres réserves inchangées :**
- le texte refusé reste affiché dans l'éditeur jusqu'au rechargement ;
- les citations ne sont ni modifiables ni supprimables (C14-D2), ce qui empêche notamment de retirer un
  bloc qui en contient une. B la qualifie de capacité manquante importante pour la rédaction ;
- L1-A, C0-B et L5 ne sont pas réputés livrés ;
- la garde d'identité ferme B01 pour la suppression de bloc ; elle n'est pas un verrou général de l'arbre.

## 7. Reproduire

Appliquer la version livrée puis le delta sur une copie de `515666e` :

```sh
git -C <banc>/repo apply <dépôt>/docs/architecture_c/lots/C0-A/C0A_REPRISE_DIFF_COMPLET.patch
git -C <banc>/repo apply <dépôt>/docs/architecture_c/lots/C0-A/C0A_REPRISE_B01_DELTA.patch
```

Exécuter ensuite les commandes du § 9 du rapport de reprise. Les attendus sont 270 OK, 33 OK et
`No changes detected`. Pour la seule vérification de B01 :

```sh
<banc>/venv/bin/python <banc>/harness/run_tests.py revue-b01 document_manager.test_e01_numerotation.C0ARepriseConcurrence
```

L'attendu est 6 OK.
