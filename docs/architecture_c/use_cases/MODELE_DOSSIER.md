# Gabarit d’un dossier de use case

Référence : [protocole obligatoire](../PROTOCOLE_VALIDATION_UML.md), version C-UML-2026-10-20-R1. Ce gabarit ne constitue pas un dossier validé ni une autorisation.

## specification.md

Indiquer UC-ID, titre, version, date, lot(s), stories et exigences sources; acteur et déclencheur; portée et exclusions; SHA observé et contrats cibles; préconditions; critères `AC01...` avec résultats observables; nominal, variantes, refus et annulation; postconditions; données et invariants; dépendances de contrat, de développement et d’activation; arbitrages avec leur décision ou blocage.

Ne pas renuméroter les IDs sources. Un sous-cas possède son propre identifiant et une référence à son parent fonctionnel, ses frontières et ses quatre vues.

## Quatre vues et éléments traçables

| Fichier obligatoire | Repères attendus |
|---|---|
| `activity.puml` + `.svg` | Identifiants d’activités/conditions et critères couverts |
| `sequence.puml` + `.svg` | Messages repérés, responsables, lectures/écritures, transaction et erreurs |
| `erd.puml` + `.svg` | Clés, attributs, relations, contraintes et statut existant/proposé/à modifier; version du modèle global cible |
| `class.puml` + `.svg` | Opérations responsables des messages et invariants; modèles, services, lectures, rendu et stockage distingués |

Les fichiers ne sont créés que lorsqu’ils contiennent une conception réelle; quatre coquilles vides n’établissent pas la modélisation. Les diagrammes supplémentaires de panne/états sont indexés et validés comme les autres.

## tracabilite.md

| Exigence source | AC local et attendu observable | Activité | Séquence | ERD | Classes | Test source ou nouveau | Contre-épreuve | Exécution |
|---|---|---|---|---|---|---|---|---|
| À renseigner | — | Élément précis | Message précis | Relation/contrainte | Opération/invariant | ID conservé | Refus et état inchangé attendu | NON EXECUTE tant que sans preuve |

Une justification remplace une cellule non pertinente pour un critère; elle ne supprime pas la vue obligatoire. Les références au seul nom de fichier sont insuffisantes.

## validation.md

Conserver les rubriques suivantes et un journal append-only des décisions documentaires :

1. Identification de version du dossier, SHA et empreintes des quatre sources/rendus et inclusions.
2. Contrôle technique par vue : outil/version, commande, date, code retour, SVG, examinateur visuel et observations.
3. Couverture de chaque AC et scénarios : preuves de revue, lacunes et résultats de tests **distincts**.
4. Contrôles architecturaux A1–A8 : résultat motivé, contradictions et corrections.
5. Attestation B : version, portée, date, réserves, statut; aucune attestation globale si un blocage du périmètre subsiste.
6. Décision utilisateur : référence explicite, date, version approuvée, réserves et périmètre. Valeur initiale : **AUCUNE APPROBATION DU DOSSIER**.
7. Préparation du développement : dépendances livrées, environnement autorisé, mandat de lot et fichiers permis; le gabarit ne les remplit pas à la place de l’utilisateur.
8. Conformité après implantation : branche/SHA, diff, tests réellement exécutés, écarts aux vues, décision de correction ou de revalidation.

Tout changement du dossier est inscrit avec impact et nouvelle validation nécessaire. Le statut courant est reporté au [registre](../registre_validation.md).
