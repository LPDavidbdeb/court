# UC-C-06 — Conserver les liens rédactionnels et leur contexte exact

**Complément C-TRANS-2026-10-21-R1 — L1-B; gel L5/L6.** US-C-06; CF2; mandat B.
Acteur : l’utilisateur humain unique (rédacteur, relecteur ou lecteur selon
l’opération). [Contrat transversal](../../MODELE_TRANSVERSAL_C.md).

Ce complément précise les invariants du dossier existant à spécifier/modéliser;
il ne constitue pas un quadruplet UML ni une attestation de validation.
[Statut faisant autorité](../../registre_validation.md). Les exigences
antérieures du plan et de la story restent applicables.

| Critère transversal | Résultat attendu |
|---|---|
| TRV06-AC01 | RENVOI et DEPENDANCE_DECLAREE conservent les occurrences et versions exactes concernées. Pour le strict, une prémisse externe mutable exige gel ou reprise explicite; le gel conserve les liens pertinents et le chemin vers les fondements exacts de la version cible figée. |

**Parcours et refus :** Choisir départ/arrivée → qualifier RENVOI ou DEPENDANCE_DECLAREE → contrôler fraîcheur, cible et cycles des dépendances déclarées → conserver le lien. Les renvois de navigation réciproques restent possibles. Une référence à une version externe figée permet de retrouver ses UP/révisions sans importer de sélection ni de conclusion.

**Dépendances et limites :** UC02; interface UC11; aucune dépendance d’implantation de L1-B vers L5. Aucun graphe inter-preuves ni service d’inférence créé. Renvoi manquant diagnostiqué, sans état historique reconstruit.

Scénarios TRV:T06 : **NON EXECUTES**. Séquences, ERD et classes locaux restent à produire et à rapprocher des responsabilités du modèle transversal. Aucun développement autorisé.
