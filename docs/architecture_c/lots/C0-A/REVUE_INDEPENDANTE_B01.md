# C0-A — Revue indépendante ciblée de B01

**Agent B — 22 octobre 2026. Verdict : C — NON CONFORME avant intégration.**

**Le scénario initial B01 de compensation d’effectifs est corrigé**, pour le
remplacement concurrent par un Statement et par une citation. Les refus
observés annulent bien les archives, repointages et suppressions de T1,
en préservant les opérations validées par T2.

**Le candidat corrigé n’est toutefois pas conforme au contrat UC14 approuvé.**
Une modification validée après la garde `pre_delete`, avant le `DELETE` SQL,
reste possible. T1 supprime alors une occurrence dont l’état courant ne
correspond plus à l’archive. Le nouveau contrôle d’état ne couvre donc pas
tout l’intervalle demandé. Deux contre-épreuves B le démontrent, dont une
avec la voie réelle `ajax_edit_node` et une avec un repointage vers une citation.
La levée du blocage d’intégration n’est pas recommandée en l’état.

Cette conclusion ne rouvre aucune décision architecturale transversale et
n’étend pas C0-A. Elle concerne la suppression UC14 et ses gardes locales.
L’orphelin tardif reste une réserve distincte (§7).

## 1. Références et reconstitution indépendante

Livraison A : **`f35ec8586866f4359d44f52a0bc5cc57c0804217`**, branche
`epic/E01-numerotation-concordance`. Les quatre entrées ont été extraites par
`git show <commit>:<chemin>`, sans dépendre de fichiers de travail de A.

| Entrée | SHA-256 |
|---|---|
| [Patch de reprise](C0A_REPRISE_DIFF_COMPLET.patch) | `fd275e7f4951e7c34686918d875eb1a6cd794e699535a23f345383800ae67708` |
| [Delta B01](C0A_REPRISE_B01_DELTA.patch) | `edb421e899fab4bcce4f25cf4a63c13f3691e8586e1d6fa11d40783dac35e4ef` |
| [Complément A](RAPPORT_REPRISE_C0A_COMPLEMENT_B01.md) | `275c81a3db58981e5f085e1b6b5d0de5b8f2f5dd9898c77a5d25db1c5083105a` |
| [Rapport de reprise antérieur](RAPPORT_REPRISE_C0A.md) | `66430e64b661f4ebc9670ae031d9048f02d87cee3481d34bfcff130da0131bad` |

B a créé une copie Git indépendante au socle
`515666eb8c6e7fdcdd265f9187c9c37b769b0fed`, puis appliqué le patch de reprise
et le delta, dans cet ordre; les deux `git apply --check` réussissent.
Le candidat reconstruit contient exactement les huit fichiers C0-A attendus,
**1 750 insertions et 140 suppressions** par rapport au socle, sans migration.
Le delta touche seulement `concordance.py`, `protection.py` et le fichier de
contre-épreuves autorisé : 148 insertions, 14 suppressions. Les trois empreintes
reconstruites correspondent exactement à celles du complément A.

Le manifeste des huit fichiers est [conservé](preuves_revue_B01/candidat_sha256.json).
Les cinq fichiers non visés par le delta restent ceux de la reprise. Les
assignations de champs et classes Meta de `document_manager/models.py` et
`case_manager/models.py` sont identiques au socle par comparaison AST.
Le contrôle Django de migrations confirme l’absence de changement de schéma.

Les contrats de référence restent les versions approuvées :
[UC13 R2-ST](../../versions_approuvees/UC-C-13_C0A-UML-R2-ST/README.md),
[UC14 R2-HIST](../../versions_approuvees/UC-C-14_C0A-UML-R2-HIST/README.md),
[UC15 R2-DIAG](../../versions_approuvees/UC-C-15_C0A-UML-R2-DIAG/README.md).
Leurs trois manifestes actifs sont vérifiés : 26, 29 et 29 entrées, sans écart.
Les versions approuvées, leurs vues et les rapports antérieurs sont inchangés.

## 2. Environnement et isolation

Banc B : `/private/tmp/court-agent-b-b01-20261021-fdff7lb6/`. Copie du code,
interpréteur et dépendances indépendants; aucune intervention dans le banc A.
Python 3.11.9, Django 5.2.4, django-treebeard 4.8.0, PostgreSQL **18.1**, extension vector installée dans
le `template1` du cluster jetable; rôle `c0a_runner` non superutilisateur.

Les deux scripts synthétiques conservés dans `docs/agent_a/banc_c0a/` ont été
copiés à l’identique dans `harness/`. Ils refusent les fichiers `.env`, les
réglages `mysite.settings.*` et les connexions hors du socket privé, avant
l’appel à libpq. Chaque journal porte le témoin d’isolation. Les seules bases
admises par le lanceur sont les bases synthétiques du banc et `postgres` sur
ce socket. Aucun accès à la base réelle ou au serveur du projet.

Le cluster n’écoute pas en TCP; socket privé en mode 700, port 55439.
Le journal contient **102 connexions, toutes `host=[local]`**. Les horodatages
des 21 et 22 octobre sont conservés tels quels. Le cluster est **arrêté**,
avec arrêt propre dans le journal et absence de `postmaster.pid`.
Les migrations existantes n’ont servi qu’à créer la base de test jetable.

## 3. Correction initiale B01 et atomicité effectivement démontrées

Dans le scénario initial, T1 contrôle P/E1/E2; T2 retire E1 par le service,
puis ajoute E3 sous P, avec Statement ou citation. Le retrait nul de E1 ne
peut plus être compensé par le retrait multiple de P/E3 : le contexte attend
une seule identité par retrait et constate ici l’absence de E1.

Les deux contre-épreuves B vérifient, sur des PID PostgreSQL distincts :

- `SuppressionRefusee` pour T1;
- P/E2/E3 encore présents et compteur `numchild` cohérent;
- seule l’archive de E1 créée et validée par T2 subsiste;
- l’extrémité reliée à E2 pointe de nouveau sur le nœud vivant, sans archive;
- aucune suppression ni archive de T1 ne reste après son refus.

B vérifie aussi une édition HTTP et un repointage vers une citation **avant
la première archive** : le nouveau contrôle d’état refuse T1; tous ses retraits,
archives et repointages sont annulés, tandis que le nouvel état validé par T2
reste présent. Les tests de panne après archive, repointage et premier retrait
d’A passent également dans la suite complète exécutée par B.

Ces résultats confirment la correction de la compensation initiale et les
rollbacks demandés. Ils ne garantissent pas le contrôle d’état jusqu’au SQL.

## 4. Blocage résiduel UC14 — état changé après la garde

**Références : UC14 AC02, AC03, AC04, AC06; C14-D2.**
Localisation du candidat : `concordance.py:393–400` et
`protection.py:246–262`. La garde compare l’état de l’instance collectée
(document, chemin, intitulé, numéro et clé générique), puis consigne son ID.
Elle ne maintient aucun verrou de ligne entre cette vérification et le SQL.
La suppression SQL porte sur les PK collectées, sans condition sur cet état.

### Entrelacement démontré avec la voie d’édition approuvée

1. T1 précontrôle P/E1/E2, crée les archives et repointe les extrémités.
2. La garde `pre_delete` d’E2 accepte son état ancien et consigne son ID.
3. Juste avant le `DELETE` SQL d’E2, T2 charge cette même occurrence et appelle
   **`ajax_edit_node`** avec un nouveau texte. L’édition réussit, répond
   **HTTP 200 / success**, crée son Statement privé et valide le repointage.
4. T1 reprend son SQL. E2 est supprimée par PK; le relevé de la garde contient
   déjà l’ID attendu, et le contrôle final du chemin est vide.
5. T1 termine sans refus. L’archive d’E2 décrit l’ancien Statement/texte et
   l’extrémité reste repointée sur cette archive, sans capturer l’association
   au nouveau Statement que T2 venait de valider.

Exécution conservée : **T1 PID 47776, T2 PID 47777**, occurrence **945**.
Ancien Statement **592**, nouveau Statement **593**. L’édition HTTP répond
success; T1 ne lève aucun refus; P/E1/E2 sont tous retirés. L’archive d’E2
porte encore Statement 592 et « enfant deux »; l’extrémité pointe sur l’archive 52.

Le nouveau Statement et ses captures ne sont pas purgés : le défaut porte sur
l’état exact de l’occurrence retirée et son association documentaire conservée,
non sur une destruction générale de tous les textes.

### Variante citation

Même fenêtre : T2 repointe E2 vers une citation par `LibraryNode.save()`,
comme le test de repointage d’A, mais **après** les gardes. T1 retire ensuite
l’occurrence-citation sans refus, en l’archivant comme l’ancien Statement.
C14-D2 impose pourtant le refus de ce contenu dans le profil C0-A.
PID **47781 / 47782**, occurrence **959**, ancien Statement **602**, citation
**59**. Les observations détaillées sont [conservées](preuves_revue_B01/observations_B.json).

### Portée et validité de la contre-épreuve

Le scénario B ne remplace ni les gardes ni le SQL. `connection.execute_wrapper`
intercale T2 avant le `DELETE` visant la PK, puis exécute la requête originale
avec ses paramètres inchangés. T2 utilise une autre connexion et valide avant
la reprise de T1. L’édition de texte utilise la vue approuvée; la variante
citation utilise une sauvegarde ORM, sans SQL brut ni bulk update.

Le collecteur de Django installé confirme l’ordre : `pre_delete.send` dans
`django/db/models/deletion.py:455–463`, puis `delete_batch(pk_list)` à la ligne
501. Un ordonnancement concurrent peut donc s’intercaler dans cette fenêtre.
Le jeu de données reprend les fixtures synthétiques de A; les entrelacements
et assertions de conformité sont propres au module B conservé dans les preuves.

**Ce défaut est bloquant pour le profil UC14 courant.** Il s’exerce dans la
suppression elle-même, sur une occurrence encore présente et avec une édition
UC13 ordinaire; il ne dépend pas du gel global, des prochains modèles ou d’un
contournement par SQL. Le renvoyer à L5 ne satisferait pas le contrôle d’état
ajouté par B01 ni la politique d’archive fidèle de C14-D2.

## 5. Tests effectivement exécutés par B

| Phase / journal conservé | Découverts et exécutés | Résultat réel | Code |
|---|---:|---|---:|
| `candidat-app` : 16 paquets applicatifs, incluant UC13/14/15 et les six tests de concurrence A | 270 | Tous OK, 19,105 s | 0 |
| `b-independant` : deux variantes initiales, deux mutations avant archive, deux mutations avant DELETE | 6 | **4 OK, 2 échecs de conformité** décrits au §4, 3,494 s | 1 |
| `candidat-outillage` : projection et oracle A/B | 33 | Tous OK, 0,034 s | 0 |
| `candidat-schema` | Contrôles Django | `No changes detected`; check sans problème | 0 |
| `ancienne-contre-epreuve-A` : six tests corrigés A, deux modules de production antérieurs | 6 | **2 OK, 4 échecs attendus**, 3,771 s | 1 |
| `ancienne-contre-epreuve-B` : deux remplacements initiaux indépendants | 2 | **2 échecs attendus**, 1,209 s | 1 |

Les quatre échecs d’A contre l’ancienne version se décomposent en **trois
acceptations indues** (deux remplacements, un repointage) et **un motif de refus
différent** pour l’ajout d’enfant, auparavant refusé par comptage. Ce dernier
n’est pas présenté comme une quatrième perte de données. Les tests détectent
bien les comportements corrigés; ils ne couvrent pas la fenêtre du §4.

Pour ces contre-épreuves seulement, B a replacé `concordance.py` et
`protection.py` du premier patch dans sa copie jetable, en conservant les
tests corrigés A. Un `finally` a restauré les modules corrigés et vérifié les
huit empreintes du candidat. Aucune modification du banc A ni du code partagé.

La suite livrée ne montre donc aucune régression détectée sur UC13/14/15,
mais ses 270 succès ne suffisent pas à déclarer UC14 conforme face aux deux
échecs B. Aucun test navigateur ou essai sur données réelles n’est annoncé.

## 6. Réponses aux six points du mandat

| Point | Conclusion indépendante |
|---|---|
| 1. B01 initial Statement / citation | Corrigé dans les deux contre-épreuves exécutées; l’ancienne version échoue |
| 2. Occurrences précontrôlées et archivées seules supprimables | Les deux remplacements initiaux sont refusés. La garantie complète d’archive fidèle reste insuffisante : une identité attendue peut avoir changé d’état avant son retrait |
| 3. Modification du contenu entre contrôle et suppression | Refus avant archive confirmé; **protection insuffisante après la garde**, y compris par édition HTTP ordinaire |
| 4. Annulation atomique en cas de refus | Démontrée : archives/repointages/retraits de T1 annulés, T2 conservée. Dans la fenêtre résiduelle, aucun refus n’est déclenché et la transaction valide l’état incohérent |
| 5. Qualité des contre-épreuves | Les suites A et B font échouer la version antérieure. La nouvelle contre-épreuve tardive démontre une lacune supplémentaire dans la garantie demandée |
| 6. Non-régression UC13/14/15 | 270 tests et 33 d’outillage OK; contrats/empreintes inchangés. **Conformité UC14 non acquise**, malgré ces succès |

## 7. Réserves distinctes et correction attendue

**Orphelin tardif : inchangé, distinct, non bloquant isolément pour le profil
C0-A borné**, selon la [revue antérieure §3](REVUE_INDEPENDANTE_REPRISE_C0A.md#3-orphelin-tardif-signalé-par-a--reproduction-et-qualification).
Il concerne un ajout sur parent périmé, après le contrôle final de suppression.
Il n’est pas la modification d’une occurrence existante encore supprimée par
T1 décrite ici. B ne l’a pas réexécuté dans cette revue ciblée; aucun résultat
nouveau ne lui est attribué. Sa correction reste un avenant de la voie d’ajout.

Les refus d’édition/suppression des citations, le texte refusé restant affiché
jusqu’au rechargement, et les limites L1-A/C0-B/L5 restent celles du rapport
antérieur. Aucun de ces lots n’est réputé livré; aucune décision transversale
n’est réexaminée.

**Correction locale à faire examiner par A :** rendre le contrôle final de
l’état et le retrait indissociables, par une sérialisation de la ligne concernée
ou une autre garantie atomique justifiée, en conservant les gardes, l’API
Treebeard et le rollback de l’ensemble. Une simple nouvelle lecture sans
protection jusqu’au DELETE laisserait une autre fenêtre.

Le test futur doit accepter les deux ordres sûrs : T2 valide d’abord et T1
refuse l’état modifié; ou T1 protège sa ligne jusqu’au retrait et l’édition T2
attend puis refuse atomiquement la cible disparue. Il ne doit pas imposer
une validation de T2 pendant qu’un verrou légitime l’empêche. Aucune nécessité
de concevoir un verrouillage général des arbres ou de changer le schéma n’est
établie par cette revue. B n’implante pas cette correction dans ce mandat.

**Ne pas intégrer le candidat actuel.** Soumettre une correction locale et
ses contre-épreuves adaptées, puis vérifier son delta et les régressions
affectées; pas de reprise générale des dossiers UML. L’objectif reste la
clôture de C0-A, puis son intégration séparément autorisée avant le lot suivant.

## 8. Preuves conservées et commandes

[Sources de tests, journaux et index](preuves_revue_B01/README.md),
[manifest SHA-256](preuves_revue_B01/manifest_sha256.json),
[contrôles finaux](preuves_revue_B01/verification_finale.json).
Le rapport complète la revue du patch antérieur sans la remplacer.

Depuis un banc reconstruit et isolé comme au §2, les commandes réellement
employées sont celles-ci (`<banc>` remplace le chemin B indiqué plus haut) :

```sh
<banc>/venv/bin/python <banc>/harness/run_tests.py candidat-app DAL Utils ai_services argument_manager case_manager cause_manager core document_manager email_manager events googlechat_manager helpers pdf_manager photos protagonist_manager video_manager
<banc>/venv/bin/python <banc>/harness/run_tests.py b-independant revue_b01_B_tests.RevueB01
<banc>/venv/bin/python <banc>/harness/run_tests.py candidat-outillage scripts.regime_citations.test_projection scripts.regime_citations.test_verifier_ab
<banc>/venv/bin/python <banc>/harness/run_tests.py candidat-schema C0A_SCHEMA_CHECK
<banc>/venv/bin/python <banc>/harness/run_tests.py ancienne-contre-epreuve-A document_manager.test_e01_numerotation.C0ARepriseConcurrence
<banc>/venv/bin/python <banc>/harness/run_tests.py ancienne-contre-epreuve-B revue_b01_B_tests.RevueB01.test_B01_statement_initial_refuse revue_b01_B_tests.RevueB01.test_B01_citation_initial_refuse
```

Les deux dernières commandes ont été exécutées avec les deux modules antérieurs,
puis restauration vérifiée. Elles ne sont pas des tests du candidat corrigé.

**Contrôle final :** 671 fichiers suivis du dépôt partagé hors `docs/` et
`legal/` comparés au relevé de début de mandat, sans écart; HEAD partagé
`f35ec8586866f4359d44f52a0bc5cc57c0804217` inchangé. Aucun fichier applicatif
partagé, migration, branche de A, pilote, sauvegarde ou serveur du projet
modifié. Aucun commit, push, fusion ou déploiement dans cette revue.
