# Rapport de consolidation C et de préparation du contrôle UML

**C-UML-2026-10-20-R1 — Livrable E — 20 octobre 2026.**

## 1. Résultat et portée

L’architecture C est conservée et complétée avec les exigences de rédaction V2. **D05 CHRONO_VERSION est intégrée comme décision utilisateur acquise pour le principe.** Les modalités non décidées restent identifiées; aucune nouvelle fonctionnalité n’est implantée.

Le contrôle préalable impose désormais quatre vues PlantUML par use case : activité, séquence, ERD cible et classes. Validation B et approbation utilisateur sont distinctes. Le lot reste l’unité de livraison; un dossier de use case n’autorise pas le lot suivant ni un déploiement.

La présente intervention est celle d’impact, intégration des décisions et planification. Elle ne prétend pas avoir produit ou validé tous les nouveaux diagrammes détaillés.

## 2. Livrables et autorité documentaire

| Livrable | Document actif | Contenu |
|---|---|---|
| A | [Avenant architectural](AVENANT_ARCHITECTURE_C.md) | D05, identités et compositions, déduplication, concordance documentaire, production/gel et réserves R01–R08 |
| B | [Matrice de couverture](MATRICE_COUVERTURE_V2_C.md) | 8 invariants, 91 critères, 14 scénarios V2, compatibilité/préalables; scénarios négatifs complémentaires |
| C | [Plan de modélisation](PLAN_MODELISATION_UML.md) | 22 use cases, activités disponibles, vues manquantes, dépendances, ordre et quatre stories complémentaires |
| D | [Protocole obligatoire](PROTOCOLE_VALIDATION_UML.md) | Dossiers à quatre vues, contrôles T/F/A, approbation, transitions et conformité après implantation |
| E | Présent rapport | Références observées, impacts, risques, limites et premier passage proposé |

Compléments : [registre courant des dossiers](registre_validation.md), [gabarit](use_cases/MODELE_DOSSIER.md), [sources reçues](references/README.md) et [historique explicite](historique/2026-10-20_avant_consolidation/README.md). Le registre D/CF actif est révisé sur place; son ancien état exact est conservé, sans deuxième registre actif.

## 3. Références Git effectivement vérifiées

Vérification en lecture seule du 20 octobre : objets et références locaux, comparaison de leurs arbres, puis `git ls-remote --heads origin`. La lecture distante a réussi après relance hors bac à sable de la commande de lecture, la première tentative ayant échoué sur DNS. Aucun fetch, checkout, changement de référence, commit, push ou fusion n’est exécuté.

| Référence | SHA constaté | Interprétation |
|---|---|---|
| HEAD local / `epic/E01-numerotation-concordance` | `212a7feee81aef46a5b43d36e8eeafe0f8870064` | Socle P6 courant de cet arbre, pas la preuve de l’état de la base réelle |
| `integration/quote-regime-step1`, local et tête distante annoncée | `212a7feee81aef46a5b43d36e8eeafe0f8870064` | Cible protégée conservée |
| `main` distant annoncé / cache `origin/main` | `34bc98ac9132b1fee12b0946a8a93b19a5a1d702` | Référence de V2, distincte de P6 |
| `main` local | `5cf86341dd41c0047c1aa05aa136ef4cb6dcef37` | Référence locale plus ancienne; ne pas l’assimiler au main distant |
| `epic/E01-numerotation-concordance` distant annoncé | `14f7533650d2a28832698b2222ced1df1cd89bb1` | La branche locale P6 est en avance; ne pas annoncer son intégration dans main |
| `docs/diagrammes-c-et-erd-20261020` distant annoncé | `30ce0acb92522460c5a3f73019070dd0e7e2353c` | Référence documentaire demandée, parent P6; 90 fichiers modifiés/ajoutés, code applicatif inchangé |
| `docs/agent-b-pont-probatoire-20261019`, local et distant annoncé | `06fe44c1a7e8582792f9d1fcfcba8155046168ee` | Premier addendum de conception |
| `feat/quote-regime-step1` local | `11214d1e83a5558be3adae7f793501263a3d57ce` | Travail étape 1 intégré au socle P6 |
| `feat/quote-regime-step2` local | `b695e4683ed68bbc82e50cd68f712b3d5c5206d5` | Étape 2 accessible localement; pas de tête distante de même nom annoncée au relevé |

L’objet `30ce0ac` n’est pas dans la base d’objets du dépôt principal; il a été inspecté dans la copie de publication indépendante qui le possède. Cette lecture a vérifié son parent P6 et son diff documentaire, sans l’importer ni modifier les références du dépôt principal. La référence et les conclusions utiles sont conservées ici; cette copie n’est pas un lieu d’autorité documentaire.

### 3.1 Main comparé à P6

Ancêtre commun : `7b260819e56686b773a56f2abea7fd0355392952`. La comparaison `git rev-list --left-right --count 34bc98ac9132b1...212a7feee81a` donne un commit propre au premier et 26 propres à P6.

L’ERD P6 ne peut pas être présenté comme l’ERD du main examiné. Celui-ci ne contient notamment pas les structures Cause/EtatCause/LienCause, ReferentHistorique/Instantanes/VersionTexte, Correspondance/ExtremiteCorrespondance/NoeudArchive, ConfirmationAppui/AncrageCitation, les champs de numérotation E01 et les champs de régime de l’étape 1. Le rapprochement avant intégration doit préserver ces acquis; il n’est pas exécuté dans ce mandat.

### 3.2 Évolution PHRASE réellement accessible

Trois commits locaux suivent P6 sur l’étape 2 : `826c4f7`, `1924df2`, puis `b695e46`. Le diff touche 14 fichiers et ajoute notamment `email_manager.0010_quote_phrase`, `pdf_manager.0010_quote_phrase`, les commandes et tests de l’étape 2.

L’inspection de `core/quote_regime.py` à ce SHA confirme le mixin `PhraseAnchor`, `create_phrase_quote`, `certify_phrase_quote`, les bornes Python `[start,end)`, les trois empreintes et la propriété `effective_certification`. Une correction sur scan distingue tranche OCR ancrée et texte certifié. Cette capacité locale précise la dépendance UC-C-08/L3-B : ne pas la recréer dans C, et vérifier sa version et ses invariants dans les futurs dossiers.

Le plan de A à ce SHA **rapporte** l’étape 1 en production et l’étape 2 sur clone, avec 205 tests, et laisse le déploiement réel de l’étape 2 sous autorisation distincte. Ces résultats sont cités comme rapport de branche : ils ne sont ni réexécutés ici, ni une attestation du serveur par B. La PK 305 et les bornes d’exemple décrivent le clone rapporté, pas une identité à imposer à une base réelle.

### 3.3 C0-A

Le [rapport](lots/C0-A/RAPPORT_EXECUTION_C0A.md) et le [diff](lots/C0-A/C0A_DIFF_COMPLET.patch) sont désormais dans le dépôt. Les 209 tests dont 31 nouveaux sont ceux de la copie isolée; le processus indique C0-A **non atterri**. Aucun test ou contrôle d’application du patch n’est relancé pour cette consolidation.

## 4. Changements de contrat et incompatibilités résolues

- La permanence globale ne gouverne plus tous les nouveaux bordereaux : CHRONO_VERSION est décidé, avec conservation des associations historiques. Les détails R ne réintroduisent pas l’alternative de principe rejetée.
- Démonstration ne devient pas une entité autonome portant conclusions et validation. La rédaction, les UP et sélections restent les autorités C; le besoin de regroupement n’impose pas une table.
- Le nouveau parcours documentaire complète la concordance rédactionnelle. Les deux ne sont pas fusionnés; une décision d’appui demeure encore une autre responsabilité.
- Les compositions exactes et les fichiers ne sont pas déduits d’un titre ou d’une cote. Le cas `[A,B]→[A,C]` et les scissions/fusions sont explicitement couverts par les scénarios.
- Le processus local antérieur disait « Classe : jamais », exigeait l’ERD seulement au changement de schéma et la séquence seulement pour l’atomicité. Ces règles sont supplantées par le mandat explicite, et le fichier actif est révisé. Les diagrammes d’états demeurent utiles en complément.
- Un modèle de données observé et un diagramme de classes observé ne sont pas les vues cibles d’un use case. La réussite technique de PlantUML ne devient pas une approbation utilisateur.

Les sources/rendus historiques restent inchangés. Leurs index signalent la nouvelle autorité et le besoin de réexamen; US-C-09 est actualisée textuellement pour D05. Les anciens rapports de conception et l’évaluation V2 gardent leur valeur historique, sans supplanter cette décision ultérieure.

## 5. Réserves et risques architecturaux

| Risque | Réserve / contrôle prévu | Portée bloquée |
|---|---|---|
| Fausse identité d’une liasse modifiée | R01/R02, composition exacte et décisions de filiation; EPIC-V2:T10 | Pièces composites, concordance et sorties concernées |
| Ordre/cotes instables ou dates inventées | D06 + R03/R04; profil et précision capturés | Classement et sous-cotes des types non décidés |
| Exclusion silencieuse d’une pièce invoquée | R05, usages analytiques/produits explicites, C-UML:N16 | Nouveau périmètre de production |
| Multiples brouillons non maîtrisés | R06 et test de concurrence | Création selon le parcours de rédaction |
| Historique régénéré depuis des objets vivants | Restitution des octets conservés; R07 pour toute promesse supplémentaire | Restitution/régénération dont le contrat reste ambigu |
| Commit SQL avec fichiers manquants ou modifiables | R08, protocole durable, pannes et droits; C-UML:N07–N09 | Premier gel réel et publication finale |
| Ancienne confirmation traitée comme un examen nouveau | Examen immuable et transition TR; aucune validation rétroactive | Strict des relations sans manifeste suffisant |
| Code écrit sur un socle qui ignore E01/A | SHA explicites, comparaison et future intégration mandatée | Toute intégration sans rapprochement |
| Dossiers approuvés devenant périmés | Empreintes, version et analyse d’impact; C-UML:N13 | Nouveau code fondé sur une ancienne approbation |
| Lots empilés sans intégration | C0-A non atterri, six conditions du processus maintenues | Exécution du lot suivant; la conception reste possible |

Les choix R01–R08 restent des décisions ou modalités à approuver dans leurs dossiers. Ils ne bloquent pas les corrections C0-A sans schéma. Les propriétés `effective_certification`, les hashes et les signaux existants ne sont pas présentés comme un gel global déjà réalisé.

## 6. Travaux avant le premier use case implantable

1. Constituer une première version du modèle global cible correspondant au périmètre C0-A/fondations, en signalant les zones futures non arbitrées.
2. Produire les dossiers **UC-C-13, puis 14 et 15** : spécification bornée au patch, activité réexaminée, séquence avec atomicité/refus, ERD local sans changement de schéma et classes/composants distinguant P6 et modifications proposées.
3. Rattacher leurs critères aux éléments des quatre vues et aux scénarios C0-A/NR pertinents, avec résultats attendus et contre-épreuves. Les résultats isolés du rapport restent identifiés séparément.
4. Effectuer les validations T/F/A, résoudre les écarts, puis soumettre les versions exactes à l’approbation utilisateur. Le premier dossier proposé est UC-C-13; l’acceptation de celui-ci ne vaut pas acceptation de tout C0-A.
5. Après approbation des trois dossiers et mandat distinct de revue/atterrissage : contrôler la conformité du patch et les conditions de lot, puis intégrer uniquement si autorisé. Aucun changement de P6 ou des ressources A n’est implicite.
6. Après C0-A atterri, préparer L1-A dans son périmètre propre, avec 01A/05E et les décisions nécessaires. Ne pas lancer ce lot dans la présente intervention.

Les contrats, modèles et rendus non PHRASE peuvent être conçus sans la bascule réelle de A. Les branches/sources, droits de stockage et migrations réellement disponibles seront des préalables d’activation vérifiés, pas supposés.

## 7. Vérifications de cette intervention

Vérifications documentaires effectuées : lecture des mandats et contrats pertinents, inspection locale des références et diffs, lecture distante des têtes, conservation exacte des sources reçues et des deux états antérieurs, matrice exhaustive des critères, inventaire des use cases et conservation des IDs de tests.

Le contrôle final de livraison vérifie les liens locaux actifs, la couverture des 91 critères et des 14 scénarios V2, les 22 statuts et les 38 lignes NR/CF3 inchangées. Il est distingué de la validation UML des dossiers futurs.

Résultats du contrôle documentaire : **176 liens locaux résolus sur 15 documents**,
8 invariants et 91 critères sans manque ni doublon, 14 scénarios V2 conservés,
16 contre-épreuves et 6 scénarios de communication supplémentaires distincts.
Les tableaux Markdown sont interprétés correctement, dont les deux inventaires
de 22 lignes. Les statuts sont 9 `A_SPECIFIER` et 13 `A_MODELISER`.
Les quatre empreintes des sources/historiques correspondent aux copies exactes;
les 38 lignes NR/CF3 restent identiques. `git diff --check` réussit; HEAD reste
P6 et aucun diff applicatif, de migration ou de `legal/` n’est constaté.

**NON EXECUTE :** nouveaux tests applicatifs, tests SQL/stockage, migrations, accès à la base réelle, vérification du serveur, production/compilation de nouveaux quadruplets cibles et déploiement. Aucun diagramme cible n’est déclaré compilé ou visuellement validé par cette intervention. Les résultats des séries existantes restent ceux de leurs livraisons précédentes.

## 8. Décision proposée à l’utilisateur

Le principe D05 et la porte UML sont déjà décidés par le mandat. Les cinq livrables sont soumis comme consolidation de conception, pas comme autorisation d’implémenter.

La prochaine intervention proposée porte sur les dossiers UML bornés à C0-A, en commençant par UC-C-13. Les arbitrages R peuvent être décidés progressivement avant les use cases qui en dépendent. **Aucun use case n’est encore VALIDE_ARCHITECTURE, APPROUVE_UTILISATEUR ou PRET_DEVELOPPEMENT au titre du nouveau protocole.**
