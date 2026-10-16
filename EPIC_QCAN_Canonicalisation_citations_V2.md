*Canonicalisation des citations avant rattachement à la version 2*

**Document de travail — version 1.0 — 14 octobre 2026**

| **Mode de maintenance** | Modifier uniquement la section ou la User Story visée; conserver les identifiants Q01–Q08.                |
|-------------------------|-----------------------------------------------------------------------------------------------------------|
| **Validation**          | Une Story = un commit/push = un verdict PASS, FAIL ou BLOQUÉ avant la suivante.                           |
| **Autorité probatoire** | La source originale fait autorité; l’OCR et la normalisation servent à détecter/localiser, pas à décider. |
| **Précondition V2**     | Aucune sous-cote de précision ne doit être attribuée avant le PASS de Q07.                                |

# Journal des versions

| **Version** | **Date**   | **Portée**                                                                                     | **État**        |
|-------------|------------|------------------------------------------------------------------------------------------------|-----------------|
| 1.0         | 2026-10-14 | Epic corrigé : prévention, MERGE/SPLIT/KEEP_DISTINCT, vérification source, GenericFK, pont V2. | Base de travail |

# 1. Objectif

Le système contient des citations extraites de documents de preuve. Plusieurs citations provenant d’une même source peuvent actuellement représenter :

- exactement le même passage;

- le même passage avec des variantes typographiques;

- le même passage avec une différence provenant de l’OCR ou d’une retranscription;

- des passages dont les bornes diffèrent;

- un passage contenu dans un autre;

- deux passages qui se chevauchent partiellement.

Le problème n’est donc pas seulement celui de doublons textuels. Le système doit distinguer :

1.  les variantes d’un même passage, qui peuvent être fusionnées;

2.  les découpages différents, qui doivent être examinés et, lorsque nécessaire, redécoupés;

3.  les passages distincts légitimes, même lorsqu’ils se chevauchent.

L’objectif de l’Epic est d’obtenir, avant tout rattachement des citations à la version 2, un corpus de citations dont chaque groupe problématique a fait l’objet d’une décision explicite et dont toutes les références sont cohérentes.

Paragraphe V2

│

▼

Confirmation d’appui

│

▼

Ligne de précision du bordereau

P-98.1

│

▼

Citation canonique

│

▼

Document source

# 2. État de référence

Les mesures de départ devront être reprises dans le dépôt et devenir reproductibles.

EmailQuote : 268

PDFQuote : 126

Total : 394

Citations appartenant à un groupe problématique : 95

Paires détectées dans une même source : 62

Il n’existe que deux modèles de citation concernés :

email_manager.Quote

pdf_manager.Quote

Les autres types de preuve ne créent pas de Quote :

- clavardage → ChatSequence;

- photos;

- événements;

- vidéos.

Ces nombres constituent l’état de référence, mais ne doivent jamais être codés en dur dans les tests. Un outil de mesure doit permettre de les recalculer.

# 3. Principes gouvernants

## 3.1 Une citation appartient toujours à une source

Une citation n’est jamais identifiée indépendamment de son document.

EmailQuote → Email

PDFQuote → PDFDocument

Deux citations textuellement identiques provenant de deux sources différentes ne sont jamais des doublons au sens de cet Epic.

## 3.2 La source fait autorité

La « bonne version » d’une citation n’est pas celle qui paraît la mieux écrite. Elle est celle qui reproduit fidèlement la source.

source : « je n'ai jamais traiter... »

quote A : « je n'ai jamais traité... »

quote B : « je n'ai jamais traiter... »

La citation fidèle est B, même si A corrige grammaticalement le texte.

### Courriels

Le contenu original du courriel constitue la référence.

### PDF

Lorsque le PDF est un scan, la transcription/OCR sert à rechercher, localiser et proposer des rapprochements. Elle ne constitue pas nécessairement l’autorité finale. Si l’OCR est ambigu, le scan doit être vérifié.

# 4. Les trois décisions possibles

Une relation détectée entre deux citations ne conduit pas automatiquement à une fusion. Chaque groupe examiné doit aboutir à une des décisions suivantes.

## MERGE

Les citations représentent réellement le même passage. Une citation devient canonique et les autres sont absorbées.

- différence d’apostrophe;

- espaces;

- différence purement OCR;

- transcription erronée d’une des variantes;

- variation sans différence de portée.

## SPLIT

Les citations ne diffèrent pas seulement par leur transcription : leurs bornes documentaires diffèrent.

A = phrase 1

B = phrase 1 + phrase 2

ou

A = fin phrase 1 + phrase 2

B = phrase 2 + début phrase 3

La solution n’est pas de choisir arbitrairement A ou B. Le passage doit être représenté conformément aux blocs probatoires nécessaires et les usages existants redistribués explicitement.

## KEEP_DISTINCT

Deux citations se chevauchent mais représentent légitimement deux passages différents. Elles demeurent distinctes.

# 5. Connecteurs discursifs

Les mots tels que les suivants ne sont pas considérés comme du bruit textuel :

Toutefois

Cependant

Mais

Donc

En revanche

Par conséquent

Ils peuvent porter une relation logique. Ils font donc partie de la citation lorsqu’ils sont compris dans le passage source sélectionné.

« Toutefois, X »

≠ automatiquement

« X »

Le cas doit être examiné et peut aboutir à MERGE, SPLIT ou KEEP_DISTINCT.

# 6. Invariant de découpage

Une citation représente un passage continu de la source. Le système ne doit pas créer artificiellement une citation composée de fragments non contigus.

Une citation existante qui contient plusieurs blocs probatoires indépendants peut devoir être remplacée par plusieurs citations atomiques. Aucun découpage ne doit modifier silencieusement la preuve qu’une trame, un fait ou un axe invoquait auparavant.

# 7. Prévention avant nettoyage

Le système doit empêcher autant que possible la création de nouveaux doublons. Le nettoyage du corpus existant ne sera considéré comme durable que si la création d’une nouvelle citation vérifie d’abord les citations existantes de la même source.

sélection d'un nouveau passage

↓

recherche de citations existantes qui recoupent ce passage

↓

aucune → créer

citation existante équivalente → proposer de la réutiliser

recouvrement ambigu → montrer les citations existantes

et laisser l'utilisateur décider

Le contrôle ne doit jamais empêcher la création volontaire de deux citations distinctes lorsque leurs bornes ou leur fonction probatoire diffèrent réellement.

# 8. Références à préserver

Une opération de fusion ou de découpage doit considérer tous les consommateurs d’une citation, pas seulement les relations que les cascades Django savent suivre.

TrameNarrative.citations_courriel

TrameNarrative.citations_pdf

RattachementAxe

AppuiFait

LibraryNode

ProducedExhibit

toute nouvelle GenericFK visant une Quote

Le détecteur dynamique déjà utilisé par les outils de purge doit être réutilisé ou extrait en service commun. Une opération destructive doit refuser de s’exécuter lorsqu’un consommateur inconnu est détecté.

# 9. Contraintes d’unicité

Le repointage naïf d’un object_id vers le winner est interdit sans analyse préalable.

Fait A → Quote 1

Fait A → Quote 2

si Quote 2 fusionne dans Quote 1 :

Fait A → Quote 1

Lors d’une collision, le service doit :

4.  conserver une seule relation;

5.  fusionner ou préserver les métadonnées pertinentes selon des règles explicites;

6.  ne jamais perdre silencieusement une note, un role, un ordre ou toute autre information distincte.

Si deux relations portent des métadonnées incompatibles qui ne peuvent être fusionnées automatiquement : STOP et décision humaine.

# 10. Sort des LibraryNode historiques

Les nœuds de citation actuellement présents dans les documents « Test » et « Affidavit » ne doivent pas être repointés automatiquement.

La décision retenue est de les supprimer, conformément au cadrage précédent, à condition qu’un nouvel audit confirme avant suppression que :

- ils appartiennent toujours uniquement à ces documents PRODUCED;

- aucun document REPRODUCED de valeur probatoire ne contient de nœud équivalent;

- aucune nouvelle dépendance ayant de la valeur ne s’y rattache.

Cette suppression est une opération explicite de nettoyage préalable. Elle ne doit jamais être un effet secondaire caché d’une fusion.

# 11. Lignes de précision du bordereau

Une ligne de précision du pont désignera une citation canonique.

P-98 → Email / PDFDocument

│

└── P-98.1 → Quote canonique

Invariant : la citation désignée par une ligne de précision doit provenir de la pièce désignée par sa ligne parente.

Une sous-cote attribuée à un passage destiné à une version notifiée constitue un référent durable. Par conséquent, aucune citation ne doit être reliée à la version 2 avant la fin du nettoyage et de la canonicalisation.

# 12. Protocole d’exécution par agent IA

L’Epic est exécuté une User Story à la fois.

1\. état du dépôt avant modification

2\. implémentation strictement limitée à la Story

3\. tests

4\. rapport

5\. commit

6\. push

7\. arrêt

L’agent ne commence pas la Story suivante.

US-Q01: prevent duplicate quote creation

US-Q02: audit quote consumers and remove obsolete nodes

...

Chaque Story produit :

docs/quote_canonicalization/reports/US-Qxx.md

et, lorsque pertinent :

docs/quote_canonicalization/reports/US-Qxx.json

# 13. Structure obligatoire des rapports

User Story

Commit SHA

État avant

Fichiers modifiés

Migrations

Tests ajoutés

Tests exécutés

Résultat exact

Mesures avant

Mesures après

Critère 1 : PASS/FAIL

Critère 2 : PASS/FAIL

...

Anomalies

Décisions manuelles nécessaires

VERDICT :

PASS

FAIL

ou

BLOQUÉ

Le rapport de l’agent n’est pas lui-même une preuve. La validation repose sur le code, le diff, les tests, les résultats reproductibles et l’état du dépôt.

# US-Q01 — Empêcher la création de nouveaux doublons

## User Story

> *En tant qu’utilisateur, je veux être averti lorsqu’un passage que je tente de créer comme citation recoupe une citation existante de la même source afin de pouvoir réutiliser celle-ci plutôt que créer inutilement un doublon.*

## Travail

Extraire ou réutiliser un service commun capable de comparer un passage proposé aux citations de la même source.

nouveau passage

↓

citations de la même source

↓

classification des recouvrements

Le système doit pouvoir signaler :

EXACT

EQUIVALENT_NORMALISE

CONTAINS

CONTAINED_BY

PARTIAL_OVERLAP

NONE

L’utilisateur doit pouvoir réutiliser une citation existante ou continuer volontairement la création. Aucune citation n’est fusionnée dans cette Story.

## Critères de succès

- seuls les passages provenant de la même source sont comparés;

- un doublon exact est détecté;

- les variantes normalisées sont signalées;

- les inclusions sont signalées;

- les chevauchements sont signalés;

- l’utilisateur peut réutiliser une citation existante;

- l’utilisateur peut créer volontairement une citation distincte;

- un connecteur discursif n’est pas supprimé par la normalisation;

- aucune modification n’est apportée aux citations existantes.

## Tests nécessaires

### T-Q01-01

Même source + texte identique → EXACT.

### T-Q01-02

Sources différentes + texte identique → aucun doublon proposé.

### T-Q01-03

Différences typographiques bénignes → rapprochement proposé.

### T-Q01-04

Citation courte contenue dans une longue → CONTAINED_BY.

### T-Q01-05

Chevauchement partiel → PARTIAL_OVERLAP.

### T-Q01-06

« Toutefois, X » et « X » ne doivent pas être transformés automatiquement en équivalence certaine.

### T-Q01-07

Réutilisation d’une citation existante n’en crée aucune nouvelle.

### T-Q01-08

Choix explicite « créer quand même » crée une nouvelle citation.

## Rapport attendu

quotes avant

quotes créées durant tests

doublons détectés

réutilisations

créations forcées

# US-Q02 — Établir la carte exhaustive des consommateurs et purger les LibraryNode obsolètes

## User Story

> *En tant que mainteneur, je veux connaître tous les objets qui utilisent une citation et retirer la dette historique explicitement déclarée jetable afin que les opérations futures puissent être exécutées sans références cachées.*

## Travail

### A. Extraire le détecteur de références

Réutiliser la logique du détecteur existant de purger_quotes.py. Le service doit découvrir dynamiquement les modèles possédant content_type/object_id et déterminer ceux qui visent des EmailQuote ou PDFQuote. Il doit également inventorier les M2M explicites.

### B. Identifier les consommateurs connus

TrameNarrative

RattachementAxe

AppuiFait

LibraryNode

ProducedExhibit

### C. Auditer les nœuds historiques

80 nœuds

uniquement documents PRODUCED Test / Affidavit

0 dans les documents REPRODUCED pertinents

### D. Suppression explicite

Seulement si cette hypothèse est confirmée. Créer sauvegarde/audit avant suppression.

## Critères de succès

- tous les consommateurs connus sont détectés;

- un consommateur GenericFK inconnu fait échouer le gate;

- l’audit des LibraryNode est reproductible;

- aucune suppression n’est faite si les hypothèses historiques ne sont plus vraies;

- les nœuds supprimés sont précisément identifiés;

- les documents source restent inchangés;

- aucune citation n’est supprimée.

## Tests nécessaires

### T-Q02-01

Détection d’une relation TrameNarrative.

### T-Q02-02

Détection d’un AppuiFait.

### T-Q02-03

Détection d’un RattachementAxe.

### T-Q02-04

Détection d’un LibraryNode.

### T-Q02-05

Détection d’un ProducedExhibit.

### T-Q02-06

Un modèle GenericFK inconnu provoque un blocage.

### T-Q02-07

La suppression ciblée des nœuds ne supprime pas leurs citations.

### T-Q02-08

Aucun nœud REPRODUCED n’est supprimé.

## Rapport attendu

consommateurs détectés

relations par type

LibraryNode avant

LibraryNode supprimés

LibraryNode après

GenericFK inconnues

dangling avant

dangling après

Condition de PASS : GenericFK inconnues = 0

# US-Q03 — Construire le moteur transactionnel de fusion

## User Story

> *En tant qu’utilisateur, je veux absorber les variantes vérifiées d’un même passage dans une citation canonique sans perdre aucun usage existant.*

## Précondition

La décision que les citations représentent le même passage a déjà été prise. Le moteur ne prend pas cette décision.

## Interface métier

merge_quotes(

winner=quote_a,

losers=\[quote_b, quote_c\],

apply=False,

)

## Règles

7.  vérifier même modèle;

8.  vérifier même source;

9.  inventorier tous les consommateurs;

10. détecter les collisions d’unicité;

11. transférer les relations;

12. dédupliquer les relations équivalentes;

13. refuser les collisions sémantiquement incompatibles;

14. écrire un journal;

15. supprimer les losers;

16. agir dans transaction.atomic().

## Le texte du winner

Le service ne choisit ni ne corrige le texte. Le winner doit avoir été préalablement validé contre la source.

## Journal

type

source

winner_pk

winner_text_snapshot

loser_pk

loser_text_snapshot

relations transférées

relations dédupliquées

conflits

date

## Critères de succès

- fusion inter-source impossible;

- fusion EmailQuote/PDFQuote impossible;

- union correcte des M2M;

- GenericFK repointées;

- collisions d’unicité gérées;

- aucune métadonnée différente n’est silencieusement écrasée;

- loser supprimé uniquement après transfert complet;

- transaction rollback intégral en cas d’erreur;

- porteur inconnu → opération refusée;

- winner conserve son PK;

- winner conserve son texte;

- log complet disponible.

## Tests nécessaires

### T-Q03-01

Fusion simple sans consommateur.

### T-Q03-02

Deux trames distinctes → union.

### T-Q03-03

Même trame des deux côtés → une relation.

### T-Q03-04

Même Fait des deux côtés → collision dédupliquée.

### T-Q03-05

Même Axe des deux côtés → collision dédupliquée.

### T-Q03-06

Relations portant des métadonnées compatibles → résultat déterministe.

### T-Q03-07

Métadonnées incompatibles → STOP sans modification.

### T-Q03-08

GenericFK transférée.

### T-Q03-09

Source différente → refus.

### T-Q03-10

Exception artificielle → rollback total.

### T-Q03-11

Journal complet.

## Rapport attendu

winner

losers

relations avant

relations transférées

relations dédupliquées

conflits

dangling après

Condition : références perdues = 0 ; dangling = 0

# US-Q04 — Construire le workbench de décision contre la source

## User Story

> *En tant qu’utilisateur, je veux voir chaque groupe problématique avec son texte source, ses bornes et ses usages afin de pouvoir décider s’il faut MERGE, SPLIT ou KEEP_DISTINCT.*

## Travail

Créer une interface ou une commande produisant, groupe par groupe :

source

citation A

citation B

positions

pages

texte stocké

texte trouvé dans la source

type de recouvrement

usages de chaque citation

Pour un courriel : afficher le contexte du body_plain_text.

Pour un PDF : afficher la transcription, fournir l’accès au PDF/scan pour vérification visuelle et signaler explicitement que l’OCR n’est pas nécessairement l’autorité.

## Décision enregistrée

MERGE

SPLIT

KEEP_DISTINCT

UNRESOLVED

Une décision doit être versionnable et auditable.

## Critères de succès

- les groupes sont regroupés par source;

- le contexte documentaire est visible;

- les usages de chaque variante sont visibles;

- le système ne choisit jamais automatiquement le winner;

- le PDF original peut être consulté pour les cas OCR;

- la décision est enregistrée séparément du résultat de détection;

- un groupe peut légitimement rester distinct.

## Tests nécessaires

### T-Q04-01

Groupe EXACT.

### T-Q04-02

Variante OCR.

### T-Q04-03

Inclusion.

### T-Q04-04

Chevauchement.

### T-Q04-05

Connecteur « Toutefois ».

### T-Q04-06

Citation non localisable.

### T-Q04-07

Décision MERGE.

### T-Q04-08

Décision SPLIT.

### T-Q04-09

Décision KEEP_DISTINCT.

### T-Q04-10

Changement de décision avant exécution.

## Rapport attendu

groupes détectés

groupes examinés

MERGE

SPLIT

KEEP_DISTINCT

UNRESOLVED

# US-Q05 — Exécuter les fusions validées contre les sources

## User Story

> *En tant qu’utilisateur, je veux appliquer uniquement les décisions MERGE que j’ai validées afin de supprimer les variantes réellement équivalentes.*

## Travail

MERGE → appel du moteur Q03

SPLIT → ignoré pour Q06

KEEP_DISTINCT → aucune écriture

UNRESOLVED → aucune écriture

Simulation obligatoire avant application.

## Critères de succès

- seules les décisions MERGE sont exécutées;

- chaque winner a été explicitement désigné;

- chaque fusion passe par Q03;

- aucune fusion n’est exécutée depuis une simple similarité;

- les autres catégories restent intactes;

- toutes les opérations produisent un journal;

- aucune référence orpheline.

## Tests nécessaires

### T-Q05-01

Décision MERGE exécutée.

### T-Q05-02

KEEP_DISTINCT ignoré.

### T-Q05-03

SPLIT ignoré.

### T-Q05-04

UNRESOLVED bloque une exécution globale si le mode exige une résolution complète.

### T-Q05-05

Simulation sans écriture.

### T-Q05-06

Batch rollback selon stratégie documentée.

## Rapport attendu

EmailQuote avant/après

PDFQuote avant/après

groupes MERGE

losers supprimés

relations transférées

relations dédupliquées

dangling

# US-Q06 — Construire et appliquer l’opération SPLIT

## User Story

> *En tant qu’utilisateur, je veux redécouper les citations dont les bornes étaient inadéquates sans élargir ni réduire silencieusement ce que leurs consommateurs invoquent.*

## Principe

Quote A = ABC

Quote B = BCDE

Une fusion n’est pas correcte.

Le système peut nécessiter :

Quote X = AB

Quote Y = C

Quote Z = DE

Le découpage n’est jamais déduit uniquement par l’algorithme.

## Travail

17. créer les nouvelles citations canoniques déterminées;

18. vérifier leur fidélité/source;

19. montrer tous les consommateurs de chaque ancienne citation;

20. exiger une destination explicite pour chaque consommateur;

21. transférer les relations;

22. supprimer les anciennes citations seulement lorsqu’elles ne sont plus utilisées;

23. conserver un journal complet.

## Règle centrale

Aucun consommateur ne doit recevoir automatiquement toutes les nouvelles citations. Chaque usage doit être assigné explicitement.

Trame T1 → ancienne citation longue

ne devient pas automatiquement :

T1 → fragment A

T1 → fragment B

T1 → fragment C

## Critères de succès

- les nouvelles citations sont des passages continus;

- chaque consommateur historique est comptabilisé;

- chaque consommateur reçoit une destination explicite;

- aucun usage n’est élargi implicitement;

- aucun usage n’est perdu;

- anciennes citations supprimées seulement lorsque leur remplacement est complet;

- opération transactionnelle;

- audit complet.

## Tests nécessaires

### T-Q06-01

Inclusion simple.

### T-Q06-02

Chevauchement partiel.

### T-Q06-03

Deux consommateurs d’une ancienne citation envoyés vers deux nouvelles citations différentes.

### T-Q06-04

Consommateur sans destination → application refusée.

### T-Q06-05

Nouvelle citation non continue → refus.

### T-Q06-06

Rollback en cours d’opération.

### T-Q06-07

Journal permettant de reconstruire ancienne quote → nouvelles quotes → redistribution des usages.

## Rapport attendu

groupes SPLIT

anciennes citations

nouvelles citations

consommateurs redistribués

consommateurs non résolus

références perdues

dangling

Conditions : consommateurs non résolus = 0 ; références perdues = 0 ; dangling = 0

# US-Q07 — Auditer et geler le corpus canonique

## User Story

> *En tant que mainteneur, je veux démontrer que tous les groupes détectés ont reçu une décision et que le corpus peut désormais servir de référentiel stable à la version 2.*

## Travail

Relancer l’analyse complète. Chaque groupe détecté doit être dans un état explicite :

MERGED

SPLIT_RESOLVED

KEEP_DISTINCT

Aucun groupe ne doit simplement disparaître du rapport sans explication.

## Audit d’intégrité

Quote avec parent valide

GenericFK dangling

M2M dangling

AppuiFait incohérent

RattachementAxe incohérent

ProducedExhibit dangling

LibraryNode dangling

journaux incomplets

groupes UNRESOLVED

Le succès n’est PAS « 0 chevauchement ». Le succès est « 0 groupe sans décision ». Un groupe KEEP_DISTINCT est résolu.

## Critères de succès

- ERROR = 0

- UNRESOLVED = 0

- les recouvrements légitimes KEEP_DISTINCT peuvent subsister.

## Tests nécessaires

### T-Q07-01

Corruption volontaire GenericFK → audit FAIL.

### T-Q07-02

Groupe sans décision → audit FAIL.

### T-Q07-03

KEEP_DISTINCT → audit PASS.

### T-Q07-04

Quote sans parent → audit FAIL.

### T-Q07-05

Journal MERGE incohérent → audit FAIL.

### T-Q07-06

Journal SPLIT incohérent → audit FAIL.

## Rapport attendu

Q07_before.json

Q07_after.json

Q07_FINAL_CORPUS.md

quotes initiales

quotes finales

MERGE

SPLIT

KEEP_DISTINCT

ERROR

WARNING

UNRESOLVED

Gate : ERROR = 0 ; UNRESOLVED = 0

# US-Q08 — Relier les citations canoniques à la version 2 par les lignes de précision

## User Story

> *En tant que rédacteur, je veux rattacher les paragraphes de la version 2 aux passages précis qu’ils invoquent en donnant à ces passages des sous-cotes stables du pont.*

## Précondition absolue

Q07 doit être PASS. Aucune sous-cote de précision ne doit être attribuée avant ce gate.

## Architecture

Ne pas créer une nouvelle architecture parallèle de type ParagraphEvidenceLink. Réutiliser la structure existante.

Statement / paragraphe V2

│

▼

ConfirmationAppui

│

▼

Bordereau précision P-X.Y

│

▼

Quote canonique

│

▼

source

## Ligne parente

P-98 → Email 21

P-98.1 → EmailQuote 31

## Invariant de provenance

parent(P-98.1).content_object

==

source(P-98.1.quote)

selon les règles documentaires applicables. Une quote d’un autre document ne peut jamais recevoir une sous-cote sous P-98.

## Permanence

Une fois une ligne de précision utilisée dans un acte notifié, son association est considérée comme figée. Une fusion ultérieure impliquant cette citation doit être interdite ou passer par un mécanisme explicite destiné aux actes déjà notifiés, hors périmètre de cet Epic.

## Critères de succès

- ligne de précision → Quote autorisé;

- cohérence parent/source vérifiée;

- paragraphes V2 peuvent désigner ces lignes;

- plusieurs paragraphes peuvent utiliser la même précision;

- un paragraphe peut utiliser plusieurs précisions;

- aucune quote non canonique/non résolue n’est admissible;

- une quote appartenant à une autre source est refusée;

- les sous-cotes sont stables.

## Tests nécessaires

### T-Q08-01

P-98.1 → EmailQuote appartenant à P-98 → PASS.

### T-Q08-02

P-98.1 → EmailQuote d’un autre Email → FAIL.

### T-Q08-03

P-42.1 → PDFQuote appartenant au PDF parent → PASS.

### T-Q08-04

Citation appartenant à un groupe UNRESOLVED → refus.

### T-Q08-05

Deux paragraphes peuvent employer P-98.1.

### T-Q08-06

Un paragraphe peut employer P-98.1 et P-72.2.

### T-Q08-07

Une sous-cote déjà figée ne change pas de Quote silencieusement.

## Rapport attendu

Pour chaque paragraphe V2 :

§

Statement

Confirmation

Sous-cote

Quote

Document source

Anomalies :

paragraphe sans appui

appui sans précision lorsque précision attendue

précision sans quote

quote/source incompatible

quote non canonique

# 14. Ordre impératif

Q01 — empêcher les nouveaux doublons

↓

Q02 — cartographier les consommateurs et supprimer la dette LibraryNode

↓

Q03 — moteur de fusion

↓

Q04 — workbench de vérification humaine

↓

Q05 — appliquer MERGE

↓

Q06 — appliquer SPLIT

↓

Q07 — audit et gel du corpus

↓

Q08 — raccordement à la version 2

Aucune Story ne peut être commencée avant validation de la précédente.

# 15. Validation après chaque push

Après chaque Story, le validateur examine :

24. SHA du commit;

25. diff depuis le dernier commit accepté;

26. fichiers modifiés;

27. respect du périmètre;

28. tests exigés;

29. contenu réel des tests;

30. résultats;

31. migrations;

32. rapport;

33. critères d’acceptation.

PASS

Story suivante autorisée.

FAIL

Même Story à corriger.

BLOQUÉ

La démonstration est impossible avec l’environnement actuel.

La Story suivante ne commence pas.

# 16. Tests de régression obligatoires

Toute Story qui modifie le moteur de références ou de fusion doit exécuter au minimum les tests des applications touchées. Au gate Q07 :

python manage.py test email_manager

python manage.py test pdf_manager

python manage.py test argument_manager

python manage.py test document_manager

python manage.py test case_manager

python manage.py check

python manage.py makemigrations --check --dry-run

Les commandes exactes peuvent être adaptées à l’organisation réelle des tests, mais le rapport doit fournir les commandes réellement exécutées.

# 17. Interdictions

- fusionner automatiquement deux citations sur la seule base d’un embedding;

- choisir la citation la mieux écrite plutôt que la plus fidèle;

- considérer l’OCR comme autorité lorsque le scan le contredit;

- supprimer les connecteurs discursifs pour créer une équivalence;

- fusionner des citations provenant de sources différentes;

- traiter une inclusion comme un doublon;

- transférer automatiquement toutes les nouvelles citations d’un SPLIT à tous les anciens consommateurs;

- écraser silencieusement les métadonnées de deux relations entrant en collision;

- ignorer un nouveau porteur GenericFK;

- créer les sous-cotes de la V2 avant Q07;

- modifier une sous-cote déjà figée par un acte notifié;

- créer une architecture paragraphe-preuve parallèle alors que la structure du pont existe déjà.

# 18. Définition de terminé

## Prévention

Une nouvelle citation ne peut plus être créée sans vérification préalable des passages déjà extraits de la même source.

## Corpus existant

Chaque groupe problématique détecté possède une décision explicite MERGE, SPLIT ou KEEP_DISTINCT, et aucun groupe ne demeure UNRESOLVED.

## Fidélité

Toute citation canonique retenue a été vérifiée contre sa source appropriée.

## Intégrité

références perdues = 0

dangling references = 0

consommateurs inconnus = 0

erreurs d’intégrité = 0

## Version 2

ligne de précision

↓

citation canonique

↓

source

et, inversement :

paragraphe

→ confirmation

→ sous-cote

→ citation

→ document

## Critère final

> *Le succès de l’Epic n’est pas qu’il n’existe plus de citations qui se chevauchent. Le succès est que chaque recouvrement connu a été qualifié; les variantes du même passage ont été fusionnées, les découpages inadéquats ont été résolus sans modifier silencieusement leurs usages, les passages légitimement distincts sont explicitement conservés, aucune référence n’a été perdue et seules les citations ainsi stabilisées peuvent recevoir une sous-cote et soutenir la version 2.*
