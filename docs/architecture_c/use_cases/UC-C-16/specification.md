# UC-C-16 — Documents retenus, citations et compositions

**Complément C-COT-2026-10-21-R1 — L3-A/L4 — US-C-16, V2 US-04.**
Acteur : rédacteur. Déclencheur : résolution des sélections en documents et
citations destinés à la production, avec leurs compositions ordonnées.

[Décision PO](../../references/DECISION_PO_COTATION_DOCUMENT_CITATIONS_2026-10-21.md),
[modèle transversal](../../MODELE_TRANSVERSAL_COTATION.md),
[AC01–AC08 de la story](../../PLAN_MODELISATION_UML.md#us-c-16--composer-les-pièces-produites).
Le dossier reste `A_SPECIFIER`; ce complément substantiel de cotation n’est
ni un quadruplet UML validé ni un mandat de développement.

| Critère complémentaire | Résultat attendu |
|---|---|
| COT16-AC01 | Distinguer identité intrinsèque du document, identité de citation, composition exacte et désignations locales de version |
| COT16-AC02 | Conserver la carte VersionActe → occurrence → utilisation → sélection de document ou citation; vérifier la provenance de chaque citation |
| COT16-AC03 | Plusieurs utilisations/citations d’un document convergent vers sa cote principale unique dans la version, tout en conservant leurs chemins et sous-cotes |
| COT16-AC04 | Des compositions ou assemblages différents restent distincts comme compositions; ils ne créent pas plusieurs cotes principales pour le même document, ni une cote autonome de citation |
| COT16-AC05 | Source entière retenue et citations du même document ne dupliquent pas sa cote; document sans citation reste admissible à la cotation principale |
| COT16-AC06 | La composition et ses états sont conservés séparément des cotes : un changement `[A,B]→[A,C]` reste détectable même si les libellés sont inchangés |

Parcours : développer les seules sélections retenues → identifier les
documents et citations et vérifier leurs liens → conserver usages et
compositions → transmettre les identités au bordereau UC09. Parent ambigu,
sélection d’une autre version ou source non résolue : refus du chemin strict,
sans fusion sur titre/texte/PK seule. Une sélection analytique ne devient pas
automatiquement une production; la décision n’ajoute aucune sélection implicite.

R01/R02 restent limités à la continuité et aux compositions des assemblages;
ils ne rouvrent pas le document comme porteur de cote principale. R05 garde
le périmètre analytique/production; D04/CF4 les contenants et fragments.
Scénarios COT:T01/T03/T04/T05/T07 et tests de composition existants :
**NON EXECUTES**. Aucun nouveau modèle physique imposé.

## Compatibilité avec le versionnement transversal

[Contrat C-TRANS](../../MODELE_TRANSVERSAL_C.md) : les entrées probatoires
proviennent d’UP pointant une révision exacte; les sélections sont développées
dans cette révision (TRV04-AC01). ResultatVersion, bordereau et rendu partagent
ces mêmes entrées. Un état figé conserve révisions, états sources, parents et
associations, sans lecture de l’arbre courant (TRV11-AC01).
Cette précision ne modifie aucun critère COT et ne clôt pas R04 technique.
