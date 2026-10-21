# UC-C-01B — Ouvrir une nouvelle version depuis un état figé

**Complément C-TRANS-2026-10-21-R1 — L5/L6.** US-C-01/11; D08/CF3; mandat A/B.
Acteur : l’utilisateur humain unique (rédacteur, relecteur ou lecteur selon
l’opération). [Contrat transversal](../../MODELE_TRANSVERSAL_C.md).

Ce complément précise les invariants du dossier existant à spécifier/modéliser;
il ne constitue pas un quadruplet UML ni une attestation de validation.
[Statut faisant autorité](../../registre_validation.md). Les exigences
antérieures du plan et de la story restent applicables.

| Critère transversal | Résultat attendu |
|---|---|
| TRV01B-AC01 | Modifier une version FIGEE crée une nouvelle VersionActe BROUILLON, son Document propre et la filiation. Le contenu source reste inchangé; les révisions de preuve identiques peuvent être réutilisées par des usages destination explicites, sans nouveau partage de texte privé PRODUCED. |

**Parcours et refus :** Choisir la version source exacte → décider le périmètre et les usages → créer de nouvelles occurrences et textes privés selon ST-R1 → réutiliser les révisions de preuve inchangées ou créer leurs nouvelles révisions complètes si une modification est décidée → conserver les cartes de filiation. Toute destination figée est refusée.

**Dépendances et limites :** UC01A/07/11; R06; interface de lecture historique disponible avant implantation globale du gel. La filiation ne réexamine ni ne reconfirme automatiquement les appuis.

Scénarios TRV:T02/T05 : **NON EXECUTES**. Séquences, ERD et classes locaux restent à produire et à rapprocher des responsabilités du modèle transversal. Aucun développement autorisé.
