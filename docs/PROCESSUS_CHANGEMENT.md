# Processus de changement du système

**Établi le 20 octobre 2026; révisé C-UML-2026-10-20-R1 sur mandat utilisateur explicite.** Ce document régit la façon dont une modification
de l'application est décidée, exécutée et intégrée. Il ne tranche aucune
décision d'architecture et n'autorise aucun lot : il dit où les décisions
s'écrivent et à quelles conditions un changement entre dans le système.

Pendant du `legal/METHODOLOGIE_POST_DEPOT.md`, pour le code.

**Révision explicite :** le [mandat UML](architecture_c/references/MANDAT_CONSOLIDATION_UML_2026-10-20.md) remplace l’ancienne sélection conditionnelle des diagrammes, notamment « Classe : jamais ». Il impose activité, séquence, ERD cible et classes pour chaque use case, avec validation B puis approbation utilisateur. Le lot reste l’unité de livraison et les conditions d’atterrissage restent applicables. L’[état antérieur exact](architecture_c/historique/2026-10-20_avant_consolidation/README.md) est conservé comme historique. Aucun lot n’est autorisé par cette révision.

## 1. La règle qui tient tout le reste

**Une question a un seul fichier, et ce fichier est dans le dépôt.**

Un document qui fait autorité n'existe pas s'il est hors du dépôt. Les
répertoires `/tmp` et `/private/tmp` sont purgés par le système : un registre
de décisions qui y réside est une décision perdue à brève échéance. Un rapport
posé à la racine du dépôt en trois révisions successives n'est pas une autorité
non plus, car plus rien n'indique laquelle est vraie.

Conséquences pratiques :

- une copie de travail isolée (worktree, base jetable) est un **lieu
  d'exécution**, jamais un lieu de conservation;
- tout artefact qui doit survivre à la session est copié dans `docs/` **avant**
  la fin de cette session;
- une révision remplace le fichier qu'elle révise; elle ne s'ajoute pas à côté.

## 2. L'unité de changement est le lot

Pas le commit, pas la user story, pas la session de travail : le **lot**, tel
que défini au § 7.1 de
[`architecture_c/DECISIONS_ARCHITECTURE_C_CONSOLIDEES.md`](architecture_c/DECISIONS_ARCHITECTURE_C_CONSOLIDEES.md).

Un lot a un nom (`C0-A`, `L1-A`, …), un répertoire
`docs/architecture_c/lots/<LOT>/`, des préalables, des critères d'acceptation
et des tests affectés. Une user story décrit ce que l'utilisateur obtient;
elle ne constitue pas une unité de livraison.

**Un lot non atterri (étape 7) bloque le lot suivant.** C'est la règle qui
empêche l'accumulation de travail non intégré.

## 3. Les sept étapes

| # | Étape | Question tranchée | Sortie | Emplacement |
|---|---|---|---|---|
| 0 | **Socle** | De quel système parle-t-on exactement ? | ERD extrait du code, à un SHA nommé | `modele_preuve/diagrammes/erd_etat_actuel/` |
| 1 | **Décision** | Qu'est-ce qui est arrêté, en arbitrage, conditionnel ? | registre D / CF, un statut par décision | `architecture_c/DECISIONS_…md` |
| 2 | **Cible** | Que doit pouvoir faire l'utilisateur, et à quels critères ? | user story + critères d'acceptation | `modele_preuve/diagrammes/user_stories_architecture_c/` |
| 3 | **Conception et contrôle UML** | Les comportements, interactions, données et responsabilités sont-ils cohérents et approuvés ? | quatre vues par use case, validation B et approbation utilisateur (§ 4) | `architecture_c/use_cases/<UC-ID>/` |
| 4 | **Mandat** | Qu'ai-je le droit de toucher, et qu'est-ce qui est interdit ? | périmètre écrit **avant** la première ligne de code | `architecture_c/lots/<LOT>/MANDAT.md` |
| 5 | **Exécution** | — | branche dédiée, base jetable, aucune ressource réelle | worktree isolé |
| 6 | **Rapport** | Qu'est-ce qui est démontré, qu'est-ce qui reste ouvert ? | diff + résultats de tests + limites subsistantes | `architecture_c/lots/<LOT>/` |
| 7 | **Atterrissage** | Est-ce dans le système ? | commits fusionnés, socle régénéré | branche d'intégration, puis `main` |

**Aucune étape ne tranche une question appartenant à une étape antérieure.**
Si l'exécution révèle qu'une décision est fausse, on remonte à l'étape 1 et on
récrit la décision : on ne la corrige pas discrètement dans le code. C'est la
seule protection contre une architecture qui dérive sans que son registre le
sache.

Le mandat de l'étape 4 est la pièce la plus utile du dispositif. Sa forme
éprouvée est celle du § 10.5 du registre : liste des fichiers modifiables,
liste des interdictions explicites, SHA de départ, nature des données de test.
Un mandat qui ne contient pas d'interdictions n'est pas un mandat.

## 4. Porte UML obligatoire avant implantation

Le [protocole de validation UML](architecture_c/PROTOCOLE_VALIDATION_UML.md) fait autorité pour les dossiers de conception. **Chaque use case touché doit disposer des quatre vues PlantUML suivantes avant implantation :**

| Vue obligatoire | Objet du contrôle |
|---|---|
| Activité | Déclencheur, préconditions, acteurs, nominal, variantes, refus, erreurs et postconditions |
| Séquence | Interfaces, services, données, validations, transactions et stockage, avec chemins d’échec |
| ERD cible | Entités persistantes, clés, cardinalités, contraintes, suppression, versionnement; existant/proposé/à modifier distingués |
| Classes | Responsabilités, opérations, interfaces, héritage/dépendances et invariants; modèles Django et composants sans table distingués |

L’ERD **observé** est extrait du code à un SHA nommé. L’ERD **cible** est une conception, nécessairement dessinée avant l’implantation puis confrontée au schéma livré. Les deux ne sont pas confondus. Le diagramme de classes ne se réduit pas à l’ERD des modèles Django.

Pour chaque vue : conserver la source `.puml`, compiler, produire le SVG, vérifier visuellement la lisibilité et contrôler liens/inclusions. Les PNG sont également conservés lorsqu’ils sont produits. Les diagrammes d’états complètent les cycles de vie; ils ne remplacent aucune des quatre vues. Une vue générale de l’existant n’est pas une vue cible contextualisée du use case.

La porte est cumulative : spécification → quatre vues → revue technique/fonctionnelle/architecturale B → approbation utilisateur de la version précise → dépendances satisfaites et mandat de lot écrit. Un diagramme compilé, une ancienne activité, une approbation de principe ou un succès de tests isolé ne passe pas cette porte.

Le [plan](architecture_c/PLAN_MODELISATION_UML.md) décrit l’ordre de conception; le [registre](architecture_c/registre_validation.md) porte les statuts courants. Le lot non atterri bloque toujours l’exécution du suivant; la rédaction de dossiers peut avancer sans modifier le système.

Régénération, depuis le dossier du use case :

```sh
plantuml -charset UTF-8 -checkonly '*.puml'
plantuml -charset UTF-8 -tsvg '*.puml'
plantuml -charset UTF-8 -tpng '*.puml'
```

Socle observé, depuis la racine, seulement dans un mandat documentaire adapté :

```sh
python docs/modele_preuve/diagrammes/erd_etat_actuel/generer_erd.py --date AAAA-MM-JJ
```

Cette commande ne fournit pas à elle seule l’ERD de la cible future. Aucun de ces exemples n’autorise une intervention sur la base réelle.

## 5. L'étape 7 — définition de « fait »

C'est l'étape absente jusqu'ici, et la cause directe du risque que le système
ne voie jamais le jour. Un lot est **fait** quand les six conditions suivantes
sont vraies, et pas avant :

1. le rapport d'exécution est dans `docs/architecture_c/lots/<LOT>/`;
2. les tests affectés au lot passent sur le socle principal autorisé et une
   base de test dédiée, pas seulement sur la copie isolée; cela ne demande
   jamais implicitement un accès à la base réelle;
3. le diff est fusionné dans une branche d'intégration, puis dans `main`;
4. l'ERD est régénéré si le schéma a changé, et le nouveau SHA est inscrit;
5. les limites subsistantes sont réaffectées nommément à un lot ultérieur;
6. le journal du § 6 est mis à jour.

Un résultat de tests obtenu sur une copie isolée **n'est pas** une intégration.
Un patch conservé hors du dépôt **n'est pas** une livraison. Tant que ces six
conditions ne sont pas réunies, le lot suivant n'est pas ouvert.

## 6. Journal des lots

Une ligne par lot, mise à jour à l'étape 7. C'est le seul endroit où lire
l'avancement réel.

| Lot | Mandat | Exécution | Rapport | Atterri | Note |
|---|---|---|---|---|---|
| C0-A | § 10.5 du registre | 19 oct. 2026, copie isolée au SHA `212a7fe` | [RAPPORT](architecture_c/lots/C0-A/RAPPORT_EXECUTION_C0A.md), 209 tests dont 31 nouveaux | **non** | diff conservé en `C0A_DIFF_COMPLET.patch`, revue et fusion à mandater |
| L1-A | à rédiger | — | — | non | préalable : C0-A atterri |

## 7. Ce que ce processus ne décide pas

Il ne tranche pas D05, ne lève pas les conditions D07 et CF4, n'autorise aucun
lot et ne modifie aucune décision du registre. Il ne vaut pas non plus pour le
répertoire `legal/`, régi par `legal/METHODOLOGIE_POST_DEPOT.md` et par le gel
du dépôt du 24 juillet 2026.
