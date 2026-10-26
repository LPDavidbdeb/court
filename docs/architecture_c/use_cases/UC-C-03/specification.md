# UC-C-03 — Organiser les révisions d’une preuve durable

**Complément C-TRANS-2026-10-21-R1 — L2.** US-C-03; D01/D11/D12; mandat B.
Acteur : l’utilisateur humain unique (rédacteur, relecteur ou lecteur selon
l’opération). [Contrat transversal](../../MODELE_TRANSVERSAL_C.md).

Ce complément précise les invariants du dossier existant à spécifier/modéliser;
il ne constitue pas un quadruplet UML ni une attestation de validation.
[Statut faisant autorité](../../registre_validation.md). Les exigences
antérieures du plan et de la story restent applicables.

| Critère transversal | Résultat attendu |
|---|---|
| TRV03-AC01 | Preuve possède une identité durable et 1..N RevisionPreuve; chaque révision identifie son arbre complet et ses nœuds. Aucun appui, conclusion ou raisonnement autonome ajouté par classement. |
| TRV03-AC02 | Modifier une révision engagée dans un gel, ou affectant des usages non choisis, crée une nouvelle révision complète de la même Preuve avec filiation et carte des nœuds; seuls les usages choisis d’une version modifiable peuvent être repointés. |

**Parcours et refus :** Créer/ouvrir Preuve → choisir la révision exacte → vérifier les usages et la mutabilité → détacher si nécessaire → organiser groupes/feuilles → contrôler structure et références → conserver la révision. Refuser cycle, parent d’une autre révision ou mutation d’une révision immuable. Une feuille vise un document ou une citation avec provenance vérifiée; seul un groupe porte des enfants.

**Dépendances et limites :** UC01A/02; interface de gel UC11 et de sélection UC04 conçue auparavant, sans imposer L5 implanté avant L2. Aucun renvoi récursif entre preuves (D01).

Scénarios TRV:T03/T04/T05 : **NON EXECUTES**. Séquences, ERD et classes locaux restent à produire et à rapprocher des responsabilités du modèle transversal. Aucun développement autorisé.
