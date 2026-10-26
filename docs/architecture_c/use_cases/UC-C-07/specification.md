# UC-C-07 — Reprendre des occurrences et leurs usages décidés

**Complément C-TRANS-2026-10-21-R1 — L2; primitives L1-B, intégration L6.** US-C-07; CF3/CF3-D1–D5; mandat B.
Acteur : l’utilisateur humain unique (rédacteur, relecteur ou lecteur selon
l’opération). [Contrat transversal](../../MODELE_TRANSVERSAL_C.md).

Ce complément précise les invariants du dossier existant à spécifier/modéliser;
il ne constitue pas un quadruplet UML ni une attestation de validation.
[Statut faisant autorité](../../registre_validation.md). Les exigences
antérieures du plan et de la story restent applicables.

| Critère transversal | Résultat attendu |
|---|---|
| TRV07-AC01 | La reprise crée des occurrences et usages destination explicites. Une révision de preuve inchangée est réutilisable; sa modification exige une nouvelle révision entière sous la Preuve durable et une carte de nœuds, sans modifier les versions source ou non ciblées. |

**Parcours et refus :** Construire le plan de reprise, contexte, réserves et prémisses → choisir les usages/révisions/sélections → recontrôler sous transaction → copier les seuls textes et usages décidés → remapper liens/insertions et cartes N:M → exiger les nouveaux examens applicables. Toute erreur annule le plan entier; un élément indisponible n’est pas omis silencieusement.

**Dépendances et limites :** UC02/03/04/05E/05P/06/12; UC08 si insertions et contrat11 si source figée. Texte PRODUCED repris : nouvel objet privé même identique (ST-R1). Une ancienne confirmation ne vaut pas nouvel examen.

Scénarios TRV:T05/T07 : **NON EXECUTES**. Séquences, ERD et classes locaux restent à produire et à rapprocher des responsabilités du modèle transversal. Aucun développement autorisé.
