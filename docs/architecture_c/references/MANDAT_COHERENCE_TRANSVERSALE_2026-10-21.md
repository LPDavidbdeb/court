# Agent B — Validation transversale de la cohérence de l'architecture C

## 1. Objectif

Nous souhaitons nous assurer que les décisions fonctionnelles du Product Owner sont représentées de façon cohérente dans l'ensemble du projet :

- User stories et critères d'acceptation;
- Use cases et spécifications;
- Diagrammes UML transversaux et locaux;
- Modèle de données;
- Matrice de couverture;
- Backlog et dépendances des lots;
- Contrats de développement et scénarios de validation.

Cette vérification complète ton mandat actuel sur le versionnement des actes et des arbres de preuve. Elle ne le remplace pas et ne doit pas interrompre inutilement ton travail en cours.

**Notre objectif est d'éviter qu'une décision correctement intégrée à un document soit absente ou contredite ailleurs dans l'architecture.**

## 2. Références existantes

Utilise les documents faisant déjà autorité, notamment :

- `DECISIONS_ARCHITECTURE_C_CONSOLIDEES.md`
- `AVENANT_ARCHITECTURE_C.md`
- `MODELE_TRANSVERSAL_COTATION.md`
- `MATRICE_COUVERTURE_V2_C.md`
- `PLAN_MODELISATION_UML.md`
- `BACKLOG_ARCHITECTURE_C.md`
- `PROTOCOLE_VALIDATION_UML.md`
- `registre_validation.md`
- Les spécifications et diagrammes des use cases concernés.

Réutilise les structures de traçabilité existantes. Ne crée pas un deuxième backlog, un registre parallèle ou un nouveau processus de gouvernance.

## 3. Décisions fonctionnelles à vérifier

### A. Hiérarchie des actes

`Cause → Acte → VersionActe`

Une cause contient plusieurs actes; un acte peut posséder plusieurs versions.

Une version en rédaction est modifiable. Une version figée conserve son état rédactionnel, documentaire et probatoire.

La modification d'un acte figé nécessite une nouvelle version.

Les événements de notification, communication et dépôt sont distincts du gel.

### B. Versionnement des arbres de preuve

Les arbres de preuve possèdent une identité durable et peuvent avoir plusieurs révisions.

Une VersionActe figée conserve les révisions exactes des arbres qu'elle utilise, y compris les dépendances et renvois pertinents.

Les versions historiques ne doivent pas pouvoir être modifiées indirectement.

Une même révision de preuve peut être réutilisée par plusieurs versions d'actes.

### C. Sources, documents, citations et cotation

Le Product Owner a définitivement décidé :

**La cote principale appartient au document source et les sous-cotes appartiennent aux citations de ce document.**

Dans une VersionActe :

- Chaque document retenu au bordereau reçoit une cote principale.
- Les citations sélectionnées reçoivent des sous-cotes liées à leur document.
- Un document retenu sans citation reçoit une cote principale et zéro sous-cote.
- Les identités intrinsèques des documents et citations demeurent indépendantes des cotes.
- Les cotes et sous-cotes sont calculées par l'autorité commune du bordereau et du ResultatVersion.
- Le gel conserve les associations exactes.

Cette décision est déjà intégrée à UC08/09/16/17 et au modèle transversal de cotation. Vérifie désormais sa compatibilité avec les autres use cases et diagrammes.

La notation et l'ordonnancement des sous-cotes demeurent à préciser; ne les considère pas comme déjà approuvés.

### D. Concordances entre versions

Le système doit produire les deux concordances promises entre la demande déposée le 24 juillet 2026 et la demande modifiée :

1. Concordance des paragraphes.
2. Concordance des cotes des pièces.

La comparaison doit utiliser les états historiques conservés, sans reconstruire rétrospectivement des informations qui n'ont pas été attestées.

Le versionnement des arbres de preuve doit également permettre de retrouver les fondements probatoires exacts de chaque version.

### E. Mono-utilisateur

L'application est destinée à un seul utilisateur humain.

Ne prévois aucune fonctionnalité collaborative inutile. Conserve seulement les protections nécessaires contre les incohérences résultant d'opérations techniques concurrentes.

## 4. Vérification de cohérence

Effectue deux contrôles complémentaires.

**Cohérence verticale**

Pour chaque décision métier importante, vérifie la chaîne :

`Décision → User Story → Critère → Use Case → Diagrammes → Scénarios → Lot`

Identifie les exigences absentes, ambiguës ou insuffisamment couvertes.

**Cohérence horizontale**

Vérifie que les différents diagrammes décrivent des règles compatibles :

- Le State Diagram de VersionActe doit correspondre aux règles de mutation et d'immutabilité représentées dans l'ERD et les séquences.
- Le State Diagram des versions de preuve doit être compatible avec UC03/04/11.
- Les relations de cotation des documents et citations doivent être identiques dans UC08/09/16/17 et le modèle transversal.
- Les opérations des Sequence Diagrams doivent correspondre aux responsabilités des Class Diagrams.
- Les transitions et opérations de gel doivent conserver toutes les relations nécessaires à la concordance.
- Les cardinalités et identités doivent être compatibles entre les ERD locaux et le modèle global.

La simple présence de diagrammes ou leur compilation correcte ne constitue pas une preuve de cohérence.

## 5. Analyse d'impact et corrections

Pour chaque contradiction ou lacune significative :

1. Identifie la décision ou l'exigence concernée.
2. Localise les artefacts touchés.
3. Explique la contradiction et sa conséquence fonctionnelle.
4. Propose la correction minimale.
5. Détermine si elle exige un arbitrage du Product Owner ou constitue une simple mise en cohérence technique.
6. Identifie les diagrammes, critères et lots qui devront être revalidés.

Privilégie les modifications des user stories et use cases existants.

Ne crée de nouveau use case que si une capacité fonctionnelle réellement distincte n'est pas couverte.

Ne modifie pas silencieusement une décision approuvée ni les versions UML contractuelles de C0-A.

## 6. Intégration au backlog

Les exigences de versionnement des actes et des arbres de preuve doivent être explicitement rattachées aux lots de développement qui en dépendent.

En particulier, vérifie que les fondations requises sont conçues et approuvées avant les développements de L1-A, L2 et des mécanismes de cotation, production et gel.

Distingue les dépendances de conception des dépendances d'implantation. La nécessité de définir une interface future ne signifie pas que tout le lot futur doit déjà être développé.

## 7. Livrables

À la fin de ton mandat actuel, fournis :

**A. Les trois modèles transversaux demandés**

- State Diagram de VersionActe;
- State Diagram des versions d'arbres de preuve;
- ERD transversal Cause / Acte / VersionActe / Preuve, intégrant la cotation documentaire.

Avec leurs sources PlantUML, rendus et invariants essentiels.

**B. Une matrice synthétique de cohérence**

Pour chaque exigence transversale importante, indique :

