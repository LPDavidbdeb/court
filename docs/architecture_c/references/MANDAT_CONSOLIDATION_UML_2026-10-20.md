# Mandat à l'agent B — Consolidation de l'architecture C et protocole de validation UML préalable

## 1. Contexte et rôle

Tu agis comme **architecte logiciel et réviseur indépendant** du projet `court`.

Tu es responsable de la cohérence fonctionnelle et architecturale, de la définition des contrats, de leur vérifiabilité et de la préparation des spécifications destinées à l'agent A, responsable du développement.

Nous poursuivons les travaux de l'architecture C, dans le contexte de la réorganisation de la preuve et de la rédaction d'actes judiciaires.

Les références comprennent notamment :

- `docs/modele_preuve/CONCEPTION_PREUVE.md`
- `docs/modele_preuve/ARCHITECTURE_CAUSES.md`
- Les 15 user stories de l'architecture C et leurs diagrammes.
- Les exigences, critères et scénarios déjà retenus pour E01.
- Les travaux sur les citations `HERITE / PHRASE`.
- L'ERD de l'état actuel du système, établi à partir de P6.
- Ton évaluation `EVALUATION_EPIC_REDACTION_V2_2026-10-20.md`.
- La proposition d'epic rédaction V2 qui a fait l'objet de cette évaluation.

Le commit de référence documentaire est :

`30ce0acb92522460c5a3f73019070dd0e7e2353c`

Tu dois cependant vérifier les références Git effectivement pertinentes, notamment les différences entre `main`, P6 et les branches de développement accessibles.

**Il ne s'agit pas de concevoir une architecture concurrente.**

Ton mandat consiste à consolider l'architecture C, à y intégrer les exigences manquantes et à définir les conditions permettant d'autoriser progressivement son implantation.

---

## 2. Décision explicite — Politique de cotation D05

Le principe de cotation est désormais décidé.

**Décision D05 : `CHRONO_VERSION`.**

Chaque nouvelle version d'un acte possède une cotation propre, déterminée par le classement chronologique des pièces effectivement retenues pour cette version.

Lorsqu'une pièce est ajoutée, retirée ou remplacée, les cotes de la version de travail sont recalculées selon ce classement.

Après le gel d'une version, les associations entre les pièces et leurs cotes deviennent immuables pour cette version.

Les versions ultérieures peuvent attribuer des cotes différentes aux mêmes pièces. Une table de correspondance permet de retrouver leur identité et leur cotation à travers les différentes versions.

Le dépôt de juillet 2026 et les associations historiques documentées restent intacts.

Il faut donc distinguer :

1. L'identité permanente des sources probatoires.
2. L'identité d'une pièce produite, qui peut être simple ou composite.
3. La composition documentaire d'une pièce.
4. La cote attribuée à cette pièce dans une version déterminée.
5. L'association historique figée entre version, pièce, composition et cote.

Cette décision règle le principe de D05.

Elle ne règle pas automatiquement tous ses détails d'application : dates incertaines, égalités chronologiques, sous-cotes, liasses, modifications de composition et particularités du dépôt historique.

Ces points doivent être spécifiés sans réintroduire une cotation globalement permanente contraire à `CHRONO_VERSION`.

---

## 3. Intégration de l'epic rédaction V2

Je retiens ta recommandation de rattacher les exigences de V2 à l'architecture C plutôt que de maintenir un epic parallèle.

Tu dois produire une comparaison de couverture permettant de distinguer :

- Ce qui est déjà couvert par C et ne nécessite aucune modification.
- Ce qui doit être précisé dans un contrat ou une user story existante.
- Ce qui nécessite une nouvelle user story ou un nouveau use case.
- Ce qui constitue une décision architecturale encore ouverte.
- Ce qui est incompatible avec les décisions déjà retenues.

En particulier :

### 3.1 Rédaction et preuve

Conserver la logique retenue dans C :

`Cible rédactionnelle → UtilisationPreuve → SélectionPreuve → Élément probatoire → Source`

Ne pas introduire automatiquement une nouvelle entité `Démonstration` portant un raisonnement autonome.

Si une fonction de regroupement rédactionnel s'avère nécessaire, définir comment elle peut être réalisée sans dupliquer les usages, les sélections, les conclusions ou leurs autorités de validation.

### 3.2 Pièces simples et composites

Définir formellement :

- Ce qui constitue une pièce produite.
- La relation entre une pièce et ses sources.
- L'identité d'une pièce composite.
- La distinction entre identité logique et composition documentaire exacte.
- Les règles de déduplication.
- Le traitement des liasses, fragments et sous-cotes.
- Les conséquences d'une modification de composition.
- Les règles applicables aux pièces issues d'une ou plusieurs sources.
- La distinction entre réutilisation probatoire et production documentaire.

Le cas d'une liasse `[A, B]` devenant `[A, C]` doit être spécifié et testé.

Une égalité de titre ou de cote ne suffit jamais à prouver une identité documentaire.

### 3.3 Concordance documentaire

Compléter la concordance rédactionnelle existante par une concordance propre aux pièces produites.

Cette concordance doit traiter au minimum :

- Les pièces conservées.
- Les pièces ajoutées.
- Les pièces retirées.
- Les pièces recotées.
- Les pièces composites dont la composition évolue.
- Les scissions et fusions.
- Les correspondances non univoques.
- Les situations où une même cote désigne des pièces différentes selon la version.
- Les correspondances avec le dépôt historique.

La concordance doit pouvoir être calculée à partir des états figés, sans dépendre des structures de travail actuelles.

### 3.4 Production documentaire

Compléter les exigences de production relatives :

- Au bordereau de la version.
- Aux références aux pièces dans l'acte.
- Aux fichiers de pièces nommés selon leurs cotes.
- Aux cahiers et assemblages.
- Aux manifestes de production.
- Aux empreintes d'intégrité.
- À la reproductibilité des versions figées.
- À la gestion des échecs de production.

L'acte, ses références, le bordereau et les fichiers doivent partager une même autorité de calcul, conformément au contrat de `ResultatVersion`.

### 3.5 Gel et communication

Préserver la distinction entre :

- Version en préparation.
- Version figée.
- Version déposée.
- Version communiquée.

Spécifier les garanties de cohérence lorsque le gel implique à la fois la base PostgreSQL et la production de fichiers.

Une transaction SQL ne doit pas être présentée comme garantissant, à elle seule, l'atomicité des opérations sur le système de fichiers.

---

# 4. Nouvelle exigence obligatoire — Conception UML préalable à chaque use case

**Aucun use case ne doit être implanté avant la production et la validation de quatre diagrammes UML réalisés avec PlantUML.**

Cette exigence est obligatoire pour les use cases existants de l'architecture C et pour tous les nouveaux use cases introduits par le présent mandat.

Les diagrammes ne sont pas de simples illustrations. Ils constituent des artefacts de conception contractuels devant permettre de vérifier le comportement attendu avant d'autoriser le développement.

Pour chaque use case, produire les quatre diagrammes suivants.

## 4.1 Activity Diagram — Diagramme d'activité

Ce diagramme doit représenter le déroulement fonctionnel du use case.

Il doit notamment présenter :

- Le déclencheur et les préconditions.
- Les acteurs et responsabilités.
- Les activités successives.
- Les choix et conditions de branchement.
- Les vérifications nécessaires.
- Les cas d'échec, refus et annulation.
- Les résultats attendus.
- Les postconditions.

Il doit distinguer, lorsque nécessaire, les actions de l'utilisateur, celles du système et celles des services techniques.

Les parcours nominaux et les principales variantes doivent être couverts.

**Objectif : valider ce que fait le système et dans quelles conditions.**

## 4.2 Sequence Diagram — Diagramme de séquence

Ce diagramme doit représenter les interactions nécessaires à l'exécution du use case.

Il doit notamment identifier :

- Les acteurs.
- Les interfaces.
- Les composants ou services applicatifs.
- Les objets et agrégats métier.
- Les accès aux données.
- Les appels, réponses et événements.
- Les validations.
- Les frontières transactionnelles.
- Les interactions avec le système de fichiers, lorsqu'elles existent.
- Les refus et chemins d'erreur pertinents.

Pour une opération complexe, notamment le gel ou la production documentaire, il peut être nécessaire de produire plusieurs scénarios de séquence.

**Objectif : valider comment les composants coopèrent pour réaliser le comportement défini par le diagramme d'activité.**

Ne pas présenter comme existant dans le code un service qui n'est encore qu'une proposition de conception.

## 4.3 Entity-Relationship Diagram — ERD

Ce diagramme doit représenter le modèle de données nécessaire au use case.

Il doit préciser :

- Les entités persistantes concernées.
- Leurs identifiants.
- Leurs attributs significatifs.
- Leurs relations.
- Les cardinalités.
- Les contraintes d'unicité.
- Les contraintes d'intégrité.
- Les règles de suppression.
- Les données versionnées ou immuables.
- Les relations avec les entités existantes.

Chaque diagramme doit clairement distinguer :

1. Les structures existantes.
2. Les structures proposées.
3. Les structures existantes à modifier.

Un ERD limité au contexte du use case est acceptable, mais il doit être cohérent avec un **ERD consolidé de l'architecture cible**.

Ne pas inventer des tables pour représenter des concepts qui ne nécessitent pas de persistance autonome.

**Objectif : valider ce qui doit être conservé, sous quelles contraintes et avec quelles relations.**

## 4.4 Class Diagram — Diagramme de classes

Ce diagramme doit représenter la structure logicielle permettant d'implanter le use case.

Il doit préciser :

- Les classes ou composants pertinents.
- Leurs principales responsabilités.
- Les attributs nécessaires à la compréhension du contrat.
- Les opérations ou méthodes significatives.
- Les interfaces et abstractions.
- Les associations et dépendances.
- Les relations d'héritage ou de composition, lorsqu'elles sont justifiées.
- Les invariants confiés aux objets ou services.

Il doit permettre d'identifier la répartition des responsabilités entre les modèles Django, les services métier, les services de lecture, les moteurs de rendu et les autres composants.

Le diagramme de classes ne doit pas reproduire mécaniquement l'ERD : il doit montrer la **structure et les responsabilités du logiciel**, y compris les classes qui ne correspondent à aucune table.

**Objectif : valider où résident les comportements et responsabilités avant leur implantation.**

---

# 5. Protocole obligatoire de validation

La production des quatre diagrammes ne suffit pas.

Chaque diagramme doit faire l'objet d'une validation explicite.

## 5.1 Validation technique PlantUML

Pour chaque diagramme :

- Le fichier source `.puml` doit être conservé.
- La syntaxe doit être compilable par PlantUML.
- Le rendu SVG doit être généré.
- Le rendu doit être vérifié visuellement.
- Les erreurs de compilation doivent être corrigées.
- Les liens et dépendances entre diagrammes doivent être contrôlés.

Un diagramme non compilable ou illisible ne peut pas être déclaré validé.

## 5.2 Validation fonctionnelle

Vérifier que les diagrammes couvrent les critères d'acceptation du use case.

Pour chaque critère, indiquer quels éléments des diagrammes permettent de vérifier sa prise en charge.

Les chemins nominaux, les refus, les erreurs et les postconditions doivent correspondre aux exigences approuvées.

Une exigence absente des diagrammes constitue une lacune à corriger.

## 5.3 Validation architecturale

Vérifier la cohérence entre les quatre diagrammes.

En particulier :

- Les activités doivent correspondre à des interactions réalisables.
- Les interactions doivent pouvoir être prises en charge par les classes et services représentés.
- Les données manipulées doivent être compatibles avec l'ERD.
- Les contraintes d'intégrité doivent être respectées par les séquences.
- Les responsabilités ne doivent pas être dupliquées sans justification.
- Les diagrammes ne doivent pas contredire les invariants de l'architecture C.
- Les choix d'un use case ne doivent pas rendre un autre use case incohérent.

Toute contradiction doit être documentée puis résolue avant validation.

## 5.4 Validation des scénarios de test

Chaque use case doit posséder une matrice de traçabilité :

`Exigence → Critère d'acceptation → Diagramme → Scénario de test`

Les scénarios existants doivent être réutilisés.

Les nouveaux scénarios doivent compléter la couverture, sans supprimer ni renuméroter arbitrairement les scénarios antérieurs.

Les tests négatifs sont obligatoires lorsque le use case porte sur un refus, une autorisation, une suppression, une mutation historique ou une opération irréversible.

## 5.5 Validation par le réviseur et approbation utilisateur

La validation comporte deux décisions distinctes.

**Validation architecturale — Agent B**

Tu attestes que :

- Les quatre diagrammes sont techniquement valides.
- Ils couvrent les exigences.
- Ils sont mutuellement cohérents.
- Ils respectent les invariants et décisions approuvés.
- Les points ouverts ont été résolus ou sont explicitement bloquants.

**Approbation fonctionnelle — Utilisateur**

Les livrables sont ensuite soumis à mon examen.

Je peux les approuver, demander des corrections ou suspendre l'autorisation du use case.

**Une validation architecturale par l'agent B ne vaut pas autorisation d'implanter.**

Aucun use case ne passe au développement sans mon approbation explicite du dossier de conception correspondant.

Toute modification ultérieure d'une décision ou d'un contrat approuvé qui affecte les diagrammes doit déclencher une analyse d'impact et, si nécessaire, une nouvelle validation.

---

# 6. Statuts des use cases

Chaque use case doit avoir un statut identifiable :

| Statut | Signification |
|---|---|
| `A_SPECIFIER` | Exigences ou contrats encore incomplets |
| `A_MODElISER` | Exigences définies, diagrammes à produire |
| `EN_REVUE` | Diagrammes produits, validation en cours |
| `CORRECTIONS_REQUISES` | Lacunes ou contradictions identifiées |
| `VALIDE_ARCHITECTURE` | Revue technique et architecturale réussie |
| `APPROUVE_UTILISATEUR` | Dossier de conception approuvé pour implantation |
| `PRET_DEVELOPPEMENT` | Dépendances et conditions préalables également satisfaites |

Le statut d'approbation doit être traçable : date, référence de la version du dossier, décision et éventuelles réserves.

Ne jamais assimiler un diagramme généré, un test PlantUML réussi ou une revue interne à une approbation utilisateur.

---

# 7. Structure documentaire attendue

Proposer une organisation durable des fichiers permettant de rattacher sans ambiguïté chaque use case à ses diagrammes.

Par exemple :

```text
docs/modele_preuve/
  architecture_c/
    decisions/
      D05_CHRONO_VERSION.md

    use_cases/
      UC-C-09/
        specification.md
        activity.puml
        sequence.puml
        erd.puml
        class.puml
        validation.md
        tracabilite.md

      UC-C-10/
        ...

    modele_global/
      erd_consolide.puml
      classes_consolidees.puml

    registre_validation.md
```

Cette arborescence est indicative.

Tu dois examiner la structure actuelle du dépôt et proposer une organisation compatible, sans déplacer arbitrairement les documents existants ni rompre leurs liens.

Les diagrammes partagés peuvent être factorisés, mais **chaque use case doit disposer de quatre vues UML identifiables, consultables et validées dans son propre dossier de conception**.

Les diagrammes de l'état existant doivent rester distincts de ceux de l'architecture cible.

---

# 8. Articulation avec le développement par l'agent A

Le processus de livraison doit suivre cette séquence :

**Étape 1 — Spécification**

Définir le comportement, les critères d'acceptation, les invariants et les dépendances du use case.

**Étape 2 — Modélisation**

Produire les quatre diagrammes PlantUML.

**Étape 3 — Validation**

Compiler, examiner et valider la couverture fonctionnelle et la cohérence architecturale.

**Étape 4 — Approbation**

Me soumettre le dossier et obtenir mon approbation explicite.

**Étape 5 — Implantation**

Seulement après les étapes précédentes, préparer les instructions techniques destinées à l'agent A.

**Étape 6 — Vérification de conformité**

Après développement, comparer l'implantation réelle aux diagrammes et aux contrats approuvés.

Une divergence doit être corrigée ou faire l'objet d'une modification de conception expressément approuvée.

L'agent A ne doit pas être autorisé à résoudre silencieusement, par un choix de code, une ambiguïté architecturale encore ouverte.

---

# 9. Livrables demandés pour le présent mandat

Pour cette première intervention, tu dois produire :

### Livrable A — Avenant architectural à C

Document exposant :

- La décision D05 `CHRONO_VERSION`.
- Les changements nécessaires aux contrats existants.
- Les spécifications relatives aux pièces composites.
- La concordance documentaire entre versions.
- Les exigences complémentaires de production documentaire.
- Les dépendances et décisions résiduelles.

### Livrable B — Matrice de couverture

Comparaison entre l'epic rédaction V2 et les user stories de C.

Pour chaque exigence, indiquer si elle est déjà couverte, à compléter, nouvelle, incompatible ou à arbitrer.

### Livrable C — Inventaire et plan de modélisation UML

Recenser tous les use cases de l'architecture C et les nouveaux use cases nécessaires.

Pour chacun, indiquer :

- Son identifiant.
- Les user stories concernées.
- Les quatre diagrammes exigés.
- Les diagrammes déjà disponibles.
- Les diagrammes manquants.
- Les dépendances.
- L'ordre recommandé de conception.
- Le statut de validation.

Les Activity Diagrams déjà produits peuvent être réutilisés, mais ils doivent être réexaminés à la lumière des nouvelles exigences.

### Livrable D — Protocole de validation

Formaliser les règles des sections 4 à 8 dans un document de référence opposable aux travaux de développement ultérieurs.

Ce protocole doit définir un véritable **point de contrôle préalable à l'implantation**, et non une simple recommandation documentaire.

### Livrable E — Rapport d'évaluation

Produire une synthèse comprenant :

- Les décisions intégrées.
- Les incompatibilités résolues.
- Les questions restant ouvertes.
- Les risques architecturaux.
- Les modifications envisagées à la conception actuelle.
- Les travaux nécessaires avant d'autoriser le premier use case.

---

# 10. Restrictions d'exécution

Pour ce mandat :

- Ne modifie pas le code applicatif.
- N'exécute aucune migration.
- Ne modifie pas la base réelle.
- Ne modifie pas les archives historiques.
- Ne présente pas une fonctionnalité cible comme déjà livrée.
- Ne considère pas les tests réalisés sur une branche isolée comme une preuve de déploiement.
- Ne modifie pas silencieusement les contrats antérieurs.
- Ne commence pas le développement des nouvelles fonctionnalités.

Tu peux créer ou mettre à jour les documents de conception nécessaires, en préservant leur historique et en rendant les modifications explicites.

La production de tous les diagrammes détaillés n'est pas nécessairement requise dans cette première intervention. En revanche, **leur production et leur validation doivent être établies comme conditions obligatoires avant toute implantation de chacun des use cases**.

## 11. Résultat attendu

Je veux obtenir une architecture C consolidée, sans duplication inutile, accompagnée d'un processus rigoureux permettant de passer progressivement des exigences fonctionnelles à une conception UML validée, puis à son implantation.

Le principe de gouvernance est le suivant :

**Un use case ne devient implantable que lorsque ses comportements, ses interactions, ses structures de données et ses responsabilités logicielles ont été décrits, vérifiés et approuvés.**

Commence par l'analyse d'impact, l'intégration des décisions et le plan de validation. Signale les arbitrages résiduels au lieu de les prendre à ma place.