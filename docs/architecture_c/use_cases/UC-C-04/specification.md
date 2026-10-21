# UC-C-04 — Sélectionner une révision exacte et ses éléments

**Complément C-TRANS-2026-10-21-R1 — L2/L3-A.** US-C-04; D01/D02; mandat B/C.
Acteur : l’utilisateur humain unique (rédacteur, relecteur ou lecteur selon
l’opération). [Contrat transversal](../../MODELE_TRANSVERSAL_C.md).

Ce complément précise les invariants du dossier existant à spécifier/modéliser;
il ne constitue pas un quadruplet UML ni une attestation de validation.
[Statut faisant autorité](../../registre_validation.md). Les exigences
antérieures du plan et de la story restent applicables.

| Critère transversal | Résultat attendu |
|---|---|
| TRV04-AC01 | Chaque UP valide appartient à l’occurrence de sa VersionActe et désigne une seule révision exacte. Ses sélections appartiennent à cette révision; plusieurs VersionActe peuvent utiliser la même révision sans se modifier indirectement. |

**Parcours et refus :** Choisir occurrence et révision → choisir racines/branches/feuilles → développer seulement cette sélection → vérifier types et contenants → résoudre les éléments documentaires dans ResultatVersion. Refuser nœud étranger, version incompatible, révision devenue obsolète par rapport au plan ou provenance ambiguë sans effet partiel. Une branche non sélectionnée ne devient pas une pièce.

**Dépendances et limites :** UC03/05P; D07/CF4 selon source; R05 pour la production. Les cotes viennent de UC09/16, jamais d’un numéro de révision de preuve. Interface bordereau conçue avant L2, implantation L3-A.

Scénarios TRV:T04/T05/T09; COT:T01/T04/T05 : **NON EXECUTES**. Séquences, ERD et classes locaux restent à produire et à rapprocher des responsabilités du modèle transversal. Aucun développement autorisé.
