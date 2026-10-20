# C0-A — Rapport d’exécution et dossier de revue indépendante

Date : 19 octobre 2026. Mandat : autorisation limitée de C0-A, conformément au §10.5 de `DECISIONS_ARCHITECTURE_C_CONSOLIDEES.md` et aux six critères d’acceptation du mandat.

**Résultat : C0-A réalisé dans une copie indépendante de P6, prêt pour revue indépendante. La validation finale comporte 209 tests réussis, dont 31 nouveaux tests C0-A. Aucun changement de schéma n’est détecté. Aucune intégration ni autorisation du lot suivant n’est déduite de ce résultat.**

## 1. Livrable et périmètre exact

Le travail se trouve exclusivement dans :

`/private/tmp/court-agent-b-c0a-20261019-bmr16wwh/`

| Élément | Valeur |
|---|---|
| Copie Git indépendante | `repo/` |
| Base exacte, HEAD inchangée | `212a7feee81aef46a5b43d36e8eeafe0f8870064` |
| Branche locale de la copie | `agent-b/c0-a` |
| État livré | Modifications non commitées, rien dans l’index; aucun remote configuré |
| Diff complet autonome | [C0A_DIFF_COMPLET.patch](C0A_DIFF_COMPLET.patch), également reproduit intégralement en annexe |
| Preuves et empreintes | [VERIFICATIONS_C0A.json](VERIFICATIONS_C0A.json) |
| Configuration synthétique | [c0a_settings.py](../harness/c0a_settings.py) |
| Lanceur avec gardes d’isolation | [run_tests.py](../harness/run_tests.py) |
| Journaux | `../logs/`, conservés, y compris les contre-épreuves en échec avant correction |

Le diff comporte **8 fichiers, 495 lignes ajoutées et 78 retirées** : six fichiers de production expressément permis et deux modules de tests E01. Aucun autre fichier de production n’a été modifié; aucune extension du périmètre n’a été nécessaire.

| Fichier | Modification |
|---|---|
| `document_manager/views/produced_views.py` | Faire passer les deux routes actives d’édition et de suppression par les services protégés. |
| `document_manager/concordance.py` | Détachement avant modification; captures avant/après; précontrôle des suppressions; conservation des captures utilisées; lecteur d’appuis limité au couple documentaire et au type vérifié. |
| `document_manager/protection.py` | Gardes ORM ciblées sur textes partagés, captures utilisées, archives liées et suppressions destructrices; vérification de l’ancien document d’un nœud historique. |
| `document_manager/models.py` | Uniquement la méthode de fraîcheur de `Correspondance`, contre les occurrences et leurs Statements actuels. |
| `case_manager/models.py` | Uniquement la méthode de fraîcheur de `ConfirmationAppui`, contre le nœud relu et le Statement effectivement porté. |
| `document_manager/export_concordance.py` | Transmettre le couple documentaire; rendre les anomalies de type/archive explicites dans la note de la ligne. |
| `document_manager/test_e01_numerotation.py` | Ajouter `C0AEditionEtConservation` : 21 tests. |
| `case_manager/test_e01_cotes_concordance.py` | Ajouter `C0AFraicheurEtPerimetre` : 10 tests. |

Les deux anciens modules E01 sont conservés octet pour octet comme préfixe des fichiers livrés. Aucune attente d’un ancien test n’a été réécrite. Les définitions de champs, les classes `Meta` et les migrations sont identiques à P6; les méthodes et gardes Python seules ont changé dans les modèles.

## 2. Corrections et conséquences observables

### 2.1 Édition d’une occurrence

`ajax_edit_node` ne réécrit plus directement le `Statement` partagé. La route appelle `detacher_pour_edition`, qui conserve une capture du texte avant changement et donne un nouveau Statement à l’occurrence lorsque le contenu est partagé ou protégé. Les autres occurrences conservent leur Statement et leur texte. Un texte privé reçoit aussi une capture avant puis après réécriture. Une sauvegarde textuellement identique ne détache pas le Statement et ne périme pas la confirmation.

Les occurrences du référent historique et des documents `REPRODUCED` refusent l’édition, y compris le simple renommage par la route HTTP. Une écriture ORM `Statement.save()` qui réécrirait un texte porté par plusieurs occurrences est refusée : l’appelant doit désigner l’occurrence et passer par le détachement. La garde historique de `LibraryNode.save()` examine désormais l’ancien document et le nouveau; déplacer le nœud hors du référent ne permet plus de contourner cette garde par un simple changement de document.

Les contenus génériques d’un autre type ou les liens génériques incomplets ne sont pas convertis silencieusement en Statements par l’éditeur. Le cas d’un nœud réellement vide reste admis.

### 2.2 Suppression, captures et refus atomiques

`ajax_delete_node` appelle `supprimer_occurrence`. Le service précontrôle le bloc entier avant toute archive, archive les occurrences liées, remplace les extrémités vivantes par leurs archives, puis supprime ce qui est autorisé dans la transaction.

Un nœud portant une `ConfirmationAppui` ou un `AncrageCitation` ne peut pas être supprimé physiquement : le schéma P6 ne fournit pas l’archivage de ces décisions et liens, et leur cascade les détruirait. Le service refuse donc **tout le bloc**, avant effet partiel. Ce refus conservateur vise aussi les lignes non confirmées; il ne constitue pas l’implémentation d’un nouvel archivage de décisions.

Un Statement orphelin reste conservé si ses appuis historiques ou ses captures sont encore utilisés. Les suppressions ORM d’une `VersionTexte` utilisée, d’une archive liée ou d’un Document emportant une concordance ou ses archives sont refusées. Ces gardes complètent les protections E01 déjà présentes. Un Document encore lié à un nœud peut également être refusé plus tôt par le `PROTECT` existant de Django.

Le nettoyage des Statements vérifie le ContentType exact : l’identifiant numérique d’un Event, par exemple, ne peut plus entraîner la suppression d’un Statement homonyme. L’archivage ne remplit `statement_pk` que pour un ContentType Statement vérifié. Cela n’ajoute pas un type aux anciennes archives.

Deux contre-épreuves injectent une panne après création d’archives et un refus après détachement. Les objets créés, textes, nœuds et extrémités reviennent à l’état antérieur. La route de suppression répond 403 aux refus métier; les pannes inattendues testées répondent 500 après annulation de la transaction du service. Les refus d’édition utilisent la réponse 403 de Django pour `PermissionDenied`.

### 2.3 Fraîcheur et conservation des anciennes décisions

`Correspondance.versions_courantes_examinees()` compare, pour chaque côté, l’ensemble des couples **(Statement actuel, empreinte du texte actuel)** à celui des captures examinées. L’appartenance au document déclaré et l’existence des occurrences/contenus sont contrôlées. Une occurrence archivée ou un contenu manquant/incompatible ne confirme pas le présent. Une relation sans texte examiné ne devient pas confirmée par vacuité.

`ConfirmationAppui.etat_courant()` relit le nœud en base, même si une ancienne instance est déjà en cache dans l’objet appelant. Il vérifie le type, l’identité du Statement et l’empreinte du texte. Un autre Statement de même texte invalide donc aussi la confirmation courante. Les états `CONFIRME` et `SANS_APPUI` suivent cette règle. Une ancienne confirmation sans capture est à réexaminer; aucun examen ancien n’est inventé.

Ces contrôles calculent `A_REEXAMINER` **sans écraser l’état historique enregistré ni remplacer les captures existantes**. Après une suppression autorisée, la concordance, ses captures examinées et l’archive restent consultables. Ils ne constituent pas le manifeste d’occurrences ou le journal immuable prévus par L1-A/C0-B.

### 2.4 Lecture des appuis historiques

L’export transmet désormais explicitement `document_source` et `document_cible` au lecteur. Celui-ci vérifie le document cible réel, filtre les correspondances au couple, vérifie l’appartenance de chaque antécédent au document source et son ContentType Statement avant de rechercher un `AppuiDepotJuillet`. Les groupes structurels réellement vides sont ignorés.

L’ancien appel sans source explicite reste utilisable si la cible possède une seule origine documentaire; plusieurs origines provoquent un `ValueError` explicite. L’export précise toujours la paire et ne mélange donc plus les appuis d’un autre Document.

Une source archivée sans type attesté, absente ou de type incompatible provoque un diagnostic. L’export conserve la ligne, laisse ses `appuis_origine` vides et joint le diagnostic à sa note; il n’infère aucun appui à partir d’un ancien `object_id`. Cette absence diagnostiquée ne vaut pas preuve d’absence d’appui. Aucun champ `nature`, filtre sur une qualification future ou nouveau contrôle strict d’export n’est anticipé.

## 3. Preuves d’isolation et respect des ressources de A

La copie a son propre répertoire `.git`, ses propres objets, aucune référence distante et aucun fichier `objects/info/alternates`. Elle a été initialisée puis alimentée à partir du seul SHA P6, en lisant le dépôt principal. Ce n’est pas un worktree et ses objets ne sont pas liés par des hardlinks à ceux de A. Son HEAD demeure P6 : aucun commit n’a été créé.

Le banc PostgreSQL **18.1** est un cluster nouvellement initialisé dans `../pgdata/`, avec un socket privé `../socket/`, port 55439 et `listen_addresses=''`. Il n’écoute sur aucun port TCP. Il utilise exclusivement les données synthétiques des tests et les migrations P6 existantes. Les bases sont `court_c0a` et `test_court_c0a` dans ce cluster. Le rôle de préparation `c0a_owner` et le rôle d’exécution `c0a_runner` sont propres à ce banc; le second n’est pas superutilisateur. `pgvector` a été préparé dans le template du seul cluster jetable. Aucun paramètre de rôle ou extension de la base réelle n’a été modifié.

La configuration Django de test est autonome et n’importe aucun module `mysite.settings.*`. Les listes d’applications et de middleware ont été extraites comme constantes par lecture AST de P6, sans exécuter ses settings. L’environnement du processus est vidé puis remplacé par une liste explicite; stockage, courriel et cache sont locaux au banc. Les clés de services sont des valeurs synthétiques désactivées.

Le lanceur interdit la lecture des fichiers `.env*`, l’import des settings réels et les connexions Python hors du socket privé. Il enveloppe aussi `psycopg2.connect`, afin de refuser avant `libpq` tout hôte, rôle ou nom de base hors de sa liste locale. Chaque journal contient la contre-épreuve : `external PostgreSQL probe rejected before libpq`. Ce test tente seulement l’entrée du garde; aucune connexion à la base réelle n’est établie. Ces mesures décrivent le banc de test; elles ne sont pas présentées comme des protections SQL de production de L1-A ou L5.

Les premières mesures ont utilisé l’interpréteur et les dépendances du `.venv` existant **en lecture seule**, avec ces settings autonomes. Pour la livraison, un environnement Python distinct a été créé dans `../venv/` : interpréteur copié et dépendances recopiées, sans lien vers le site-packages du dépôt principal, sans installation de P6 en mode editable. La validation finale des 209 tests et le contrôle de schéma ont été rejoués avec cet environnement indépendant. La bibliothèque standard demeure celle de l’installation système Python 3.11.9.

Le cluster jetable a été **arrêté après validation**; `postmaster.pid` est absent. Son répertoire et ses journaux sont conservés pour revue. Aucune base réelle, sauvegarde, ressource de récupération, ressource de bascule ou serveur de déploiement n’a été utilisé.

Le dépôt principal est propre à la livraison. Les références contrôlées n’ont pas changé :

| Référence du dépôt principal | SHA conservé |
|---|---|
| `epic/E01-numerotation-concordance` et HEAD | `14f7533650d2a28832698b2222ced1df1cd89bb1` |
| `integration/quote-regime-step1` — cible P6 | `212a7feee81aef46a5b43d36e8eeafe0f8870064` |
| `docs/agent-b-pont-probatoire-20261019` | `06fe44c1a7e8582792f9d1fcfcba8155046168ee` |

Les fichiers de pilote, scripts, oracles et tests de l’Agent A sont identiques à P6 dans la copie. Les trois documents antérieurs de conception/validation ont conservé leurs empreintes; celles-ci figurent dans le JSON de vérification. Aucun fichier de `legal/`, aucune cote historique et aucun fichier de l’archive gelée n’ont été écrits. D05 demeure en arbitrage : l’exécution des tests existants de cotation ne constitue aucune approbation de leur politique future.

## 4. Tests effectivement exécutés

### 4.1 Référence, contre-épreuves et corrections

Les temps ci-dessous sont ceux affichés par le runner, hors préparation du banc. Les journaux conservent les sorties complètes; les essais négatifs antérieurs n’ont pas été remplacés par les résultats positifs.

| Exécution | Tests | Résultat | Temps | Journal |
|---|---:|---|---:|---|
| Référence : quatre suites applicatives à P6, avant modification de production | 145 | OK | 9,822 s | [baseline.log](../logs/baseline.log) |
| Première mise au point des contre-épreuves | 28 | 22 échecs, 3 erreurs | 1,415 s | [counterexamples-before.log](../logs/counterexamples-before.log) |
| Contre-épreuves stabilisées, avant corrections de production | 29 | 23 échecs, 2 erreurs | 1,507 s | [counterexamples-before-final.log](../logs/counterexamples-before-final.log) |
| Première correction, anciennes suites et 29 nouveaux tests | 174 | OK | 11,508 s | [corrected.log](../logs/corrected.log) |
| Deux gardes ORM supplémentaires, avant leur correction | 2 | 2 échecs | 0,063 s | [guards-before.log](../logs/guards-before.log) |
| Quatre suites applicatives avec les 31 nouveaux tests | 176 | OK | 12,321 s | [final.log](../logs/final.log) |
| Tests unitaires des instruments projection/comparateur de A, inchangés | 33 | OK | 0,158 s | [instrument-unit.log](../logs/instrument-unit.log) |
| **Rejeu final combiné dans le venv indépendant** | **209** | **OK, code de sortie 0** | **14,971 s** | [final-independent.log](../logs/final-independent.log) |
| `makemigrations --check --dry-run`, puis `check`, via le lanceur isolé | — | `No changes detected`; `System check identified no issues (0 silenced).`, code 0 | — | [schema-check.log](../logs/schema-check.log) |

Pendant la mise au point initiale d’un **nouveau** test, l’attente a été corrigée pour accepter aussi le `ProtectedError` déjà émis par le `PROTECT` de P6 lors de la suppression d’un Document vivant. Cette protection existante satisfaisait déjà le refus attendu. Le contrôle de la suppression d’un Document dont l’occurrence est archivée a ensuite été ajouté pour éprouver le cas réellement exposé. Aucun ancien test n’a changé. Les deux erreurs du jeu stabilisé avant correction montrent notamment l’API de paire encore absente et le traitement défectueux d’une source archivée.

Les messages 403 et 500 présents dans les journaux positifs correspondent aux refus et pannes volontairement exercés, ainsi qu’aux contre-épreuves des suites existantes; le résultat agrégé final est `OK`, sans échec ni erreur de test.

### 4.2 Composition des 209 tests finaux

| Module | Tests exécutés | Nouveaux tests C0-A |
|---|---:|---:|
| `document_manager.test_e01_numerotation` | 72 | 21 |
| `case_manager.test_e01_cotes_concordance` | 66 | 10 |
| `core.test_regime_citations` | 33 | 0 |
| `argument_manager.test_affidavit_ordre` | 5 | 0 |
| `scripts.regime_citations.test_projection` | 12 | 0 |
| `scripts.regime_citations.test_verifier_ab` | 21 | 0 |
| **Total** | **209** | **31** |

La référence de 145 tests est constituée des quatre premières suites avant ajout de C0-A : 51 + 56 + 33 + 5. Les tests des deux instruments sont des tests unitaires sur fixtures : leur succès **n’annonce pas une nouvelle exécution du pilote, de P6 sur le référent réel, de la récupération ou de la bascule de A**.

Les contrôles hors runner comprennent `git diff --check` (succès), la comparaison AST des définitions de modèles avec P6, la conservation exacte du préfixe des deux anciens fichiers de tests, la liste exhaustive des huit fichiers modifiés et les empreintes du patch/fichiers. Aucun fichier de migration n’a changé et aucune migration nouvelle n’a été générée. Les migrations existantes ont seulement servi à créer la base jetable des tests.

## 5. Correspondance avec les critères d’acceptation

Abréviations : **D** = `document_manager.test_e01_numerotation.C0AEditionEtConservation`; **P** = `case_manager.test_e01_cotes_concordance.C0AFraicheurEtPerimetre`. Les identifiants ci-dessous sont ceux des tests réellement exécutés.

| Critère du mandat | Preuves principales réussies | Portée de la conclusion |
|---|---|---|
| 1. Modifier une occurrence partagée sans modifier les autres | D.`test_http_edition_detache_deux_documents_produced`; D.`test_http_cible_detache_le_texte_du_referent`; D.`test_ecriture_orm_directe_dun_statement_partage_est_refusee` | Route HTTP avec détachement; refus de l’écriture ORM partagée en place. |
| 2. Maintenir la protection des référents historiques | D.`test_http_referent_refuse_sans_effet_partiel`; D.`test_changer_le_document_dun_noeud_historique_ne_contourne_pas_la_garde`; anciennes suites E01 de protection | Protections E01 ciblées, sans promesse de gel global L5. |
| 3. Réexaminer après changement de texte ou de Statement | D.`test_traitement_reexamine_apres_detachement_partage`; D.`test_meme_texte_autre_statement_reexamine_le_traitement`; D.`test_detachement_du_cote_source_perime_aussi_le_traitement`; P.`test_confirmation_appui_perimee_apres_detachement`; P.`test_meme_texte_autre_statement_invalide_meme_un_noeud_deja_charge` | Identité et texte actuels relus. Le manifeste complet des occurrences reste à L1-A. |
| 4. Garder les décisions et captures disponibles | D.`test_http_suppression_liee_archive_et_preserve_la_source`; D.`test_suppression_conserve_les_captures_du_statement_devenu_prive`; D.`test_purge_directe_du_statement_examine_est_refusee`; D.`test_purge_directe_dune_capture_examinee_est_refusee`; D.`test_suppression_archive_liee_est_refusee`; P.`test_suppression_avec_decision_dappui_refuse_tout_le_bloc` | États/captures existants conservés lors des voies corrigées; suppression refusée lorsqu’aucun archivage disponible ne sauverait la décision. Aucun journal de reconfirmation créé. |
| 5. Atomicité des refus | D.`test_http_referent_refuse_sans_effet_partiel`; D.`test_refus_apres_detachement_annule_aussi_les_nouveaux_objets`; D.`test_echec_archivage_annule_tout_le_bloc_http`; P.`test_suppression_avec_decision_dappui_refuse_tout_le_bloc` | Absence d’effet partiel après refus préalable, refus tardif et panne d’archivage injectée. Pas de certification de sérialisation concurrente globale. |
| 6. Non-régression P6/citations | 145 anciens tests applicatifs conservés et réussis; 33 tests unitaires des instruments inchangés réussis | Non-régression sur les suites et fixtures exécutées; aucune validation réelle/reprise de pilote revendiquée. |

Les variantes C0-A des scénarios de conception sont rattachées ainsi :

| Scénario | Couverture réalisée dans C0-A | Reste au plan futur |
|---|---|---|
| NR03 | Réécriture privée/partagée, source ou cible; nouvelle identité de Statement même à texte égal; anciennes captures conservées; sauvegarde identique témoin | Composition exacte des occurrences d’un examen, historique des reconfirmations, concurrence et intégration CF3 complète |
| NR07 | Lecteur explicite du couple; appel ambigu refusé; autre origine exclue de l’export; ContentType vérifié; archive inconnue diagnostiquée | Qualification `nature`, manifeste, types historiques attestés et sélection CF3 |
| NR11 | Deux routes HTTP corrigées; référent/REPRODUCED refusés; suppression autorisée archivée; refus/pannes atomiques | Gel de VersionActe, autres surfaces de mutation et protections globales L5 |
| TR02, partie C0-A | Détachement ou substitution rend l’état courant à réexaminer; confirmation sans capture ne certifie pas le texte courant; aucune capture ancienne inventée | Transition complète et admissibilité du nouvel export strict renforcé en C0-B |

Les **38 scénarios du plan consolidé restent conservés dans ce document antérieur**. Ce rapport ne les marque pas collectivement exécutés; il ne revendique que les variantes ci-dessus et les tests nommés. Les contrôles nouveaux IM01–IM08 et la transition complète TR01–TR06 ne sont pas certifiés par C0-A.

## 6. Problèmes confirmés et limites restantes

### 6.1 Défauts corrigés dans le lot

Les contre-épreuves ont confirmé la réécriture HTTP d’un Statement partagé, une fraîcheur calculée sur l’ancien Statement encore courant ailleurs, une confirmation servie depuis un nœud en cache et des chemins de suppression risquant d’emporter des captures ou décisions. Elles ont également exposé le mélange des origines documentaires dans le lecteur/export, la confusion des identifiants de contenus génériques et le contournement par réaffectation du document d’un nœud historique. Les corrections et les tests correspondants restent dans les six fichiers autorisés.

### 6.2 L1-A : examens, qualification et garanties persistantes

- Aucun `ExamenEditorial`, manifeste, ordinal de révision, journal JSON append-only, champ `nature` ou nouveau modèle n’est créé. Aucun trigger ni droit SQL de production n’est ajouté.
- La comparaison d’ensembles (Statement, empreinte) ne prouve pas l’identité de toutes les occurrences examinées. Remplacer une extrémité par une autre occurrence du même Statement ou changer la multiplicité d’occurrences identiques peut conserver le même ensemble. Il faut le manifeste L1-A pour attester la composition exacte et gérer les conflits de révision.
- Les signaux ciblés ne garantissent pas l’immutabilité contre `QuerySet.update`, bulk, SQL direct ou des écritures contournant le modèle. Le contenu d’une `VersionTexte` n’est pas rendu absolument immuable par C0-A : sa suppression est protégée lorsqu’elle est utilisée. Les protections SQL et leur exercice sous rôles restreints restent à réaliser.

### 6.3 C0-B : histoire complète et transition des anciennes confirmations

- Les captures et états disponibles restent lisibles dans les opérations corrigées, mais le service de reconfirmation existant peut encore remplacer les ensembles M2M examinés et ses projections. C0-A ne conserve pas toutes les décisions successives dans un journal distinct. La suppression explicite d’une décision ou d’une relation n’est pas globalement verrouillée par ce lot.
- Aucune confirmation historique n’est transformée en examen complet. L’absence de capture est à réexaminer; la présence de captures compatibles ne suffit toujours pas à prouver un ancien manifeste complet. L’éligibilité au nouvel export strict renforcé et la distinction entre relevé hérité et examen nouveau restent à C0-B.
- Les archives anciennes sans type attesté ne fournissent pas automatiquement des appuis historiques certifiés. C0-A produit un diagnostic et conserve les données disponibles; il ne reconstitue pas une preuve manquante. L’export existant ne reçoit pas ici le nouveau contrat strict complet de C0-B.
- Le refus conservateur de supprimer un nœud muni de confirmations/ancrages peut bloquer une opération qu’un futur archivage permettrait. C’est une limite volontaire du schéma P6, à résoudre par le lot habilité, pas par une cascade destructrice.

### 6.4 L5, intégration et sources réelles

- Aucun gel global de version, protection de toutes les M2M/fichiers/archives, isolation concurrente complète ou garde universelle de toutes les voies Treebeard/SQL n’est revendiqué. Les transactions testées démontrent l’atomicité des chemins corrigés, pas leur sérialisation contre toute écriture concurrente.
- Aucun adaptateur PHRASE de l’étape 2, contrôle des sources D07/CF4, changement de politique D05, migration future ou intégration CF3 complète n’est réalisé.
- Aucun contrôle du référent réel E01:T01/T03/T24, récupération A, bascule réelle, vérification de sauvegarde ou déploiement n’a été lancé. Les données réelles et les sources juridiques du dossier n’ont pas été modifiées ni réévaluées.

Ces limites sont des objets des lots ultérieurs; aucune n’est présentée comme déjà levée par le succès des 209 tests C0-A.

## 7. Reproduction dans le banc conservé

Le cluster local est arrêté. Les commandes suivantes servent uniquement à une revue de ce banc déjà préparé, dans son répertoire conservé. Elles ne chargent pas l’environnement du dépôt principal et ne passent pas par `manage.py` avec ses settings réels. Les chemins sont volontairement explicites.

Redémarrer le **seul cluster jetable** avec les mêmes options sans TCP :

```sh
/Library/PostgreSQL/18/bin/pg_ctl -D /private/tmp/court-agent-b-c0a-20261019-bmr16wwh/pgdata -l /private/tmp/court-agent-b-c0a-20261019-bmr16wwh/logs/postgresql.log -o "-k /private/tmp/court-agent-b-c0a-20261019-bmr16wwh/socket -p 55439 -h '' -c max_connections=20 -c shared_buffers=32MB -c fsync=off" -w start
```

Exécuter les six mêmes suites, sous un **nouveau nom de journal** pour préserver le résultat livré :

```sh
/private/tmp/court-agent-b-c0a-20261019-bmr16wwh/venv/bin/python /private/tmp/court-agent-b-c0a-20261019-bmr16wwh/harness/run_tests.py revue-independante document_manager.test_e01_numerotation case_manager.test_e01_cotes_concordance core.test_regime_citations argument_manager.test_affidavit_ordre scripts.regime_citations.test_projection scripts.regime_citations.test_verifier_ab
```

Contrôler l’absence de nouveau schéma, toujours via le même lanceur :

```sh
/private/tmp/court-agent-b-c0a-20261019-bmr16wwh/venv/bin/python /private/tmp/court-agent-b-c0a-20261019-bmr16wwh/harness/run_tests.py revue-schema C0A_SCHEMA_CHECK
```

Puis arrêter ce cluster :

```sh
/Library/PostgreSQL/18/bin/pg_ctl -D /private/tmp/court-agent-b-c0a-20261019-bmr16wwh/pgdata -m fast -w stop
```

Les migrations P6 existent dans la copie; le lancement de tests peut les appliquer à sa base jetable si nécessaire. Aucune commande d’application à un autre dépôt, de commit, de fusion ou de déploiement n’est proposée ici.

## 8. État remis à la revue

**Le périmètre C0-A est terminé pour revue indépendante.** Le diff reste non commité dans la copie isolée. Les 31 nouveaux tests et les suites de référence passent; les résultats, les états négatifs antérieurs et les limites sont conservés. La base jetable est arrêtée.

La prochaine étape est la revue de ce diff et de ses limites. Aucun autre lot n’est commencé. L’intégration éventuelle, toute modification hors périmètre et les lots L1-A/C0-B/L5 exigent le mandat applicable; le présent rapport n’en tient pas lieu.

## Annexe — Diff complet par rapport au SHA P6

Patch autonome : `C0A_DIFF_COMPLET.patch` (42 106 octets).

SHA-256 : `d10781a1c815e2b41d0c14ea39e8a51e8d2803bcb6c313fd4d22dec95b827a27`.

Le bloc ci-dessous reproduit tous les octets textuels du patch, sans abrègement.

```diff
diff --git a/case_manager/models.py b/case_manager/models.py
index 4a0f0cd548b9e0219bdc6852a6f6d26400ce27d2..83ee2094a8607b8a3ca58bb13db80eb80c1ea4bf 100644
--- a/case_manager/models.py
+++ b/case_manager/models.py
@@ -655,7 +655,16 @@ class ConfirmationAppui(models.Model):
         """
         if self.etat not in (EtatAppui.CONFIRME, EtatAppui.SANS_APPUI):
             return self.etat
-        if self.version_examinee and not self.version_examinee.est_courante:
+        from document_manager.models import LibraryNode, VersionTexte
+        noeud = LibraryNode.objects.filter(pk=self.noeud_id).first()
+        version = self.version_examinee
+        if (version is None or noeud is None
+                or noeud.content_type_id != ContentType.objects.get_for_model(Statement).pk
+                or noeud.object_id != version.statement_id):
+            return EtatAppui.A_REEXAMINER
+        statement = noeud.content_object
+        if not isinstance(statement, Statement) or \
+                version.empreinte != VersionTexte.empreinte_de(statement.text):
             return EtatAppui.A_REEXAMINER
         if self.portee_sha256 and \
                 self.portee_sha256 != self.empreinte_portee(self.portee):
diff --git a/case_manager/test_e01_cotes_concordance.py b/case_manager/test_e01_cotes_concordance.py
index 29df60161cba132e2ab73cd661ad61886361c2c9..e7777d0974cd38b0cdfc1bb32bde3c08954af5ef 100644
--- a/case_manager/test_e01_cotes_concordance.py
+++ b/case_manager/test_e01_cotes_concordance.py
@@ -842,3 +842,112 @@ class T29DemonstrationIntegree(T27ConditionsStrictes):
         r = self._construire()
         self.assertTrue(r['strict_possible'])
         self.assertTrue(exp.en_json(r, strict=True))
+
+
+class C0AFraicheurEtPerimetre(BaseCotes):
+    def setUp(self):
+        super().setUp()
+        self.schema = schema_acte()
+        self.source = faire_document("origine", schema=self.schema)
+        self.cible = faire_document("rédaction", schema=self.schema)
+        self.rs, self.rc = racine_de(self.source), racine_de(self.cible)
+        self.ns = ajouter(self.rs, self.source, "1", "texte initial")
+        self.nc = ajouter(self.rc, self.cible, "1", "", statement=self.ns.content_object)
+        self.piece = entree("P-5", un_evenement("pièce", self.d2015), rang=5)
+
+    def _confirmation(self, etat=EtatAppui.CONFIRME):
+        return ConfirmationAppui.objects.create(
+            noeud=self.nc, entree=self.piece if etat == EtatAppui.CONFIRME else None,
+            version_examinee=VersionTexte.capter(self.nc.content_object), etat=etat,
+            portee="la date", portee_sha256=ConfirmationAppui.empreinte_portee("la date"),
+            motif="décision examinée")
+
+    def _appui_source(self):
+        AppuiDepotJuillet.objects.create(statement=self.ns.content_object,
+                                       entree=self.piece, cote_citee="P-5")
+        return svc.relier(self.source, self.cible, [self.ns], [self.nc])
+
+    def _autre_origine(self):
+        autre = faire_document("autre analyse", schema=self.schema)
+        n = ajouter(racine_de(autre), autre, "1", "autre texte")
+        piece = entree("P-6", un_evenement("autre pièce", self.d2015), rang=6)
+        AppuiDepotJuillet.objects.create(statement=n.content_object, entree=piece, cote_citee="P-6")
+        svc.relier(autre, self.cible, [n], [self.nc])
+        return autre
+
+    def test_confirmation_appui_perimee_apres_detachement(self):
+        conf = self._confirmation()
+        svc.detacher_pour_edition(self.nc, "autre texte")
+        self.assertEqual(conf.etat_courant(), EtatAppui.A_REEXAMINER)
+        conf.refresh_from_db()
+        self.assertEqual(conf.etat, EtatAppui.CONFIRME)
+        self.assertEqual(conf.version_examinee.texte, "texte initial")
+
+    def test_meme_texte_autre_statement_invalide_meme_un_noeud_deja_charge(self):
+        conf = self._confirmation()
+        self.assertEqual(conf.noeud.object_id, self.ns.object_id)
+        nouveau = Statement.objects.create(text="texte initial")
+        LibraryNode.objects.filter(pk=self.nc.pk).update(object_id=nouveau.pk)
+        self.assertEqual(conf.etat_courant(), EtatAppui.A_REEXAMINER)
+
+    def test_absence_dappui_reexaminee_apres_detachement(self):
+        conf = self._confirmation(EtatAppui.SANS_APPUI)
+        svc.detacher_pour_edition(self.nc, "autre texte")
+        self.assertEqual(conf.etat_courant(), EtatAppui.A_REEXAMINER)
+
+    def test_confirmation_sans_capture_ne_certifie_pas_le_texte_courant(self):
+        conf = ConfirmationAppui.objects.create(noeud=self.nc, entree=self.piece,
+                                                etat=EtatAppui.CONFIRME)
+        self.assertEqual(conf.etat_courant(), EtatAppui.A_REEXAMINER)
+
+    def test_lecteur_restreint_au_couple_explicitement_demande(self):
+        self._appui_source(); self._autre_origine()
+        appuis = svc.appuis_dorigine(self.nc, document_source=self.source,
+                                    document_cible=self.cible)
+        self.assertEqual([a['entree'].pk for a in appuis], [self.piece.pk])
+
+    def test_lecteur_sans_couple_refuse_plusieurs_origines_documentaires(self):
+        self._appui_source(); self._autre_origine()
+        with self.assertRaises(ValueError):
+            svc.appuis_dorigine(self.nc)
+
+    def test_export_ne_melange_pas_les_appuis_dun_autre_document(self):
+        self._appui_source(); self._autre_origine()
+        resultat = exp.construire(self.source, self.cible)
+        lignes = [l for l in resultat['lignes'] if l.get('noeud_cible') == self.nc.pk]
+        self.assertEqual(len(lignes), 1)
+        self.assertEqual([a['entree_pk'] for a in lignes[0]['appuis_origine']], [self.piece.pk])
+
+    def test_identifiant_generique_ne_designe_pas_un_statement_homonyme(self):
+        event = Event.objects.create(pk=self.ns.object_id, date="2015-01-01", explanation="autre type")
+        self._appui_source()
+        LibraryNode.objects.filter(pk=self.ns.pk).update(
+            content_type=ContentType.objects.get_for_model(Event), object_id=event.pk)
+        with self.assertRaises(ValueError):
+            svc.appuis_dorigine(self.nc)
+        resultat = exp.construire(self.source, self.cible)
+        ligne = next(l for l in resultat['lignes'] if l.get('noeud_cible') == self.nc.pk)
+        self.assertEqual(ligne['appuis_origine'], [])
+        self.assertIn("Statement", ligne['note'])
+
+    def test_archive_non_typee_reste_diagnostiquee_sans_deviner(self):
+        self._appui_source()
+        svc.supprimer_occurrence(self.ns)
+        with self.assertRaises(ValueError):
+            svc.appuis_dorigine(self.nc)
+        resultat = exp.construire(self.source, self.cible)
+        ligne = next(l for l in resultat['lignes'] if l.get('noeud_cible') == self.nc.pk)
+        self.assertEqual(ligne['appuis_origine'], [])
+        self.assertIn("archiv", ligne['note'])
+
+    def test_suppression_avec_decision_dappui_refuse_tout_le_bloc(self):
+        from document_manager.protection import SuppressionRefusee
+        from document_manager.models import NoeudArchive
+        conf = self._confirmation()
+        avant = LibraryNode.objects.count()
+        with self.assertRaises(SuppressionRefusee):
+            svc.supprimer_occurrence(self.rc)
+        self.assertEqual(LibraryNode.objects.count(), avant)
+        self.assertEqual(NoeudArchive.objects.count(), 0)
+        self.assertEqual(ConfirmationAppui.objects.get(pk=conf.pk).version_examinee.texte,
+                         "texte initial")
diff --git a/document_manager/concordance.py b/document_manager/concordance.py
index 1cf3cb8a87b4f9e918d08b320444d58f9b61ee2e..ad5ee9e7be71455df236408ac8d35e0f8d1378ce 100644
--- a/document_manager/concordance.py
+++ b/document_manager/concordance.py
@@ -28,13 +28,15 @@ Reconfirmer les pièces d'un paragraphe réécrit ne dit rien de la première
 question. C'est la confusion que `etat_courant()` existe pour empêcher.
 """
 from django.db import transaction
+from django.contrib.contenttypes.models import ContentType
 
 from document_manager.models import (
     Correspondance, EtatConfirmation, ExtremiteCorrespondance, LibraryNode,
     RoleExtremite, Statement, TraitementEditorial, VersionTexte,
 )
 from document_manager.protection import (
-    SuppressionRefusee, archiver_noeud, est_reproduit, statement_protege,
+    ModificationRefusee, SuppressionRefusee, archiver_noeud, captures_utilisees,
+    est_reproduit, statement_protege, verifier_suppression_noeud,
 )
 
 
@@ -129,31 +131,44 @@ def antecedents_de(noeud_cible):
     return out
 
 
-def appuis_dorigine(noeud_cible):
-    """
-    Les appuis de JUILLET des antécédents de cette cible.
+def appuis_dorigine(noeud_cible, *, document_source=None, document_cible=None):
+    """Appuis de juillet du couple demandé, jamais ceux d'une autre origine.
 
-    Identifiés comme tels : ce sont les références de la version source, pas les
-    appuis du nouvel énoncé. Les confondre ferait passer pour déposé en juillet
-    un paragraphe qui ne l'a pas été.
+    L'appel historique sans couple reste admis pour une seule origine
+    documentaire. Une archive non typée ne permet pas d'utiliser son ancien
+    object_id comme un Statement.pk : elle demande un diagnostic explicite.
     """
     from case_manager.models import AppuiDepotJuillet
+    if document_cible is not None and document_cible.pk != noeud_cible.document_id:
+        raise ValueError("L'occurrence n'appartient pas au document cible demandé.")
+    corrs = correspondances_de(noeud_cible, RoleExtremite.CIBLE).filter(
+        document_cible_id=noeud_cible.document_id)
+    if document_source is not None:
+        corrs = corrs.filter(document_source=document_source)
+    elif corrs.order_by().values('document_source_id').distinct().count() > 1:
+        raise ValueError("Plusieurs documents source : préciser le couple documentaire.")
+
+    ct_statement = ContentType.objects.get_for_model(Statement)
     out = []
-    for ant in antecedents_de(noeud_cible):
-        if ant.object_id is None:
-            continue
-        for a in (AppuiDepotJuillet.objects
-                  .filter(statement_id=ant.object_id)
-                  .select_related('entree')):
-            out.append({
-                'antecedent': ant,
-                'appui_depot': a,
-                'entree': a.entree,
-                'cote_de_juillet': a.entree.cote,
-                'cote_citee': a.cote_citee,
-                'via_liasse': a.via_liasse,
-                'origine': 'VERSION SOURCE — appui du dépôt de juillet',
-            })
+    for corr in corrs:
+        for e in corr.extremites.filter(role=RoleExtremite.SOURCE).select_related('noeud'):
+            ant = e.noeud
+            if ant is None:
+                raise ValueError("Antécédent archivé ou absent : type historique non attesté.")
+            if ant.document_id != corr.document_source_id:
+                raise ValueError("L'antécédent n'appartient pas au document source déclaré.")
+            if ant.content_type_id is None and ant.object_id is None:
+                continue  # groupe structurel sans Statement, aucun appui à rechercher
+            if ant.content_type_id != ct_statement.pk or not isinstance(ant.content_object, Statement):
+                raise ValueError("L'antécédent ne porte pas un Statement vérifié.")
+            for a in (AppuiDepotJuillet.objects
+                      .filter(statement_id=ant.object_id).select_related('entree')):
+                out.append({
+                    'antecedent': ant, 'appui_depot': a, 'entree': a.entree,
+                    'cote_de_juillet': a.entree.cote, 'cote_citee': a.cote_citee,
+                    'via_liasse': a.via_liasse,
+                    'origine': 'VERSION SOURCE — appui du dépôt de juillet',
+                })
     return out
 
 
@@ -182,15 +197,18 @@ def detacher_pour_edition(noeud_cible, nouveau_texte, motif="réécriture"):
             f"texte ne se réécrit pas.")
 
     from document_manager.protection import est_referent
+    if est_referent(noeud_cible.document_id):
+        raise ModificationRefusee("Le texte d'une occurrence du référent ne se réécrit pas.")
+    if obj.text == nouveau_texte:
+        return obj
+    VersionTexte.capter(obj, motif="texte avant réécriture")
     partage = (LibraryNode.objects
                .filter(content_type=noeud_cible.content_type,
                        object_id=obj.pk)
                .exclude(pk=noeud_cible.pk).exists())
-    doit_detacher = partage or statement_protege(obj.pk) or \
-        est_referent(noeud_cible.document_id)
+    doit_detacher = partage or statement_protege(obj.pk)
 
     if doit_detacher:
-        VersionTexte.capter(obj, motif="texte source, avant détachement")
         nouveau = Statement.objects.create(
             text=nouveau_texte, is_true=obj.is_true,
             is_falsifiable=obj.is_falsifiable, is_user_created=True)
@@ -224,17 +242,9 @@ def supprimer_occurrence(noeud, motif="retrait décidé"):
     """
     bloc = [noeud] + list(noeud.get_descendants())
 
-    # --- contrôle préalable du bloc entier ---
+    # Vérifier aussi les décisions que la cascade détruirait, avant toute archive.
     for n in bloc:
-        if est_reproduit(n.document):
-            raise SuppressionRefusee(
-                f"Bloc refusé : le nœud {n.pk} appartient au document REPRODUIT "
-                f"« {n.document.title[:50]} ». Aucune suppression effectuée.")
-        from document_manager.protection import est_referent
-        if est_referent(n.document_id):
-            raise SuppressionRefusee(
-                f"Bloc refusé : le nœud {n.pk} appartient au référent "
-                f"historique. Aucune suppression effectuée.")
+        verifier_suppression_noeud(n)
 
     # --- archivage, puis dénouage des correspondances ---
     archives = {}
@@ -249,11 +259,9 @@ def supprimer_occurrence(noeud, motif="retrait décidé"):
     # --- les Statements devenus inutilisés ---
     # Un Statement encore porté par une autre occurrence reste intact ; un
     # Statement utilisé par un document REPRODUIT l'est quoi qu'il arrive.
+    ct_statement = ContentType.objects.get_for_model(Statement)
     candidats = {n.object_id for n in bloc if n.object_id is not None
-                 and n.content_type_id is not None}
-    ct_statement = next((n.content_type for n in bloc
-                         if n.content_type and n.content_type.model == 'statement'),
-                        None)
+                 and n.content_type_id == ct_statement.pk}
 
     for n in sorted(bloc, key=lambda x: -len(x.path)):
         LibraryNode.objects.filter(pk=n.pk).delete()
@@ -269,8 +277,8 @@ def supprimer_occurrence(noeud, motif="retrait décidé"):
             stmt = Statement.objects.filter(pk=sid).first()
             if stmt is None:
                 continue
-            if stmt.appuis_depot.exists():
-                # L'énoncé est cité par le constat du dépôt : il reste.
+            if stmt.appuis_depot.exists() or captures_utilisees(sid):
+                # Références historiques et textes d'examens restent consultables.
                 continue
             stmt.delete()
             supprimes.append(sid)
diff --git a/document_manager/export_concordance.py b/document_manager/export_concordance.py
index 54323f515a3d0fd1db14c3535a1c11eb5d89eafd..fc53b26abae4ba89b13214d18da2faecbe435429 100644
--- a/document_manager/export_concordance.py
+++ b/document_manager/export_concordance.py
@@ -304,8 +304,15 @@ def _ligne(c, es, ec, ns, nc, num_source, num_cible, index_cible, etat_courant,
     appuis_origine, appuis_retenus = [], []
     texte_rendu, non_resolues = None, []
 
+    note = c.note
     if nc is not None:
-        for a in svc.appuis_dorigine(nc):
+        try:
+            origines = svc.appuis_dorigine(
+                nc, document_source=c.document_source, document_cible=c.document_cible)
+        except ValueError as erreur:
+            origines = []
+            note = "\n".join(filter(None, [note, str(erreur)]))
+        for a in origines:
             appuis_origine.append({
                 'origine': a['origine'],
                 'antecedent_noeud': a['antecedent'].pk,
@@ -358,7 +365,7 @@ def _ligne(c, es, ec, ns, nc, num_source, num_cible, index_cible, etat_courant,
         'texte_rendu': texte_rendu,
         'citations_non_resolues': non_resolues,
         'motif': c.motif,
-        'note': c.note,
+        'note': note,
     }
 
 
diff --git a/document_manager/models.py b/document_manager/models.py
index a49db20d489169c7f9cde0205a64636963d50109..4a1592a4d991a1230c77c5637e84f72486721260 100644
--- a/document_manager/models.py
+++ b/document_manager/models.py
@@ -632,11 +632,29 @@ class Correspondance(models.Model):
         Une confirmation acquise sur V1 cesse de confirmer V2 — elle reste
         consultable, mais le traitement courant redevient à réexaminer.
         """
-        for v in list(self.versions_source_examinees.all()) + \
-                 list(self.versions_cible_examinees.all()):
-            if not v.est_courante:
+        # Lire les occurrences actuelles, pas le Statement ancien d'une capture.
+        # Sans manifeste, la composition d'un ancien examen n'est pas attestée.
+        contient_texte = False
+        for role, champ, document_id in (
+            (RoleExtremite.SOURCE, self.versions_source_examinees, self.document_source_id),
+            (RoleExtremite.CIBLE, self.versions_cible_examinees, self.document_cible_id),
+        ):
+            captures = {(v.statement_id, v.empreinte) for v in champ.all()}
+            actuels = set()
+            for e in self.extremites.filter(role=role).select_related('noeud'):
+                n = e.noeud
+                if n is None or n.document_id != document_id:
+                    return False
+                if n.content_type_id is None and n.object_id is None:
+                    continue
+                obj = n.content_object
+                if not isinstance(obj, Statement):
+                    return False
+                contient_texte = True
+                actuels.add((obj.pk, VersionTexte.empreinte_de(obj.text)))
+            if actuels != captures:
                 return False
-        return True
+        return contient_texte
 
     def etat_courant(self):
         """L'état tenant compte d'une éventuelle réécriture depuis la décision."""
diff --git a/document_manager/protection.py b/document_manager/protection.py
index 114f50c82b479b8815e5ac810a5124d2866dc358..894116bcccf903a164459692d471e0d8635cf00c 100644
--- a/document_manager/protection.py
+++ b/document_manager/protection.py
@@ -29,11 +29,12 @@ import hashlib
 from django.core.exceptions import PermissionDenied
 from django.contrib.contenttypes.models import ContentType
 from django.db.models.signals import pre_delete, pre_save
+from django.db.models import Q
 from django.dispatch import receiver
 
 from document_manager.models import (
     Document, DocumentSource, LibraryNode, NoeudArchive, ReferentHistorique,
-    Statement,
+    Statement, VersionTexte,
 )
 
 
@@ -129,6 +130,16 @@ def est_referent(document_pk):
     return ReferentHistorique.objects.filter(document_id=document_pk).exists()
 
 
+def captures_utilisees(statement_pk):
+    """Captures encore requises par les références E01 existantes."""
+    return VersionTexte.objects.filter(statement_id=statement_pk).filter(
+        Q(correspondances_source_examinees__isnull=False)
+        | Q(correspondances_cible_examinees__isnull=False)
+        | Q(confirmations_appui__isnull=False)
+        | Q(ancrages__isnull=False)
+    ).exists()
+
+
 def archiver_noeud(noeud, motif="", statement_supprime=False):
     """Conserve ce qu'une occurrence portait, avant sa disparition physique."""
     texte = ""
@@ -142,7 +153,8 @@ def archiver_noeud(noeud, motif="", statement_supprime=False):
         depth=noeud.depth,
         item=noeud.item or "",
         paragraph_number=noeud.paragraph_number or "",
-        statement_pk=noeud.object_id,
+        statement_pk=(noeud.object_id if noeud.content_type_id ==
+                      ContentType.objects.get_for_model(Statement).pk else None),
         statement_supprime=statement_supprime,
         texte=texte,
         texte_sha256=hashlib.sha256(texte.encode('utf-8')).hexdigest() if texte else "",
@@ -156,7 +168,11 @@ def archiver_noeud(noeud, motif="", statement_supprime=False):
 
 @receiver(pre_delete, sender=LibraryNode, dispatch_uid="e01_garde_noeud")
 def garde_suppression_noeud(sender, instance, **kwargs):
-    """Refuse la suppression d'un nœud reproduit ou appartenant au référent."""
+    verifier_suppression_noeud(instance)
+
+
+def verifier_suppression_noeud(instance):
+    """Précontrôle commun au service de bloc et aux suppressions ORM."""
     if est_reproduit(instance.document):
         raise SuppressionRefusee(
             f"Nœud {instance.pk} : il appartient au document REPRODUIT "
@@ -169,6 +185,11 @@ def garde_suppression_noeud(sender, instance, **kwargs):
             f"« {instance.document.title[:60]} », acte déposé. Sa structure "
             f"est figée."
         )
+    if instance.confirmations_appui.exists() or instance.ancrages_citation.exists():
+        raise SuppressionRefusee(
+            f"Nœud {instance.pk} : la suppression détruirait des décisions "
+            "d'appui ou des ancrages de citation; leur archivage n'est pas disponible."
+        )
 
 
 @receiver(pre_delete, sender=Statement, dispatch_uid="e01_garde_statement")
@@ -203,6 +224,29 @@ def garde_suppression_statement(sender, instance, **kwargs):
             f"Supprimer d'abord les occurrences, sinon elles désigneraient un "
             f"objet disparu."
         )
+    if instance.appuis_depot.exists() or captures_utilisees(instance.pk):
+        raise SuppressionRefusee(
+            f"Statement {instance.pk} : ses références historiques ou captures "
+            "examinées doivent rester consultables."
+        )
+
+
+@receiver(pre_delete, sender=VersionTexte, dispatch_uid="e01_garde_capture_utilisee")
+def garde_suppression_version_texte(sender, instance, **kwargs):
+    if (instance.correspondances_source_examinees.exists()
+            or instance.correspondances_cible_examinees.exists()
+            or instance.confirmations_appui.exists() or instance.ancrages.exists()):
+        raise SuppressionRefusee(
+            f"VersionTexte {instance.pk} : capture encore utilisée par un examen ou une citation."
+        )
+
+
+@receiver(pre_delete, sender=NoeudArchive, dispatch_uid="e01_garde_archive_liee")
+def garde_suppression_archive(sender, instance, **kwargs):
+    if instance.extremites.exists():
+        raise SuppressionRefusee(
+            f"Archive {instance.pk} : encore nécessaire à une concordance."
+        )
 
 
 @receiver(pre_delete, sender=Document, dispatch_uid="e01_garde_document")
@@ -223,6 +267,11 @@ def garde_suppression_document(sender, instance, **kwargs):
         raise SuppressionRefusee(
             f"Document {instance.pk} : référent historique. Acte déposé."
         )
+    if (instance.concordances_source.exists() or instance.concordances_cible.exists()
+            or instance.noeuds_archives.exists()):
+        raise SuppressionRefusee(
+            f"Document {instance.pk} : sa suppression détruirait une concordance ou ses archives."
+        )
 
 
 @receiver(pre_save, sender=Statement, dispatch_uid="e01_garde_texte_statement")
@@ -243,8 +292,9 @@ def garde_modification_statement(sender, instance, **kwargs):
     if ancien is None or ancien == instance.text:
         return  # création, ou sauvegarde sans changement de contenu
     ct = ContentType.objects.get_for_model(Statement)
-    for n in (LibraryNode.objects.filter(content_type=ct, object_id=instance.pk)
-              .select_related('document')):
+    occurrences = list(LibraryNode.objects.filter(
+        content_type=ct, object_id=instance.pk).select_related('document'))
+    for n in occurrences:
         if est_reproduit(n.document):
             raise ModificationRefusee(
                 f"Statement {instance.pk} : son texte est cité par le document "
@@ -257,6 +307,11 @@ def garde_modification_statement(sender, instance, **kwargs):
                 f"historique « {n.document.title[:60]} », acte déposé. Pour "
                 f"réécrire la version cible, lui donner son propre Statement."
             )
+    if len(occurrences) > 1:
+        raise ModificationRefusee(
+            f"Statement {instance.pk} : partagé par plusieurs occurrences. "
+            "Réécrire une occurrence par détachement, sans modifier les autres."
+        )
 
 
 @receiver(pre_save, sender=LibraryNode, dispatch_uid="e01_garde_noeud_maj")
@@ -271,11 +326,11 @@ def garde_modification_noeud(sender, instance, **kwargs):
     """
     if instance.pk is None:
         return
-    if not est_referent(instance.document_id):
-        return
     ancien = LibraryNode.objects.filter(pk=instance.pk).first()
     if ancien is None:
         return
+    if not (est_referent(ancien.document_id) or est_referent(instance.document_id)):
+        return
     surveilles = ('item', 'path', 'depth', 'content_type_id', 'object_id',
                   'document_id', 'is_evidence')
     changes = [c for c in surveilles
diff --git a/document_manager/test_e01_numerotation.py b/document_manager/test_e01_numerotation.py
index 5932484d74ed1ab6184293b042f1d0063b91def8..024369bfeae5adb934627a6c1e06a10a0f306cda 100644
--- a/document_manager/test_e01_numerotation.py
+++ b/document_manager/test_e01_numerotation.py
@@ -789,3 +789,220 @@ class T16EditionPartagee(BaseConcordance):
         self.assertEqual(
             LibraryNode.objects.get(pk=self.s["1"].pk).object_id, st.pk,
             "L'occurrence source continue de désigner le texte d'origine.")
+
+
+# C0-A — contre-épreuves sur occurrences, voies HTTP et conservation E01.
+class C0AEditionEtConservation(BaseE01):
+    def setUp(self):
+        super().setUp()
+        from django.contrib.auth import get_user_model
+        self.client.force_login(get_user_model().objects.create_superuser(
+            username="c0a", email="c0a@example.test", password="test"))
+        self.source = faire_document("origine", schema=self.schema)
+        self.cible = faire_document("rédaction", schema=self.schema)
+        self.rs, self.rc = racine_de(self.source), racine_de(self.cible)
+        self.st = Statement.objects.create(text="texte initial", is_user_created=True)
+        self.ns = ajouter(self.rs, self.source, "1", "", statement=self.st)
+        self.nc = ajouter(self.rc, self.cible, "1", "", statement=self.st)
+
+    def _post(self, action, noeud=None, **data):
+        from django.urls import reverse
+        return self.client.post(reverse("document_manager:ajax_" + action + "_node",
+                                        args=[(noeud or self.nc).pk]), data)
+
+    def _confirmer(self):
+        corr = svc.relier(self.source, self.cible, [self.ns], [self.nc])
+        return svc.confirmer_traitement(corr, TraitementEditorial.CONSERVE,
+                                       motif="textes examinés")
+
+    def test_http_edition_detache_deux_documents_produced(self):
+        response = self._post("edit", item="nouveau", text="texte réécrit")
+        self.assertEqual(response.status_code, 200)
+        self.ns.refresh_from_db(); self.nc.refresh_from_db(); self.st.refresh_from_db()
+        self.assertEqual(self.st.text, "texte initial")
+        self.assertEqual(self.ns.object_id, self.st.pk)
+        self.assertNotEqual(self.nc.object_id, self.st.pk)
+        self.assertEqual(self.nc.content_object.text, "texte réécrit")
+
+    def test_http_cible_detache_le_texte_du_referent(self):
+        ReferentHistorique.objects.create(document=self.source, libelle="référent")
+        response = self._post("edit", item="nouveau", text="texte réécrit")
+        self.assertEqual(response.status_code, 200)
+        self.st.refresh_from_db()
+        self.assertEqual(self.st.text, "texte initial")
+
+    def test_http_referent_refuse_sans_effet_partiel(self):
+        ReferentHistorique.objects.create(document=self.cible, libelle="référent")
+        counts = (Statement.objects.count(), VersionTexte.objects.count())
+        response = self._post("edit", item="interdit", text="interdit")
+        self.assertEqual(response.status_code, 403)
+        self.nc.refresh_from_db(); self.st.refresh_from_db()
+        self.assertEqual((self.nc.item, self.st.text), ("1", "texte initial"))
+        self.assertEqual(counts, (Statement.objects.count(), VersionTexte.objects.count()))
+
+    def test_http_reproduced_refuse_aussi_le_simple_renommage(self):
+        self.cible.source_type = DocumentSource.REPRODUCED
+        self.cible.save(update_fields=['source_type'])
+        response = self._post("edit", item="interdit", text="texte initial")
+        self.assertEqual(response.status_code, 403)
+        self.nc.refresh_from_db()
+        self.assertEqual(self.nc.item, "1")
+
+    def test_traitement_reexamine_apres_detachement_partage(self):
+        corr = self._confirmer()
+        svc.detacher_pour_edition(self.nc, "texte réécrit")
+        self.assertEqual(corr.etat_courant(), EtatConfirmation.A_REEXAMINER)
+        corr.refresh_from_db()
+        self.assertEqual(corr.etat, EtatConfirmation.CONFIRME)
+        self.assertEqual(corr.versions_cible_examinees.get().texte, "texte initial")
+
+    def test_meme_texte_autre_statement_reexamine_le_traitement(self):
+        corr = self._confirmer()
+        autre = Statement.objects.create(text="texte initial")
+        LibraryNode.objects.filter(pk=self.nc.pk).update(object_id=autre.pk)
+        self.assertEqual(corr.etat_courant(), EtatConfirmation.A_REEXAMINER)
+
+    def test_detachement_du_cote_source_perime_aussi_le_traitement(self):
+        corr = self._confirmer()
+        svc.detacher_pour_edition(self.ns, "autre origine")
+        self.assertEqual(corr.etat_courant(), EtatConfirmation.A_REEXAMINER)
+        self.st.refresh_from_db()
+        self.assertEqual(self.st.text, "texte initial")
+
+    def test_sauvegarde_identique_ne_detache_pas_le_statement(self):
+        corr = self._confirmer()
+        nouveau = svc.detacher_pour_edition(self.nc, "texte initial")
+        self.assertEqual(nouveau.pk, self.st.pk)
+        self.assertEqual(corr.etat_courant(), EtatConfirmation.CONFIRME)
+
+    def test_edition_privee_capture_le_texte_avant_modification(self):
+        prive = ajouter(self.rc, self.cible, "2", "avant")
+        svc.detacher_pour_edition(prive, "après")
+        self.assertEqual(set(VersionTexte.objects.filter(
+            statement_id=prive.object_id).values_list('texte', flat=True)), {"avant", "après"})
+
+    def test_http_suppression_liee_archive_et_preserve_la_source(self):
+        corr = self._confirmer()
+        response = self._post("delete")
+        self.assertEqual(response.status_code, 200)
+        archive = NoeudArchive.objects.get(noeud_pk=self.nc.pk)
+        self.assertEqual(archive.texte, "texte initial")
+        self.assertEqual(archive.document_id, self.cible.pk)
+        ext = corr.extremites.get(role=RoleExtremite.CIBLE)
+        self.assertIsNone(ext.noeud_id)
+        self.assertEqual(ext.archive_id, archive.pk)
+        self.assertTrue(Statement.objects.filter(pk=self.st.pk).exists())
+        self.assertEqual(corr.versions_cible_examinees.get().texte, "texte initial")
+
+    def test_suppression_conserve_les_captures_du_statement_devenu_prive(self):
+        prive = Statement.objects.create(text="version examinée")
+        self.nc.object_id = prive.pk; self.nc.save(update_fields=['object_id'])
+        corr = self._confirmer()
+        ancien = corr.versions_cible_examinees.get()
+        svc.detacher_pour_edition(self.nc, "version au retrait")
+        resultat = svc.supprimer_occurrence(self.nc)
+        self.assertNotIn(prive.pk, resultat['statements_supprimes'])
+        self.assertEqual(VersionTexte.objects.get(pk=ancien.pk).texte, "version examinée")
+        self.assertEqual(NoeudArchive.objects.get(noeud_pk=self.nc.pk).texte,
+                         "version au retrait")
+        corr.refresh_from_db()
+        self.assertEqual(corr.etat, EtatConfirmation.CONFIRME)
+
+    def test_purge_directe_du_statement_examine_est_refusee(self):
+        prive = Statement.objects.create(text="version examinée")
+        self.nc.object_id = prive.pk; self.nc.save(update_fields=['object_id'])
+        corr = self._confirmer()
+        LibraryNode.objects.filter(pk=self.nc.pk).update(object_id=self.st.pk)
+        with refus_attendu(self, SuppressionRefusee):
+            prive.delete()
+        self.assertEqual(corr.versions_cible_examinees.get().texte, "version examinée")
+
+    def test_purge_directe_dune_capture_examinee_est_refusee(self):
+        corr = self._confirmer()
+        capture = corr.versions_cible_examinees.get()
+        with refus_attendu(self, SuppressionRefusee):
+            VersionTexte.objects.filter(pk=capture.pk).delete()
+        self.assertTrue(corr.versions_cible_examinees.filter(pk=capture.pk).exists())
+
+    def test_suppression_document_ne_detruit_pas_sa_concordance(self):
+        corr = self._confirmer()
+        from django.db.models.deletion import ProtectedError
+        with refus_attendu(self, (SuppressionRefusee, ProtectedError)):
+            self.cible.delete()
+        self.assertTrue(Correspondance.objects.filter(pk=corr.pk).exists())
+        self.assertTrue(LibraryNode.objects.filter(pk=self.nc.pk).exists())
+
+    def test_suppression_archive_liee_est_refusee(self):
+        corr = self._confirmer()
+        svc.supprimer_occurrence(self.nc)
+        archive = NoeudArchive.objects.get(noeud_pk=self.nc.pk)
+        with refus_attendu(self, SuppressionRefusee):
+            archive.delete()
+        self.assertEqual(corr.extremites.get(role=RoleExtremite.CIBLE).archive_id, archive.pk)
+
+    def test_echec_archivage_annule_tout_le_bloc_http(self):
+        from unittest.mock import patch
+        original = svc.archiver_noeud
+        enfant = ajouter(self.nc, self.cible, "a", "enfant")
+        corr = self._confirmer()
+        def panne(noeud, **kwargs):
+            resultat = original(noeud, **kwargs)
+            if noeud.pk == enfant.pk:
+                raise RuntimeError("panne d'archivage simulée")
+            return resultat
+        with patch('document_manager.concordance.archiver_noeud', side_effect=panne):
+            response = self._post("delete")
+        self.assertEqual(response.status_code, 500)
+        self.assertEqual(NoeudArchive.objects.count(), 0)
+        self.assertEqual(LibraryNode.objects.filter(pk__in=[self.nc.pk, enfant.pk]).count(), 2)
+        self.assertEqual(corr.extremites.get(role=RoleExtremite.CIBLE).noeud_id, self.nc.pk)
+
+    def test_refus_apres_detachement_annule_aussi_les_nouveaux_objets(self):
+        from unittest.mock import patch
+        original = LibraryNode.save
+        avant = (Statement.objects.count(), VersionTexte.objects.count())
+        def refus(noeud, *args, **kwargs):
+            if noeud.item == "REFUS_SIMULE":
+                raise ModificationRefusee("renommage refusé")
+            return original(noeud, *args, **kwargs)
+        with patch.object(LibraryNode, 'save', refus):
+            response = self._post("edit", item="REFUS_SIMULE", text="nouveau texte")
+        self.assertEqual(response.status_code, 403)
+        self.nc.refresh_from_db(); self.st.refresh_from_db()
+        self.assertEqual((self.nc.item, self.nc.object_id, self.st.text),
+                         ("1", self.st.pk, "texte initial"))
+        self.assertEqual(avant, (Statement.objects.count(), VersionTexte.objects.count()))
+
+    def test_un_identifiant_generique_ne_declenche_pas_la_purge_dun_statement(self):
+        from events.models import Event
+        orphelin = Statement.objects.create(text="sans rapport avec le bloc")
+        event = Event.objects.create(pk=orphelin.pk, date="2015-01-01", explanation="autre type")
+        self.rc.add_child(document=self.cible,
+                          content_type=ContentType.objects.get_for_model(Event), object_id=event.pk)
+        svc.supprimer_occurrence(self.rc)
+        self.assertTrue(Statement.objects.filter(pk=orphelin.pk).exists())
+        self.assertTrue(Event.objects.filter(pk=event.pk).exists())
+
+    def test_suppression_document_archive_ne_detruit_pas_sa_concordance(self):
+        corr = self._confirmer()
+        svc.supprimer_occurrence(self.nc)
+        with refus_attendu(self, SuppressionRefusee):
+            self.cible.delete()
+        self.assertTrue(Correspondance.objects.filter(pk=corr.pk).exists())
+        self.assertTrue(NoeudArchive.objects.filter(noeud_pk=self.nc.pk).exists())
+
+    def test_ecriture_orm_directe_dun_statement_partage_est_refusee(self):
+        with refus_attendu(self, ModificationRefusee):
+            self.st.text = "écriture sans occurrence"
+            self.st.save(update_fields=['text'])
+        self.st.refresh_from_db()
+        self.assertEqual(self.st.text, "texte initial")
+        self.assertEqual(self.ns.content_object.text, "texte initial")
+
+    def test_changer_le_document_dun_noeud_historique_ne_contourne_pas_la_garde(self):
+        ReferentHistorique.objects.create(document=self.source, libelle="référent")
+        with refus_attendu(self, ModificationRefusee):
+            self.ns.document = self.cible
+            self.ns.save(update_fields=['document'])
+        self.ns.refresh_from_db()
+        self.assertEqual(self.ns.document_id, self.source.pk)
diff --git a/document_manager/views/produced_views.py b/document_manager/views/produced_views.py
index 01933c032ec414a774e62dc468872c54ee707a2d..e3198a29d358228e381add94ddbf8693f68efb8e 100644
--- a/document_manager/views/produced_views.py
+++ b/document_manager/views/produced_views.py
@@ -7,7 +7,8 @@ from collections import defaultdict
 from datetime import date
 
 from ..models import Document, Statement, LibraryNode, DocumentSource
-from .. import numerotation
+from .. import concordance, numerotation
+from ..protection import ModificationRefusee, SuppressionRefusee, est_referent, est_reproduit
 from ..forms.manual_forms import ProducedDocumentForm, NodeForm, LibraryNodeCreateForm
 from argument_manager.models import TrameNarrative
 from pdf_manager.models import Quote as PDFQuote
@@ -233,15 +234,19 @@ def ajax_edit_node(request, node_pk):
         form = NodeForm(request.POST)
         if form.is_valid():
             data = form.cleaned_data
-            node_to_edit.item = data['item']
-            node_to_edit.save()
-            if node_to_edit.content_object and hasattr(node_to_edit.content_object, 'text'):
-                node_to_edit.content_object.text = data['text']
-                node_to_edit.content_object.save()
+            if est_reproduit(node_to_edit.document) or est_referent(node_to_edit.document_id):
+                raise ModificationRefusee("Une occurrence reproduite ou historique ne se réécrit pas.")
+            obj = node_to_edit.content_object
+            if isinstance(obj, Statement):
+                concordance.detacher_pour_edition(node_to_edit, data['text'])
+            elif node_to_edit.content_type_id is None and node_to_edit.object_id is None:
+                node_to_edit.content_object = Statement.objects.create(
+                    text=data['text'], is_user_created=True)
+                node_to_edit.save(update_fields=['content_type', 'object_id'])
             else:
-                new_statement = Statement.objects.create(text=data['text'], is_user_created=True)
-                node_to_edit.content_object = new_statement
-                node_to_edit.save()
+                raise ModificationRefusee("Cette occurrence ne porte pas un Statement rédactionnel.")
+            node_to_edit.item = data['item']
+            node_to_edit.save(update_fields=['item'])
             return JsonResponse({'status': 'success', 'message': 'Node updated.'})
         else:
             return JsonResponse({'status': 'error', 'message': 'Form is invalid', 'errors': form.errors.as_json()}, status=400)
@@ -256,21 +261,10 @@ def ajax_delete_node(request, node_pk):
     try:
         node_to_delete = get_object_or_404(LibraryNode, pk=node_pk)
         
-        content_objects_to_consider = {}
-        for node in [node_to_delete] + list(node_to_delete.get_descendants()):
-            if node.content_object:
-                key = (node.content_type_id, node.object_id)
-                if key not in content_objects_to_consider:
-                    content_objects_to_consider[key] = node.content_object
-        
-        node_to_delete.delete()
+        concordance.supprimer_occurrence(node_to_delete, motif="retrait décidé dans l'éditeur")
 
-        statement_content_type = ContentType.objects.get_for_model(Statement)
-        for (ct_id, obj_id), content_obj in content_objects_to_consider.items():
-            if ct_id == statement_content_type.id and isinstance(content_obj, Statement) and content_obj.is_user_created:
-                if not LibraryNode.objects.filter(content_type=statement_content_type, object_id=content_obj.pk).exists():
-                    content_obj.delete()
-            
         return JsonResponse({'status': 'success', 'message': f"Node '{node_to_delete.item}' and its descendants deleted successfully."})
+    except (SuppressionRefusee, ModificationRefusee) as e:
+        return JsonResponse({'status': 'error', 'message': str(e)}, status=403)
     except Exception as e:
         return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
```
