# UC-C-15 — Traçabilité TRANS-04

C0A-UML-R1. Exécution applicative sur `515666e` : **NON EXECUTEE** pour tous
les scénarios. La contre-épreuve en mémoire ne valide pas l’ORM ou l’export.

| Source | AC | Activité | Séquence | ERD | Classes | Scénarios / statut du patch |
|---|---|---|---|---|---|---|
| NR07 | AC01 | ACT-01; restriction couple | SEQ-02/03 | ERD-PAIR; Correspondance.document_source_id/document_cible_id | CLS-PAIR | `C0AFraicheurEtPerimetre.test_lecteur_restreint_au_couple_explicitement_demande`; `test_export_ne_melange_pas_les_appuis_dun_autre_document` présents |
| CF3-26 typé | AC02 | ACT-VALID | SEQ-VALID | ERD-ORIG; LibraryNode.content_type_id/object_id | CLS-TYPE; AppuiDepotJuillet.statement_id | `test_identifiant_generique_ne_designe_pas_un_statement_homonyme`; variante structurel vide; garde présente |
| Mandat revue §5, COV-F-AC01 | AC03 | ACT-DIAG/RESULT | SEQ-DIAG/RESULT | ExtremiteCorrespondance.noeud_id/archive_id et ERD-ORIG | LectureAppuis; itération de concordance | **COV:T-F01 à ajouter** : valide+type invalide, ordre inverse, valide+archive, valide+mauvais Document. Contre-épreuve en mémoire : défaut actuel confirmé |
| Appui historique distinct du courant | AC04 | qualification VERSION SOURCE | SEQ-EXPORT | AppuiDepotJuillet.cote_citee; BordereauDepotJuillet.cote | appuis_dorigine : lecture seule | NR07; comparer comptes ConfirmationAppui avant/après; aucune mutation attendue |
| Couple obligatoire si ambigu | AC05 | ACT-GLOBAL | SEQ-GLOBAL | ERD-PAIR; LibraryNode.document_id | CLS-PAIR | `test_lecteur_sans_couple_refuse_plusieurs_origines_documentaires`; variante document_cible étranger, refus sans lecture étrangère |
| Export sans perte silencieuse | AC06 | ACT-EXPORT | SEQ-EXPORT | AppuiDepotJuillet.entree_id / diagnostics non persistants : aucun nouveau schéma | CLS-LECTURE; export_concordance._ligne + LectureAppuis | COV:T-F01 à ajouter côté export; **patch non conforme AC03/06**; maintien EX01–EX07 à revalider |

Les tests d’anomalie seule et archive seule du patch ne couvrent pas le mélange
exigé. Ni `test_identifiant_generique...` ni `test_archive_non_typee...` ne
démontre la conservation d’appuis valides quand une autre extrémité est invalide.
