# UC-C-01A — Créer un acte et sa première version

**Complément C-TRANS-2026-10-21-R1 — L1-A.** US-C-01; D12/CF1; mandat A/E.
Acteur : l’utilisateur humain unique (rédacteur, relecteur ou lecteur selon
l’opération). [Contrat transversal](../../MODELE_TRANSVERSAL_C.md).

Ce complément précise les invariants du dossier existant à spécifier/modéliser;
il ne constitue pas un quadruplet UML ni une attestation de validation.
[Statut faisant autorité](../../registre_validation.md). Les exigences
antérieures du plan et de la story restent applicables.

| Critère transversal | Résultat attendu |
|---|---|
| TRV01A-AC01 | La Cause contient plusieurs Acte; un Acte est créé avec sa première VersionActe et un Document PRODUCED propre. Les versions supplémentaires appartiennent au même Acte sans remplacer les précédentes. |
| TRV01A-AC02 | Un seul utilisateur humain. Les doubles soumissions, onglets et tâches concurrents respectent la règle R06 approuvée et ne créent ni branche implicite ni objet partiel. Aucun mécanisme collaboratif ajouté. |

**Parcours et refus :** Choisir la Cause et la nature du travail → contrôler le parcours et les entrées → créer atomiquement le contexte et son Document propre → ouvrir BROUILLON. Une analyse interne ne crée aucun événement de dépôt ou d’envoi.

**Dépendances et limites :** R06 pour parcours et brouillons actifs; UC13/14/15 et 05E pour les fondations. Le contrat futur de révision de preuve est défini sans importer proof_manager ni livrer L2.

Scénarios TRV:T01/T13 : **NON EXECUTES**. Séquences, ERD et classes locaux restent à produire et à rapprocher des responsabilités du modèle transversal. Aucun développement autorisé.
