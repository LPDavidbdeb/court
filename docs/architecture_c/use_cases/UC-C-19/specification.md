# UC-C-19 — Consigner des événements attestés distincts du gel

**Complément C-TRANS-2026-10-21-R1 — L6.** US-C-19; avenant §6.2; mandat A/E.
Acteur : l’utilisateur humain unique (rédacteur, relecteur ou lecteur selon
l’opération). [Contrat transversal](../../MODELE_TRANSVERSAL_C.md).

Ce complément précise les invariants du dossier existant à spécifier/modéliser;
il ne constitue pas un quadruplet UML ni une attestation de validation.
[Statut faisant autorité](../../registre_validation.md). Les exigences
antérieures du plan et de la story restent applicables.

| Critère transversal | Résultat attendu |
|---|---|
| TRV19-AC01 | Une version peut être figée sans événement, puis notifiée, communiquée et déposée à des moments distincts. Plusieurs événements sont conservés sans changer l’état ni le contenu figé; aucun destinataire, envoi ou fichier transmis inventé pour juillet. |

**Parcours et refus :** Identifier version/livrables ou référent historique attesté → relever événement effectivement survenu et preuves disponibles → ajouter sa trace séparée. Une erreur de relevé exige une correction traçable sans réécrire le contenu figé. Les références historiques papier gardent leurs lacunes, sans créer un dépôt numérique fictif.

**Dépendances et limites :** UC11/18A/18B et modèles Transmission/FichierTransmis à adapter explicitement, sans prétendre qu’ils fournissent déjà le contexte cible. Un utilisateur humain; aucune validation d’équipe requise.

Scénarios TRV:T11/T13; C-UML:T19-01–T19-06 : **NON EXECUTES**. Séquences, ERD et classes locaux restent à produire et à rapprocher des responsabilités du modèle transversal. Aucun développement autorisé.
