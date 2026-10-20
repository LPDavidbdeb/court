# UC-C-14 — Traçabilité C0A-UML-R2-HIST

Tous les scénarios applicatifs ci-dessous sont **NON EXECUTES**. Les anciens
tests et 38 scénarios NR/CF3 restent conservés, sans succès nouveau prétendu.
Le contrat sans purge et les refus d’archives insuffisantes restent à approuver.

| Source | AC | Activité | Séquence | ERD | Classes | Scénario attendu / limite |
|---|---|---|---|---|---|---|
| ST01/ST05, NR01/11 | AC01 | ACT14-BLOC/GARDE/REFUS | SEQ14-BLOC/GARDE/REFUS | ReferentHistorique, ConfirmationAppui, AncrageCitation et leurs FK | CLS14-GARDE | C14:T01/T02 : un membre interdit refuse tout le bloc, sans archive. Ancien test suppression_avec_decision_dappui… conservé. |
| Archive fidèle / type qualifié | AC02 | ACT14-TYPE | SEQ14-TYPE | ERD14-GFK; absence de type historique dans NoeudArchive | protection.verifier_archivabilite | C14:T03/T04 : citation HERITE/PHRASE, autre type, objet absent, clé partielle ou PK homonyme : refus sans effet. |
| NR12 partiel | AC03 | ACT14-ARCH | SEQ14-ARCH | ERD14-ARCH; item/path/depth/paragraph_number/texte | CLS14-ARCH | C14:T05 : capturer tous les champs, différencier texte vide vérifié et structure; aucune origine inventée. |
| Filiation / conservation des décisions | AC04 | ACT14-REL/DELETE/HIST | SEQ14-REL/DELETE | ERD14-REL; ExtremiteCorrespondance.noeud/archive; M2M examinées | CLS14-REL/DELETE | C14:T06 : relation via archive, vieux texte/captures/décision inchangés; UC15 signale type non attesté. |
| ST02/ST04/ST05, C14-D1 | AC05 | ACT14-KEEP | SEQ14-KEEP | ERD14-KEEP; Statement et VersionTexte conservés | CLS14-KEEP | C14:T07 : privé apparent, origine inconnue, partagé, appui/capture utiles : aucune purge; pas de droit de nouveau partage. |
| Atomicité NR11 | AC06 | ACT14-TX/ROLLBACK | SEQ14-ROLLBACK | Archives et extrémités restaurées; transaction portée par séquence | CLS14-SERVICE | C14:T08/T09 : échecs après archive, après repointage, après premier retrait; égalité des états avant/après refus. |
| Gardes des référents disponibles | AC07 | ACT14-GARDE/HIST | gardes finales et SEQ14-ROLLBACK | VersionTexte, NoeudArchive, Document; cascades réelles | protection.gardes ORM | C14:T10 : suppression ORM de capture utilisée/archive liée/Document nécessaire refusée; SQL/bulk restent hors garantie. |

## Scénarios à affecter au mandat futur

| ID | Construction / résultat attendu | Lot / exécution |
|---|---|---|
| C14:T01 | REPRODUCED puis référent PRODUCED comme cible ou descendant : refus intégral, captures inchangées. | C0-A; NON EXECUTE |
| C14:T02 | Bloc contenant ConfirmationAppui puis AncrageCitation : aucune cascade de décision ou d’ancrage. | C0-A; NON EXECUTE |
| C14:T03 | Citation courriel/PDF × HERITE/PHRASE et Event de PK homonyme : aucun faux Statement, refus du bloc non archivable. | C0-A; NON EXECUTE |
| C14:T04 | Structure pure autorisée; clé partielle ou objet disparu : refus, sans archive présentée comme fidèle. | C0-A; NON EXECUTE |
| C14:T05 | Statement texte normal puis vide : position/item/numéro/identité conservés; texte vide ne devient pas structure. | C0-A; NON EXECUTE |
| C14:T06 | Occurrence liée archivée : extrémité historique lisible, ancienne décision et VersionTexte intactes; aucun appui courant créé. | C0-A, compléments C0-B; NON EXECUTE |
| C14:T07 | Après retrait de la dernière occurrence, Statement et toutes ses captures restent présents, sans être rendus partageables. | C0-A local, propriété L1-A; NON EXECUTE |
| C14:T08 | Exception à la création de la seconde archive puis au second repointage : rollback des archives déjà créées et des relations. | C0-A; NON EXECUTE |
| C14:T09 | Refus final/exception après le premier delete de nœud : bloc et relations restaurés; erreur HTTP visible. Variante conflit concurrent à éprouver sans promettre sérialisation universelle. | C0-A; NON EXECUTE |
| C14:T10 | Suppressions ORM gardées de capture utilisée/archive liée/Document : refus; preuve distincte de toute garantie SQL/bulk. | C0-A, L1-A/C0-B/L5; NON EXECUTE |

Écart C0A-14-01 : le patch purge encore et admet certains contenus non Statement.
Les résultats P6 ne prouvent pas la conformité au nouveau contrat. Les méthodes
historiques test_suppression_conserve_les_captures_du_statement_devenu_prive,
test_un_identifiant_generique_ne_declenche_pas_la_purge_dun_statement et les
tests de gardes ne sont pas supprimés ou renommés dans ce mandat documentaire.
