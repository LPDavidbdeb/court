# UC-C-11 — Figer une version et ses révisions probatoires exactes

**Complément C-TRANS-2026-10-21-R1 — L5.** US-C-11; D08/CF3-D5; mandat A/B/C.
Acteur : l’utilisateur humain unique (rédacteur, relecteur ou lecteur selon
l’opération). [Contrat transversal](../../MODELE_TRANSVERSAL_C.md).

Ce complément précise les invariants du dossier existant à spécifier/modéliser;
il ne constitue pas un quadruplet UML ni une attestation de validation.
[Statut faisant autorité](../../registre_validation.md). Les exigences
antérieures du plan et de la story restent applicables.

| Critère transversal | Résultat attendu |
|---|---|
| TRV11-AC01 | Le gel conserve et protège la révision exacte de chaque preuve utilisée, les sélections/nœuds, les états documentaires/citations et les liens pertinents vers les versions cibles exactes. Les fondements historiques restent consultables après modification de brouillons. |
| TRV11-AC02 | Entrées recontrôlées et stockage garanti avant finalisation; aucun FIGEE partiel. Immutabilité des décisions déjà conservées distincte de ce verrouillage global. Répétition idempotente, aucune notification/communication/dépôt implicite. |

**Parcours et refus :** Préparer ResultatVersion et fichiers → acquérir les protections et recontrôler l’ensemble des entrées/révisions/renvois pertinents → vérifier leur clôture et les fichiers → conserver le contenu canonique et rendre les révisions engagées immuables → publier FIGEE. Panne ou mutation concurrente : pas de FIGEE incomplet. Une modification ultérieure ouvre une autre VersionActe et, si nécessaire, une autre révision de preuve.

**Dépendances et limites :** UC01A/03/04/06/09/10/16/18A; R08 stockage et finalisation. Une version cible CF2 déjà figée fournit sa propre histoire; pas de pointeur vers sa dernière version. Les nouvelles associations exactes doivent être protégées contre ORM/bulk/SQL/suppressions selon les droits définis.

Scénarios TRV:T02/T05/T06/T08/T12; COT:T06 : **NON EXECUTES**. Séquences, ERD et classes locaux restent à produire et à rapprocher des responsabilités du modèle transversal. Aucun développement autorisé.
