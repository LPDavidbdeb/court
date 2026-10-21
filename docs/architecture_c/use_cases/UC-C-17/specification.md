# UC-C-17 — Concordance des documents et citations entre versions

**Complément C-COT-2026-10-21-R1 — L6, contrats L3-A — US-C-17, V2 US-08.**
Acteur : lecteur. Déclencheur : comparaison de deux VersionActe identifiées,
depuis leurs états conservés et l’union de leurs bordereaux.

[Décision PO](../../references/DECISION_PO_COTATION_DOCUMENT_CITATIONS_2026-10-21.md),
[modèle transversal](../../MODELE_TRANSVERSAL_COTATION.md),
[AC01–AC08 de la story](../../PLAN_MODELISATION_UML.md#us-c-17--comparer-les-pièces-entre-versions).
Le dossier demeure `A_SPECIFIER`; les quatre vues et leur validation restent
à produire. Aucun développement autorisé par ce complément.

| Critère complémentaire | Résultat attendu |
|---|---|
| COT17-AC01 | Retrouver un même document par son identité qualifiée malgré une cote principale différente entre les versions |
| COT17-AC02 | Retrouver la même citation par son identité propre et son document parent malgré un changement de sous-cote |
| COT17-AC03 | Exposer les cotes et sous-cotes de chaque version et les utilisations/sélections correspondantes; distinguer recotation, modification de composition, ajout et retrait de citation |
| COT17-AC04 | Ne rapprocher ni documents ni citations sur un libellé seul, une PK sans modèle, un titre ou un texte semblable; signaler tout parent incohérent |
| COT17-AC05 | Comparer les états figés, même après modification du travail courant; aucune recomposition de l’ancien bordereau depuis les relations vivantes |
| COT17-AC06 | Préserver les associations et lacunes attestées de juillet; une sous-cote historique absente reste inconnue, aucune histoire complétée à partir du présent |

Parcours : charger les deux états → comparer les documents par identité →
comparer leurs citations par identité/provenance → exposer séparément cotes,
sous-cotes, compositions et usages. Des scissions/fusions d’assemblages
requièrent toujours une carte N:M explicite; une recotation seule ne les crée
pas. Une capture manquante ou un rapprochement ambigu reste un diagnostic.

Dépendances : UC09/16 pour le contrat des associations, UC11 pour les états
gelés; R01/R02 seulement sur les compositions concernées. Scénarios
COT:T02/T03/T06 et scénarios historiques de concordance : **NON EXECUTES**.

## Compatibilité avec le versionnement transversal

[Contrat C-TRANS](../../MODELE_TRANSVERSAL_C.md) : les entrées probatoires
proviennent d’UP pointant une révision exacte; les sélections sont développées
dans cette révision (TRV04-AC01). ResultatVersion, bordereau et rendu partagent
ces mêmes entrées. Un état figé conserve révisions, états sources, parents et
associations, sans lecture de l’arbre courant (TRV11-AC01).
Cette précision ne modifie aucun critère COT et ne clôt pas R04 technique.

| Critère transversal complémentaire | Résultat attendu |
|---|---|
| TRV17-AC01 | Livrer la concordance des cotes des pièces entre le référent papier du 24 juillet 2026 et la demande modifiée, séparée de la concordance des paragraphes UC12 mais sur le même couple explicitement identifié. Comparer identités de documents/citations, associations/cotes/sous-cotes et compositions attestées; retrouver les révisions probatoires exactes des versions instrumentées. Toute lacune de juillet demeure signalée, sans révision ni examen rétrospectif inventé. |

Scénarios TRV:T09/T10/T12 : **NON EXECUTES**. Les captures héritées et les
cotes de juillet sont des références conservées, pas un ResultatVersion
moderne recréé à partir du présent.
