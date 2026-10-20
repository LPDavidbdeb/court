# Mandat à l'Agent B — Validation de couverture du backlog et préparation de C0-A

## 1. Décision sur le backlog

J'ai examiné le backlog `BLC-2026-10-20-R1` de l'architecture C.

**J'accepte sa structure comme référence provisoire de pilotage du chantier du second pont entre la preuve et les actes judiciaires.**

Je retiens notamment :

- Les 44 tickets répartis entre préparations transversales, décisions, dossiers UML et lots de livraison.
- Les 22 use cases identifiés.
- La séparation entre conception, approbation et implantation.
- Les dépendances et l'ordre de livraison proposés.
- La conservation des exigences E01, des 38 scénarios NR/CF3 et des décisions architecturales existantes.
- La priorité accordée à C0-A et aux dossiers UML-13, UML-14 et UML-15.

Cette acceptation ne constitue toutefois ni une validation de la complétude fonctionnelle de l'epic ni une autorisation de développement.

**Je souhaite maintenant vérifier que le backlog couvre réellement toutes les capacités nécessaires, et particulièrement les fonctionnalités qui pourraient être demeurées implicites entre plusieurs use cases.**

## 2. Première tâche — Revue de couverture fonctionnelle

Examine les six questions suivantes en confrontant le backlog aux documents qui font autorité :

- `DECISIONS_ARCHITECTURE_C_CONSOLIDEES.md`
- `AVENANT_ARCHITECTURE_C.md`
- `MATRICE_COUVERTURE_V2_C.md`
- `PLAN_MODELISATION_UML.md`
- `PROTOCOLE_VALIDATION_UML.md`
- `registre_validation.md`
- Les spécifications existantes et les documents de conception initiaux.

Pour chaque question, détermine si la capacité est entièrement couverte, partiellement couverte, absente ou encore indécidable.

Identifie les exigences, use cases, critères d'acceptation et scénarios de test qui établissent ton diagnostic.

### A. Construction d'un raisonnement probatoire composé

Vérifie que la combinaison des UC-C-02, 03, 05P et 06 permet de représenter un raisonnement composé de propositions successives, de prémisses, de conclusions intermédiaires, de réserves et d'appuis distincts.

Utilise comme cas de référence notre raisonnement relatif aux cours de danse :

1. La mère participait à des cours certains soirs.
2. Ces cours nécessitaient son absence du domicile.
3. Pendant certaines de ces absences, le père assumait la prise en charge des enfants.
4. Ces faits contribuent à caractériser sa participation régulière aux responsabilités parentales.

Le système doit permettre de conserver les sources et les appuis propres à chaque proposition, de représenter les relations entre propositions et de modifier ou réutiliser le raisonnement sans attribuer automatiquement un appui à une conclusion qu'il ne soutient pas directement.

Vérifie si cette capacité est démontrable avec l'architecture C actuelle.

Ne réintroduis pas une entité `Démonstration` autonome par défaut. Si une lacune existe, propose la modification minimale compatible avec la chaîne architecturale approuvée :

`Cible rédactionnelle → UtilisationPreuve → SélectionPreuve → Élément probatoire → Source`

### B. Allégations négatives et constats d'absence

Vérifie qu'il est possible d'appuyer un paragraphe alléguant une absence.

Exemple : une requête ne contient pas une allégation déterminée.

Cette capacité doit permettre de définir :

- Le document ou l'ensemble documentaire examiné.
- La portée du constat.
- Les critères d'examen, lorsque nécessaires.
- Les éléments documentaires permettant de vérifier le constat.
- Les limites de ce qui peut raisonnablement être conclu.

Il ne faut ni inventer une citation inexistante ni confondre l'absence d'une allégation dans un document avec la preuve générale que le fait allégué n'existe pas.

Détermine si cette fonction est déjà représentable dans les UC-C-03, 04 ou 05P.

Si elle l'est, indique le critère d'acceptation correspondant. Sinon, propose un complément vérifiable.

### C. Compatibilité des citations HERITE et PHRASE

Le chantier A a maintenant livré les étapes 1 et 2 dans l'application réelle.

La base comporte :

- 268 citations de courriels `HERITE`.
- 126 citations PDF `HERITE`.
- Une première citation `PHRASE` certifiée, liée à son antécédent.

Le commit actuellement publié sur `epic/E01-numerotation-concordance` est :

`515666eb8c6e7fdcdd265f9187c9c37b769b0fed`

Vérifie comment les UC-C-03, 04, 08 et le lot L3-B doivent traiter les deux régimes.

En particulier :

- Une citation historique demeure identifiable et ses usages existants doivent rester préservés.
- Une citation `PHRASE` dispose de garanties d'ancrage et de certification propres.
- Une relation `derived_from` ne certifie pas rétroactivement la citation historique.
- Le second pont ne doit pas confondre les garanties disponibles selon le régime.
- Les conditions d'admissibilité d'une citation dans un rendu strict doivent être explicites.

Il faut établir si les 394 citations historiques peuvent être utilisées dans le second pont, à quelles conditions, et comment sont signalées les garanties qui leur manquent éventuellement.

Ne développe pas un nouveau régime de citations : celui-ci relève du fournisseur A.

### D. Vérification des dépendances et des cycles

Examine les dépendances entre les dix lots, particulièrement celles qui concernent L3-A, L3-B, L4, L5 et L6.

L3-A renvoie notamment à des contrats de use cases dont certaines fonctionnalités seront livrées ultérieurement.

Distingue explicitement :

1. Les dépendances de conception : un contrat doit être défini avant l'implantation.
2. Les dépendances d'exécution : une fonctionnalité doit déjà être implantée.
3. Les dépendances de validation : plusieurs fonctionnalités doivent être présentes pour un test intégré.

Vérifie que le graphe des dépendances d'exécution ne contient aucun cycle.

Si des contrats doivent être définis avant leur implantation, identifie-les sans transformer artificiellement leur use case complet en préalable au lot précédent.

### E. Continuité du parcours utilisateur

Vérifie que les use cases permettent de réaliser un parcours complet de rédaction, depuis les preuves déjà recueillies.

Le scénario de référence doit comprendre :

1. Créer une analyse ou une version de travail.
2. Rédiger et organiser des propositions factuelles.
3. Rechercher ou retrouver des preuves existantes.
4. Sélectionner précisément les éléments qui soutiennent une proposition.
5. Examiner leurs appuis et leurs limites.
6. Insérer des citations fidèles et des références.
7. Déterminer les pièces effectivement utilisées pour la production.
8. Attribuer les cotes chronologiquement selon `CHRONO_VERSION`.
9. Produire le texte, le bordereau et les fichiers correspondants.
10. Figer et conserver la version.
11. Préparer une version ultérieure, avec les concordances nécessaires.

Pour chaque transition, identifie le use case responsable, les données reçues et produites, ainsi que les opérations laissées à l'utilisateur.

Signale les transitions qui exigeraient une manipulation manuelle non prévue ou une fonctionnalité absente.

Ce parcours transversal ne doit pas entraîner automatiquement onze nouvelles stories. Son rôle est d'établir la complétude des fonctionnalités existantes.

### F. Référence Git et autorité d'intégration

La branche réellement déployée par l'Agent A est `epic/E01-numerotation-concordance`, au commit `515666e`.

Le patch C0-A a été conçu sur le socle antérieur P6, au commit `212a7fe`.

Exécute TRANS-01 afin de déterminer :

- Les différences pertinentes entre P6 et le socle actuel.
- La compatibilité du patch C0-A avec ces changements.
- Les dépendances nouvelles envers les composants `HERITE / PHRASE`.
- Les conflits éventuels.
- La référence exacte recommandée pour les prochaines validations.
- La destination Git proposée pour l'intégration des lots C.

Distingue le socle technique constaté du socle formellement autorisé.

Ne décide pas unilatéralement de modifier la branche d'intégration ou de faire converger `main` et `epic`.

## 3. Deuxième tâche — Actualiser la matrice de couverture

À partir de cette analyse, complète la matrice `V2/C` et, lorsque nécessaire, le backlog.

Pour chaque lacune identifiée, indique :

- L'exigence concernée.
- Le comportement attendu.
- Le ou les use cases responsables.
- Le critère d'acceptation existant ou manquant.
- Les scénarios de test nécessaires.
- Le lot chargé de sa livraison.
- L'éventuelle décision utilisateur requise.

Distingue les lacunes réelles des éléments déjà couverts par les spécifications détaillées.

Je ne souhaite pas une inflation du nombre de tickets. Une correction ciblée d'un critère d'acceptation ou l'ajout d'un test transversal est préférable à une nouvelle story lorsque cela suffit.

Toute nouvelle story proposée doit répondre à une capacité utilisateur distincte qui ne peut raisonnablement être intégrée à une story existante.

**Le résultat recherché est une couverture démontrable, pas une augmentation du volume documentaire.**

## 4. Troisième tâche — Poursuivre les préparations de C0-A

Cette revue de couverture ne doit pas interrompre les travaux indépendants déjà identifiés comme prioritaires.

Poursuis donc :

**TRANS-01**

Établir le socle technique autorisable à partir du commit actuel et la compatibilité de C0-A.

**TRANS-02**

Préparer les premières versions de l'ERD consolidé et du diagramme des classes consolidé, en limitant leur périmètre initial à C0-A.

**TRANS-04**

Établir la traçabilité entre les exigences, les critères d'acceptation, les diagrammes, les tests et les lots.

**UML-13**

Préparer en priorité le dossier complet du use case UC-C-13 relatif à la modification d'une occurrence partageant un `Statement`.

Il doit comprendre les quatre vues obligatoires :

- Activity Diagram.
- Sequence Diagram.
- Entity-Relationship Diagram.
- Class Diagram.

Les diagrammes doivent être compilables, produire des SVG lisibles et faire l'objet des validations prévues par le protocole.

Une fois UML-13 suffisamment avancé, prépare UML-14 et UML-15 dans le même cadre.

N'accorde aucune approbation utilisateur par présomption. Soumets-moi les dossiers de conception à approuver.

## 5. Attention particulière à C0-A

Le lot C0-A existe déjà sous forme de patch et de résultats de tests sur clone.

Il ne doit pas être traité comme s'il était inexistant, mais ses 209 tests réussis ne constituent pas une preuve de conformité au nouveau socle.

Dans la revue, vérifie notamment que la consultation des appuis d'origine traite correctement une combinaison d'associations valides et invalides : une anomalie sur un référent ne doit pas faire disparaître silencieusement tous les appuis valides.

Si le comportement est déjà couvert, indique le test qui le démontre. Sinon, consigne la lacune et la correction attendue dans le dossier de revue C0-A.

Ne modifie pas le patch avant autorisation de son périmètre de correction.

## 6. Gouvernance et restrictions

La gouvernance récemment décidée demeure applicable.

- L'Agent B conçoit, analyse, modélise et révise.
- J'approuve les décisions fonctionnelles et les dossiers de conception.
- L'Agent A est responsable de l'implantation.

Pour ce mandat, tu peux modifier les documents du chantier C dans ton périmètre autorisé.

En revanche :

- Ne modifie pas le code applicatif.
- N'applique aucune migration.
- Ne modifie pas la base réelle.
- Ne fusionne pas C0-A.
- Ne modifie pas les travaux de l'Agent A.
- Ne lance pas de nouveau lot de développement.
- N'invente pas de décisions utilisateur pour fermer artificiellement une réserve.

Les décisions `DEC-R01` à `DEC-R08` restent ouvertes tant que je ne les ai pas approuvées, sauf lorsqu'il s'agit d'un choix purement technique relevant explicitement de ton mandat.

Ne produis pas prématurément les 88 diagrammes des 22 dossiers. La conception doit avancer progressivement, selon les dépendances.

## 7. Livrables attendus

Je souhaite recevoir :

**A. Rapport de couverture fonctionnelle**

Une analyse des six questions, indiquant les capacités démontrées, les lacunes et les décisions résiduelles.

**B. Matrice de couverture actualisée**

Les correspondances entre exigences, use cases, critères, scénarios et lots, sans duplication inutile.

**C. Backlog révisé, si nécessaire**

Une version R2 du backlog uniquement si les résultats imposent des corrections. Explique chaque ajout, retrait ou changement de dépendance.

**D. Résultats de TRANS-01, TRANS-02 et TRANS-04**

Le socle technique proposé, les premières vues consolidées et les références de traçabilité.

**E. Dossier UML-13**

Le dossier de conception du premier use case, avec ses quatre diagrammes, les validations effectuées et les points restant à approuver.

**F. Préparation de C0-A**

Un diagnostic de compatibilité et la liste des conditions permettant de soumettre l'intégration de C0-A à autorisation.

## 8. Résultat attendu

Je souhaite pouvoir répondre à deux questions :

**Premièrement : le backlog couvre-t-il l'ensemble des fonctionnalités nécessaires à la réalisation du second pont entre la preuve et les actes, ou reste-t-il des trous identifiables?**

**Deuxièmement : pouvons-nous désormais approuver le dossier UML-13 et préparer l'intégration de C0-A sur le socle actuel, sans conflit avec les développements de l'Agent A?**

Ne reprends pas l'architecture depuis le début. Travaille à partir des décisions, contrats et scénarios existants.

**Tu es autorisé à commencer immédiatement cette revue de couverture et les travaux documentaires préparatoires de C0-A. Aucune autorisation de développement ou d'intégration n'est accordée par le présent mandat.**