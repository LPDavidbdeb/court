# Agent B — Approbation d'UC-C-13 R2-ST et poursuite de la validation UML de C0-A

## 1. Décision d'approbation

J'ai fait examiner les quatre diagrammes UML d'UC-C-13 R2, ainsi que les deux modèles consolidés, à partir de leur publication sur GitHub.

L'examen a notamment confirmé :

- La suppression de la modification directe d'un `Statement` dans le profil C0-A.
- La création systématique d'un nouveau `Statement` lorsqu'une occurrence éditable reçoit un texte réellement différent.
- Le maintien de l'ancien `Statement` et la préservation des autres occurrences.
- L'atomicité des captures, de la création, du repointage et de la modification de `item`.
- La distinction entre les garanties apportées par C0-A et celles qui restent à implanter dans L1-A.
- La cohérence des diagrammes locaux avec les modèles UML consolidés.

**J'APPROUVE EXPRESSÉMENT le sous-cas `UC-C-13::C0A_ISOLER`, dans sa version `C0A-UML-R2-ST`.**

Cette approbation porte exclusivement sur le dossier identifié dans la publication GitHub :

- PR : `#30`
- Commit de fusion : `cd584c3`
- Dossier : `docs/architecture_c/use_cases/UC-C-13/`
- Modèle global : `G-C0A-R2-ST`
- Version exacte identifiée par `manifest_sha256.json`

Les invariants fonctionnels ST01–ST05 demeurent acquis.

Cette approbation ne comprend pas :

- Le mécanisme permanent de provenance et de propriété proposé pour L1-A.
- L'activation de la modification directe d'un `Statement` privé.
- L'approbation des dossiers UC-C-14 et UC-C-15.
- L'approbation du patch C0-A dans son état actuel.
- L'autorisation de développement, de fusion ou de migration.

## 2. Enregistrer durablement l'approbation

Conformément à notre gouvernance, je veux que cette décision soit inscrite dans les artefacts persistants du projet.

Mets à jour :

1. Le registre de validation UML.
2. Le dossier de validation d'UC-C-13.
3. Le backlog, si son état doit être ajusté.
4. Les références de traçabilité pertinentes.

La décision doit conserver la date, l'identifiant du sous-cas, la version approuvée, le commit Git de référence et son périmètre exact.

Le statut `APPROUVE_UTILISATEUR` est autorisé pour **ce seul sous-cas**. Le statut `PRET_DEVELOPPEMENT` ne doit pas être attribué automatiquement : les dépendances et conditions du lot C0-A restent à satisfaire.

**Ne modifie pas le contenu fonctionnel des quatre diagrammes approuvés.** Toute évolution ultérieure affectant leur contrat devra produire une nouvelle version et une nouvelle demande d'approbation.

Prépare un commit documentaire distinct, sans inclure les travaux non liés. Sa publication suivra le processus de changement du projet; aucune modification du code applicatif n'est autorisée.

## 3. Poursuivre avec UC-C-14 et UC-C-15

La prochaine priorité est désormais la validation graphique des deux autres dossiers nécessaires à C0-A.

Je souhaite recevoir, pour chacun :

- La spécification fonctionnelle.
- Les quatre diagrammes UML PlantUML.
- Les rendus SVG et PNG.
- La traçabilité entre critères, diagrammes et tests.
- L'attestation architecturale de l'Agent B.
- Les éventuelles réserves nécessitant mon arbitrage.

**Les diagrammes constituent les artefacts centraux de conception.**

Toute correction à une spécification doit se traduire dans les vues UML concernées, avec une mise à jour des modèles consolidés lorsque nécessaire.

Le prochain examen portera sur les diagrammes réels, et non uniquement sur une synthèse textuelle.

## 4. Questions fonctionnelles à régler dans ces dossiers

### A. Édition de `item` pour une occurrence portant une citation

L'Agent A a constaté que le patch refuse toute modification d'une occurrence portant une citation, même lorsque seul son intitulé `item` est modifié.

Je souhaite distinguer explicitement :

- La modification du contenu probatoire, qui ne doit pas altérer la source.
- La modification des propriétés rédactionnelles d'une occurrence `PRODUCED` éditable.
- La protection intégrale des occurrences `REPRODUCED` et des occurrences historiques protégées.

Détermine quel use case possède cette responsabilité.

Si une occurrence `PRODUCED` non protégée peut modifier `item` sans toucher au texte de la citation, ce comportement doit être représenté dans l'activité, la séquence et les responsabilités logicielles concernées.

Distingue également le simple changement d'intitulé des changements susceptibles d'affecter la numérotation, le rôle ou la portée d'un examen.

Soumets-moi tout arbitrage fonctionnel nécessaire; ne considère pas la règle actuelle HTTP 403 comme approuvée par défaut.

### B. Concordances devenues « à réexaminer »

L'Agent A a identifié un comportement dans lequel une concordance portant une citation devient « à réexaminer » sans possibilité apparente de reconfirmation.

Vérifie le contrat applicable :

- Conditions de péremption d'un examen.
- Possibilité d'effectuer un nouvel examen.
- Conservation des décisions antérieures.
- Distinction entre une source inadmissible et une décision simplement devenue périmée.

Représente les transitions d'état et leur traitement dans les diagrammes concernés.

### C. Anomalie C0A-REV-01

La lecture des appuis d'origine ne doit pas perdre les appuis valides lorsqu'un autre référent du même ensemble est invalide.

Le modèle cible doit distinguer :

- Les appuis valides conservés.
- Les anomalies identifiées.
- Les erreurs globales empêchant la lecture.
- Les conditions empêchant de considérer une consultation incomplète comme un résultat strictement validé.

Cette correction doit être matérialisée dans UC-C-15 et dans les modèles globaux concernés.

## 5. Maintenir la conception et le suivi synchronisés

La gouvernance que j'ai instaurée vise à obtenir une architecture **concrète, graphique, persistante et évolutive**.

Je veux donc que chaque décision significative suive cette chaîne :

**Décision fonctionnelle → analyse d'impact → mise à jour des UML → validation architecturale → examen graphique → approbation utilisateur → implantation par A → contrôle de conformité.**

Les sources `.puml`, leurs rendus, les contrats et les versions approuvées doivent demeurer consultables dans Git.

Le backlog doit refléter l'état de ces travaux, sans remplacer les diagrammes comme référence de conception.

## 6. Prochaine livraison attendue

Après l'enregistrement de l'approbation d'UC-C-13, prépare en priorité :

**A. UC-C-14 — Suppression d'occurrences**

Dossier UML complet, tenant compte de ST01–ST05 et de la conservation des contenus historiques.

**B. UC-C-15 — Consultation des appuis d'origine**

Dossier UML complet, intégrant la correction de C0A-REV-01 et le traitement des diagnostics.

**C. Analyse ciblée des comportements liés aux citations**

Attribution du traitement de `item` et des concordances aux use cases compétents, avec représentation graphique des décisions proposées.

**D. Mise à jour du modèle global C0-A**

ERD et diagramme de classes consolidés, uniquement dans la mesure où les décisions nouvelles les affectent.

Publie les artefacts de conception selon notre processus documentaire afin que je puisse les examiner directement, comme nous venons de le faire pour UC-C-13.

## 7. Limites du mandat

Aucun code applicatif, patch C0-A, migration ou base réelle ne doit être modifié.

Aucune approbation implicite d'UC-C-14 ou UC-C-15 ne doit être enregistrée.

L'Agent A ne reçoit pas encore d'autorisation d'implantation.

**Résultat attendu : enregistrer définitivement l'approbation du profil UC-C-13 R2-ST, puis soumettre UC-C-14 et UC-C-15 à une véritable revue graphique en vue de leur approbation respective.**