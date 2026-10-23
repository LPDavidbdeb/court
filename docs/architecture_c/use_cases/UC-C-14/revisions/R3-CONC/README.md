# UC14 — Révision R3-CONC avant correction

**23 octobre 2026 — conception proposée, aucune autorisation d'implantation.**
Cette révision traite uniquement la fenêtre résiduelle entre `pre_delete` et
le `DELETE` SQL constatée dans la [revue indépendante B01](../../../../lots/C0-A/REVUE_INDEPENDANTE_B01.md#4-blocage-résiduel-uc14--état-changé-après-la-garde).
Le candidat `f35ec85` reste **NON CONFORME**. Aucun résultat de test de cette
ancienne livraison n'est attribué au mécanisme proposé.

La protection recommandée combine un plan d'état attendu, des verrous locaux
conservés jusqu'au commit externe, une relecture sous protection et une
sauvegarde des instances existantes sans réinsertion implicite. Les parents
dont Treebeard modifie les compteurs et les textes Statement archivés sont
inclus dans les protections nécessaires. Le contrat UC14 AC01–AC07 et les
décisions C14-D1/D2 restent inchangés.

| Vue | Rendu | Source | Objet |
|---|---|---|---|
| Séquence principale | [SVG](sequence.svg) | [PlantUML](sequence.puml) | T1/T2, deux ordres sûrs, attente jusqu'au commit, refus sans résurrection |
| Activité UC14 | [SVG](activity.svg) | [PlantUML](activity.puml) | Précontrôles, protection, archives, gardes, annulation |
| Classes / services | [SVG](class.svg) | [PlantUML](class.puml) | Responsabilités et opérations proposées, sans table nouvelle |
| ERD conservé | [SVG](erd.svg) | [PlantUML](erd.puml) | ERD R2-HIST inchangé sur le fond; seul chemin d'inclusion adapté |
| Annulation et reprise T2 | [SVG](sequence_rollback.svg) | [PlantUML](sequence_rollback.puml) | Rollback T1, libération des protections, effets indépendants |
| Plusieurs occurrences | [SVG](sequence_multiple.svg) | [PlantUML](sequence_multiple.puml) | Ordre des verrous, parents, refus global et risque de deadlock |
| Activité de l'écriture T2 | [SVG](activity_t2.svg) | [PlantUML](activity_t2.puml) | Impact technique UC13 et sauvegarde ORM périmée |

Les sept PNG homonymes sont également conservés. La séquence principale
renvoie aux deux séquences complémentaires pour rester lisible. L'activité
T2 complète les vues partagées sans remplacer silencieusement UC13 R2-ST.

Lire la [spécification limitée](specification.md), l'[analyse du défaut et
de cohérence](analyse_coherence.md), le [plan de contre-épreuves](plan_tests.md),
la [traçabilité](tracabilite.md) et la [revue indépendante](validation.md).
Les [empreintes de conception](manifest_conception.json) identifient les
artefacts présentés à la revue; les [contrôles documentaires](controles_documentaires.json)
consignent ce qui a réellement été vérifié.

## Décision attendue et périmètre proposé

Cette livraison prépare l'étape UML préalable demandée par l'utilisateur.
La revue indépendante de conception ne vaut ni exécution des contre-épreuves
PostgreSQL, ni levée de B01, ni approbation utilisateur.

Après validation de la conception et **approbation explicite de l'utilisateur**,
seule la correction isolée décrite au §6 de l'[analyse](analyse_coherence.md)
pourra être engagée : services/gardes locaux, sauvegarde des instances
LibraryNode existantes, voie d'édition HTTP et tests associés. Ni migration,
ni arbre global, ni ajout UC02, ni lot suivant. Aucun commit, push, merge,
déploiement, accès à la base réelle ou modification du banc A dans ce dossier.

Les [versions approuvées](../../../../versions_approuvees/UC-C-14_C0A-UML-R2-HIST/README.md),
leurs manifestes et les anciennes vues locales restent conservés à l'identique.
R3-CONC est une version à examiner distinctement; l'approbation de R2 ne lui
est pas transférée. Le [registre unique](../../../../registre_validation.md)
porte ce suivi par version.
