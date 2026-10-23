# UC14 R3-CONC — Traçabilité de conception

**23 octobre 2026.** [AC01–AC07 et G01–G10](specification.md) ·
[tests T01–T24 prévus, NON EXECUTES](plan_tests.md).
Les identifiants de messages figurent dans les sources PlantUML et leurs
rendus; les noms de helpers restent proposés.

| Exigence / contrat | Activité | Séquence | Classes / ERD | Tests prévus |
|---|---|---|---|---|
| Bloc exact; B01 initial; G01/G02 | ACT14-PLAN/LOCK/COMPARE | SEQ14-PLAN/LOCK/COMPARE | PlanRetrait, comparer_plan_et_etat | T01/02/13/20 |
| AC01/02, C14-D2; G09 | ACT14-GARDE/TYPE | contrôles avant SEQ14-ARCH | verifier_suppression_noeud / verifier_archivabilite | T04/06/22 |
| AC03, archive exacte; G03 | ACT14-ARCH, textes protégés | Statement sous protection, SEQ14-ARCH | proteger_textes_et_verifier / archiver_noeud; NoeudArchive inchangée | T19/21 |
| Continuité contrôle–DELETE–commit; G04 | ACT14-DUREE/DELETE/COMMIT | SEQ14-DUREE/DELETE/COMMIT | CLS14-DUREE/DELETE; atomic/PostgreSQL | T05/06/12 |
| T2 termine d'abord; G05 | ACT14-COMPARE/REFUS/ROLLBACK | Cas A, SEQ14-COMPARE | PlanRetrait + comparaison | T03/04/13 |
| T2 attend puis refuse; G06 | activité T2, T2-LOCK/NOINSERT | Cas B, SEQ14-ATTENTE/NOINSERT | CLS14-T2/NOINSERT, LibraryNode.save | T05/06/07/08 |
| AC04/06; G07, annulation locale | ACT14-REL/ROLLBACK | sequence_rollback, RB-WRITE/ROLLBACK/REPRISE | orchestration concordance / transaction | T09/10/11 |
| AC05 : aucune purge | ACT14-SUCCES | statements_supprimes vide | CLS14-KEEP; Statement/VersionTexte inchangés | T21/23/24 |
| Plusieurs occurrences et effets indépendants; G08 | Plan complet et refus entier | sequence_multiple, MULTI-LOCK/REFUS/RB/INDEP | ordre PK, parents compris | T13/14/15/16/17/18 |
| UC13 R2-ST conservé; G10 | activity_t2, branche HTTP | T2, captures/COW avant commit | produced_views + detacher_pour_edition | T03/05/09/23/24 |
| AC07, pas de gel global | limite explicite | gardes conservées | note LibraryNode + ERD conservé | T22/24 |
| Aucun changement de schéma | pas de nouvel état persistant | protections transactionnelles | erd.puml R2-HIST, valeurs transitoires dans class.puml | T24 + comparaison documentaire exécutée |

## Continuité avec les validations précédentes

Les [UC13 R2-ST](../../../../versions_approuvees/UC-C-13_C0A-UML-R2-ST/README.md),
[UC14 R2-HIST](../../../../versions_approuvees/UC-C-14_C0A-UML-R2-HIST/README.md)
et [UC15 R2-DIAG](../../../../versions_approuvees/UC-C-15_C0A-UML-R2-DIAG/README.md)
sont préservés, avec leurs sources, rendus, approbations et empreintes.
Cette révision ne réécrit aucune ancienne attestation et ne transfère aucune
approbation à la nouvelle stratégie de concurrence. Les quatre vues UC14 et
l'activité T2 rendent explicite l'impact technique sur UC13. Les critères
fonctionnels approuvés restent les mêmes.

Les autres scénarios NR/CF3, le backlog, la couverture et les modèles
transversaux ne sont ni renumérotés ni requalifiés comme exécutés par ce
dossier. Aucun ticket ni lot nouveau n'est créé. Le [registre unique](../../../../registre_validation.md)
porte le lien vers cette révision; le présent fichier établit uniquement
la correspondance locale entre exigences, vues et essais.
