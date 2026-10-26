# C0-A — Préparation technique de l'intégration

**Agent A, 21 octobre 2026. Diagnostic, pas une intégration.** Tout a été fait dans des copies Git
isolées. Rien n'a été modifié, poussé, fusionné ni déployé sur les branches principales ; aucune
migration réelle n'a été appliquée. Je n'ai accédé ni à la base réelle ni à Cloud Run, et je n'ai pas
touché aux fichiers de l'Agent B.

## Conclusion

**Aucun bloqueur technique.** Il ne reste que des décisions (§ 5).

- **Le code C0-A corrigé s'intègre sans conflit**, à condition d'apporter d'abord à `main` le socle
  E01. Il ne peut pas y être intégré **seul**.
- **Le candidat intégré est vérifié** :
  - 270 tests applicatifs et 33 d'outillage réussis ;
  - aucun changement de schéma ;
  - code applicatif identique, octet pour octet, au candidat déjà testé sur `515666e`.

## 1. Références examinées

| Référence | SHA | Nature |
|---|---|---|
| `main` (origin) | `cb56fa62f3d8aa8a6455a3a06783d734d23ed986` | fusion de la PR #31, approbations UC13–15 et mandat C0-A |
| PR #30 (fusion) | `cd584c307fcc31096dd93daae6a8fc26ab949eaf` | UC-C-13 R2-ST approuvé |
| PR #31 (tête approuvée / fusion) | `30724df7ec5cbd1aba8ef25d59b5c3a162d20dab` / `cb56fa6` | UC-C-14 R2-HIST, UC-C-15 R2-DIAG |
| `epic/E01-numerotation-concordance` | `f35ec8586866f4359d44f52a0bc5cc57c0804217` | socle `515666e` plus 3 commits documentaires de A |
| Socle historique | `515666eb8c6e7fdcdd265f9187c9c37b769b0fed` | code de l'application en service localement (étape 2 du régime, plan § 12.6) |

**Divergence.**
- La base commune de `main` et de `epic/E01` est `7b26081` (13 octobre).
- `epic/E01` a 34 commits que `main` n'a pas. Ils apportent **109 fichiers applicatifs et 11
  migrations** : E01, l'application `cause_manager`, les étapes 1 et 2 du régime des citations.
- `main` a 7 commits propres, **tous documentaires** : aucun fichier applicatif modifié depuis la base
  commune.

**Conséquence pour C0-A.** Cinq des huit fichiers de C0-A **n'existent pas dans `main`** :
`concordance.py`, `protection.py`, `export_concordance.py` et les deux modules de tests E01. Les trois
autres y sont dans leur état antérieur à E01. `git apply` du patch de reprise échoue donc sur `main`
(essai fait). C0-A dépend des modèles, migrations et services d'E01 : **une intégration ciblée de C0-A
seul dans `main` n'est pas possible.**

## 2. Candidat corrigé reconstruit

Copie Git indépendante, partie de `515666e` : propre `.git`, aucun remote, aucun alternates. On y
applique, dans l'ordre, les deux patchs **tels que publiés dans `f35ec85`** :

| Patch | SHA-256 |
|---|---|
| `C0A_REPRISE_DIFF_COMPLET.patch` | `fd275e7f…` |
| `C0A_REPRISE_B01_DELTA.patch` | `edb421e8…` |

**Les 8 fichiers obtenus ont exactement les empreintes livrées** dans le complément B01. Les livrables
historiques n'ont pas été modifiés.

## 3. Applicabilité sur `main`

Seconde copie indépendante, partie de `main` `cb56fa6` :

| Étape | Résultat |
|---|---|
| C0-A appliqué directement sur `main` | **échec** : 5 fichiers absents, 3 contextes absents |
| `git merge --no-ff f35ec85` (epic/E01) dans `main` | **aucun conflit** ; arbre `6afbe3f1…` |
| Patch livré puis delta B01, appliqués après la fusion | **aucun conflit** ; arbre `f928ae7e…` ; 8 fichiers, empreintes identiques au candidat |
| Comparaison avec le candidat testé sur `515666e` | **671 fichiers hors `docs/` et `legal/`, tous identiques** ; les écarts se limitent à 320 fichiers documentaires |

**Autres constats :**
- **Dépendances.** Aucune dépendance nouvelle : `requirements` inchangés. `epic/E01` ajoute une ligne à
  `mysite/settings/base.py` et une ligne à `mysite/urls.py`.
- **Migrations.** C0-A n'en ajoute **aucune**. Les 11 migrations nouvelles pour `main` sont celles d'E01
  et du régime, déjà appliquées sur la base locale en service.
- **Régime HERITE / PHRASE.** C0-A ne touche ni aux modèles de citation ni à `core/quote_regime.py`. Ses
  seuls contacts avec les citations sont le refus des nœuds-citations, en édition et en suppression, et
  le diagnostic `TYPE_NON_PRIS_EN_CHARGE` en lecture. Les suites du régime passent sur le candidat
  intégré : 33 et 22 tests.

## 4. Contrôles exécutés sur le candidat intégré

Banc `/private/tmp/court-agent-a-integ-20261021-MVGq5I` :
- copie `repo` sur la branche locale `integration/c0a-candidat` ;
- PostgreSQL 18.1 jetable et neuf, socket privé, aucune écoute TCP ;
- scripts synthétiques de `docs/agent_a/banc_c0a/` ;
- Python 3.11.9 et Django 5.2.4, environnement du banc C0-A (`pip freeze` identique au `.venv` du
  projet).

Les 89 connexions sont **toutes locales** ; la contre-épreuve vers la base réelle est refusée avant
`libpq` dans chaque journal. Le cluster est arrêté.

| Journal (SHA-256, préfixe) | Étiquettes | Résultat |
|---|---|---|
| `integ-schema` (`e35d391b…`) | `C0A_SCHEMA_CHECK` | `No changes detected` ; `System check identified no issues (0 silenced).` |
| `integ-c0a-cible` (`6faaaa9e…`) | 5 classes C0-A, dont `C0ARepriseConcurrence` (B01) | **34/34 OK** |
| `integ-app-complete` (`55b43da9…`) | 16 paquets applicatifs | **270/270 OK** |
| `integ-outillage` (`6ba6b770…`) | `scripts.regime_citations.test_projection`, `test_verifier_ab` | **33/33 OK** |

**Composition des 270 tests :**

| Module | Tests |
|---|---:|
| `document_manager.test_e01_numerotation` | 96 |
| `case_manager.test_e01_cotes_concordance` | 76 |
| `core.test_regime_citations` | 33 |
| `core.test_regime_citations_etape2` | 22 |
| `cause_manager.tests` | 12 |
| `case_manager.test_piece_file_audit` | 13 |
| `case_manager.test_evidence_audit` | 8 |
| `argument_manager.test_affidavit_ordre` | 5 |
| `case_manager.test_procedural_registry` | 4 |
| `email_manager.tests` | 1 |

Ces résultats portent sur le **candidat intégré à `main`**, et non sur `515666e`. Les commits de la copie
isolée sont locaux ; les empreintes d'arbre ci-dessus sont reproductibles.

## 5. Bloqueurs et décisions requises

**Il n'y a pas de bloqueur technique.** Quatre décisions doivent être prises avant toute exécution :

| # | Décision | Pourquoi |
|---|---|---|
| D1 | **Validation de B01 par l'Agent B**, y compris l'extension à l'état archivé (complément § 2) | préalable fixé par le processus |
| D2 | **Apporter à `main` le socle E01 (`epic/E01` à `f35ec85`), puis C0-A** | C0-A ne peut pas entrer seul dans `main`. Ce socle est déjà le code en service localement, mais il n'a jamais atterri dans `main` |
| D3 | **Cloud Run : déployer ou non** | tout push sur `main` sans `[skip ci]` lance `deploy.yml` : construction de l'image, déploiement Cloud Run, puis **`manage.py migrate` sur Cloud SQL**. Les 11 migrations d'E01 et du régime y seraient appliquées. L'état de Cloud Run et de Cloud SQL n'a pas été examiné. Recommandation : intégrer avec `[skip ci]` et traiter un éventuel déploiement Cloud Run comme une décision séparée, précédée d'une sauvegarde de Cloud SQL |
| D4 | **Mise en service locale de C0-A** (arbre de travail principal sur `epic/E01` et serveur local) | distincte de l'intégration. Sans migration, elle se fait par avance rapide du code et se défait par `git reset --keep` |

## 6. Chemin d'intégration recommandé, après D1 à D4

Toujours dans un **clone séparé** : l'arbre de travail principal contient des fichiers non suivis de
l'Agent B qui sont suivis dans `main`, et Git y refuserait la fusion.

1. Créer `integration/c0a` depuis `origin/main` (`cb56fa6`, ou la tête du moment, après une nouvelle
   vérification qu'aucun fichier applicatif n'a changé).
2. Fusionner `epic/E01-numerotation-concordance` à `f35ec85` (`--no-ff`, sans conflit attendu).
3. Commiter C0-A en **deux commits traçables** : le patch de reprise livré, puis le delta B01. Vérifier
   les 8 empreintes du complément.
4. Rejouer, sur base de test dédiée et jetable : `C0A_SCHEMA_CHECK`, les 34 tests ciblés, les 270 de la
   suite et les 33 d'outillage.
5. Pousser `integration/c0a`, puis ouvrir une PR vers `main` pour la revue de conformité de B.
6. Fusionner dans `main` avec **`[skip ci]` dans le message de fusion** (D3), puis inscrire C0-A au
   journal des lots et régénérer l'ERD (processus § 5). L'ERD ne changera pas pour C0-A, qui n'a aucune
   migration.
7. Si D4 est autorisé, mettre en service localement : avancer `epic/E01` jusqu'au code intégré, en
   préservant les fichiers de l'Agent B, sans aucune migration à appliquer.

**`epic/E01` et le travail existant dans `main` sont préservés.** La fusion ne réécrit rien ; les
documents de l'Agent B sont déjà dans `main`.

**Retour arrière :**

| Situation | Procédure |
|---|---|
| Avant la fusion dans `main` | supprimer `integration/c0a` |
| Après la fusion | `git revert` des deux commits C0-A (et `git revert -m 1` de la fusion E01 si elle doit aussi être retirée) ; aucune migration C0-A à défaire |
| Mise en service locale | `git reset --keep f35ec85` |
| Cloud Run, s'il est déployé un jour | décision et sauvegarde propres, hors C0-A |

## 7. Réserves inchangées

- **Orphelin tardif** (revue B, § 3) : non traité, avenant ciblé à décider. Le risque est faible dans un
  usage mono-utilisateur.
- **Citations ni modifiables ni supprimables** (C14-D2), et **texte refusé encore affiché** dans
  l'éditeur.
- **L1-A, C0-B et L5** non livrés.
